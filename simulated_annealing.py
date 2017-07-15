import time
import copy
import math
import random

from grid_problem import *
from utils import *

program_start = time.time()

p = GridProblem()

MAX_ITERATIONS = 10000
INITIAL_TEMPERATURE = 10
COOLING_RATE = 0.013
ITERATIONS_PER_TEMPERATURE = 1

cur_temperature = INITIAL_TEMPERATURE
temp_reduction = lambda temp: temp * (1 - COOLING_RATE)
stopping_condition = lambda: should_stop or cur_temperature < 1

initial_solution = p.generate_initial_solution()
initial_fitness = fitness(p, initial_solution)
cur_solution = initial_solution
cur_fitness = initial_fitness 
best_solution = cur_solution
best_fitness = cur_fitness
should_stop = False

print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
print_solution(p, initial_solution)
print('\n')

for _ in xrange(0, MAX_ITERATIONS):
    for i in xrange(0, ITERATIONS_PER_TEMPERATURE):
        neighborhood = solution_neighborhood(p, cur_solution)
        if len(neighborhood) == 0:
            should_stop = True
            break

        index = random.randint(0, len(neighborhood) - 1)
        neighbor = neighborhood[index]
        neighbor_fitness = fitness(p, neighbor)
        change_in_fitness = neighbor_fitness - cur_fitness
        if change_in_fitness > 0 or random.random() < math.exp(change_in_fitness / cur_temperature):
            cur_solution = neighbor
            cur_fitness = neighbor_fitness
            if neighbor_fitness > best_fitness:
                best_solution = neighbor
                best_fitness = neighbor_fitness
                # print(best_fitness)

    cur_temperature = temp_reduction(cur_temperature)

    if stopping_condition():
        break

print('-----   Final (Cost: {})   -----'.format(-best_fitness))
print_solution(p, best_solution)
print('Time: {}s'.format(time.time() - program_start))
