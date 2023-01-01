#
# These functions provide the simulation of complex commands like CI
# using simple primites like PA, PD, PR. This is useful for plotters 
# that don't understand advanced commands like the HP 7440A without a 
# Graphics Enhancement Cartridge.
#
#
from chiplotle import *
import math
import chiplotle.geometry as geometry


simulatedHPGLcommands = [ "CI", "AA" ]


def simulated_CI(radius, chord_angle = 72):
    """ Create a sequence of simple HPGL to simulate CI command. 
    This is useful for plotters that don't have advanced commands 
    like the HP 7440A. """
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

def simulated_AA(current_x, current_y, center_x, center_y, arc_angle, chord_angle = 5):
    """ Create a sequence of simple HPGL to simulate AA command. 
    This is useful for plotters that don't have advanced commands 
    like the HP 7440A. """
    segments = int(360.0/chord_angle)
    start_angle = math.atan2(current_y-center_y,current_x-center_x)
    radius = math.sqrt((current_y-center_y)**2+(current_x-center_x)**2)
    c = geometry.shapes.arc_circle(radius,start_angle,arc_angle,segments).points
    plot = []
    for p in c:
        p.x += center_x
        p.y += center_y    
        plot.append(hpgl.PA([p]))

    return plot
