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