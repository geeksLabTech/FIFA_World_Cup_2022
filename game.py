from field import Field
from team import Team
from player import Player
from algorithms.particle_swarm import particle_swarm_optimization
from abc import ABC, abstractmethod
import random
class Game(ABC) :
    def __init__(self, team1 : Team, team2 : Team, field : Field , time , points : list , players : Player):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.points = points
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
    
    
    def transitions(self, player : list[ Player]):
        #TODO : Transformar la funcion de enjambre de particulas , debe devolver una accion
        player_acction_time_current = {}
        for player in players:
            player_acction_time_current[player] = particle_swarm_optimization(player)
        
        #TODO : Llamar a la red bayesiana con las acciones , eso debe devolver la accion que tuvo mas probabilidad
        #TODO : Luego se executa la accion
      