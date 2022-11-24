from multiprocessing import Pool
from time import sleep
import pandas as pd
from typing import List, Tuple
from team import Team
from game import Football
from field import Field
from team import Team

import json
from group import Group


class Tournament:

    def load_groups(self):
        
        data = {}
        with open("groups.json", 'r') as f:
            # load json file
            data = json.load(f)

        groups = []
        for g in data.keys():
            teams = data[g]
            groups.append(Group(g,teams))
            
        return groups

    def __init__(self) -> None:
        groups = self.load_groups()
        self.groups = groups
        self.group_winners = []
        self.teams_8th = []
        self.teams_4th = []
        self.matches = []
        self.teams = []


    def play_match_group(self,match,g):
        zones = [
        "Defense Left",
        "Defense Center",
        "Defense Right",

        "Midfield Left",
        "Midfield Center",
        "Midfield Right",

        "Attack Left",
        "Attack Center",
        "Attack Right"
        ]
        field = Field("f1", 3, 3, zones)
        
        team1 = Team(match[0], field.field)
        team2 = Team(match[1], field.field)

        Pros = []
        match = {
            team1.team_name: 0,
            team2.team_name: 0
        }

        game = Football(team1, team2, field, 90)
        result = game.play()
        if type(result) is tuple:
            g.Tie(result[0])
            g.Tie(result[1])
        else:
            g.Winner(result)

    def play_game(self, match):
        zones = [
        "Defense Left",
        "Defense Center",
        "Defense Right",

        "Midfield Left",
        "Midfield Center",
        "Midfield Right",

        "Attack Left",
        "Attack Center",
        "Attack Right"
        ]
        field = Field("f1", 3, 3, zones)
        
        team1 = Team(match[0], field.field)
        team2 = Team(match[1], field.field)

        Pros = []
        match = {
            team1.team_name: 0,
            team2.team_name: 0
        }

        game = Football(team1, team2, field, 90)
        result = game.play()
        if type(result) is tuple:
            return result[0]
        else:
            return self.play_game(match)

    def run_group_games(self, group:Group):
        matches = group.get_matches() 
        while len(matches) > 0:
            match = matches.pop()
            # p.map(self.play_match_group, [match,group])
            # p.apply_async(self.play_match_group, args=(match,group))
            self.play_match_group(match,group)
            
        return group.get_groups_classifications()
    
    def run_games(self, matches):
        teams = []
        with Pool(12) as p:
            teams.append(p.map(self.play_game, matches))
                # teams.append(self.play_game(match))
            # p.join()
        return teams
    
    def run(self):
        
        print("Starting tournament")
        # for group in self.groups:
        with Pool(12) as p:
            self.group_winners.append(p.map(self.run_group_games, self.groups))
            # p.join()
                # self.group_winners.append(self.run_group_games(group))

        # 8th Finals
        self.matches = [
                        (self.group_winners[0][0], self.group_winners[1][1]), # 49
                        (self.group_winners[2][0], self.group_winners[3][1]), # 50
                        (self.group_winners[1][0], self.group_winners[0][1]), # 51
                        (self.group_winners[3][0], self.group_winners[2][1]), # 52
                        
                        (self.group_winners[4][0], self.group_winners[5][1]), # 53
                        (self.group_winners[6][0], self.group_winners[7][1]), # 54
                        (self.group_winners[5][0], self.group_winners[4][1]), # 55
                        (self.group_winners[7][0], self.group_winners[6][1])] # 56
        
        self.teams_8th = self.run_games(self.matches)
        
        # Quarter Finals
        
        self.matches = [
            (self.teams_8th[0],self.teams_8th[1]),
            (self.teams_8th[2],self.teams_8th[3]),
            (self.teams_8th[4],self.teams_8th[5]),
            (self.teams_8th[6],self.teams_8th[7]),
        ] 
        
        self.teams_4th = self.run_games(self.matches)

        # Semi Finals
        self.matches = [
            (self.teams_4th[0],self.teams_4th[1]),
            (self.teams_4th[2],self.teams_4th[3])
        ]
        
        final_teams = self.run_games(self.matches)
        # get difference between self.teams and final_teams
        third_place = list(set(self.teams) - set(final_teams))
        
        # Final
        winner = self.play_game((final_teams[0],final_teams[1]))
        third = self.play_game((third_place[0],third_place[1]))
        
        
        print("Classified teams", self.group_winners)
        print("4th Finals teams", self.teams_8th)
        print("4th Finals teams", self.teams_4th)
        
        print("Third Place: ",third)    
        print("Second Place: ", list(set(final_teams) - set([winner]))[0])
        print("Winner: ",winner)
        