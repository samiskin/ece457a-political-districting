import shapefile
import us

from termcolor import colored

AREA = 0
PERIMETER = 1
TRACT = 6

# {STATE: {TRACT_DICTIONARY}}
# TRACT_DICTIONARY MAPS TRACT_ID TO KEYS: AREA, PERIMETER, COORDINATES
tracts = {}

def print_fields(reader):
    for field in reader.fields:
        print field[0],
    print '\n'

# Process shapefile data for a subset of states
def process_data(*args, **kwargs):
    if len(args) == 0:
        print 'Provide a set of states as arguments to process_data().'
        return

    for state in args:
        try:
            fips = get_fips(state)
            shp = open('shapefiles/tr%s_d00.shp' % (fips), 'rb')
            dbf = open('shapefiles/tr%s_d00.dbf' % (fips), 'rb')
            reader = shapefile.Reader(shp=shp, dbf =dbf)

            if state not in tracts:
                tracts[state] = {}

            for shape in reader.shapeRecords():
                tract_id = get_tract_id(shape.record)
                if tract_id not in tracts[state]:
                    tracts[state][tract_id] = {}

                tracts[state][tract_id]['AREA'] = get_area(shape.record)
                tracts[state][tract_id]['PERIMETER'] = get_perimeter(shape.record)
                tracts[state][tract_id]['COORDINATES'] = shape.shape.points

            shp.close()
            dbf.close()
        except IOError:
            print ('Failed to read shapefile for %s' % (state))

def get_tract_id(record):
    return record[TRACT]

def get_area(record):
    return record[AREA]

def get_perimeter(record):
    return record[PERIMETER]

def get_fips(state):
    return us.states.lookup(unicode(state)).fips

def print_tracts(*args, **kwargs):
    states = args if len(args) > 0 else tracts.keys()
    for state in sorted(states):
        print colored('State: %s' % (state), 'green')
        _outer = tracts[state]
        for tract_id in sorted(_outer.keys()):
            _inner = _outer[tract_id]
            print '\tTract: %s \n\t\t- Area: %s\n\t\t- Perimeter: %s' % (
                tract_id,
                _inner['AREA'],
                _inner['PERIMETER']
            )

def main():
    process_data('Iowa', 'North Carolina', 'South Carolina')
    print_tracts('Iowa')

if __name__ == '__main__':
    main()
