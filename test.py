import sys

#from PyQt4 import QtGui
from PySide import QtGui

app = QtGui.QApplication(sys.argv)

file_browser = QtGui.QTreeView()
file_model = QtGui.QFileSystemModel()
file_model.setRootPath("/")
file_browser.setModel(file_model)
file_browser.show()

sys.exit(app.exec_())