#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel, QMenu, QProgressBar
from PySide6.QtGui import QAction, QMouseEvent, QIcon
from PySide6.QtCore import Qt, Signal, QPoint, QSize, QThread

from data.lib.QtUtils import QGridWidget, QGridFrame, QIconWidget
#----------------------------------------------------------------------

    # Class
class InstalledButton(QGridFrame):
    class _IconWorker(QThread):
        done = Signal(QIcon)

        def __init__(self, path: str) -> None:
            super(InstalledButton._IconWorker, self).__init__()

            self.path = path

        def run(self) -> None:
            iw = QIconWidget().file_icon(self.path)
            if iw: self.done.emit(iw)


    settings_icon = None
    kill_process_icon = None
    remove_from_list_icon = None
    edit_icon = None
    show_in_explorer_icon = None
    uninstall_icon = None


    kill_process_clicked = Signal()
    remove_from_list_clicked = Signal()
    update_app_clicked = Signal()
    uninstall_clicked = Signal()
    
    mouse_pressed = Signal()
    edit_clicked = Signal()
    show_in_explorer_clicked = Signal()


    def __init__(self, name: str = '', tag_name: str = '', release: str = '', path: str = '', lang : dict = {}, icon: str = None, compact_mode: bool = False, is_running: bool = False) -> None:
        super().__init__()

        self._icon = QIconWidget(None, icon, QSize(36, 36))
        self._release = release
        self._lang = lang
        self._is_running = is_running

        self.setFixedHeight(60)
        self.setProperty('color', 'main')

        self._icon_couple = self.widget_icon_couple(self._icon, self.generate_text(compact_mode, name, tag_name, path))
        self.layout_.addWidget(self._icon_couple, 0, 0)
        self.layout_.setAlignment(self._icon_couple, Qt.AlignmentFlag.AlignLeft)


        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setVisible(False)

        self.layout_.addWidget(self._progress_bar, 0, 1)
        self.layout_.setAlignment(self._progress_bar, Qt.AlignmentFlag.AlignRight)


        self._update_button = QPushButton()
        self._update_button.setText(lang['QPushButton']['update'])
        self._update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_button.setProperty('color', 'main')
        self._update_button.setProperty('transparent', True)
        self._update_button.setProperty('small', 'true')
        self._update_button.clicked.connect(lambda: self.update_app_clicked.emit())
        self._update_button.setVisible(False)

        self._settings_button = QPushButton()
        self._settings_button.setIcon(self.settings_icon)
        self._settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._settings_button.setProperty('color', 'main')
        self._settings_button.clicked.connect(self.button_click)

        self.button_group = self.widget_couple(4, self._update_button, self._settings_button)

        self.layout_.addWidget(self.button_group, 0, 1)
        self.layout_.setAlignment(self.button_group, Qt.AlignmentFlag.AlignRight)

        self.setProperty('running', is_running)


    def set_icon(self, icon: str, base_icon: str) -> None:
        if not icon: return

        self._raw_icon = icon
        if QIconWidget.is_file_icon(self._raw_icon):
            self._icon.icon = base_icon
            self._icon_thread = InstalledButton._IconWorker(icon)
            self._icon_thread.done.connect(self.icon_loaded)
            self._icon_thread.start()
        else:
            self._icon.icon = icon

    def icon_loaded(self, icon: QIcon) -> None:
        self._icon_thread = None
        self._icon.icon = icon


    def set_update(self, visible: bool) -> None:
        self._progress_bar.setValue(0)
        self._update_button.setVisible(visible)


    def set_disabled(self, disabled: bool) -> None:
        self._progress_bar.setVisible(disabled)
        self.button_group.setVisible(not disabled)
        self.setCursor(Qt.CursorShape.ArrowCursor if disabled else Qt.CursorShape.PointingHandCursor)
        self.setProperty('side', 'all' if disabled else 'all-hover')
        self.setDisabled(disabled)


    def set_compact_mode(self, compact_mode: bool, path: str) -> None:
        self.compact_mode = compact_mode
        self._icon_couple.text_widget.desc.setText(self.small_path(path) if compact_mode else path)


    def set_text(self, name: str, tag_name: str, path: str) -> None:
        self._icon_couple.text_widget.title.setText(f'{name} ({tag_name})')
        self._icon_couple.text_widget.desc.setText(self.small_path(path) if self.compact_mode else path)


    def set_is_running(self, is_running: bool) -> None:
        self._is_running = is_running
        self.setProperty('running', is_running)
        self.style().unpolish(self)
        self.style().polish(self)


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
        widget.layout_.setSpacing(4)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        widget.title = QLabel(f'{name} ({tag_name if tag_name else "Custom"})')
        widget.title.setProperty('brighttitle', True)
        widget.title.setFixedSize(widget.title.sizeHint())
        widget.layout_.addWidget(widget.title, 0, 1)

        widget.desc = QLabel(self.small_path(path) if compact_mode else path)
        widget.desc.setProperty('smallbrightnormal', True)
        widget.layout_.addWidget(widget.desc, 1, 1)
        widget.layout_.setRowStretch(2, 1)

        return widget

    def widget_icon_couple(self, icon: QIconWidget = None, text_widget: QGridWidget = None) -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(16)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        icon.setFixedSize(40, 40)

        widget.text_widget = text_widget

        widget.layout_.addWidget(icon, 0, 0)
        widget.layout_.addWidget(text_widget, 0, 1)

        widget.layout_.setColumnStretch(2, 1)

        return widget

    def widget_couple(self, spacing = 4, *widgets) -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(spacing)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        i = 0
        for i, widget_ in enumerate(widgets):
            widget.layout_.addWidget(widget_, 0, i)

        widget.layout_.setColumnStretch(i, 1)

        return widget

    def button_click(self) -> None:
        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        action_showInExplorer = QAction(self._lang['QAction']['showInExplorer'])
        action_showInExplorer.setIcon(self.show_in_explorer_icon)
        action_showInExplorer.triggered.connect(self.show_in_explorer)
        menu.addAction(action_showInExplorer)

        menu.addSeparator()

        action_edit = QAction(self._lang['QAction']['edit'])
        action_edit.setIcon(self.edit_icon)
        action_edit.triggered.connect(self.edit)
        menu.addAction(action_edit)

        if self._is_running:
            menu.addSeparator()

            action_kill = QAction(self._lang['QAction']['killProcess'])
            action_kill.setIcon(self.kill_process_icon)
            action_kill.triggered.connect(lambda: self.kill_process_clicked.emit())
            menu.addAction(action_kill)

        menu.addSeparator()

        action_remove = QAction(self._lang['QAction']['removeFromList'])
        action_remove.setIcon(self.remove_from_list_icon)
        action_remove.triggered.connect(lambda: self.remove_from_list_clicked.emit())
        menu.addAction(action_remove)

        if self._release in ['official', 'prerelease'] and not self._is_running:
            action_uninstall = QAction(self._lang['QAction']['uninstall'])
            action_uninstall.setIcon(self.uninstall_icon)
            action_uninstall.triggered.connect(lambda: self.uninstall_clicked.emit())
            menu.addAction(action_uninstall)

        menu.exec(self._settings_button.mapToGlobal(QPoint(0, 0)))

    def show_in_explorer(self) -> None:
        self.show_in_explorer_clicked.emit()

    def edit(self) -> None:
        self.edit_clicked.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_pressed.emit()
        return super().mousePressEvent(event)

    def progress_changed(self, value: int) -> None:
        self._progress_bar.setValue(value)
#----------------------------------------------------------------------
