import sys
from PyQt5.QtWidgets import QApplication
from ui import LoginForm, MainForm


def on_login_success():
    loginForm.hide()
    mainForm.recalc_elements_availability()
    mainForm.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    loginForm = LoginForm(on_login_success)
    loginForm.show()
    sys.exit(app.exec())
