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

from data.lib.QtUtils import QFiles, QNamedLineEdit, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QDragList, QBaseApplication, QColorSet
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, app: QBaseApplication, save_path: str = './data/save.dat', main_color_set: QColorSet = None, neutral_color_set: QColorSet = None) -> None:
        self.platform = PlatformType.from_qplatform(app.platform)
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
        self.exit_during_app_run_notif = True
        self.update_done_notif = True # TODO: Implement this functionallity
        self.update_failed_notif = True # TODO: Implement this functionallity
        self.app_install_done_notif = True
        self.app_install_failed_notif = True
        self.app_uninstall_done_notif = True
        self.app_uninstall_failed_notif = True
        self.app_exec_failed_notif = True
        self.request_worker_failed_notif = True
        self.process_already_running_notif = True
        self.process_ended_notif = True
        self.process_killed_notif = True

        super().__init__(app, save_path, main_color_set = main_color_set, neutral_color_set = neutral_color_set)


    @property
    def category_keywords(self) -> list[str]:
        return [category.keyword for category in self.categories]


    def _settings_menu_extra(self):
        return {
            self.get_lang_data('QSettingsDialog.QSidePanel.installs.title'): (self.settings_menu_installs(), f'{self.get_icon_dir()}/sidepanel/installs.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.updates.title'): (self.settings_menu_updates(), f'{self.get_icon_dir()}/sidepanel/updates.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.interface.title'): (self.settings_menu_interface(), f'{self.get_icon_dir()}/sidepanel/interface.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.notification.title'): (self.settings_menu_notification(), f'{self.get_icon_dir()}/sidepanel/notification.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.token.title'): (self.settings_menu_github(), f'{self.get_icon_dir()}/sidepanel/token.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.categories.title'): (self.settings_menu_categories(), f'{self.get_icon_dir()}/sidepanel/categories.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.followedApps.title'): (self.settings_menu_followed_apps(), f'{self.get_icon_dir()}/sidepanel/followedApps.png')
        }, self.get_extra


    def settings_menu_installs(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.installs')
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.installsLocation.title'), lang.get_data('QLabel.installsLocation.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.installs_folder_button = QFileButton(
            None,
            lang.get_data('QFileButton.installsLocation'),
            self.apps_folder,
            f'{self.get_icon_dir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.installs_folder_button.setFixedWidth(350)
        root_frame.layout_.addWidget(widget.installs_folder_button, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.installs_folder_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.downloadsLocation.title'), lang.get_data('QLabel.downloadsLocation.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.downloads_folder_button = QFileButton(
            None,
            lang.get_data('QFileButton.downloadsLocation'),
            self.downloads_folder,
            f'{self.get_icon_dir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.downloads_folder_button.setFixedWidth(350)
        root_frame.layout_.addWidget(widget.downloads_folder_button, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.downloads_folder_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_updates(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.updates')
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.checkForUpdates.title'), lang.get_data('QLabel.checkForUpdates.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.checkForUpdates.title'))
        widget.check_for_updates_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.checkForUpdates.values.never'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.daily'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.weekly'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.monthly'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.atLaunch')
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.layout_.addWidget(widget.check_for_updates_combobox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.checkForAppsUpdates.title'), lang.get_data('QLabel.checkForAppsUpdates.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.check_for_apps_updates_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.checkForAppsUpdates.title'))
        widget.check_for_apps_updates_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.checkForAppsUpdates.values.never'),
            lang.get_data('QNamedComboBox.checkForAppsUpdates.values.daily'),
            lang.get_data('QNamedComboBox.checkForAppsUpdates.values.weekly'),
            lang.get_data('QNamedComboBox.checkForAppsUpdates.values.monthly'),
            lang.get_data('QNamedComboBox.checkForAppsUpdates.values.atLaunch')
        ])
        widget.check_for_apps_updates_combobox.combo_box.setCurrentIndex(self.check_for_apps_updates)
        root_frame.layout_.addWidget(widget.check_for_apps_updates_combobox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.check_for_apps_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.newAppsCheckForUpdates.title'), lang.get_data('QLabel.newAppsCheckForUpdates.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.new_apps_check_for_updates_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.newAppsCheckForUpdates.title'))
        widget.new_apps_check_for_updates_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.newAppsCheckForUpdates.values.never'),
            lang.get_data('QNamedComboBox.newAppsCheckForUpdates.values.daily'),
            lang.get_data('QNamedComboBox.newAppsCheckForUpdates.values.weekly'),
            lang.get_data('QNamedComboBox.newAppsCheckForUpdates.values.monthly'),
            lang.get_data('QNamedComboBox.newAppsCheckForUpdates.values.atLaunch')
        ])
        widget.new_apps_check_for_updates_combobox.combo_box.setCurrentIndex(self.new_apps_check_for_updates)
        root_frame.layout_.addWidget(widget.new_apps_check_for_updates_combobox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.new_apps_check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.newAppsAutoUpdate.title'), lang.get_data('QLabel.newAppsAutoUpdate.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.new_apps_auto_update_checkbox = QNamedToggleButton()
        widget.new_apps_auto_update_checkbox.setText(lang.get_data('QToggleButton.newAppsAutoUpdate'))
        widget.new_apps_auto_update_checkbox.setChecked(self.new_apps_auto_update)
        root_frame.layout_.addWidget(widget.new_apps_auto_update_checkbox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.new_apps_auto_update_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_interface(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.interface')
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        # label = QSettingsDialog.textGroup(lang.get_data('QLabel.startAtLaunch.title'), lang.get_data('QLabel.startAtLaunch.description'))
        # root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang.get_data('QToggleButton.startAtLaunch'))
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        # root_frame.layout_.addWidget(widget.start_at_launch_checkbox, root_frame.layout_.count(), 0)
        # root_frame.layout_.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.minimizeToTray.title'), lang.get_data('QLabel.minimizeToTray.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.minimize_to_tray_checkbox = QNamedToggleButton()
        widget.minimize_to_tray_checkbox.setText(lang.get_data('QToggleButton.minimizeToTray'))
        widget.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
        root_frame.layout_.addWidget(widget.minimize_to_tray_checkbox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.minimize_to_tray_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.compactPaths.title'), lang.get_data('QLabel.compactPaths.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.compact_paths_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.compactPaths.title'))
        widget.compact_paths_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.compactPaths.values.auto'),
            lang.get_data('QNamedComboBox.compactPaths.values.enabled'),
            lang.get_data('QNamedComboBox.compactPaths.values.disabled')
        ])
        widget.compact_paths_combobox.combo_box.setCurrentIndex(self.compact_paths)
        root_frame.layout_.addWidget(widget.compact_paths_combobox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.compact_paths_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_notification(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.notification')
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        all_checkboxes: list[QNamedToggleButton] = []

        def check_all(checked: bool):
            for checkbox in all_checkboxes:
                checkbox.setChecked(checked)

        def invert_all():
            for checkbox in all_checkboxes:
                checkbox.setChecked(not checkbox.isChecked())

        buttonframe = QGridFrame()
        buttonframe.layout_.setSpacing(16)
        buttonframe.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(buttonframe, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(buttonframe, Qt.AlignmentFlag.AlignTop)

        button = QPushButton(lang.get_data('QPushButton.checkAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(True))
        buttonframe.layout_.addWidget(button, 0, buttonframe.layout_.count())

        button = QPushButton(lang.get_data('QPushButton.uncheckAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(False))
        buttonframe.layout_.addWidget(button, 0, buttonframe.layout_.count())

        button = QPushButton(lang.get_data('QPushButton.invertAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: invert_all())
        buttonframe.layout_.addWidget(button, 1, 0, 1, 2)


        subframe = QGridFrame()
        subframe.layout_.setSpacing(16)
        subframe.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(subframe, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(subframe, Qt.AlignmentFlag.AlignTop)


        def generate_notif(key: str, checked: bool) -> QNamedToggleButton:
            frame = QFrame()
            frame.setProperty('border-top', True)
            frame.setFixedHeight(1)
            subframe.layout_.addWidget(frame, subframe.layout_.count(), 0)

            label = QSettingsDialog._text_group(lang.get_data(f'QLabel.{key}.title'), lang.get_data(f'QLabel.{key}.description'))
            subframe.layout_.addWidget(label, subframe.layout_.count(), 0)

            w = QNamedToggleButton()
            w.setText(lang.get_data('QToggleButton')[key])
            w.setChecked(checked)
            subframe.layout_.addWidget(w, subframe.layout_.count(), 0)
            subframe.layout_.setAlignment(w, Qt.AlignmentFlag.AlignLeft)

            all_checkboxes.append(w)

            return w


        widget.goes_to_tray_notif_checkbox = generate_notif('goesToTray', self.goes_to_tray_notif)
        widget.exit_during_work_notif_checkbox = generate_notif('exitDuringWork', self.exit_during_work_notif)
        widget.exit_during_app_run_notif_checkbox = generate_notif('exitDuringAppRun', self.exit_during_app_run_notif)
        widget.update_done_notif_checkbox = generate_notif('updateDone', self.update_done_notif)
        widget.update_failed_notif_checkbox = generate_notif('updateFailed', self.update_failed_notif)
        widget.app_install_done_notif_checkbox = generate_notif('appInstallDone', self.app_install_done_notif)
        widget.app_install_failed_notif_checkbox = generate_notif('appInstallFailed', self.app_install_failed_notif)
        widget.app_uninstall_done_notif_checkbox = generate_notif('appUninstallDone', self.app_uninstall_done_notif)
        widget.app_uninstall_failed_notif_checkbox = generate_notif('appUninstallFailed', self.app_uninstall_failed_notif)
        widget.app_exec_failed_notif_checkbox = generate_notif('appExecFailed', self.app_exec_failed_notif)
        widget.request_worker_failed_notif_checkbox = generate_notif('requestWorkerFailed', self.request_worker_failed_notif)
        widget.process_already_running_notif_checkbox = generate_notif('processAlreadyRunning', self.process_already_running_notif)
        widget.process_ended_notif_checkbox = generate_notif('processEnded', self.process_ended_notif)
        widget.process_killed_notif_checkbox = generate_notif('processKilled', self.process_killed_notif)

        return widget



    def settings_menu_github(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.token')
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.github.title'), lang.get_data('QLabel.github.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        label = QLabel(f'<a href=\"https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">{lang["QLabel"]["github"]["createToken"]}</a>')
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.github_token_lineedit = QNamedLineEdit(None, 'null', lang.get_data('QNamedLineEdit.github'))
        widget.github_token_lineedit.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        widget.github_token_lineedit.setText(self.token['github'])
        widget.github_token_lineedit.setFixedWidth(350)
        root_frame.layout_.addWidget(widget.github_token_lineedit, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.github_token_lineedit, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_followed_apps(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.followedApps')
        key = 'url'
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.followedApps.title'), lang.get_data('QLabel.followedApps.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.followed_apps_list = QDragList()
        root_frame.layout_.addWidget(widget.followed_apps_list, root_frame.layout_.count(), 0)

        for app in self.followed_apps:
            widget.followed_apps_list.add_item(SettingsListNamedItem(lang.get_data('SettingsListNamedItem'), key, app))

        button = QPushButton()
        button.setIcon(self.get_icon('pushbutton/plus.png'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: widget.followed_apps_list.add_item(SettingsListNamedItem(lang.get_data('SettingsListNamedItem'), key, '')))
        root_frame.layout_.addWidget(button, root_frame.layout_.count(), 0)


        return widget



    def settings_menu_categories(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.categories')
        key = 'category'
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.categories.title'), lang.get_data('QLabel.categories.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.categories_list = QDragList()
        root_frame.layout_.addWidget(widget.categories_list, root_frame.layout_.count(), 0)

        for cat in self.categories:
            widget.categories_list.add_item(CategoryListNamedItem(lang.get_data('CategoryListNamedItem'), key, cat))

        button = QPushButton()
        button.setIcon(self.get_icon('pushbutton/plus.png'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: widget.categories_list.add_item(CategoryListNamedItem(lang.get_data('CategoryListNamedItem'), key, Category('', './data/icons/questionMark.svg'))))
        root_frame.layout_.addWidget(button, root_frame.layout_.count(), 0)


        return widget



    def get_extra(self, extra_tabs: dict = {}):
        self.apps_folder = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.installs.title')].installs_folder_button.path()
        self.downloads_folder = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.installs.title')].downloads_folder_button.path()
        self.check_for_updates = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.updates.title')].check_for_updates_combobox.combo_box.currentIndex()
        self.check_for_apps_updates = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.updates.title')].check_for_apps_updates_combobox.combo_box.currentIndex()
        self.new_apps_check_for_updates = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.updates.title')].new_apps_check_for_updates_combobox.combo_box.currentIndex()
        self.new_apps_auto_update = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.updates.title')].new_apps_auto_update_checkbox.isChecked()

        self.start_at_launch = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].start_at_launch_checkbox.isChecked()
        self.minimize_to_tray = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].minimize_to_tray_checkbox.isChecked()

        self.compact_paths = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].compact_paths_combobox.combo_box.currentIndex()

        self.token['github'] = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.token.title')].github_token_lineedit.text()

        self.categories = self.without_duplicates([Category(item.keyword, item.icon) for item in extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.categories.title')].categories_list.items if item.keyword != ''])

        self.followed_apps = self.without_duplicates([item.keyword for item in extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.followedApps.title')].followed_apps_list.items if self.valid_url(item.keyword) if item.keyword != ''])

        self.goes_to_tray_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].goes_to_tray_notif_checkbox.isChecked()
        self.exit_during_work_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].exit_during_work_notif_checkbox.isChecked()
        self.exit_during_app_run_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].exit_during_app_run_notif_checkbox.isChecked()
        self.update_done_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].update_done_notif_checkbox.isChecked()
        self.update_failed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].update_failed_notif_checkbox.isChecked()
        self.app_install_done_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].app_install_done_notif_checkbox.isChecked()
        self.app_install_failed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].app_install_failed_notif_checkbox.isChecked()
        self.app_uninstall_done_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].app_uninstall_done_notif_checkbox.isChecked()
        self.app_uninstall_failed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].app_uninstall_failed_notif_checkbox.isChecked()
        self.app_exec_failed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].app_exec_failed_notif_checkbox.isChecked()
        self.request_worker_failed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].request_worker_failed_notif_checkbox.isChecked()
        self.process_already_running_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].process_already_running_notif_checkbox.isChecked()
        self.process_ended_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].process_ended_notif_checkbox.isChecked()
        self.process_killed_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].process_killed_notif_checkbox.isChecked()



    def valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


    def without_duplicates(self, l: list) -> list:
        return list(dict.fromkeys(l))


    def _save_extra_data(self) -> dict:
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
            'exitDuringAppRunNotif': self.exit_during_app_run_notif,
            'updateDoneNotif': self.update_done_notif,
            'updateFailedNotif': self.update_failed_notif,
            'appInstallDoneNotif': self.app_install_done_notif,
            'appInstallFailedNotif': self.app_install_failed_notif,
            'appUninstallDoneNotif': self.app_uninstall_done_notif,
            'appUninstallFailedNotif': self.app_uninstall_failed_notif,
            'appExecFailedNotif': self.app_exec_failed_notif,
            'requestWorkerFailedNotif': self.request_worker_failed_notif,
            'processAlreadyRunningNotif': self.process_already_running_notif,
            'processEndedNotif': self.process_ended_notif,
            'processKilledNotif': self.process_killed_notif
        }

    def _load_extra_data(self, extra_data: dict = ..., reload: list = [], reload_all: bool = False) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.apps['official'] = extra_data['apps.official']
        with exc: self.apps['pre'] = extra_data['apps.pre']
        with exc: self.apps['custom'] = extra_data['apps.custom']

        with exc: self.apps_folder = extra_data['folders.apps']
        with exc: self.downloads_folder = extra_data['folders.downloads']

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
        with exc: self.exit_during_app_run_notif = extra_data['exitDuringAppRunNotif']
        with exc: self.update_done_notif = extra_data['updateDoneNotif']
        with exc: self.update_failed_notif = extra_data['updateFailedNotif']
        with exc: self.app_install_done_notif = extra_data['appInstallDoneNotif']
        with exc: self.app_install_failed_notif = extra_data['appInstallFailedNotif']
        with exc: self.app_uninstall_done_notif = extra_data['appUninstallDoneNotif']
        with exc: self.app_uninstall_failed_notif = extra_data['appUninstallFailedNotif']
        with exc: self.app_exec_failed_notif = extra_data['appExecFailedNotif']
        with exc: self.request_worker_failed_notif = extra_data['requestWorkerFailedNotif']
        with exc: self.process_already_running_notif = extra_data['processAlreadyRunningNotif']
        with exc: self.process_ended_notif = extra_data['processEndedNotif']
        with exc: self.process_killed_notif = extra_data['processKilledNotif']

        return res

    def export_extra_data(self) -> dict:
        dct = self._save_extra_data()
        del dct['apps']
        return dct
#----------------------------------------------------------------------
