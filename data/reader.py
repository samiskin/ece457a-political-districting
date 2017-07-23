import shapefile
import us

from termcolor import colored

AREA_KEY = 'AREA'
NAME_KEY = 'NAME'
POPULATION_KEY = 'POPULATION'
COORDINATES_KEY = 'COORDINATES'
WIDTH_KEY = 'WIDTH'
HEIGHT_KEY = 'HEIGHT'
NEIGHBOURS_KEY = "NEIGHBOURS"
PERIMETER_KEY = "PERIMETER"

STATEFP = 0
GEOID = 3
NAME = 4
ALAND = 13

TOP_LEFT = 0
BOTTOM_LEFT = 1
BOTTOM_RIGHT = 2
TOP_RIGHT = 3

X = 0
Y = 1

NEGLIGIBLE_BORDER_LENGTH = 0.5

class Data:
    def __init__(self):
        # {State: {}}
        # {} MAPS COUNTY GEOID TO KEYS: AREA, NAME, POPULATION, COORDINATES, NEIGHBOURS
        # NEIGHBOURS MAPS COUNTY GEOID TO SHARED BORDER LENGTH
        self.map = {}

        # MAPS COUNTY_NAME TO POPULATION
        self.populations = {}

        # USED DURING ADJACENCY MAPPING TO SAVE MEMORY USAGE
        self.counties = set()

        self.process_data('Iowa')

    def print_fields(self, reader):
        for field in reader.fields:
            print field[0],
        print '\n'

    # Process shapefile data for a subset of states
    def process_data(self, *args, **kwargs):
        if len(args) == 0:
            print 'Provide a set of states as arguments to process_data().'
            return

        states = set(args)
        self.get_county_populations()
        self.process_shapefiles(states)
        self.get_county_adjacencies(states)

    def process_shapefiles(self, states):
        try:
            shp = open('data/files/tl_2016_us_county.shp', 'rb')
            dbf = open('data/files/tl_2016_us_county.dbf', 'rb')
            reader = shapefile.Reader(shp=shp, dbf =dbf)

            for shape_record in reader.shapeRecords():
                record = shape_record.record
                shape = shape_record.shape

                state = self.get_state_name(record)
                if state not in states:     # State we are not interested in
                    continue

                if state not in self.map:
                    self.map[state] = {}

                county = self.get_county_geoid(record)
                if county not in self.map[state]:
                    self.map[state][county] = {}

                self.map[state][county][AREA_KEY] = self.get_county_area(record)
                self.map[state][county][NAME_KEY] = self.get_county_name(record)
                self.map[state][county][POPULATION_KEY] = self.get_county_population(self.get_county_name(record))

                coordinates = self.get_coordinates(shape.bbox)
                self.map[state][county][COORDINATES_KEY] = coordinates
                self.map[state][county][PERIMETER_KEY] = self.get_perimeter(coordinates)
                self.map[state][county][WIDTH_KEY] = self.get_width(coordinates)
                self.map[state][county][HEIGHT_KEY] = self.get_height(coordinates)

                self.counties.add(county)

            shp.close()
            dbf.close()
        except IOError:
            print 'Failed to read shapefiles. Make sure to unzip files.zip first.'
            return

    def get_county_populations(self):
        try:
            pop = open('data/files/county_population.csv', 'rb')

            lines = pop.readlines()
            for line in lines:
                name, population = line.strip().split(', ')
                self.populations[name] = population

            pop.close()
        except IOError:
            print 'Failed to read county_population.csv. Make sure to unzip files.zip first.'
            return

    def get_county_adjacencies(self, states):
        try:
            # Big file, may take a while to read; Check files/county_adjacency for specific format
            adj = open('data/files/county_adjacency.txt', 'rb')

            lines = adj.readlines()
            active_county = None

            for line in lines:
                line = line.strip()
                if ', ' in line:    # delimiter for county adjacency
                    active_county, first_neighbor = map(int, line.split(', '))

                    if active_county not in self.counties or first_neighbor not in self.counties:  # Ignore counties not in state
                        continue

                    for state in states:
                        if active_county in self.map[state]:
                            if NEIGHBOURS_KEY not in self.map[state][active_county]:
                                self.map[state][active_county][NEIGHBOURS_KEY] = {}

                            # Deduplication needed since each county is also own neighbour
                            if active_county != first_neighbor:
                                border_length = self.get_neighbour_border_lengths(state, active_county, first_neighbor)
                                if border_length > NEGLIGIBLE_BORDER_LENGTH:    # Ignore neighbours that share a negligible border (ie. corner)
                                    self.map[state][active_county][NEIGHBOURS_KEY][first_neighbor] = border_length
                else:
                    geo_id = int(line)
                    if active_county not in self.counties or geo_id not in self.counties:    # Ignore counties not in state
                        continue

                    # Implicitly assumed to be adjacent to active county
                    for state in states:
                        if active_county in self.map[state] and active_county != geo_id:
                            if NEIGHBOURS_KEY not in self.map[state][active_county]:
                                self.map[state][active_county][NEIGHBOURS_KEY] = {}

                            border_length = self.get_neighbour_border_lengths(state, active_county, geo_id)
                            if border_length > NEGLIGIBLE_BORDER_LENGTH:    # Ignore neighbours that share a negligible border (ie. corner) only
                                self.map[state][active_county][NEIGHBOURS_KEY][geo_id] = border_length

            adj.close()
        except IOError:
            print 'Failed to read adjacency file. Make sure to unzip files.zip first.'
            return

    def get_neighbour_border_lengths(self, state, county, neighbour):
        border_length = 0.0
        county = self.map[state][county][COORDINATES_KEY]
        neighbour = self.map[state][neighbour][COORDINATES_KEY]

        # Edge case: neighbour enclosed within or completely overlaps (should almost never happen in practice, but just for completeness)
        if neighbour[TOP_LEFT][X] >= county[TOP_LEFT][X] and \
           neighbour[TOP_RIGHT][X] <= county[TOP_RIGHT][X] and \
           neighbour[TOP_LEFT][Y] <= county[TOP_LEFT][Y] and \
           neighbour[TOP_RIGHT][Y] <= county[TOP_RIGHT][Y] and \
           neighbour[BOTTOM_LEFT][Y] >= county[BOTTOM_LEFT][Y] and \
           neighbour[BOTTOM_RIGHT][Y] >= county[BOTTOM_RIGHT][Y]:
            return self.map[state][neighbour][PERIMETER_KEY]

        # Vertical border
        vertical_diff = abs(
            min(neighbour[TOP_LEFT][Y], county[TOP_LEFT][Y]) - max(neighbour[BOTTOM_RIGHT][Y], county[BOTTOM_RIGHT][Y])
        )

        if neighbour[BOTTOM_LEFT][Y] <= county[TOP_LEFT][Y] or neighbour[TOP_LEFT][Y] >= county[BOTTOM_LEFT][Y]:
            if neighbour[TOP_LEFT][X] >= county[TOP_LEFT][X]:
                border_length += vertical_diff
            if neighbour[TOP_RIGHT][X] <= county[TOP_RIGHT][X]:
                border_length += vertical_diff

        # Horizontal border
        horizontal_diff = abs(
            max(neighbour[TOP_LEFT][X], county[TOP_LEFT][X]) - min(neighbour[TOP_RIGHT][X], county[TOP_RIGHT][X])
        )

        if neighbour[TOP_LEFT][X] <= county[TOP_RIGHT][X] or neighbour[TOP_RIGHT][X] >= county[TOP_LEFT][X]:
            if neighbour[TOP_LEFT][Y] <= county[TOP_RIGHT][Y]:
                border_length += horizontal_diff
            if neighbour[BOTTOM_LEFT][Y] >= county[BOTTOM_RIGHT][Y]:
                border_length += horizontal_diff

        return self.convert_to_km(border_length)

    def convert_to_km(self, value):
        # Use Iowa County dimensions as standard
        return value / (1.652672/158.33)

    def get_perimeter(self, coordinates):
        return self.convert_to_km(
            abs(coordinates[TOP_LEFT][Y] - coordinates[BOTTOM_LEFT][Y]) + \
            abs(coordinates[BOTTOM_LEFT][X] - coordinates[BOTTOM_RIGHT][X]) + \
            abs(coordinates[BOTTOM_RIGHT][Y] - coordinates[TOP_RIGHT][Y]) + \
            abs(coordinates[TOP_RIGHT][X] - coordinates[TOP_LEFT][X])
        )

    def get_coordinates(self, bbox):
        bottom_left_x = bbox[:2][0]
        bottom_left_y = bbox[:2][1]
        top_right_x = bbox[2:][0]
        top_right_y = bbox[2:][1]

        return [
            (bottom_left_x, top_right_y),   # TOP_LEFT
            (bottom_left_x, bottom_left_y), # BOTTOM_LEFT
            (top_right_x, bottom_left_y),   # BOTTOM_RIGHT
            (top_right_x, top_right_y),     # TOP_RIGHT
        ]

    def get_width(self, coordinates):
        return abs(coordinates[TOP_LEFT][X] - coordinates[TOP_RIGHT][X])

    def get_height(self, coordinates):
        return abs(coordinates[TOP_LEFT][Y] - coordinates[BOTTOM_LEFT][Y])

    def get_state_name(self, record):
        return us.states.lookup(record[STATEFP]).name

    def get_county_geoid(self, record):
        return int(record[GEOID])

    def get_county_area(self, record):
        return float(record[ALAND])/ 10**6

    def get_county_name(self, record):
        return record[NAME]

    def get_county_population(self, name):
        return self.populations[name] if name in self.populations else None

    def neighbours_string(self, state, county, neighbours):
        # Prints the neighbour's name and the length of border shared betweeen county and the neighbour
        return ', '.join(['%s (%s)' % (self.map[state][n][NAME_KEY], self.map[state][county][NEIGHBOURS_KEY][n]) for n in sorted(neighbours)])

    def print_mapping(self, *args, **kwargs):
        states = args if len(args) > 0 else tracts.keys()
        for state in sorted(states):
            print colored('State: %s' % (state), 'green')
            _outer = self.map[state]
            for county in sorted(_outer.keys()):
                _inner = _outer[county]
                print '\tCounty: %s \n\t\t- Name: %s\n\t\t- Area: %s\n\t\t- Population: %s\n\t\t- Neighbours: %s\n\t\t- Coordinates: %s\n\t\t- Perimeter: %s\n' % (
                    county,
                    _inner[NAME_KEY],
                    _inner[AREA_KEY],
                    _inner[POPULATION_KEY],
                    neighbours_string(state, county, _inner[NEIGHBOURS_KEY].keys()) if NEIGHBOURS_KEY in _inner else 'None',
                    _inner[COORDINATES_KEY],
                    _inner[PERIMETER_KEY],
                )
