import sys
from PyQt5.QtWidgets import QApplication
from ui import LoginForm


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = LoginForm()
    wnd.show()
    sys.exit(app.exec())
