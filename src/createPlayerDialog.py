from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QGridLayout, QLabel, QLineEdit)

from PyQt5.QtCore import Qt

class CreatePlayerDialog(QDialog):
    
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.__createLayout()
        self.setWindowTitle("Create Player")

    def __createLayout(self):
        """Creates the dialog layout"""
        self.resize(300, 100)
        self.setSizeGripEnabled(True)

        verticalLayout = QVBoxLayout(self)
        gridLayout = QGridLayout()

        # Player Name
        nameLabel = QLabel("Player Name", self)
        gridLayout.addWidget(nameLabel, 0, 0, 1, 1)
        self.nameEdit = QLineEdit(self)
        self.nameEdit.setToolTip("Type a player name")
        self.nameEdit.textEdited.connect(self.__onUserInputChanged)
        gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)

        # Player Rating
        ratingLabel = QLabel("Player Rating", self)
        gridLayout.addWidget(ratingLabel, 1, 0, 1, 1)
        self.ratingEdit = QLineEdit(self)
        self.ratingEdit.setToolTip("Type a rating")
        self.ratingEdit.textEdited.connect(self.__onUserInputChanged)
        gridLayout.addWidget(self.ratingEdit, 1, 1, 1, 1)



        verticalLayout.addLayout(gridLayout)

        # Buttons at the bottom
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel |
                                     QDialogButtonBox.Ok)
        verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
 
        # Add connections
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        

    def __isUserInputValid(self):
        if self.nameEdit.text().strip() == '':
            return False
        ratingValue = self.ratingEdit.text().strip()
        if ratingValue == '':
            return False
        try:
           rating = int(ratingValue)
           if rating < 0:
               return False
        except:
            return False
        return True

    def __onUserInputChanged(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.__isUserInputValid())


