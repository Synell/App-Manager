#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
from datetime import datetime
import traceback, shutil, os, requests
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    received = Signal(dict, str)
    failed = Signal(str)
    finished = Signal()

class RequestWorker(QThread):
    token: str = None

    def __init__(self, parent: QObject = None, followed_apps: list[str] = []):
        super(RequestWorker, self).__init__(parent)
        self.signals = __WorkerSignals__()
        self.followed_apps = followed_apps
        self.time = datetime.now()

    def run(self):
        for app in self.followed_apps:
            try:
                response = requests.get(
                    f'{app.replace("https://github.com/", "https://api.github.com/repos/")}/releases',
                    headers = {'Authorization': f'token {self.token["github"]}'} if self.token['github'] else None
                )

                if response.status_code != 200:
                    self.signals.failed.emit(f'[{response.status_code}] {response.reason}')
                    continue

                response = response.json()

                if type(response) is not list:
                    return self.signals.failed.emit('Invalid response')

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

        self.signals.finished.emit()
#----------------------------------------------------------------------
