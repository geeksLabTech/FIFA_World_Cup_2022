import tarski
from  game import Game
import tarski.fstrips as fs
from zone import Zone
from utils.node import Node

def build_model(game : Game , zonegoal : Zone):
    
    lang = tarski.fstrips.language("FIFA_World_Cup_2022")

    # Define the predicate
    ball_posecion = lang.predicate('ball_posecion', 'object', )    
    player_in_team = lang.predicate('player_in_team','object','object')
    position = lang.predicate('position','object','object')
    ball_in_goal = lang.predicate('ball_in_goal')
    problem = tarski.fstrips.create_fstrips_problem(domain_name="FIFA_World_Cup_2022",problem_name='Shoose_Action' ,language=lang) 

   

    for player in game.players:
        if(player.ballposition):
            init = tarski.model.create(lang)
            init.add(ball_posecion(player))
            init.add(position(player ,player.posicion))
            init.add(player_in_team(player,player.team))
            problem.init = init

            problem.goal = position(game.positionBall , zonegoal)
        continue

    


    #Define actions 

    x = lang.variable('x', 'object')
    y = lang.variable('y', 'object')
    z = lang.variable('z', 'object') 

    # Action 1
    move = problem.action('move', [x,y,z],
                        precondition = position(z,x),
                        effects = fs.AddEffect (position(z,y)))

    # Action 2
    shoot = problem.action('shoot', [z],
                        precondition = ball_posecion(z),
                        effects = fs.AddEffect(ball_in_goal()))

    # Action 3
    pass_ball = problem.action('pass_ball', [x,y,z],
                        precondition = ball_posecion(z) & player_in_team(z,x) & player_in_team(y,x),
                        effects = [fs.DelEffect(ball_posecion(z)),fs.AddEffect(ball_posecion(y))])
    
def build_planning_graph(problem , root : Node): # se llama con esta la primera vez root = Node(0,None,problem.init) 
    actions = []
    for action in problem.actions:
        if(float(root.name)%2 == 0):
            for precondition in action.precondition:
                if(precondition in problem.init):
                    actions.append(action)
        else:
            for effect in action.effects:
                if(effect in problem.init):
                    actions.append(action)
    root.children = Node(float(root.name + 1),None ,actions)



    


