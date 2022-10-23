#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PyQt6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

from .PlatformType import PlatformType
from .SettingsListNamedItem import SettingsListNamedItem
from datetime import datetime
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

        self.token = None

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


    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']: (self.settings_menu_installs(), f'{self.getIconsDir()}/sidepanel/installs.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']: (self.settings_menu_updates(), f'{self.getIconsDir()}/sidepanel/updates.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']: (self.settings_menu_interface(), f'{self.getIconsDir()}/sidepanel/interface.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['notification']['title']: (self.settings_menu_notification(), f'{self.getIconsDir()}/sidepanel/notification.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['github']['title']: (self.settings_menu_github(), f'{self.getIconsDir()}/sidepanel/github.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['followedApps']['title']: (self.settings_menu_followed_apps(), f'{self.getIconsDir()}/sidepanel/followedApps.png')
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
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.installs_folder_button = QFileButton(
            None,
            lang['QFileButton']['installsLocation'],
            self.apps_folder,
            f'{self.getIconsDir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.installs_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.installs_folder_button, 1, 0)
        root_frame.grid_layout.setAlignment(widget.installs_folder_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['downloadsLocation']['title'], lang['QLabel']['downloadsLocation']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        widget.downloads_folder_button = QFileButton(
            None,
            lang['QFileButton']['downloadsLocation'],
            self.downloads_folder,
            f'{self.getIconsDir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.downloads_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.downloads_folder_button, 4, 0)
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
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        widget.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(widget.check_for_updates_combobox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['checkForAppsUpdates']['title'], lang['QLabel']['checkForAppsUpdates']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        widget.check_for_apps_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForAppsUpdates']['title'])
        widget.check_for_apps_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForAppsUpdates']['values']['atLaunch']
        ])
        widget.check_for_apps_updates_combobox.combo_box.setCurrentIndex(self.check_for_apps_updates)
        root_frame.grid_layout.addWidget(widget.check_for_apps_updates_combobox, 4, 0)
        root_frame.grid_layout.setAlignment(widget.check_for_apps_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 5, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['newAppsCheckForUpdates']['title'], lang['QLabel']['newAppsCheckForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, 6, 0)

        widget.new_apps_check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['newAppsCheckForUpdates']['title'])
        widget.new_apps_check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['never'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['daily'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['newAppsCheckForUpdates']['values']['atLaunch']
        ])
        widget.new_apps_check_for_updates_combobox.combo_box.setCurrentIndex(self.new_apps_check_for_updates)
        root_frame.grid_layout.addWidget(widget.new_apps_check_for_updates_combobox, 7, 0)
        root_frame.grid_layout.setAlignment(widget.new_apps_check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 8, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['newAppsAutoUpdate']['title'], lang['QLabel']['newAppsAutoUpdate']['description'])
        root_frame.grid_layout.addWidget(label, 9, 0)

        widget.new_apps_auto_update_checkbox = QNamedToggleButton()
        widget.new_apps_auto_update_checkbox.setText(lang['QToggleButton']['newAppsAutoUpdate'])
        widget.new_apps_auto_update_checkbox.setChecked(self.new_apps_auto_update)
        root_frame.grid_layout.addWidget(widget.new_apps_auto_update_checkbox, 10, 0)
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
        # root_frame.grid_layout.addWidget(label, 0, 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang['QToggleButton']['startAtLaunch'])
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        # root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, 1, 0)
        # root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['minimizeToTray']['title'], lang['QLabel']['minimizeToTray']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        widget.minimize_to_tray_checkbox = QNamedToggleButton()
        widget.minimize_to_tray_checkbox.setText(lang['QToggleButton']['minimizeToTray'])
        widget.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
        root_frame.grid_layout.addWidget(widget.minimize_to_tray_checkbox, 4, 0)
        root_frame.grid_layout.setAlignment(widget.minimize_to_tray_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 5, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['compactPaths']['title'], lang['QLabel']['compactPaths']['description'])
        root_frame.grid_layout.addWidget(label, 6, 0)

        widget.compact_paths_combobox = QNamedComboBox(None, lang['QNamedComboBox']['compactPaths']['title'])
        widget.compact_paths_combobox.combo_box.addItems([
            lang['QNamedComboBox']['compactPaths']['values']['auto'],
            lang['QNamedComboBox']['compactPaths']['values']['enabled'],
            lang['QNamedComboBox']['compactPaths']['values']['disabled']
        ])
        widget.compact_paths_combobox.combo_box.setCurrentIndex(self.compact_paths)
        root_frame.grid_layout.addWidget(widget.compact_paths_combobox, 7, 0)
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
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.goes_to_tray_notif_checkbox = QNamedToggleButton()
        widget.goes_to_tray_notif_checkbox.setText(lang['QToggleButton']['goesToTray'])
        widget.goes_to_tray_notif_checkbox.setChecked(self.goes_to_tray_notif)
        root_frame.grid_layout.addWidget(widget.goes_to_tray_notif_checkbox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.goes_to_tray_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['exitDuringWork']['title'], lang['QLabel']['exitDuringWork']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        widget.exit_during_work_notif_checkbox = QNamedToggleButton()
        widget.exit_during_work_notif_checkbox.setText(lang['QToggleButton']['exitDuringWork'])
        widget.exit_during_work_notif_checkbox.setChecked(self.exit_during_work_notif)
        root_frame.grid_layout.addWidget(widget.exit_during_work_notif_checkbox, 4, 0)
        root_frame.grid_layout.setAlignment(widget.exit_during_work_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 5, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['updateDone']['title'], lang['QLabel']['updateDone']['description'])
        root_frame.grid_layout.addWidget(label, 6, 0)

        widget.update_done_notif_checkbox = QNamedToggleButton()
        widget.update_done_notif_checkbox.setText(lang['QToggleButton']['updateDone'])
        widget.update_done_notif_checkbox.setChecked(self.update_done_notif)
        root_frame.grid_layout.addWidget(widget.update_done_notif_checkbox, 7, 0)
        root_frame.grid_layout.setAlignment(widget.update_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 8, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['updateFailed']['title'], lang['QLabel']['updateFailed']['description'])
        root_frame.grid_layout.addWidget(label, 9, 0)

        widget.update_failed_notif_checkbox = QNamedToggleButton()
        widget.update_failed_notif_checkbox.setText(lang['QToggleButton']['updateFailed'])
        widget.update_failed_notif_checkbox.setChecked(self.update_failed_notif)
        root_frame.grid_layout.addWidget(widget.update_failed_notif_checkbox, 10, 0)
        root_frame.grid_layout.setAlignment(widget.update_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 11, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appInstallDone']['title'], lang['QLabel']['appInstallDone']['description'])
        root_frame.grid_layout.addWidget(label, 12, 0)

        widget.app_install_done_notif_checkbox = QNamedToggleButton()
        widget.app_install_done_notif_checkbox.setText(lang['QToggleButton']['appInstallDone'])
        widget.app_install_done_notif_checkbox.setChecked(self.app_install_done_notif)
        root_frame.grid_layout.addWidget(widget.app_install_done_notif_checkbox, 13, 0)
        root_frame.grid_layout.setAlignment(widget.app_install_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 14, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appInstallFailed']['title'], lang['QLabel']['appInstallFailed']['description'])
        root_frame.grid_layout.addWidget(label, 15, 0)

        widget.app_install_failed_notif_checkbox = QNamedToggleButton()
        widget.app_install_failed_notif_checkbox.setText(lang['QToggleButton']['appInstallFailed'])
        widget.app_install_failed_notif_checkbox.setChecked(self.app_install_failed_notif)
        root_frame.grid_layout.addWidget(widget.app_install_failed_notif_checkbox, 16, 0)
        root_frame.grid_layout.setAlignment(widget.app_install_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 17, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appUninstallDone']['title'], lang['QLabel']['appUninstallDone']['description'])
        root_frame.grid_layout.addWidget(label, 18, 0)

        widget.app_uninstall_done_notif_checkbox = QNamedToggleButton()
        widget.app_uninstall_done_notif_checkbox.setText(lang['QToggleButton']['appUninstallDone'])
        widget.app_uninstall_done_notif_checkbox.setChecked(self.app_uninstall_done_notif)
        root_frame.grid_layout.addWidget(widget.app_uninstall_done_notif_checkbox, 19, 0)
        root_frame.grid_layout.setAlignment(widget.app_uninstall_done_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 20, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['appUninstallFailed']['title'], lang['QLabel']['appUninstallFailed']['description'])
        root_frame.grid_layout.addWidget(label, 21, 0)

        widget.app_uninstall_failed_notif_checkbox = QNamedToggleButton()
        widget.app_uninstall_failed_notif_checkbox.setText(lang['QToggleButton']['appUninstallFailed'])
        widget.app_uninstall_failed_notif_checkbox.setChecked(self.app_uninstall_failed_notif)
        root_frame.grid_layout.addWidget(widget.app_uninstall_failed_notif_checkbox, 22, 0)
        root_frame.grid_layout.setAlignment(widget.app_uninstall_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 23, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['requestWorkerFailed']['title'], lang['QLabel']['requestWorkerFailed']['description'])
        root_frame.grid_layout.addWidget(label, 24, 0)

        widget.request_worker_failed_notif_checkbox = QNamedToggleButton()
        widget.request_worker_failed_notif_checkbox.setText(lang['QToggleButton']['requestWorkerFailed'])
        widget.request_worker_failed_notif_checkbox.setChecked(self.request_worker_failed_notif)
        root_frame.grid_layout.addWidget(widget.request_worker_failed_notif_checkbox, 25, 0)
        root_frame.grid_layout.setAlignment(widget.request_worker_failed_notif_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_github(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['github']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['token']['title'], lang['QLabel']['token']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        label = QLabel(f'<a href=\"https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">{lang["QLabel"]["createToken"]}</a>')
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        root_frame.grid_layout.addWidget(label, 1, 0)

        widget.token_lineedit = QNamedLineEdit(None, 'null', lang['QNamedLineEdit']['token'])
        widget.token_lineedit.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        widget.token_lineedit.setText(self.token)
        widget.token_lineedit.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.token_lineedit, 2, 0)
        root_frame.grid_layout.setAlignment(widget.token_lineedit, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_followed_apps(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['followedApps']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['followedApps']['title'], lang['QLabel']['followedApps']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.followed_apps_list = QDragList()
        root_frame.grid_layout.addWidget(widget.followed_apps_list, 1, 0)

        for app in self.followed_apps:
            widget.followed_apps_list.add_item(SettingsListNamedItem(lang['SettingsListNamedItem'], app))

        button = QPushButton()
        button.setIcon(self.getIcon('pushbutton/plus.png'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: widget.followed_apps_list.add_item(SettingsListNamedItem(lang['SettingsListNamedItem'], '')))
        root_frame.grid_layout.addWidget(button, 2, 0)


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

        self.token = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['github']['title']].token_lineedit.text()

        self.followed_apps = [item.url for item in extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['followedApps']['title']].followed_apps_list.items if self.valid_url(item.url)]

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


    def save_extra_data(self) -> dict:
        return {
            'apps': self.apps,
            'folders': {
                'apps': self.apps_folder,
                'downloads': self.downloads_folder
            },
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

    def load_extra_data(self, extra_data: dict = ...) -> None:
        try:
            self.apps['official'] = extra_data['apps']['official']
            self.apps['pre'] = extra_data['apps']['pre']
            self.apps['custom'] = extra_data['apps']['custom']

            self.apps_folder = extra_data['folders']['apps']
            self.downloads_folder = extra_data['folders']['downloads']

            self.followed_apps = extra_data['followedApps']

            self.check_for_updates = extra_data['checkForUpdates']
            self.check_for_apps_updates = extra_data['checkForAppsUpdates']

            self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)
            self.last_check_for_apps_updates = datetime.strptime(extra_data['lastCheckForAppsUpdates'], self.dateformat)

            self.start_at_launch = extra_data['startAtLaunch']
            self.minimize_to_tray = extra_data['minimizeToTray']

            self.compact_paths = extra_data['compactPaths']

            self.token = extra_data['token']

            self.goes_to_tray_notif = extra_data['goesToTrayNotif']
            self.exit_during_work_notif = extra_data['exitDuringWorkNotif']
            self.update_done_notif = extra_data['updateDoneNotif']
            self.update_failed_notif = extra_data['updateFailedNotif']
            self.app_install_done_notif = extra_data['appInstallDoneNotif']
            self.app_install_failed_notif = extra_data['appInstallFailedNotif']
            self.app_uninstall_done_notif = extra_data['appUninstallDoneNotif']
            self.app_uninstall_failed_notif = extra_data['appUninstallFailedNotif']
            self.request_worker_failed_notif = extra_data['requestWorkerFailedNotif']

        except: self.save()
#----------------------------------------------------------------------
