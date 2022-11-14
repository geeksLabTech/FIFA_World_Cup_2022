from planning import Action , PlanningProblem

def football_model():
    return PlanningProblem(initial = 'BallPocesion(P) & PlayerInTeam(P,T) & PlayerInTeam(P1 ,T) & PlayerInTeam(P2,T) & PlayerInTeam(P3,T)  & PlayerInTeam(P4,T) & PlayerInTeam(P5,T) & PlayerInTeam(P6,T) & PlayerInTeam(P2,T) & PlayerInTeam(P7,T) & PlayerInTeam(P8,T) & PlayerInTeam(P9,T) & PlayerInTeam(P10,T) ',
                            goals = 'BallInGoal()',
                            actions = [Action('Move(x,y,z)',
                                            precond = 'Position(z,x) ',
                                            effect = 'Position(z,y)',
                                            domain = 'Player(z) & Posicion(x) & Posicion(y)'),
                                        Action ('Shoot(z)',
                                            precond = 'BallPocesion(z)',
                                            effect = 'BallInGoal() & ~BallPocesion(z)',
                                            domain = 'Player(z)'),
                                        Action('Pass(x,y,z)',
                                            precond = 'BallPocesion(z) & PlayerInTeam(z,x) & PlayerInTeam(y,x)' ,
                                            effect = '~BallPocesion(z) & BallPocesion(y)',
                                            domain = 'Player(y) & Player(z) & Team(z)')],
                            domain = 'Player(P) & Team(T) & Player(P1) & Player(P2) & Player(P3) & Player(P4) & Player(P5) & Player(P6) & Player(P7) & Player(P8) & Player(P9) & Player(P10)')