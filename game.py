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
        print("Time: ", self.time)





