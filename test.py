from numpy import *

import simulated_annealing 
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

def simulated_annealing_test():
	comp_list = []
	pop_list = []
	fitness_list = []
	diff_sum = 0

	for _ in range(NUMBER_OF_RUNS):
		sa_init_comp, sa_init_pop, sa_init_fitness, sa_best_comp, sa_best_pop, sa_best_fitness = simulated_annealing.test(10, 0.003, 2)

		comp_list.append(sa_best_comp)
		pop_list.append(sa_best_pop)
		fitness_list.append(sa_best_fitness)
		diff_sum += sa_best_fitness - sa_init_fitness

	print "COMP:"
	print "min:", amin(comp_list)
	print "max:", amax(comp_list)
	print "median:", median(comp_list)
	print "stdev:", std(comp_list)

	print "POP EQ:"
	print "min:", amin(pop_list)
	print "max:", amax(pop_list)
	print "median:", median(pop_list)
	print "stdev:", std(pop_list)

	print "FITNESS:" 
	print "min:", amin(fitness_list)
	print "max:", amax(fitness_list)
	print "median:", median(fitness_list)
	print "stdev:", std(fitness_list)

	print "AVG DIFF IN FITNESS:"
	print diff_sum/NUMBER_OF_RUNS

simulated_annealing_test()

