#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QProgressBar, QLabel
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import os, zipfile, shutil, json, traceback
from urllib.request import urlopen, Request
from datetime import timedelta
from time import process_time

from .InstallButton import InstallButton
from data.lib.qtUtils import QGridFrame, QGridWidget
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        download_progress_changed = pyqtSignal(float)
        install_progress_changed = pyqtSignal(float)
        download_speed_changed = pyqtSignal(float)
        install_speed_changed = pyqtSignal(float)
        download_done = pyqtSignal()
        install_done = pyqtSignal()
        failed = pyqtSignal(str)

class InstallWorker(QThread):
    def __init__(self, data: InstallButton.download_data, download_folder: str = './data/#tmp#', install_folder: str = './data/apps'):
        super(InstallWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.data = data
        self.dest_path = f'{download_folder}/{data.name}'
        self.out_path = f'{install_folder}/{data.name}'

    def run(self):
        try:
            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path)

            filename = self.data.link.split('/')[-1].replace(' ', '_')
            file_path = os.path.join(self.dest_path, filename)
            exclude_path = ['MACOSX', '__MACOSX']

            read_bytes = 0
            chunk_size = 1024
            time = process_time()
            timed_chunk = 0

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
                        timed_chunk += chunk_size

                        deltatime = timedelta(seconds = process_time() - time)
                        if deltatime >= timedelta(milliseconds = 500):
                            self.signals.download_speed_changed.emit(timed_chunk / deltatime.total_seconds())
                            timed_chunk = 0
                            time = process_time()

                        self.signals.download_progress_changed.emit(read_bytes / total)

            self.signals.download_done.emit()
            self.signals.download_speed_changed.emit(-1)

            if not os.path.exists(self.out_path):
                os.makedirs(self.out_path)

            self.zipfile = zipfile.ZipFile(file_path)

            items = self.zipfile.infolist()
            total_n = len(items)
            time = process_time()
            timed_items = 0

            self.signals.install_speed_changed.emit(0)

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in exclude_path):
                    self.zipfile.extract(item, self.out_path)

                self.signals.install_progress_changed.emit(n / total_n)
                timed_items += 1

                deltatime = timedelta(seconds = process_time() - time)
                if deltatime >= timedelta(milliseconds = 500):
                    self.signals.install_speed_changed.emit(timed_items / deltatime.total_seconds())
                    timed_items = 0
                    time = process_time()

            self.zipfile.close()

            manifest = f'{self.out_path}/manifest.json'
            if os.path.exists(manifest):
                with open(manifest, 'r', encoding = 'utf-8') as f:
                    d = json.load(f)
            else: d = {}
            d['release'] = 'pre' if self.data.prerelease else 'official'
            d['tag_name'] = self.data.tag_name
            d['url'] = self.data.link
            file = self.get_file()
            if (not ('command' in d)): d['command'] = f'"{file}"'
            d['created_at'] = self.data.created_at
            if (not ('icon' in d)): d['icon'] = file
            if (not ('cwd' in d)): d['cwd'] = self.out_path

            with open(manifest, 'w', encoding = 'utf-8') as f:
                json.dump(d, f, indent = 4, sort_keys = True, ensure_ascii = False)

            shutil.rmtree(self.dest_path)

            self.signals.install_done.emit()
            self.signals.install_speed_changed.emit(-1)

        except Exception as e:
            print(traceback.format_exc())
            self.signals.failed.emit(str(e))

    def get_file(self) -> str|None:
        for format in ['exe', 'bat']:
                for file in os.listdir(self.out_path):
                    if file.endswith(f'.{format}'):
                        return f'{self.out_path}/{file}'
        return None


class Installer(QGridFrame):
    done = pyqtSignal(str)

    def __init__(self, parent = None, lang: dict = {}, data: InstallButton.download_data = None, download_folder: str = './data/#tmp#', install_folder: str = './data/apps'):
        super(Installer, self).__init__(parent)

        self.lang = lang
        self.data = data
        self.download_folder = download_folder
        self.install_folder = install_folder


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
        self.download_progress.setProperty('class', 'small')
        self.download_progress.setFixedHeight(6)
        self.download_progress.setTextVisible(False)
        self.download_progress.setRange(0, 100)
        widget.grid_layout.addWidget(self.download_progress, 1, 0)

        widget.grid_layout.setRowStretch(2, 1)
        self.grid_layout.addWidget(widget, 2, 0)


        widget = QGridWidget()

        self.install_label = QLabel(f'{self.lang["QLabel"]["install"]} - {self.lang["QLabel"]["waiting"]}')
        label.setProperty('smallbrightnormal', True)
        widget.grid_layout.addWidget(self.install_label, 0, 0)

        self.install_progress = QProgressBar()
        self.install_progress.setProperty('class', 'small')
        self.install_progress.setFixedHeight(6)
        self.install_progress.setTextVisible(False)
        self.install_progress.setRange(0, 100)
        self.install_progress.setValue(0)
        widget.grid_layout.addWidget(self.install_progress, 1, 0)

        widget.grid_layout.setRowStretch(2, 1)
        self.grid_layout.addWidget(widget, 3, 0)


        self.grid_layout.setRowStretch(4, 1)

        self.setProperty('side', 'all')


    def start(self):
        self.iw = InstallWorker(self.data, self.download_folder, self.install_folder)
        self.iw.signals.download_progress_changed.connect(self.download_progress_changed)
        self.iw.signals.install_progress_changed.connect(self.install_progress_changed)
        self.iw.signals.download_speed_changed.connect(self.download_speed_changed)
        self.iw.signals.install_speed_changed.connect(self.install_speed_changed)
        self.iw.signals.download_done.connect(self.download_done)
        self.iw.signals.install_done.connect(self.install_done)
        self.iw.signals.failed.connect(self.failed)
        self.iw.start()

    def convert(self, bytes: float) -> str:
        step_unit = 1024
        units = ['B', 'KB', 'MB', 'GB', 'TB']

        for x in units[:-1]:
            if bytes < step_unit:
                return f'{bytes:.2f} {x}'
            bytes /= step_unit
        return f'{bytes:.2f} {units[-1]}'

    def update_main(self):
        self.main_progress.setValue(int((self.download_progress.value() / 2) + (self.install_progress.value() / 2)))

    def download_progress_changed(self, value: float):
        self.download_progress.setValue(int(value * 100))
        self.update_main()

    def download_speed_changed(self, value: float):
        self.download_label.setText(f'{self.lang["QLabel"]["download"]} - {self.lang["QLabel"]["bytes"].replace("%s", self.convert(value)) if value >= 0 else self.lang["QLabel"]["done"]}')

    def download_done(self):
        self.download_progress.setValue(100)
        self.update_main()

    def install_progress_changed(self, value: float):
        self.install_progress.setValue(int(value * 100))
        self.update_main()

    def install_speed_changed(self, value: float):
        self.install_label.setText(f'{self.lang["QLabel"]["install"]} - ' + self.lang['QLabel']['items'].replace('%s', f'{value:.1f}') if value >= 0 else self.lang['QLabel']['done'])

    def install_done(self):
        self.install_progress.setValue(100)
        self.update_main()
        self.done.emit(f'{self.data.name}')

    def failed(self, message):
        self.done.emit(f'{self.data.name}')
#----------------------------------------------------------------------
