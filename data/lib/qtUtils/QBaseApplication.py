#----------------------------------------------------------------------

    # Libraries
from sys import argv
from PyQt6.QtWidgets import QApplication, QMainWindow
import os
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class QBaseApplication(QApplication):
    def __init__(self):
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('Base Qt Window')
#----------------------------------------------------------------------
