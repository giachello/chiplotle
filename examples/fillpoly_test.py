import random
from chiplotle import *
from chiplotle.plotters.fillpoly import fill
from chiplotle.plotters.baseplotter import _BasePlotter

plotter : _BasePlotter = instantiate_plotters( )[0]
plotter.select_pen(2)
point1 = Coordinate(0,0)

polygon = CoordinateArray([(1000,1000),(1000,2000),
    (1000,2000),(2000,2000),
    (2000,2000),(2000,1000),
    (2000,1000),(1000,1000)])

numpoints = 7

filltype = 4
spacing = 100
hatchangle = 45

poly = fill(polygon, numpoints, point1, filltype,  spacing, hatchangle)

print(poly)

plotter.write(poly)
plotter.select_pen(0)
plotter.flush()
