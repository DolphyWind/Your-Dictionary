import os
import shutil

class Word:
    def __init__(self, word: str = None, imagePath: str = None, definitions: list = None, exampleSentences: list = None):
        if not word:
            return
        self.word = word

        self.imagePath = imagePath
        self.imageExists = True
        self.fileExtension = ''
        if not os.path.exists(self.imagePath):
            self.imageExists = False
        self.copyImageToDataFolder()

        self.definitions = definitions
        self.exampleSentences = exampleSentences

    def copyImageToDataFolder(self):
        if not self.imageExists:
            return

        self.fileExtension = self.imagePath.split('.')[-1]
        self.newImagePath = f'data/{self.word}.{self.fileExtension}'
        if self.imagePath != self.newImagePath:
            shutil.copy2(self.imagePath, self.newImagePath)

    def getAsDictionary(self):
        return {'imageExists': self.imageExists,'definitions': self.definitions, 'exampleSentences': self.exampleSentences, 'fileExtension': self.fileExtension}

    def loadFromDict(self, wordName: str, dct: dict):
        self.word = wordName
        self.imageExists = dct['imageExists']
        self.definitions = dct['definitions']
        self.exampleSentences = dct['exampleSentences']
        self.fileExtension = dct['fileExtension']
        if self.imageExists:
            self.imagePath = f'data/{self.word}.{self.fileExtension}'
