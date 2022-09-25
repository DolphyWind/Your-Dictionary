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
    SURF_WORDS = 5

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

        self.previousMenu = Menu.MAIN_MENU
        self.currentMenu = Menu.MAIN_MENU
        self.switchMenu(Menu.MAIN_MENU)

        self.show()

    def modifyWord(self, word: str):
        word = word.lower().strip().capitalize()
        return word

    def switchMenu(self, menu: Menu, wordData: word.Word = None):
        if menu != self.currentMenu:
            self.previousMenu = self.currentMenu
            self.currentMenu = menu

        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)

        if menu == Menu.MAIN_MENU:
            self.createMainMenu()
        elif menu == Menu.ADD_WORD:
            self.createAddWordMenu(wordData)
        elif menu == Menu.SEARCH_WORD:
            self.createSearchWordMenu()
        else:
            self.central.setLayout(self.mainMenu_HLayout)

    def createMainMenu(self):
        # region Title
        self.mainMenu_Title = QtWidgets.QLabel("Your Dictionary")
        self.mainMenu_Title.setFont(header_font)
        self.mainMenu_Title.setAlignment(QtCore.Qt.AlignCenter)
        # endregion

        # region Buttons
        self.mainMenu_AddAWordButton = QtWidgets.QPushButton("Add Word")
        self.mainMenu_AddAWordButton.clicked.connect(lambda: self.switchMenu(Menu.ADD_WORD))

        self.mainMenu_SearchWordButton = QtWidgets.QPushButton("Search Word")
        self.mainMenu_SearchWordButton.clicked.connect(lambda: self.switchMenu(Menu.SEARCH_WORD))

        self.mainMenu_GameButton = QtWidgets.QPushButton("Word Game")
        self.mainMenu_GameButton.clicked.connect(lambda: self.switchMenu(Menu.PLAY_GAME))

        self.mainMenu_SurfWordsButton = QtWidgets.QPushButton("Surf Words")
        self.mainMenu_SurfWordsButton.clicked.connect(lambda: self.switchMenu(Menu.SURF_WORDS))

        self.mainMenu_QuitButton = QtWidgets.QPushButton("Quit Application")
        self.mainMenu_QuitButton.clicked.connect(self.close)
        # endregion

        # region Layouts
        self.mainMenu_HLayout = QtWidgets.QHBoxLayout()
        self.mainMenu_VLayout = QtWidgets.QVBoxLayout()

        self.mainMenuButtons = []
        self.mainMenuButtons.append(self.mainMenu_AddAWordButton)
        self.mainMenuButtons.append(self.mainMenu_SearchWordButton)
        self.mainMenuButtons.append(self.mainMenu_SurfWordsButton)
        self.mainMenuButtons.append(self.mainMenu_GameButton)
        self.mainMenuButtons.append(self.mainMenu_QuitButton)

        for b in self.mainMenuButtons:
            b.setMinimumHeight(50)
            b.setMaximumHeight(50)
            b.setFont(button_font)

        self.mainMenu_VLayout.addStretch()
        self.mainMenu_VLayout.addWidget(self.mainMenu_Title)
        self.mainMenu_VLayout.addStretch()
        for b in self.mainMenuButtons:
            self.mainMenu_VLayout.addWidget(b)
        self.mainMenu_VLayout.addStretch()

        self.mainMenu_HLayout.addStretch()
        self.mainMenu_HLayout.addLayout(self.mainMenu_VLayout)
        self.mainMenu_HLayout.addStretch()

        self.central.setLayout(self.mainMenu_HLayout)
        # endregion

    def createAddWordMenu(self, preloadedWord:word.Word = None):
        # region Word Typing
        self.addWord_WordLabel = QtWidgets.QLabel("Word: ")
        self.addWord_WordLabel.setFont(inapp_font)

        self.addWord_WordLineEdit = QtWidgets.QLineEdit()
        self.addWord_WordLineEdit.setFont(inapp_font)
        self.addWord_WordLineEdit.setMinimumWidth(300)
        # endregion

        # region Word Layouts
        self.addWord_WordHLayout = QtWidgets.QHBoxLayout()
        self.addWord_WordHLayout.addWidget(self.addWord_WordLabel)
        self.addWord_WordHLayout.addWidget(self.addWord_WordLineEdit)
        # endregion

        # region Add Choose Image Line
        self.addWord_ChooseImageButton = QtWidgets.QPushButton("Choose Image")
        self.addWord_ChooseImageButton.setFont(inapp_font)
        self.addWord_ChooseImageText = QtWidgets.QLabel("Choose Image...")
        self.addWord_ChooseImageText.setFont(inapp_font)
        self.currentFilename = ""

        def formatFilename(filename):
            filename.replace('\\', '/')
            chooseImageStr = filename.split('/')[-1]
            if len(chooseImageStr) > 20:
                chooseImageStr = "..." + chooseImageStr[-17:]
            return chooseImageStr

        def chooseImage():
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"Image files (*.png *.jpg)")[0]
            if not filename:
                return
            self.currentFilename = filename

            chooseImageStr = formatFilename(filename)
            self.addWord_ChooseImageText.setText(chooseImageStr)

        self.addWord_ChooseImageButton.clicked.connect(chooseImage)
        # endregion

        # region Choose Image Layout
        self.addWord_ChooseImageHLayout = QtWidgets.QHBoxLayout()
        self.addWord_ChooseImageHLayout.addWidget(self.addWord_ChooseImageButton)
        self.addWord_ChooseImageHLayout.addWidget(self.addWord_ChooseImageText)
        # endregion

        # region Add Definitions
        self.addWord_DefinitionsLineEdit = QtWidgets.QLineEdit()
        self.addWord_DefinitionsLineEdit.setPlaceholderText("New Definition")
        self.addWord_DefinitionsLineEdit.setFont(inapp_font)

        self.addWord_AddDefButton = QtWidgets.QPushButton("Add")
        self.addWord_AddDefButton.setFont(inapp_font)

        self.addWord_RemoveDefButton = QtWidgets.QPushButton("Remove")
        self.addWord_RemoveDefButton.setFont(inapp_font)

        self.addWord_DefinitionsListWidget = QtWidgets.QListWidget()
        self.addWord_DefinitionsListWidget.setFont(inapp_font)

        def addNewDefinition():
            word = self.addWord_DefinitionsLineEdit.text()

            if not word:
                return
            for i in range(self.addWord_DefinitionsListWidget.count()):
                item = self.addWord_DefinitionsListWidget.item(i)
                if item.text() == word:
                    return
            self.addWord_DefinitionsListWidget.addItem(word)
            self.addWord_DefinitionsLineEdit.clear()

        def removeNewDefinition():
            item = self.addWord_DefinitionsListWidget.currentItem()
            if not item:
                return
            self.addWord_DefinitionsListWidget.takeItem(self.addWord_DefinitionsListWidget.row(item))

        self.addWord_AddDefButton.clicked.connect(addNewDefinition)
        self.addWord_RemoveDefButton.clicked.connect(removeNewDefinition)
        # endregion

        # region Definition Layouts
        self.addWord_DefinitionsVLayout = QtWidgets.QVBoxLayout()
        self.addWord_DefinitionsVLayout.addStretch()
        self.addWord_DefinitionsVLayout.addWidget(self.addWord_DefinitionsLineEdit)
        self.addWord_DefinitionsVLayout.addWidget(self.addWord_AddDefButton)
        self.addWord_DefinitionsVLayout.addWidget(self.addWord_RemoveDefButton)
        self.addWord_DefinitionsVLayout.addStretch()

        self.addWord_DefinitionsHLayout = QtWidgets.QHBoxLayout()
        self.addWord_DefinitionsHLayout.addLayout(self.addWord_DefinitionsVLayout)
        self.addWord_DefinitionsHLayout.addWidget(self.addWord_DefinitionsListWidget)
        # endregion

        # region Add Example Sentences
        self.addWord_SentencesLineEdit = QtWidgets.QLineEdit()
        self.addWord_SentencesLineEdit.setPlaceholderText("New Sentence")
        self.addWord_SentencesLineEdit.setFont(inapp_font)

        self.addWord_AddSentencesButton = QtWidgets.QPushButton("Add")
        self.addWord_AddSentencesButton.setFont(inapp_font)

        self.addWord_RemoveSentencesButton = QtWidgets.QPushButton("Remove")
        self.addWord_RemoveSentencesButton.setFont(inapp_font)

        self.addWord_SentencesListWidget = QtWidgets.QListWidget()
        self.addWord_SentencesListWidget.setFont(inapp_font)

        def addNewSentence():
            word = self.addWord_SentencesLineEdit.text()

            if not word:
                return
            for i in range(self.addWord_SentencesListWidget.count()):
                item = self.addWord_SentencesListWidget.item(i)
                if item.text() == word:
                    return
            self.addWord_SentencesListWidget.addItem(word)
            self.addWord_SentencesLineEdit.clear()
        def removeNewSentence():
            item = self.addWord_SentencesListWidget.currentItem()
            if not item:
                return
            self.addWord_SentencesListWidget.takeItem(self.addWord_SentencesListWidget.row(item))

        self.addWord_AddSentencesButton.clicked.connect(addNewSentence)
        self.addWord_RemoveSentencesButton.clicked.connect(removeNewSentence)
        # endregion

        # region Check if has pre loaded word
        if preloadedWord is not None:
            self.addWord_WordLineEdit.setText(preloadedWord.word)
            self.addWord_WordLineEdit.setDisabled(True)

            if preloadedWord.imageExists:
                self.currentFilename = preloadedWord.imagePath
                self.addWord_ChooseImageText.setText(formatFilename(self.currentFilename))

            for d in preloadedWord.definitions:
                self.addWord_DefinitionsListWidget.addItem(QtWidgets.QListWidgetItem(d))
            for es in preloadedWord.exampleSentences:
                self.addWord_SentencesListWidget.addItem(QtWidgets.QListWidgetItem(es))

        # endregion

        # region Example Sentence Layouts
        self.addWord_SentencesVLayout = QtWidgets.QVBoxLayout()
        self.addWord_SentencesVLayout.addStretch()
        self.addWord_SentencesVLayout.addWidget(self.addWord_SentencesLineEdit)
        self.addWord_SentencesVLayout.addWidget(self.addWord_AddSentencesButton)
        self.addWord_SentencesVLayout.addWidget(self.addWord_RemoveSentencesButton)
        self.addWord_SentencesVLayout.addStretch()

        self.addWord_SentencesHLayout = QtWidgets.QHBoxLayout()
        self.addWord_SentencesHLayout.addLayout(self.addWord_SentencesVLayout)
        self.addWord_SentencesHLayout.addWidget(self.addWord_SentencesListWidget)
        # endregion

        # region Back and Save Buttons
        self.addWord_SaveButton = QtWidgets.QPushButton("Save")
        self.addWord_SaveButton.setFont(inapp_font)

        self.addWord_BackButton = QtWidgets.QPushButton("Back")
        self.addWord_BackButton.setFont(inapp_font)
        self.addWord_BackButton.clicked.connect(lambda: self.switchMenu(self.previousMenu))

        def addWord():
            wordName = self.addWord_WordLineEdit.text()
            wordName = self.modifyWord(wordName)
            if not wordName:
                QtWidgets.QMessageBox.warning(self, 'Error', "You have to specify a word name!")
                return

            if self.addWord_DefinitionsListWidget.count() == 0:
                QtWidgets.QMessageBox.warning(self, 'Error', "You have to specify at least one definition!")
                return

            definitionsList = []
            for i in range(self.addWord_DefinitionsListWidget.count()):
                item = self.addWord_DefinitionsListWidget.item(i)
                definitionsList.append(item.text())

            sentenceList = []
            for i in range(self.addWord_SentencesListWidget.count()):
                item = self.addWord_SentencesListWidget.item(i)
                sentenceList.append(item.text())

            if wordName in self.wordData.keys():
                QtWidgets.QMessageBox.information(self, 'Updated a word!', f"Successfully updated {wordName}!")
            else:
                QtWidgets.QMessageBox.information(self, 'Added a word!', f'You successfully added {wordName} to your dictionary!')

            w = word.Word(wordName, self.currentFilename, definitionsList, sentenceList)
            self.wordData[wordName] = w.getAsDictionary()

            self.saveWords()
            self.switchMenu(Menu.ADD_WORD)

        self.addWord_SaveButton.clicked.connect(addWord)
        # endregion

        # region Back and Save Layout
        self.addWord_SaveBackHLayout = QtWidgets.QHBoxLayout()
        self.addWord_SaveBackHLayout.addWidget(self.addWord_BackButton)
        self.addWord_SaveBackHLayout.addStretch()
        self.addWord_SaveBackHLayout.addWidget(self.addWord_SaveButton)
        # endregion

        # region Main Layouts
        self.addWord_HLayout = QtWidgets.QHBoxLayout()
        self.addWord_VLayout = QtWidgets.QVBoxLayout()

        self.addWord_VLayout.addStretch()
        self.addWord_VLayout.addLayout(self.addWord_WordHLayout)
        self.addWord_VLayout.addLayout(self.addWord_ChooseImageHLayout)
        self.addWord_VLayout.addStretch()
        self.addWord_VLayout.addLayout(self.addWord_DefinitionsHLayout)
        self.addWord_VLayout.addStretch()
        self.addWord_VLayout.addLayout(self.addWord_SentencesHLayout)
        self.addWord_VLayout.addStretch()
        self.addWord_VLayout.addLayout(self.addWord_SaveBackHLayout)
        self.addWord_VLayout.addStretch()

        self.addWord_HLayout.addStretch()
        self.addWord_HLayout.addLayout(self.addWord_VLayout)
        self.addWord_HLayout.addStretch()

        self.central.setLayout(self.addWord_HLayout)
        # endregion

    def createSearchWordMenu(self):
        # region Line Edit and List Widget
        def updateListWidget(word: str):
            self.searchWord_ListWidget.clear()

            searched = self.modifyWord(word)

            for w in self.wordData.keys():
                if w.startswith(searched):
                    self.searchWord_ListWidget.addItem(QtWidgets.QListWidgetItem(w))

        self.searchWord_LineEdit = QtWidgets.QLineEdit()
        self.searchWord_LineEdit.setPlaceholderText("Search Words...")
        self.searchWord_LineEdit.setFont(inapp_font)
        self.searchWord_LineEdit.setMinimumWidth(400)
        self.searchWord_LineEdit.textChanged.connect(lambda: updateListWidget(self.searchWord_LineEdit.text()))

        self.searchWord_ListWidget = QtWidgets.QListWidget()
        self.searchWord_ListWidget.setFont(inapp_font)
        self.searchWord_ListWidget.setMinimumHeight(400)

        updateListWidget('')
        # endregion

        # region Back, Edit and Open buttons and layouts

        def editSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()
            selectedWord = word.Word()
            selectedWord.loadFromDict(selectedWordStr, self.wordData[selectedWordStr])

            self.switchMenu(Menu.ADD_WORD, selectedWord)

        self.searchWord_BackButton = QtWidgets.QPushButton("Back")
        self.searchWord_BackButton.setFont(inapp_font)
        self.searchWord_BackButton.clicked.connect(lambda: self.switchMenu(Menu.MAIN_MENU))

        self.searchWord_EditButton = QtWidgets.QPushButton("Edit selected")
        self.searchWord_EditButton.setFont(inapp_font)
        self.searchWord_EditButton.clicked.connect(editSelected)

        self.searchWord_OpenButton = QtWidgets.QPushButton("Open Selected")
        self.searchWord_OpenButton.setFont(inapp_font)

        self.searchWord_ButtonHLayout = QtWidgets.QHBoxLayout()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_BackButton)
        self.searchWord_ButtonHLayout.addStretch()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_EditButton)
        self.searchWord_ButtonHLayout.addStretch()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_OpenButton)

        # endregion

        # region Main Layouts
        self.searchWord_MainVLayout = QtWidgets.QVBoxLayout()

        self.searchWord_MainVLayout.addStretch()
        self.searchWord_MainVLayout.addWidget(self.searchWord_LineEdit)
        self.searchWord_MainVLayout.addWidget(self.searchWord_ListWidget)
        self.searchWord_MainVLayout.addStretch()
        self.searchWord_MainVLayout.addLayout(self.searchWord_ButtonHLayout)
        self.searchWord_MainVLayout.addStretch()

        self.searchWord_MainHLayout = QtWidgets.QHBoxLayout()

        self.searchWord_MainHLayout.addStretch()
        self.searchWord_MainHLayout.addLayout(self.searchWord_MainVLayout)
        self.searchWord_MainHLayout.addStretch()

        self.central.setLayout(self.searchWord_MainHLayout)
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
