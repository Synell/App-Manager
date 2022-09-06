#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QFrame, QCheckBox
from PyQt6.QtCore import Qt

from .PlatformType import PlatformType
import os

from data.lib.qtUtils import QFiles, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
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
        self.start_at_launch = True

        super().__init__(save_path)


    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']: (self.settings_menu_installs(), f'{self.getIconsDir()}/sidepanel/installs.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['updatesAndStartup']['title']: (self.settings_menu_updates_and_startup(), f'{self.getIconsDir()}/sidepanel/updates.png')
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
        lang = self.language_data['QSettingsDialog']['QSidePanel']['updatesAndStartup']
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


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.grid_layout.addWidget(frame, 5, 0)

        # label = QSettingsDialog.textGroup(lang['QLabel']['checkForAppsUpdates']['title'], lang['QLabel']['checkForAppsUpdates']['description'])
        # root_frame.grid_layout.addWidget(label, 6, 0)

        # widget.start_at_launch_checkbox = QNamedComboBox(None, lang['QNamedComboBox']['checkForAppsUpdates']['title'])
        # widget.start_at_launch_checkbox.combo_box.setCurrentIndex(self.check_for_apps_updates)
        # root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, 7, 0)
        # root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget


    def get_extra(self, extra_tabs: dict = {}):
        self.apps_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].installs_folder_button.path()
        self.downloads_folder = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['installs']['title']].downloads_folder_button.path()
        self.check_for_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updatesAndStartup']['title']].check_for_updates_combobox.combo_box.currentIndex()
        self.check_for_apps_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updatesAndStartup']['title']].check_for_apps_updates_combobox.combo_box.currentIndex()
        #TODO: checkbox


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
            'startAtLaunch': self.start_at_launch
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
            self.start_at_launch = extra_data['startAtLaunch']

        except: self.save()
#----------------------------------------------------------------------
