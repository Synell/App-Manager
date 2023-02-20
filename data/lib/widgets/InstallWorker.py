#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QProgressBar, QLabel
from PySide6.QtCore import QObject, Signal, QThread
import os, zipfile, shutil, json
from urllib.request import urlopen, Request
from datetime import timedelta
from time import sleep

from .InstallButton import InstallButton
from data.lib.qtUtils import QGridFrame, QGridWidget
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    download_progress_changed = Signal(float)
    install_progress_changed = Signal(float)
    download_speed_changed = Signal(float)
    install_speed_changed = Signal(float)
    download_eta_changed = Signal(timedelta)
    install_eta_changed = Signal(timedelta)
    download_done = Signal()
    install_done = Signal()
    install_failed = Signal(str, int)



class InstallWorker(QThread):
    def __init__(self, parent: QObject, data: InstallButton.download_data, download_folder: str = './data/#tmp#', install_folder: str = './data/apps', check_for_updates: int = 4, auto_update: bool = True) -> None:
        super(InstallWorker, self).__init__(parent)
        self.signals = __WorkerSignals__()
        self.data = data
        self.dest_path = f'{download_folder}/{data.name}'
        self.out_path = f'{install_folder}/{data.name}'
        self.check_for_updates = check_for_updates
        self.auto_update = auto_update
        self.timer = TimeWorker(self, timedelta(milliseconds = 500))
        self.timer.time_triggered.connect(self.time_triggered)
        self.speed = 0
        self.timed_chunk = 0
        self.timed_items = 0
        self.install = False
        self.done = False
        # self.download_left = 0
        # self.install_left = 0
        self.state = 0
        # self.speeds = []
        # self.len_speeds = 4


    def run(self) -> None:
        self.timer.start()

        try:
            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path)

            filename = self.data.link.split('/')[-1].replace(' ', '_')
            file_path = os.path.join(self.dest_path, filename)
            exclude_path = ['MACOSX', '__MACOSX']

            read_bytes = 0
            chunk_size = 1024

            with urlopen(Request(self.data.link, headers = {'Authorization': f'token {self.data.token}'}) if self.data.token else self.data.link) as r:
                total = int(r.info()['Content-Length'])
                with open(file_path, 'ab') as f:
                    self.signals.download_speed_changed.emit(0)
                    while True:
                        chunk = r.read(chunk_size)

                        if chunk is None:
                            continue

                        elif chunk == b'':
                            break

                        f.write(chunk)
                        read_bytes += chunk_size
                        self.timed_chunk += chunk_size

                        # self.download_left = total - read_bytes
                        self.signals.download_progress_changed.emit(read_bytes / total)

            self.signals.download_done.emit()
            self.signals.download_speed_changed.emit(-1)

            if not os.path.exists(self.out_path):
                os.makedirs(self.out_path)

            self.zipfile = zipfile.ZipFile(file_path)

            items = self.zipfile.infolist()
            total_n = len(items)

            self.signals.install_speed_changed.emit(0)
            self.install = True
            self.speeds = []

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in exclude_path):
                    self.zipfile.extract(item, self.out_path)

                # self.install_left = total_n - n
                self.signals.install_progress_changed.emit(n / total_n)
                self.timed_items += 1

            self.zipfile.close()

            self.state = 3

            manifest = f'{self.out_path}/manifest.json'
            if os.path.exists(manifest):
                with open(manifest, 'r', encoding = 'utf-8') as f:
                    d = json.load(f)
            else: d = {}
            d['release'] = 'pre' if self.data.prerelease else 'official'
            d['tag_name'] = self.data.tag_name
            file = self.get_file()
            if (not ('command' in d)): d['command'] = f'"{file}"'
            d['created_at'] = self.data.created_at
            if (not ('icon' in d)): d['icon'] = file
            if (not ('cwd' in d)): d['cwd'] = self.out_path
            if (not ('checkForUpdates' in d)): d['checkForUpdates'] = self.check_for_updates
            if (not ('autoUpdate' in d)): d['autoUpdate'] = self.auto_update
            if (not ('category' in d)): d['category'] = None

            self.state = 4

            with open(manifest, 'w', encoding = 'utf-8') as f:
                json.dump(d, f, indent = 4, sort_keys = True, ensure_ascii = False)

            self.state = 5

            shutil.rmtree(self.dest_path)

            self.signals.install_done.emit()
            self.signals.install_speed_changed.emit(-1)

        except Exception as e:
            self.signals.install_failed.emit(str(e), self.state)

        self.timer.exit(0)
        self.done = True


    def time_triggered(self, deltatime: timedelta) -> None:
        if self.done: return

        if not self.install:
            self.signals.download_speed_changed.emit(self.timed_chunk / deltatime.total_seconds())

        else:
            self.signals.install_speed_changed.emit(self.timed_items / deltatime.total_seconds())

        # if not self.install:
        #     t = self.timed_chunk / deltatime.total_seconds()
        #     self.signals.download_speed_changed.emit(t)

        #     if len(self.speeds) >= self.len_speeds: self.speeds.pop(0)
        #     if t: self.speeds.append(self.download_left / t)
        #     self.signals.download_eta_changed.emit(timedelta(seconds = (sum(self.speeds) / len(self.speeds) if self.speeds else -1)))

        # else:
        #     t = self.timed_items / deltatime.total_seconds()
        #     self.signals.install_speed_changed.emit(t)

        #     if len(self.speeds) >= self.len_speeds: self.speeds.pop(0)
        #     if t: self.speeds.append(self.install_left / t)
        #     self.signals.install_eta_changed.emit(timedelta(seconds = (sum(self.speeds) / len(self.speeds) if self.speeds else -1)))

        self.timed_chunk = 0


    def get_file(self) -> str | None:
        for format in ['exe', 'bat']:
            for file in os.listdir(self.out_path):
                if file.endswith(f'.{format}'):
                    return f'{self.out_path}/{file}'
        return None


    def exit(self, retcode: int = 0) -> None:
        self.timer.exit(retcode)
        if self.timer.isRunning():
            self.timer.terminate()

        return super().exit(retcode)



class TimeWorker(QThread):
    time_triggered = Signal(timedelta)

    def __init__(self, parent: QObject, interval: timedelta) -> None:
        super(TimeWorker, self).__init__(parent)
        self.interval = interval

    def run(self) -> None:
        while True:
            self.time_triggered.emit(self.interval)
            sleep(self.interval.total_seconds())



class Installer(QGridFrame):
    done = Signal(str)
    failed = Signal(str, str)

    def __init__(self, parent = None, lang: dict = {}, data: InstallButton.download_data = None, download_folder: str = './data/#tmp#', install_folder: str = './data/apps', check_for_updates: int = 0, auto_update: bool = False) -> None:
        super(Installer, self).__init__(parent)

        self.lang = lang
        self.data = data
        self.download_folder = download_folder
        self.install_folder = install_folder
        self.check_for_updates = check_for_updates
        self.auto_update = auto_update


        label = QLabel(self.data.name)
        label.setProperty('brighttitle', True)
        self.grid_layout.addWidget(label, 0, 0)

        self.main_progress = QProgressBar()
        self.main_progress.setRange(0, 100)
        self.grid_layout.addWidget(self.main_progress, 1, 0)


        widget = QGridWidget()

        self.download_label = QLabel(f'{self.lang["QLabel"]["download"]} - {self.lang["QLabel"]["waiting"]}')
        self.download_label.setProperty('smallbrightnormal', True)
        widget.grid_layout.addWidget(self.download_label, 0, 0)

        self.download_progress = QProgressBar()
        self.download_progress.setProperty('small', True)
        self.download_progress.setFixedHeight(6)
        self.download_progress.setTextVisible(False)
        self.download_progress.setRange(0, 100)
        widget.grid_layout.addWidget(self.download_progress, 1, 0)

        widget.grid_layout.setRowStretch(2, 1)
        self.grid_layout.addWidget(widget, 2, 0)


        widget = QGridWidget()

        self.install_label = QLabel(f'{self.lang["QLabel"]["install"]} - {self.lang["QLabel"]["waiting"]}')
        self.install_label.setProperty('smallbrightnormal', True)
        widget.grid_layout.addWidget(self.install_label, 0, 0)

        self.install_progress = QProgressBar()
        self.install_progress.setProperty('small', True)
        self.install_progress.setFixedHeight(6)
        self.install_progress.setTextVisible(False)
        self.install_progress.setRange(0, 100)
        self.install_progress.setValue(0)
        widget.grid_layout.addWidget(self.install_progress, 1, 0)

        widget.grid_layout.setRowStretch(2, 1)
        self.grid_layout.addWidget(widget, 3, 0)


        self.grid_layout.setRowStretch(4, 1)

        self.setProperty('side', 'all')


    def start(self) -> None:
        self.iw = InstallWorker(self, self.data, self.download_folder, self.install_folder, self.check_for_updates, self.auto_update)
        self.iw.signals.download_progress_changed.connect(self.download_progress_changed)
        self.iw.signals.install_progress_changed.connect(self.install_progress_changed)
        self.iw.signals.download_speed_changed.connect(self.download_speed_changed)
        self.iw.signals.install_speed_changed.connect(self.install_speed_changed)
        self.iw.signals.download_done.connect(self.download_done)
        self.iw.signals.install_done.connect(self.install_done)
        self.iw.signals.install_failed.connect(self.install_failed)
        self.iw.start()

    def convert(self, bytes: float) -> str:
        step_unit = 1024
        units = ['B', 'KB', 'MB', 'GB', 'TB']

        for x in units[:-1]:
            if bytes < step_unit:
                return f'{bytes:.2f} {x}'
            bytes /= step_unit
        return f'{bytes:.2f} {units[-1]}'

    def update_main(self) -> None:
        self.main_progress.setValue(int((self.download_progress.value() / 2) + (self.install_progress.value() / 2)))

    def download_progress_changed(self, value: float) -> None:
        self.download_progress.setValue(int(value * 100))
        self.update_main()

    def download_speed_changed(self, value: float) -> None:
        self.download_label.setText(f'{self.lang["QLabel"]["download"]} - {self.lang["QLabel"]["bytes"].replace("%s", self.convert(value)) if value >= 0 else self.lang["QLabel"]["done"]}')

    def download_done(self) -> None:
        self.download_progress.setValue(100)
        self.update_main()

    def install_progress_changed(self, value: float) -> None:
        self.install_progress.setValue(int(value * 100))
        self.update_main()

    def install_speed_changed(self, value: float) -> None:
        self.install_label.setText(f'{self.lang["QLabel"]["install"]} - ' + self.lang['QLabel']['items'].replace('%s', f'{value:.1f}') if value >= 0 else self.lang['QLabel']['done'])

    def install_done(self) -> None:
        self.iw.exit()
        self.install_progress.setValue(100)
        self.update_main()
        self.done.emit(f'{self.data.name}')

    def install_failed(self, message: str, exit_code: int) -> None:
        self.iw.exit()
        self.failed.emit(f'{self.data.name}', message)
#----------------------------------------------------------------------
