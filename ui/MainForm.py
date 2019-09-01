from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, qApp, QVBoxLayout, QTableWidget, QFormLayout, \
    QLineEdit, QCalendarWidget, QHBoxLayout, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, \
    QTableWidgetItem, QAbstractItemView, QMessageBox

from core.engine import GLog
import state


class MainForm(QMainWindow):
    def __init__(self):
        GLog.debug("ui.MainForm.__init__")
        super().__init__()
        uic.loadUi('ui/MainForm.ui', self)
        self.actionExit.triggered.connect(qApp.quit)

    def recalc_elements_availability(self):
        cur_user = state.State[state.STATE_KEY_USER]
        GLog.debug("ui.MainForm.recalc_elements_availability: %s", cur_user.admin)
        self.menuAdmin.setEnabled(cur_user.admin)
        self.actionAdminUsers.setEnabled(cur_user.admin)
