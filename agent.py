import numpy as np

class Agent:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def evaluate_actions(self, environment, players):
        pass

    def play(self, environment, players):
        pass


class RandomAgent(Agent):

    def evaluate_actions(self, players):
        selected_actions = []
        for player in players:
            selected_actions.append(np.random.choice(player.actions))
        return selected_actions

    def play(self, environment, players):
        return self.evaluate_actions(players)