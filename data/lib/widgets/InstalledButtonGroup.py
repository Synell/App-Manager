#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QObject
from datetime import datetime
import subprocess, json, os

from data.lib.qtUtils import QIconWidget
from data.lib.widgets import InstallButton, InstallWorker

from .InstalledButton import InstalledButton
from .dialog import EditAppDialog
#----------------------------------------------------------------------

    # Class
class InstalledButtonGroup(QObject):
    update_app = Signal(str)
    update_app_done = Signal(str, bool)

    remove_from_list = Signal(str)
    uninstall = Signal(str)

    info_changed = Signal(str)

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


    def add_button(self, key: str) -> InstalledButton:
        button = InstalledButton(self.name, self.tag_name, self.release, self.path, self.lang, self.base_icon, self.compact_mode)

        self.buttons[key] = button

        button.mouse_pressed.connect(self.mouse_pressed)
        button.edit_clicked.connect(self.edit)
        button.show_in_explorer_clicked.connect(self.show_in_explorer)
        button.remove_from_list.connect(lambda: self.remove_from_list.emit(self.path))
        button.update_app.connect(lambda: self.update_app.emit(self.path))
        button.uninstall.connect(lambda: self.uninstall.emit(self.path))

        button.set_update(bool(self.has_update))
        button.set_disabled(self.is_disabled)

        button.set_icon(self.raw_icon, self.base_icon)

        return button

    def get_button(self, key: str) -> InstalledButton:
        return self.buttons[key]

    def remove_button(self, key: str) -> None:
        self.buttons[key].deleteLater()
        self.buttons.pop(key)


    def keys(self) -> list[str]:
        return list(self.buttons.keys())


    def set_icon(self, icon: str) -> None:
        self.raw_icon = icon

        if QIconWidget.is_file_icon(self.raw_icon):
            for button in self.buttons.values():
                button.icon.icon = self.base_icon
                button.set_icon(icon, self.base_icon)

        else:
            for button in self.buttons.values():
                button.icon.icon = icon


    def set_update(self, has_update: bool, download_data: InstallButton.download_data = None) -> None:
        self.has_update = has_update
        self.download_data = download_data

        for button in self.buttons.values():
            button.set_update(self.has_update and self.release in ['official', 'prerelease'])

        if self.auto_update and self.has_update: self.update_app.emit(self.path)


    def set_disabled(self, disabled: bool) -> None:
        self.is_disabled = disabled

        for button in self.buttons.values():
            button.set_disabled(disabled)


    def set_compact_mode(self, compact_mode: bool) -> None:
        self.compact_mode = compact_mode

        for button in self.buttons.values():
            button.set_compact_mode(compact_mode, self.path)


    def show_in_explorer(self) -> None:
        path = self.path.replace('/', '\\')
        subprocess.Popen(rf'explorer /select, "{path}"', shell = False)

    def edit(self) -> None:
        edit_dialog = EditAppDialog(self.mw, self.lang['EditAppDialog'], self.name, self.tag_name, self.release, self.created_at, self.raw_icon, self.cwd, self.command, self.path, self.check_for_updates, self.auto_update, self.category)
        edit_dialog.refresh_app_info.connect(self.refresh_info)
        edit_dialog.exec()

    def mouse_pressed(self) -> None:
        try:
            subprocess.Popen(rf'{self.command}', cwd = rf'{self.cwd}', shell = False)

        except Exception as e:
            print('oof: ' + str(e)) #todo

    def init_update(self, download_path: str) -> None:
        if not self.download_data: return print('missing dl data')
        self.set_disabled(True)
        self.install_worker = InstallWorker(self, self.download_data, download_path, os.path.dirname(self.path))
        self.install_worker.signals.download_progress_changed.connect(lambda val: self.progress_changed(val / 2))
        self.install_worker.signals.install_progress_changed.connect(lambda val: self.progress_changed(0.5 + (val / 2)))
        self.install_worker.signals.install_done.connect(lambda: self.progress_done(True))
        self.install_worker.signals.install_failed.connect(lambda: self.progress_done(False))
        self.install_worker.start()

    def progress_changed(self, value: float) -> None:
        v = int(value * 100)
        for button in self.buttons.values():
            button.progress_changed(v)

    def progress_done(self, success: bool) -> None:
        self.set_disabled(False)

        if success:
            self.set_update(False)
            self.download_data = None

        if self.install_worker:
            self.install_worker.exit()

            if self.install_worker.isRunning():
                self.install_worker.terminate()

        self.install_worker = None
        self.update_app_done.emit(self.path, success)

    def refresh_info(self):
        with open(f'{self.path}/manifest.json', 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            self.command = data['command']
            self.cwd = data['cwd']
            self.raw_icon = data['icon']
            self.set_icon(self.raw_icon)
            if self.release in ['official', 'prerelease']:
                self.check_for_updates = data['checkForUpdates']
                self.auto_update = data['autoUpdate']
            self.category = data['category'] if 'category' in data else None

        self.info_changed.emit(self.path)

    def clear_parent(self) -> None:
        for button in self.buttons.values():
            button.setParent(None)
#----------------------------------------------------------------------
