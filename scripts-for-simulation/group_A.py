from multiprocessing import Process
from time import sleep
import pandas as pd
from typing import List, Tuple
from team import Team
from game import Football
from field import Field
from team import Team
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


def run_group_matches(matches: List[Tuple[str, str]], group_name: str, field, iterations=30):
    df = pd.DataFrame(columns=['Team1', 'Team2', 'Wins1', "Wins2"])
    for t1,t2 in matches:
        team1 = Team(t2, field.field)
        team2 = Team(t1, field.field)

        Pros = []
        match = {
            team1.team_name: 0,
            team2.team_name: 0
        }

        def function_x():
            game = Football(team1, team2, field, 90)
            x = game.play()
            if x is not None:
                match[x.team_name] += 1
        
        for i in range(iterations):
            function_x()
        
        df = df.append({'Team1': team1.team_name, 'Team2': team2.team_name, 'Wins1': match[team1.team_name], 'Wins2': match[team2.team_name]}, ignore_index=True)
        print(df)
    df.to_csv(f'{group_name}.csv')

group_A = [('qatar', 'ecuador'), ('qatar', 'senegal'), ('qatar', 'netherlands'), ('ecuador', 'senegal'), ('ecuador', 'netherlands'), ('senegal', 'netherlands')]


run_group_matches(group_A, 'group_A', field)