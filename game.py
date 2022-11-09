from field import Field
from team import Team
from zone import Zone
from abc import ABC, abstractmethod
class Game(ABC) :
    def __init__(self, team1 : Team, team2 : Team, field : Field , zone : list[Zone] , time):
        self.team1 = team1
        self.team2 = team2
        self.zone = zone
        self.field = self.zone_field(field)
        self.time = time
    
    def zone_field(self ,field: Field):
        field = [None]*field.width[None]*field.lenght
        defense_x0 , defense_x1 = self.zone[0].funcion(field)
        attack_x0 , attack_x1 = self.zone[1].funcion(field)
        middle_x0 , middle_x1 = self.zone[2].funcion(field)
        for i in range(field.width):
            for j in range(field.lenght):
                if(i >= defense_x0 and i <= defense_x1):
                    field.field[i][j] = self.zone[0].name
                elif(i >= attack_x0 and i <= attack_x1):
                    field.field[i][j] = self.zone[1].name
                elif(i >= middle_x0 and i <= middle_x1):
                    field.field[i][j] = self.zone[2].name

    @abstractmethod
    def play(self):
        pass

class Football(Game):
    def __init__(self,team1 , team2 , field, zone , time):
        zone = []
        zone.append(('Defense', lambda field : ((0 , field.length/3), (field.width/3 , ))))
        zone.append(('Midfield',lambda field : (field.length/3 ,  field.length/3)))
        zone.append(('Attack',lambda field : (2*field.length/3 , field.length)))
        super().__init__(team1 , team2 , field , zone, time)
    
    def play(self):
        print("Playing Football")
        print("Time: ", self.time)





