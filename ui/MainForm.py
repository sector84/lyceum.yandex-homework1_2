from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from core.engine import GLog


class MainForm(QMainWindow):
    def __init__(self):
        GLog.debug("ui.MainForm.__init__")
        super().__init__()
        uic.loadUi('ui/MainForm.ui', self)
