#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Group Utility

This file will contain functions that will help us make the groups.

Author: John Hsu

"""

import sys


def calculateNumberOfGroups(numberOfPlayers):
    if numberOfPlayers == 8:
        return 2
    if numberOfPlayers < 5:
        return 1
    return numberOfPlayers // 5


def calculateSizeOfEachGroup(numberOfPlayers, numberOfGroups):
    if numberOfPlayers == 8:
        return [4, 4]
    if numberOfPlayers == 9:
        return [4, 5]
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


def getGroups(numberOfPlayers):
    return calculateSizeOfEachGroup(
        numberOfPlayers,
        calculateNumberOfGroups(numberOfPlayers))


if __name__ == '__main__':
    retCode = 0
    if getGroups(2) != [2]:
        print("Failed for 2", file=sys.stderr)
        retCode += 1
    if getGroups(3) != [3]:
        print("Failed for 3", file=sys.stderr)
        retCode += 1
    if getGroups(4) != [4]:
        print("Failed for 4")
    if getGroups(5) != [5]:
        print("Failed for 5")
    if getGroups(6) != [6]:
        print("Failed for 6")
    if getGroups(7) != [7]:
        print("Failed for 7")
    if getGroups(8) != [4, 4]:
        print("Failed for 8")
    if getGroups(9) != [4, 5]:
        print("Failed for 9")
    if getGroups(10) != [5, 5]:
        print("Failed for 10")
    if getGroups(11) != [5, 6]:
        print("Failed for 11")
    if getGroups(12) != [6, 6]:
        print("Failed for 12")
    if getGroups(13) != [6, 7]:
        print("Failed for 13")
    if getGroups(14) != [7, 7]:
        print("Failed for 14")
    if getGroups(15) != [5, 5, 5]:
        print("Failed for 15")
    if getGroups(16) != [5, 5, 6]:
        print("Failed for 16")
    if getGroups(17) != [5, 6, 6]:
        print("Failed for 17")
    if getGroups(18) != [6, 6, 6]:
        print("Failed for 18")
    if getGroups(19) != [6, 6, 7]:
        print("Failed for 19")
    if getGroups(20) != [5, 5, 5, 5]:
        print("Failed for 20")
    if getGroups(21) != [5, 5, 5, 6]:
        print("Failed for 21")
    if getGroups(22) != [5, 5, 6, 6]:
        print("Failed for 22")
    if getGroups(23) != [5, 6, 6, 6]:
        print("Failed for 23")
    if getGroups(24) != [6, 6, 6, 6]:
        print("Failed for 24")
    if getGroups(25) != [5, 5, 5, 5, 5]:
        print("Failed for 25")
    if getGroups(26) != [5, 5, 5, 5, 6]:
        print("Failed for 26")
    sys.exit(retCode)
