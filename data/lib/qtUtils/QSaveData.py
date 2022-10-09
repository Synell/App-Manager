#----------------------------------------------------------------------

    # Libraries
from typing import Callable
from PyQt6.QtGui import QIcon
import json, os
from enum import Enum

from .QMessageBoxWithWidget import QMessageBoxWithWidget
from .QBaseApplication import QBaseApplication
from .QSettingsDialog import QSettingsDialog
#----------------------------------------------------------------------

    # Class
class QSaveData:
    color = 'blue'

    class StyleSheetMode(Enum):
        All = 'all'
        Global = 'global'
        Local = 'local'

    class IconMode(Enum):
        Global = 'global'
        Local = 'local'

    def __init__(self, save_path = './data/save.dat', lang_folder = './data/lang/', themes_folder = './data/themes/', default_language = 'english', default_theme = 'neutron', default_theme_variant = 'dark') -> None:
        self.language = default_language
        self.theme = default_theme
        self.theme_variant = default_theme_variant
        self.path = save_path
        self.lang_folder = lang_folder
        self.themes_folder = themes_folder

        self.load()

    def save(self) -> None:
        extra_data = self.save_extra_data()
        with open(self.path, 'w', encoding = 'utf-8') as outfile:
            json.dump(obj = {'language': self.language, 'theme': self.theme, 'themeVariant': self.theme_variant} | extra_data, fp = outfile, ensure_ascii = False)

    def save_extra_data(self) -> dict: return {}

    def load(self) -> None:
        if not os.path.exists(self.path): self.save()
        with open(self.path, 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)
        self.language = data['language']
        self.theme = data['theme']
        self.theme_variant = data['themeVariant']
        self.load_language_data()
        self.load_theme_data()
        self.load_extra_data(data)

    def load_language_data(self) -> None:
        with open(f'{self.lang_folder}{self.language}.json', 'r', encoding = 'utf-8') as infile:
            self.language_data = json.load(infile)['data']

    def load_theme_data(self) -> None:
        self.theme_data = ''
        with open(f'{self.themes_folder}/{self.theme}.json', 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)['qss']
            path = data[self.theme_variant]['location']

        with open(f'data/lib/qtUtils/themes/{self.theme}/{self.theme_variant}/{path}/main.json', 'r', encoding = 'utf-8') as infile:
            files = json.load(infile)['files']

        for file in files:
            with open(f'data/lib/qtUtils/themes/{self.theme}/{self.theme_variant}/{path}/{file}.qss', 'r', encoding = 'utf-8') as infile:
                self.theme_data += infile.read()

        self.theme_data = self.theme_data.replace('{path}', f'data/lib/qtUtils/themes/{self.theme}/{self.theme_variant}/{path}/icons/'.replace('//', '/'))

    def load_extra_data(self, extra_data: dict = {}) -> None: pass

    def setStyleSheet(self, app: QBaseApplication = None) -> None:
        if not app: return
        app.setStyleSheet(self.getStyleSheet(app, QSaveData.StyleSheetMode.All))

    def getStyleSheet(self, app: QBaseApplication = None, mode: StyleSheetMode = StyleSheetMode.All) -> str:
        if not app: return ''

        match mode:
            case QSaveData.StyleSheetMode.All:
                return self.getStyleSheet(app, QSaveData.StyleSheetMode.Global) + self.getStyleSheet(app, QSaveData.StyleSheetMode.Local)
            case QSaveData.StyleSheetMode.Global:
                return self.theme_data
            case QSaveData.StyleSheetMode.Local:
                with open(f'{self.themes_folder}/{self.theme}.json', 'r', encoding = 'utf-8') as infile:
                    data = json.load(infile)['qss']
                    path = data[self.theme_variant]['location']

                with open(f'{self.themes_folder}/{self.theme}/{self.theme_variant}/{path}/main.json', 'r', encoding = 'utf-8') as infile:
                    files = json.load(infile)['files']

                theme_data = ''

                for file in files:
                    with open(f'{self.themes_folder}/{self.theme}/{self.theme_variant}/{path}/{file}.qss', 'r', encoding = 'utf-8') as infile:
                        theme_data += infile.read()

                return theme_data.replace('{path}', f'{self.themes_folder}/{self.theme}/{self.theme_variant}/icons/'.replace('//', '/'))
        return ''

    def getIconsDir(self) -> str:
        return f'{self.themes_folder}/{self.theme}/{self.theme_variant}/icons/'

    def getIcon(self, path, asQIcon = True, mode: IconMode = IconMode.Local) -> QIcon|str:
        if mode == QSaveData.IconMode.Local:
            if asQIcon: return QIcon(f'{self.themes_folder}/{self.theme}/{self.theme_variant}/icons/{path}')
            return f'{self.themes_folder}/{self.theme}/{self.theme_variant}/icons/{path}'
        elif mode == QSaveData.IconMode.Global:
            if asQIcon: return QIcon(f'./data/lib/qtUtils/themes/{self.theme}/{self.theme_variant}/icons/{path}')
            return f'./data/lib/qtUtils/themes/{self.theme}/{self.theme_variant}/icons/{path}'

    def settings_menu(self, app: QBaseApplication = None) -> list:
        dat = self.settings_menu_extra()
        response = QSettingsDialog(
            parent = app.window,
            settings_data = self.language_data['QSettingsDialog'],
            lang_folder = self.lang_folder,
            themes_folder = self.themes_folder,
            current_lang = self.language,
            current_theme = self.theme,
            current_theme_variant = self.theme_variant,
            extra_tabs = dat[0],
            get_function = dat[1]
        ).exec()
        if response != None:
            self.language = response[0]
            self.theme = response[1]
            self.theme_variant = response[2]

            self.save()
            self.load()
            self.setStyleSheet(app)
            QMessageBoxWithWidget(app,
                self.language_data['QMessageBox']['information']['settingsReload']['title'],
                self.language_data['QMessageBox']['information']['settingsReload']['text'],
                None,
                QMessageBoxWithWidget.Icon.Information,
                None
            ).exec()

    def settings_menu_extra(self) -> tuple[dict, Callable|None]:
        return {}, None
#----------------------------------------------------------------------
