#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from collections import namedtuple
from data.lib.QtUtils import QGridFrame, QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QFileButton, QFiles, QBaseApplication, QNamedComboBox, QNamedToggleButton
from data.lib.widgets import Category
#----------------------------------------------------------------------

    # Class
class CustomizeInstallationDialog(QDialog):
    download_custom_data = namedtuple('download_custom_data', ['download_data', 'install_folder', 'category', 'check_for_updates', 'auto_update'])

    _install_location_icon = None

    icon_size = 64
    categories: list[Category] = []

    default_category: str = None
    default_install_folder: str = './data/apps/'
    default_check_for_updates: int = 4
    default_auto_update: bool = True

    @staticmethod
    def init(app: QBaseApplication) -> None:
        CustomizeInstallationDialog._install_location_icon = f'{app.save_data.get_icon_dir()}filebutton/folder.png'

    def __init__(self, parent = None, lang = {}, download_data = None) -> None:
        super().__init__(parent)

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._lang = lang
        self.download_data = download_data

        right_buttons = QGridWidget()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        self._cancel_button = QPushButton(lang['QPushButton']['cancel'])
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_button.clicked.connect(self.reject)
        self._cancel_button.setProperty('color', 'white')
        self._cancel_button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(self._cancel_button, 0, 0)

        self._install_button = QPushButton(lang['QPushButton']['install'])
        self._install_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._install_button.clicked.connect(self.accept)
        self._install_button.setProperty('color', 'main')
        right_buttons.layout_.addWidget(self._install_button, 0, 1)

        self.setWindowTitle(lang['title'].replace('%s', download_data.name))

        self._root = QSlidingStackedWidget()
        self._root.set_orientation(Qt.Orientation.Horizontal)
        self._pages = {}

        root_frame = QGridFrame()
        root_frame.layout_.addWidget(self._root, 0, 0)
        root_frame.layout_.setSpacing(0)
        root_frame.layout_.setContentsMargins(16, 16, 16, 16)

        self._pages['general'] = self._menu_general()
        self._root.addWidget(self._pages['general'])

        self._pages['updates'] = self.settings_menu_updates()
        self._root.addWidget(self._pages['updates'])

        if len(self.download_data.files_data) > 1:
            self._pages['which_data'] = self._menu_which_data()
            self._root.addWidget(self._pages['which_data'])

        self._frame = QGridFrame()
        self._frame.layout_.addWidget(right_buttons, 0, 0)
        self._frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self._frame.layout_.setSpacing(0)
        self._frame.layout_.setContentsMargins(16, 16, 16, 16)
        self._frame.setProperty('border-top', True)
        self._frame.setProperty('border-bottom', True)
        self._frame.setProperty('border-left', True)
        self._frame.setProperty('border-right', True)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)) // 2, int(parent.window().size().height() * (13 / 15)))

        self._layout.addWidget(root_frame, 0, 0)
        self._layout.addWidget(self._frame, 1, 0)

        self.setLayout(self._layout)
        self._update_keywords()


    def _menu_general(self) -> QWidget:
        lang = self._lang['QSlidingStackedWidget']
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = CustomizeInstallationDialog._text_group(lang['QLabel']['installLocation']['title'], lang['QLabel']['installLocation']['description'].replace('%s', self.download_data.name))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        l = {
            "title": lang['QFileButton']['installLocation']['title'],
            "dialog": lang['QFileButton']['installLocation']['dialog'].replace('%s', self.download_data.name)
        }

        widget.installs_folder_button = QFileButton(
            None,
            l,
            self.default_install_folder,
            self._install_location_icon,
            QFiles.Dialog.ExistingDirectory
        )
        widget.installs_folder_button.setFixedWidth(350)
        root_frame.layout_.addWidget(widget.installs_folder_button, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.installs_folder_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = CustomizeInstallationDialog._text_group(lang['QLabel']['category']['title'], lang['QLabel']['category']['description'].replace('%s', self.download_data.name))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.category = QNamedComboBox(None, lang['QNamedComboBox']['category']['title'])
        widget.category.setProperty('title', True)
        widget.category.combo_box.addItems([lang['QNamedComboBox']['category']['values']['none']] + [cat.keyword for cat in self.categories])
        if self.default_category:
            if self.default_category in [cat.keyword for cat in self.categories]:
                widget.category.combo_box.setCurrentText(self.default_category)

        root_frame.layout_.addWidget(widget.category, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.category, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_updates(self):
        lang = self._lang['QSlidingStackedWidget']
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 16, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = CustomizeInstallationDialog._text_group(lang['QLabel']['checkForUpdates']['title'], lang['QLabel']['checkForUpdates']['description'])
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        widget.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.default_check_for_updates)
        root_frame.layout_.addWidget(widget.check_for_updates_combobox, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = CustomizeInstallationDialog._text_group(lang['QLabel']['autoUpdate']['title'], lang['QLabel']['autoUpdate']['description'])
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        widget.auto_update = QNamedToggleButton()
        widget.auto_update.setText(lang['QToggleButton']['autoUpdate'])
        widget.auto_update.setChecked(self.default_auto_update)
        root_frame.layout_.addWidget(widget.auto_update, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(widget.auto_update, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _menu_which_data(self) -> QWidget:
        lang = self._lang['QSlidingStackedWidget']
        widget = QScrollableGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        widget.layout_.addWidget(root_frame, 0, 0)
        widget.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = CustomizeInstallationDialog._text_group(lang['QLabel']['whichData']['title'], lang['QLabel']['whichData']['description'].replace('%s', self.download_data.name))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        for fd in self.download_data.files_data:
            # TODO: add the ability to select which files to download
            print(fd.link.split('/')[-1], fd.portable)


        return widget



    def _text_group(title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 1, 0)
        widget.layout_.setRowStretch(2, 1)

        return widget

    def accept(self) -> None:
        if self._root.current_index == self._root.count() - 1:
            return super().accept()
        self._root.slide_in_next()
        self._update_keywords()

    def reject(self) -> None:
        if self._root.current_index == 0:
            return super().reject()
        self._root.slide_in_previous()
        self._update_keywords()

    def _update_keywords(self) -> None:
        if self._root.current_index < self._root.count() - 1:
            self._install_button.setText(self._lang['QPushButton']['next'])
        else:
            self._install_button.setText(self._lang['QPushButton']['install'])

        if self._root.current_index == 0:
            self._cancel_button.setText(self._lang['QPushButton']['cancel'])
        else:
            self._cancel_button.setText(self._lang['QPushButton']['back'])

    def exec(self) -> download_custom_data | None:
        if super().exec():
            return self.download_custom_data(
                self.download_data,
                self._pages['general'].installs_folder_button.path(),
                self._pages['general'].category.combo_box.currentText() if self._pages['general'].category.combo_box.currentText() != self._lang['QSlidingStackedWidget']['QNamedComboBox']['category']['values']['none'] else None,
                self._pages['updates'].check_for_updates_combobox.combo_box.currentIndex(),
                self._pages['updates'].auto_update.isChecked()
            )
        return None
#----------------------------------------------------------------------
