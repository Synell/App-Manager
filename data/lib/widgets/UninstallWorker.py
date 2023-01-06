#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
import traceback, shutil, os
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        done = Signal(str)
        failed = Signal(str, str)

class UninstallWorker(QThread):
    def __init__(self, parent: QObject = None, path: str = None):
        super(UninstallWorker, self).__init__(parent)
        self.signals = __WorkerSignals__()
        self.path = path

    def run(self):
        try:
            shutil.rmtree(self.path)

            self.signals.done.emit(self.path)

        except Exception as e:
            self.signals.failed.emit(self.path, str(e))
#----------------------------------------------------------------------
