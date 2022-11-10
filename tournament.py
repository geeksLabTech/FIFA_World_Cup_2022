from group import Group

class Tournament:

    def load_groups(self):
        return [Group("A",["team1","team2","team3","team4"])]

    def __init__(self) -> None:
        groups = self.load_groups()

        self.groups = groups
        self.matches = []
        
        for group in groups:
            self.matches += group.get_matches()
   
    def run(self):
        pass