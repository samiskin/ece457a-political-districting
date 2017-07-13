import shapefile
import us

STATEFP = 0
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

def print_areas():
    for state in sorted(districts.keys()):
        print state
        for geoid in sorted(districts[state].keys()):
            print '\t- ' + geoid + ': ' + str(districts[state][geoid])

def get_land_area(record):
    return record[ALAND]

def get_state_identifier(record):
    return us.states.lookup(record[STATEFP]).name

def get_geoid_identifier(record):
    return record[GEOID]

def main():
    process_data()
    print_areas()

if __name__ == '__main__':
    main()
