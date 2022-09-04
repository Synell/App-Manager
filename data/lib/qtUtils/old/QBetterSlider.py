#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QSpinBox, QSlider, QGridLayout, QWidget
from PyQt6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QBetterSlider(QWidget):
    def __init__(self, minimum: int = 0, maximum: int = 100):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setSpacing(1)

        self.__layout__.setColumnStretch(2, 1)
        self.__layout__.setRowStretch(1, 1)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.spinBox = QSpinBox()

        self.setRange(0, 100)
        self.setRange(minimum, maximum)

        self.slider.valueChanged.connect(self.__valueChanged__)
        self.spinBox.valueChanged.connect(self.__valueChanged__)

        self.__layout__.addWidget(self.slider, 0, 0)
        self.__layout__.addWidget(self.spinBox, 0, 1)

    def __valueChanged__(self, value):
        self.spinBox.setValue(value)
        self.slider.setValue(value)

    def setRange(self, minimum: int = 0, maximum: int = 0):
        if minimum > maximum: minimum, maximum = maximum, minimum
        elif minimum == maximum: return

        self.__minimum__ = minimum
        self.__maximum__ = maximum

        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.spinBox.setMinimum(minimum)
        self.spinBox.setMaximum(maximum)

    def range(self):
        return self.__minimum_, self.__maximum__

    def setMinimum(self, minimum: int = 0):
        if minimum > self.__maximum__: return
        elif minimum == self.__maximum__: return

        self.__minimum__ = minimum

        self.slider.setMinimum(minimum)
        self.spinBox.setMinimum(minimum)

    def minimum(self):
        return self.__minimum__

    def setMaximum(self, maximum: int = 0):
        if self.__minimum__ > maximum: return
        elif self.__minimum__ == maximum: return

        self.__maximum__ = maximum

        self.slider.setMaximum(maximum)
        self.spinBox.setMaximum(maximum)

    def maximum(self):
        return self.__maximum__

    def value(self):
        return self.slider.value()

    def setValue(self, value: int = 0):
        if value <= self.__maximum__ and value >= self.__minimum__:
            self.__valueChanged__(value)
#----------------------------------------------------------------------
