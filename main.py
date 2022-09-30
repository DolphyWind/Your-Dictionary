import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import json
from enum import Enum
import random
import word

header_font = QtGui.QFont("OpenSans", 28)
wordTitle_font = QtGui.QFont("OpenSans", 22)
button_font = QtGui.QFont("OpenSans", 16)
text_font = QtGui.QFont("OpenSans", 16)
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

        self.menuList = [Menu.MAIN_MENU]
        self.previousMenu = None
        self.currentMenu = Menu.MAIN_MENU
        self.switchMenu(Menu.MAIN_MENU)

        self.show()

    def modifyWord(self, word: str):
        word = word.lower().strip().capitalize()
        return word

    def switchMenu(self, menu: Menu, wordData: word.Word = None):

        if menu == Menu.PLAY_GAME:
            return

        if menu == Menu.SURF_WORDS:
            if len(self.wordData) == 0:
                QtWidgets.QMessageBox.warning(self, 'Error!', 'You Have to add some words to your dictionary!', QtWidgets.QMessageBox.Ok)
                return

        if menu == self.previousMenu:
            self.menuList.pop(-1)

        if menu != self.menuList[-1]:
            self.menuList.append(menu)
        try:
            self.previousMenu = self.menuList[-2]
        except:
            self.previousMenu = None
        self.currentMenu = self.menuList[-1]

        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)

        if menu == Menu.MAIN_MENU:
            self.createMainMenu()
        elif menu == Menu.ADD_WORD:
            self.createAddWordMenu(wordData)
        elif menu == Menu.SEARCH_WORD:
            self.createSearchWordMenu()
        elif menu == Menu.SURF_WORDS:
            self.createSurfWordsMenu(wordData)
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
        self.addWord_BackButton.clicked.connect(lambda: self.switchMenu(self.previousMenu, preloadedWord))

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

            self.saveWordData()
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

        def openSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()
            selectedWord = word.Word()
            selectedWord.loadFromDict(selectedWordStr, self.wordData[selectedWordStr])

            self.switchMenu(Menu.SURF_WORDS, selectedWord)

        def removeSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()

            reply = QtWidgets.QMessageBox.question(self, "Are you sure?", f"Do you really Want to remove {selectedWordStr} from your dictionary?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.wordData.pop(selectedWordStr)
                self.switchMenu(Menu.SEARCH_WORD)


        self.searchWord_BackButton = QtWidgets.QPushButton("Back")
        self.searchWord_BackButton.setFont(inapp_font)
        self.searchWord_BackButton.clicked.connect(lambda: self.switchMenu(self.previousMenu))

        self.searchWord_EditButton = QtWidgets.QPushButton("Edit selected")
        self.searchWord_EditButton.setFont(inapp_font)
        self.searchWord_EditButton.clicked.connect(editSelected)

        self.searchWord_OpenButton = QtWidgets.QPushButton("Open Selected")
        self.searchWord_OpenButton.setFont(inapp_font)
        self.searchWord_OpenButton.clicked.connect(openSelected)

        self.searchWord_RemoveButton = QtWidgets.QPushButton("Remove Selected")
        self.searchWord_RemoveButton.setFont(inapp_font)
        self.searchWord_RemoveButton.clicked.connect(removeSelected)

        self.searchWord_ButtonHLayout = QtWidgets.QHBoxLayout()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_BackButton)
        self.searchWord_ButtonHLayout.addStretch()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_EditButton)
        self.searchWord_ButtonHLayout.addStretch()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_OpenButton)
        self.searchWord_ButtonHLayout.addStretch()
        self.searchWord_ButtonHLayout.addWidget(self.searchWord_RemoveButton)

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

    def createSurfWordsMenu(self, currentWord:word.Word = None):

        # region Initialize
        if currentWord is None:
            currentWord = word.Word()
            keys_list = list(self.wordData.keys())
            randomWord = keys_list[0]
            currentWord.loadFromDict(randomWord, self.wordData[randomWord])

        index = 0
        for i in range(len(self.wordData.keys())):
            if list(self.wordData.keys())[i] == currentWord.word:
                index = i
        # endregion

        # region Image and Title
        self.surfWords_ImageLabel = None

        if currentWord.imageExists:
            self.surfWords_ImageLabel = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(currentWord.imagePath)
            ratio = pixmap.width() / pixmap.height()
            max_wh = 128

            new_width, new_height = 0, 0
            if ratio > 1:
                new_width = max_wh
                new_height = int(max_wh / ratio)
            else:
                new_width = int(max_wh * ratio)
                new_height = max_wh

            pixmap = pixmap.scaledToWidth(new_width, QtCore.Qt.SmoothTransformation)
            pixmap = pixmap.scaledToHeight(new_height, QtCore.Qt.SmoothTransformation)

            self.surfWords_ImageLabel.setPixmap(pixmap)

        self.surfWords_TitleLabel = QtWidgets.QLabel(currentWord.word)
        self.surfWords_TitleLabel.setFont(wordTitle_font)

        self.surfWords_TitleHLayout = QtWidgets.QHBoxLayout()
        self.surfWords_TitleHLayout.addStretch()
        if self.surfWords_ImageLabel is not None:
            self.surfWords_TitleHLayout.addWidget(self.surfWords_ImageLabel)
        self.surfWords_TitleHLayout.addWidget(self.surfWords_TitleLabel)
        self.surfWords_TitleHLayout.addStretch()
        # endregion

        # region Definitions
        self.surfWords_DefinitionsLabel = QtWidgets.QLabel("Definitions")
        self.surfWords_DefinitionsLabel.setStyleSheet("color: #5c5a5a")
        self.surfWords_DefinitionsLabel.setFont(text_font)

        self.surfWords_DefinitionsScrollArea = QtWidgets.QScrollArea()
        self.surfWords_DefinitionsScrollArea.setMaximumHeight(200)
        self.surfWords_DefinitionsScrollArea.setMinimumWidth(500)
        self.surfWords_DefinitionsCenteral = QtWidgets.QWidget()
        self.surfWords_DefinitionsScrollAreaVLayout = QtWidgets.QVBoxLayout()

        for i, d in enumerate(currentWord.definitions):
            lbl = QtWidgets.QLabel(f'{i + 1}. {d}')
            lbl.setFont(text_font)
            self.surfWords_DefinitionsScrollAreaVLayout.addWidget(lbl)

        self.surfWords_DefinitionsCenteral.setLayout(self.surfWords_DefinitionsScrollAreaVLayout)
        self.surfWords_DefinitionsScrollArea.setWidget(self.surfWords_DefinitionsCenteral)

        self.surfWords_DefinitionsVLayout = QtWidgets.QVBoxLayout()
        self.surfWords_DefinitionsVLayout.addWidget(self.surfWords_DefinitionsLabel)
        self.surfWords_DefinitionsVLayout.addWidget(self.surfWords_DefinitionsScrollArea)

        # endregion

        # region Example Sentences
        self.surfWords_SentencesLabel = QtWidgets.QLabel("Example Sentences")
        self.surfWords_SentencesLabel.setStyleSheet("color: #5c5a5a")
        self.surfWords_SentencesLabel.setFont(text_font)

        self.surfWords_SentencesScrollArea = QtWidgets.QScrollArea()
        self.surfWords_SentencesScrollArea.setMaximumHeight(150)
        self.surfWords_SentencesScrollArea.setMinimumWidth(500)

        self.surfWords_SentencesCenteral = QtWidgets.QWidget()
        self.surfWords_SentencesScrollAreaVLayout = QtWidgets.QVBoxLayout()

        for i, es in enumerate(currentWord.exampleSentences):
            lbl = QtWidgets.QLabel(f'{i + 1}. {es}')
            lbl.setFont(text_font)
            self.surfWords_SentencesScrollAreaVLayout.addWidget(lbl)

        self.surfWords_SentencesCenteral.setLayout(self.surfWords_SentencesScrollAreaVLayout)
        self.surfWords_SentencesScrollArea.setWidget(self.surfWords_SentencesCenteral)

        self.surfWords_SentencesVLayout = QtWidgets.QVBoxLayout()
        self.surfWords_SentencesVLayout.addWidget(self.surfWords_SentencesLabel)
        self.surfWords_SentencesVLayout.addWidget(self.surfWords_SentencesScrollArea)

        self.emptyObject = QtWidgets.QWidget()
        self.emptyObject.setMinimumHeight(self.surfWords_SentencesScrollArea.height())
        self.emptyObject.setMaximumHeight(150)
        self.emptyObject.setMinimumWidth(500)

        # endregion

        # region Buttons

        def changeWord(index, step):
            index += step
            if index < 0:
                index = len(self.wordData.keys()) - 1
            elif index > len(self.wordData.keys()) - 1:
                index = 0
            key_list = list(self.wordData.keys())
            currentStr = key_list[index]
            currentWord.loadFromDict(currentStr, self.wordData[currentStr])
            self.switchMenu(Menu.SURF_WORDS, currentWord)

        def getRandomWord():
            new_word = word.Word()
            keys_list = list(self.wordData.keys())
            if len(keys_list) <= 1:
                return
            randomWord = random.choice(keys_list)
            while randomWord == currentWord.word:
                randomWord = random.choice(keys_list)
            new_word.loadFromDict(randomWord, self.wordData[randomWord])
            self.switchMenu(self.currentMenu, new_word)

        def removeSelected():
            selectedWordStr = currentWord.word

            reply = QtWidgets.QMessageBox.question(self, "Are you sure?", f"Do you really Want to remove {selectedWordStr} from your dictionary?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.wordData.pop(selectedWordStr)
                self.switchMenu(self.previousMenu)

        button_width = 120

        self.surfWords_PreviousButton = QtWidgets.QPushButton("<< Previous")
        self.surfWords_PreviousButton.setFont(inapp_font)
        self.surfWords_PreviousButton.setMinimumWidth(button_width)
        self.surfWords_PreviousButton.clicked.connect(lambda: changeWord(index, -1))

        self.surfWords_NextButton = QtWidgets.QPushButton("Next >>")
        self.surfWords_NextButton.setFont(inapp_font)
        self.surfWords_NextButton.setMinimumWidth(button_width)
        self.surfWords_NextButton.clicked.connect(lambda: changeWord(index, 1))

        self.surfWords_BackButton = QtWidgets.QPushButton("Back")
        self.surfWords_BackButton.setFont(inapp_font)
        self.surfWords_BackButton.setMinimumWidth(button_width)
        self.surfWords_BackButton.clicked.connect(lambda: self.switchMenu(self.previousMenu, currentWord))

        self.surfWords_GetRandomButton = QtWidgets.QPushButton("Get Random")
        self.surfWords_GetRandomButton.setFont(inapp_font)
        self.surfWords_GetRandomButton.setMinimumWidth(button_width)
        self.surfWords_GetRandomButton.clicked.connect(getRandomWord)

        self.surfWords_FirstVLayout = QtWidgets.QVBoxLayout()
        self.surfWords_FirstVLayout.addWidget(self.surfWords_GetRandomButton)
        self.surfWords_FirstVLayout.addWidget(self.surfWords_BackButton)

        self.surfWords_EditButton = QtWidgets.QPushButton("Edit")
        self.surfWords_EditButton.setFont(inapp_font)
        self.surfWords_EditButton.setMinimumWidth(button_width)
        self.surfWords_EditButton.clicked.connect(lambda: self.switchMenu(Menu.ADD_WORD, currentWord))

        self.surfWords_RemoveButton = QtWidgets.QPushButton("Remove")
        self.surfWords_RemoveButton.setFont(inapp_font)
        self.surfWords_RemoveButton.setMinimumWidth(button_width)
        self.surfWords_RemoveButton.clicked.connect(removeSelected)

        self.surfWords_SecondVLayout = QtWidgets.QVBoxLayout()
        self.surfWords_SecondVLayout.addWidget(self.surfWords_EditButton)
        self.surfWords_SecondVLayout.addWidget(self.surfWords_RemoveButton)

        self.surfWords_ButtonHLayout = QtWidgets.QHBoxLayout()
        self.surfWords_ButtonHLayout.addStretch()
        self.surfWords_ButtonHLayout.addWidget(self.surfWords_PreviousButton)
        self.surfWords_ButtonHLayout.addStretch()
        self.surfWords_ButtonHLayout.addLayout(self.surfWords_FirstVLayout)
        self.surfWords_ButtonHLayout.addStretch()
        self.surfWords_ButtonHLayout.addLayout(self.surfWords_SecondVLayout)
        self.surfWords_ButtonHLayout.addStretch()
        self.surfWords_ButtonHLayout.addWidget(self.surfWords_NextButton)
        self.surfWords_ButtonHLayout.addStretch()

        # endregion

        # region Main Layouts
        self.surfWords_MainVLayout = QtWidgets.QVBoxLayout()

        self.surfWords_MainVLayout.addStretch()
        self.surfWords_MainVLayout.addLayout(self.surfWords_TitleHLayout)
        self.surfWords_MainVLayout.addStretch()
        self.surfWords_MainVLayout.addLayout(self.surfWords_DefinitionsVLayout)
        if len(currentWord.exampleSentences) != 0:
            self.surfWords_MainVLayout.addStretch()
            self.surfWords_MainVLayout.addLayout(self.surfWords_SentencesVLayout)
        else:
            self.surfWords_MainVLayout.addStretch()
            self.surfWords_MainVLayout.addWidget(self.emptyObject)
        self.surfWords_MainVLayout.addStretch()
        self.surfWords_MainVLayout.addLayout(self.surfWords_ButtonHLayout)
        self.surfWords_MainVLayout.addStretch()

        self.surfWords_MainHLayout = QtWidgets.QHBoxLayout()
        self.surfWords_MainHLayout.addStretch()
        self.surfWords_MainHLayout.addLayout(self.surfWords_MainVLayout)
        self.surfWords_MainHLayout.addStretch()

        self.central.setLayout(self.surfWords_MainHLayout)
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

    def saveWordData(self):
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
    window.saveWordData()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
