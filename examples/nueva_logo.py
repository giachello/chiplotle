import math
from chiplotle import *
from chiplotle.plotters.baseplotter import _BasePlotter

plotter : _BasePlotter = instantiate_plotters( )[0]

plotter.select_pen(3)

plotter.write(hpgl.PU([(2375, 1500)]))

coords = [(2375, 1500), (2375, 6000), (3708, 4875)] 
plotter.write(hpgl.PD(coords))

plotter.write(hpgl.PU([(6292, 2562)]))

coords2 = [(6292, 2562), (7625, 1500), (7625, 6000)]
plotter.write(hpgl.PD(coords2))


circles_centers = []
radius = 550
for n in range(0,8):
    circles_centers.append((5000+radius*math.cos(2*math.pi/8*n),3750+radius*math.sin(2*math.pi/8*n)))

for i in circles_centers:
    plotter.write(hpgl.PU())
    plotter.write(hpgl.PA([i]))
    plotter.write(hpgl.CI(100,10))

oval_centers = []
radius = 1200
for n in range(0,8):
    oval_centers.append((5000+radius*math.cos(2*math.pi/8*n),3750+radius*math.sin(2*math.pi/8*n)))

for m in range(0,8):
    i = oval_centers[m]
    long_radius = 400
    short_radius = 200
    arc = []

    for n in range(0,37):
        point_x = i[0]+long_radius*math.cos(2*math.pi/72*(n+18))
        point_y = i[1]+short_radius*math.sin(2*math.pi/72*(n+18))
        r = math.sqrt((i[0]-point_x)**2+(i[1]-point_y)**2)
        rotated_x = math.cos(2*math.pi/8*m)*(point_x-i[0])-math.sin(2*math.pi/8*m)*(point_y-i[1])+i[0]
        rotated_y = math.sin(2*math.pi/8*m)*(point_x-i[0])+math.cos(2*math.pi/8*m)*(point_y-i[1])+i[1]
        arc.append((rotated_x,rotated_y))

    plotter.write(hpgl.PU())
    plotter.write(hpgl.PA([arc[0]]))
    for j in range(1,37):
        plotter.write(hpgl.PD([arc[j]]))


plotter.write(hpgl.PU([(3000,500)]))
plotter.write(hpgl.SI(1,1.5))
plotter.write(hpgl.LB("GO MAVS!"))
plotter.select_pen(0)
plotter.flush()
