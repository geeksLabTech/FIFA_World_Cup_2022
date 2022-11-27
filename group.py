import random
from team import Team

class Group:
    def __init__(self,name,teams):
        self.name = name
        self.teams = teams
        self.scores = { team : 0 for team in self.teams}
        
    def get_matches(self):
        matches = []
        for n,t in enumerate(self.teams):
            for m,t2 in enumerate(self.teams):
                if m <= n:
                    continue
                matches.append((t,t2))
        return matches
    
    def Tie(self,team: Team):
        self.scores[team.team_name] += 1
    
    def Winner(self,team: Team):
        self.scores[team.team_name] += 3
        
    def get_groups_classifications(self):
        a = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:2]
        return [i[0] for i in a]