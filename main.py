#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from math import *
import os, json, zipfile, shutil, traceback, sys, subprocess
from urllib.request import urlopen, Request
from datetime import datetime, timedelta
from app import Application
from data.lib import *
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
            informative_text = str(err),
            icon = QMessageBoxWithWidget.Icon.Critical
        ).exec()
        exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__ if sys.argv[0].endswith('.py') else sys.executable)))

        if os.path.exists('./#tmp#/'):
            try:
                for file in os.listdir('./#tmp#'):
                    shutil.copy(f'./#tmp#/{file}', f'./{file}')
                shutil.rmtree('./#tmp#')

            except: pass

        app = Application()
        app.window.showNormal()
        exit_code = app.exec()
        if (exit_code == 0 and app.must_update):
            ex = 'py main.py' if sys.argv[0].endswith('.py') else f'./{sys.executable}'
            try: subprocess.Popen(rf'{"py updater.py" if sys.argv[0].endswith(".py") else "./Updater"} "{app.must_update}" "{ex}"', creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, cwd = os.getcwd(), shell = False)
            except Exception as e:
                exit_code = 1

        sys.exit(exit_code)

    except Exception as err:
        print(err)
        app = ApplicationError(err)
#----------------------------------------------------------------------
