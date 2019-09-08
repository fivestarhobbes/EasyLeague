# -*- coding: utf-8 -*-

"""
Group Utility

This file will contain functions that will help us make the groups.

Author: John Hsu

"""


def calculateNumberOfGroups(numberOfPlayers):
    if numberOfPlayers == 8:
        return 2
    if numberOfPlayers < 5:
        return 1
    return numberOfPlayers / 5


def calculateSizeOfEachGroup(numberOfPlayers, numberOfGroups):
    if numberOfPlayers == 8:
        return [4, 4]
    if numberOfPlayers <= 7:
        return [numberOfPlayers]
    groupSizeList = [5 for x in range(numberOfGroups)]
    playersLeftOver = numberOfPlayers % 5
    index = len(groupSizeList) - 1
    while playersLeftOver > 0:
        groupSizeList[index] += 1
        playersLeftOver -= 1
        if index == 0:
            index = len(groupSizeList) - 1
        else:
            index -= 1
    return groupSizeList
