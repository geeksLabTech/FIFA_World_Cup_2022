from group import Group
import json
class Tournament:

    def load_groups(self):
        
        data = {}
        with open("groups.json") as f:
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
        
        for group in groups:
            self.matches += group.get_matches()
   
    def run(self):
        pass