#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal
from data.lib.qtUtils import QGridWidget, QGridFrame, QScrollableGridWidget
import yaml
#----------------------------------------------------------------------

    # Class
class ChangeAppDialog(QDialog):
    install_app_icon = None
    install_menu_called = pyqtSignal()
    app_changed = pyqtSignal()

    def __init__(self, parent = None, project_path: str = '', apps = [], lang: dict = {}):
        super().__init__(parent)

        self.lang = lang
        self.project_path = project_path

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

        with open(f'{project_path}/ProjectSettings/ProjectSettings.pylite-asset', 'r', encoding = 'utf-8') as infile:
            data = yaml.load(infile, Loader = yaml.FullLoader)
            self.name = data['appSettings']['name']
            self.app_path = data['appSettings']['appPath']

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle(self.lang['title'])

        self.root = QGridFrame()
        self.root.grid_layout.setSpacing(0)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.root.setProperty('border-top', True)
        self.root.setProperty('border-bottom', True)
        self.root.setProperty('border-left', True)
        self.root.setProperty('border-right', True)


        self.root.top = QGridFrame()
        self.root.top.grid_layout.setSpacing(0)
        self.root.top.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.root.grid_layout.addWidget(self.root.top, 0, 0)
        self.root.grid_layout.setAlignment(self.root.top, Qt.AlignmentFlag.AlignTop)
        self.root.top.grid_layout.setRowStretch(2, 1)


        self.root.top.title = QGridFrame()
        self.root.top.title.grid_layout.setSpacing(0)
        self.root.top.title.grid_layout.setContentsMargins(16, 16, 16, 16)

        self.root.top.title.label = QLabel(self.lang['QLabel']['selectappAndPlatform'])
        self.root.top.title.label.setProperty('brighttitle', True)
        self.root.top.title.grid_layout.addWidget(self.root.top.title.label, 0, 0)

        self.root.top.title.grid_layout.setAlignment(self.root.top.title.label, Qt.AlignmentFlag.AlignLeft)
        self.root.top.grid_layout.addWidget(self.root.top.title, 0, 0)
        self.root.top.grid_layout.setAlignment(self.root.top.title, Qt.AlignmentFlag.AlignTop)


        self.root.top.info = QGridFrame()
        self.root.top.info.grid_layout.setSpacing(0)
        self.root.top.info.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.root.top.info.setProperty('border-top', True)

        self.root.top.info.label = self.generate_text()
        self.root.top.info.grid_layout.addWidget(self.root.top.info.label, 0, 0)
        self.root.top.info.grid_layout.setAlignment(self.root.top.info.label, Qt.AlignmentFlag.AlignLeft)

        self.root.top.grid_layout.addWidget(self.root.top.info, 1, 0)
        self.root.top.grid_layout.setAlignment(self.root.top.info, Qt.AlignmentFlag.AlignTop)


        self.root.install_list = QScrollableGridWidget()
        self.root.install_list.scroll_layout.setSpacing(16)
        self.root.install_list.scroll_layout.setContentsMargins(16, 16, 16, 16)
        self.root.install_list.setProperty('border-top', True)
        self.root.grid_layout.addWidget(self.root.install_list, 1, 0)
        self.root.grid_layout.setRowStretch(1, 2)

        sendParam = lambda p: lambda: self.select_app(p)
        for index, app in enumerate(apps):
            button = QRadioButton(app.split('/')[-1])
            button.clicked.connect(sendParam(app))
            if len(app) != 1:
                button.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                button.setDisabled(True)
            if app == self.app_path: button.setChecked(True)
            self.root.install_list.scroll_layout.addWidget(button, index, 0)
            self.root.install_list.scroll_layout.setAlignment(button, Qt.AlignmentFlag.AlignTop)

        self.root.install_list.scroll_layout.setRowStretch(len(apps), 1)


        self.root.bottom = QGridFrame()
        self.root.bottom.grid_layout.setSpacing(16)
        self.root.bottom.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.root.bottom.setProperty('border-top', True)

        self.root.bottom.install_app = QPushButton(self.lang['QPushButton']['installappVersion'])
        self.root.bottom.install_app.setIcon(self.install_app_icon)
        self.root.bottom.install_app.setCursor(Qt.CursorShape.PointingHandCursor)
        self.root.bottom.install_app.setProperty('readmore', True)
        self.root.bottom.install_app.clicked.connect(self.goto_install_menu)
        self.root.bottom.grid_layout.addWidget(self.root.bottom.install_app, 0, 0)
        self.root.bottom.grid_layout.setAlignment(self.root.bottom.install_app, Qt.AlignmentFlag.AlignLeft)

        self.root.bottom.right = QGridWidget()
        self.root.bottom.right.grid_layout.setSpacing(16)
        self.root.bottom.right.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.root.bottom.grid_layout.addWidget(self.root.bottom.right, 0, 1)
        self.root.bottom.grid_layout.setAlignment(self.root.bottom.right, Qt.AlignmentFlag.AlignRight)

        self.root.bottom.right.cancel = QPushButton(self.lang['QPushButton']['cancel'])
        self.root.bottom.right.cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.root.bottom.right.cancel.setProperty('color', 'white')
        self.root.bottom.right.cancel.setProperty('transparent', True)
        self.root.bottom.right.cancel.clicked.connect(self.reject)
        self.root.bottom.right.grid_layout.addWidget(self.root.bottom.right.cancel, 0, 0)

        self.root.bottom.right.open_with = QPushButton(self.lang['QPushButton']['openWith'].replace('%s', self.app_path.split('/')[-1]))
        if apps: self.root.bottom.right.open_with.setCursor(Qt.CursorShape.PointingHandCursor)
        else: self.root.bottom.right.open_with.setDisabled(True)
        self.root.bottom.right.open_with.setProperty('color', 'main')
        self.root.bottom.right.open_with.clicked.connect(self.accept)
        self.root.bottom.right.grid_layout.addWidget(self.root.bottom.right.open_with, 0, 1)

        self.root.grid_layout.addWidget(self.root.bottom, 3, 0)
        self.root.grid_layout.setAlignment(self.root.bottom, Qt.AlignmentFlag.AlignBottom)


        self.layout.addWidget(self.root, 0, 0)
        self.setLayout(self.layout)
        self.select_app(self.app_path)

    def generate_text(self):
        widget = QGridWidget()
        widget.grid_layout.setSpacing(4)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(self.name if len(self.name) < 64 else self.name[:64] + '...')
        label.setProperty('brighttitle', True)
        label.setFixedSize(label.sizeHint())
        widget.grid_layout.addWidget(label, 0, 1)

        if self.app_path:
            label = QLabel(self.app_path.split('/')[-1])
            label.setProperty('smallbrightnormal', True)
            label.setFixedSize(label.sizeHint())
            widget.grid_layout.addWidget(label, 1, 1)
            widget.grid_layout.setRowStretch(2, 1)

        return widget

    def select_app(self, path: str = ''):
        self.new_app_path = path
        self.root.bottom.right.open_with.setText(self.lang['QPushButton']['openWith'].replace('%s', self.new_app_path.split('/')[-1]))

    def goto_install_menu(self):
        self.reject()
        self.install_menu_called.emit()

    def exec(self):
        if super().exec():
            with open(f'{self.project_path}/ProjectSettings/ProjectSettings.pylite-asset', 'r', encoding = 'utf-8') as infile:
                data = yaml.load(infile, Loader = yaml.FullLoader)
                data['appSettings']['appPath'] = self.new_app_path
                with open(f'{self.project_path}/ProjectSettings/ProjectSettings.pylite-asset', 'w', encoding = 'utf-8') as outfile:
                    yaml.dump(data, outfile, default_flow_style = False, allow_unicode = True)
            self.accept()
            self.app_changed.emit()
#----------------------------------------------------------------------
