import numpy as np
import random


def initialize_population(actions : list):
    path_list = []
    i = 0
    while i < 1000:
        j = 0
        path_current = []
        while j < 5:
            position = random.randint(0,3)
            path_current.append(position)
            j+=1
        path_list.append(path_current)
        i+=1


def evaluate(path_list : list):
    return #TODO misma funcion de evauluacion 

# get the top 500 paths
def get_bet_path(dictionary: dict):
    best_path = []
    dict(sorted(dictionary.items()))
    
    for i in range(1000,500,-1):
        best_path.append(dictionary[i])
    return best_path


def crossover(path_list : list):
    new_path_list = []
    for i in range(500):
        for j in range(500):
            if i != j:
                new_path = []
                for k in range(5):
                    if k < 3:
                        new_path.append(path_list[i][k])
                    else:
                        new_path.append(path_list[j][k])
                new_path_list.append(new_path)
    return new_path_list


def mutation(path_list : list , actions : list):
    new_path_list = []
    for i in range(1000):
        new_path = []
        ismutation = np.random.choice([0,1], p=[0.9,0.1])
        if ismutation == 1:
            position = random.randint(0,4)
            new_path = path_list[i]
            action = random.randint(0,3)
            new_path[position] = actions[action]
            new_path_list.append(new_path)
        else:
            new_path_list.append(path_list[i])
    return new_path_list

def execute_metaheristic():
    i = 0
    actions = ['move', 'pass' , 'shoot']
    list_path =initialize_population(actions)
    while i < 500:
        dictionary = evaluate(list_path)
        list_path = get_bet_path(dictionary)
        list_path = crossover(list_path)
        list_path = mutation(list_path,actions)
    return list_path[len(list_path)-1]
        



