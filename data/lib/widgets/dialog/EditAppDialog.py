#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal, QSize
from datetime import datetime
from data.lib.QtUtils import QFileButton, QFiles, QGridFrame, QGridWidget, QScrollableGridWidget, QSidePanelWidget, QSidePanelItem, QNamedLineEdit, QFlowScrollableWidget, QIconWidget, QNamedComboBox, QNamedToggleButton
import json, os
from data.lib.widgets import Category
#----------------------------------------------------------------------

    # Class
class EditAppDialog(QDialog):
    general_tab_icon = None
    advanced_tab_icon = None
    updates_tab_icon = None
    icon_tab_icon = None
    icon_file_button_icon = None
    folder_file_button_icon = None
    icon_path = None
    icon_size = 64
    refresh_app_info = Signal()

    categories: list[Category] = []

    def __init__(self, parent = None, lang = {}, name: str = '', tag_name: str = '', release: str = '', created_at: datetime = '', raw_icon: str = '', cwd: str = '', command: str = '', path: str = '', check_for_updates: int = 4, auto_update: bool = True, category: str = None) -> None:
        super().__init__(parent)

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.path = path
        self.lang = lang
        self.name = name
        self.tag_name = tag_name
        self.release = release
        self.created_at = created_at
        self.raw_icon = raw_icon
        self.cwd = cwd
        self.command = command
        self.check_for_updates = check_for_updates
        self.auto_update = auto_update
        self.category = category

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(lang['QPushButton']['apply'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        self.setWindowTitle(lang['title'].replace('%s', name))

        self.frame = QGridFrame()
        self.frame.grid_layout.addWidget(right_buttons, 0, 0)
        self.frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self.frame.grid_layout.setSpacing(0)
        self.frame.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.frame.setProperty('border-top', True)
        self.frame.setProperty('border-bottom', True)
        self.frame.setProperty('border-left', True)
        self.frame.setProperty('border-right', True)

        self.root = QSidePanelWidget(width = 220)

        self.tabs = {}
        self.tabs[self.lang['QSidePanel']['general']['title']] = self.general_tab_widget()
        self.tabs[self.lang['QSidePanel']['advanced']['title']] = self.advanced_tab_widget()
        if self.release in ['official', 'prerelease']: self.tabs[self.lang['QSidePanel']['updates']['title']] = self.updates_tab_widget()
        self.tabs[self.lang['QSidePanel']['icon']['title']] = self.icon_tab_widget()

        for k, v in self.tabs.items():
            self.root.add_widget(v[0], k, v[1])

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

        self._layout.addWidget(self.root, 0, 0)
        self._layout.addWidget(self.frame, 1, 0)

        self.setLayout(self._layout)


        w = self.tabs[self.lang['QSidePanel']['icon']['title']][0]

        for index, icon in enumerate(['../none.svg'] + os.listdir(self.icon_path)):
            if not icon.endswith('.svg'): continue
            b = self.generate_button(f'{self.icon_path}/{icon}')
            w.bottom.scroll_layout.addWidget(b)

        w.bottom.setFixedHeight(w.bottom.heightMM() + 16) # Cuz weird things happen when resizing the window



    def general_tab_widget(self) -> tuple[QWidget, str]:
        lang = self.lang['QSidePanel']['general']

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self.textGroup(lang['QLabel']['name']['title'], lang['QLabel']['name']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        app_name = QLabel(self.name)
        app_name.setProperty('title', True)
        app_name.setWordWrap(True)
        app_name.setFixedHeight(app_name.sizeHint().height())
        root_frame.grid_layout.addWidget(app_name, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(app_name, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['category']['title'], lang['QLabel']['category']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.app_category = QNamedComboBox(None, lang['QNamedComboBox']['category']['title'])
        self.app_category.setProperty('title', True)
        self.app_category.combo_box.addItems([lang['QNamedComboBox']['category']['values']['none']] + [cat.keyword for cat in self.categories])
        if self.category:
            if self.category in [cat.keyword for cat in self.categories]:
                self.app_category.combo_box.setCurrentText(self.category)
        root_frame.grid_layout.addWidget(self.app_category, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.app_category, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['version']['title'], lang['QLabel']['version']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        app_version = QLabel(self.tag_name if self.tag_name else '???')
        app_version.setProperty('title', True)
        app_version.setWordWrap(True)
        app_version.setFixedHeight(app_version.sizeHint().height())
        root_frame.grid_layout.addWidget(app_version, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(app_version, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['release']['title'], lang['QLabel']['release']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        app_release = QLabel(lang['QLabel']['release'][self.release])
        app_release.setProperty('title', True)
        app_release.setWordWrap(True)
        app_release.setFixedHeight(app_release.sizeHint().height())
        root_frame.grid_layout.addWidget(app_release, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(app_release, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['releaseDate']['title'], lang['QLabel']['releaseDate']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        app_release_date = QLabel(self.created_at.strftime('%d/%m/%Y %H:%M:%S')) if self.created_at else QLabel('???')
        app_release_date.setProperty('title', True)
        app_release_date.setWordWrap(True)
        app_release_date.setFixedHeight(app_release_date.sizeHint().height())
        root_frame.grid_layout.addWidget(app_release_date, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(app_release_date, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['location']['title'], lang['QLabel']['location']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        app_location = QLabel(self.path)
        app_location.setProperty('title', True)
        app_location.setWordWrap(True)
        app_location.setFixedHeight(app_location.sizeHint().height())
        root_frame.grid_layout.addWidget(app_location, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(app_location, Qt.AlignmentFlag.AlignLeft)


        return widget, self.general_tab_icon



    def advanced_tab_widget(self) -> tuple[QWidget, str]:
        lang = self.lang['QSidePanel']['advanced']

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self.textGroup(lang['QLabel']['cwd']['title'], lang['QLabel']['cwd']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.cwd_button = QFileButton(
            self, lang['QFileButton']['cwd'],
            self.cwd,
            self.folder_file_button_icon,
            QFiles.Dialog.ExistingDirectory
        )
        root_frame.grid_layout.addWidget(self.cwd_button, root_frame.grid_layout.count(), 0)

        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['command']['title'], lang['QLabel']['command']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.command_lineedit = QNamedLineEdit(name = lang['QNamedLineEdit']['command'], placeholder = 'null')
        self.command_lineedit.setText(self.command)
        root_frame.grid_layout.addWidget(self.command_lineedit, root_frame.grid_layout.count(), 0)


        return widget, self.advanced_tab_icon



    def updates_tab_widget(self) -> tuple[QWidget, str]:
        lang = self.lang['QSidePanel']['updates']

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self.textGroup(lang['QLabel']['checkForUpdates']['title'], lang['QLabel']['checkForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        self.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
        ])
        self.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(self.check_for_updates_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)

        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['autoUpdate']['title'], lang['QLabel']['autoUpdate']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.auto_update_checkbox = QNamedToggleButton()
        self.auto_update_checkbox.setText(lang['QToggleButton']['autoUpdate'])
        self.auto_update_checkbox.setChecked(self.auto_update)
        root_frame.grid_layout.addWidget(self.auto_update_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.auto_update_checkbox, Qt.AlignmentFlag.AlignLeft)


        return widget, self.updates_tab_icon



    def icon_tab_widget(self) -> tuple[QWidget, str]:
        lang = self.lang['QSidePanel']['icon']

        widget = QGridFrame()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.grid_layout.addWidget(root_frame, 0, 0)
        widget.grid_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        widget.top = QGridFrame()
        widget.top.grid_layout.setSpacing(16)
        widget.top.grid_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.top, root_frame.grid_layout.count(), 0)

        label = self.textGroup(lang['QLabel']['icon']['title'], lang['QLabel']['icon']['description'])
        widget.top.grid_layout.addWidget(label, 0, 0, 1, 2)

        widget.top.icon_group = self.icon_with_text(self.raw_icon, lang['QLabel']['currentIcon'])
        widget.top.grid_layout.addWidget(widget.top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, lang['QFileButton']['icon'],
            self.raw_icon,
            self.icon_file_button_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.svg *.ico *.png *.jpg *.jpeg *.exe *.bat *.sh);;SVG (*.svg);;ICO (*.ico);;PNG (*.png);;JPEG (*.jpg *.jpeg);;Executable (*.exe);;Batch (*.bat);;Shell (*.sh)'
        )
        self.icon_button.path_changed.connect(self.icon_file_button_path_changed)
        self.icon_button.setMinimumWidth(int(self.icon_button.sizeHint().width() * 1.25))
        widget.top.grid_layout.addWidget(self.icon_button, 1, 1)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self.textGroup(lang['QLabel']['predefinedIcons']['title'], lang['QLabel']['predefinedIcons']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)


        widget.bottom = QFlowScrollableWidget()
        widget.bottom.scroll_layout.setSpacing(16)
        widget.bottom.scroll_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.bottom, root_frame.grid_layout.count(), 0)


        return widget, self.icon_tab_icon



    def update(self, path: str = None) -> None:
        if not path: return
        if not os.path.isfile(path): return

        w = self.tabs[self.lang['QSidePanel']['icon']['title']][0]
        self.icon_button.setPath(path)
        w.top.icon_group.icon_widget.icon = path



    def icon_file_button_path_changed(self, path: str = None) -> None:
        if not path: return
        self.update(path)



    def textGroup(self, title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(0)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setRowStretch(2, 1)

        return widget



    def icon_with_text(self, icon: str = None, text: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = QIconWidget(None, icon, QSize(40, 40), True)
        widget.grid_layout.addWidget(widget.icon_widget, 1, 0)
        widget.grid_layout.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.grid_layout.setRowStretch(2, 1)

        return widget



    def generate_button(self, path: str = None) -> QIconWidget:
        button = QIconWidget(None, path, QSize(self.icon_size, self.icon_size))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('imagebutton', True)
        button.mouseReleaseEvent = lambda _: self.icon_click(os.path.abspath(path))

        return button



    def icon_click(self, path: str = None) -> None:
        if not path: return
        if not os.path.exists(path) or not os.path.isfile(path): return

        self.update(path)



    def exec(self) -> None:
        if super().exec():
            with open(f'{self.path}/manifest.json', 'r', encoding = 'utf-8') as infile:
                data = json.load(infile)
            if self.cwd_button.path(): data['cwd'] = self.cwd_button.path()
            if self.command_lineedit.text(): data['command'] = self.command_lineedit.text()
            if self.icon_button.path(): data['icon'] = self.icon_button.path()
            if self.release in ['official', 'prerelease']:
                data['checkForUpdates'] = self.check_for_updates_combobox.combo_box.currentIndex()
                data['autoUpdate'] = self.auto_update_checkbox.isChecked()
            if self.app_category.combo_box.currentText(): data['category'] = self.app_category.combo_box.currentText() if self.app_category.combo_box.currentIndex() != 0 else None

            with open(f'{self.path}/manifest.json', 'w', encoding = 'utf-8') as outfile:
                json.dump(data, outfile, indent = 4)

            self.refresh_app_info.emit()
        return None
#----------------------------------------------------------------------
