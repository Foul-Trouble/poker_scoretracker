from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication,
                             QMainWindow, QPushButton, QDialog)

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer

import json


class NewPlayer(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('new_player.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Creating New Player')
        self.show()
        self.saveButton.clicked.connect(self.end)

    def end(self):
        self.createProfile()
        self.close()

    def createProfile(self):
        profile_exists = False
        with open("json/players.json", 'r') as file:
            data = json.load(file)
        for i in data:
            if i["info"]["name"] == self.nameField.text():
                profile_exists = True
                break
        else:
            data.append({
                "info":
                    {"name": self.nameField.text(),
                     "email": self.emailField.text(),
                     "address": self.addressField.text(),
                     "phone_number": self.phonenumberField.text()
                     },
                "player_statistics": {
                                "games_won": "0",
                                "games_lost": "0",
                                "games_played": "0",
                                "+/-": "0"
                                },
                "player_history": []
            }
            )
        if not profile_exists:
            with open("json/players.json", 'w') as file:
                json.dump(data, file, indent=4)
        else:
            print("A profile with this name already exists!")




