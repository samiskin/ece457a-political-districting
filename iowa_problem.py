from __future__ import print_function
import math
import random
from data.reader import *
from data.visualizer import *
from utils import get_district_map

W = 6
H = 6
NUM_DISTRICTS = 5

VISUALIZE = True

def print_solution(p, solution):
    districts = get_district_map(p, solution)
    if VISUALIZE:
        for district in districts.keys():
            print("DISTRICT: " + str(district) + ", POPULATION: " + str(sum([p.populations[cell] for cell in districts[district]])))
            # print(districts[district])
        visualizer = Visualizer(p.data, districts)
    else:
        for district in districts.keys():
            print("DISTRICT: " + str(district) + ", POPULATION: " + str(sum([p.populations[cell] for cell in districts[district]])))
            print(districts[district])

class Problem:
    def __init__(self):
        self.num_districts = NUM_DISTRICTS

        self.data = Data()

        self.cell_ids = self.data.map['Iowa'].keys() # [ id_1, id_2, ...]

        self.populations = {} # { id => pop }
        self.areas = {} # { id => area }
        self.borders = {} # { id => [(id, border_length), ...] }
        self.total_population = 0

        for cell_id in self.cell_ids:
            cell_data = self.data.map['Iowa'][cell_id]
            self.populations[cell_id] = int(cell_data[POPULATION_KEY])
            self.total_population = self.total_population + int(cell_data[POPULATION_KEY])
            self.areas[cell_id] = float(cell_data[AREA_KEY])

            for neighbour_id in cell_data[NEIGHBOURS_KEY]:
                if cell_id not in self.borders:
                    self.borders[cell_id] = []
                self.borders[cell_id].append((neighbour_id, cell_data[NEIGHBOURS_KEY][neighbour_id]))

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
        cells = list(self.cell_ids)
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

        result = {}
        for i in range(len(districts)):
            district = districts[i]
            for cell in district['cells']:
                result[cell] = i

        return result
