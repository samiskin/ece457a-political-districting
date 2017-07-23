import simulated_annealing 
import csv

# @list: headers
# @list of lists: data
# @string: file_name
def export_csv(headers, data, file_name):
	with open(file_name, "wb") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows([headers])
	    writer.writerows(data)

simulated_annealing.test(10, 0.003, 2)
