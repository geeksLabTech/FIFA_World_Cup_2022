from map import Map
from team import Team
from zone import Zone
from abc import ABC, abstractmethod
class Game(ABC) :
    def __init__(self, team1 : Team, team2 : Team, map : Map , zone : list[Zone] , time):
        self.team1 = team1
        self.team2 = team2
        self.zone = zone
        self.map = self.zone_map(map)
        self.time = time
    
    def zone_map(self ,map: Map):
        map = [None]*map.width[None]*map.lenght
        defense_x0 , defense_x1 = self.zone[0].funcion(map)
        attack_x0 , attack_x1 = self.zone[1].funcion(map)
        middle_x0 , middle_x1 = self.zone[2].funcion(map)
        for i in range(map.width):
            for j in range(map.lenght):
                if(i >= defense_x0 and i <= defense_x1):
                    map.map[i][j] = self.zone[0].name
                elif(i >= attack_x0 and i <= attack_x1):
                    map.map[i][j] = self.zone[1].name
                elif(i >= middle_x0 and i <= middle_x1):
                    map.map[i][j] = self.zone[2].name


                    
                


    @abstractmethod
    def play(self):
        pass

class Football(Game):
    def __init__(self,team1 , team2 , map , zone , time):
        zone = []
        zone.append(('Defense', lambda mapa : (0 , mapa.length/3)))
        zone.append(('Midfield',lambda mapa : (mapa.length/3 ,  mapa.length/3)))
        zone.append(('Attack',lambda mapa : (2*mapa.length/3 , mapa.length)))
        super().__init__(team1 , team2 , map , zone, time)
    
    def play(self):
        print("Playing Football")
        print("Time: ", self.time)





