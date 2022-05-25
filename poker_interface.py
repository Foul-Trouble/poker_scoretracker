from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog, QCheckBox, QComboBox, QVBoxLayout, QHBoxLayout,
                             QStyleFactory, QLCDNumber, QTableWidgetItem)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer, QTime

import json

import new_player
import game_creator


def clearLayout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('poker_interface.ui', self)
        self.initUI()

    @staticmethod
    def run_gui():
        app = QApplication([])
        ex = MainGUI()
        app.exec_()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('G.U.I. Main Window')
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

        with open("style_sheets/Adaptic.qss", "r") as fh:
            self.setStyleSheet(fh.read())

        self.exitButton.clicked.connect(self.exitSoftware)
        self.addNewPlayerButton.clicked.connect(self.createNewPlayer)
        self.newGameButton.clicked.connect(self.createGame)

        self.playerStatistics.setColumnWidth(0, 169)
        self.playerStatistics.setColumnWidth(1, 50)
        self.playerStatistics.setColumnWidth(2, 50)
        self.playerStatistics.setColumnWidth(3, 50)
        with open('json/players.json', 'r') as f:
            player_data = json.load(f)
        self.playerStatistics.setRowCount(len(player_data))
        for row, player in enumerate(player_data):
            self.playerStatistics.setItem(row, 0, QTableWidgetItem(player["info"]["name"]))
            self.playerStatistics.setItem(row, 1, QTableWidgetItem(player["player_statistics"]["games_won"]))
            self.playerStatistics.setItem(row, 2, QTableWidgetItem(player["player_statistics"]["games_lost"]))
            self.playerStatistics.setItem(row, 3, QTableWidgetItem(player["player_statistics"]["+/-"]))

        self.gameStatistics.setColumnWidth(0, 150)
        self.gameStatistics.setColumnWidth(1, 150)
        self.gameStatistics.setColumnWidth(2, 150)
        self.gameStatistics.setColumnWidth(3, 150)
        self.gameStatistics.setColumnWidth(4, 150)

        with open('json/games.json', 'r') as f:
            game_data = json.load(f)
        self.gameStatistics.setRowCount(len(game_data))
        for row, game in enumerate(game_data):
            self.gameStatistics.setItem(row, 0, QTableWidgetItem(game["info"]["date"]))
            self.gameStatistics.setItem(row, 1, QTableWidgetItem(game["info"]["location"]))
            self.gameStatistics.setItem(row, 2, QTableWidgetItem(game["game_statistics"]["winner"]))
            self.gameStatistics.setItem(row, 3, QTableWidgetItem(game["game_statistics"]["loser"]))
            self.gameStatistics.setItem(row, 4, QTableWidgetItem(game["info"]["amount_in_pot"]))

    def displayTime(self):
        currentTime = QTime.currentTime()

        displayTxt = currentTime.toString('hh:mm')

        self.currentTime.display(displayTxt)

    def exitSoftware(self):
        exit()

    def createNewPlayer(self):
        create = new_player.NewPlayer(self)
        create.saveButton.clicked.connect(self.refreshStatistics)

    def refreshStatistics(self):
        with open('json/players.json', 'r') as f:
            player_data = json.load(f)
        self.playerStatistics.clear()
        self.playerStatistics.setRowCount(len(player_data))
        for row, player in enumerate(player_data):
            self.playerStatistics.setItem(row, 0, QTableWidgetItem(player["info"]["name"]))
            self.playerStatistics.setItem(row, 1, QTableWidgetItem(player["player_statistics"]["games_won"]))
            self.playerStatistics.setItem(row, 2, QTableWidgetItem(player["player_statistics"]["games_lost"]))
            self.playerStatistics.setItem(row, 3, QTableWidgetItem(player["player_statistics"]["+/-"]))

    def createGame(self):
        create = game_creator.GameCreation(self)


if __name__ == "__main__":
    MainGUI.run_gui()
