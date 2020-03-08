#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EasyLeague Application

This program will allow users to setup and run a league.

Author: John Hsu and Sergey Satskiy

"""

from util import setFullHeight
from grouputil import getGroups
from createPlayerDialog import CreatePlayerDialog
from player import Player, PlayerTableItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence, QCursor
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication,
                             QPushButton, QDialog, QFileDialog, QMessageBox,
                             QShortcut, QTreeWidget, QAbstractItemView,
                             QVBoxLayout, QHBoxLayout, QLabel, QWidget,
                             QTreeWidgetItem, QHeaderView, QLayout,
                             QScrollArea)
import csv
import sys
from os.path import dirname, abspath, sep
from enum import Enum
sys.path.insert(0, dirname(__file__))


IMAGE_PATH = dirname(dirname(abspath(__file__))) + sep + "img" + sep
MAX_NUMBER_OF_GROUPS = 100


class Direction(Enum):
    UP = -1
    DOWN = 1


class EasyLeagueMainWindow(QMainWindow):
    """
    This method will create the main window for EasyLeague software

    """

    def __init__(self):
        """doc"""
        super().__init__()
        self.__roster = []
        self.__rosterTable = None
        self.__leagueTable = None
        self.__vLayout = None
        self.__groups = []
        self.__selectedItem = None
        self.__initUI()

    def __initUI(self):
        """
        This method will create the initial screen for EasyLeague
        """
        self.__createMainMenu()
        self.__createGroupContextMenu()
        self.__createToolbar()
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

        createPlayerButton = QPushButton('Create Player', self)
        createPlayerButton.clicked.connect(self.__onCreatePlayer)

        createGroupsButton = QPushButton('Create Groups', self)
        createGroupsButton.clicked.connect(self.__onCreateGroups)

        toolbar.addWidget(loadButton)
        toolbar.addWidget(createPlayerButton)
        toolbar.addWidget(createGroupsButton)

    def __createTable(self):
        table = QTreeWidget()
        table.setAlternatingRowColors(True)
        table.setRootIsDecorated(False)
        table.setItemsExpandable(False)
        table.setSortingEnabled(True)
        table.sortByColumn(1, Qt.DescendingOrder)
        table.setUniformRowHeights(True)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        headerLabels = ["Name", "Rating"]
        table.setHeaderLabels(headerLabels)
        table.header().setSectionResizeMode(0, QHeaderView.Stretch)
        table.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        return table

    def __createLayout(self):

        # Create roster vBox
        rosterVbox = QVBoxLayout()
        self.__rosterLabel = QLabel("Roster")
        rosterVbox.addWidget(self.__rosterLabel)
        self.__rosterTable = self.__createTable()
        self.__rosterTable.itemSelectionChanged.connect(self.__onRosterSelect)
        rosterVbox.addWidget(self.__rosterTable)
        self.__rosterButton = QPushButton("Add")
        self.__rosterButton.setEnabled(False)
        self.__rosterButton.clicked.connect(self.__onAddToLeague)
        rosterVbox.addWidget(self.__rosterButton)

        # Create League vBox
        leagueVbox = QVBoxLayout()
        self.__leagueLabel = QLabel("League")
        leagueVbox.addWidget(self.__leagueLabel)
        self.__leagueTable = self.__createTable()
        self.__leagueTable.itemSelectionChanged.connect(self.__onLeagueSelect)
        leagueVbox.addWidget(self.__leagueTable)
        self.__leagueButton = QPushButton("Remove")
        self.__leagueButton.setEnabled(False)
        self.__leagueButton.clicked.connect(self.__onRemoveFromLeague)
        leagueVbox.addWidget(self.__leagueButton)

        # Create Groups vBox
        class ScrollContainer(QWidget):
            def __init__(self):
                QWidget.__init__(self)
                self.layout = QVBoxLayout()
                self.layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
                self.setLayout(self.layout)
        scrollContainer = ScrollContainer()

#        groupVbox = QVBoxLayout()
        groupLabel = QLabel("Groups")
#        groupVbox.addWidget(groupLabel)
        scrollContainer.layout.addWidget(groupLabel)
        for groupNumber in range(MAX_NUMBER_OF_GROUPS):
            groupNumberLabel = QLabel("Group " + str(groupNumber + 1))
            groupNumberTable = self.__createTable()
            groupNumberTable.setContextMenuPolicy(Qt.CustomContextMenu)
            groupNumberTable.customContextMenuRequested.connect(
                self.__handleShowPlayerContextMenu)
#            groupVbox.addWidget(groupNumberLabel)
#            groupVbox.addWidget(groupNumberTable)
            scrollContainer.layout.addWidget(groupNumberLabel)
            scrollContainer.layout.addWidget(groupNumberTable)
            self.__groups.append([groupNumberLabel, groupNumberTable])
        self.__hideGroups()

        groupScroll = QScrollArea()
        groupScroll.setWidget(scrollContainer)

        mainHbox = QHBoxLayout()
        mainHbox.addLayout(rosterVbox)
        mainHbox.addLayout(leagueVbox)
#        mainHbox.addLayout(groupVbox)
        mainHbox.addWidget(groupScroll)

        mainWidget = QWidget()
        mainWidget.setLayout(mainHbox)

        self.setCentralWidget(mainWidget)

    def __createGroupContextMenu(self):
        """Create the context menu for a group"""
        self.__groupMenu = QMenu(self)
        self.__moveUpMenuItem = self.__groupMenu.addAction(
            'Move Up', self.__movePlayerUp)
        self.__moveDownMenuItem = self.__groupMenu.addAction(
            'Move Down', self.__movePlayerDown)

    def __movePlayerUp(self):
        self.__movePlayer(Direction.UP)

    def __movePlayerDown(self):
        self.__movePlayer(Direction.DOWN)

    def __movePlayer(self, direction):
        # Add to the target group
        targetGroupIndex = self.__selectedItem[1] + direction
        targetGroup = self.__groups[targetGroupIndex][1]
        playerName = self.__selectedItem[0].data(0, Qt.DisplayRole)
        playerRating = self.__selectedItem[0].data(1, Qt.DisplayRole)
        targetGroup.addTopLevelItem(
            PlayerTableItem([playerName, playerRating]))

        # Remove from the source group
        sourceGroupIndex = self.__selectedItem[1]
        sourceGroup = self.__groups[sourceGroupIndex][1]
        sourceGroup.takeTopLevelItem(sourceGroup.currentIndex().row())

        # Re-adjust height
        setFullHeight(targetGroup)
        setFullHeight(sourceGroup)

        # Re-sort the view by rating
        targetGroup.sortByColumn(1, Qt.DescendingOrder)

    def __handleShowPlayerContextMenu(self, coord):
        lastGroupIndex = self.__getVisibleGroups() - 1
        for groupNumber, groupInfo in enumerate(self.__groups):
            if groupInfo[1].hasFocus():
                playerItem = groupInfo[1].itemAt(coord)
                if playerItem is not None:
                    self.__selectedItem = (playerItem, groupNumber)
                    self.__moveUpMenuItem.setEnabled(groupNumber != 0)
                    self.__moveDownMenuItem.setEnabled(
                        groupNumber != lastGroupIndex)
                    self.__groupMenu.popup(QCursor.pos())
                    break

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
                    if row[5] == "":
                        player.rating = 0
                    else:
                        player.rating = int(row[5])
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

        self.__populate()

    def __onCreatePlayer(self):
        """Create a new player"""
        playerDialog = CreatePlayerDialog(self)
        if playerDialog.exec_() == QDialog.Rejected:
            return
        name = playerDialog.nameEdit.text().strip()
        for index in range(self.__rosterTable.topLevelItemCount()):
            item = self.__rosterTable.topLevelItem(index)
            if item.data(0, Qt.DisplayRole).lower() == name.lower():
                QMessageBox.critical(
                    self, "Error", "Player is already in the roster")
                return
        for index in range(self.__leagueTable.topLevelItemCount()):
            item = self.__leagueTable.topLevelItem(index)
            if item.data(0, Qt.DisplayRole).lower() == name.lower():
                QMessageBox.critical(
                    self, "Error", "Player is already in the league")
                return
        rating = playerDialog.ratingEdit.text().strip()
        self.__leagueTable.addTopLevelItem(PlayerTableItem([name, rating]))
        self.__updateLeagueLabel()

    def __onCreateGroups(self):
        if self.__leagueTable.topLevelItemCount() == 0:
            QMessageBox.critical(self, "Error", "League is empty")
            return
        groups = getGroups(self.__leagueTable.topLevelItemCount())
        if len(groups) > MAX_NUMBER_OF_GROUPS:
            QMessageBox.critical(self, "Error", "Too many groups")
            return
        self.__hideGroups()
        tempLeague = []
        for index in range(self.__leagueTable.topLevelItemCount()):
            item = self.__leagueTable.topLevelItem(index)
            name = item.data(0, Qt.DisplayRole)
            rating = int(item.data(1, Qt.DisplayRole))
            tempLeague.append((name, rating))

        def sortSecond(val):
            return val[1]

        tempLeague.sort(key=sortSecond, reverse=True)
        # print(tempLeague)
        tempLeagueIndex = 0
        currGroup = 0
        for size in groups:
            for index in range(size):
                player = tempLeague[tempLeagueIndex]
                name = player[0]
                rating = player[1]
                self.__groups[currGroup][1].addTopLevelItem(
                    PlayerTableItem([name, str(rating)]))
                tempLeagueIndex += 1
            currGroup += 1
        self.__showGroups(len(groups))
        self.hide()
        self.show()

    def __populate(self):
        for player in self.__roster:
            self.__rosterTable.addTopLevelItem(PlayerTableItem(player))
        self.__updateRosterLabel()

    def __onRosterSelect(self):
        if len(self.__rosterTable.selectedItems()) >= 1:
            self.__rosterButton.setEnabled(True)
        else:
            self.__rosterButton.setEnabled(False)

    def __onLeagueSelect(self):
        if len(self.__leagueTable.selectedItems()) >= 1:
            self.__leagueButton.setEnabled(True)
        else:
            self.__leagueButton.setEnabled(False)

    def __onAddToLeague(self):
        selectedItem = self.__rosterTable.selectedItems()[0]
        self.__leagueTable.addTopLevelItem(
            PlayerTableItem([selectedItem.data(0, Qt.DisplayRole),
                             selectedItem.data(1, Qt.DisplayRole)]))
        self.__rosterTable.takeTopLevelItem(
            self.__rosterTable.currentIndex().row())
        self.__updateRosterLabel()
        self.__updateLeagueLabel()

    def __onRemoveFromLeague(self):
        selectedItem = self.__leagueTable.selectedItems()[0]
        self.__rosterTable.addTopLevelItem(PlayerTableItem(
            [selectedItem.data(0, Qt.DisplayRole), selectedItem.data(1, Qt.DisplayRole)]))
        self.__leagueTable.takeTopLevelItem(
            self.__leagueTable.currentIndex().row())
        self.__updateRosterLabel()
        self.__updateLeagueLabel()

    def __hideGroups(self):
        for index, group in enumerate(self.__groups):
            if index == 0:
                group[1].clear()
                continue
            group[0].setVisible(False)
            group[1].setVisible(False)
            group[1].clear()

    def __showGroups(self, numberOfGroups):
        for groupIndex in range(numberOfGroups):
            self.__groups[groupIndex][0].setVisible(True)
            self.__groups[groupIndex][1].setVisible(True)
            setFullHeight(self.__groups[groupIndex][1])

    def __updateRosterLabel(self):
        self.__rosterLabel.setText(
            'Roster (' + str(self.__rosterTable.topLevelItemCount()) + ')')
        self.hide()
        self.show()

    def __updateLeagueLabel(self):
        self.__leagueLabel.setText(
            'League (' + str(self.__leagueTable.topLevelItemCount()) + ')')
        self.hide()
        self.show()

    def __getVisibleGroups(self):
        numberVisible = 0
        for groupInfo in self.__groups:
            if groupInfo[1].isVisible():
                numberVisible += 1
        return numberVisible


def main():
    app = QApplication(sys.argv)
    ex = EasyLeagueMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
