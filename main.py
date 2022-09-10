import sys
from PyQt5 import QtWidgets, QtGui, QtCore

header_font = QtGui.QFont("OpenSans", 28)
button_font = QtGui.QFont("OpenSans", 16)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.windowSize = (600, 800)
        self.setWindowTitle("Your Dictionary")
        self.setGeometry(0, 0, self.windowSize[0], self.windowSize[1])
        self.center()
        self.createMainMenu()

        self.show()

    def createMainMenu(self):
        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainVLayout = QtWidgets.QVBoxLayout()

        self.mainTitle = QtWidgets.QLabel("Your Dictionary")
        self.mainTitle.setFont(header_font)
        self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.addAWordButton = QtWidgets.QPushButton("Add Word")
        self.searchWordButton = QtWidgets.QPushButton("Search Word")
        self.gameButton = QtWidgets.QPushButton("Play A Game")
        self.getARandomWordButton = QtWidgets.QPushButton("Get A Random Word")

        self.quitButton = QtWidgets.QPushButton("Quit Application")
        self.quitButton.clicked.connect(self.close)

        self.mainMenuButtons = []
        self.mainMenuButtons.append(self.addAWordButton)
        self.mainMenuButtons.append(self.searchWordButton)
        self.mainMenuButtons.append(self.gameButton)
        self.mainMenuButtons.append(self.getARandomWordButton)
        self.mainMenuButtons.append(self.quitButton)

        for b in self.mainMenuButtons:
            b.setMinimumHeight(50)
            b.setMaximumHeight(50)
            b.setFont(button_font)

        self.mainVLayout.addStretch()
        self.mainVLayout.addWidget(self.mainTitle)
        self.mainVLayout.addStretch()
        for b in self.mainMenuButtons:
            self.mainVLayout.addWidget(b)
        self.mainVLayout.addStretch()

        self.mainHLayout.addStretch()
        self.mainHLayout.addLayout(self.mainVLayout)
        self.mainHLayout.addStretch()

        self.setLayout(self.mainHLayout)


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
