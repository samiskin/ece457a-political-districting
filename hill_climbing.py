import time

# from grid_problem import *
from iowa_problem import *

from utils import *

program_start = time.time()

p = Problem()

MAX_ITERATIONS = 10000

def main(): 
	initial_solution = p.generate_initial_solution()
	initial_fitness = fitness(p, initial_solution)
	cur_solution = initial_solution
	cur_fitness = initial_fitness

	print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
	print_solution(p, initial_solution)
	print('\n')

	for iter in xrange(0, MAX_ITERATIONS):
	    neighborhood = solution_neighborhood(p, cur_solution)
	    local_best = max(neighborhood, key=lambda sol: fitness(p, sol))
	    local_best_fitness = fitness(p, local_best)
	    if local_best_fitness > cur_fitness:
	        cur_fitness = local_best_fitness
	        cur_solution = local_best
	    else:
	        break

	print('-----   Final (Cost: {})   -----'.format(-cur_fitness))
	print_solution(p, cur_solution)
	print('Time: {}s'.format(time.time() - program_start))

def test(): 
	initial_solution = p.generate_initial_solution()
	
	initial_fitness = fitness(p, initial_solution)
	initial_fitness_details = fitness_details(p, initial_solution)
	
	cur_solution = initial_solution
	
	cur_fitness = initial_fitness
	cur_fitness_details = initial_fitness_details

	print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
	print_solution(p, initial_solution)
	print('\n')

	for iter in xrange(0, MAX_ITERATIONS):
	    neighborhood = solution_neighborhood(p, cur_solution)
	    local_best = max(neighborhood, key=lambda sol: fitness(p, sol))
	    local_best_fitness = fitness(p, local_best)
	    local_best_fitness_details = fitness_details(p, local_best)
	    if local_best_fitness > cur_fitness:
	        cur_fitness = local_best_fitness
	        cur_fitness_details = local_best_fitness_details
	        cur_solution = local_best
	    else:
	        break

	print('-----   Final (Cost: {})   -----'.format(-cur_fitness))
	print_solution(p, cur_solution)
	print('Time: {}s'.format(time.time() - program_start))

	return initial_fitness_details + cur_fitness_details

if __name__ == "__main__":
    main()
