#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from PyQt6.QtWidgets import QGridLayout, QWidget, QDialog, QDialogButtonBox, QStyle, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from .QBaseApplication import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QMessageBoxWithWidget(QDialog):
    class Icon(Enum):
        NoIcon = None
        Information = QStyle.StandardPixmap.SP_MessageBoxInformation
        Warning = QStyle.StandardPixmap.SP_MessageBoxWarning
        Critical = QStyle.StandardPixmap.SP_MessageBoxCritical
        About = QStyle.StandardPixmap.SP_MessageBoxQuestion

    def __init__(self, app: QBaseApplication = None, title: str = '', text: str = '', informative_text: str = '', icon: Icon|QIcon = Icon.NoIcon, widget: QWidget = None):
        super().__init__(parent = app.window)
        self.__layout__ = QGridLayout(self)

        self.__left__ = QWidget()
        self.__left_layout__ = QGridLayout(self.__left__)

        self.__right__ = QWidget()
        self.__right_layout__ = QGridLayout(self.__right__)
        self.__right_layout__.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.msg_box_widget = widget

        self.__layout__.addWidget(self.__left__, 0, 0)
        self.__layout__.addWidget(self.__right__, 0, 1)
        if self.msg_box_widget:
            self.__layout__.addWidget(self.msg_box_widget, 1, 0, 1, 2)

        if app:
            match icon:
                case QMessageBoxWithWidget.Icon.Warning: app.beep()
                case QMessageBoxWithWidget.Icon.Critical: app.beep()

        pixmap = QLabel()
        pixmap.setPixmap(self.__generatePixmap__(icon))
        self.__left_layout__.addWidget(pixmap)
        self.__left_layout__.setAlignment(pixmap, Qt.AlignmentFlag.AlignTop)
        self.__left_layout__.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(title)

        text = QLabel(text)
        informative_text = QLabel(informative_text)

        self.__right_layout__.addWidget(text, 0, 0)
        self.__right_layout__.setAlignment(text, Qt.AlignmentFlag.AlignLeft)
        self.__right_layout__.addWidget(informative_text, 1, 0)
        self.__right_layout__.setAlignment(informative_text, Qt.AlignmentFlag.AlignLeft)


        QBtn = QDialogButtonBox.StandardButton.Ok

        self.__buttonBox__ = QDialogButtonBox(QBtn)
        self.__buttonBox__.accepted.connect(self.accept)
        self.__buttonBox__.rejected.connect(self.reject)

        self.__layout__.addWidget(self.__buttonBox__, 2, 1)


    def __generatePixmap__(self, icon: Icon|QIcon = Icon.NoIcon):
        if type(icon) is QMessageBoxWithWidget.Icon:
            style = self.style()
            icon_size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize)
            icon = style.standardIcon(icon.value)
        elif type(icon) is not QIcon:
            return QPixmap()

        if not icon.isNull():
            return icon.pixmap(icon_size)
        return QPixmap()
#----------------------------------------------------------------------
