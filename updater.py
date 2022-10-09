#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from sys import exit
from math import *
import os, json, base64, math
from data.lib.qtUtils import *
from data.lib.widgets import SaveData
from data.lib.widgets.updater import *
from data.lib.widgets.updater import data as updater_data
#----------------------------------------------------------------------

    # Class
class QUpdater(QBaseApplication):
    BUILD = '07e6d408'
    VERSION = 'Experimental'

    COLOR_LINK = QUtilsColor()

    UPDATE_LINK = ''

    def __init__(self):
        super().__init__()

        self.save_data = SaveData(save_path = os.path.abspath('./data/save.dat').replace('\\', '/'))

        self.save_data.setStyleSheet(self)
        self.window.setProperty('color', 'cyan')

        self.setWindowIcon(QIcon('./data/icons/AppManager.svg'))

        self.window.setFixedSize(int(self.primaryScreen().size().width() * (7 / 30)), int(self.primaryScreen().size().height() * (16 / 27)))

        self.create_widgets()
        self.load_colors()
        self.update_title()

        self.run()



    def update_title(self):
        self.window.setWindowTitle(self.save_data.language_data['QUpdater']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD}')

    def load_color(self, data: str, element: str, var: str):
        def find(keyword: str = ''):
            keyword += '{'

            start = data.find(keyword)
            if start == -1: return ''

            end = data[start:].find('}')
            if end == -1: return ''
            return data[start + len(keyword) : start + end]


        def get_variable(qss: str = '', var_name: str = ''):
            var_name += ':'

            start = qss.find(f'{var_name}')
            if start == -1: return ''

            end = qss[start:].find(';')
            if end == -1: return ''

            if qss[start - 1] == '-': return get_variable(qss[start + end + 1 :], var_name)

            return qss[start + len(var_name) : start + end]

        return get_variable(find(element), var)

    def load_colors(self):
        data = (
            self.save_data.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Local) + '\n' +
            self.save_data.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Global)
        ).replace(' ', '').replace('\t', '').replace('\n', '')

        linkColor = self.load_color(data, f'QLabel[color=\'{self.window.property("color")}\']::link', 'color')

        if linkColor:
            self.COLOR_LINK = QUtilsColor(linkColor)
            SaveData.COLOR_LINK = self.COLOR_LINK

        QNamedLineEdit.normal_color = self.load_color(data, 'QWidget[QNamedLineEdit=true]QLabel', 'color')
        QNamedLineEdit.hover_color = self.load_color(data, 'QWidget[QNamedLineEdit=true]QLabel[hover=true]', 'color')
        QNamedLineEdit.focus_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QNamedLineEdit=true][color=\'main\']QLabel[focus=true]', 'color')

        QNamedTextEdit.normal_color = self.load_color(data, 'QWidget[QNamedTextEdit=true]QLabel', 'color')
        QNamedTextEdit.hover_color = self.load_color(data, 'QWidget[QNamedTextEdit=true]QLabel[hover=true]', 'color')
        QNamedTextEdit.focus_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QNamedTextEdit=true][color=\'main\']QLabel[focus=true]', 'color')

        QNamedComboBox.normal_color = self.load_color(data, 'QWidget[QNamedComboBox=true]QLabel', 'color')
        QNamedComboBox.hover_color = self.load_color(data, 'QWidget[QNamedComboBox=true]QLabel[hover=true]', 'color')
        QNamedComboBox.focus_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QNamedComboBox=true][color=\'main\']QLabel[focus=true]', 'color')

        QNamedSpinBox.normal_color = self.load_color(data, 'QWidget[QNamedSpinBox=true]QLabel', 'color')
        QNamedSpinBox.hover_color = self.load_color(data, 'QWidget[QNamedSpinBox=true]QLabel[hover=true]', 'color')
        QNamedSpinBox.focus_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QNamedSpinBox=true][color=\'main\']QLabel[focus=true]', 'color')

        QNamedDoubleSpinBox.normal_color = self.load_color(data, 'QWidget[QNamedDoubleSpinBox=true]QLabel', 'color')
        QNamedDoubleSpinBox.hover_color = self.load_color(data, 'QWidget[QNamedDoubleSpinBox=true]QLabel[hover=true]', 'color')
        QNamedDoubleSpinBox.focus_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QNamedDoubleSpinBox=true][color=\'main\']QLabel[focus=true]', 'color')

        QFileButton.normal_color = self.load_color(data, 'QWidget[QFileButton=true]QLabel', 'color')
        QFileButton.hover_color = self.load_color(data, 'QWidget[QFileButton=true]QLabel[hover=true]', 'color')

        QToggleButton.normal_color = self.load_color(data, f'QWidget[QToggleButton=true]QCheckBox', 'color')
        QToggleButton.normal_color_handle = self.load_color(data, f'QWidget[QToggleButton=true]QCheckBox::handle', 'color')
        QToggleButton.checked_color = self.load_color(data, f'QWidget[color=\'{self.window.property("color")}\']QWidget[QToggleButton=true]QCheckBox:checked', 'color')
        QToggleButton.checked_color_handle = self.load_color(data, f'QWidget[QToggleButton=true]QCheckBox:checked::handle', 'color')

    def settings_menu(self):
        self.save_data.settings_menu(self)
        self.load_colors()



    def not_implemented(self, text = ''):
        if text:
            w = QDropDownWidget(text = lang['details'], widget = QLabel(text))
        else: w = None

        lang = self.save_data.language_data['QMessageBox']['critical']['notImplemented']

        QMessageBoxWithWidget(
            app = self,
            title = lang['title'],
            text = lang['text'],
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def create_widgets(self):
        self.root = QGridWidget()
        self.root.grid_layout.setSpacing(0)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.window.setCentralWidget(self.root)


        top_frame = QGridFrame()
        top_frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(top_frame, 0, 0)
        top_frame.grid_layout.setSpacing(5)
        top_frame.grid_layout.setContentsMargins(15, 10, 15, 10)

        self.progress_percent = QLabel('Installing... (40%)')
        self.progress_percent.setProperty('h', 2)
        top_frame.grid_layout.addWidget(self.progress_percent, 0, 0)

        self.progress_eta = QLabel('Calculating remaining time...')
        self.progress_eta.setProperty('subtitle', True)
        self.progress_eta.setProperty('bold', True)
        top_frame.grid_layout.addWidget(self.progress_eta, 1, 0)


        self.progress = QProgressBar()
        self.progress.setProperty('color', 'main')
        self.progress.setProperty('small', True)
        self.progress.setProperty('light', True)
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        self.progress.setValue(40)
        self.root.grid_layout.addWidget(self.progress, 1, 0)


        ratio = 1192 / self.window.width() # 1192x674
        self.screenshots = QSlidingStackedWidget()
        self.screenshots.set_speed(650)
        self.screenshots.set_animation(QEasingCurve.Type.OutCubic)
        self.screenshots.set_has_opacity_effect(False)
        self.screenshots.setFixedHeight(math.ceil(674 / ratio))
        self.screenshots.layout().setContentsMargins(0, 0, 0, 0)
        self.screenshots.layout().setSpacing(0)
        self.root.grid_layout.addWidget(self.screenshots, 2, 0)

        for image in updater_data.images:
            self.screenshots.addWidget(QIconWidget(None, base64.b64decode(image), QSize(self.window.width() + 1, math.ceil(674 / ratio)), False))

        bottom_frame = QGridFrame()
        bottom_frame.setFixedHeight(int(self.window.height() / 2.125))
        bottom_frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(bottom_frame, 3, 0)
        bottom_frame.grid_layout.setSpacing(5)
        bottom_frame.grid_layout.setContentsMargins(10, 10, 10, 10)

    def run(self):
        self.slide_worker = SlideWorker(self.screenshots)
        self.slide_worker.signals.slide_changed.connect(self.screenshots.slide_loop_next)
        self.slide_worker.start()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    app = QUpdater()
    app.window.showNormal()
    exit(app.exec())
#----------------------------------------------------------------------
