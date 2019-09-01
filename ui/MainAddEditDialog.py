from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from core.engine import GLog
from state import *


class MainAddEditDialog(QDialog):
    def __init__(self, *args):
        GLog.debug("ui.MainAddEditDialog.__init__")
        super().__init__(*args)
        uic.loadUi('ui/mainAddEditDialog.ui', self)
        self.btnSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.close)
        self.init_value()

    def init_value(self):
        self.valueDoubleSpinBox.setValue(State[STATE_KEY_ELEMENT].get('value', 0) if State[STATE_KEY_ELEMENT] else 0)
        self.dateTimeEdit.setDateTime(State[STATE_KEY_ELEMENT].get('date', '') if State[STATE_KEY_ELEMENT] else '')
        self.noteTextEdit.setText(State[STATE_KEY_ELEMENT].get('note', '') if State[STATE_KEY_ELEMENT] else '')
