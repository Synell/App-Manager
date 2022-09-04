#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
#----------------------------------------------------------------------

    # Class
class QDropDownWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text: str = '', widget: QWidget = None):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setSpacing(1)

        self.__layout__.setColumnStretch(1, 1)
        self.__layout__.setRowStretch(2, 1)

        self.__show_hide_button__ = QPushButton(text)
        self.__show_hide_button__.setCheckable(True)
        self.__show_hide_button__.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.__show_hide_button__.setProperty('QDropDownWidget', True)
        self.__show_hide_button__.clicked.connect(self.__show_hide_button_clicked__)

        self.show_hide_widget = widget

        self.__layout__.addWidget(self.__show_hide_button__, 0, 0)
        self.__layout__.setAlignment(self.__show_hide_button__, Qt.AlignmentFlag.AlignRight)
        self.__layout__.addWidget(self.show_hide_widget , 1, 0)

        self.show_hide_widget.hide()

    def __show_hide_button_clicked__(self, event = None):
        if self.__show_hide_button__.isChecked(): self.show_hide_widget.show()
        else: self.show_hide_widget.hide()
        self.clicked.emit()
#----------------------------------------------------------------------
