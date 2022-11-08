import random
import math
import copy
import sys

# based on https://www.geeksforgeeks.org/implementation-of-particle-swarm-optimization/

# TODO Modify this to use values from the player stats for velocity and position
class Particle:
    def __init__(self, fitness, dim, minx, maxx, seed):
        self.rnd = random.Random(seed)
        
        # all coordinates start at 0.0 in the initial step
        self.position = [0.0 for i in range(dim)]
        self.velocity = [0.0 for i in range(dim)]
        
        # in the beginning, the best position is the initial position
        self.best_part_pos = [0.0 for i in range(dim)]
        
        # generate random values for position and velocity vectors
        for i in range(dim):
            self.position[i] = (maxx - minx) * self.rnd.random() + minx
            self.velocity[i] = (maxx - minx) * self.rnd.random() + minx
        
        # eval curr fitness
        self.fitness = fitness(self.position)
        
        self.best_part_pos = copy.copy(self.position)
        self.best_part_pos_fit_val = self.fitness
    
def particle_swarm_optimization(fitness, max_iter, n, dim, minx, maxx):
    # inertia
    w = 0.720
    # cognitive
    c1 = 1.49445
    # social
    c2 = 1.49445

    rnd = random.Random(0)

    swarm = swarm = [Particle(fitness, dim, minx, maxx, i) for i in range(n)]
    
    best_swarm_pos = [0.0 for i in range(dim)]
    best_swarm_pos_fit_val = sys.float_info.max
    
    for i in range(n):
        if swarm[i].fitness < best_swarm_pos_fit_val:
            best_swarm_pos = copy.copy(swarm[i].position)
            best_swarm_pos_fit_val = swarm[i].fitness
    
    # optimization loop
    iter = 0
    while iter < max_iter:
        if iter % 10 == 0 and iter > 1:
            print("iteration: ", iter, " best fitness: %.3f" % best_swarm_pos_fit_val)

        for i in range(n):
            for k in range(dim):
                r1 = rnd.random()
                r2 = rnd.random()

                swarm[i].velocity[k] = (
                    w * swarm[i].velocity[k] + 
                    (c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].position[k])) +
                    (c2 * r2 * (best_swarm_pos[k] - swarm[i].position[k]))
                )
                # make values inside minx and maxx
                swarm[i].velocity[k] = min(swarm[i].velocity[k], maxx)
                swarm[i].velocity[k] = max(swarm[i].velocity[k], minx)

            for k in range(dim):
                swarm[i].position[k] += swarm[i].velocity[k]

            swarm[i].fitness = fitness(swarm[i].position)

            # update particle's best position
            if swarm[i].fitness < swarm[i].best_part_pos_fit_val:
                swarm[i].best_part_pos = copy.copy(swarm[i].position)
                swarm[i].best_part_pos_fit_val = swarm[i].fitness

            # updte swarm's best position
            if swarm[i].fitness < best_swarm_pos_fit_val:
                best_swarm_pos = copy.copy(swarm[i].position)
                best_swarm_pos_fit_val = swarm[i].fitness
                
        iter += 1
    return best_swarm_pos, best_swarm_pos_fit_val