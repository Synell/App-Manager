#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QObject
from datetime import datetime
import subprocess, json, os

from data.lib.QtUtils import QIconWidget
from data.lib.widgets import InstallButton, InstallWorker

from .InstalledButton import InstalledButton
from .dialog import EditAppDialog
from .AppWorker import AppWorker
#----------------------------------------------------------------------

    # Class
class InstalledButtonGroup(QObject):
    update_app = Signal(str)
    update_app_done = Signal(str, bool)

    process_already_running = Signal(str)
    process_ended = Signal(str)
    process_killed = Signal(str)

    remove_from_list = Signal(str)
    uninstall = Signal(str)

    info_changed = Signal(str)

    exec_failed = Signal(str, str)

    def __init__(self, mw: QMainWindow, name: str = '', path: str = '', lang : dict = {}, icon: str = None, disabled: bool = False, has_update: InstallButton.download_data = False, compact_mode: bool = False) -> None:
        super().__init__()

        self.mw = mw
        self.name = name
        self.path = path
        self.lang = lang
        self.base_icon = icon
        self.has_update = has_update
        self.is_disabled = disabled
        self.compact_mode = compact_mode
        self.download_data = has_update
        self.install_worker = None
        
        self.buttons: dict[str, InstalledButton] = {}

        with open(f'{path}/manifest.json', 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            self.release = data['release']
            self.tag_name = data['tag_name'] if data['tag_name'] else 'Custom'
            self.command = data['command']
            self.created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ') if data['created_at'] else None
            self.cwd = data['cwd']
            self.raw_icon = data['icon']
            if self.release in ['official', 'prerelease']:
                self.check_for_updates = data['checkForUpdates']
                self.auto_update = data['autoUpdate']
            else:
                self.check_for_updates = 0
                self.auto_update = False
            self.category = data['category'] if 'category' in data else None

        self._set_compact_mode(self.compact_mode)

        self._thread = AppWorker(self, self.command, self.cwd)
        self._thread.signals.finished.connect(self._process_ended)


    def add_button(self, key: str) -> InstalledButton:
        button = InstalledButton(self.name, self.tag_name, self.release, self.path, self.lang, self.base_icon, self.compact_mode, self._thread.isRunning())

        self.buttons[key] = button

        button.mouse_pressed.connect(self._mouse_pressed)
        button.edit_clicked.connect(self._edit)
        button.show_in_explorer_clicked.connect(self._show_in_explorer)
        button.kill_process_clicked.connect(self._kill_process)
        button.remove_from_list_clicked.connect(lambda: self.remove_from_list.emit(self.path))
        button.update_app_clicked.connect(lambda: self.update_app.emit(self.path))
        button.uninstall_clicked.connect(self._uninstall)

        button.set_update(bool(self.has_update))
        button.set_disabled(self.is_disabled)
        button.set_compact_mode(self.compact_mode, self.path)
        button.set_is_running(self._thread.isRunning())

        button.set_icon(self.raw_icon, self.base_icon)

        return button

    def get_button(self, key: str) -> InstalledButton:
        return self.buttons[key]

    def remove_button(self, key: str) -> None:
        self.buttons[key].deleteLater()
        self.buttons.pop(key)


    def keys(self) -> list[str]:
        return list(self.buttons.keys())


    def _set_icon(self, icon: str) -> None:
        self.raw_icon = icon

        if QIconWidget.is_file_icon(self.raw_icon):
            for button in self.buttons.values():
                button._icon.icon = self.base_icon
                button.set_icon(icon, self.base_icon)

        else:
            for button in self.buttons.values():
                button._icon.icon = icon


    def _set_update(self, has_update: bool, download_data: InstallButton.download_data = None) -> None:
        self.has_update = has_update
        self.download_data = download_data

        for button in self.buttons.values():
            button.set_update(self.has_update and self.release in ['official', 'prerelease'])

        if self.auto_update and self.has_update: self.update_app.emit(self.path)


    def _set_disabled(self, disabled: bool) -> None:
        self.is_disabled = disabled

        for button in self.buttons.values():
            button.set_disabled(disabled)


    def _set_compact_mode(self, compact_mode: bool) -> None:
        self.compact_mode = compact_mode

        for button in self.buttons.values():
            button.set_compact_mode(compact_mode, self.path)


    def _set_is_running(self, is_running: bool) -> None:
        for button in self.buttons.values():
            button.set_is_running(is_running)


    def _show_in_explorer(self) -> None:
        path = self.path.replace('/', '\\')
        subprocess.Popen(rf'explorer /select, "{path}"', shell = False)

    def _edit(self) -> None:
        edit_dialog = EditAppDialog(self.mw, self.lang['EditAppDialog'], self.name, self.tag_name, self.release, self.created_at, self.raw_icon, self.cwd, self.command, self.path, self.check_for_updates, self.auto_update, self.category)
        edit_dialog.refresh_app_info.connect(self.refresh_info)
        edit_dialog.exec()

    def _process_ended(self) -> None:
        self.process_ended.emit(self.name)
        self._set_is_running(False)

    def is_process_running(self) -> bool:
        return self._thread.isRunning()

    def _kill_process(self) -> None:
        is_running = self._thread.isRunning()

        if is_running:
            self._thread.terminate()

        if not self._thread.isRunning() and is_running:
            self._set_is_running(False)
            self.process_killed.emit(self.name)


    def _uninstall(self) -> None:
        if not self._thread.isRunning():
            self.uninstall.emit(self.path)

    def _mouse_pressed(self) -> None:
        try:
            if self._thread.isRunning():
                return self.process_already_running.emit(self.name)

            self._thread.command = self.command
            self._thread.cwd = self.cwd

            self._thread.start()
            self._set_is_running(True)

        except Exception as e:
            self._thread.terminate()
            self._set_is_running(False)
            self.exec_failed.emit(self.name, str(e))

    def init_update(self, download_path: str) -> None:
        if not self.download_data: return print('missing dl data')
        self._set_disabled(True)
        self.install_worker = InstallWorker(self, self.download_data, self.download_data.files_data[0], download_path, os.path.dirname(self.path))
        self.install_worker.signals.download_progress_changed.connect(lambda val: self._progress_changed(val / 2))
        self.install_worker.signals.install_progress_changed.connect(lambda val: self._progress_changed(0.5 + (val / 2)))
        self.install_worker.signals.install_done.connect(lambda: self._progress_done(True))
        self.install_worker.signals.install_failed.connect(lambda: self._progress_done(False))
        self.install_worker.start()

    def _progress_changed(self, value: float) -> None:
        v = int(value * 100)
        for button in self.buttons.values():
            button.progress_changed(v)

    def _progress_done(self, success: bool) -> None:
        self._set_disabled(False)

        if success:
            self._set_update(False)
            self.download_data = None

        if self.install_worker:
            self.install_worker.exit()

            if self.install_worker.isRunning():
                self.install_worker.terminate()

        self.install_worker = None
        self.update_app_done.emit(self.path, success)
        self.refresh_info()

    def refresh_info(self) -> None:
        with open(f'{self.path}/manifest.json', 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            self.tag_name = data['tag_name']
            self.command = data['command']
            self.cwd = data['cwd']
            self.raw_icon = data['icon']
            self._set_icon(self.raw_icon)
            if self.release in ['official', 'prerelease']:
                self.check_for_updates = data['checkForUpdates']
                self.auto_update = data['autoUpdate']
            self.category = data['category'] if 'category' in data else None

        for button in self.buttons.values():
            button.set_text(self.name, self.tag_name, self.path)

        self.info_changed.emit(self.path)

    def clear_parent(self) -> None:
        for button in self.buttons.values():
            button.setParent(None)
#----------------------------------------------------------------------
