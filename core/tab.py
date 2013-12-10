# coding=utf-8

from PySide import QtGui
from core.highlighter import Highlighter
from qutepart import Qutepart


class EditorTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupEditor()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.editor)
        # mainLayout.addStretch(1)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.editor.adjustSize()
        self.setLayout(mainLayout)

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily('Monaco')
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.editor = Qutepart()
        # self.editor.setFont(font)
        self.editor.adjustSize()

        # self.highlighter = Highlighter(self.editor.document())