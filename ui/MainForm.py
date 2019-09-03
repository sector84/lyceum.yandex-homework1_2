from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, qApp, QVBoxLayout, QTableWidget, QFormLayout, \
    QLineEdit, QCalendarWidget, QHBoxLayout, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, \
    QTableWidgetItem, QAbstractItemView, QMessageBox

from core.engine import GLog
from entities import Expenses, Expense, Incomes, Income
from state import *


class MainForm(QMainWindow):
    def __init__(self, actualize_visual_state_callback):
        GLog.debug("ui.MainForm.__init__")
        super().__init__()
        self.add_edit_dialog = None
        self.actualize_visual_state_callback = actualize_visual_state_callback
        uic.loadUi('ui/mainForm.ui', self)
        self.actionExit.triggered.connect(qApp.quit)
        self.btnExit.clicked.connect(qApp.quit)

        self.actionAdminUsers.triggered.connect(self.open_users)
        self.actionAdd_item.triggered.connect(self.add_item)
        self.btnAdd.clicked.connect(self.add_item)
        self.actionRemove_item.triggered.connect(self.remove_item)
        self.btnRemove.clicked.connect(self.remove_item)
        self.actionEdit_item.triggered.connect(self.edit_item)
        self.btnEdit.clicked.connect(self.edit_item)

        self.tableIncomes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableIncomes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableExpenses.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableExpenses.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableIncomes.setColumnWidth(0, 80)
        self.tableIncomes.setColumnWidth(1, 150)
        self.tableIncomes.setColumnWidth(2, 100)
        self.tableIncomes.setColumnWidth(3, 350)

        self.tableExpenses.setColumnWidth(0, 80)
        self.tableExpenses.setColumnWidth(1, 150)
        self.tableExpenses.setColumnWidth(2, 100)
        self.tableExpenses.setColumnWidth(3, 350)

    def open_users(self):
        State[STATE_KEY_SECTION] = STATE_SECTION_ADMIN_USERS
        self.actualize_visual_state_callback()

    def recalc_elements_availability(self):
        cur_user = State[STATE_KEY_USER]
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
            self.tableExpenses.setItem(num, 1, QTableWidgetItem(expense.date_str))
            self.tableExpenses.setItem(num, 2, QTableWidgetItem(str(expense.value)))
            self.tableExpenses.setItem(num, 3, QTableWidgetItem(expense.note))

    def init_incomes(self):
        for num, income in enumerate(Incomes.list()):
            self.tableIncomes.insertRow(num)
            self.tableIncomes.setItem(num, 0, QTableWidgetItem(str(income.ID)))
            self.tableIncomes.setItem(num, 1, QTableWidgetItem(income.date_str))
            self.tableIncomes.setItem(num, 2, QTableWidgetItem(str(income.value)))
            self.tableIncomes.setItem(num, 3, QTableWidgetItem(income.note))

    def add_item(self):
        State[STATE_KEY_ELEMENT] = None
        entity = Expense if self.tabWidget.currentIndex() == 0 else Income
        table = self.tableExpenses if self.tabWidget.currentIndex() == 0 else self.tableIncomes
        self.add_edit_dialog.init_value()
        if self.add_edit_dialog.exec():
            try:
                dt = self.add_edit_dialog.dateTimeEdit.dateTime()
                res = entity.create({
                    'value': self.add_edit_dialog.valueDoubleSpinBox.value(),
                    'date': dt.toSecsSinceEpoch() + dt.offsetFromUtc(),
                    'note': self.add_edit_dialog.noteTextEdit.toPlainText(),
                })
            except Exception as e:
                # todo: хорошо бы конечно оповщение о том что пошло не так - но не в этой жизни...
                GLog.error("ui.MainForm.add_item :: error :%s" % e)
                return
            row_number = table.rowCount()
            table.insertRow(row_number)
            table.setItem(row_number, 0, QTableWidgetItem(str(res.ID)))
            table.setItem(row_number, 1, QTableWidgetItem(res.date_str))
            table.setItem(row_number, 2, QTableWidgetItem(str(res.value)))
            table.setItem(row_number, 3, QTableWidgetItem(res.note))
            # table.resizeColumnsToContents()

    def edit_item(self):
        entity = Expense if self.tabWidget.currentIndex() == 0 else Income
        table = self.tableExpenses if self.tabWidget.currentIndex() == 0 else self.tableIncomes
        rows = table.selectionModel().selectedRows()
        if len(rows) != 1:
            # todo: говнокодство конечно... надо дисейблить кнопку пока ничего не выбрано или выбрано >1 в таблице... но времени нет
            msg = 'Пользователь не выбран/выбрано больше 1 пользователя, изменение невозможно'
            QMessageBox.information(self, 'Edit item', msg)
            return
        index = rows[0]
        GLog.debug('edit_item :: row: %s => User.ID:%s' % (index.row(), table.item(index.row(), 0).text()))
        State[STATE_KEY_ELEMENT] = {
            'id': table.item(index.row(), 0).text(),
            'value': float(table.item(index.row(), 2).text()),
            'date': datetime.strptime(table.item(index.row(), 1).text(), '%Y-%m-%d %H:%M:%S').timestamp(),
            'note': table.item(index.row(), 3).text(),
        }
        self.add_edit_dialog.init_value()
        if not self.add_edit_dialog.exec():
            return
        try:
            res = entity.edit(State[STATE_KEY_ELEMENT]['id'], {
                'value': self.add_edit_dialog.valueDoubleSpinBox.value(),
                'date': self.add_edit_dialog.dateTimeEdit.dateTime().toSecsSinceEpoch(),
                'note': self.add_edit_dialog.noteTextEdit.toPlainText(),
            })
        except Exception as e:
            # todo: хорошо бы конечно оповщение о том что пошло не так - но не в этой жизни...
            GLog.error("ui.MainForm.edit_item :: error :%s" % e)
            return

        table.setItem(index.row(), 0, QTableWidgetItem(str(res.ID)))
        table.setItem(index.row(), 1, QTableWidgetItem(res.date_str))
        table.setItem(index.row(), 2, QTableWidgetItem(str(res.value)))
        table.setItem(index.row(), 3, QTableWidgetItem(res.note))
        # table.resizeColumnsToContents()

    def remove_item(self):
        entity = Expense if self.tabWidget.currentIndex() == 0 else Income
        table = self.tableExpenses if self.tabWidget.currentIndex() == 0 else self.tableIncomes
        rows = table.selectionModel().selectedRows()
        if len(rows) == 0:
            # todo: говнокодство конечно... надо дисейблить кнопку пока ничего не выбрано в таблице... но времени нет
            msg = 'Пользователь не выбран, удалять нечего'
            QMessageBox.information(self, 'Remove item', msg)
            return

        msg = f'Вы действительно хотете удалить {"пользователя" if len(rows) == 1 else "пользователей"}?'
        reply = QMessageBox.question(
            self, f'Remove item{"" if len(rows) == 1 else "s"}', msg,
            QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for index in sorted(rows, reverse=True):
                GLog.debug('remove_item :: row: %s => User.ID:%s' % (index.row(), table.item(index.row(), 0).text()))
                try:
                    entity = Expense if self.tabWidget.currentIndex() == 0 else Income
                    entity.delete(table.item(index.row(), 0).text())
                except Exception as e:
                    # todo: хорошо бы конечно оповщение о том что пошло не так - но не в этой жизни...
                    GLog.error("ui.MainForm.remove_item :: error :%s" % e)
                    return
                table.model().removeRow(index.row())
