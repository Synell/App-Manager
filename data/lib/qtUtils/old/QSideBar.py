#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon
from .QScrollableGridWidget import QScrollableGridWidget
from enum import Enum
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class QSideBarSeparator:
    class Shape(Enum):
        NoSeparator = 0
        Line = 1
        DoubleLine = 2
        TripleLine = 3
        DotLine = 4
        DotLineLarge = 5
        SquareDotLine = 6

    def __init__(self, shape = Shape.Line):
        if type(shape) is QSideBarSeparator.Shape:
            self.__shape__ = shape
        else: self.__shape__ = QSideBarSeparator.Shape.Line


    @property
    def shape(self):
        return self.__shape__

    def setShape(self, shape: Shape = Shape.Line):
        if type(shape) is QSideBarSeparator.Shape:
            self.__shape__ = shape
        else: print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a \'QSideBarSeparator.Shape\'.')



class QSideBarItem:
    def __init__(self, displayName: str = 'button', icon: QIcon = None, clickEvent = None):
        self.setDisplayName(displayName)
        self.setIcon(icon)
        self.setClickedEvent(clickEvent)


    def setDisplayName(self, displayName: str = 'button'):
        if type(displayName) is str:
            self.__displayName__ = displayName
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a string.')

    @property
    def displayName(self):
        return self.__displayName__


    def setIcon(self, icon: QIcon = None):
        if type(icon) is QIcon:
            self.__icon__ = icon
        elif icon == None:
            self.__icon__ = QIcon('') #./data/lib/qtUtils/themes/winRounded/dark/icons/sidebar/noIcon.png
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a QIcon.')

    @property
    def icon(self):
        return self.__icon__


    def setClickedEvent(self, clickEvent = None):
        if callable(clickEvent):
            self.__clickEvent__ = clickEvent
        elif clickEvent == None:
            self.__clickEvent__ = self.__uselessFunction__
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a function.')

    @property
    def clickedEvent(self):
        return self.__clickEvent__

    def __uselessFunction__(self):
        pass



class QSideBar(QScrollableGridWidget):
    def __init__(self, parent = None, animation: QEasingCurve.Type = QEasingCurve.Type.InOutCubic, animationTime: int = 500, retractedWidth: int = 60, extendedWidth: int = 300):
        super().__init__()
        self.scrollWidget.setProperty('class', 'QSideBar')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.__items__ = []

        self.setParent(parent)

        self.__extendedWidth__ = extendedWidth

        self.setMinimumWidth(retractedWidth)
        self.setMaximumWidth(retractedWidth)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self.__enterAnimMin__ = QPropertyAnimation(self, b'minimumWidth')
        self.__enterAnimMin__.setEasingCurve(animation)
        self.__enterAnimMin__.setStartValue(retractedWidth)
        self.__enterAnimMin__.setEndValue(extendedWidth)
        self.__enterAnimMin__.setDuration(animationTime)

        self.__enterAnimMax__ = QPropertyAnimation(self, b'maximumWidth')
        self.__enterAnimMax__.setEasingCurve(animation)
        self.__enterAnimMax__.setStartValue(retractedWidth)
        self.__enterAnimMax__.setEndValue(extendedWidth)
        self.__enterAnimMax__.setDuration(animationTime)

        self.__leaveAnimMin__ = QPropertyAnimation(self, b'minimumWidth')
        self.__leaveAnimMin__.setEasingCurve(animation)
        self.__leaveAnimMin__.setStartValue(extendedWidth)
        self.__leaveAnimMin__.setEndValue(retractedWidth)
        self.__leaveAnimMin__.setDuration(animationTime)

        self.__leaveAnimMax__ = QPropertyAnimation(self, b'maximumWidth')
        self.__leaveAnimMax__.setEasingCurve(animation)
        self.__leaveAnimMax__.setStartValue(extendedWidth)
        self.__leaveAnimMax__.setEndValue(retractedWidth)
        self.__leaveAnimMax__.setDuration(animationTime)

        self.installEventFilter(self)

    def addSeparator(self, separator: QSideBarSeparator = QSideBarSeparator()):
        if type(separator) is QSideBarSeparator:
            self.__items__.append(separator)
        else: print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a QSideBarSeparator.')

    def addItem(self, item: QSideBarItem = QSideBarItem()):
        if type(item) is QSideBarItem or type(item) is QSideBarSeparator:
            self.__items__.append(item)
            self.update()
        else: raise ValueError('Argument must be a QSideBarItem.')

    def addItems(self, *items: QSideBarItem):
        for item in items:
            self.addItem(item)

    def insertItem(self, index: int = 0, item: QSideBarItem = QSideBarItem()):
        if (type(item) is QSideBarItem or type(item) is QSideBarSeparator) and type(index) is int:
            self.__items__.append(item)
            self.update()
        else: raise ValueError('Argument must be an integer and a QSideBarItem.')

    def insertItems(self, index: int = 0, *items: QSideBarItem):
        for item in items:
            self.insertItem(index, item)

    def clear(self):
        self.__items__ = []
        self.update()

    def pop(self, index: int = 0):
        if type(index) is int:
            self.__items__.pop(index)
            self.update()
        else: raise ValueError('Argument must be an integer.')

    def getItems(self):
        return self.__items__

    def getItem(self, index: int = 0):
        return self.__items__[index]

    def count(self):
        return len(self.__items__)

    def update(self):
        for i in reversed(range(self.scrollLayout.count())): 
            self.scrollLayout.itemAt(i).widget().deleteLater()

        for index, item in enumerate(self.__items__):
            match item:
                case QSideBarItem():
                    button = QPushButton(item.displayName)
                    button.setProperty('class', 'QSideBar')
                    button.setIcon(item.icon)
                    button.clicked.connect(item.clickedEvent)
                case QSideBarSeparator():
                    match item.shape:
                        case QSideBarSeparator.Shape.NoSeparator: button = QPushButton()
                        case QSideBarSeparator.Shape.Line: button = QPushButton('─' * 25)
                        case QSideBarSeparator.Shape.DoubleLine: button = QPushButton('═' * 25)
                        case QSideBarSeparator.Shape.TripleLine: button = QPushButton('≡' * 25)
                        case QSideBarSeparator.Shape.SquareDotLine: button = QPushButton('┅' * 25)
                        case QSideBarSeparator.Shape.DotLine: button = QPushButton('∙' * 60)
                        case QSideBarSeparator.Shape.DotLineLarge: button = QPushButton('•' * 30)
                    button.setDisabled(True)
                    button.setProperty('class', 'QSideBarSeparator')
                case _: button = QPushButton()

            button.setFixedWidth(self.__extendedWidth__)
            button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.scrollLayout.addWidget(button, index, 0)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Enter.__int__():
            #if self.width() == 60:
                self.__enterAnimMin__.start()
                self.__enterAnimMax__.start()
                self.update()
        elif event.type() == QEvent.Type.Leave.__int__():
            #if self.width() == 300:
                self.__leaveAnimMin__.start()
                self.__leaveAnimMax__.start()
                self.update()

        return super().eventFilter(source, event)
#----------------------------------------------------------------------
