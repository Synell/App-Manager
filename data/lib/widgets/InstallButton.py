#----------------------------------------------------------------------

    # Libraries
from collections import namedtuple
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, Signal, QSize
from .PlatformType import PlatformType

from data.lib.qtUtils import QGridWidget, QGridFrame, QIconWidget
#----------------------------------------------------------------------

    # Class
class InstallButton(QGridFrame):
    lang = {}
    download_data = namedtuple('download_data', ['name', 'tag_name', 'files_data', 'prerelease', 'created_at', 'token'])
    file_data = namedtuple('file_data', ['link', 'compressed'])
    platform = PlatformType.Windows
    token: str = None

    download = Signal(download_data)

    def __init__(self, data: dict = {}, button_text: str = 'Install', name: str = '', tag_name: str = '', icon: str = None, disabled: bool = False) -> None:
        super().__init__()

        self.data = data
        self.name = name
        self.tag_name = tag_name

        self.setFixedHeight(60)
        self.setProperty('side', 'all')

        widget = self.widget_couple(icon, self.generate_text(f'{name} ({tag_name})'))
        self.grid_layout.addWidget(widget, 0, 0)
        self.grid_layout.setAlignment(widget, Qt.AlignmentFlag.AlignLeft)

        self.push_button = QPushButton(button_text)
        self.push_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.push_button.setDisabled(disabled)
        # if disabled: self.setCursor(Qt.CursorShape.ForbiddenCursor)
        self.push_button.setProperty('color', 'main')
        self.push_button.clicked.connect(self.install_click)
        self.grid_layout.addWidget(self.push_button, 0, 1)
        self.grid_layout.setAlignment(self.push_button, Qt.AlignmentFlag.AlignRight)
        self.set_disabled(disabled)

    def generate_text(self, title) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(4)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setProperty('brighttitle', True)
        label.setFixedSize(label.sizeHint())
        widget.grid_layout.addWidget(label, 0, 1)

        label = QLabel(f'by {self.data["author"]["login"]}')
        label.setProperty('smallbrightnormal', True)
        label.setFixedSize(label.sizeHint())
        widget.grid_layout.addWidget(label, 1, 1)
        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def widget_couple(self, icon: str = None, text_widget: QGridWidget = None) -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        iw = QIconWidget(None, icon, QSize(40, 40))

        widget.grid_layout.addWidget(iw, 0, 0)
        widget.grid_layout.addWidget(text_widget, 0, 1)

        widget.grid_layout.setColumnStretch(2, 1)

        return widget


    @staticmethod
    def get_release(data: dict, token: str = None) -> download_data | None:
        def is_compressed_content_type(s: str) -> bool:
            types = []
            match InstallButton.platform:
                case PlatformType.Windows:
                    types = [
                        'application/x-zip-compressed', # .zip
                        'application/zip' # .zip
                        #'application/octet-stream' # .7z
                    ]
                case PlatformType.Linux:
                    types = [
                        'application/x-gzip', # .tar.gz
                        'application/gzip' # .tar.gz
                    ]
                case PlatformType.MacOS:
                    types = [
                        'application/x-gzip', # .tar.gz
                        'application/gzip' # .tar.gz
                        #'application/octet-stream' # .7z
                    ]

            for i in types:
                if i == s: return True
            return False
        
        def is_binary_content_type(s: str) -> bool:
            return s in ['binary/octet-stream', 'application/octet-stream']
        
        def is_portable(s: str) -> bool:
            return 'portable' in s.lower()

        def better_file(files: list[InstallButton.file_data]) -> list[InstallButton.file_data]:
            def get_platform_file(lst: list[InstallButton.file_data]) -> InstallButton.file_data | None:
                for i in InstallButton.platform.value:
                    for j in lst:
                        if i.lower() in j.link.lower(): return lst[lst.index(j)]

                return None

            f = [i for i in files if is_portable(i.link)] # Portable version

            result = get_platform_file(f)
            if result: return [result]

            f = [i for i in files if not is_portable(i.link)] # Normal version

            result = get_platform_file(f)
            if result: return [result]

            print('Unable to find a suitable file')
            return files


        files = [
            InstallButton.file_data(
                asset['browser_download_url'],
                is_compressed_content_type(asset['content_type'])
            )
            for asset in data['assets']
                if is_binary_content_type(asset['content_type']) or
                    is_compressed_content_type(asset['content_type'])
        ]

        if files:
            return InstallButton.download_data(
                data['name'],
                data['tag_name'],
                better_file(files),
                data['prerelease'], data['created_at'],
                token
            )


    def install_click(self) -> None:
        rel = InstallButton.get_release(self.data, self.token)

        if rel:
            self.push_button.setDisabled(True)
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.download.emit(rel)
        else: print('Unable to download')

    def set_disabled(self, b: bool) -> None:
        self.push_button.setDisabled(b)
        if b:
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.push_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.push_button.setCursor(Qt.CursorShape.PointingHandCursor)
#----------------------------------------------------------------------
