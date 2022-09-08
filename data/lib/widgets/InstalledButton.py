#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QLabel, QMenu, QProgressBar
from PyQt6.QtGui import QAction, QMouseEvent, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QSize, QThread
import subprocess, json

from data.lib.qtUtils import QGridWidget, QGridFrame, QIconWidget
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
        self.is_disabled = disabled
        self.compact_mode = compact_mode

        with open(f'{path}/manifest.json', 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            self.release = data['release']
            self.tag_name = data['tag_name'] if data['tag_name'] else 'Custom'
            self.command = data['command']
            self.url = data['url']
            self.icon = QIconWidget(None, icon, QSize(40, 40))
            self.icon_thread = __IconWorker__(data['icon'])
            self.icon_thread.done.connect(self.icon_loaded)

        self.setFixedHeight(60)
        self.setProperty('color', 'main')

        self.icon_couple = self.widget_icon_couple(self.icon, self.generate_text(compact_mode))
        self.grid_layout.addWidget(self.icon_couple, 0, 0)
        self.grid_layout.setAlignment(self.icon_couple, Qt.AlignmentFlag.AlignLeft)


        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)

        self.grid_layout.addWidget(self.progress_bar, 0, 1)
        self.grid_layout.setAlignment(self.progress_bar, Qt.AlignmentFlag.AlignRight)


        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty('side', 'all-hover')

        self.update_button = QPushButton()
        self.update_button.setText(lang['QPushButton']['update'])
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.setProperty('color', 'main')
        self.update_button.setProperty('transparent', True)
        self.update_button.setProperty('small', 'true')
        self.update_button.clicked.connect(lambda: self.update_app.emit(self.path))
        self.update_button.setVisible(False)

        self.settings_button = QPushButton()
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_button.setProperty('color', 'main')
        self.settings_button.clicked.connect(self.button_click)

        self.button_group = self.widget_couple(4, self.update_button, self.settings_button)

        self.grid_layout.addWidget(self.button_group, 0, 1)
        self.grid_layout.setAlignment(self.button_group, Qt.AlignmentFlag.AlignRight)


        self.set_update(self.has_update)
        self.set_disabled(self.is_disabled)

        self.icon_thread.start()


    def icon_loaded(self, icon: QIcon) -> None:
        self.icon.icon = icon


    def set_update(self, has_update: bool) -> None:
        self.has_update = has_update
        self.update_button.setVisible(self.has_update and self.release in ['official', 'prerelease'])


    def set_disabled(self, disabled: bool) -> None:
        self.is_disabled = disabled
        self.progress_bar.setVisible(disabled)
        self.button_group.setVisible(not disabled)
        self.setCursor(Qt.CursorShape.ArrowCursor if disabled else Qt.CursorShape.PointingHandCursor)
        self.setProperty('side', 'all' if disabled else 'all-hover')

    def set_compact_mode(self, compact_mode: bool) -> None:
        self.compact_mode = compact_mode
        self.icon_couple.text_widget.widgets[1].desc.setText(self.small_path(self.path) if compact_mode else self.path)


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

        widget.title = QLabel(f'{self.name} ({self.tag_name})')
        widget.title.setProperty('brighttitle', True)
        widget.title.setFixedSize(widget.title.sizeHint())
        widget.grid_layout.addWidget(widget.title, 0, 1)

        widget.desc = QLabel(self.small_path(self.path) if compact_mode else self.path)
        widget.desc.setProperty('smallbrightnormal', True)
        widget.grid_layout.addWidget(widget.desc, 1, 1)
        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def widget_icon_couple(self, icon: QIconWidget = None, text_widget: QGridWidget = None) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        icon.setFixedSize(40, 40)

        widget.text_widget = text_widget

        widget.grid_layout.addWidget(icon, 0, 0)
        widget.grid_layout.addWidget(text_widget, 0, 1)

        widget.grid_layout.setColumnStretch(2, 1)

        return widget

    def widget_couple(self, spacing = 4, *widgets) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(spacing)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.widgets = list(widgets)

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
        print('edit') #todo

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        try:
            subprocess.Popen(rf'{self.command}')
        except:
            print('oof') #todo

        return super().mousePressEvent(a0)

#----------------------------------------------------------------------

    # Worker
class __IconWorker__(QThread):
    done = pyqtSignal(QIcon)
    def __init__(self, path: str) -> None:
        super(__IconWorker__, self).__init__()

        self.path = path

    def run(self) -> None:
        iw = QIconWidget().file_icon(self.path)
        if iw: self.done.emit(iw)
#----------------------------------------------------------------------
