from __future__ import print_function
import math

W = 8
H = 7
NUM_DISTRICTS = 7

toXY = lambda i: (i % W, i / W)
toI = lambda x, y: y*W + x

def print_solution(p, solution):
    for y in range(H):
        for x in range(W):
            print('\033[{}m{:5}\033[0m'.format(solution[toI(x,y)] + 31, p.populations[toI(x,y)]), end='')
        print('\n')

def get_cell_borders(i):
    (x, y) = toXY(i)
    borders = set([])
    if (x > 0):
        borders.add((toI(x - 1, y), 1))
    if (x < W - 1):
        borders.add((toI(x + 1, y), 1))
    if (y > 0):
        borders.add((toI(x, y - 1), 1))
    if (y < H - 1):
        borders.add((toI(x, y + 1), 1))
    return borders

class GridProblem:
    def __init__(self):
        #populations = [int(random.random()*100 + 1) for i in range(w*h)]
        self.populations = [1 for i in range(W*H)]
        self.areas = [1 for i in range(W*H)]
        self.borders = [get_cell_borders(i) for i in range(W*H)]
        self.num_districts = NUM_DISTRICTS
        self.total_population = reduce(lambda x, y: x + y, self.populations)

    
    def generate_initial_solution(self):
        # Set the initial solution to just rows.  Note that if the number of districts
        # doesn't match the number of rows, this may not be a valid initial solution.
        return [int(i / (math.ceil((float(W*H))/self.num_districts))) for i in range(W*H)]

