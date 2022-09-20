#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import traceback, shutil, os
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        done = pyqtSignal(str)
        failed = pyqtSignal(str, str)

class UninstallWorker(QThread):
    def __init__(self, path: str = None):
        super(UninstallWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.path = path

    def run(self):
        try:
            shutil.rmtree(self.path)

            self.signals.done.emit(self.path)

        except Exception as e:
            self.signals.failed.emit(self.path, str(e))
#----------------------------------------------------------------------
