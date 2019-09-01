from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, qApp, QVBoxLayout, QTableWidget, QFormLayout, \
    QLineEdit, QCalendarWidget, QHBoxLayout, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, \
    QTableWidgetItem, QAbstractItemView, QMessageBox

from core.engine import GLog
from entities import Users, User
from state import *


class UsersForm(QMainWindow):
    def __init__(self, actualize_visual_state_callback):
        GLog.debug("ui.UsersForm.__init__")
        super().__init__()
        self.add_edit_dialog = None
        self.actualize_visual_state_callback = actualize_visual_state_callback
        uic.loadUi('ui/usersForm.ui', self)
        self.actionExit.triggered.connect(self.close)
        self.actionExit.setShortcut('Ctrl+W')
        self.actionAdd_item.triggered.connect(self.add_item)
        self.btnAdd.clicked.connect(self.add_item)
        self.actionRemove_item.triggered.connect(self.remove_item)
        self.btnRemove.clicked.connect(self.remove_item)
        self.actionEdit_item.triggered.connect(self.edit_item)
        self.btnEdit.clicked.connect(self.edit_item)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 350)
        self.init_data()

    def init_data(self):
        for num, user in enumerate(Users.list()):
            self.table.insertRow(num)
            self.table.setItem(num, 0, QTableWidgetItem(str(user.ID)))
            self.table.setItem(num, 1, QTableWidgetItem(user.name))
            self.table.setItem(num, 2, QTableWidgetItem(user.login))
            self.table.setItem(num, 3, QTableWidgetItem('Да' if user.admin else 'Нет'))

    def close(self):
        State[STATE_KEY_SECTION] = STATE_SECTION_MAIN_EXPENSES
        self.actualize_visual_state_callback()

    def add_item(self):
        State[STATE_KEY_ELEMENT] = None
        self.add_edit_dialog.init_value()
        if self.add_edit_dialog.exec():
            user = User.create({
                'is_admin': self.add_edit_dialog.isAdmin.isChecked(),
                'name': self.add_edit_dialog.userName.text(),
                'login': self.add_edit_dialog.userLogin.text(),
                'password': self.add_edit_dialog.userPassword.text(),
            })
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(user.ID)))
            self.table.setItem(row_number, 1, QTableWidgetItem(user.name))
            self.table.setItem(row_number, 2, QTableWidgetItem(user.login))
            self.table.setItem(row_number, 3, QTableWidgetItem('Да' if user.admin else 'Нет'))
            # self.table.resizeColumnsToContents()

    def edit_item(self):
        rows = self.table.selectionModel().selectedRows()
        if len(rows) != 1:
            # todo: говнокодство конечно... надо дисейблить кнопку пока ничего не выбрано или выбрано >1 в таблице... но времени нет
            msg = 'Пользователь не выбран/выбрано больше 1 пользователя, изменение невозможно'
            QMessageBox.information(self, 'Edit item', msg)
            return
        index = rows[0]
        GLog.debug('edit_item :: row: %s => User.ID:%s' % (index.row(), self.table.item(index.row(), 0).text()))
        State[STATE_KEY_ELEMENT] = {
            'id': self.table.item(index.row(), 0).text(),
            'name': self.table.item(index.row(), 1).text(),
            'login': self.table.item(index.row(), 2).text(),
            'is_admin': self.table.item(index.row(), 3).text() == "Да",
        }
        self.add_edit_dialog.init_value()
        if not self.add_edit_dialog.exec():
            return
        user = User.edit(State[STATE_KEY_ELEMENT]['id'], {
            'is_admin': self.add_edit_dialog.isAdmin.isChecked(),
            'name': self.add_edit_dialog.userName.text(),
            'login': self.add_edit_dialog.userLogin.text(),
            'password': self.add_edit_dialog.userPassword.text(),
        })
        self.table.setItem(index.row(), 0, QTableWidgetItem(str(user.ID)))
        self.table.setItem(index.row(), 1, QTableWidgetItem(user.name))
        self.table.setItem(index.row(), 2, QTableWidgetItem(user.login))
        self.table.setItem(index.row(), 3, QTableWidgetItem('Да' if user.admin else 'Нет'))
        # self.table.resizeColumnsToContents()

    def remove_item(self):
        rows = self.table.selectionModel().selectedRows()
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
                GLog.debug('remove_item :: row: %s => User.ID:%s' % (index.row(), self.table.item(index.row(), 0).text()))
                User.delete(self.table.item(index.row(), 0).text())
                self.table.model().removeRow(index.row())
