import sys
from PyQt5.QtWidgets import QApplication
from ui import LoginForm, MainForm, UsersForm, UserAddEditDialog, MainAddEditDialog
from state import *


def actualize_visual_state():
    if State[STATE_KEY_SECTION] == STATE_SECTION_MAIN_EXPENSES:
        loginForm.hide()
        usersForm.hide()
        mainForm.show()
    elif State[STATE_KEY_SECTION] == STATE_SECTION_MAIN_INCOMES:
        loginForm.hide()
        usersForm.hide()
        mainForm.show()
    elif State[STATE_KEY_SECTION] == STATE_SECTION_ADMIN_USERS:
        loginForm.hide()
        mainForm.hide()
        usersForm.show()


def on_login_success():
    State[STATE_KEY_SECTION] = STATE_SECTION_MAIN_EXPENSES
    mainForm.recalc_elements_availability()
    mainForm.init_data()
    actualize_visual_state()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm(actualize_visual_state)
    mainForm.add_edit_dialog = MainAddEditDialog(mainForm)
    usersForm = UsersForm(actualize_visual_state)
    usersForm.add_edit_dialog = UserAddEditDialog(usersForm)
    loginForm = LoginForm(on_login_success)
    loginForm.show()
    sys.exit(app.exec())
