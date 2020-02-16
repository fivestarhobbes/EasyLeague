# -*- coding: utf-8 -*-
"""

This file holds the utility functions for EasyLeague

Author: John Hsu and Sergey Satskiy

"""


def setFullHeight(treeWidget):
    """
    Sets the full height for a QTreeWidget object to display all rows.
    """
    fullHeight = 0
    topLevelCount = treeWidget.topLevelItemCount()

    for rowIndex in range(topLevelCount):
        item = treeWidget.topLevelItem(rowIndex)
        fullHeight += treeWidget.rowHeight(treeWidget.indexFromItem(item))

    if fullHeight != 0:
        fullHeight += treeWidget.header().sizeHint().height()
        treeWidget.setMinimumHeight(fullHeight + 5)
