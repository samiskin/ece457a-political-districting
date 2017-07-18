import shapefile
import us

from termcolor import colored

AREA_KEY = 'AREA'
NAME_KEY = 'NAME'
POPULATION_KEY = 'POPULATION'
COORDINATES_KEY = 'COORDINATES'
NEIGHBOURS_KEY = "NEIGHBOURS"
PERIMETER_KEY = "PERIMETER"

STATEFP = 0
GEOID = 3
NAME = 4
ALAND = 13

# {State: {}}
# {} MAPS COUNTY GEOID TO KEYS: AREA, NAME, POPULATION, COORDINATES, NEIGHBOURS
_map = {}

# MAPS COUNTY_NAME TO POPULATION
_populations = {}

# USED DURING ADJACENCY MAPPING TO SAVE MEMORY USAGE
_counties = set()

def print_fields(reader):
    for field in reader.fields:
        print field[0],
    print '\n'

# Process shapefile data for a subset of states
def process_data(*args, **kwargs):
    if len(args) == 0:
        print 'Provide a set of states as arguments to process_data().'
        return

    states = set(args)
    get_county_populations()
    process_shapefiles(states)
    get_county_adjacencies(states)

def process_shapefiles(states):
    global _map
    global _counties

    try:
        shp = open('files/tl_2016_us_county.shp', 'rb')
        dbf = open('files/tl_2016_us_county.dbf', 'rb')
        reader = shapefile.Reader(shp=shp, dbf =dbf)

        for shape_record in reader.shapeRecords():
            record = shape_record.record
            shape = shape_record.shape

            state = get_state_name(record)
            if state not in states:     # State we are not interested in
                continue

            if state not in _map:
                _map[state] = {}

            county = get_county_geoid(record)
            if county not in _map[state]:
                _map[state][county] = {}

            _map[state][county][AREA_KEY] = get_county_area(record)
            _map[state][county][NAME_KEY] = get_county_name(record)
            _map[state][county][POPULATION_KEY] = get_county_population(get_county_name(record))

            coordinates = get_coordinates(shape.bbox)
            _map[state][county][COORDINATES_KEY] = get_coordinates(coordinates)
            _map[state][county][PERIMETER_KEY] = get_perimeter(coordinates)

            _counties.add(county)

        shp.close()
        dbf.close()
    except IOError:
        print 'Failed to read shapefiles. Make sure to unzip files.zip first.'
        return

def get_county_populations():
    global _populations

    try:
        pop = open('files/county_population.csv', 'rb')

        lines = pop.readlines()
        for line in lines:
            name, population = line.strip().split(', ')
            _populations[name] = population

        pop.close()
    except IOError:
        print 'Failed to read county_population.csv. Make sure to unzip files.zip first.'
        return

def get_county_adjacencies(states):
    global _map
    global _counties

    try:
        # Big file, may take a while to read; Check files/county_adjacency for specific format
        adj = open('files/county_adjacency.txt', 'rb')

        lines = adj.readlines()
        active_county = None

        for line in lines:
            line = line.strip()
            if ', ' in line:    # delimiter for county adjacency
                active_county, first_neighbor = map(int, line.split(', '))

                if active_county not in _counties or first_neighbor not in _counties:  # Ignore counties not in state
                    active_county = None
                    continue

                for state in states:
                    if active_county in _map[state]:
                        if NEIGHBOURS_KEY not in _map[state][active_county]:
                            _map[state][active_county][NEIGHBOURS_KEY] = []

                        # Deduplication needed since each county is also own neighbour
                        if active_county != first_neighbor:
                            _map[state][active_county][NEIGHBOURS_KEY].append(first_neighbor)
            else:
                geo_id = int(line)
                if not active_county or geo_id not in _counties:    # Ignore counties not in state
                    continue

                # Implicitly assumed to be adjacent to active county
                for state in states:
                    if active_county in _map[state] and active_county != geo_id:
                        _map[state][active_county][NEIGHBOURS_KEY].append(geo_id)

        adj.close()
    except IOError:
        print 'Failed to read adjacency file. Make sure to unzip files.zip first.'
        return

def get_perimeter(coordinates):
    return abs(coordinates[0][1] - coordinates[1][1]) + \
           abs(coordinates[1][0] - coordinates[2][0]) + \
           abs(coordinates[3][1] - coordinates[2][1]) + \
           abs(coordinates[3][0] - coordinates[0][0])

def get_coordinates(bbox):
    bottom_left_x = bbox[:2][0]
    bottom_left_y = bbox[:2][1]
    top_right_x = bbox[2:][0]
    top_right_y = bbox[2:][1]

    return [
        (bottom_left_x, top_right_y),
        (bottom_left_x, bottom_left_y),
        (top_right_x, bottom_left_y),
        (top_right_x, top_right_y),
    ]

def get_state_name(record):
    return us.states.lookup(record[STATEFP]).name

def get_county_geoid(record):
    return int(record[GEOID])

def get_county_area(record):
    return float(record[ALAND])/ 10**6

def get_county_name(record):
    return record[NAME]

def get_county_population(name):
    return _populations[name] if name in _populations else None

def neighbours_string(county, state, neighbours):
    return ', '.join(['%s (%s)' % (_map[state][n][NAME_KEY], n) for n in neighbours])

def print_mapping(*args, **kwargs):
    states = args if len(args) > 0 else tracts.keys()
    for state in sorted(states):
        print colored('State: %s' % (state), 'green')
        _outer = _map[state]
        for county in sorted(_outer.keys()):
            _inner = _outer[county]
            print '\tCounty: %s \n\t\t- Name: %s\n\t\t- Area: %s\n\t\t- Population: %s\n\t\t- Neighbours: %s\n\t\t- Coordinates: %s\n\t\t- Perimeter: %s\n' % (
                county,
                _inner[NAME_KEY],
                _inner[AREA_KEY],
                _inner[POPULATION_KEY],
                neighbours_string(county, state, _inner[NEIGHBOURS_KEY]) if NEIGHBOURS_KEY in _inner else 'None',
                _inner[COORDINATES_KEY],
                _inner[PERIMETER_KEY],
            )

def main():
    process_data('Iowa')
    print_mapping('Iowa')

if __name__ == '__main__':
    main()
