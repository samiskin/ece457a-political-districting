import matplotlib.pyplot as plot
import matplotlib.patches as patches

from reader import *

class Visualizer:
    def __init__(self, data, districts):
        self.color = {
            0: 'red',
            1: 'yellow',
            2: 'green',
            3: 'blue'
        }

        self.fig = plot.figure()
        self.ax = self.fig.add_subplot(111)
        for district in districts:
            print district
            for county_id in districts[district]:
                county = data.map['Iowa'][county_id]
                coordinates = county[COORDINATES_KEY]
                width = county[WIDTH_KEY]
                height = county[HEIGHT_KEY]

                self.ax.add_patch(
                    patches.Rectangle(
                        coordinates[BOTTOM_LEFT],
                        width,
                        height,
                        color=self.color[district]
                    )
                )
        plot.xlim([-100, -80])
        plot.ylim([30, 50])
        plot.show()
