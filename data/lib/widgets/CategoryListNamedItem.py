#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from data.lib.QtUtils import QDragListItem, QNamedLineEdit, QGridWidget
from .Category import Category
from .dialog import EditCategoryIconDialog
#----------------------------------------------------------------------

    # Class
class CategoryListNamedItem(QDragListItem):
    remove_icon = None

    def __init__(self, lang: dict, key: str, category: Category):
        super().__init__(None)

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')

        self.lang = lang

        self.layout_.setContentsMargins(10, 10, 10, 10)
        self.layout_.setSpacing(32)

        self._keyword_lineedit = QNamedLineEdit(None, 'null', lang['QNamedLineEdit'][key])
        self._keyword_lineedit.setText(category.keyword)
        self.layout_.addWidget(self._keyword_lineedit, 0, 0)

        self._icon = category.icon

        widget = QGridWidget(None)
        widget.layout_.setContentsMargins(0, 0, 0, 0)
        widget.layout_.setSpacing(8)
        self.layout_.addWidget(widget, 0, 1, Qt.AlignmentFlag.AlignRight)

        self._icon_button = QPushButton(None)
        self._icon_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_button.setIcon(QIcon(category.icon))
        widget.layout_.addWidget(self._icon_button, 0, 0)
        self._icon_button.clicked.connect(self.icon_button_clicked)
        self._icon_button.setFixedWidth(int(self._icon_button.sizeHint().height() * 1.5))

        self._remove_button = QPushButton(None)
        self._remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._remove_button.setIcon(QIcon(self.remove_icon))
        widget.layout_.addWidget(self._remove_button, 0, 1)
        self._remove_button.clicked.connect(self.deleteLater)
        self._remove_button.setFixedWidth(int(self._remove_button.sizeHint().height() * 1.5))

        widget.layout_.setColumnStretch(2, 1)

    @property
    def keyword(self) -> str:
        return self._keyword_lineedit.text()

    @property
    def icon(self) -> str:
        return self._icon

    def icon_button_clicked(self):
        icon = EditCategoryIconDialog(self.window(), self.lang['EditCategoryIconDialog'], self._icon).exec()
        if icon:
            self._icon = icon
            self._icon_button.setIcon(QIcon(self._icon))
#----------------------------------------------------------------------
