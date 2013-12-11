#!/usr/bin/env python

import os
import gc

from PySide import QtCore, QtGui
from core.sidebar import SidebarTreeView

from core.tab import EditorTab


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setup_styles()
        self.setup_signals()
        self.setup_ui()
        self.setup_file_menu()
        self.setup_help_menu()

    def setup_ui(self):
        self.statusBar().showMessage('Ready')

        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.workspace_close)

        self.tree = SidebarTreeView()
        self.tree.doubleClicked.connect(self.tree_open_file)

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.tabs)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.splitter)
        self.setLayout(hbox)
        self.setCentralWidget(self.splitter)

        # self.setCentralWidget(self.tabs)
        self.setWindowTitle("Shadow IDE")

    def setup_styles(self):
        self.style_path = 'assets/css/style.css'
        if os.path.exists(self.style_path):
            self.setStyleSheet(open(self.style_path).read())

    def setup_signals(self):
        pass

    def setup_workspace(self, path):
        self.tree.open_directory(path)

    def about(self):
        QtGui.QMessageBox.about(self, "About Syntax Highlighter",
                                "<p>The <b>Syntax Highlighter</b> example shows how to " \
                                "perform simple syntax highlighting by subclassing the " \
                                "QSyntaxHighlighter class and describing highlighting " \
                                "rules using regular expressions.</p>")

    def workspace_new(self, path=None):
        tab = EditorTab()
        icon = QtGui.QIcon("assets/icon/file.png")

        index = self.tabs.addTab(tab, icon, os.path.basename(path) if path else self.tr("Untitled"))
        self.tabs.setCurrentIndex(index)
        return tab

    def workspace_close(self, index):
        self.tabs.removeTab(index)

    def workspace_active(self):
        index = self.tabs.currentIndex()
        return self.tabs.widget(index)

    def workspace_active_close(self):
        index = self.tabs.currentIndex()
        self.workspace_close(index)

    def close_window(self):
        for i in range(self.tabs.count()):
            pass

    def open_directory(self, path=None):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        # directory = QtGui.QFileDialog.getExistingDirectory(self,
        #                                            "QFileDialog.getExistingDirectory()",
        #                                            '', options)
        # if directory:
        #     print(directory)
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open directory", '', options)
        if path:
            self.setup_workspace(path)

    def tree_open_file(self, index):
        path = self.tree.model().filePath(index)
        if not os.path.isdir(path):
            return self.open_file(path)

    def open_file(self, path=None):
        inFile = QtCore.QFile(path)
        if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            text = inFile.readAll()
            try:
                text = str(text, encoding='ascii')
            except TypeError:
                text = str(text)

            tab = self.workspace_new(path)
            tab.editor.setPlainText(text)
            tab.editor.detectSyntax(sourceFilePath=path)

    def setup_file_menu(self):
        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addAction("&New file", self.workspace_new, "Ctrl+T")
        fileMenu.addAction("&Open directory...", self.open_directory, "Ctrl+O")
        fileMenu.addSeparator()
        fileMenu.addAction("&Save", self.save, QtGui.QKeySequence.Save)
        fileMenu.addAction("Save &As...", self.saveAs, QtGui.QKeySequence.SaveAs)
        fileMenu.addSeparator()
        fileMenu.addAction("&Close", self.workspace_active_close, "Ctrl+W")
        fileMenu.addSeparator()
        fileMenu.addAction("E&xit", QtGui.qApp.quit, "Ctrl+Q")
        self.menuBar().addMenu(fileMenu)

        settings_menu = QtGui.QMenu("&Settings", self)
        settings_menu.addAction("&Refresh styles", self.setup_styles, "Ctrl+R")
        self.menuBar().addMenu(settings_menu)

        # bookmark_menu = QtGui.QMenu("&Bookmark", self)
        # bookmark_menu.addAction(self.workspace_active().editor.toggleBookmarkAction)
        # bookmark_menu.addAction(self.workspace_active().editor.prevBookmarkAction)
        # bookmark_menu.addAction(self.workspace_active().editor.nextBookmarkAction)
        # self.menuBar().addMenu(bookmark_menu)

        # edit_menu = QtGui.QMenu("&Edit", self)
        # edit_menu.addAction(self.workspace_active().editor.moveLineUpAction)
        # edit_menu.addAction(self.workspace_active().editor.moveLineDownAction)
        # self.menuBar().addMenu(edit_menu)

    def setup_help_menu(self):
        helpMenu = QtGui.QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction("&About", self.about)
        helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, "Save As", self.curFile)

        if not fileName:
            return False

        return self.saveFile(fileName)

    def documentWasModified(self):
        self.setWindowModified(True)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


def app_quit():
    global file_browser
    file_browser = None
    gc.collect()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    app.lastWindowClosed.connect(app_quit)
    window = MainWindow()
    window.resize(800, 512)
    window.show()

    sys.exit(app.exec_())
