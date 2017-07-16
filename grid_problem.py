from __future__ import print_function
import math
import random
import r_centers

W = 6
H = 6
NUM_DISTRICTS = 4

FONT_COLORS = [ 31, 32, 33, 34, 35, 36, 37, 90 ]
FILL_COLORS = [ 7, 40, 41, 42, 44, 45, 46, 47, 100, 101, 103, 104, 105 ]

# COLORS = FONT_COLORS + FILL_COLORS
COLORS = FONT_COLORS

toXY = lambda i: (i % W, i / W)
toI = lambda x, y: y*W + x

def print_solution(p, solution):
    for y in range(H):
        for x in range(W):
            print('\033[{}m{:5}\033[0m'.format(COLORS[solution[toI(x,y)]], p.populations[toI(x,y)]), end='')
        print('\n')

def print_centers(p, centers):
    for y in range(H):
        for x in range(W):
            if toI(x,y) in centers:
                print('\033[{}m{:5}\033[0m'.format(31, p.populations[toI(x,y)]), end='')
            else:
                print('\033[{}m{:5}\033[0m'.format(37, p.populations[toI(x,y)]), end='')
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
        # self.populations = [int(random.random()*100 + 1) for i in range(W * H)]
        self.populations = [1 for i in range(W*H)]
        self.areas = [1 for i in range(W*H)]
        self.borders = [get_cell_borders(i) for i in range(W*H)]
        self.num_districts = NUM_DISTRICTS
        self.total_population = reduce(lambda x, y: x + y, self.populations)
        self.centers = r_centers.get_centers(W, H, NUM_DISTRICTS)
        print_centers(self, self.centers)

    def split_district(self, cells):
        seed_a = cells.pop(random.randrange(len(cells)))
        district_a = [ seed_a ]
        neighbours_a = map(lambda x: x[0], self.borders[seed_a])
        pop_a = self.populations[seed_a]

        seed_b = cells.pop(random.randrange(len(cells)))
        district_b = [ seed_b ]
        neighbours_b = map(lambda x: x[0], self.borders[seed_b])
        pop_b = self.populations[seed_b]

        while (cells):
            free_a_neighbours = set.intersection(set(cells), set(neighbours_a))
            if free_a_neighbours:
                cell = free_a_neighbours[random.randrange(len(free_a_neighbours))]
                cells.remove(cell)
                district_a.append(cell)
                neighbours_a = neighbours_a + map(lambda x: x[0], self.borders[cell])
                pop_a = pop_a + self.populations[cell]

            free_b_neighbours = set.intersection(set(cells), set(neighbours_b))
            if free_b_neighbours:
                cell = free_b_neighbours[random.randrange(len(free_b_neighbours))]
                cells.remove(cell)
                district_b.append(cell)
                neighbours_b = neighbours_b + map(lambda x: x[0], self.borders[cell])
                pop_b = pop_b + self.populations[cell]
        
        return ({
            'cells': district_a,
            'population': pop_a
        }, {
            'cells': district_b,
            'population': pop_b
        })

    def get_district_neighbours(self, cells):
        neighbours = set([])
        for cell in cells:
            neighbours = neighbours | set(map(lambda x: x[0], self.borders[cell]))
        return neighbours - set(cells)
    
    def generate_initial_solution(self):
        '''
        Implementation of random initial solution based on tabu search paper:
            "A tabu search heuristic and adaptive memory procedure for political districting."
            Bozkaya, Burcin, Erhan Erkut, and Gilbert Laporte.
            European Journal of Operational Research 144.1 (2003): 12-26.
        
        districts => array of districts
        district => {
            'cells': [ array of cells in district ],
            'population': population of district
        }
        '''
        target_pop = self.total_population / NUM_DISTRICTS
        cells = range(W * H)
        random.shuffle(cells)
        districts = []
        
        seed = cells.pop()
        current_population = self.populations[seed]
        current_district = [seed]
        while (cells):
            free_neighbours = list(set.intersection(set(cells), self.get_district_neighbours(current_district)))
            random.shuffle(free_neighbours)

            if current_population > target_pop or not free_neighbours:
                districts.append({
                    'cells': current_district,
                    'population': current_population
                })
                seed = cells.pop()
                current_population = self.populations[seed]
                current_district = [seed]
            else:
                cell = free_neighbours.pop()
                cells.remove(cell)
                current_district.append(cell)
                current_population = current_population + self.populations[cell]
        districts.append({
            'cells': current_district,
            'population': current_population
        })

        if len(districts) < NUM_DISTRICTS:
            while(len(districts) != NUM_DISTRICTS):
                districts.sort(key=lambda x: x['population'])

                biggest_district = districts.pop()
                (district_a, district_b) = self.split_district(biggest_district['cells'])
                districts.append(district_a)
                districts.append(district_b)

        elif len(districts) > NUM_DISTRICTS:
            while(len(districts) != NUM_DISTRICTS):
                districts.sort(key=lambda x: x['population'])

                smallest_district = districts.pop(0)
                neighbourhood = self.get_district_neighbours(smallest_district['cells'])

                merging_district_index = None
                for i in range(len(districts)):
                    district = districts[i]
                    if set.intersection(set(district['cells']), neighbourhood):
                        merging_district_index = i
                        break
                
                merging_district = districts.pop(merging_district_index)
                districts.append({
                    'cells': smallest_district['cells'] + merging_district['cells'],
                    'population': smallest_district['population'] + merging_district['population']
                })

        result = [-1] * (W * H)
        for i in range(len(districts)):
            district = districts[i]
            for cell in district['cells']:
                result[cell] = i
        # return [int(i / (math.ceil((float(W*H))/self.num_districts))) for i in range(W*H)]
        return result

