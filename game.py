from field import Field
from team import Team
from player import Player
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import numpy as np
from player import Player
import action
from planning import football
from zone import Zone
import random
import planning
from planning.planning import ForwardPlan
from planning.search import breadth_first_tree_search

class Game(ABC) :
    def __init__(self, team1 : Team, team2 : Team, field : Field , time , points : list ):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.points = points
        self.time = time
       
    @abstractmethod
    def play(self):
        pass

class Football(Game):
    def __init__(self,team1 , team2 , field , time , points):
        super().__init__(team1 , team2 , field , time , points)
    
    def play(self):
        print("Playing Football")
        self.team1.set_active_players([player.name for player in self.team1.players[0:11]])
        self.team2.set_active_players([player.name for player in self.team2.players[0:11]])
        team_with_posecionball = self.select_initial_team_with_ball()
        player_with_ballposition = self.select_initial_player_with_ball(team_with_posecionball)
        self.initialize_attakers_positions(self.team1 , self.team2)
        for i in range(self.time):
            if(i!= 0):
                self.move_player_in_team_with_ballposicion(player_with_ballposition,team_with_posecionball)
            actions_defenses = []
            if(self.team1 == team_with_posecionball):
                actions_defenses = self.move_player_in_team_without_ballposicion(player_with_ballposition,self.team2)
            else:
                actions_defenses= self.move_player_in_team_without_ballposicion(player_with_ballposition,self.team2)
            variables ,problem =football.football_model(team_with_posecionball,player_with_ballposition)
            sol = breadth_first_tree_search(ForwardPlan(problem))[0]
            solution = sol.solution(variables)
            player_success ,action = self.choose_player_success(variables([solution.args[0]],solution.name),actions_defenses)
            
            print("Time: ", i, end="\r")
        print("Game Over")
        if(self.points[0] > self.points[1]):
            print("Team 1 win" , self.points)
        else : print('Team 2 win' , self.points)
        


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
      
    def move_player_in_team_with_ballposicion(self , player_with_ball : Player , team : Team):
        for player in team.players:
            if (player_with_ball.current_position.types == 'Atack' or player_with_ball.position.types == 'Midfield'):
                if(self.IsValid(player.current_position.row + 1)):
                    player.position.row += 1
    

    def move_player_in_team_without_ballposicion(self , player_with_ball : Player ,team : Team):
        actions = []
        for player in team.players:
            if(player.current_position == player_with_ball.current_position and not player.role == 'goalkeeper'):
                entry = action.Entry('entry')
                actions.append((player,entry))
            elif(not player.current_position  == player.position):
                if(self.IsValid(player.current_position.row - 1)):
                    move = action.Move('move', player.current_position.row - 1)
                    actions.append((player,move))
        return actions

    def select_initial_team_with_ball(self):
        return self.team1 if random.randint(0,1) == 0 else self.team2

    def select_initial_player_with_ball(self, team : Team):
        att = [player for player in team.players if player.role == 'F']
        return random.choice(att)

    def initialize_attakers_positions(self, firstTeam: Team, secondTeam: Team):
        for i in range(len(firstTeam.players)):
            if firstTeam.players[i].role == 'F':
                firstTeam.players[i] = firstTeam.players[i].current_position.row - 1 

            if secondTeam.players[i].role == 'F':
                secondTeam.players[i] = secondTeam.players[i].current_position.row - 1 

        return firstTeam, secondTeam
        
    def IsValid(self , row):
        if(row < 3):
            return True
        return False

    
    

    