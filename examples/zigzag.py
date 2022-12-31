import random
from chiplotle import *
from chiplotle.plotters.baseplotter import _BasePlotter

plotter : _BasePlotter = instantiate_plotters( )[0]

plotter.select_pen(5)

coords = [(x, random.randint(0, 4000)) for x in range(0, 800, 100)]
plotter.write(hpgl.PD(coords))
plotter.select_pen(1)
plotter.write(hpgl.CI(200))
plotter.write(hpgl.PU([(2000,2000)]))
plotter.write(hpgl.CI(1000,10))
plotter.select_pen(0)
plotter.flush()
