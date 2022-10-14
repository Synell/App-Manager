#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from sys import exit
from math import *
import os, json, base64, math, sys
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

    def load_colors(self):
        qss = QssParser(
            self.save_data.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Local) + '\n' +
            self.save_data.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Global)
        )

        self.COLOR_LINK = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QLabel', attributes = {'color': self.window.property('color')}, items = ['link'])
            )['color']
        )
        SaveData.COLOR_LINK = self.COLOR_LINK

        QNamedLineEdit.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedLineEdit.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedLineEdit.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedTextEdit.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedTextEdit.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedTextEdit.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedComboBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedComboBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedComboBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedSpinBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedSpinBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedSpinBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedDoubleSpinBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedDoubleSpinBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedDoubleSpinBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QFileButton.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QFileButton': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QFileButton.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QFileButton': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']

        QToggleButton.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox')
        )['color']
        QToggleButton.normal_color_handle = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', items = ['handle'])
        )['color']
        QToggleButton.checked_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'])
        )['color']
        QToggleButton.checked_color_handle = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'], items = ['handle'])
        )['color']

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
        self.root.grid_layout.setAlignment(top_frame, Qt.AlignmentFlag.AlignTop)
        top_frame.grid_layout.setSpacing(5)
        top_frame.grid_layout.setContentsMargins(15, 10, 15, 10)

        self.progress_percent = QLabel(self.save_data.language_data['QUpdater']['QLabel']['downloading'].replace('%s', self.save_data.language_data['QUpdater']['QLabel']['waiting']))
        self.progress_percent.setProperty('h', 2)
        top_frame.grid_layout.addWidget(self.progress_percent, 0, 0)

        self.progress_eta = QLabel(self.save_data.language_data['QUpdater']['QLabel']['calculatingRemainingTime'])
        self.progress_eta.setProperty('subtitle', True)
        self.progress_eta.setProperty('bold', True)
        top_frame.grid_layout.addWidget(self.progress_eta, 1, 0)


        self.progress = QProgressBar()
        self.progress.setProperty('color', 'main')
        self.progress.setProperty('small', True)
        self.progress.setProperty('light', True)
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        self.progress.setValue(0)
        self.root.grid_layout.addWidget(self.progress, 1, 0)
        self.root.grid_layout.setAlignment(self.progress, Qt.AlignmentFlag.AlignTop)


        ratio = 1192 / self.window.width() # 1192x674
        self.screenshots = QSlidingStackedWidget()
        self.screenshots.set_speed(650)
        self.screenshots.set_animation(QEasingCurve.Type.OutCubic)
        self.screenshots.set_has_opacity_effect(False)
        self.screenshots.setFixedHeight(math.ceil(674 / ratio))
        self.screenshots.layout().setContentsMargins(0, 0, 0, 0)
        self.screenshots.layout().setSpacing(0)
        self.root.grid_layout.addWidget(self.screenshots, 2, 0)
        self.root.grid_layout.setAlignment(self.screenshots, Qt.AlignmentFlag.AlignTop)

        for image in updater_data.images:
            self.screenshots.addWidget(QIconWidget(None, base64.b64decode(image), QSize(self.window.width() + 1, math.ceil(674 / ratio)), False))

        bottom_frame = QGridFrame()
        bottom_frame.setFixedHeight(int(self.window.height() / 2.125))
        # bottom_frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(bottom_frame, 3, 0)
        bottom_frame.grid_layout.setSpacing(5)
        bottom_frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        bottom_frame.top = QGridFrame()
        bottom_frame.top.grid_layout.setSpacing(0)
        bottom_frame.top.grid_layout.setContentsMargins(10, 10, 10, 10)
        bottom_frame.grid_layout.addWidget(bottom_frame.top, 0, 0)


        bottom_frame.bottom = QGridFrame()
        bottom_frame.bottom.grid_layout.setSpacing(5)
        bottom_frame.bottom.grid_layout.setContentsMargins(10, 10, 10, 10)
        bottom_frame.bottom.setProperty('border-top', True)
        bottom_frame.grid_layout.addWidget(bottom_frame.bottom, 0, 0)
        bottom_frame.grid_layout.setAlignment(bottom_frame.bottom, Qt.AlignmentFlag.AlignBottom)

        # right_buttons = QGridFrame()
        # right_buttons.grid_layout.setSpacing(10)
        # right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)
        # bottom_frame.bottom.grid_layout.addWidget(right_buttons, 0, 0)
        # bottom_frame.bottom.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.close_button = QPushButton('Close')
        self.close_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        self.close_button.setDisabled(True)
        self.close_button.setProperty('color', 'white')
        self.close_button.setProperty('transparent', True)
        bottom_frame.bottom.grid_layout.addWidget(self.close_button, 0, 0)
        bottom_frame.bottom.grid_layout.setAlignment(self.close_button, Qt.AlignmentFlag.AlignLeft)

        self.open_button = QPushButton('Open App')
        self.open_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        self.open_button.setDisabled(True)
        self.open_button.setProperty('color', 'main')
        bottom_frame.bottom.grid_layout.addWidget(self.open_button, 0, 1)
        bottom_frame.bottom.grid_layout.setAlignment(self.open_button, Qt.AlignmentFlag.AlignRight)


    def run(self):
        self.slide_worker = SlideWorker()
        self.slide_worker.signals.slide_changed.connect(self.slide)
        self.slide_worker.start()

        self.update_worker = UpdateWorker(self.UPDATE_LINK, self.save_data.token, self.save_data.downloads_folder)
        self.update_worker.signals.download_progress_changed.connect(self.download_progress_changed)
        self.update_worker.signals.download_speed_changed.connect(self.download_speed_changed)
        self.update_worker.signals.download_done.connect(self.download_done)
        self.update_worker.signals.install_progress_changed.connect(self.install_progress_changed)
        self.update_worker.signals.install_speed_changed.connect(self.install_speed_changed)
        self.update_worker.signals.install_done.connect(self.install_done)
        self.update_worker.signals.install_failed.connect(self.install_failed)
        # self.update_worker.start()

    def slide(self):
        self.screenshots.slide_loop_next()

    def download_speed_changed(self, speed: float):
        self.progress_eta.setText(self.save_data.language_data['QUpdater']['QLabel']['bytes'].replace('%s', self.convert(speed)))

    def download_progress_changed(self, progress: float):
        self.progress.setValue(int(progress * 50))
        self.progress_percent.setText(self.save_data.language_data['QUpdater']['QLabel']['downloading'].replace('%s', f'{int(progress * 100)} %'))

    def download_done(self):
        self.progress.setValue(50)
        self.progress_percent.setText(self.save_data.language_data['QUpdater']['QLabel']['downloading'].replace('%s', self.save_data.language_data['QUpdater']['QLabel']['done']))
        self.progress_eta.setText(self.save_data.language_data['QUpdater']['QLabel']['done'])

    def install_speed_changed(self, speed: float):
        self.progress_eta.setText(self.save_data.language_data['QUpdater']['QLabel']['items'].replace('%s', f'{speed}'))

    def install_progress_changed(self, progress: float):
        self.progress.setValue(int(50 + progress * 50))
        self.progress_percent.setText(self.save_data.language_data['QUpdater']['QLabel']['installing'].replace('%s', f'{int(progress * 100)} %'))

    def install_done(self):
        self.progress.setValue(100)
        self.progress_percent.setText(self.save_data.language_data['QUpdater']['QLabel']['done'])
        self.progress_eta.setText('')

        self.close_button.setDisabled(False)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.close_button.clicked.connect(self.close)

        self.open_button.setDisabled(False)
        self.open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.open_button.clicked.connect(self.open_app)

    def install_failed(self, error: str):
        pass # todo

    def convert(self, bytes: float) -> str:
        step_unit = 1024
        units = ['B', 'KB', 'MB', 'GB', 'TB']

        for x in units[:-1]:
            if bytes < step_unit:
                return f'{bytes:.2f} {x}'
            bytes /= step_unit
        return f'{bytes:.2f} {units[-1]}'
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    if len(sys.argv) > 1: QUpdater.UPDATE_LINK = sys.argv[1]
    else: QUpdater.UPDATE_LINK = 'https://github.com/Synell/PERT-Maker/releases/download/07e69431/Windows.PERT_Maker.Rel-07e69431.zip'#exit()

    app = QUpdater()
    app.window.showNormal()
    exit(app.exec())
#----------------------------------------------------------------------
