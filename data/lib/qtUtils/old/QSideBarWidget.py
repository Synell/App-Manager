#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import QEasingCurve
from .QSideBar import QSideBar
#----------------------------------------------------------------------

    # Class
class QSideBarWidget(QWidget):
    def __init__(self, parent = None, widget: QWidget = None, animation: QEasingCurve.Type = QEasingCurve.Type.InOutCubic, animationTime: int = 500, retractedWidth: int = 60, extendedWidth: int = 300):
        super().__init__(parent)
        self.__layout__ = QGridLayout(self)

        self.sidebar = QSideBar(self, animation = animation, animationTime = animationTime, retractedWidth = retractedWidth, extendedWidth = extendedWidth)
        self.widget = widget

        self.__layout__.setSpacing(0)
        self.__layout__.setContentsMargins(0, 0, 0, 0)

        self.__layout__.addWidget(self.sidebar, 0, 0)
        self.__layout__.addWidget(self.widget, 0, 1)
#----------------------------------------------------------------------
