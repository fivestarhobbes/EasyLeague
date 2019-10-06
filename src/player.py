# -*- coding: utf-8 -*-

"""
EasyLeague Player Class

This class stores the data about a player

Author: John Hsu and Sergey Satskiy

"""
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt


class Player:

    def __init__(self):
        self.memberID = None
        self.lastName = None
        self.firstName = None
        self.middleName = None
        self.sex = None
        self.rating = None
        self.expiration = None
        self.lastPlayed = None
        self.email = None

    def __str__(self):
        return self.firstName + " " + self.lastName


class PlayerTableItem(QTreeWidgetItem):

    def __init__(self, player):
        if type(player) == Player:
            items = [player.firstName + ' ' + player.lastName,
                     str(player.rating)]
        else:
            items = player
        QTreeWidgetItem.__init__(self, items)

    def __lt__(self, other):
        sortColumn = self.treeWidget().sortColumn()

        if sortColumn == 1:
            lhs = int(self.text(1))
            rhs = int(other.text(1))
            return lhs < rhs

        return QTreeWidgetItem.__lt__(self, other)

    def __str__(self):
        return self.data(0, Qt.DisplayRole)
