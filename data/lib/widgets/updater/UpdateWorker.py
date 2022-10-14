#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import os, zipfile, shutil, traceback
from urllib.request import urlopen, Request
from datetime import timedelta
from time import sleep
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        download_progress_changed = pyqtSignal(float)
        install_progress_changed = pyqtSignal(float)
        download_speed_changed = pyqtSignal(float)
        install_speed_changed = pyqtSignal(float)
        download_done = pyqtSignal()
        install_done = pyqtSignal()
        install_failed = pyqtSignal(str)

class UpdateWorker(QThread):
    def __init__(self, link: str, token: str, download_folder: str):
        super(UpdateWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.link = link
        self.token = token
        self.dest_path = f'{download_folder}/AppManager'
        self.out_path = f'./temp/'
        self.timer = TimeWorker(timedelta(milliseconds = 500))
        self.timer.time_triggered.connect(self.time_triggered)
        self.speed = 0
        self.timed_chunk = 0
        self.timed_items = 0
        self.install = False
        self.done = False

    def run(self):
        self.timer.start()

        try:
            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path)

            filename = self.link.split('/')[-1].replace(' ', '_')
            file_path = os.path.join(self.dest_path, filename)
            exclude_path = ['MACOSX', '__MACOSX']

            read_bytes = 0
            chunk_size = 1024

            with urlopen(Request(self.link, headers = {'Authorization': f'token {self.token}'}) if self.token else self.link) as r:
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

                        self.signals.download_progress_changed.emit(read_bytes / total)

            self.signals.download_done.emit()
            self.signals.download_speed_changed.emit(-1)

            self.zipfile = zipfile.ZipFile(file_path)

            items = self.zipfile.infolist()
            total_n = len(items)

            self.signals.install_speed_changed.emit(0)
            self.install = True

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in exclude_path):
                    self.zipfile.extract(item, self.out_path)

                self.signals.install_progress_changed.emit(n / total_n)
                self.timed_items += 1

            self.zipfile.close()

            shutil.rmtree(self.dest_path)

            self.signals.install_speed_changed.emit(-1)
            self.signals.install_done.emit()

        except Exception as e:
            print(traceback.format_exc())
            self.signals.install_failed.emit(str(e))

        self.timer.exit(0)
        self.done = True


    def time_triggered(self, deltatime: timedelta):
        if self.done: return

        if not self.install:
            self.signals.download_speed_changed.emit(self.timed_chunk / deltatime.total_seconds())

        else:
            self.signals.install_speed_changed.emit(self.timed_items / deltatime.total_seconds())

        self.timed_chunk = 0



class TimeWorker(QThread):
    time_triggered = pyqtSignal(timedelta)

    def __init__(self, interval: timedelta):
        super(TimeWorker, self).__init__()
        self.interval = interval

    def run(self):
        while True:
            self.time_triggered.emit(self.interval)
            sleep(self.interval.total_seconds())
#----------------------------------------------------------------------
