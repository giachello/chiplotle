
from chiplotle import *
from chiplotle.plotters.baseplotter import _BasePlotter
from chiplotle.plotters.drawingplotter import _DrawingPlotter
import chiplotle.geometry as geometry


def draw_circle(radius, chord_angle):
    c = geometry.shapes.circle(radius,int(360.0/chord_angle)).points
    c2=CoordinateArray()
    for i in range(1,len(c)):
        c2.append(c[i]-c[i-1])
    c2.append(c[0]-c[len(c)-1])

    pen_status = int(plotter.status) & 1
    plotter.pen_up()
    plotter.write(hpgl.PR([c[0]]))
    plotter.pen_down()
    plotter.write(hpgl.PR(c2))
    plotter.pen_up()
    plotter.write(hpgl.PR([-c[0]]))
    if pen_status == 1:
        plotter.pen_down()


plotter : _DrawingPlotter = instantiate_plotters( )[0]

plotter.select_pen(1)
plotter.write(hpgl.PU([(3000,3000)]))
plotter.pen_down()
plotter.write(hpgl.PR([(0,1000), (1000,0), (0,-1000), (-1000,0)]))
plotter.pen_up()

draw_circle(200,5)
draw_circle(500,10)
plotter.select_pen(2)

draw_circle(1000,20)
plotter.select_pen(3)

draw_circle(1500,45)
plotter.select_pen(5)

draw_circle(2000,90)


plotter.write(hpgl.PU([]))
plotter.select_pen(0)

plotter.flush()

