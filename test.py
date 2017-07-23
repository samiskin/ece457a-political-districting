from numpy import *

import simulated_annealing 
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

def simulated_annealing_report():
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

	# generate simulated annealing report
	sa_report = simulated_annealing_report()
	sa_row = ["Simulated Annealing"]
	for stat in sa_report:
		for stat_value in stat:
			sa_row.append(stat_value)
	report.append(sa_row)

	# export the report to csv
	print report
	file_name = "test_%s_runs.csv" % (NUMBER_OF_RUNS)
	export_csv(report, file_name)

if __name__ == '__main__':
    main()

