#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from data.lib.qtUtils import QFileButton, QFiles, QGridFrame, QGridWidget, QScrollableGridWidget, QSidePanelWidget, QSidePanelItem, QNamedLineEdit, QNamedTextEdit, QFlowWidget
import yaml, os
#----------------------------------------------------------------------

    # Class
class EditProjectDialog(QDialog):
    general_tab_icon = None
    icon_tab_icon = None
    icon_file_button_icon = None
    icon_path = None
    icon_size = 64
    refresh_projects = pyqtSignal()

    def __init__(self, parent = None, path: str = '', lang = {}):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.path = path
        self.lang = lang

        with open(f'{self.path}/ProjectSettings/ProjectSettings.pylite-asset', 'r', encoding = 'utf-8') as infile:
            self.data = yaml.load(infile, Loader = yaml.FullLoader)

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

        self.setWindowTitle(lang['title'])

        self.frame = QGridFrame()
        self.frame.grid_layout.addWidget(right_buttons, 0, 0)
        self.frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self.frame.grid_layout.setSpacing(0)
        self.frame.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.frame.setProperty('border-top', True)
        self.frame.setProperty('border-bottom', True)
        self.frame.setProperty('border-left', True)
        self.frame.setProperty('border-right', True)

        self.root = QSidePanelWidget(widget = QGridWidget(), width = 220)
        self.root.widget.layout().setSpacing(0)
        self.root.widget.layout().setContentsMargins(16, 16, 16, 16)

        def clear_root_widget(widget: QWidget):
            for i in reversed(range(self.root.widget.layout().count())):
                self.root.widget.layout().itemAt(i).widget().setHidden(True)
            widget.setHidden(False)

        def show_tab(widget, index):
            clear_root_widget(widget)
            self.root.sidepanel.set_current_index(index)

        self.tabs = {self.lang['QSidePanel']['general']['title']: self.general_tab_widget(), self.lang['QSidePanel']['icon']['title']: self.icon_tab_widget()}


        kLst = list(self.tabs.keys())
        sendParam = lambda w, i: lambda: show_tab(w, i)
        for index, key in enumerate(kLst):
            self.root.widget.layout().addWidget(self.tabs[key][0])
            self.root.sidepanel.add_item(QSidePanelItem(key, self.tabs[key][1], sendParam(self.tabs[key][0], index)))

        show_tab(self.tabs[self.lang['QSidePanel']['general']['title']][0], 0)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

        self.layout.addWidget(self.root, 0, 0)
        self.layout.addWidget(self.frame, 1, 0)

        self.setLayout(self.layout)


        w = self.tabs[self.lang['QSidePanel']['icon']['title']][0]

        for index, icon in enumerate(['../none.svg'] + os.listdir(self.icon_path)):
            b = self.generate_button(f'{self.icon_path}/{icon}')
            w.bottom.scroll_layout.addWidget(b)

        w.bottom.setFixedHeight(w.bottom.heightMM() + 16) # Cuz weird things happen when resizing the window



    def general_tab_widget(self):
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
        root_frame.grid_layout.addWidget(label, 0, 0)

        self.project_name = QNamedLineEdit(name = lang['QNamedLineEdit']['name'], placeholder = self.data['EditorSettings']['name'])
        self.project_name.setFixedWidth(int(self.project_name.sizeHint().width() * 2))
        root_frame.grid_layout.addWidget(self.project_name, 1, 0)
        root_frame.grid_layout.setAlignment(self.project_name, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = self.textGroup(lang['QLabel']['description']['title'], lang['QLabel']['description']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        self.project_description = QNamedTextEdit(name = lang['QNamedTextEdit']['description'], placeholder = self.data['EditorSettings']['description'])
        self.project_description.setFixedWidth(int(self.project_description.sizeHint().width() * 2))
        root_frame.grid_layout.addWidget(self.project_description, 4, 0)
        root_frame.grid_layout.setAlignment(self.project_description, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 5, 0)


        label = self.textGroup(lang['QLabel']['version']['title'], lang['QLabel']['version']['description'])
        root_frame.grid_layout.addWidget(label, 6, 0)

        self.project_version = QNamedLineEdit(name = lang['QNamedLineEdit']['version'], placeholder = self.data['EditorSettings']['version'])
        self.project_version.setFixedWidth(int(self.project_version.sizeHint().width() * 2))
        root_frame.grid_layout.addWidget(self.project_version, 7, 0)
        root_frame.grid_layout.setAlignment(self.project_version, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 8, 0)


        label = self.textGroup(lang['QLabel']['location']['title'], lang['QLabel']['location']['description'])
        root_frame.grid_layout.addWidget(label, 9, 0)

        project_path = QLabel(self.path)
        project_path.setProperty('title', True)
        project_path.setWordWrap(True)
        project_path.setFixedHeight(project_path.sizeHint().height())
        root_frame.grid_layout.addWidget(project_path, 10, 0)
        root_frame.grid_layout.setAlignment(project_path, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 11, 0)


        label = self.textGroup(lang['QLabel']['lastModified']['title'], lang['QLabel']['lastModified']['description'])
        root_frame.grid_layout.addWidget(label, 12, 0)

        project_last_modified = QLabel(self.data['EditorSettings']['lastModified'].strftime('%d/%m/%Y %H:%M:%S'))
        project_last_modified.setProperty('title', True)
        project_last_modified.setWordWrap(True)
        project_last_modified.setFixedHeight(project_last_modified.sizeHint().height())
        root_frame.grid_layout.addWidget(project_last_modified, 13, 0)
        root_frame.grid_layout.setAlignment(project_last_modified, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 14, 0)


        label = self.textGroup(lang['QLabel']['template']['title'], lang['QLabel']['template']['description'])
        root_frame.grid_layout.addWidget(label, 15, 0)

        project_template = QLabel(self.data['EditorSettings']['template'])
        project_template.setProperty('title', True)
        project_template.setWordWrap(True)
        project_template.setFixedHeight(project_template.sizeHint().height())
        root_frame.grid_layout.addWidget(project_template, 16, 0)
        root_frame.grid_layout.setAlignment(project_template, Qt.AlignmentFlag.AlignLeft)


        return widget, self.general_tab_icon



    def icon_tab_widget(self):
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
        root_frame.grid_layout.addWidget(widget.top, 0, 0)

        label = self.textGroup(lang['QLabel']['icon']['title'], lang['QLabel']['icon']['description'])
        widget.top.grid_layout.addWidget(label, 0, 0, 1, 2)

        widget.top.icon_group = self.icon_with_text(self.data['EditorSettings']['icon'], lang['QLabel']['currentIcon'])
        widget.top.grid_layout.addWidget(widget.top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, lang['QFileButton']['icon'],
            self.data['EditorSettings']['icon'],
            self.icon_file_button_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.svg *.ico *.png *.jpg *.jpeg);;SVG (*.svg);;ICO (*.ico);;PNG (*.png);;JPEG (*.jpg *.jpeg)'
        )
        self.icon_button.path_changed.connect(self.icon_file_button_path_changed)
        self.icon_button.setMinimumWidth(int(self.icon_button.sizeHint().width() * 1.25))
        widget.top.grid_layout.addWidget(self.icon_button, 1, 1)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 1, 0)


        label = self.textGroup(lang['QLabel']['predefinedIcons']['title'], lang['QLabel']['predefinedIcons']['description'])
        root_frame.grid_layout.addWidget(label, 2, 0)


        widget.bottom = QFlowWidget()
        widget.bottom.scroll_layout.setSpacing(16)
        widget.bottom.scroll_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.bottom, 3, 0)


        return widget, self.icon_tab_icon



    def update(self, path: str = None):
        if not path: return
        if not os.path.isfile(path): return

        w = self.tabs[self.lang['QSidePanel']['icon']['title']][0]
        self.icon_button.setPath(path)
        w.top.icon_group.grid_layout.removeWidget(w.top.icon_group.icon_widget)
        w.top.icon_group.icon_widget = self.icon_widget(path)
        w.top.icon_group.grid_layout.addWidget(w.top.icon_group.icon_widget, 1, 0)
        w.top.icon_group.grid_layout.setAlignment(w.top.icon_group.icon_widget, Qt.AlignmentFlag.AlignCenter)



    def icon_file_button_path_changed(self, path: str = None):
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



    def icon_widget(self, icon: str = None, size: int = 40) -> QSvgWidget|QLabel:
        if icon:
            if os.path.isfile(icon):
                if icon.endswith('.svg'): pixmap = QSvgWidget(icon)
                else:
                    pmap = QPixmap(icon).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    pixmap = QLabel()
                    pixmap.setPixmap(pmap)
            else:
                pixmap = QSvgWidget()
        else:
            pixmap = QSvgWidget()

        pixmap.setFixedSize(size, size)

        return pixmap



    def icon_with_text(self, icon: str = None, text: str = ''):
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = self.icon_widget(icon)
        widget.grid_layout.addWidget(widget.icon_widget, 1, 0)
        widget.grid_layout.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.grid_layout.setRowStretch(2, 1)

        return widget



    def generate_button(self, path: str = None):
        button = self.icon_widget(path, self.icon_size)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('imagebutton', True)
        button.mouseReleaseEvent = lambda _: self.icon_click(os.path.abspath(path))

        return button



    def icon_click(self, path: str = None):
        if not path: return
        if not os.path.exists(path) or not os.path.isfile(path): return

        self.update(path)



    def exec(self):
        if super().exec():
            if self.project_name.text(): self.data['EditorSettings']['name'] = self.project_name.text()
            if self.project_description.text(): self.data['EditorSettings']['description'] = self.project_description.text()
            if self.project_version.text(): self.data['EditorSettings']['version'] = self.project_version.text()
            if self.icon_button.path(): self.data['EditorSettings']['icon'] = self.icon_button.path()

            with open(f'{self.path}/ProjectSettings/ProjectSettings.pylite-asset', 'w', encoding = 'utf-8') as infile:
                yaml.dump(self.data, infile, default_flow_style = False)
            self.refresh_projects.emit()
        return None
#----------------------------------------------------------------------
