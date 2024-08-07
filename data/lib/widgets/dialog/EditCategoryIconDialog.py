#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize
from data.lib.QtUtils import QFileButton, QFiles, QGridFrame, QGridWidget, QScrollableGridWidget, QFlowScrollableWidget, QIconWidget
import os
#----------------------------------------------------------------------

    # Class
class EditCategoryIconDialog(QDialog):
    icon_file_button_icon = None
    icon_path = None
    icon_size = 64

    def __init__(self, parent = None, lang = {}, raw_icon: str = '') -> None:
        super().__init__(parent)

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.lang = lang
        self.raw_icon = raw_icon

        right_buttons = QGridWidget()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(button, 0, 0)

        button = QPushButton(lang['QPushButton']['apply'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.layout_.addWidget(button, 0, 1)

        self.setWindowTitle(lang['title'])

        self.frame = QGridFrame()
        self.frame.layout_.addWidget(right_buttons, 0, 0)
        self.frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self.frame.layout_.setSpacing(0)
        self.frame.layout_.setContentsMargins(16, 16, 16, 16)
        self.frame.setProperty('border-top', True)
        self.frame.setProperty('border-bottom', True)
        self.frame.setProperty('border-left', True)
        self.frame.setProperty('border-right', True)

        self.root = QScrollableGridWidget()
        self.root.layout_.setSpacing(0)
        self.root.layout_.setContentsMargins(16, 16, 16, 16)

        self.icon_widget = self.icon_tab_widget()
        self.root.layout_.addWidget(self.icon_widget, 0, 0)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

        self._layout.addWidget(self.root, 0, 0)
        self._layout.addWidget(self.frame, 1, 0)

        self.setLayout(self._layout)


        for index, icon in enumerate(['../none.svg'] + os.listdir(self.icon_path)):
            if not icon.endswith('.svg'): continue
            b = self.generate_button(f'{self.icon_path}/{icon}')
            self.icon_widget.bottom.layout_.addWidget(b)

        self.icon_widget.bottom.setFixedHeight(self.icon_widget.bottom.heightMM() - 40) # Cuz weird things happen when resizing the window



    def icon_tab_widget(self) -> QWidget:
        widget = QGridFrame()
        widget.layout_.setSpacing(16)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        widget.top = QGridFrame()
        widget.top.layout_.setSpacing(16)
        widget.top.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(widget.top, root_frame.layout_.count(), 0)

        label = self.textGroup(self.lang['QLabel']['icon']['title'], self.lang['QLabel']['icon']['description'])
        widget.top.layout_.addWidget(label, 0, 0, 1, 2)

        widget.top.icon_group = self.icon_with_text(self.raw_icon, self.lang['QLabel']['currentIcon'])
        widget.top.layout_.addWidget(widget.top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, self.lang['QFileButton']['icon'],
            self.raw_icon,
            self.icon_file_button_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.svg *.ico *.png *.jpg *.jpeg);;SVG (*.svg);;ICO (*.ico);;PNG (*.png);;JPEG (*.jpg *.jpeg)'
        )
        self.icon_button.path_changed.connect(self.icon_file_button_path_changed)
        self.icon_button.setMinimumWidth(int(self.icon_button.sizeHint().width() * 1.25))
        widget.top.layout_.addWidget(self.icon_button, 1, 1)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = self.textGroup(self.lang['QLabel']['predefinedIcons']['title'], self.lang['QLabel']['predefinedIcons']['description'])
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)


        widget.bottom = QFlowScrollableWidget()
        widget.bottom.layout_.setSpacing(16)
        widget.bottom.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(widget.bottom, root_frame.layout_.count(), 0)


        return widget



    def update(self, path: str = None) -> None:
        if not path: return
        if not os.path.isfile(path): return

        self.icon_button.setPath(path)
        self.icon_widget.top.icon_group.icon_widget.icon = path



    def icon_file_button_path_changed(self, path: str = None) -> None:
        if not path: return
        self.update(path)



    def textGroup(self, title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 1, 0)
        widget.layout_.setRowStretch(2, 1)

        return widget



    def icon_with_text(self, icon: str = None, text: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(16)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.layout_.addWidget(label, 0, 0)
        widget.layout_.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = QIconWidget(None, icon, QSize(40, 40), True)
        widget.layout_.addWidget(widget.icon_widget, 1, 0)
        widget.layout_.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.layout_.setRowStretch(2, 1)

        return widget



    def generate_button(self, path: str = None) -> QIconWidget:
        button = QIconWidget(None, path, QSize(self.icon_size, self.icon_size))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('imagebutton', True)
        button.mouseReleaseEvent = lambda _: self.icon_click(os.path.abspath(path))

        return button



    def icon_click(self, path: str = None) -> None:
        if not path: return
        if not os.path.exists(path) or not os.path.isfile(path): return

        self.update(path)



    def exec(self) -> str | None:
        if super().exec():
            if self.icon_button.path(): return self.icon_button.path()

        return None
#----------------------------------------------------------------------
