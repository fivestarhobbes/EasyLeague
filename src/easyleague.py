#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EasyLeague Application

This program will allow users to setup and run a league.

Author: John Hsu

"""

import sys
from os.path import dirname, abspath, sep

from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication
from PyQt5.QtGui import QIcon



IMAGE_PATH = dirname(dirname(abspath(__file__))) + sep + "img" + sep

class EasyLeagueMainWindow(QMainWindow):
    """
    This method will create the main window for EasyLeague software

    """

    def __init__(self):
        """doc"""
        super().__init__()

        self.initUI()


    def initUI(self):
        """
        This method will create the initial screen for EasyLeague
        """
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        optionMenu = menubar.addMenu('Options')


        savAct = QAction(QIcon(IMAGE_PATH + "save.png"), 'Save', self)
        fileMenu.addAction(savAct)

        newAct = QAction(QIcon(IMAGE_PATH + "new.png"), 'New', self)
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
        loadFileAct.triggered.connect(self.onLoadFile)
        optionMenu.addAction(loadFileAct)

        self.setGeometry(200, 0, 1000, 800)
        self.setWindowTitle('EasyLeague')
        self.show()

    def onLoadFile(self, checked):
        print('Here you go')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EasyLeagueMainWindow()
    sys.exit(app.exec_())
