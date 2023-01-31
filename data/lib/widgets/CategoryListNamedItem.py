#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal

from data.lib.qtUtils import QDragListItem, QNamedLineEdit, QNamedComboBox, QGridWidget
from .Category import Category
#----------------------------------------------------------------------

    # Class
class CategoryListNamedItem(QDragListItem):
    remove_icon = None

    def __init__(self, lang: dict, key: str, category: Category):
        super().__init__(None)

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')

        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(50)

        self._keyword_lineedit = QNamedLineEdit(None, 'null', lang['QNamedLineEdit'][key])
        self._keyword_lineedit.setText(category.keyword)
        self.grid_layout.addWidget(self._keyword_lineedit, 0, 0)

        self._icon = category.icon

        widget = QGridWidget(None)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(16)
        self.grid_layout.addWidget(widget, 0, 1, Qt.AlignmentFlag.AlignRight)

        self._icon_button = QPushButton(None)
        self._icon_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_button.setIcon(QIcon(category.icon))
        widget.grid_layout.addWidget(self._icon_button, 0, 0)
        self._icon_button.clicked.connect(self.icon_button_clicked)
        self._icon_button.setFixedWidth(int(self._icon_button.sizeHint().height() * 1.5))

        self._remove_button = QPushButton(None)
        self._remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._remove_button.setIcon(QIcon(self.remove_icon))
        widget.grid_layout.addWidget(self._remove_button, 0, 1)
        self._remove_button.clicked.connect(self.deleteLater)
        self._remove_button.setFixedWidth(int(self._remove_button.sizeHint().height() * 1.5))

        widget.grid_layout.setColumnStretch(2, 1)

    @property
    def keyword(self) -> str:
        return self._keyword_lineedit.text()

    @property
    def icon(self) -> str:
        return self._icon

    def icon_button_clicked(self):
        print('icon_button_clicked')
#----------------------------------------------------------------------
