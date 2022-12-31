#
# These functions provide the simulation of complex commands like CI
# using simple primites like PA, PD, PR. This is useful for plotters 
# that don't understand advanced commands like the HP 7440A without a 
# Graphics Enhancement Cartridge.
#
#
from chiplotle import *
import chiplotle.geometry as geometry


simulatedHPGLcommands = [ "CI" ]


def simulated_CI(radius, chord_angle):
    """ Create a sequence of simple HPGL to simulate CI command. 
    This is useful for plotters that don't have advanced commands 
    like the HP 7440A. """
    if chord_angle is None:
        segments = 72
    else:
        segments = int(360.0/chord_angle)
    c = geometry.shapes.circle(radius,segments).points
    c2 = CoordinateArray()
    for i in range(1,len(c)):
        c2.append(c[i]-c[i-1])
    c2.append(c[0]-c[len(c)-1])

    plot = [hpgl.PU()]
    plot.append(hpgl.PR([c[0]]))
    plot.append(hpgl.PD())
    plot.append(hpgl.PR(c2))
    plot.append(hpgl.PU())
    plot.append(hpgl.PR([-c[0]]))

    return plot
