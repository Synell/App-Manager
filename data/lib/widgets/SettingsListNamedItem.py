#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal

from data.lib.qtUtils import QDragListItem, QNamedLineEdit, QNamedComboBox
#----------------------------------------------------------------------

    # Class
class SettingsListNamedItem(QDragListItem):
    remove_icon = None

    def __init__(self, lang: dict, key: str, keyword: str):
        super().__init__(None)

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')

        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(50)

        self._keyword_lineedit = QNamedLineEdit(None, 'null', lang['QNamedLineEdit'][key])
        self._keyword_lineedit.setText(keyword)
        self.grid_layout.addWidget(self._keyword_lineedit, 0, 0)

        self.remove_button = QPushButton(None)
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.setIcon(QIcon(self.remove_icon))
        self.grid_layout.addWidget(self.remove_button, 0, 3)
        self.grid_layout.setAlignment(self.remove_button, Qt.AlignmentFlag.AlignRight)
        self.remove_button.clicked.connect(self.deleteLater)
        self.remove_button.setFixedWidth(int(self.remove_button.sizeHint().height() * 1.5))

    @property
    def keyword(self) -> str:
        return self._keyword_lineedit.text()
#----------------------------------------------------------------------
