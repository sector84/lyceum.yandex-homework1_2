from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from core.engine import GLog
from state import *


class UserAddEditDialog(QDialog):
    def __init__(self, *args):
        GLog.debug("ui.UserAddEditDialog.__init__")
        super().__init__(*args)
        uic.loadUi('ui/userAddEditDialog.ui', self)
        self.bntSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.close)
        self.init_value()

    def init_value(self):
        self.isAdmin.setChecked(State[STATE_KEY_ELEMENT].get('is_admin', False) if State[STATE_KEY_ELEMENT] else False)
        self.userName.setText(State[STATE_KEY_ELEMENT].get('name', '') if State[STATE_KEY_ELEMENT] else '')
        self.userLogin.setText(State[STATE_KEY_ELEMENT].get('login', '') if State[STATE_KEY_ELEMENT] else '')
        self.userPassword.setText('')
