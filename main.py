#!/usr/bin/env python

import os

from PySide import QtCore, QtGui
from core.sidebar import SidebarTreeView

from core.tab import EditorTab


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setup_file_menu()
        self.setup_help_menu()

        self.setup_styles()
        self.setup_signals()

        self.setup_ui()

    def setup_ui(self):
        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.workspace_close)

        self.tree = SidebarTreeView()

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.tabs)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.splitter)
        self.setLayout(hbox)
        self.setCentralWidget(self.splitter)

        self.workspace_new()

        # self.setCentralWidget(self.tabs)
        self.setWindowTitle("Syntax Highlighter")

    def setup_styles(self):
        self.style_path = 'assets/css/style.css'
        if os.path.exists(self.style_path):
            self.setStyleSheet(open(self.style_path).read())

    def setup_signals(self):
        pass

    def about(self):
        QtGui.QMessageBox.about(self, "About Syntax Highlighter",
                                "<p>The <b>Syntax Highlighter</b> example shows how to " \
                                "perform simple syntax highlighting by subclassing the " \
                                "QSyntaxHighlighter class and describing highlighting " \
                                "rules using regular expressions.</p>")

    def new_file(self):
        self.editor.clear()

    def workspace_new(self):
        tab = EditorTab()
        icon = QtGui.QIcon("assets/icon/file.png")

        index = self.tabs.addTab(tab, icon, self.tr("Untitled"))
        self.tabs.setCurrentIndex(index)
        return tab

    def workspace_close(self, index):
        self.tabs.removeTab(index)

    def workspace_active_close(self):
        index = self.tabs.currentIndex()
        self.workspace_close(index)

    def close_window(self):
        for i in range(self.tabs.count()):
            pass

    def openFile(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open File", '', "*.*")

        if path:
            inFile = QtCore.QFile(path[0])
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                text = inFile.readAll()

                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)

                tab = self.workspace_new()
                tab.editor.setPlainText(text)


    def setup_file_menu(self):
        fileMenu = QtGui.QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction("&New tab...", self.workspace_new, "Ctrl+T")
        fileMenu.addAction("&New window...", self.new_file, "Ctrl+N")
        fileMenu.addAction("&Refresh...", self.setup_styles, "Ctrl+R")
        fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        fileMenu.addAction("&Close...", self.workspace_active_close, "Ctrl+W")
        fileMenu.addAction("E&xit", QtGui.qApp.quit, "Ctrl+Q")

    def setup_help_menu(self):
        helpMenu = QtGui.QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction("&About", self.about)
        helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 512)
    window.show()

    sys.exit(app.exec_())
