from PyQt5 import uic
from PyQt5.QtCore import QDateTime
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
        ts = State[STATE_KEY_ELEMENT].get('date', 0) if State[STATE_KEY_ELEMENT] else 0
        d = QDateTime.fromSecsSinceEpoch(ts) if ts > 0 else QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(d)
        self.noteTextEdit.setPlainText(State[STATE_KEY_ELEMENT].get('note', '') if State[STATE_KEY_ELEMENT] else '')
