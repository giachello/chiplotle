#
# Test of simulated AA instruction
# similar to 7440A test program page 7-10 - 7-11 of the HP 7440A Color Pro Programming Manual
#

from chiplotle import *
from chiplotle.plotters.baseplotter import _BasePlotter
from chiplotle.plotters.drawingplotter import _DrawingPlotter
from chiplotle.plotters.simulatedcommands import simulated_AA, simulated_AR
import chiplotle.geometry as geometry
import chiplotle.tools.io as io


plot = []
plot.append(hpgl.PA([(5000,2000)]))
plot.append(hpgl.SP(1))
plot.append(hpgl.PD([]))
plot = plot + simulated_AA(5000,2000,3000,2000,45,5)
plot.append(hpgl.PU([(4060,3060)]))
plot.append(hpgl.PD([]))
plot = plot + simulated_AA(4060,3060,3000,2000,-45,5)
plot.append(hpgl.PU([(4000,2000)]))
plot.append(hpgl.PD([]))
plot = plot + simulated_AA(4000,2000,3000,2000,45,5)

plot.append(hpgl.SP(2))
plot.append(hpgl.PU([(10,10)]))
plot.append(hpgl.PD([]))
plot = plot + simulated_AR(0,2000,90,5)
plot = plot + simulated_AR(2000,0,90,5)
plot.append(hpgl.PU([]))
plot.append(hpgl.SP(0))

plot.append(hpgl.SP(3))
plot.append(hpgl.PA([(10,5000)]))
plot.append(hpgl.PD([]))
plot.append(hpgl.PR([(1000,0)]))
plot = plot + simulated_AR(0,-700,-90,5)
plot = plot + simulated_AR(700,0,90,5)
plot.append(hpgl.PR([(1000,0)]))


io.view(plot, fmt="hpgl")





plotter : _DrawingPlotter = instantiate_plotters( )[0]

plotter.select_pen(1)
plotter.write(hpgl.PA([(5000,2000)]))
plotter.pen_down()
plotter.write(hpgl.AA((3000,2000),45))

plotter.pen_up([(4060,3060)])
plotter.pen_down()
plotter.write(hpgl.AA((3000,2000),-45))

plotter.pen_up([(4000,2000)])
plotter.pen_down()
plotter.write(hpgl.AA((3000,2000),45))


plotter.write(hpgl.PU([(10,10)]))

plotter.write(hpgl.SP(2))
plotter.write(hpgl.PD([]))
plotter.write(hpgl.AR((0,2000),90,5))
plotter.write(hpgl.AR((2000,0),90,5))
plotter.pen_up()

plotter.select_pen(3)
plotter.write(hpgl.PA([(10,5000)]))
plotter.pen_down()
plotter.write(hpgl.PR([(1000,0)]))
plotter.write(hpgl.AR((0,-700),-90,5))
plotter.write(hpgl.AR((700,0),90,5))
plotter.write(hpgl.PR([(1000,0)]))

plotter.pen_up()
plotter.select_pen(0)

plotter.flush()

