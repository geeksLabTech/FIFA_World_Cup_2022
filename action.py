from abc import ABC, abstractmethod
from player import Player
from game import Game
from field import Field


class Action(ABC):
    def __ini__(self , name) :
        self.name = name

    @abstractmethod
    def execute(self):
        pass


class SimpleAction(Action):
    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def execute(self):
        pass


class ComplexAction(Action):
    def __init__(self, name ):
        super().__init__(name)

    @abstractmethod
    def execute(self , object : object ):
        pass


class Shoot(SimpleAction):
    def __init__(self, name , tipo):
        super().__init__(name , tipo)
    
    def execute(self):
        #TODO : Calcular la accion resultante  que el jugador meta el gol(Redes Bayesianas)
        # return bool (hecho o no gol)
        pass


class Pass(ComplexAction):
    def __init__(self, name , tipo):
        super().__init__(name , tipo)
    
    def execute(self , player : Player):
        player.ballposition =  True

        pass   


class Move(ComplexAction):
    def __ini__(self, name):
        return super().__ini__(name)

    def execute(self, player : Player ):
        #TODO Calcular la accion resultante perder o no la pelota (Redes Bayesianas) jugador que gana la pelota
        player.ballposition = True
        #Todo : Mover al jugador de zona
        pass


class Mild_Entry(ComplexAction):
    def __init__(self, name):
        return super().__init__(name)

    def execute(self, player : Player):
        #TODO Calcular la accion resultante perder o no la pelota (Redes Bayesianas) jugador que gana la pelota
        player.ballposition = True
        pass


class Strong_Entry(ComplexAction):
    def __init__(self, name):
        return super().__init__(name)

    def execute(self, player : Player):
        #TODO Calcular la accion resultante perder o no la pelota (Redes Bayesianas) jugador que gana la pelota
        player.ballposition = True
        pass

    