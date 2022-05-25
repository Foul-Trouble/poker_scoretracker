from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog, QCheckBox, QRadioButton)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer

import json
import copy
import main_game


class GameStartData:
    def __init__(self):
        self.players = []
        self.location = None
        self.buyin = None


class GameCreation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('game_creator.ui', self)
        self.initUI()
        global players

    def initUI(self):
        self.setWindowTitle('Creating New Game...')
        self.show()
        self.startButton.clicked.connect(self.end)

        with open('json/players.json', 'r') as f:
            player_data = json.load(f)
        for enu, player in enumerate(player_data):
            def choices(enum):
                def addToPlayers():
                    if player_data[enum]["info"]["name"] not in gameStartInfo.players:
                        gameStartInfo.players.append(player_data[enum]["info"]["name"])
                    else:
                        gameStartInfo.players.remove(player_data[enum]["info"]["name"])
                choice = QCheckBox()
                choice.setAccessibleName(player["info"]["name"])
                choice.setText(player["info"]["name"])
                self.choosePlayersLayout.addWidget(choice)
                choice.clicked.connect(addToPlayers)
            choices(enu)

        for enu, player in enumerate(player_data):
            def choices(enum):
                def switchLocation():
                    if player_data[enum]["info"]["name"] not in gameStartInfo.players:
                        gameStartInfo.location = f"{player_data[enum]['info']['name']}'s House"
                choice = QRadioButton()
                choice.setAccessibleName(f"{player_data[enum]['info']['name']}'s")
                choice.setText(f"{player_data[enum]['info']['name']}'s")
                self.chooseLocationLayout.addWidget(choice)
                choice.clicked.connect(switchLocation)
            choices(enu)

    def end(self):
        create = main_game.MainGame(self)
        self.close()


gameStartInfo = GameStartData()
