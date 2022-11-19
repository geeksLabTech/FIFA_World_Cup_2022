
import json

from player import Player
from zone import Zone
from typing import List


class Team():
    def __init__(self, name, zones):
        self.team_name = name
        self.players = self.get_players(zones)
        self.active_players = self.players

    def get_players(self,zones) -> List[Player]:
        
        with open('data.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        with open("lineups.json", "r") as file:
            lineups = json.load(file)[self.team_name]
        

        players = []
        # TODO Refactor this code
        for en,p in enumerate(lineups['att']):
            name = p
            team = self
            try:
                features = data[self.team_name][p]
            except KeyError:
                features = {}
            position = "F"
            players.append(Player(name,team,features,position, zones[6+en%3], zones[6+en%3] , False))
        
        for en,p in enumerate(lineups['mid']):
            name = p
            team = self
            try:
                features = data[self.team_name][p]
            except:
                features = {}
            position = "M"
            players.append(Player(name,team,features,position, zones[3+en%3], zones[3+en%3] , False))
        for en,p in enumerate(lineups['def']):
            name = p
            team = self
            try:
                features = data[self.team_name][p]
            except:
                features = {}
            position = "D"
            players.append(Player(name,team,features,position, zones[en%3], zones[en%3] , False))
            
        p = lineups['goalkeeper']

        name = p
        team = self
        try:
            features = data[self.team_name][p]
        except:
            features = {}
        position = "G"
        players.append(Player(name,team,features,position, Zone("Gate",5,5,"Gate"), Zone("Gate",5,5,"Gate") , False))
        assert len(players) == 11
        return players
    
    def set_active_players(self,names):
        for p in self.players:
            if p.name in names:
                self.active_players.append(p)
