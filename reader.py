import shapefile
import us

STATEFIPS = 0
GEOID = 2
ALAND = 8
AWATER = 9

# STATE: [DISTRICT: AREA], AREA represented by km^2
districts = {}

def print_fields(reader):
    for field in reader.fields:
        print field[0],
    print '\n'

def process_data():
    global districts
    shp = open('shapefiles/tl_2016_us_cd115.shp', 'rb')
    dbf = open('shapefiles/tl_2016_us_cd115.dbf', 'rb')
    reader = shapefile.Reader(shp=shp, dbf =dbf)

    for record in reader.iterRecords():
        state = get_state_identifier(record)
        if state not in districts:
            districts[state] = {}
        geoid = get_geoid_identifier(record)
        districts[state][geoid] = get_land_area(record) / float(10**6)

def print_areas(*args, **kwargs):
    states = args if args else districts.keys()

    for state in sorted(states):
        print state
        for geoid in sorted(districts[state].keys()):
            print '\t- ' + geoid + ': ' + str(districts[state][geoid])
        print_shapefiles(unicode(state))

def get_land_area(record):
    return record[ALAND]

def get_state_identifier(record):
    return us.states.lookup(record[STATEFIPS]).name

def get_geoid_identifier(record):
    return record[GEOID]

def print_shapefiles(state):
    urls = us.states.lookup(state).shapefile_urls()
    for region, url in urls.items():
        print '%s: %s' % (region, url)
    print '\n'

def main():
    process_data()
    print_areas('Iowa', 'North Carolina', 'South Carolina')

if __name__ == '__main__':
    main()
