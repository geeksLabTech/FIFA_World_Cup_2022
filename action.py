from abc import ABC, abstractmethod
from player import Player
# from game import Game
# from field import Field
from zone import Zone

class Action(ABC):
    def __init__(self , name) :
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
    def execute(self , *object : object):
        pass


class Shoot(SimpleAction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self):
        # return bool (hecho o no gol)
        pass
class Pass(ComplexAction):
    def __init__(self, name ):
        super().__init__(name)

    def execute(self , player : Player ):
        player.ballposition =  True


class Move(ComplexAction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, player : Player , zone : Zone):
        player.position = zone

class Tackle(ComplexAction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, player : Player):
        player.ballposition = True


class Intercept(ComplexAction):
    def __init__(self, name):
        super().__init__(name)  

    def execute(self , player : Player):
        player.ballposition = True   

class Entry(ComplexAction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, player : Player):
        player.ballposition = True

