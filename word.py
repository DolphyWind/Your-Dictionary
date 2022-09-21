import os
import shutil

class Word:
    def __init__(self, word: str, imagePath: str = None, definitions: list = None, exampleSentences: list = None):
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
        shutil.copy2(self.imagePath, self.newImagePath)

    def getAsDictionary(self):
        return {'imageExists': self.imageExists,'definitions': self.definitions, 'exampleSentences': self.exampleSentences, 'fileExtension': self.fileExtension}