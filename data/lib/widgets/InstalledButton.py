#----------------------------------------------------------------------

    # Libraries
from collections import namedtuple
from PyQt6.QtWidgets import QPushButton, QLabel, QMenu, QProgressBar
from PyQt6.QtGui import QAction, QIcon, QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtSvgWidgets import QSvgWidget
from .PlatformType import PlatformType
import subprocess, json, os

from data.lib.qtUtils import QGridWidget, QGridFrame
#----------------------------------------------------------------------

    # Class
class InstalledButton(QGridFrame):
    settings_icon = None
    remove_from_list_icon = None
    edit_icon = None
    show_in_explorer_icon = None
    uninstall_icon = None

    remove_from_list = pyqtSignal(str)
    update_app = pyqtSignal(str)
    uninstall = pyqtSignal(str)

    def __init__(self, name: str = '', path: str = '', lang : dict = {}, icon: str = None, disabled: bool = False, has_update: bool = False, compact_mode: bool = False) -> None:
        super().__init__()

        self.name = name
        self.path = path
        self.lang = lang
        self.has_update = has_update
        with open(f'{path}/manifest.json', 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            self.release = data['release']
            self.tag_name = data['tag_name'] if data['tag_name'] else 'Custom'
            self.command = data['command']
            self.url = data['url']

        self.setFixedHeight(60)
        self.setProperty('color', 'main')

        widget = self.widget_icon_couple(icon, self.generate_text(compact_mode))
        self.grid_layout.addWidget(widget, 0, 0)
        self.grid_layout.setAlignment(widget, Qt.AlignmentFlag.AlignLeft)

        # self.mousePressEvent.connect(self.launch_app)

        if disabled:
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)

            self.grid_layout.addWidget(self.progress_bar, 0, 1)
            self.grid_layout.setAlignment(self.progress_bar, Qt.AlignmentFlag.AlignRight)

            self.setProperty('side', 'all')
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setProperty('side', 'all-hover')

            self.update_button = QPushButton()
            self.update_button.setText(lang['QPushButton']['update'])
            self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.update_button.setProperty('color', 'main')
            self.update_button.setProperty('transparent', True)
            self.update_button.setProperty('small', 'true')
            self.update_button.clicked.connect(lambda: self.update_app.emit(self.path))

            self.settings_button = QPushButton()
            self.settings_button.setIcon(self.settings_icon)
            self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.settings_button.setProperty('color', 'main')
            self.settings_button.clicked.connect(self.button_click)

            if self.has_update and self.release in ['official', 'prerelease']:
                button_group = self.widget_couple(4, self.update_button, self.settings_button)

                self.grid_layout.addWidget(button_group, 0, 1)
                self.grid_layout.setAlignment(button_group, Qt.AlignmentFlag.AlignRight)

            else:
                self.grid_layout.addWidget(self.settings_button, 0, 1)
                self.grid_layout.setAlignment(self.settings_button, Qt.AlignmentFlag.AlignRight)


    def small_path(self, path: str) -> str:
        limit = 5
        folders = path.split('/')
        if len(folders) > limit:
            start = ''
            end = ''
            for i in range(limit // 2):
                start += f'{folders[i]}/'
                end = f'/{folders[-i - 1] + end}'
            return f'{start}{(folders[i + 1] + "/") if limit % 2 else ""}...{end}'

        return path

    def generate_text(self, compact_mode: bool) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(4)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f'{self.name} ({self.tag_name})')
        label.setProperty('brighttitle', True)
        label.setFixedSize(label.sizeHint())
        widget.grid_layout.addWidget(label, 0, 1)

        label = QLabel(self.small_path(self.path) if compact_mode else self.path) #self.path.split('/')[0] + '/.../' + self.path.split('/')[-1]
        label.setProperty('smallbrightnormal', True)
        widget.grid_layout.addWidget(label, 1, 1)
        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def widget_icon_couple(self, icon: str = None, text_widget: QGridWidget = None) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        pixmap = QSvgWidget(icon)
        pixmap.setFixedSize(40, 40)

        widget.grid_layout.addWidget(pixmap, 0, 0)
        widget.grid_layout.addWidget(text_widget, 0, 1)

        widget.grid_layout.setColumnStretch(2, 1)

        return widget

    def widget_couple(self, spacing = 4, *widgets) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(spacing)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        i = 0
        for i, widget_ in enumerate(widgets):
            widget.grid_layout.addWidget(widget_, 0, i)

        widget.grid_layout.setColumnStretch(i, 1)

        return widget

    def button_click(self) -> None:
        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        action_showInExplorer = QAction(self.lang['QAction']['showInExplorer'])
        action_showInExplorer.setIcon(self.show_in_explorer_icon)
        action_showInExplorer.triggered.connect(self.show_in_explorer)
        menu.addAction(action_showInExplorer)

        menu.addSeparator()

        action_edit = QAction(self.lang['QAction']['edit'])
        action_edit.setIcon(self.edit_icon)
        action_edit.triggered.connect(self.edit)
        menu.addAction(action_edit)

        menu.addSeparator()

        action_remove = QAction(self.lang['QAction']['removeFromList'])
        action_remove.setIcon(self.remove_from_list_icon)
        action_remove.triggered.connect(lambda: self.remove_from_list.emit(self.path))
        menu.addAction(action_remove)

        action_uninstall = QAction(self.lang['QAction']['uninstall'])
        action_uninstall.setIcon(self.uninstall_icon)
        action_uninstall.triggered.connect(lambda: self.uninstall.emit(self.path))
        menu.addAction(action_uninstall)

        menu.exec(self.settings_button.mapToGlobal(QPoint(0, 0)))

    def show_in_explorer(self) -> None:
        path = self.path.replace('/', '\\')
        subprocess.Popen(rf'explorer /select, "{path}"')

    def edit(self) -> None:
        print('edit')

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        try:
            subprocess.Popen(rf'{self.command}')
        except:
            print('oof')

        return super().mousePressEvent(a0)
#----------------------------------------------------------------------
