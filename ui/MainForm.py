from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, qApp, QVBoxLayout, QTableWidget, QFormLayout, \
    QLineEdit, QCalendarWidget, QHBoxLayout, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, \
    QTableWidgetItem, QAbstractItemView, QMessageBox

from core.engine import GLog
from entities import Expenses, Incomes
import state


class MainForm(QMainWindow):
    def __init__(self):
        GLog.debug("ui.MainForm.__init__")
        super().__init__()
        uic.loadUi('ui/mainForm.ui', self)
        self.actionExit.triggered.connect(qApp.quit)

        self.tableIncomes.setColumnWidth(0, 80)
        self.tableIncomes.setColumnWidth(1, 150)
        self.tableIncomes.setColumnWidth(2, 100)
        self.tableIncomes.setColumnWidth(3, 350)

        self.tableExpenses.setColumnWidth(0, 80)
        self.tableExpenses.setColumnWidth(1, 150)
        self.tableExpenses.setColumnWidth(2, 100)
        self.tableExpenses.setColumnWidth(3, 350)

    def recalc_elements_availability(self):
        cur_user = state.State[state.STATE_KEY_USER]
        GLog.debug("ui.MainForm.recalc_elements_availability: %s", cur_user.admin)
        self.menuAdmin.setEnabled(cur_user.admin)
        self.actionAdminUsers.setEnabled(cur_user.admin)

    def init_data(self):
        self.init_expenses()
        self.init_incomes()

    def init_expenses(self):
        for num, expense in enumerate(Expenses.list()):
            self.tableExpenses.insertRow(num)
            self.tableExpenses.setItem(num, 0, QTableWidgetItem(str(expense.ID)))
            self.tableExpenses.setItem(num, 1, QTableWidgetItem(expense.date))
            self.tableExpenses.setItem(num, 2, QTableWidgetItem(str(expense.value)))
            self.tableExpenses.setItem(num, 3, QTableWidgetItem(expense.note))

    def init_incomes(self):
        for num, expense in enumerate(Incomes.list()):
            self.tableIncomes.insertRow(num)
            self.tableIncomes.setItem(num, 0, QTableWidgetItem(str(expense.ID)))
            self.tableIncomes.setItem(num, 1, QTableWidgetItem(expense.date))
            self.tableIncomes.setItem(num, 2, QTableWidgetItem(str(expense.value)))
            self.tableIncomes.setItem(num, 3, QTableWidgetItem(expense.note))
