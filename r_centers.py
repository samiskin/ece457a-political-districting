import random
from pyeasyga import pyeasyga

def get_centers(w, h, num_centers):
    # define and set function to create a candidate solution representation
    def create_individual(data):
        individual = cells
        random.shuffle(individual)
        return individual[:num_centers]

    # define and set the GA's crossover operation
    def crossover(parent_1, parent_2):
        length = len(parent_1)
        crossover_index = random.randrange(1, len(parent_1))
        child_1 = parent_1[:crossover_index] + parent_2[crossover_index:]
        child_2 = parent_2[:crossover_index] + parent_1[crossover_index:]
        while len(set(child_1)) < length:
            child_1 = list(set(child_1 + [child_2[random.randint(0, length-1)]]))
        while len(set(child_2)) < length:
            child_2 = list(set(child_2 + [child_1[random.randint(0, length-1)]]))

        return child_1, child_2

    # define and set the GA's mutation operation
    def mutate(individual):
        temp = random.randint(0, num_cells - 1)
        while (temp in individual):
            temp = random.randint(0, num_cells - 1)
        
        individual[random.randint(0, len(individual)-1)] = temp

    # define and set the GA's selection operation
    def selection(population):
        return random.choice(population)

    def get_distance(a, b):
        (x1, y1) = toXY(a)
        (x2, y2) = toXY(b)
        return abs(x1 - x2) + abs(y1 - y2)

    # define a fitness function
    def fitness (individual, data):
        fitness = 0
        for cell in list(set(cells) - set(individual)):
            closest_distance = None
            for center in individual:
                distance = get_distance(cell, center)
                if not closest_distance or closest_distance > distance:
                    closest_distance = distance
            fitness = fitness + closest_distance

        return fitness

    
    num_cells = w*h
    cells = range(num_cells)
    toXY = lambda i: (i % w, i / w)

    # initialise the GA
    ga = pyeasyga.GeneticAlgorithm({},
                                population_size=20,
                                generations=100,
                                crossover_probability=0.8,
                                mutation_probability=0.2,
                                elitism=True,
                                maximise_fitness=False)
    ga.create_individual = create_individual
    ga.crossover_function = crossover
    ga.mutate_function = mutate
    ga.selection_function = selection
    ga.fitness_function = fitness       # set the GA's fitness function
    ga.run()                            # run the GA
    # print ga.best_individual()
    return ga.best_individual()[1]