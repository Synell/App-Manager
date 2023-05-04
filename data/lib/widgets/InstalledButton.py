#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel, QMenu, QProgressBar
from PySide6.QtGui import QAction, QMouseEvent, QIcon
from PySide6.QtCore import Qt, Signal, QPoint, QSize, QThread

from data.lib.qtUtils import QGridWidget, QGridFrame, QIconWidget
#----------------------------------------------------------------------

    # Class
class InstalledButton(QGridFrame):
    settings_icon = None
    remove_from_list_icon = None
    edit_icon = None
    show_in_explorer_icon = None
    uninstall_icon = None

    remove_from_list = Signal()
    update_app = Signal()
    uninstall = Signal()
    
    mouse_pressed = Signal()
    edit_clicked = Signal()
    show_in_explorer_clicked = Signal()

    def __init__(self, name: str = '', tag_name: str = '', release: str = '', path: str = '', lang : dict = {}, icon: str = None, compact_mode: bool = False) -> None:
        super().__init__()

        self.icon = QIconWidget(None, icon, QSize(36, 36))
        self.release = release
        self.lang = lang

        self.setFixedHeight(60)
        self.setProperty('color', 'main')

        self.icon_couple = self.widget_icon_couple(self.icon, self.generate_text(compact_mode, name, tag_name, path))
        self.grid_layout.addWidget(self.icon_couple, 0, 0)
        self.grid_layout.setAlignment(self.icon_couple, Qt.AlignmentFlag.AlignLeft)


        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)

        self.grid_layout.addWidget(self.progress_bar, 0, 1)
        self.grid_layout.setAlignment(self.progress_bar, Qt.AlignmentFlag.AlignRight)


        self.update_button = QPushButton()
        self.update_button.setText(lang['QPushButton']['update'])
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.setProperty('color', 'main')
        self.update_button.setProperty('transparent', True)
        self.update_button.setProperty('small', 'true')
        self.update_button.clicked.connect(lambda: self.update_app.emit())
        self.update_button.setVisible(False)

        self.settings_button = QPushButton()
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_button.setProperty('color', 'main')
        self.settings_button.clicked.connect(self.button_click)

        self.button_group = self.widget_couple(4, self.update_button, self.settings_button)

        self.grid_layout.addWidget(self.button_group, 0, 1)
        self.grid_layout.setAlignment(self.button_group, Qt.AlignmentFlag.AlignRight)


    def set_icon(self, icon: str, base_icon: str) -> None:
        self.raw_icon = icon
        if QIconWidget.is_file_icon(self.raw_icon):
            self.icon.icon = base_icon
            self.icon_thread = __IconWorker__(icon)
            self.icon_thread.done.connect(self.icon_loaded)
            self.icon_thread.start()
        else:
            self.icon.icon = icon

    def icon_loaded(self, icon: QIcon) -> None:
        self.icon_thread = None
        self.icon.icon = icon


    def set_update(self, visible: bool) -> None:
        self.progress_bar.setValue(0)
        self.update_button.setVisible(visible)


    def set_disabled(self, disabled: bool) -> None:
        self.progress_bar.setVisible(disabled)
        self.button_group.setVisible(not disabled)
        self.setCursor(Qt.CursorShape.ArrowCursor if disabled else Qt.CursorShape.PointingHandCursor)
        self.setProperty('side', 'all' if disabled else 'all-hover')
        self.setDisabled(disabled)


    def set_compact_mode(self, compact_mode: bool, path: str) -> None:
        self.compact_mode = compact_mode
        self.icon_couple.text_widget.desc.setText(self.small_path(path) if compact_mode else path)


    def set_text(self, name: str, tag_name: str, path: str) -> None:
        self.icon_couple.text_widget.title.setText(f'{name} ({tag_name})')
        self.icon_couple.text_widget.desc.setText(self.small_path(path) if self.compact_mode else path)


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

    def generate_text(self, compact_mode: bool, name: str, tag_name: str, path: str) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(4)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        widget.title = QLabel(f'{name} ({tag_name})')
        widget.title.setProperty('brighttitle', True)
        widget.title.setFixedSize(widget.title.sizeHint())
        widget.grid_layout.addWidget(widget.title, 0, 1)

        widget.desc = QLabel(self.small_path(path) if compact_mode else path)
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
        action_remove.triggered.connect(lambda: self.remove_from_list.emit())
        menu.addAction(action_remove)

        if self.release in ['official', 'prerelease']:
            action_uninstall = QAction(self.lang['QAction']['uninstall'])
            action_uninstall.setIcon(self.uninstall_icon)
            action_uninstall.triggered.connect(lambda: self.uninstall.emit())
            menu.addAction(action_uninstall)

        menu.exec(self.settings_button.mapToGlobal(QPoint(0, 0)))

    def show_in_explorer(self) -> None:
        self.show_in_explorer_clicked.emit()

    def edit(self) -> None:
        self.edit_clicked.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_pressed.emit()
        return super().mousePressEvent(event)

    def progress_changed(self, value: int) -> None:
        self.progress_bar.setValue(value)
#----------------------------------------------------------------------

    # Worker
class __IconWorker__(QThread):
    done = Signal(QIcon)
    def __init__(self, path: str) -> None:
        super(__IconWorker__, self).__init__()

        self.path = path

    def run(self) -> None:
        iw = QIconWidget().file_icon(self.path)
        if iw: self.done.emit(iw)
#----------------------------------------------------------------------
