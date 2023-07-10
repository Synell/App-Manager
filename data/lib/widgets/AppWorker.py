#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
import subprocess, psutil
#----------------------------------------------------------------------

    # Class
class AppWorker(QThread):
    class _WorkerSignals(QObject):
        finished = Signal()

    def __init__(self, parent: QObject = None, command: str = '', cwd: str = ''):
        super(AppWorker, self).__init__(parent)
        self.signals = AppWorker._WorkerSignals()
        self._command = command
        self._cwd = cwd
        self._process = None

    @property
    def command(self) -> str:
        return self._command

    @command.setter
    def command(self, value: str) -> None:
        if not self.isRunning():
            self._command = value

    @property
    def cwd(self) -> str:
        return self._cwd

    @cwd.setter
    def cwd(self, value: str) -> None:
        if not self.isRunning():
            self._cwd = value

    def run(self):
        self._process = subprocess.Popen(rf'{self._command}', cwd = rf'{self._cwd}', shell = True)
        self._process.wait()
        self.signals.finished.emit()

    def terminate(self):
        if not self._process: return

        process = psutil.Process(self._process.pid)

        for proc in process.children(recursive = True):
            proc.kill()

        process.kill()

        self._process = None
        super().terminate()
#----------------------------------------------------------------------
