import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import json
from enum import Enum

import word
from word import Word

header_font = QtGui.QFont("OpenSans", 28)
button_font = QtGui.QFont("OpenSans", 16)
inapp_font = QtGui.QFont("OpenSans", 12)

class Menu(Enum):
    MAIN_MENU = 1
    ADD_WORD = 2
    SEARCH_WORD = 3
    PLAY_GAME = 4
    REMOVE_WORDS = 5
    SURF_WORDS = 6

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.wordData = dict()
        self.loadWords()

        self.mainLayout = QtWidgets.QHBoxLayout()

        self.windowSize = (600, 800)
        self.setWindowTitle("Your Dictionary")
        self.setGeometry(0, 0, self.windowSize[0], self.windowSize[1])
        self.center()

        self.switchMenu(Menu.MAIN_MENU)

        self.show()

    def switchMenu(self, menu: Menu):
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)

        if menu == Menu.MAIN_MENU:
            self.createMainMenu()
            self.central.setLayout(self.mainMenuHLayout)
        elif menu == Menu.ADD_WORD:
            self.createAddWordMenu()
            self.central.setLayout(self.addWordHLayout)
        else:
            self.central.setLayout(self.mainMenuHLayout)


    def createMainMenu(self):
        self.mainMenuHLayout = QtWidgets.QHBoxLayout()
        self.mainMenuVLayout = QtWidgets.QVBoxLayout()

        self.mainTitle = QtWidgets.QLabel("Your Dictionary")
        self.mainTitle.setFont(header_font)
        self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.addAWordButton = QtWidgets.QPushButton("Add Word")
        self.addAWordButton.clicked.connect(lambda: self.switchMenu(Menu.ADD_WORD))

        self.searchWordButton = QtWidgets.QPushButton("Search Word")
        self.searchWordButton.clicked.connect(lambda: self.switchMenu(Menu.SEARCH_WORD))

        self.gameButton = QtWidgets.QPushButton("Word Game")
        self.gameButton.clicked.connect(lambda: self.switchMenu(Menu.PLAY_GAME))

        self.removeWordsButton = QtWidgets.QPushButton("Remove Words")
        self.removeWordsButton.clicked.connect(lambda: self.switchMenu(Menu.REMOVE_WORDS))

        self.surfWordsButton = QtWidgets.QPushButton("Surf Words")
        self.surfWordsButton.clicked.connect(lambda: self.switchMenu(Menu.SURF_WORDS))

        self.quitButton = QtWidgets.QPushButton("Quit Application")
        self.quitButton.clicked.connect(self.close)

        self.mainMenuButtons = []
        self.mainMenuButtons.append(self.addAWordButton)
        self.mainMenuButtons.append(self.searchWordButton)
        self.mainMenuButtons.append(self.gameButton)
        self.mainMenuButtons.append(self.removeWordsButton)
        self.mainMenuButtons.append(self.surfWordsButton)
        self.mainMenuButtons.append(self.quitButton)

        for b in self.mainMenuButtons:
            b.setMinimumHeight(50)
            b.setMaximumHeight(50)
            b.setFont(button_font)

        self.mainMenuVLayout.addStretch()
        self.mainMenuVLayout.addWidget(self.mainTitle)
        self.mainMenuVLayout.addStretch()
        for b in self.mainMenuButtons:
            self.mainMenuVLayout.addWidget(b)
        self.mainMenuVLayout.addStretch()

        self.mainMenuHLayout.addStretch()
        self.mainMenuHLayout.addLayout(self.mainMenuVLayout)
        self.mainMenuHLayout.addStretch()

    def createAddWordMenu(self):
        # region Word Typing
        self.wordLabel = QtWidgets.QLabel("Word: ")
        self.wordLabel.setFont(inapp_font)

        self.wordLineEdit = QtWidgets.QLineEdit()
        self.wordLineEdit.setFont(inapp_font)
        self.wordLineEdit.setMinimumWidth(300)
        # endregion

        # region Word Layouts
        self.wordHLayout = QtWidgets.QHBoxLayout()
        self.wordHLayout.addWidget(self.wordLabel)
        self.wordHLayout.addWidget(self.wordLineEdit)

        self.addWordHLayout = QtWidgets.QHBoxLayout()
        self.addWordVLayout = QtWidgets.QVBoxLayout()
        # endregion

        # region Add Choose Image Line
        self.chooseImageButton = QtWidgets.QPushButton("Choose Image")
        self.chooseImageButton.setFont(inapp_font)
        self.chooseImageText = QtWidgets.QLabel("Choose Image...")
        self.chooseImageText.setFont(inapp_font)
        self.currentFilename = ""
        def chooseImage():
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"Image files (*.png *.jpg)")[0]
            self.currentFilename = filename
            if not filename:
                return

            filename.replace('\\','/')
            choseImageStr = filename.split('/')[-1]
            if len(choseImageStr) > 20:
                choseImageStr = "..." + choseImageStr[-17:]
            self.chooseImageText.setText(choseImageStr)
        self.chooseImageButton.clicked.connect(chooseImage)
        # endregion

        # region Choose Image Layout
        self.chooseImageHLayout = QtWidgets.QHBoxLayout()
        self.chooseImageHLayout.addWidget(self.chooseImageButton)
        self.chooseImageHLayout.addWidget(self.chooseImageText)
        # endregion

        # region Add Definitions
        self.definitionsLineEdit = QtWidgets.QLineEdit()
        self.definitionsLineEdit.setPlaceholderText("New Definition")
        self.definitionsLineEdit.setFont(inapp_font)

        self.addDefButton = QtWidgets.QPushButton("Add")
        self.addDefButton.setFont(inapp_font)

        self.removeDefButton = QtWidgets.QPushButton("Remove")
        self.removeDefButton.setFont(inapp_font)

        self.definitionsListWidget = QtWidgets.QListWidget()
        self.definitionsListWidget.setFont(inapp_font)

        def addNewDefinition():
            word = self.definitionsLineEdit.text()
            if not word:
                return
            for i in range(self.definitionsListWidget.count()):
                item = self.definitionsListWidget.item(i)
                if item.text() == word:
                    return
            self.definitionsListWidget.addItem(word)
            self.definitionsLineEdit.clear()

        def removeNewDefinition():
            item = self.definitionsListWidget.currentItem()
            if not item:
                return
            self.definitionsListWidget.takeItem(self.definitionsListWidget.row(item))

        self.addDefButton.clicked.connect(addNewDefinition)
        self.removeDefButton.clicked.connect(removeNewDefinition)
        # endregion

        # region Definition Layouts
        self.definitionsVLayout = QtWidgets.QVBoxLayout()
        self.definitionsVLayout.addStretch()
        self.definitionsVLayout.addWidget(self.definitionsLineEdit)
        self.definitionsVLayout.addWidget(self.addDefButton)
        self.definitionsVLayout.addWidget(self.removeDefButton)
        self.definitionsVLayout.addStretch()

        self.definitionsHLayout = QtWidgets.QHBoxLayout()
        self.definitionsHLayout.addLayout(self.definitionsVLayout)
        self.definitionsHLayout.addWidget(self.definitionsListWidget)
        # endregion

        # region Add Example Sentences
        self.sentencesLineEdit = QtWidgets.QLineEdit()
        self.sentencesLineEdit.setPlaceholderText("New Sentence")
        self.sentencesLineEdit.setFont(inapp_font)

        self.addSentencesButton = QtWidgets.QPushButton("Add")
        self.addSentencesButton.setFont(inapp_font)

        self.removeSentencesButton = QtWidgets.QPushButton("Remove")
        self.removeSentencesButton.setFont(inapp_font)

        self.sentencesListWidget = QtWidgets.QListWidget()
        self.sentencesListWidget.setFont(inapp_font)

        def addNewSentence():
            word = self.sentencesLineEdit.text()
            if not word:
                return
            for i in range(self.sentencesListWidget.count()):
                item = self.sentencesListWidget.item(i)
                if item.text() == word:
                    return
            self.sentencesListWidget.addItem(word)
            self.sentencesLineEdit.clear()
        def removeNewSentence():
            item = self.sentencesListWidget.currentItem()
            if not item:
                return
            self.sentencesListWidget.takeItem(self.sentencesListWidget.row(item))

        self.addSentencesButton.clicked.connect(addNewSentence)
        self.removeSentencesButton.clicked.connect(removeNewSentence)
        # endregion

        # region Example Sentence Layouts
        self.sentencesVLayout = QtWidgets.QVBoxLayout()
        self.sentencesVLayout.addStretch()
        self.sentencesVLayout.addWidget(self.sentencesLineEdit)
        self.sentencesVLayout.addWidget(self.addSentencesButton)
        self.sentencesVLayout.addWidget(self.removeSentencesButton)
        self.sentencesVLayout.addStretch()

        self.sentencesHLayout = QtWidgets.QHBoxLayout()
        self.sentencesHLayout.addLayout(self.sentencesVLayout)
        self.sentencesHLayout.addWidget(self.sentencesListWidget)
        # endregion

        # region Back and Save Buttons
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setFont(inapp_font)

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setFont(inapp_font)
        self.backButton.clicked.connect(lambda: self.switchMenu(Menu.MAIN_MENU))

        def saveWord():
            wordName = self.wordLineEdit.text()
            if not wordName:
                QtWidgets.QMessageBox.warning(self, 'Error', "You have to specify a word name!")
                return

            if wordName in self.wordData.keys():
                QtWidgets.QMessageBox.warning(self, 'Error', "This word already exists!")
                return

            if self.definitionsListWidget.count() == 0:
                QtWidgets.QMessageBox.warning(self, 'Error', "You have to specify at least one definition!")
                return

            definitionsList = []
            for i in range(self.definitionsListWidget.count()):
                item = self.definitionsListWidget.item(i)
                definitionsList.append(item.text())

            sentenceList = []
            for i in range(self.sentencesListWidget.count()):
                item = self.sentencesListWidget.item(i)
                sentenceList.append(item.text())

            w = word.Word(wordName, self.currentFilename, definitionsList, sentenceList)
            self.wordData[wordName] = w.getAsDictionary()
            QtWidgets.QMessageBox.information(self, 'Added a word!', f'You successfully added {wordName} in your dictionary!')
            self.switchMenu(Menu.ADD_WORD)

        self.saveButton.clicked.connect(saveWord)
        # endregion

        # region Back and Save Layout
        self.saveBackHLayout = QtWidgets.QHBoxLayout()
        self.saveBackHLayout.addWidget(self.backButton)
        self.saveBackHLayout.addStretch()
        self.saveBackHLayout.addWidget(self.saveButton)
        # endregion

        # region Main Layouts
        self.addWordVLayout.addStretch()
        self.addWordVLayout.addLayout(self.wordHLayout)
        self.addWordVLayout.addLayout(self.chooseImageHLayout)
        self.addWordVLayout.addStretch()
        self.addWordVLayout.addLayout(self.definitionsHLayout)
        self.addWordVLayout.addStretch()
        self.addWordVLayout.addLayout(self.sentencesHLayout)
        self.addWordVLayout.addStretch()
        self.addWordVLayout.addLayout(self.saveBackHLayout)
        self.addWordVLayout.addStretch()

        self.addWordHLayout.addStretch()
        self.addWordHLayout.addLayout(self.addWordVLayout)
        self.addWordHLayout.addStretch()
        # endregion

    def loadWords(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/words.json"):
            f = open("data/words.json", "w")
            f.write("{}")
            f.close()
        with open("data/words.json") as f:
            self.wordData = json.load(f)

    def saveWords(self):
        with open("data/words.json", 'w') as f:
            json.dump(self.wordData, f)


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    exit_code = app.exec_()
    window.saveWords()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
