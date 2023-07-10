#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from data.lib.qtUtils import QDragListItem, QNamedLineEdit
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

        self._remove_button = QPushButton(None)
        self._remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._remove_button.setIcon(QIcon(self.remove_icon))
        self.grid_layout.addWidget(self._remove_button, 0, 1)
        self.grid_layout.setAlignment(self._remove_button, Qt.AlignmentFlag.AlignRight)
        self._remove_button.clicked.connect(self.deleteLater)
        self._remove_button.setFixedWidth(int(self._remove_button.sizeHint().height() * 1.5))

    @property
    def keyword(self) -> str:
        return self._keyword_lineedit.text()
#----------------------------------------------------------------------
