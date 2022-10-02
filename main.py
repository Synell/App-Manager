#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from sys import exit
from math import *
from data.lib import *
from app import Application
import subprocess, os
#----------------------------------------------------------------------

    # Class
class ApplicationError(QApplication):
    def __init__(self, err: str = ''):
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('App Manager - Error')
        QMessageBoxWithWidget(
            app = self,
            title = 'App Manager - Error',
            text = 'Oups, something went wrong...',
            informativeText = str(err),
            icon = QMessageBoxWithWidget.Icon.Critical
        ).exec()
        exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        app = Application()
        app.window.showNormal()
        exit_code = app.exec()
        if (exit_code == 0 and app.must_update):
            try: subprocess.Popen(rf'./Updater', creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, cwd = os.path.dirname(os.path.abspath(__file__)))
            except: exit_code = 1

        exit(exit_code)

    except Exception as err:
        print(err)
        app = ApplicationError(err)
#----------------------------------------------------------------------
