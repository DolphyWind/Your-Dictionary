import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.windowSize = (800, 600)
        self.setWindowTitle("Your Dictionary")
        self.setGeometry(0, 0, self.windowSize[0], self.windowSize[1])
        self.center()
        self.createMainMenu()

        self.show()

    def createMainMenu(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
