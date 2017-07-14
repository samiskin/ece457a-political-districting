from __future__ import print_function
from sets import Set
import copy
import math
import random


w = 8
h = 7
num_districts = 7

toXY = lambda i: (i % w, i / w)
toI = lambda x, y: y*w + x

#populations = [int(random.random()*100 + 1) for i in range(w*h)]
populations = [1 for i in range(w*h)]
areas = [1 for i in range(w*h)]

# A solution is a mapping from cell index to district number.  Since ids are all
# just 0, 1, 2, ... n, its stored as an array
# Ex: [ 5, 5, 7, 1, 1, 1 ] means units 0, 1 are in district 5, unit 2 is in
# district 7, and units 3, 4, 5 are all in district 1

# A border of a cell id is a tuple of (neighbor_id, border_length)

# A district is a Set of ids (integers)


def print_solution(solution):
    for y in range(h):
        for x in range(w):
            print('\033[{}m{:5}\033[0m'.format(solution[toI(x,y)] + 31, populations[toI(x,y)]), end='')
        print('\n')

def get_cell_borders(i):
    (x, y) = toXY(i)
    borders = Set()
    if (x > 0):
        borders.add((toI(x - 1, y), 1))
    if (x < w - 1):
        borders.add((toI(x + 1, y), 1))
    if (y > 0):
        borders.add((toI(x, y - 1), 1))
    if (y < h - 1):
        borders.add((toI(x, y + 1), 1))
    return borders

# Map of cell to set of (neighbor_id, border_length)s for each neighbor
borders = [get_cell_borders(i) for i in range(w*h)]

def get_perimeter(district):
    base = Set()
    perimeter = 0
    for i in district:
        for (neighbor, length) in borders[i]:
            if neighbor in base:
                perimeter -= length
            else:
                perimeter += length
        base.add(i)
    return perimeter

def get_area(cells):
    return reduce((lambda x, y: x + areas[y]), cells, 0)

# Array of sets, index is district, value is a set of cell ids for that district
def get_district_map(solution):
    districts = [ Set() for d in range(0, num_districts) ]
    for i, d in enumerate(solution):
        districts[d].add(i)
    return filter(lambda s: len(s) != 0, districts)

def get_population(district):
    return reduce(lambda x, y: x + populations[y], district, 0)


total_pop = reduce(lambda x, y: x + y, populations)
def fitness(solution):
    districts = get_district_map(solution)
    d_compact = lambda d: get_perimeter(d)**2 / float(get_area(d))
    d_pop = lambda d: abs(get_population(d) - (total_pop / float(num_districts)))
    return -reduce(lambda f, d: f + d_compact(d) + 2*d_pop(d), districts, 0)

# Determine neighbors by moving a cell from one district to another
# without causing any discontinuities
def solution_neighborhood(solution):
    districts = get_district_map(solution)
    neighborhood = []
    for (cell, district) in enumerate(solution):
        if len(districts[district]) == 1:
            continue
        if not is_contiguous_without_cell(districts[district], cell):
            continue
        for (border_cell, _) in borders[cell]:
            if border_cell not in districts[district]:
                # Swap cell to border_cell's district
                neighbor = copy.deepcopy(solution)
                neighbor[cell] = solution[border_cell]
                neighborhood.append(neighbor)
    return neighborhood

def is_contiguous_without_cell(district, cell_to_skip):
    cells_to_check = set(district)
    cells_to_check.remove(cell_to_skip)
    random_cell = cells_to_check.pop()
    def floodfill(cell):
        if cell == cell_to_skip:
            return
        for (neighbor, _) in borders[cell]:
            if neighbor in district:
                if neighbor in cells_to_check:
                    cells_to_check.remove(neighbor)
                    floodfill(neighbor)
    floodfill(random_cell)
    return len(cells_to_check) == 0;


    
# Set the initial solution to just rows.  Note that if the number of districts
# doesn't match the number of rows, this may not be a valid initial solution.
# You might want to figure out a better way to generate a random valid initial
# solution
initial_solution = [int(i / (math.ceil((float(w*h))/num_districts))) for i in range(w*h)]
initial_fitness = fitness(initial_solution)
cur_solution = initial_solution
cur_fitness = initial_fitness 
best_solution = cur_solution
best_fitness = cur_fitness
should_stop = False
print(cur_fitness)

# Simulated Annealing
max_iterations = 10000
initial_temperature = 10
cooling_rate = 0.013
temp_reduction = lambda temp: temp * (1 - cooling_rate)
stopping_condition = lambda: should_stop or cur_temperature < 1
iterations_per_temperature = 1

cur_temperature = initial_temperature

for iter in xrange(0, max_iterations):
    for i in xrange(0, iterations_per_temperature):
        neighborhood = solution_neighborhood(cur_solution)
        if len(neighborhood) == 0:
            should_stop = True
            break

        index = random.randint(0, len(neighborhood) - 1)
        neighbor = neighborhood[index]
        neighbor_fitness = fitness(neighbor)
        change_in_fitness = neighbor_fitness - cur_fitness
        if change_in_fitness > 0 or random.random() < math.exp(change_in_fitness / cur_temperature):
            cur_solution = neighbor
            cur_fitness = neighbor_fitness
            if neighbor_fitness > best_fitness:
                best_solution = neighbor
                best_fitness = neighbor_fitness
                print(best_fitness)

    cur_temperature = temp_reduction(cur_temperature)

    if stopping_condition():
        break


# # Hill Climbing
# for iter in xrange(0, max_iterations):
#     neighborhood = solution_neighborhood(cur_solution)
#     local_best = max(neighborhood, key=fitness)
#     local_best_fitness = fitness(best)
#     if local_best_fitness > cur_fitness:
#         cur_fitness = local_best_fitness 
#         cur_solution = local_best
#     else:
#         break
#     best_solution = cur_solution

print('\n\n')
print('-----  Initial (Cost: {})  -----'.format(-initial_fitness))
print_solution(initial_solution)
print('\n')
print('-----   Final (Cost: {})   -----'.format(-best_fitness))
print_solution(best_solution)
