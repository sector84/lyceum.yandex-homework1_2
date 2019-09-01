from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from core.engine import GLog
from entities import User
import state


class LoginForm(QDialog):
    def __init__(self, on_login_success):
        GLog.debug("ui.LoginForm.__init__")
        super().__init__()
        self.on_login_success = on_login_success
        uic.loadUi('ui/loginForm.ui', self)
        self.btnLogin.clicked.connect(self.on_login)

    def on_login(self):
        GLog.debug("ui.LoginForm.on_login")
        login = self.inputLogin.text()
        password = self.inputPass.text()
        GLog.info(f"ui.LoginForm.on_login :: try to login as: {login}")
        user = User.select_by_credentials(login, password)
        if user.ID > 0:
            state.State[state.STATE_KEY_USER] = user
            state.State[state.STATE_KEY_SECTION] = state.STATE_SECTION_MAIN_EXPENSES
            self.on_login_success()
