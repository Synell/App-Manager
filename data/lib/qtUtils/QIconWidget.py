#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QIcon, QFileSystemModel
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QSize, QFileInfo
import os
from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QIconWidget(QGridFrame):
    def __init__(self, parent = None, icon: str|QPixmap|QSvgWidget|QIcon|None = None, icon_size: QSize = QSize(96, 96), check_file: bool = True) -> None:
        super().__init__(parent)
        self.__icon_size__ = QSize(96, 96)
        self.__check_file__ = False
        self.set(icon, icon_size)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self.setProperty('QIconWidget', True)
        self.update()

    def set(self, icon: str|QPixmap|QSvgWidget|QIcon, size: QSize = 0) -> None:
        self.icon = icon
        self.icon_size = size
        self.update()

    @property
    def icon(self) -> str|QPixmap|QSvgWidget|QIcon:
        return self.__icon__

    @icon.setter
    def icon(self, icon: str|QPixmap|QSvgWidget|QIcon) -> None:
        self.__icon__ = icon
        self.update()

    @property
    def icon_size(self) -> QSize:
        return self.__icon_size__

    @icon_size.setter
    def icon_size(self, size: QSize) -> None:
        self.__icon_size__ = size
        self.update()

    @property
    def check_file(self) -> bool:
        return self.__check_file__

    @check_file.setter
    def check_file(self, check_file: bool) -> None:
        self.__check_file__ = check_file
        self.update()

    @staticmethod
    def file_icon(path: str) -> QIcon:
        file = QFileInfo(path)
        model = QFileSystemModel()
        model.setRootPath(file.path())
        qq = model.iconProvider()
        return qq.icon(file)

    def update(self) -> None:
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        if self.icon:
            if type(self.icon) is QPixmap:
                pixmap = QLabel()
                pixmap.setPixmap(self.icon.scaled(self.icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            elif type(self.icon) is QSvgWidget:
                pixmap = self.icon

            elif type(self.icon) is QIcon:
                pixmap = QLabel()
                pixmap.setPixmap(self.icon.pixmap(self.icon_size))

            elif type(self.icon) is str:
                if os.path.isfile(self.icon):
                    if self.icon.endswith('.svg'): pixmap = QSvgWidget(self.icon)
                    elif self.__check_extension__(self.icon, ['.png', '.jpg', '.jpeg', '.bmp', '.gif']):
                        pmap = QPixmap(self.icon).scaled(self.icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        pixmap = QLabel()
                        pixmap.setPixmap(pmap)

                    elif self.check_file:
                        pixmap = QLabel()
                        pixmap.setPixmap(QIconWidget.file_icon(self.icon).pixmap(self.icon_size))

                    else:
                        pixmap = QSvgWidget()

                else:
                    pixmap = QSvgWidget()

        else:
            pixmap = QSvgWidget()

        pixmap.setFixedSize(self.icon_size)

        self.grid_layout.addWidget(pixmap, 0, 0)

    def __check_extension__(self, path: str, ext: list[str]) -> bool:
        for i in ext:
            if path.endswith(i): return True
        return False
#----------------------------------------------------------------------
