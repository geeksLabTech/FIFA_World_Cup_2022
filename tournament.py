import json
import random

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
        self.matches = []
        self.teams = []
        

    def play(self,match):
        return match[random.randint(0,1)]

    def run_games(self, matches):
        teams = []
        
        while len(matches) > 0:
            match = matches.pop()
            teams.append(self.play(match))
        
        return teams
    def run(self):
        
        for group in self.groups:
            group.play_matches()

        # 8th Finals
        self.matches = [
                        (self.groups[0].teams[0], self.groups[1].teams[1]), # 49
                        (self.groups[2].teams[0], self.groups[3].teams[1]), # 50
                        (self.groups[1].teams[0], self.groups[0].teams[1]), # 51
                        (self.groups[3].teams[0], self.groups[2].teams[1]), # 52
                        
                        (self.groups[4].teams[0], self.groups[5].teams[1]), # 53
                        (self.groups[6].teams[0], self.groups[7].teams[1]), # 54
                        (self.groups[5].teams[0], self.groups[4].teams[1]), # 55
                        (self.groups[7].teams[0], self.groups[6].teams[1])] # 56
        
        self.teams = self.run_games(self.matches)
        
        # Quarter Finals
        
        self.matches = [
            (self.teams[0],self.teams[1]),
            (self.teams[2],self.teams[3]),
            (self.teams[4],self.teams[5]),
            (self.teams[6],self.teams[7]),
        ] 
        
        self.teams = self.run_games(self.matches)

        # Semi Finals
        self.matches = [
            (self.teams[0],self.teams[1]),
            (self.teams[2],self.teams[3])
        ]
        
        final_teams = self.run_games(self.matches)
        # get difference between self.teams and final_teams
        third_place = list(set(self.teams) - set(final_teams))
        
        # Final
        winner = self.play((final_teams[0],final_teams[1]))
        third = self.play((third_place[0],third_place[1]))
        
        print("Winner: ",winner)
        print("Second Place: ", list(set(final_teams) - set([winner]))[0])
        print("Third Place: ",third)    