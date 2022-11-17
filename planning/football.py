from planning.planning import Action , PlanningProblem
from player import Player
from team import Team
def football_model(team:Team, player:Player):
    names = {'P': player}
    iter = 1
    for p in team.active_players:
        if p.name != player.name:
            names[f'P{iter}'] = p
            iter += 1
            
    return names,PlanningProblem(initial = 'BallPocesion(P) & Player(P) & Player(P1) & Player(P2) & Player(P3)  & Player(P4) & Player(P5) & Player(P6) & Player(P7) & Player(P8) & Player(P9) & Player(P10) ',
                            goals = 'BallInGoal()',
                            actions = [Action('Move(x,y,z)',
                                            precond = 'Position(z,x) ',
                                            effect = 'Position(z,y)',
                                            domain = 'Player(z) & Posicion(x) & Posicion(y)'),
                                        Action ('Shoot(z)',
                                            precond = 'BallPocesion(z)',
                                            effect = 'BallInGoal() & ~BallPocesion(z)',
                                            domain = 'Player(z)'),
                                        Action('Pass(x,y)',
                                            precond = 'BallPocesion(x) & Player(x) & Player(y)' ,
                                            effect = '~BallPocesion(x) & BallPocesion(y)',
                                            domain = 'Player(y) & Player(z)')],
                            domain = 'Player(P) & Player(P1) & Player(P2) & Player(P3) & Player(P4) & Player(P5) & Player(P6) & Player(P7) & Player(P8) & Player(P9) & Player(P10)')