#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

from .PlatformType import PlatformType
from .SettingsListNamedItem import SettingsListNamedItem
from .CategoryListNamedItem import CategoryListNamedItem
from .Category import Category
from datetime import datetime
from contextlib import suppress
import os

from data.lib.qtUtils import QFiles, QNamedLineEdit, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QDragList
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, save_path: str = './data/save.dat') -> None:
        self.platform = PlatformType.Windows
        self.apps_folder = os.path.abspath('./data/apps/').replace('\\', '/')
        self.downloads_folder = os.path.abspath('./data/downloads/').replace('\\', '/')
        self.apps = {'official': [], 'pre': [], 'custom': []}
        self.categories: list[Category] = []
        self.followed_apps = []
        self.check_for_updates = 4
        self.check_for_apps_updates = 4
        self.new_apps_check_for_updates = 4
        self.new_apps_auto_update = True

        self.last_check_for_updates = datetime.now()
        self.last_check_for_apps_updates = datetime.now()

        self.start_at_launch = True # TODO: Implement this functionallity
        self.minimize_to_tray = True

        self.compact_paths = 0

        self.token = {
            'github': ''
        }

        self.goes_to_tray_notif = True
        self.exit_during_work_notif = True
        self.update_done_notif = True # TODO: Implement this functionallity
        self.update_failed_notif = True # TODO: Implement this functionallity
        self.app_install_done_notif = True
        self.app_install_failed_notif = True
        self.app_uninstall_done_notif = True
        self.app_uninstall_failed_notif = True
        self.request_worker_failed_notif = True

        super().__init__(save_path)


    @property
    def category_keywords(self) -> list[str]:
        return [category.keyword for category in self.categories]


    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']: (self.settings_menu_installs(), f'{self.get_icon_dir()}/sidepanel/installs.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']: (self.settings_menu_updates(), f'{self.get_icon_dir()}/sidepanel/updates.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']: (self.settings_menu_interface(), f'{self.get_icon_dir()}/sidepanel/interface.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']: (self.settings_menu_notification(), f'{self.get_icon_dir()}/sidepanel/notification.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['token']['title']: (self.settings_menu_github(), f'{self.get_icon_dir()}/sidepanel/token.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['categories']['title']: (self.settings_menu_categories(), f'{self.get_icon_dir()}/sidepanel/categories.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['followedApps']['title']: (self.settings_menu_followed_apps(), f'{self.get_icon_dir()}/sidepanel/followedApps.png')
        }, self.get_extra


    def settings_menu_installs(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['installs']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['installsLocation']['title'], lang['QLabel']['installsLocation']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.installs_folder_button = QFileButton(
            None,
            lang['QFileButton']['installsLocation'],
            self.apps_folder,
            f'{self.get_icon_dir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.installs_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.installs_folder_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.installs_folder_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['downloadsLocation']['title'], lang['QLabel']['downloadsLocation']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.downloads_folder_button = QFileButton(
            None,
            lang['QFileButton']['downloadsLocation'],
            self.downloads_folder,
            f'{self.get_icon_dir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.downloads_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.downloads_folder_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.downloads_folder_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_updates(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['updates']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['checkForUpdates']['title'], lang['QLabel']['checkForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        widget.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(widget.check_for_updates_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['checkForAppsUpdates']['title'], lang['QLabel']['checkForAppsUpdates']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.check_for_apps_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForAppsUpdates']['title'])
        widget.check_for_apps_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['atLaunch']
        ])
        widget.check_for_apps_updates_combobox.combo_box.setCurrentIndex(self.check_for_apps_updates)
        root_frame.grid_layout.addWidget(widget.check_for_apps_updates_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.check_for_apps_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['newAppsCheckForUpdates']['title'], lang['QLabel']['newAppsCheckForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.new_apps_check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['newAppsCheckForUpdates']['title'])
        widget.new_apps_check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['never'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['daily'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['atLaunch']
        ])
        widget.new_apps_check_for_updates_combobox.combo_box.setCurrentIndex(self.new_apps_check_for_updates)
        root_frame.grid_layout.addWidget(widget.new_apps_check_for_updates_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.new_apps_check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['newAppsAutoUpdate']['title'], lang['QLabel']['newAppsAutoUpdate']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.new_apps_auto_update_checkbox = QNamedToggleButton()
        widget.new_apps_auto_update_checkbox.setText(lang['QToggleButton']['newAppsAutoUpdate'])
        widget.new_apps_auto_update_checkbox.setChecked(self.new_apps_auto_update)
        root_frame.grid_layout.addWidget(widget.new_apps_auto_update_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.new_apps_auto_update_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_interface(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['interface']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        # label = QSettingsDialog.textGroup(lang['QLabel']['startAtLaunch']['title'], lang['QLabel']['startAtLaunch']['description'])
        # root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang['QToggleButton']['startAtLaunch'])
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        # root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, root_frame.grid_layout.count(), 0)
        # root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['minimizeToTray']['title'], lang['QLabel']['minimizeToTray']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.minimize_to_tray_checkbox = QNamedToggleButton()
        widget.minimize_to_tray_checkbox.setText(lang['QToggleButton']['minimizeToTray'])
        widget.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
        root_frame.grid_layout.addWidget(widget.minimize_to_tray_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.minimize_to_tray_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['compactPaths']['title'], lang['QLabel']['compactPaths']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.compact_paths_combobox = QNamedComboBox(None, lang['QNamedComboBox']['compactPaths']['title'])
        widget.compact_paths_combobox.combo_box.addItems([
            lang['QNamedComboBox']['compactPaths']['values']['auto'],
            lang['QNamedComboBox']['compactPaths']['values']['enabled'],
            lang['QNamedComboBox']['compactPaths']['values']['disabled']
        ])
        widget.compact_paths_combobox.combo_box.setCurrentIndex(self.compact_paths)
        root_frame.grid_layout.addWidget(widget.compact_paths_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.compact_paths_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_notification(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['notification']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['goesToTray']['title'], lang['QLabel']['goesToTray']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.goes_to_tray_notif_checkbox = QNamedToggleButton()
        widget.goes_to_tray_notif_checkbox.setText(lang['QToggleButton']['goesToTray'])
        widget.goes_to_tray_notif_checkbox.setChecked(self.goes_to_tray_notif)
        root_frame.grid_layout.addWidget(widget.goes_to_tray_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.goes_to_tray_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['exitDuringWork']['title'], lang['QLabel']['exitDuringWork']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.exit_during_work_notif_checkbox = QNamedToggleButton()
        widget.exit_during_work_notif_checkbox.setText(lang['QToggleButton']['exitDuringWork'])
        widget.exit_during_work_notif_checkbox.setChecked(self.exit_during_work_notif)
        root_frame.grid_layout.addWidget(widget.exit_during_work_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.exit_during_work_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['updateDone']['title'], lang['QLabel']['updateDone']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.update_done_notif_checkbox = QNamedToggleButton()
        widget.update_done_notif_checkbox.setText(lang['QToggleButton']['updateDone'])
        widget.update_done_notif_checkbox.setChecked(self.update_done_notif)
        root_frame.grid_layout.addWidget(widget.update_done_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.update_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['updateFailed']['title'], lang['QLabel']['updateFailed']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.update_failed_notif_checkbox = QNamedToggleButton()
        widget.update_failed_notif_checkbox.setText(lang['QToggleButton']['updateFailed'])
        widget.update_failed_notif_checkbox.setChecked(self.update_failed_notif)
        root_frame.grid_layout.addWidget(widget.update_failed_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.update_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appInstallDone']['title'], lang['QLabel']['appInstallDone']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.app_install_done_notif_checkbox = QNamedToggleButton()
        widget.app_install_done_notif_checkbox.setText(lang['QToggleButton']['appInstallDone'])
        widget.app_install_done_notif_checkbox.setChecked(self.app_install_done_notif)
        root_frame.grid_layout.addWidget(widget.app_install_done_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.app_install_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appInstallFailed']['title'], lang['QLabel']['appInstallFailed']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.app_install_failed_notif_checkbox = QNamedToggleButton()
        widget.app_install_failed_notif_checkbox.setText(lang['QToggleButton']['appInstallFailed'])
        widget.app_install_failed_notif_checkbox.setChecked(self.app_install_failed_notif)
        root_frame.grid_layout.addWidget(widget.app_install_failed_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.app_install_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appUninstallDone']['title'], lang['QLabel']['appUninstallDone']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.app_uninstall_done_notif_checkbox = QNamedToggleButton()
        widget.app_uninstall_done_notif_checkbox.setText(lang['QToggleButton']['appUninstallDone'])
        widget.app_uninstall_done_notif_checkbox.setChecked(self.app_uninstall_done_notif)
        root_frame.grid_layout.addWidget(widget.app_uninstall_done_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.app_uninstall_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appUninstallFailed']['title'], lang['QLabel']['appUninstallFailed']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.app_uninstall_failed_notif_checkbox = QNamedToggleButton()
        widget.app_uninstall_failed_notif_checkbox.setText(lang['QToggleButton']['appUninstallFailed'])
        widget.app_uninstall_failed_notif_checkbox.setChecked(self.app_uninstall_failed_notif)
        root_frame.grid_layout.addWidget(widget.app_uninstall_failed_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.app_uninstall_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['requestWorkerFailed']['title'], lang['QLabel']['requestWorkerFailed']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.request_worker_failed_notif_checkbox = QNamedToggleButton()
        widget.request_worker_failed_notif_checkbox.setText(lang['QToggleButton']['requestWorkerFailed'])
        widget.request_worker_failed_notif_checkbox.setChecked(self.request_worker_failed_notif)
        root_frame.grid_layout.addWidget(widget.request_worker_failed_notif_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.request_worker_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_github(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['token']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['github']['title'], lang['QLabel']['github']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        label = QLabel(f'<a href=\"https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">{lang["QLabel"]["github"]["createToken"]}</a>')
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.github_token_lineedit = QNamedLineEdit(None, 'null', lang['QNamedLineEdit']['github'])
        widget.github_token_lineedit.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        widget.github_token_lineedit.setText(self.token['github'])
        widget.github_token_lineedit.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.github_token_lineedit, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.github_token_lineedit, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_followed_apps(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['followedApps']
        key = 'url'
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['followedApps']['title'], lang['QLabel']['followedApps']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.followed_apps_list = QDragList()
        root_frame.grid_layout.addWidget(widget.followed_apps_list, root_frame.grid_layout.count(), 0)

        for app in self.followed_apps:
            widget.followed_apps_list.add_item(SettingsListNamedItem(lang['SettingsListNamedItem'], key, app))

        button = QPushButton()
        button.setIcon(self.get_icon('pushbutton/plus.png'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: widget.followed_apps_list.add_item(SettingsListNamedItem(lang['SettingsListNamedItem'], key, '')))
        root_frame.grid_layout.addWidget(button, root_frame.grid_layout.count(), 0)


        return widget



    def settings_menu_categories(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['categories']
        key = 'category'
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['categories']['title'], lang['QLabel']['categories']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.categories_list = QDragList()
        root_frame.grid_layout.addWidget(widget.categories_list, root_frame.grid_layout.count(), 0)

        for cat in self.categories:
            widget.categories_list.add_item(CategoryListNamedItem(lang['CategoryListNamedItem'], key, cat))

        button = QPushButton()
        button.setIcon(self.get_icon('pushbutton/plus.png'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: widget.categories_list.add_item(CategoryListNamedItem(lang['CategoryListNamedItem'], key, Category('', './data/icons/questionMark.svg'))))
        root_frame.grid_layout.addWidget(button, root_frame.grid_layout.count(), 0)


        return widget



    def get_extra(self, extra_tabs: dict = {}):
        self.apps_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].installs_folder_button.path()
        self.downloads_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].downloads_folder_button.path()
        self.check_for_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].check_for_updates_combobox.combo_box.currentIndex()
        self.check_for_apps_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].check_for_apps_updates_combobox.combo_box.currentIndex()
        self.new_apps_check_for_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].new_apps_check_for_updates_combobox.combo_box.currentIndex()
        self.new_apps_auto_update = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].new_apps_auto_update_checkbox.isChecked()

        self.start_at_launch = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].start_at_launch_checkbox.isChecked()
        self.minimize_to_tray = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].minimize_to_tray_checkbox.isChecked()

        self.compact_paths = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].compact_paths_combobox.combo_box.currentIndex()

        self.token['github'] = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['token']['title']].github_token_lineedit.text()

        self.categories = self.without_duplicates([Category(item.keyword, item.icon) for item in extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['categories']['title']].categories_list.items if item.keyword != ''])

        self.followed_apps = self.without_duplicates([item.keyword for item in extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['followedApps']['title']].followed_apps_list.items if self.valid_url(item.keyword) if item.keyword != ''])

        self.goes_to_tray_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].goes_to_tray_notif_checkbox.isChecked()
        self.exit_during_work_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].exit_during_work_notif_checkbox.isChecked()
        self.update_done_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].update_done_notif_checkbox.isChecked()
        self.update_failed_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].update_failed_notif_checkbox.isChecked()
        self.app_install_done_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].app_install_done_notif_checkbox.isChecked()
        self.app_install_failed_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].app_install_failed_notif_checkbox.isChecked()
        self.app_uninstall_done_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].app_uninstall_done_notif_checkbox.isChecked()
        self.app_uninstall_failed_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].app_uninstall_failed_notif_checkbox.isChecked()
        self.request_worker_failed_notif = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']].request_worker_failed_notif_checkbox.isChecked()



    def valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


    def without_duplicates(self, l: list) -> list:
        return list(dict.fromkeys(l))


    def save_extra_data(self) -> dict:
        return {
            'apps': self.apps,
            'folders': {
                'apps': self.apps_folder,
                'downloads': self.downloads_folder
            },
            'categories': [[cat.keyword, cat.icon] for cat in self.categories],
            'followedApps': self.followed_apps,

            'checkForUpdates': self.check_for_updates,
            'checkForAppsUpdates': self.check_for_apps_updates,
            'newAppsCheckForUpdates': self.new_apps_check_for_updates,
            'newAppsAutoUpdate': self.new_apps_auto_update,

            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),
            'lastCheckForAppsUpdates': self.last_check_for_apps_updates.strftime(self.dateformat),

            'startAtLaunch': self.start_at_launch,
            'minimizeToTray': self.minimize_to_tray,

            'compactPaths': self.compact_paths,

            'token': self.token,

            'goesToTrayNotif': self.goes_to_tray_notif,
            'exitDuringWorkNotif': self.exit_during_work_notif,
            'updateDoneNotif': self.update_done_notif,
            'updateFailedNotif': self.update_failed_notif,
            'appInstallDoneNotif': self.app_install_done_notif,
            'appInstallFailedNotif': self.app_install_failed_notif,
            'appUninstallDoneNotif': self.app_uninstall_done_notif,
            'appUninstallFailedNotif': self.app_uninstall_failed_notif,
            'requestWorkerFailedNotif': self.request_worker_failed_notif
        }

    def load_extra_data(self, extra_data: dict = ..., reload: list = []) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.apps['official'] = extra_data['apps']['official']
        with exc: self.apps['pre'] = extra_data['apps']['pre']
        with exc: self.apps['custom'] = extra_data['apps']['custom']

        with exc: self.apps_folder = extra_data['folders']['apps']
        with exc: self.downloads_folder = extra_data['folders']['downloads']

        cat_list = []
        with exc: cat_list = extra_data['categories']
        cat_list_good = []
        self.categories = []

        for cat in cat_list:
            if not isinstance(cat, list):
                cat_list_good.append(Category(cat, './data/icons/questionMark.svg'))

            elif len(cat) == 2:
                cat_list_good.append(Category(*cat))

        cat_names = []
        for cat in cat_list_good:
            if cat.keyword not in cat_names:
                cat_names.append(cat.keyword)
                self.categories.append(cat)

        with exc: self.followed_apps = extra_data['followedApps']

        with exc: self.check_for_updates = extra_data['checkForUpdates']
        with exc: self.check_for_apps_updates = extra_data['checkForAppsUpdates']
        with exc: self.new_apps_check_for_updates = extra_data['newAppsCheckForUpdates']
        with exc: self.new_apps_auto_update = extra_data['newAppsAutoUpdate']

        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)
        with exc: self.last_check_for_apps_updates = datetime.strptime(extra_data['lastCheckForAppsUpdates'], self.dateformat)

        with exc: self.start_at_launch = extra_data['startAtLaunch']
        with exc: self.minimize_to_tray = extra_data['minimizeToTray']

        with exc: self.compact_paths = extra_data['compactPaths']

        with exc:
            if isinstance(extra_data['token'], dict): self.token = extra_data['token']
            else: self.token['github'] = extra_data['token']

        with exc: self.goes_to_tray_notif = extra_data['goesToTrayNotif']
        with exc: self.exit_during_work_notif = extra_data['exitDuringWorkNotif']
        with exc: self.update_done_notif = extra_data['updateDoneNotif']
        with exc: self.update_failed_notif = extra_data['updateFailedNotif']
        with exc: self.app_install_done_notif = extra_data['appInstallDoneNotif']
        with exc: self.app_install_failed_notif = extra_data['appInstallFailedNotif']
        with exc: self.app_uninstall_done_notif = extra_data['appUninstallDoneNotif']
        with exc: self.app_uninstall_failed_notif = extra_data['appUninstallFailedNotif']
        with exc: self.request_worker_failed_notif = extra_data['requestWorkerFailedNotif']

        return res

    def export_extra_data(self) -> dict:
        dct = self.save_extra_data()
        del dct['apps']
        return dct
#----------------------------------------------------------------------
