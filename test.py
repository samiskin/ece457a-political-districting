from numpy import *

import simulated_annealing 
import particle_swarm
import hill_climbing 
import tabu_search

import csv

NUMBER_OF_RUNS = 2

# @list: headers
# @list of lists: data
# @string: file_name
def export_csv(headers, data, file_name):
	with open(file_name, "wb") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows([headers])
	    writer.writerows(data)
# @list: data
def calculate_stats_helper(data):
	print "min:", amin(data)
	print "max:", amax(data)
	print "median:", median(data)
	print "stdev:", std(data)
	return (amin(data), amax(data), median(data), std(data))

def calculate_stats(comp_list, pop_list, fitness_list, diff_sum):
	print "COMP:"
	calculate_stats_helper(comp_list)
	print "POP EQ:"
	calculate_stats_helper(pop_list)
	print "FITNESS:" 
	calculate_stats_helper(fitness_list)
	print "AVG DIFF IN FITNESS:"
	print diff_sum/NUMBER_OF_RUNS

def simulated_annealing_test(init_temp, cooling_rate, iterations_per_temp):
	comp_list = []
	pop_list = []
	fitness_list = []
	diff_sum = 0

	for _ in range(NUMBER_OF_RUNS):
		sa_init_comp, sa_init_pop, sa_init_fitness, sa_best_comp, sa_best_pop, sa_best_fitness = simulated_annealing.test(init_temp, cooling_rate, iterations_per_temp)

		comp_list.append(sa_best_comp)
		pop_list.append(sa_best_pop)
		fitness_list.append(sa_best_fitness)
		diff_sum += sa_best_fitness - sa_init_fitness

	calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

def particle_swarm_report(c1, c2, c3):
	comp_list = []
	pop_list = []
	fitness_list = []
	diff_sum = 0

	for _ in range(NUMBER_OF_RUNS):
		init_comp, init_pop, init_fitness, best_comp, best_pop, best_fitness = particle_swarm.test(c1, c2, c3)
				
		comp_list.append(best_comp)
		pop_list.append(best_pop)
		fitness_list.append(best_fitness)
		diff_sum += init_fitness - best_fitness

	calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

def hill_climbing_report():
	comp_list = []
	pop_list = []
	fitness_list = []
	diff_sum = 0

	for _ in range(NUMBER_OF_RUNS):
		init_comp, init_pop, init_fitness, best_comp, best_pop, best_fitness = hill_climbing.test()
				
		comp_list.append(best_comp)
		pop_list.append(best_pop)
		fitness_list.append(best_fitness)
		diff_sum += init_fitness - best_fitness

	calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

def tabu_search_report(tenure):
	comp_list = []
	pop_list = []
	fitness_list = []
	diff_sum = 0

	for _ in range(NUMBER_OF_RUNS):
		init_comp, init_pop, init_fitness, best_comp, best_pop, best_fitness = tabu_search.test(tenure)
				
		comp_list.append(best_comp)
		pop_list.append(best_pop)
		fitness_list.append(best_fitness)
		diff_sum += init_fitness - best_fitness

	calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

def main():
	# simulated_annealing_test(10, 0.003, 2)
	# particle_swarm_report(1, 1, 1)
	# hill_climbing_report()
	tabu_search_report(5)
	
if __name__ == '__main__':
    main()

