#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QFrame, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
#----------------------------------------------------------------------
