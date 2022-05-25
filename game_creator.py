from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer


class gameCreation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('game_creator.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Creating New Game...')
        self.show()
        self.startButton.clicked.connect(self.end)

    def end(self):
        self.close()

