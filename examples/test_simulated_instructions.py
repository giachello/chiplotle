# Test simulated instructions CI, AA, AR, ...
#
import math
from chiplotle import *
from chiplotle.plotters.baseplotter import _BasePlotter

#plotter : _BasePlotter = instantiate_plotters( )[0]
plotter = instantiate_virtual_plotter()

plotter.select_pen(3)

plotter.write(hpgl.PU([(1000,1000)]))
plotter.write(hpgl.CI(500,10))

plotter.pen_down()
plotter.write(hpgl.AA((1500,0),90,5.0))

plotter.select_pen(0)
plotter.flush()

io.view(plotter, "hpgl")
