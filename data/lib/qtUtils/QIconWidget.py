#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
import os
from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QIconWidget(QGridFrame):
    def __init__(self, parent = None, icon: str = None, icon_size: int = 96):
        super().__init__(parent)
        self.__icon_size__ = 96
        self.set_icon(icon, icon_size)

        self.setProperty('QIconWidget', True)
        self.update()

    def set_icon(self, icon: str, size: int = 0) -> None:
        self.__icon__ = icon
        if size > 0: self.__icon_size__ = size
        self.update()

    def update(self) -> None:
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        if self.__icon__:
            if os.path.isfile(self.__icon__):
                if self.__icon__.endswith('.svg'): pixmap = QSvgWidget(self.__icon__)
                else:
                    pmap = QPixmap(self.__icon__).scaled(self.__icon_size__, self.__icon_size__, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    pixmap = QLabel()
                    pixmap.setPixmap(pmap)
            else:
                pixmap = QSvgWidget()
        else:
            pixmap = QSvgWidget()

        pixmap.setFixedSize(self.__icon_size__, self.__icon_size__)

        self.grid_layout.addWidget(pixmap, 0, 0)
#----------------------------------------------------------------------
