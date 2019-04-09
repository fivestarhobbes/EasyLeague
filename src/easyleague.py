#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EasyLeague Application

This program will allow users to setup and run a league.

Author: John Hsu

"""

import sys, csv
from os.path import dirname, abspath, sep

from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication,
                            QPushButton, QDialog, QFileDialog, QMessageBox, QShortcut, QTreeWidget, QAbstractItemView, QVBoxLayout)
from PyQt5.QtGui import QIcon, QKeySequence

from  player import Player


IMAGE_PATH = dirname(dirname(abspath(__file__))) + sep + "img" + sep

class EasyLeagueMainWindow(QMainWindow):
    """
    This method will create the main window for EasyLeague software

    """

    def __init__(self):
        """doc"""
        super().__init__()
        self.__roster = []
        self.__table = None
        self.__vLayout = None
        self.__initUI()


    def __initUI(self):
        """
        This method will create the initial screen for EasyLeague
        """
        self.__createMainMenu()
        self.__createToolbar()
        self.__createTable()
        self.__createLayout()
        self.setGeometry(200, 0, 1000, 800)
        self.setWindowTitle('EasyLeague')
        self.show()

    def __createMainMenu(self):
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

        self.loadFileAct = QAction('Load File', self)
        self.loadFileAct.triggered.connect(self.__onLoadFile)
        optionMenu.addAction(self.loadFileAct)

        self.loadShortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.loadShortcut.activated.connect(self.__onLoadFile)

    def __createToolbar(self):
        toolbar = self.addToolBar("Load")
        loadButton = QPushButton('Load', self)
        loadButton.setToolTip("Load File (Command+O)")
        loadButton.setIcon(QIcon(IMAGE_PATH + "load.png"))
        loadButton.clicked.connect(self.__onLoadFile)
        toolbar.addWidget(loadButton)

    def __createTable(self):
        self.__table = QTreeWidget()
        self.__table.setAlternatingRowColors(True)
        self.__table.setRootIsDecorated(False)
        self.__table.setItemsExpandable(False)
        self.__table.setSortingEnabled(True)
        self.__table.setUniformRowHeights(True)
        self.__table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.__table.setSelectionBehavior(QAbstractItemView.SelectRows)

        headerLabels = ["Name", "Rating"]
        self.__table.setHeaderLabels(headerLabels)

    def __createLayout(self):
    #    self.__vLayout = QVBoxLayout(self)
    #    self.__vLayout.addWidget(self.__table)
        self.setCentralWidget(self.__table)

    def __onLoadFile(self, checked=None):
        dialog = QFileDialog(self, 'Open League Roster')
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        if dialog.exec_() != QDialog.Accepted:
            return

        files = dialog.selectedFiles()
        if len(files) != 1:
            QMessageBox.critical(self, "Error", "Only 1 file can be selected")
            return

        selectedFile = files[0]
        if not selectedFile.endswith('.csv'):
            QMessageBox.critical(self, "Error", "file must be a .csv file")
            return
        try:
            with open(selectedFile) as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                self.__roster = []
                firstRow = True
                for row in csvReader:
                    if firstRow:
                        firstRow = False
                        continue

                    player = Player()
                    player.memberID = row[0]
                    player.lastName = row[1]
                    player.firstName = row[2]
                    player.middleName = row[3]
                    player.sex = row[4]
                    player.rating = row[5]
                    player.expiration = row[6]
                    player.lastPlayed = row[7]
                    player.email = row[8]
                    self.__roster.append(player)

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            return
        except:
            QMessageBox.critical(self, "Error", "unknown error")
            return

        for item in self.__roster:
            print(str(item))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EasyLeagueMainWindow()
    sys.exit(app.exec_())
