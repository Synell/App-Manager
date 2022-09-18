#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QFrame, QLabel, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt

from .PlatformType import PlatformType
from .SettingsListNamedItem import SettingsListNamedItem
from datetime import datetime
import os

from data.lib.qtUtils import QFiles, QNamedLineEdit, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QDragList
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%d %H:%M:%S'
    COLOR_LINK = QUtilsColor()

    def __init__(self, save_path: str = './data/save.dat') -> None:
        self.platform = PlatformType.Windows
        self.apps_folder = os.path.abspath('./data/apps/').replace('\\', '/')
        self.downloads_folder = os.path.abspath('./data/downloads/').replace('\\', '/')
        self.apps = {'official': [], 'pre': [], 'custom': []}
        self.followed_apps = [
            "https://github.com/CLF78/Reggie-Next",
            "https://github.com/RoadrunnerWMC/Level-Info-Editor"
        ]
        self.check_for_updates = 4
        self.check_for_apps_updates = 4

        self.last_check_for_updates = datetime.now()
        self.last_check_for_apps_updates = datetime.now()

        self.start_at_launch = True
        self.minimize_to_tray = True

        self.compact_paths = 0

        self.token = None

        super().__init__(save_path)


    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']: (self.settings_menu_installs(), f'{self.getIconsDir()}/sidepanel/installs.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']: (self.settings_menu_updates_and_startup(), f'{self.getIconsDir()}/sidepanel/updates.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']: (self.settings_menu_interface(), f'{self.getIconsDir()}/sidepanel/interface.png'),
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


    def settings_menu_updates_and_startup(self):
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


        label = QSettingsDialog.textGroup(lang['QLabel']['startAtLaunch']['title'], lang['QLabel']['startAtLaunch']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang['QToggleButton']['startAtLaunch'])
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


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

        label = QLabel(f'<a href=\"https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\" style=\"color: {self.COLOR_LINK.hex};\">{lang["QLabel"]["createToken"]}</a>')
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

        # widget.followed_apps_list = QListWidget()
        # widget.followed_apps_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        widget.followed_apps_list = QDragList()
        root_frame.grid_layout.addWidget(widget.followed_apps_list, 1, 0)

        for index, app in enumerate(self.followed_apps):
            # widget.followed_apps_list.addItem(app)
            # widget.followed_apps_list.item(index).setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsEditable)
            widget.followed_apps_list.add_item(SettingsListNamedItem({}, app))


        return widget


    def get_extra(self, extra_tabs: dict = {}):
        self.apps_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].installs_folder_button.path()
        self.downloads_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].downloads_folder_button.path()
        self.check_for_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].check_for_updates_combobox.combo_box.currentIndex()
        self.check_for_apps_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].check_for_apps_updates_combobox.combo_box.currentIndex()

        self.start_at_launch = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].start_at_launch_checkbox.isChecked()
        self.minimize_to_tray = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].minimize_to_tray_checkbox.isChecked()

        self.compact_paths = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['interface']['title']].compact_paths_combobox.combo_box.currentIndex()

        self.token = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['github']['title']].token_lineedit.text()


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

            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),
            'lastCheckForAppsUpdates': self.last_check_for_apps_updates.strftime(self.dateformat),

            'startAtLaunch': self.start_at_launch,
            'minimizeToTray': self.minimize_to_tray,

            'compactPaths': self.compact_paths,

            'token': self.token
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

        except: self.save()
#----------------------------------------------------------------------
