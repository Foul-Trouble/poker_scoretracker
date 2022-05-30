from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog, QCheckBox, QRadioButton, QTableWidgetItem)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer, QTime

import json
import datetime


class Player:
    def __init__(self, name):
        from game_creator import gameStartInfo
        self.name = name
        self.hands_won = 0
        self.current_balance = gameStartInfo.buyin
        self.current_count = 0
        self.game_record = []
        self.in_game = True

    def add_money(self, amount, hand, time):
        self.current_balance += amount
        self.game_record.append(f'${amount} added at hand {hand}, at game time {time}')
        self.in_game = True

    def out_of_money(self, hand, time):
        self.current_balance = 0
        self.in_game = False
        self.game_record.append(f'Ran out of money at hand {hand}, at game time {time}')

    def cash_out(self, hand, time):
        self.in_game = False
        self.game_record.append(f'Cashed out with {self.current_balance} after hand {hand}, at game time {time}')


class Game:
    def __init__(self):
        self.game_active_players = []
        self.hand_active_players = []
        self.active_player = None
        self.hand = 1
        self.call_amount = 0
        self.pot_amount = 0
        self.game_record = []


class MainGame(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('main_game.ui', self)
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
        self.log_time = None

        self.game = Game()
        from game_creator import gameStartInfo
        for enu, player in enumerate(gameStartInfo.players):
            player = Player(player)
            self.game.game_active_players.append(player)
        self.initUI()
        self.time = QTime(0, 0, 0)

    def initUI(self):
        self.setWindowTitle(f'Main Game - {datetime.date.today()}')
        self.setFixedSize(975, 620)
        self.show()
        for enu, player in enumerate(self.game.game_active_players):
            def choices(enum):
                def chosenPlayer():
                    self.game.active_player = self.game.game_active_players[enum]
                    self.update_buttons()
                choice = QRadioButton()
                choice.setAccessibleName(self.game.game_active_players[enum].name)
                choice.setText(self.game.game_active_players[enum].name)
                self.playersLayout.addWidget(choice)
                choice.clicked.connect(chosenPlayer)
            choices(enu)
        self.scoreboardTable.setColumnWidth(0, 169)
        self.scoreboardTable.setColumnWidth(1, 100)
        self.scoreboardTable.setColumnWidth(2, 100)
        self.scoreboardTable.setColumnWidth(3, 100)
        self.scoreboardTable.setRowCount(len(self.game.game_active_players))
        for row, player in enumerate(self.game.game_active_players):
            self.scoreboardTable.setItem(row, 0, QTableWidgetItem(player.name))
            self.scoreboardTable.setItem(row, 1, QTableWidgetItem(f'${player.current_balance}'))
            self.scoreboardTable.setItem(row, 2, QTableWidgetItem(player.current_count))
            self.scoreboardTable.setItem(row, 3, QTableWidgetItem(str(player.hands_won)))

        self.endGameButton.clicked.connect(self.endGame)
        self.nextHandButton.clicked.connect(self.nextHand)
        self.smallBlindButton.clicked.connect(self.smallBlind)
        self.bigBlindButton.clicked.connect(self.bigBlind)
        self.callButton.clicked.connect(self.call)
        self.raiseButton.clicked.connect(self.raise_amount)
        self.foldButton.clicked.connect(self.fold)
        self.allInButton.clicked.connect(self.allIn)
        self.wonByBluffButton.clicked.connect(self.wonbybluff)
        self.wonByTopButton.clicked.connect(self.wonbytop)
        self.add5DollarsButton.clicked.connect(self.add5dollars)
        self.add10DollarsButton.clicked.connect(self.add10dollars)

    def displayTime(self):
        currentTime = QTime.currentTime()
        self.time = self.time.addSecs(1)

        time = self.time.toString("hh:mm")
        displayTxt = currentTime.toString('hh:mm')
        self.log_time = self.time.toString("hh:mm:ss")

        self.currentTime.display(displayTxt)
        self.gameTime.display(time)

    def add5dollars(self):
        self.game.active_player.add_money(5, self.game.hand, self.log_time)

    def add10dollars(self):
        self.game.active_player.add_money(10, self.game.hand, self.log_time)

    def smallBlind(self):
        if self.numberField.text() != "":
            amount = float(self.numberField.text())
            if amount < self.game.active_player.current_balance:
                self.game.pot_amount += amount
                self.game.call_amount = amount
                self.numberField.clear()
                self.game.active_player.current_balance -= self.game.call_amount
                self.updateScoreboard()

    def bigBlind(self):
        if self.numberField.text() != "":
            amount = float(self.numberField.text())
            if amount < self.game.active_player.current_balance:
                self.game.pot_amount += amount
                self.game.call_amount = amount
                self.numberField.clear()
                self.game.active_player.current_balance -= self.game.call_amount
                self.updateScoreboard()

    def call(self):
        if self.game.call_amount < self.game.active_player.current_balance:
            self.game.pot_amount += float(self.game.call_amount)
            self.currentInPotLabel.setText(f'${self.game.pot_amount}')
            self.game.active_player.current_balance -= self.game.call_amount
            self.updateScoreboard()

    def raise_amount(self):
        if self.numberField.text() != "":
            amount = float(self.numberField.text()) + self.game.call_amount
            if amount < self.game.active_player.current_balance:
                self.game.pot_amount += amount
                self.game.call_amount = amount
                self.numberField.clear()
                self.game.active_player.current_balance -= self.game.call_amount
                self.updateScoreboard()
            else:
                print("This player does not have enough for this raise")

    def fold(self):
        self.game.hand_active_players.remove(self.game.active_player.name)

    def allIn(self):
        self.game.pot_amount += self.game.active_player.current_balance
        if self.game.call_amount < self.game.active_player.current_balance:
            self.game.call_amount = self.game.active_player.current_balance
        self.game.active_player.current_balance = 0

        self.updateScoreboard()

    def wonbybluff(self):
        if self.game.active_player is not None:
            self.game.active_player.current_balance += self.game.pot_amount
            self.game.pot_amount = 0
            self.game.call_amount = 0
            self.game.hand += 1
            self.updateScoreboard()
            self.raiseButton.setEnabled(False)

    def wonbytop(self):
        if self.game.active_player is not None:
            self.game.active_player.current_balance += self.game.pot_amount
            self.game.pot_amount = 0
            self.game.call_amount = 0
            self.game.hand += 1
            self.updateScoreboard()

    def updateScoreboard(self):
        self.scoreboardTable.clearContents()
        self.scoreboardTable.setRowCount(len(self.game.game_active_players))
        for row, player in enumerate(self.game.game_active_players):
            self.scoreboardTable.setItem(row, 0, QTableWidgetItem(player.name))
            self.scoreboardTable.setItem(row, 1, QTableWidgetItem(f'${player.current_balance}'))
            self.scoreboardTable.setItem(row, 2, QTableWidgetItem(player.current_count))
            self.scoreboardTable.setItem(row, 3, QTableWidgetItem(str(player.hands_won)))
        self.currentCallLabel.setText(f'${self.game.call_amount}')
        self.currentInPotLabel.setText(f'${self.game.pot_amount}')
        self.handCount.display(self.game.hand)

    def update_buttons(self):
        if self.game.active_player.current_balance <= self.game.call_amount:
            self.callButton.setEnabled(False)
            self.raiseButton.setEnabled(False)
        else:
            self.callButton.setEnabled(True)
            self.raiseButton.setEnabled(True)

    def nextHand(self):
        self.updateScoreboard()

    def endGame(self):
        self.close()
