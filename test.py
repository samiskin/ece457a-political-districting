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
# @list: data
def calculate_stats(data):
	return (amin(data), amax(data), median(data), std(data))

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

	comp_stats = calculate_stats(comp_list)
	print "COMP:"
	print "min:", comp_stats[0]
	print "max:", comp_stats[1]
	print "median:", comp_stats[2]
	print "stdev:", comp_stats[3]

	pop_stats = calculate_stats(pop_list)
	print "POP EQ:"
	print "min:", pop_stats[0]
	print "max:", pop_stats[1]
	print "median:", pop_stats[2]
	print "stdev:", pop_stats[3]

	fitness_stats = calculate_stats(fitness_list)
	print "FITNESS:" 
	print "min:", fitness_stats[0]
	print "max:", fitness_stats[1]
	print "median:", fitness_stats[2]
	print "stdev:", fitness_stats[3]

	print "AVG DIFF IN FITNESS:"
	print diff_sum/NUMBER_OF_RUNS


def main():
	simulated_annealing_test()

if __name__ == '__main__':
    main()

