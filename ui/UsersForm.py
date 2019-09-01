from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, qApp, QVBoxLayout, QTableWidget, QFormLayout, \
    QLineEdit, QCalendarWidget, QHBoxLayout, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, \
    QTableWidgetItem, QAbstractItemView, QMessageBox

from core.engine import GLog
from entities import Users


class UsersForm(QMainWindow):
    def __init__(self):
        GLog.debug("ui.UsersForm.__init__")
        super().__init__()
        uic.loadUi('ui/usersForm.ui', self)
        self.actionExit.triggered.connect(qApp.quit)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 350)

    def init_data(self):
        for num, user in enumerate(Users.list()):
            self.tableExpenses.insertRow(num)
            self.tableExpenses.setItem(num, 0, QTableWidgetItem(str(user.ID)))
            self.tableExpenses.setItem(num, 1, QTableWidgetItem(user.name))
            self.tableExpenses.setItem(num, 2, QTableWidgetItem(user.login))
            self.tableExpenses.setItem(num, 3, QTableWidgetItem('Да' if user.admin else 'Нет'))
