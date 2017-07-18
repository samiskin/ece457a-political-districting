import shapefile
import us

from termcolor import colored

STATEFP = 0
GEOID = 3
NAME = 4
ALAND = 13

# {STATE: {COUNTY_DICTIONARY}}
# COUNTY_DICTIONARY MAPS COUNTY GEOID TO KEYS: AREA, NAME, POPULATION
_map = {}

# MAPS COUNTY_NAME TO POPULATION
_populations = {}

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

    try:
        pop = open('files/county_population.csv', 'rb')

        lines = pop.readlines()
        for line in lines:
            name, population = line.split(', ')
            _populations[name] = population

        pop.close()
    except IOError:
        print 'Failed to read county_population.csv. Make sure to unzip files.zip first.'
        return

    try:
        shp = open('files/tl_2016_us_county.shp', 'rb')
        dbf = open('files/tl_2016_us_county.dbf', 'rb')
        reader = shapefile.Reader(shp=shp, dbf =dbf)

        for shape in reader.shapeRecords():
            record = shape.record
            state = get_state_name(record)
            if state not in states:     # State we are not interested in
                continue

            if state not in _map:
                _map[state] = {}

            county = get_county_geoid(record)
            if county not in _map[state]:
                _map[state][county] = {}

            _map[state][county]['AREA'] = get_county_area(record)
            _map[state][county]['NAME'] = get_county_name(record)
            _map[state][county]['POPULATION'] = get_county_population(get_county_name(record))

        shp.close()
        dbf.close()
    except IOError:
        print 'Failed to read shapefiles. Make sure to unzip files.zip first.'

def get_state_name(record):
    return us.states.lookup(record[STATEFP]).name

def get_county_geoid(record):
    return record[GEOID]

def get_county_area(record):
    return float(record[ALAND])/ 10**6

def get_county_name(record):
    return record[NAME]

def get_county_population(name):
    return _populations[name] if name in _populations else None

def print_mapping(*args, **kwargs):
    states = args if len(args) > 0 else tracts.keys()
    for state in sorted(states):
        print colored('State: %s' % (state), 'green')
        _outer = _map[state]
        for county in sorted(_outer.keys()):
            _inner = _outer[county]
            print '\tCounty: %s \n\t\t- Name: %s\n\t\t- Area: %s\n\t\t- Population: %s' % (
                county,
                _inner['NAME'],
                _inner['AREA'],
                _inner['POPULATION']
            )

def main():
    process_data('Iowa')
    print_mapping('Iowa')

if __name__ == '__main__':
    main()
