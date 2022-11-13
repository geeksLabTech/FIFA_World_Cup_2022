from field import Field
from team import Team
# from zone import Zone
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import numpy as np
from player import Player

class Game(ABC) :
    def __init__(self, team1 : Team, team2 : Team, field : Field , time):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.time = time
    
    @abstractmethod
    def play(self):
        pass

class Football(Game):
    def __init__(self,team1 , team2 , field , time):
        super().__init__(team1 , team2 , field , time)
    
    def play(self):
        print("Playing Football")
        for i in range(self.time):
            print("Time: ", i, end="\r")
        print("Game Over")
        import random
        winner = self.team1.name if random.randint(0,1) == 0 else self.team2.name
        print(f"winner: {winner}")


    def choose_player_success(self, player_with_ball: Tuple[Player, str], adversaries: List[Tuple[Player, str]]):

        player, action = player_with_ball

        player_prob = player.attributes_score[action]
        # Dictionary with player name as key and TabularCPD as value
        total = sum([x[0].attributes_score[x[1]] for x in adversaries]) + player_prob
        model = {player.name: player_prob/total}
        for adversary in adversaries:
            player, action = adversary
            player_prob = player.attributes_score[action]
            model[player.name] = player_prob/total

        # Choose a random action in model based on player_probs
        player_name = np.random.choice(list(model.keys()), p=list(model.values()))
        return player_name




