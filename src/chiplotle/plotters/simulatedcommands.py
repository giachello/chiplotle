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


simulatedHPGLcommands = [ "CI", "AA", "AR" ]

def deg_to_rad(angle:float):
    return angle/180.0*math.pi

def rad_to_deg(angle:float):
    return angle/math.pi*180


def simulated_CI(radius, chord_angle : float = 72):
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

def simulated_AA(current_x, current_y, center_x, center_y, arc_angle, chord_angle : float = 5):
    """ Create a sequence of simple HPGL to simulate AA command. 
    This is useful for plotters that don't have advanced commands 
    like the HP 7440A. """
    # chord angle normalization, per 7440A Programming Manual, page 7-9
    if chord_angle is None:
        chord_angle = 5
    if chord_angle > 180.0: 
        chord_angle = 360.0 - chord_angle
    if chord_angle == 0:
        chord_angle = 0.36
    segments = int(360.0/chord_angle)
    start_angle = math.atan2(current_y-center_y,current_x-center_x)
    radius = math.sqrt((current_y-center_y)**2+(current_x-center_x)**2)
    end_angle = start_angle+deg_to_rad(arc_angle)
    # arc_circle doesn't do clockwise, so switch angles if necessary
    flipped : bool = False
    if end_angle < start_angle:
        t = start_angle
        start_angle = end_angle 
        end_angle = t
        flipped = True
        
    c = geometry.shapes.arc_circle(radius,start_angle,end_angle,segments).points
    plot = []

    if flipped:
        c = reversed(c)
    for p in c:
        p.x += center_x
        p.y += center_y    
        plot.append(hpgl.PA([p]))

    return plot

def simulated_AR(center_x, center_y, arc_angle, chord_angle : float = 5):
    """ Create a sequence of simple HPGL to simulate AA command. 
    This is useful for plotters that don't have advanced commands 
    like the HP 7440A. """
    # chord angle normalization, per 7440A Programming Manual, page 7-9
    if chord_angle is None:
        chord_angle = 5
    if chord_angle > 180.0: 
        chord_angle = 360.0 - chord_angle
    if chord_angle == 0:
        chord_angle = 0.36
    segments = int(360.0/chord_angle)
    start_angle = math.atan2(-center_y,-center_x)
    radius = math.sqrt((center_y)**2+(center_x)**2)
    end_angle = start_angle+deg_to_rad(arc_angle)
    # arc_circle doesn't do clockwise, so switch angles if necessary
    flipped : bool = False
    if end_angle < start_angle:
        t = start_angle
        start_angle = end_angle 
        end_angle = t
        flipped = True
        
    c = geometry.shapes.arc_circle(radius,start_angle,end_angle,segments).points
    plot = []
    prev_x = -center_x
    prev_y = -center_y

    if flipped:
        c = reversed(c)
    for p in c:
        plot.append(hpgl.PR([(p.x - prev_x,p.y - prev_y)]))
        prev_x = p.x
        prev_y = p.y
      
    return plot
