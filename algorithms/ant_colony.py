
import numpy as np
from typing import Self
from game import Football
from team import Team
from constants import ZONES, FIELD
import pandas as pd
        


class PlayerNode:
    def __init__(self, player_name, player_dic, is_in_official_team: bool, initial_pheromone: float, is_start: bool):
        self.player_name = player_name
        self.player_attributes = player_dic
        self.pheromone = initial_pheromone
        self.visitants: list[int] = []
        self.is_in_official_team = is_in_official_team
        self.adjacent_nodes: list[Self] = []
        self.is_start = is_start


    def __str__(self):
        return self.player_name

    
class AntColony:
    def __init__(self, team_name, fixed_goalkeeper_dic, nodes: list[PlayerNode], target_to_optimize, target_oponent: Team, initial_pheromone: float, evaporation_rate: float, alpha: float = 1, beta: float = 0.5, delta_tau: float = 2, Q=1):
        self.team_name = team_name
        self.fixed_goalkeeper_dic = fixed_goalkeeper_dic
        self.target_oponent = target_oponent
        self.nodes = nodes
        self.target_to_optimize = target_to_optimize
        self.initial_pheromone = initial_pheromone
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        self.Q = Q

        
        # A solution is a tuple with (path, total_distance)
        self.good_solutions = []


    def run(self, iterations: int):
        
        for i in range(iterations):
            print(f'Start Iteration {i}')
            for node in self.nodes:
                node.visitants = []

            solutions_from_ants = self.__run_ants()
            assert len(solutions_from_ants) == 2, "Not enough solutions"
            # A result is the mean of goals difference of the games simulated
            results = [self.__simulate_solution(solution[0]) for solution in solutions_from_ants]
            self.__evaporate_pheromone()

            for i in range(len(results)):
                if results[i][0] > self.target_to_optimize:
                    self.good_solutions.append((results[i][1], results[i][0]))
                    self.__update_pheromone(solutions_from_ants[i][0], solutions_from_ants[i][1])

        if len(self.good_solutions) == 0:
            return "No good solutions found"
            
        best_solution = max(self.good_solutions, key=lambda x: x[1])
        return best_solution

    def __run_ants(self, ants=2):
        probabilities = [self.__calculate_pheromone(node) * self.__calculate_heuristic(node, 0) for node in self.nodes]
        p = np.array(probabilities)
        p /= p.sum()
        assert len(self.nodes) > 0, "No nodes"
        random_start_nodes: list[int] = list(np.random.choice([i for i in range(len(self.nodes))], size=ants, p=p, replace=False))
        solutions_from_ants = []
        for index in random_start_nodes:
            if ants == 0:
                break
            path, distance = self.__run_ant_from_node(self.nodes[index], ant_id=ants, path=[])
            solutions_from_ants.append((path, distance))
            print("Ant finished")
            ants-=1
        
        return solutions_from_ants


    def __run_ant_from_node(self, node: PlayerNode, ant_id, distance: int=0, visited_nodes: int = 0, path: list[PlayerNode] = []):
        visited_nodes += 1
        node.visitants.append(ant_id)
        # print(f'path with visited_nodes {visited_nodes}, and total nodes {len(path)}')
        path.append(node)

        if not node.is_in_official_team:
            distance+=1

        if visited_nodes == 10:
            # print('path', len(path))
            return path, distance
           

        next_node = self.__select_next_node(node, ant_id, distance)

        return self.__run_ant_from_node(next_node, ant_id, distance, visited_nodes, path)


    def __select_next_node(self, node: PlayerNode, ant_id, current_distance: int):
        valid_adjacent_nodes = [x for x in node.adjacent_nodes if ant_id not in x.visitants]

        assert len(valid_adjacent_nodes) > 0, "No valid adjacent nodes"

        probabilities = [self.__calculate_pheromone(node) * self.__calculate_heuristic(node, current_distance) for node in valid_adjacent_nodes]
        # Normalize:
        p = np.array(probabilities)
        p /= p.sum()
        selected_node_index = np.random.choice(len(valid_adjacent_nodes), p=p, replace=False)
        return valid_adjacent_nodes[selected_node_index]


    def __calculate_pheromone(self, node: PlayerNode):
        return node.pheromone ** self.alpha


    def __calculate_heuristic(self, node: PlayerNode, current_distance: int):
        if not node.is_in_official_team:
            current_distance+=1
        if current_distance == 0:
            return 1
        return (1 / current_distance) ** self.beta

    
    def __evaporate_pheromone(self):
        for node in self.nodes:
            node.pheromone *= (1 - self.evaporation_rate)


    def __update_pheromone(self, path: list[PlayerNode], total_distance: int):
        for node in path:
            node.pheromone += self.Q / total_distance
        
    

    def __build_lineup(self, solution: list[PlayerNode]):
        # print('solution', len(solution))
        players = [(x.player_name, x.player_attributes) for x in solution]
        # print('goalkeeper_dic', self.fixed_goalkeeper_dic)
        lineup = {
            'goalkeeper': self.fixed_goalkeeper_dic,
            'att': [],
            'def': [],
            'mid': [],
        }
        for player in players:
            # print('player', player[0])
            player_name = player[0]
            if player[1][player_name]['position'] == 'F':
                lineup['att'].append(player[0])
            elif player[1][player_name]['position'] == 'D':
                lineup['def'].append(player[0])
            elif player[1][player_name]['position'] == 'M':
                lineup['mid'].append(player[0])

        return lineup


    def __simulate_solution(self, solution: list[PlayerNode]):
        lineup = self.__build_lineup(solution)
        # for x in lineup:
        #     print('lineup', x, len(lineup[x]))
        new_team = Team(self.team_name, FIELD.field, lineup)

        result = self.__run_matches(new_team, self.target_oponent)
        return result, lineup


    def __run_matches(self, new_team: Team, oponent_team: Team, iterations=30):
        # df = pd.DataFrame(columns=['Team1', 'Team2', 'Wins1', "Wins2"])
        
        results = {
            new_team.team_name: 0,
            oponent_team.team_name: 0
        }

        def function_x():
            game = Football(new_team, oponent_team, FIELD, 90)
            x = game.play()
            if x is not None:
                if type(x) is not tuple:
                    
                    results[x.team_name] += 1
            
        for _ in range(iterations):
            function_x()
            
        # df = df.append({'Team1': new_team.team_name, 'Team2': oponent_team.team_name, 'Wins1': results[new_team.team_name], 'Wins2': results[oponent_team.team_name]}, ignore_index=True)
        # print(df)
        print('finished microsimulation')
        print(f'Team1: {new_team.team_name}, Team2: {oponent_team.team_name}, Wins1: {results[new_team.team_name]}, Wins2: {results[oponent_team.team_name]}')
        return results[new_team.team_name] - results[oponent_team.team_name]

# to normalize probs
# >>> p = np.array(p)
# >>> p /= p.sum() 


