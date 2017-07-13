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

populations = [int(random.random()*100 + 1) for i in range(w*h)]
areas = [1 for i in range(w*h)]

# A solution is a mapping from cell index to district number
# This initial solution distributes districts evenly across rows
initial_solution = [int(i / (math.ceil((float(w*h))/num_districts))) for i in range(w*h)]

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

borders = [get_cell_borders(i) for i in range(w*h)]

def get_perimeter(cells): # district: list of indices
    base = Set()
    perimeter = 0
    for i in cells:
        for (neighbor, length) in borders[i]:
            if neighbor in base:
                perimeter -= length
            else:
                perimeter += length
        base.add(i)
    return perimeter

def get_area(cells):
    return reduce((lambda x, y: x + areas[y]), cells, 0)


# Map of district number -> set of cells
def get_district_map(solution):
    districts = [ Set() for d in range(0, num_districts + 1) ]
    for i, d in enumerate(solution):
        districts[d].add(i)
    return filter(lambda s: len(s) != 0, districts)

def get_population(district):
    return reduce(lambda x, y: x + populations[y], district, 0)


total_pop = reduce(lambda x, y: x + y, populations)
def district_fitness(d):
    compact = get_perimeter(d)**2 / float(get_area(d))
    pop = abs(get_population(d) - (total_pop / float(num_districts)))
    print('c: {}, p: {}, c + p: {}'.format(compact, pop, compact + pop))
    return compact + pop


def fitness(solution):
    districts = get_district_map(solution)
    d_compact = lambda d: get_perimeter(d)**2 / float(get_area(d))
    d_pop = lambda d: abs(get_population(d) - (total_pop / float(num_districts)))
    return -reduce(lambda f, d: f + d_compact(d) + d_pop(d), districts, 0)


# Converted from http://algs4.cs.princeton.edu/41graph/Bridge.java.html
def get_bridges(district):
    pre = {}
    low = {}
    for i in district:
        pre[i] = -1
        low[i] = -1

    count = {'val': 0} # Hack to let me use the global variable in dfs
    bridges = Set()
    def dfs(u, v): # edge e = (u, v)
        count['val'] += 1
        pre[v] = count['val']
        low[v] = pre[v]
        district_borders = filter(lambda w: w[0] in district, borders[v])
        neighbors = map(lambda w: w[0],  district_borders)
        for w in neighbors:
            if (pre[w] == -1):
                dfs(v, w)
                low[v] = min(low[v], low[w])
                if (low[w] == pre[w]):
                    bridges.add(v)
            elif w != u:
                low[v] = min(low[v], pre[w])

    for cell in district:
        dfs(cell, cell)

    return bridges

# Determine neighbors by moving a cell from one district to another
# without causing any discontinuities
def solution_neighborhood(solution):
    districts = get_district_map(solution)
    neighborhood = []
    for (cell, district) in enumerate(solution):
        if len(districts[district]) == 1:
            continue
        bridges = get_bridges(districts[district])
        if cell in bridges:
            continue
        for (border_cell, _) in borders[cell]:
            if border_cell not in districts[district]:
                neighbor = copy.deepcopy(solution)
                neighbor[cell] = solution[border_cell]
                neighborhood.append(neighbor)
    return neighborhood

cur_solution = initial_solution
cur_fitness = fitness(cur_solution)
while True:
    neighborhood = solution_neighborhood(cur_solution)
    best = max(neighborhood, key=fitness)
    best_fitness = fitness(best)
    if best_fitness > cur_fitness:
        cur_fitness = best_fitness
        cur_solution = best
    else:
        break

#print('----------------------------------------')
print('\n\n\n\n')
print_solution(initial_solution)
print('\n\n\n\n')
#print('----------------------------------------')
print_solution(cur_solution)
#print('----------------------------------------')

