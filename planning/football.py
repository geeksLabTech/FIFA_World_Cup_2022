from planning import Action , PlanningProblem

def football_model():
    return PlanningProblem(initial = 'BallPocesion(P) & PlayerInTeam(P,T)',
                            goals = 'Postion(B, ZG)',
                            actions = [Action('Move(x,y,z)',
                                            precond = 'Position(z,x) ',
                                            effect = 'Position(z,y)',
                                            domain = 'PLayer(z) & Posicion(x) & Posicion(y)' ),
                                        Action ('Shoot(z)',
                                            precond = 'BallPocesion(z)',
                                            effect = 'BallInGoal() & ~BallPocesio(z)',
                                            domain = 'Player(z)'),
                                        Action('Pass(x,y,z)',
                                            precond = 'BallPocesion(z) & PlayerInTeam(z,x) & PlayerInTeam(y,x)' ,
                                            effect = '~BallPocesion(z) & BallPocesio(y)',
                                            domain = 'Player(y) & Player(z) & Team(z)')],
                            domain = 'Player(P) & Team(T)')