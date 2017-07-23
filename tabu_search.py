import time
import math
import random

from grid_problem import *
from utils import *

def main():
	program_start = time.time()

	p = Problem()

	MAX_ITERATIONS = 10000
	TABU_TENURE = 5 #

	initial_solution = p.generate_initial_solution()
	cur_solution = initial_solution
	best_solution = cur_solution
	initial_fitness = fitness(p, cur_solution)
	best_fitness = initial_fitness

	print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
	print_solution(p, initial_solution)
	print('\n')

	# width: districts
	# height: geographical units
	tenure_table = [[0 for x in range(len(p.areas))] for y in range(p.num_districts)]

	while True: # UNTIL STOPPING CONDITION IS MET
		# generate the set of all feasible moves producing the corresponding
		# set of feasible solutions in the neighbourhood N(s) of the current
		# solution s
		changed_gus_to_neighborhood = solution_neighborhood_for_tabu(p, cur_solution)
		if len(changed_gus_to_neighborhood) == 0:
			break

		cur_fitness = fitness(p, cur_solution)
		did_cur_change = False 
		for cur_changed_cell_info, neighbor in changed_gus_to_neighborhood.iteritems():
			# look up if cell that was change is not tabu (i.e. tenure is 0)
			cell, old_district, new_district = cur_changed_cell_info
			tenure = tenure_table[new_district][cell]
			if tenure  > 0:
				continue

			# check if the fitness is better
			if fitness(p, neighbor) < cur_fitness:
				continue

			cur_fitness = fitness(p, neighbor)
			cur_solution = neighbor
			did_cur_change = True

		if not did_cur_change:
			break

		# update the best fitness
		best_fitness = cur_fitness
		best_solution = cur_solution

		# update tabu tenure list
		# decrease all other values by 1
		for x in range(p.num_districts):
			for y in range(len(p.areas)):
				tenure_table[x][y] = tenure_table[x][y] - 1
				if tenure_table[x][y] < 0:
					tenure_table[x][y] = 0

		# cell that was moved gets new tenure value
		tenure_table[cur_changed_cell_info[2]][cur_changed_cell_info[0]] = TABU_TENURE

	print('-----   Final (Cost: {})   -----'.format(-best_fitness))
	print_solution(p, best_solution)
	print('Time: {}s'.format(time.time() - program_start))

def test(tenure):
	program_start = time.time()

	p = Problem()

	MAX_ITERATIONS = 10000
	# TABU_TENURE = 5 #
	TABU_TENURE = tenure

	initial_solution = p.generate_initial_solution()
	cur_solution = initial_solution
	best_solution = cur_solution

	initial_fitness = fitness(p, cur_solution)
	best_fitness = initial_fitness

	initial_fitness_details = fitness_details(p, cur_solution)
	best_fitness_details = initial_fitness_details

	print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
	print_solution(p, initial_solution)
	print('\n')

	# width: districts
	# height: geographical units
	tenure_table = [[0 for x in range(len(p.areas))] for y in range(p.num_districts)]

	while True: # UNTIL STOPPING CONDITION IS MET
		# generate the set of all feasible moves producing the corresponding
		# set of feasible solutions in the neighbourhood N(s) of the current
		# solution s
		changed_gus_to_neighborhood = solution_neighborhood_for_tabu(p, cur_solution)
		if len(changed_gus_to_neighborhood) == 0:
			break

		cur_fitness = fitness(p, cur_solution)
		cur_fitness_details = fitness_details(p, cur_solution)

		did_cur_change = False 
		for cur_changed_cell_info, neighbor in changed_gus_to_neighborhood.iteritems():
			# look up if cell that was change is not tabu (i.e. tenure is 0)
			cell, old_district, new_district = cur_changed_cell_info
			tenure = tenure_table[new_district][cell]
			if tenure  > 0:
				continue

			# check if the fitness is better
			if fitness(p, neighbor) < cur_fitness:
				continue

			cur_fitness = fitness(p, neighbor)
			cur_fitness_details = fitness_details(p, neighbor)

			cur_solution = neighbor
			did_cur_change = True

		if not did_cur_change:
			break

		# update the best fitness
		best_fitness = cur_fitness
		best_fitness_details = cur_fitness_details
		best_solution = cur_solution

		# update tabu tenure list
		# decrease all other values by 1
		for x in range(p.num_districts):
			for y in range(len(p.areas)):
				tenure_table[x][y] = tenure_table[x][y] - 1
				if tenure_table[x][y] < 0:
					tenure_table[x][y] = 0

		# cell that was moved gets new tenure value
		tenure_table[cur_changed_cell_info[2]][cur_changed_cell_info[0]] = TABU_TENURE

	print('-----   Final (Cost: {})   -----'.format(-best_fitness))
	print_solution(p, best_solution)
	print('Time: {}s'.format(time.time() - program_start))

    # returns tuple of size 6: (initial compactness, intial population equality, initial overall fitness, best ....)
	return initial_fitness_details + best_fitness_details

if __name__ == "__main__":
    main()
