import sys
from PySide import QtGui, QtCore
from qutepart import Qutepart


def main():
    app = QtGui.QApplication(sys.argv)
    qute = Qutepart()
    qute.show()
    app.exec_()

if __name__ == '__main__':
    main()
