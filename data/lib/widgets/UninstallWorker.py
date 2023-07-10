#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
import traceback, shutil, os
#----------------------------------------------------------------------

    # Class
class UninstallWorker(QThread):
    class _WorkerSignals(QObject):
        done = Signal(str)
        failed = Signal(str, str)

    def __init__(self, parent: QObject = None, path: str = None):
        super(UninstallWorker, self).__init__(parent)
        self.signals = UninstallWorker._WorkerSignals()
        self.path = path

    def run(self):
        try:
            shutil.rmtree(self.path)

            self.signals.done.emit(self.path)

        except Exception as e:
            self.signals.failed.emit(self.path, str(e))
#----------------------------------------------------------------------
