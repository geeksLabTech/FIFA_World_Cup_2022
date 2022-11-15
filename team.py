
import json

from player import Player


class Team():
    def __init__(self, name ):
        self.team_name = name
        self.players = self.get_players()
        self.active_players = []
    
    def get_players(self) -> list[Player]:
        
        with open('data.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        players = []
        for p in data[self.team_name]:
            name = p
            team = self.team_name
            features = data[self.team_name][p]
            position = features['position'] if 'position' in features else "D"
            players.append(Player(name,team,features,position))
        return players

    def set_active_players(self,names):
        for p in self.players:
            if p.name in names:
                self.active_players.append(p)

            