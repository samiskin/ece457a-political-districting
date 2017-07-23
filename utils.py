import copy

# A solution is a mapping from cell index to district number.  Since ids are all
# just 0, 1, 2, ... n, its stored as an array
# Ex: [ 5, 5, 7, 1, 1, 1 ] means units 0, 1 are in district 5, unit 2 is in
# district 7, and units 3, 4, 5 are all in district 1

# A border of a cell id is a tuple of (neighbor_id, border_length)

# A district is a Set of ids (integers)


def get_perimeter(p, district):
    base = set([])
    perimeter = 0
    for i in district:
        for (neighbor, length) in p.borders[i]:
            if neighbor in base:
                perimeter -= length
            else:
                perimeter += length
        base.add(i)
    return perimeter

def get_area(p, cells):
    return reduce((lambda x, y: x + p.areas[y]), cells, 0)

# Array of sets, index is district, value is a set of cell ids for that district
def get_district_map(p, solution):
    districts = {}
    for cell,district in solution.iteritems():
        if district not in districts:
            districts[district] = set([])
        districts[district].add(cell)
    return districts

def get_population(p, district):
    return reduce(lambda x, y: x + p.populations[y], district, 0)


def fitness(p, solution):
    districts = get_district_map(p, solution)
    d_compact = lambda d: get_perimeter(p,d)**2 / float(get_area(p,d))
    d_pop = lambda d: abs(get_population(p,d) - (p.total_population / float(p.num_districts)))
    return -reduce(lambda f, d: f + d_compact(d) + 2*d_pop(d), districts.values(), 0)

# Determine neighbors by moving a cell from one district to another
# without causing any discontinuities
def solution_neighborhood(p,solution):
    districts = get_district_map(p,solution)
    neighborhood = []
    for cell,district in solution.iteritems():
        if not is_contiguous_without_cell(p,districts[district], cell):
            continue
        for (border_cell, _) in p.borders[cell]:
            if border_cell not in districts[district]:
                # Swap cell to border_cell's district
                neighbor = copy.deepcopy(solution)
                neighbor[cell] = solution[border_cell]
                neighborhood.append(neighbor)
    return neighborhood

def solution_neighborhood_for_tabu(p,solution):
    districts = get_district_map(p,solution)
    changed_gu_to_neighborhood = {}

    for (cell, district) in solution.iteritems():
        if not is_contiguous_without_cell(p,districts[district], cell):
            continue
        for (border_cell, _) in p.borders[cell]:
            if border_cell not in districts[district]:
                # Swap cell to border_cell's district
                neighbor = copy.deepcopy(solution)
                neighbor[cell] = solution[border_cell]
                changed_gu_to_neighborhood[(cell, solution[cell], solution[border_cell])] = neighbor
    return changed_gu_to_neighborhood

def is_contiguous_without_cell(p,district, cell_to_skip):
    if len(district) <= 1:
        return False
    cells_to_check = set(district)
    cells_to_check.remove(cell_to_skip)
    random_cell = cells_to_check.pop()
    def floodfill(cell):
        if cell == cell_to_skip:
            return
        for (neighbor, _) in p.borders[cell]:
            if neighbor in district:
                if neighbor in cells_to_check:
                    cells_to_check.remove(neighbor)
                    floodfill(neighbor)
    floodfill(random_cell)
    return len(cells_to_check) == 0;
