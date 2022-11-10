from field import Field
from team import Team
# from zone import Zone
from abc import ABC, abstractmethod
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





