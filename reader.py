import shapefile
import us

STATEFP = 0
GEOID = 2
ALAND = 8
AWATER = 9

def print_fields(reader):
    for field in reader.fields:
        print field[0],
    print '\n'

def print_areas(reader):
    result = []
    index = -1

    for i, field in enumerate(reader.fields):
        if field[0] == 'ALAND':
            index = i

    if index == -1:
        return

    for record in reader.iterRecords():
        print get_geoid_identifier(record) + " (" + get_state_identifier(record) + "): " + str(record[index])

def get_state_identifier(record):
    return us.states.lookup(record[0]).name

def get_geoid_identifier(record):
    return record[GEOID]

def main():
    shp = open('shapefiles/tl_2016_us_cd115.shp', 'rb')
    dbf = open('shapefiles/tl_2016_us_cd115.dbf', 'rb')
    reader = shapefile.Reader(shp=shp, dbf =dbf)

    print_fields(reader)
    print_areas(reader)

if __name__ == '__main__':
    main()
