
import json

class Player:
    def __init__(self, name, team, actions, features):
        self.name = name
        self.actions = actions
        self.features = features
        self.team = team
        self.load_data()

    def load_data(self):
        #  open data.json
        with open('data.json') as json_file:
            data = json.load(json_file)
            self.attack = data[self.team][self.name]['attack']
            self.creativity = data[self.team][self.name]['creativity']
            self.defense = data[self.team][self.name]['defense']
            self.tactical = data[self.team][self.name]['tactical']
            self.technical = data[self.team][self.name]['technical']
