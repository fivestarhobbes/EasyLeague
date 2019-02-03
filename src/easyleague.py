#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This program creates a submenu.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        optionMenu = menubar.addMenu('Options')

        savAct = QAction('Save', self)
        fileMenu.addAction(savAct)

        newAct = QAction('New', self)
        fileMenu.addAction(newAct)

        createGrpAct = QAction('Create Group', self)
        optionMenu.addAction(createGrpAct)

        createLstAct = QAction('Create New List', self)
        optionMenu.addAction(createLstAct)

        addPlayerAct = QAction('Add Player', self)
        optionMenu.addAction(addPlayerAct)

        rmvPlayerAct = QAction('Remove Player', self)
        optionMenu.addAction(rmvPlayerAct)

        loadFileAct = QAction('Load File', self)
        optionMenu.addAction(loadFileAct)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')
        self.show()


if __name__ == '__main__':
    print("Before")
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
