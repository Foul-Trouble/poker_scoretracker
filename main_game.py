from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog, QCheckBox, QRadioButton)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer, QTime

import json
import datetime


class MainGame(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('main_game.ui', self)
        self.initUI()
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

    def initUI(self):
        self.setWindowTitle(f'Main Game - {datetime.date.today()}')
        self.setFixedSize(975, 620)
        self.show()
        from game_creator import gameStartInfo
        for enu, player in enumerate(gameStartInfo.players):
            def choices(enum):
                def chosenPlayer():
                    print(gameStartInfo.players[enu])
                choice = QRadioButton()
                choice.setAccessibleName(gameStartInfo.players[enu])
                choice.setText(gameStartInfo.players[enu])
                self.playersLayout.addWidget(choice)
                choice.clicked.connect(chosenPlayer)
            choices(enu)
        self.endGameButton.clicked.connect(self.endGame)

    def displayTime(self):
        currentTime = QTime.currentTime()

        displayTxt = currentTime.toString('hh:mm')

        self.currentTime.display(displayTxt)

    def endGame(self):
        self.close()
