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
from planning.planning import ForwardPlan
from planning.search import breadth_first_tree_search
from planning.planning import Action

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
            #TODO Javier lo rojo eso que esta ahi es tuyo
            player_success = self.choose_player_success(variables([solution.args[0]],solution.name),actions_defenses)
            self.action_success(player_with_ballposition, solution.name,actions_defenses , player_success)
            print("Time: ", i, end="\r")
        print("Game Over")
        if(self.points[0] > self.points[1]):
            print("Team 1 win" , self.points)
        else : print('Team 2 win' , self.points)
        
    def action_success(self ,playerballposition : Player, actionplayerball : str , actions_defeses : List[Tuple[Player,str]], player_success : Player):
        for i in actions_defeses:
            if (i[0] == player_success):
                self.execute_action(i[1],i[0] , 'D')
                return
                
        self.execute_action(actionplayerball,playerballposition, 'A')
        
    def execute_action(self,action_name : str , player: Player , rol : str):
        if(action_name == 'Move'):
            success_action = action.Move('move')
            if(rol == 'D'):
                success_action.execute(player,-1,0)

            #TODO necesito que el jugador ue tiene la pelota me diga para donde se mueve
        elif(action_name == 'Entry'):
            success_action = action.Entry('entry')
            success_action.execute(player)
        elif(action_name == 'Shoot'):
            success_action = action.Shoot('shoot')
            success_action.execute()
        elif(action_name == 'Pass'):
            success_action = action.Pass('pass')
            #TODO necesito que el jugador que tiene la pelota me diga a quien esta pasado 
            # los que estan defendiendo no pasan
            return


    # TODO Refactor this function
    def choose_player_success(self, player_with_ball: Tuple[Player, Action], dicc: Dict[str, Player], adversaries: List[Tuple[Player, str]], pos_to_zone: Dict[Tuple[int, int], Zone]):
        all_players = [player_with_ball] + adversaries
        current_player, action = player_with_ball
        player_prob = current_player.attributes_score[action]
        real_adversaries = []
        positions_arr = [(0,1), (1,0), (0,-1), (-1, 0), (1,1), (-1,-1), (1,-1), (-1,1)]

        if action.name == 'Pass':
            target_player = dicc[str(action.args[1])]
            real_adversaries = [(p, act) for p, act in adversaries if p.current_position == target_player.current_position or p.current_position == current_player.current_position]
            total = sum([x[0].attributes_score[x[1]] for x in real_adversaries]) + player_prob
            success_probs = [player_prob/total]
            players_to_choose = [player_with_ball] + real_adversaries
            for x in real_adversaries:
                adv_prov = x[0].attributes_score[x[1]] / total
                success_probs.append(adv_prov)
            
            succesful_player = np.random.choice([x[0].name for x in players_to_choose], p=success_probs)
            result = ()
            for x in all_players:
                if x[0].name == succesful_player:
                    if type(x[1]) == Action:
                        result = (x[0], x[1].name, target_player)
                    else:
                        result = (x[0], x[1])
                    break
            
            return result

        elif action.name == 'Shoot':
            real_adversaries = [(p, act) for p, act in adversaries if p.current_position == current_player.current_position or p.role == 'G']
            total = sum([x[0].attributes_score[x[1]] for x in real_adversaries]) + player_prob
            success_probs = [player_prob/total]
            players_to_choose = [player_with_ball] + real_adversaries
            for x in real_adversaries:
                adv_prov = x[0].attributes_score[x[1]] / total
                success_probs.append(adv_prov)
            
            succesful_player = np.random.choice([x[0].name for x in players_to_choose], p=success_probs)
            result = ()
            for x in all_players:
                if x[0].name == succesful_player:
                    if type(x[1]) == Action:
                        result = (x[0], x[1].name)
                    else:
                        result = (x[0], x[1])
                    break
            
            return result
        elif action.name == 'Move':
            current_zone = current_player.current_position
            possible_coords_zones = [current_zone.get_coords() + pos for pos in positions_arr if current_zone.get_coords() + pos in pos_to_zone]
            zones_probs: Dict[Zone, Dict[Player, float]] = {}
            for coords in possible_coords_zones:
                possible_adversaries = [(p, act) for p, act in adversaries if p.current_position.get_coords() == coords]
                total = sum([x[0].attributes_score[x[1]] for x in possible_adversaries]) + player_prob
                zones_probs[pos_to_zone[coords]] = {current_player: player_prob/total}
                for x in possible_adversaries:
                    adv_prov = x[0].attributes_score[x[1]]
                    zones_probs[pos_to_zone[coords]][x[0]] = adv_prov/total
                
            success_arr = [zones_probs[x][current_player] for x in zones_probs]
            total_success = sum(success_arr)
            normalized_success_arr = [x/total_success for x in success_arr]

            target_coords_zone = np.random.choice(possible_coords_zones, p=normalized_success_arr)
            target_zone = pos_to_zone[target_coords_zone]

            target_players = zones_probs[target_zone].keys()
            target_probs = []
            for x in target_players:
                target_probs.append(zones_probs[target_zone][x])

            succesful_player = np.random.choice([x.name for x in target_players], p=target_probs)
            result = ()
            for x in all_players:
                if x[0].name == succesful_player:
                    if type(x[1]) == Action:
                        result = (x[0], x[1].name, target_zone)
                    else:
                        result = (x[0], x[1])
                    break
            
            return result
            
      
    def move_player_in_team_with_ballposicion(self , player_with_ball : Player , team : Team):
        for player in team.players:
            if (player_with_ball.current_position.types == 'Attack' or player_with_ball.position.types == 'Midfield'):
                if(self.IsValid(player.current_position.row + 1)):
                    player.position.row += 1
    

    def move_player_in_team_without_ballposicion(self , player_with_ball : Player ,team : Team):
        actions = []
        for player in team.players:
            if(player.current_position == player_with_ball.current_position and not player.role == 'goalkeeper'):  
                actions.append((player,'Entry'))
            elif(not player.current_position  == player.position):
                if(self.IsValid(player.current_position.row - 1)):
                    actions.append((player,'Move' ))
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

    
    

    