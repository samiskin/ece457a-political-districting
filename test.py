from numpy import *

import simulated_annealing 
import particle_swarm
import hill_climbing 

import csv

NUMBER_OF_RUNS = 2
DEBUG = False

# @list: headers
# @list of lists: data
# @string: file_name
def export_csv(data, file_name):
	with open(file_name, "wb") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows(data)

def format_algo_row_data(algo_name, report):
	row = [algo_name]
	for stat in report:
		for stat_value in stat:
			row.append(stat_value)
	return row

# @list: data
def calculate_stats_helper(data):
	if DEBUG:
		print "min:", amin(data)
		print "max:", amax(data)
		print "median:", median(data)
		print "stdev:", std(data)
	
	return [amin(data), amax(data), median(data), std(data)]

def calculate_stats(comp_list, pop_list, fitness_list, diff_sum):
	if DEBUG:
		print "COMP:"
		calculate_stats_helper(comp_list)
		print "POP EQ:"
		calculate_stats_helper(pop_list)
		print "FITNESS:" 
		calculate_stats_helper(fitness_list)
		print "AVG DIFF IN FITNESS:"
		print diff_sum/NUMBER_OF_RUNS

	return [calculate_stats_helper(comp_list), calculate_stats_helper(pop_list), calculate_stats_helper(fitness_list)]

def simulated_annealing_report(init_temp, cooling_rate, iterations_per_temp):
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

	return calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

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

	return calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

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

	return calculate_stats(comp_list, pop_list, fitness_list, diff_sum)

def main():
	report = []

	# generate headers
	criteria = ["Compactness", "Population Equality", "Fitness"]
	criteria_stats = ["min", "max", "median", "standard deviation"]

	header1 = [""]
	header2 = ["Algorithm"]
	for i in range(len(criteria)):
		for j in range(len(criteria_stats)):
			if j == 0:
				header1.append(criteria[i])
			else:
				header1.append("")
			header2.append(criteria_stats[j])
	report.append(header1)
	report.append(header2)

	# generate SA report
	report.append(format_algo_row_data("SA", simulated_annealing_report(10, 0.003, 2)))

	# generate PSO report
	report.append(format_algo_row_data("PSO", particle_swarm_report(1, 1, 1)))

	# generate hill climbing
	report.append(format_algo_row_data("Hill Climbing", particle_swarm_report(1, 1, 1)))

	# export the report to csv
	file_name = "test_%s_runs.csv" % (NUMBER_OF_RUNS)
	export_csv(report, file_name)

	# simulated_annealing_report(10, 0.003, 2)
	# particle_swarm_report(1, 1, 1)
	# hill_climbing_report()

if __name__ == '__main__':
    main()

