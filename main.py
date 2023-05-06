import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import json
from enum import Enum
import random
import word
import time

header_font = QtGui.QFont("OpenSans", 28)
wordTitle_font = QtGui.QFont("OpenSans", 22)
button_font = QtGui.QFont("OpenSans", 16)
text_font = QtGui.QFont("OpenSans", 16)
inapp_font = QtGui.QFont("OpenSans", 12)

class Global:
    GAME_PROMPT_KEY = 'prompt_game_howtoplay'
    HIGHSCORE_KEY = 'highscore'

class Menu(Enum):
    MAIN_MENU = 1
    ADD_WORD = 2
    SEARCH_WORD = 3
    PLAY_GAME = 4
    SURF_WORDS = 5

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.wordDataDict = dict()
        self.appdataDict = {
            Global.GAME_PROMPT_KEY: True,
            Global.HIGHSCORE_KEY: 0,
        }
        self.loadWords()
        self.loadAppdata()
        
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.appVersion = 'v1.7'

        self.windowSize = (600, 800)
        self.setWindowTitle(f"Your Dictionary {self.appVersion}")
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
            if self.appdataDict[Global.GAME_PROMPT_KEY]:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msgBox.setWindowTitle("How word game works?")
                msgBox.setText("On each round, game will pick a random word. In order to gain points, you have to choose the definition of that word among four choices. Right answer gives you four points. Wrong answer takes one of your points. When the game ends, your score will get multiplied by how many words you saved to better indicate how well you know these words. Good luck!")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                
                cb = QtWidgets.QCheckBox("Do not show again")
                msgBox.setCheckBox(cb)
                
                msgBox.exec()
                self.appdataDict[Global.GAME_PROMPT_KEY] = not cb.isChecked()
                
        if menu == Menu.SURF_WORDS:
            if len(self.wordDataDict) == 0:
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
            self.createSearchWordMenu(wordData)
        elif menu == Menu.SURF_WORDS:
            self.createSurfWordsMenu(wordData)
        elif menu == Menu.PLAY_GAME:
            self.createPlayGameMenu()
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
        self.addWord_WordLineEdit = QtWidgets.QLineEdit()
        self.addWord_WordLineEdit.setFont(inapp_font)
        self.addWord_WordLineEdit.setMinimumWidth(300)
        self.addWord_WordLineEdit.setPlaceholderText("New Word")
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

        # region Manipulating List Widgets

        def addToListWidget(lWidget, wordName, textBox):
            word = wordName
            word = self.modifyWord(word)
            if not word:
                return
            for i in range(lWidget.count()):
                item = lWidget.item(i)
                if item.text() == word:
                    return
            lWidget.addItem(word)
            textBox.clear()

        def removeFromListWidget(lWidget):
            item = lWidget.currentItem()
            if not item:
                return
            lWidget.takeItem(lWidget.row(item))

        def moveSelectedToUp(lWidget):
            items = lWidget.selectedIndexes()

            if not items or items[0].row() == 0:
                return
            index = items[0].row()
            item = lWidget.takeItem(index)
            lWidget.insertItem(index - 1, item)
            lWidget.setCurrentRow(index - 1)

        def moveSelectedToDown(lWidget):
            items = lWidget.selectedIndexes()

            if not items or items[0].row() == lWidget.count() - 1:
                return
            index = items[0].row()
            item = lWidget.takeItem(index)
            lWidget.insertItem(index + 1, item)
            lWidget.setCurrentRow(index + 1)


        # endregion

        # region Add Definitions
        self.addWord_DefinitionsLineEdit = QtWidgets.QLineEdit()
        self.addWord_DefinitionsLineEdit.setPlaceholderText("New Definition")
        self.addWord_DefinitionsLineEdit.setFont(inapp_font)
        self.addWord_DefinitionsLineEdit.setMaximumWidth(175)

        self.addWord_DefinitionsListWidget = QtWidgets.QListWidget()
        self.addWord_DefinitionsListWidget.setFont(inapp_font)

        self.addWord_AddDefButton = QtWidgets.QPushButton("Add")
        self.addWord_AddDefButton.setFont(inapp_font)
        self.addWord_AddDefButton.clicked.connect(
            lambda: addToListWidget(self.addWord_DefinitionsListWidget, self.addWord_DefinitionsLineEdit.text(), self.addWord_DefinitionsLineEdit)
        )

        self.addWord_RemoveDefButton = QtWidgets.QPushButton("Remove")
        self.addWord_RemoveDefButton.setFont(inapp_font)
        self.addWord_RemoveDefButton.clicked.connect(lambda: removeFromListWidget(self.addWord_DefinitionsListWidget))

        self.addWord_UpDefButton = QtWidgets.QPushButton("Up")
        self.addWord_UpDefButton.setFont(inapp_font)
        self.addWord_UpDefButton.clicked.connect(lambda: moveSelectedToUp(self.addWord_DefinitionsListWidget))

        self.addWord_DownDefButton = QtWidgets.QPushButton("Down")
        self.addWord_DownDefButton.setFont(inapp_font)
        self.addWord_DownDefButton.clicked.connect(lambda: moveSelectedToDown(self.addWord_DefinitionsListWidget))

        # endregion

        # region Definition Layouts

        self.addWord_AddRemoveDefHLayout = QtWidgets.QHBoxLayout()
        self.addWord_AddRemoveDefHLayout.addWidget(self.addWord_AddDefButton)
        self.addWord_AddRemoveDefHLayout.addWidget(self.addWord_RemoveDefButton)

        self.addWord_UpDownDefHLayout = QtWidgets.QHBoxLayout()
        self.addWord_UpDownDefHLayout.addWidget(self.addWord_UpDefButton)
        self.addWord_UpDownDefHLayout.addWidget(self.addWord_DownDefButton)

        self.addWord_DefinitionsVLayout = QtWidgets.QVBoxLayout()
        self.addWord_DefinitionsVLayout.addStretch()
        self.addWord_DefinitionsVLayout.addWidget(self.addWord_DefinitionsLineEdit)
        self.addWord_DefinitionsVLayout.addLayout(self.addWord_AddRemoveDefHLayout)
        self.addWord_DefinitionsVLayout.addLayout(self.addWord_UpDownDefHLayout)
        self.addWord_DefinitionsVLayout.addStretch()

        self.addWord_DefinitionsHLayout = QtWidgets.QHBoxLayout()
        self.addWord_DefinitionsHLayout.addLayout(self.addWord_DefinitionsVLayout)
        self.addWord_DefinitionsHLayout.addWidget(self.addWord_DefinitionsListWidget)
        # endregion

        # region Add Example Sentences
        self.addWord_SentencesTextEdit = QtWidgets.QTextEdit()
        self.addWord_SentencesTextEdit.setPlaceholderText("New Sentence")
        self.addWord_SentencesTextEdit.setFont(inapp_font)
        self.addWord_SentencesTextEdit.setMaximumWidth(175)
        self.addWord_SentencesTextEdit.setMaximumHeight(80)
        self.addWord_SentencesTextEdit.setMinimumHeight(80)

        self.addWord_SentencesListWidget = QtWidgets.QListWidget()
        self.addWord_SentencesListWidget.setFont(inapp_font)

        self.addWord_AddSentencesButton = QtWidgets.QPushButton("Add")
        self.addWord_AddSentencesButton.setFont(inapp_font)
        self.addWord_AddSentencesButton.clicked.connect(
            lambda: addToListWidget(self.addWord_SentencesListWidget, self.addWord_SentencesTextEdit.toPlainText(), self.addWord_SentencesTextEdit)
        )

        self.addWord_RemoveSentencesButton = QtWidgets.QPushButton("Remove")
        self.addWord_RemoveSentencesButton.setFont(inapp_font)
        self.addWord_RemoveSentencesButton.clicked.connect(lambda: removeFromListWidget(self.addWord_SentencesListWidget))

        self.addWord_UpSentenceButton = QtWidgets.QPushButton("Up")
        self.addWord_UpSentenceButton.setFont(inapp_font)
        self.addWord_UpSentenceButton.clicked.connect(lambda: moveSelectedToUp(self.addWord_SentencesListWidget))

        self.addWord_DownSentenceButton = QtWidgets.QPushButton("Down")
        self.addWord_DownSentenceButton.setFont(inapp_font)
        self.addWord_DownSentenceButton.clicked.connect(lambda: moveSelectedToDown(self.addWord_SentencesListWidget))

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

        self.addWord_AddRemoveSentencesHLayout = QtWidgets.QHBoxLayout()
        self.addWord_AddRemoveSentencesHLayout.addWidget(self.addWord_AddSentencesButton)
        self.addWord_AddRemoveSentencesHLayout.addWidget(self.addWord_RemoveSentencesButton)

        self.addWord_UpDownSentencesHLayout = QtWidgets.QHBoxLayout()
        self.addWord_UpDownSentencesHLayout.addWidget(self.addWord_UpSentenceButton)
        self.addWord_UpDownSentencesHLayout.addWidget(self.addWord_DownSentenceButton)

        self.addWord_SentencesVLayout = QtWidgets.QVBoxLayout()
        self.addWord_SentencesVLayout.addStretch()
        self.addWord_SentencesVLayout.addWidget(self.addWord_SentencesTextEdit)
        self.addWord_SentencesVLayout.addLayout(self.addWord_AddRemoveSentencesHLayout)
        self.addWord_SentencesVLayout.addLayout(self.addWord_UpDownSentencesHLayout)
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

            if wordName in self.wordDataDict.keys():
                if preloadedWord is None:
                    mbox = QtWidgets.QMessageBox.question(self, 'Are you sure?', f'This word already exists. Do you want to update it?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
                    if mbox == QtWidgets.QMessageBox.No:
                        return

                QtWidgets.QMessageBox.information(self, 'Updated a word!', f'Successfully updated "{wordName}"!')
            else:
                QtWidgets.QMessageBox.information(self, 'Added a word!', f'You successfully added {wordName} to your dictionary!')

            w = word.Word(wordName, self.currentFilename, definitionsList, sentenceList)
            self.wordDataDict[wordName] = w.getAsDictionary()

            self.saveWordData()
            if preloadedWord is None:
                self.switchMenu(self.currentMenu)
            else:
                self.switchMenu(self.previousMenu, w)

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
        self.addWord_VLayout.addWidget(self.addWord_WordLineEdit)
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

    def createSearchWordMenu(self, selectedWord:word.Word = None):
        # region Line Edit and List Widget
        def updateListWidget(word: str):
            self.searchWord_ListWidget.clear()

            searched = self.modifyWord(word)
            searched = searched.lower()

            matchedWordsStartsWith = []
            matchedWordsIncludes = []

            for w in self.wordDataDict.keys():
                if w.lower().startswith(searched):
                    matchedWordsStartsWith.append(w)
                elif searched in w.lower():
                    matchedWordsIncludes.append(w)

            matchedWordsStartsWith = sorted(matchedWordsStartsWith)
            matchedWordsIncludes = sorted(matchedWordsIncludes)
            matchedWords = matchedWordsStartsWith + matchedWordsIncludes

            for w in matchedWords:
                self.searchWord_ListWidget.addItem(QtWidgets.QListWidgetItem(w))
            
            self.wordInfo_Label.setText(f"Listing {len(matchedWords)} of {len(self.wordDataDict)} words")

        self.searchWord_LineEdit = QtWidgets.QLineEdit()
        self.searchWord_LineEdit.setPlaceholderText("Search Words...")
        self.searchWord_LineEdit.setFont(inapp_font)
        self.searchWord_LineEdit.setMinimumWidth(400)
        self.searchWord_LineEdit.textChanged.connect(lambda: updateListWidget(self.searchWord_LineEdit.text()))

        self.searchWord_ListWidget = QtWidgets.QListWidget()
        self.searchWord_ListWidget.setFont(inapp_font)
        self.searchWord_ListWidget.setMinimumHeight(400)
        
        self.wordInfo_Label = QtWidgets.QLabel(f"Listing {len(self.wordDataDict)} of {len(self.wordDataDict)} words")
        self.wordInfo_Label.setFont(inapp_font)

        updateListWidget('')
        if selectedWord is not None:
            self.searchWord_ListWidget.setCurrentItem(self.searchWord_ListWidget.findItems(selectedWord.word, QtCore.Qt.MatchExactly)[0])

        # endregion

        # region Back, Edit and Open buttons and layouts

        def editSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()
            selectedWord = word.Word()
            selectedWord.loadFromDict(selectedWordStr, self.wordDataDict[selectedWordStr])

            self.switchMenu(Menu.ADD_WORD, selectedWord)

        def openSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()
            selectedWord = word.Word()
            selectedWord.loadFromDict(selectedWordStr, self.wordDataDict[selectedWordStr])

            self.switchMenu(Menu.SURF_WORDS, selectedWord)

        def removeSelected():
            selectedItem = self.searchWord_ListWidget.selectedItems()
            if not selectedItem:
                return
            selectedWordStr = selectedItem[0].text()

            reply = QtWidgets.QMessageBox.question(self, "Are you sure?", f"Do you really Want to remove {selectedWordStr} from your dictionary?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.wordDataDict.pop(selectedWordStr)
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
        self.searchWord_MainVLayout.addWidget(self.wordInfo_Label)
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

        keys_list = sorted(list(self.wordDataDict.keys()))

        # region Initialize
        if currentWord is None:
            currentWord = word.Word()
            randomWord = keys_list[0]
            currentWord.loadFromDict(randomWord, self.wordDataDict[randomWord])

        index = 0
        for i in range(len(keys_list)):
            if keys_list[i] == currentWord.word:
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
            lbl.setWordWrap(True)
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
            lbl.setWordWrap(True)
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
                index = len(keys_list) - 1
            elif index > len(keys_list) - 1:
                index = 0
            currentStr = keys_list[index]
            currentWord.loadFromDict(currentStr, self.wordDataDict[currentStr])
            self.switchMenu(Menu.SURF_WORDS, currentWord)

        def getRandomWord():
            new_word = word.Word()
            if len(keys_list) <= 1:
                return
            randomWord = random.choice(keys_list)
            while randomWord == currentWord.word:
                randomWord = random.choice(keys_list)
            new_word.loadFromDict(randomWord, self.wordDataDict[randomWord])
            self.switchMenu(self.currentMenu, new_word)

        def removeSelected():
            selectedWordStr = currentWord.word

            reply = QtWidgets.QMessageBox.question(self, "Are you sure?", f"Do you really Want to remove {selectedWordStr} from your dictionary?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.wordDataDict.pop(selectedWordStr)
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

        self.surfWords_GetRandomButton = QtWidgets.QPushButton("Random")
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

    def createPlayGameMenu(self):
        all_keys = list(self.wordDataDict.keys())
        shuffled_keys = list(self.wordDataDict.keys())
        random.shuffle(shuffled_keys)
        self.score = 0
        
        def chose_correct_answer():
            self.score += 4
            self.score_Label.setText(f"Score: {self.score}")
            reload_playgame()
        
        def chose_wrong_answer():
            self.score -= 1
            self.score_Label.setText(f"Score: {self.score}")
            for button in self.buttons:
                button.setStyleSheet("QPushButton:disabled { color: white; background-color: red;}")
                button.setEnabled(False)
            self.buttons[3].setStyleSheet("QPushButton:disabled { color: white; background-color: blue;}")
            
            def erase_colors():
                try:
                    for button in self.buttons:
                        button.setStyleSheet("")
                        button.setEnabled(True)
                    
                    reload_playgame()
                except:
                    pass
            
            QtCore.QTimer.singleShot(800, erase_colors)
        
        def reload_playgame():
            # Choose words
            if not shuffled_keys:
                pass
            
            current_word = shuffled_keys[0]
            del shuffled_keys[0]
            other_words = [current_word]
            
            definitions = self.wordDataDict[current_word]['definitions']
            incorrect_words = []
            while True:
                incorrect_words = random.sample(all_keys, 3)
                all_ok = True
                for word in incorrect_words:
                    for word_def in self.wordDataDict[word]['definitions']:
                        if word_def in definitions:
                            all_ok = False
                            break
                    if not all_ok:
                        break
                
                if all_ok:
                    break
            
            # Update Widgets
            self.buttons = [self.choiceA_button, self.choiceB_button, self.choiceC_button, self.choiceD_button]
            random.shuffle(self.buttons)
            try:
                for button in self.buttons:
                    button.clicked.disconnect()
            except:
                pass
            for i, inc_word in enumerate(incorrect_words):
                self.buttons[i].setText(random.choice(self.wordDataDict[inc_word]['definitions']))
                self.buttons[i].clicked.connect(chose_wrong_answer)
            self.buttons[3].setText(random.choice(self.wordDataDict[current_word]['definitions']))
            self.buttons[3].clicked.connect(chose_correct_answer)
            
            self.bottom_question_label.setText(f"of the word \"<font color=\"red\">{current_word}</font>\"?")
        
        # region score and timer label
        self.score_Label = QtWidgets.QLabel("Score: 0")
        self.score_Label.setFont(inapp_font)
        self.score_Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.score_Label.setMinimumWidth(200)
        self.timer_Label = QtWidgets.QLabel("Timer: 60")
        self.timer_Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.timer_Label.setFont(inapp_font)
        self.timer_Label.setMinimumWidth(200)
        
        self.playGame_TopHLayout = QtWidgets.QHBoxLayout()
        self.playGame_TopHLayout.addWidget(self.score_Label)
        self.playGame_TopHLayout.addStretch()
        self.playGame_TopHLayout.addWidget(self.timer_Label)
        # endregion
        
        # region Question Label
        # self.question_label = QtWidgets.QLabel("What is the correct definition of the word <font color=\"red\">word</font>?")
        self.top_question_label = QtWidgets.QLabel("What is the correct definition")
        self.top_question_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.top_question_label.setFont(text_font)
        
        self.bottom_question_label = QtWidgets.QLabel("of the word \"<font color=\"red\">word</font>\"?")
        self.bottom_question_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.bottom_question_label.setFont(text_font)
        # endregion
        
        # region Correct/Incorrect label
        self.correct_incorrect_Label = QtWidgets.QLabel("")
        self.correct_incorrect_HLayout = QtWidgets.QHBoxLayout()
        self.correct_incorrect_HLayout.addStretch()
        self.correct_incorrect_HLayout.addWidget(self.correct_incorrect_Label)
        self.correct_incorrect_HLayout.addStretch()
        # endregion
        
        # region Buttons
        self.choiceA_button = QtWidgets.QPushButton("Choice A")
        self.choiceA_button.setFont(button_font)
        self.choiceB_button = QtWidgets.QPushButton("Choice B")
        self.choiceB_button.setFont(button_font)
        self.choiceC_button = QtWidgets.QPushButton("Choice C")
        self.choiceC_button.setFont(button_font)
        self.choiceD_button = QtWidgets.QPushButton("Choice D")
        self.choiceD_button.setFont(button_font)
        
        self.playGame_ABHorizontalLayout = QtWidgets.QHBoxLayout()
        self.playGame_ABHorizontalLayout.addWidget(self.choiceA_button)
        self.playGame_ABHorizontalLayout.addWidget(self.choiceB_button)
        
        self.playGame_CDHorizontalLayout = QtWidgets.QHBoxLayout()
        self.playGame_CDHorizontalLayout.addWidget(self.choiceC_button)
        self.playGame_CDHorizontalLayout.addWidget(self.choiceD_button)
        
        self.playGame_buttonsVLayout = QtWidgets.QVBoxLayout()
        self.playGame_buttonsVLayout.addLayout(self.playGame_ABHorizontalLayout)
        self.playGame_buttonsVLayout.addLayout(self.playGame_CDHorizontalLayout)
        # endregion
        
        # region Bottom buttons
        self.playGame_BackButton = QtWidgets.QPushButton("Back")
        self.playGame_BackButton.setFont(inapp_font)
        self.playGame_BackButton.setMinimumWidth(120)
        self.playGame_BackButton.setMaximumWidth(120)
        self.playGame_BackButton.clicked.connect(lambda: self.switchMenu(self.previousMenu))
        
        self.playGame_BottomHLayout = QtWidgets.QHBoxLayout()
        self.playGame_BottomHLayout.addStretch()
        self.playGame_BottomHLayout.addWidget(self.playGame_BackButton)
        self.playGame_BottomHLayout.addStretch()
        # endregion
        
        # region Main Layouts
        self.playGame_MainVLayout = QtWidgets.QVBoxLayout()
        self.playGame_MainVLayout.addWidget(self.getVerticalSpacer(30))
        self.playGame_MainVLayout.addLayout(self.playGame_TopHLayout)
        self.playGame_MainVLayout.addStretch()
        self.playGame_MainVLayout.addWidget(self.top_question_label)
        self.playGame_MainVLayout.addWidget(self.bottom_question_label)
        self.playGame_MainVLayout.addWidget(self.getVerticalSpacer(120))
        self.playGame_MainVLayout.addLayout(self.playGame_buttonsVLayout)
        
        self.playGame_MainVLayout.addWidget(self.getVerticalSpacer(45))
        self.playGame_MainVLayout.addLayout(self.playGame_BottomHLayout)
        self.playGame_MainVLayout.addWidget(self.getVerticalSpacer(30))
        
        self.playGame_MainHLayout = QtWidgets.QHBoxLayout()
        self.playGame_MainHLayout.addStretch()
        self.playGame_MainHLayout.addLayout(self.playGame_MainVLayout)
        self.playGame_MainHLayout.addStretch()
        self.central.setLayout(self.playGame_MainHLayout)
        # endregion
        
        reload_playgame()
    
    def loadWords(self):
        if not os.path.exists(word.dataFoldername):
            os.mkdir(word.dataFoldername)
        if not os.path.exists(f"{word.dataFoldername}/words.json"):
            f = open(f"{word.dataFoldername}/words.json", "w")
            f.write("{}")
            f.close()
        with open(f"{word.dataFoldername}/words.json") as f:
            self.wordDataDict = json.load(f)

    def loadAppdata(self):
        if not os.path.exists(word.dataFoldername):
            os.mkdir(word.dataFoldername)
        if not os.path.exists(f"{word.dataFoldername}/appdata.json"):
            f = open(f"{word.dataFoldername}/appdata.json", "w")
            json.dump(self.appdataDict, f)
            f.close()
        with open(f"{word.dataFoldername}/appdata.json") as f:
            self.appdataDict = json.load(f)
    
    # Creates a label with given height and returns it
    def getVerticalSpacer(self, height):
        spacer = QtWidgets.QLabel(" ")
        spacer.setMinimumHeight(height)
        spacer.setMaximumHeight(height)
        return spacer
    
    def saveWordData(self):
        with open(f"{word.dataFoldername}/words.json", 'w') as f:
            json.dump(self.wordDataDict, f)
    
    def saveAppdata(self):
        with open(f"{word.dataFoldername}/appdata.json", 'w') as f:
            json.dump(self.appdataDict, f)


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    exit_code = app.exec()
    window.saveWordData()
    window.saveAppdata()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
