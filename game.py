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
    def __init__(self, team1, team2, field, time):
        super().__init__(team1 , team2 , field , time , [0,0])
    
    def play(self):
        print("Start Game")
        team_with_ball_possession = self.select_initial_team_with_ball()
        player_with_ballposition = self.select_initial_player_with_ball(team_with_ball_possession)
        self.initialize_attakers_positions(self.team1 , self.team2)
        print('Initialization Complete')
        for i in range(self.time):
            if(i!= 0):
                self.move_player_in_team_with_ballposicion(player_with_ballposition,team_with_ball_possession)
            actions_defenses = []
            if(self.team1 == team_with_ball_possession):
                actions_defenses = self.move_player_in_team_without_ballposicion(player_with_ballposition,self.team2)
            else:
                actions_defenses= self.move_player_in_team_without_ballposicion(player_with_ballposition,self.team2)
            variables ,problem =football.football_model(team_with_ball_possession,player_with_ballposition)
            sol = breadth_first_tree_search(ForwardPlan(problem))
            action_of_player_with_ball, prob = self.get_best_solution(sol,variables)
            print('action', action_of_player_with_ball, type(action_of_player_with_ball))
            results = self.choose_player_success((player_with_ballposition, action_of_player_with_ball), variables,actions_defenses, self.field.coords_to_zone)
            self.process_results(results)
            # self.action_success(player_with_ballposition, solution.name,actions_defenses , player_success)
            print("Time: ", i, end="\r")
        print("Game Over")
        if(self.points[0] > self.points[1]):
            print(f"Team {self.team1.team_name} win" , self.points)
        elif self.points[0] < self.points[1]:
            print(f'Team {self.team2.team_name} win' , self.points)
        else:
            print(f'Draw {self.team1.team_name} {self.team2.team_name}')

    def process_results (self , result):
        if(result[1] == 'Shoot'):
            print('Ejecuto disparo')
            team_with_ball = None
            team = result[0].team
            if team == self.team1:
                self.points[0] += 1
                team_with_ball = self.team2
            else:
                self.points[1] += 1
                team_with_ball = self.team1
            self.set_players_to_original_positions(self.team1 , self.team2)
            self.initialize_attakers_positions(self.team1 , self.team2)
            self.select_initial_player_with_ball(team_with_ball)
        if(result[1] == 'Move'):
            action.Move.execute(result[0],result[2])
        if(result[1] == 'Pass'):
            action.Pass.execute(result[0], result[2])
        if(result[1] == 'Intercept'):
            action.Intercept.execute(result[0], result[2])
        if(result[1] == 'Entry'):
            action.Entry.execute(result[0] , result[2])
        if(result[1] == 'Defend' ):
            action.Tackle.execute(result[0], result[2])
        
        
    def get_best_solution(self , sol , variables):
        best = -1
        final_sol = None 
        for s in sol :
            sol_act , sol_prec = s.solution(variables)
            if(sol_prec > best):
                best = sol_prec
                final_sol = sol_act
        return final_sol.path()[1].action, best

    def move_player(self,x:int,y:int,player:Player, field:list[Zone]):
        zones = {}
        for i in field:
            for a in range(3):
                for b in range(3):
                    zones[(a,b)] = i
        player.current_position = zones[(x,y)]

    # TODO Refactor this function
    def choose_player_success(self, player_with_ball: Tuple[Player, Action], dicc: Dict[str, Player], adversaries: List[Tuple[Player, str]], pos_to_zone: Dict[Tuple[int, int], Zone]):
        all_players = [player_with_ball] + adversaries
        current_player, action = player_with_ball
        player_prob = current_player.attributes_score[action.name]
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
                        result = (x[0], x[1], current_player)
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
                        print('Disparo:', result)
                    else:
                        result = (x[0], x[1], current_player)
                    break
            
            return result
        elif action.name == 'Move':
            current_zone = current_player.current_position
            # print('current_zone_coords', current_zone.get_coords())
            # print('pos_to_zone', pos_to_zone )
            # print('mmm', current_zone.get_coords()+positions_arr[0])
            current_zone_coords = current_zone.get_coords()
            possible_coords_zones = [(current_zone_coords[0]+pos[0], current_zone_coords[1]+pos[1]) for pos in positions_arr if (current_zone_coords[0]+pos[0], current_zone_coords[1]+pos[1]) in pos_to_zone]
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

            # print('possible coords_zones', possible_coords_zones)
            target_index_coords_zone = np.random.choice([i for i in range(len(possible_coords_zones))], p=normalized_success_arr)
            target_coords_zone = possible_coords_zones[target_index_coords_zone]
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
                        result = (x[0], x[1], current_player)
                    break
            
            return result
            
      
    def move_player_in_team_with_ballposicion(self , player_with_ball : Player , team : Team):
        for player in team.players:
            if (player_with_ball.current_position.types == 'Attack' or player_with_ball.position.types == 'Midfield'):
                if(player.role == 'G'):
                    continue
                if(self.IsValid(player.current_position.row + 1)):
                    # player.position.row += 1
                    self.move_player(player.current_position.row+1,player.current_position.column,player,self.field.field)

    def move_player_in_team_without_ballposicion(self , player_with_ball : Player ,team : Team):
        actions = []
        for player in team.players:
            if(player.role == 'G'):
                actions.append((player,'Defend'))
            if(player.current_position == player_with_ball.current_position):  
                actions.append((player,'Entry'))
            elif(not player.current_position  == player.position):
                if(self.IsValid(player.current_position.row - 1)):
                    player.position.row += 1
                    actions.append((player,'Intercept'))
        return actions

    def select_initial_team_with_ball(self):
        return self.team1 if random.randint(0,1) == 0 else self.team2


    def select_initial_player_with_ball(self, team : Team):
        att = [player for player in team.players if player.role == 'F']
        return random.choice(att)

    def set_players_to_original_positions(self , firstTeam : Team , secondTeam : Team):
        for player in firstTeam.players:
            player.current_position = player.position
        for player in secondTeam.players:
            player.current_position = player.position


    def initialize_attakers_positions(self, firstTeam: Team, secondTeam: Team):
        for i in range(len(firstTeam.players)):
            if firstTeam.players[i].role == 'F':
                self.move_player(firstTeam.players[i].position.row-1,firstTeam.players[i].position.column,firstTeam.players[i],self.field.field)
                # firstTeam.players[i] = firstTeam.players[i].current_position.row - 1 

            if secondTeam.players[i].role == 'F':
                self.move_player(secondTeam.players[i].position.row-1,secondTeam.players[i].position.column,secondTeam.players[i],self.field.field)
                # secondTeam.players[i] = secondTeam.players[i].current_position.row - 1 

        return firstTeam, secondTeam
        
    def IsValid(self , row):
        if(row < 3):
            return True
        return False

    
    

    