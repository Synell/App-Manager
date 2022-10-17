#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from datetime import datetime
import traceback, shutil, os, requests
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    received = pyqtSignal(dict, str)
    failed = pyqtSignal(str)

class RequestWorker(QThread):
    token: str = None

    def __init__(self, followed_apps: list[str] = []):
        super(RequestWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.followed_apps = followed_apps
        self.time = datetime.now()

    def run(self):
        for app in self.followed_apps:
            try:
                response = requests.get(f'{app.replace("https://github.com/", "https://api.github.com/repos/")}/releases', headers = {'Authorization': self.token} if self.token else None)
                if response.status_code != 200: continue
                response = response.json()
                if type(response) is not list: return self.signals.failed.emit('Invalid response')

                name = f'{app.replace("https://github.com/", "").split("/")[-1].replace("-", " ")}'

                official_release = None
                for i in response:
                    if not i['prerelease']:
                        i['name'] = name
                        official_release = i
                        break

                pre_release = None
                for i in response:
                    if i['prerelease']:
                        i['name'] = name
                        pre_release = i
                        break

                if official_release and pre_release:
                    self.signals.received.emit(official_release, app)
                elif official_release:
                    self.signals.received.emit(official_release, app)
                elif pre_release:
                    self.signals.received.emit(pre_release, app)

            except Exception as e:
                self.signals.failed.emit(f'{e}')
#----------------------------------------------------------------------
