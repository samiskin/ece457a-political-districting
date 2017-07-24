import math
import random
import time

# from grid_problem import *
from iowa_problem import *

from utils import *

program_start = time.time()

p = Problem()

# A swap is a tuple of (id, district)
# A velocity is an array of swaps

MAX_DIF_LEN = 4
MAX_VEL_LEN = 10
C1 = 1
C2 = 1
C3 = 1
MAX_ITERATIONS = 1000
NUM_PARTICLES = 5

def find_valid_swap(districts_a, districts_b):
    randomized_districts = list(range(0, len(districts_b)))
    random.shuffle(randomized_districts)

    for rand_district in randomized_districts:
        for cell in districts_b[rand_district]:
            for (neighbor, _) in p.borders[cell]:
                if neighbor not in districts_b[rand_district] \
                        and neighbor in districts_a[rand_district]:
                    district_of_neighbor = (i for i,v in districts_b.iteritems() if neighbor in v).next()
                    if is_contiguous_without_cell(p, districts_b[district_of_neighbor], neighbor):
                        return (neighbor, district_of_neighbor, rand_district)
    return (None, None, None)


def sol_minus_sol(sol_a, sol_b):
    districts_a = get_district_map(p, sol_a)
    districts_b = get_district_map(p, sol_b)
    swaps = []
    for i in xrange(0, MAX_DIF_LEN):
       (cell_to_swap, orig_cell_district, new_cell_district) = find_valid_swap(districts_a, districts_b)
       if cell_to_swap is None:
           break
       districts_b[orig_cell_district].remove(cell_to_swap)
       districts_b[new_cell_district].add(cell_to_swap)
       swaps.append((cell_to_swap, new_cell_district))

    return swaps

def sol_plus_vel(orig_sol, vel):
    sol = dict(orig_sol)
    for (cell_to_swap, new_district) in vel:
        sol[cell_to_swap] = new_district
    return sol


def num_mul_vel(num, vel):
    assert(num <= 1 and num >= 0)
    end = int(math.ceil(num * len(vel)))
    return vel[0:end]


def rand_swap(districts, tabu_list = set([])):
    randomized_districts = list(range(0, len(districts)))
    random.shuffle(randomized_districts)

    for rand_district in randomized_districts:
        for cell in districts[rand_district]:
            for (neighbor, _) in p.borders[cell]:
                if neighbor not in districts[rand_district] and (neighbor,
                        rand_district) not in tabu_list:
                    district_of_neighbor = (i for i,v in districts.iteritems() if neighbor in v).next()
                    if is_contiguous_without_cell(p, districts[district_of_neighbor], neighbor):
                        return (neighbor, district_of_neighbor, rand_district)
    return (None, None, None)

def rand_vel(sol):
    tabu_list = set([])
    swaps = []
    districts = get_district_map(p, sol)
    while len(swaps) < MAX_VEL_LEN:
       (cell_to_swap, orig_cell_district, new_cell_district) = rand_swap(districts, tabu_list)
       if cell_to_swap is None:
           break
       tabu_list.add((cell_to_swap, orig_cell_district))
       districts[orig_cell_district].remove(cell_to_swap)
       districts[new_cell_district].add(cell_to_swap)
       swaps.append((cell_to_swap, new_cell_district))
    return swaps


#-------------------------------------------------------------------------------------


def tick(X, pbest, gbest):
    r1 = random.random()
    r2 = random.random()
    V = rand_vel(X)
    D = sol_plus_vel(X, num_mul_vel(C1, V))
    E = sol_plus_vel(D, num_mul_vel(r1 * C2, sol_minus_sol(pbest, D)))
    X2 = sol_plus_vel(E, num_mul_vel(r2 * C3, sol_minus_sol(gbest, E)))
    return X2

def tick_for_testing(X, pbest, gbest, c1, c2, c3):
    r1 = random.random()
    r2 = random.random()
    V = rand_vel(X)
    D = sol_plus_vel(X, num_mul_vel(c1, V))
    E = sol_plus_vel(D, num_mul_vel(r1 * c2, sol_minus_sol(pbest, D)))
    X2 = sol_plus_vel(E, num_mul_vel(r2 * c3, sol_minus_sol(gbest, E)))
    return X2

def main():
    particles = [p.generate_initial_solution() for i in xrange(0, NUM_PARTICLES)]
    vels = [rand_vel(particle) for particle in particles]
    pbests = [particle for particle in particles]
    gbest = max(particles, key=lambda sol: fitness(p, sol))

    print('-----  Initial Best (Cost: {})  -----'.format(-fitness(p, gbest)))
    print_solution(p, gbest)
    print('\n')

    for _ in xrange(0, MAX_ITERATIONS):
        for i, particle in enumerate(particles):
            new_x = tick(particle, pbests[i], gbest)
            new_fitness = fitness(p, new_x)
            if new_fitness > fitness(p, pbests[i]):
                pbests[i] = new_x
            if new_fitness > fitness(p, gbest):
                gbest = new_x
            particles[i] = new_x

    print('-----   Final (Cost: {})   -----'.format(-fitness(p, gbest)))
    print_solution(p, gbest)
    print('Time: {}s'.format(time.time() - program_start))

def test(c1, c2, c3):
    particles = [p.generate_initial_solution() for i in xrange(0, NUM_PARTICLES)]
    vels = [rand_vel(particle) for particle in particles]
    pbests = [particle for particle in particles]
    gbest = max(particles, key=lambda sol: fitness(p, sol))

    print('-----  Initial Best (Cost: {})  -----'.format(-fitness(p, gbest)))
    print_solution(p, gbest)
    print('\n')

    initial_fitness_details = fitness_details(p, gbest)

    for _ in xrange(0, MAX_ITERATIONS):
        for i, particle in enumerate(particles):
            new_x = tick_for_testing(particle, pbests[i], gbest, c1, c2, c3)
            new_fitness = fitness(p, new_x)
            if new_fitness > fitness(p, pbests[i]):
                pbests[i] = new_x
            if new_fitness > fitness(p, gbest):
                gbest = new_x
            particles[i] = new_x

    print('-----   Final (Cost: {})   -----'.format(-fitness(p, gbest)))
    print_solution(p, gbest)
    print('Time: {}s'.format(time.time() - program_start))

    best_fitness_details = fitness_details(p, gbest)

    return initial_fitness_details + best_fitness_details

if __name__ == "__main__":
    main()
