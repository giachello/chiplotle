from chiplotle.geometry.core.coordinatearray import CoordinateArray, Coordinate
import math
from chiplotle import *
import chiplotle.geometry as geometry

MAXPOLY = 1024
intersect_skew = 0.0000001

def fill(polygon: CoordinateArray, numpoints : int, point1: Coordinate,
	  filltype: int,  spacing: float,
	  hatchangle: float) :
    """ Create a plot structure for a given polygon and filltype
        polygon: definition of the polygon, as a set of pairs of coordinates, 
        e.g. for a rectangle (a,b, b,c, c,d, d,a)
        numpoints: the number of points in the polygon - 1, e.g. rectangle: 7
        point1: position of the polygon
        filltype: 0-2 Full, 3: horizontal, 4: crosshatch
        spacing: the spacing between the hatches
        hatchangle: the angle of the hatching
    """
#	typedef struct {
#		double x, y;
#	} HPGL_Pt2;

    pxmin: float
    pxmax: float
    pymin: float
    pymax: float
    polyxmin: float
    polyymin: float
    polyxmax: float
    polyymax: float
    scanx1: float
    scanx2: float
    scany1: float
    scany2: float
    segment : CoordinateArray
    tmp : Coordinate
    segx: float
    segy: float
#	static int i;		/* to please valgrind when debugging memory accesses */
    j: int
    k: int
    jj: int
    kk: int
    numlines: int
    penwidth: float
    rot_ang : float
    pxdiff = 0.0
    pydiff = 0.0
    avx: float
    avy: float
    bvx: float
    bvy: float
    ax: float
    ay: float
    bx: float
    by: float
    atx: float
    aty: float
    btx: float
    bty: float
    mu: float


    def _fill_horiz():
        nonlocal pxmin, pxmax, pymin, pymax, polyxmin, polyymin, polyxmax, polyymax
        nonlocal scanx1, scanx2, scany1, scany2, segment, tmp, segx, segy
        nonlocal j,k,jj,kk, numlines, penwidth, rot_ang,pxdiff,pydiff
        nonlocal avx,avy,bvx, bvy,ax,ay,bx,by,atx,aty,btx,bty,mu

        pxmin = point1.x - 0.5
        pymin = point1.y - 0.5
        pxmax = polyxmax
        pymax = polyymax
        
        if polyxmin == polyxmax and polyymin == polyymax:
            print("zero area polygon\n")
            return

        pydiff = pymax - pymin
        pxdiff = pxmax - pxmin
        if hatchangle != 0.0:
            rot_ang = math.tan(math.pi * hatchangle / 180.0)
            pymin = pymin - rot_ang * pxdiff
            pymax = pymax + rot_ang * pxdiff

        numlines = int(abs(1. + (pymax - pymin + penwidth) / penwidth))

    # start at lowest y , run scanlines parallel x across polygon 
    # looking for intersections with edges 

        pydiff = 0.0

        if hatchangle != 0.0:
            pydiff = math.tan(math.pi * hatchangle / 180.) * pxdiff

        for i in range(0, numlines + 1):	# /* for all scanlines ... */
            k = -1
            segment = CoordinateArray()
            scany1 = pymin + float( i *penwidth )
            scany2 = scany1 + pydiff
            if scany1 >= pymax or scany1 <= pymin:
                continue

            if scany2 < polyymin:
                continue
    # /* coefficients for current scan line */
            bx = pxmin
            btx = pxmax
            by = scany1
            bty = scany2
            bvx = btx - bx
            bvy = bty - by

            for j in range(0, numpoints + 1, 2): 	# /*for all polygon edges */
                ax = polygon[j].x
                ay = polygon[j].y
                atx = polygon[j + 1].x
                aty = polygon[j + 1].y
                avx = atx - ax
                avy = aty - ay

                if abs(bvy * avx - avy * bvx) < 1.e-8:
                    continue
                mu = (avx * (ay - by) +
                    avy * (bx - ax)) / (bvy * avx - avy * bvx)

    # /*determine coordinates of intersection */
                if mu >= 0.0 and mu <= 1.01: 
                    segx = bx + mu * bvx	# /*x coordinate of intersection */
                    segy = by + mu * bvy	# /*y coordinate of intersection */
                else:
                    continue

                if ((segy < min(polygon[j].y, polygon[j + 1].y) - intersect_skew)
                    or (segy > max(polygon[j].y, polygon[j + 1].y) + intersect_skew)
                    or (segx < min(polygon[j].x, polygon[j + 1].x) - intersect_skew)
                    or (segx > max( polygon[j].x, polygon[j + 1].x) + intersect_skew)): 
                    print("intersection  at %f %f is not within (%f,%f)-(%f,%f)\n" % 
                    (segx,segy,polygon[j].x,polygon[j].y,polygon[j+1].x,polygon[j+1].y ))
                else:
                    skip_rest : bool = False
                    for kk in range( 0, k + 1): 
                        if abs(segment[kk].x - segx) < 1.e-8:
                            skip_rest = True
                    if not skip_rest:
                        k = k + 1
                        segment.append(Coordinate(segx, segy))

        # /*fprintf(stderr,"fill: intersection %d with line %d at (%f %f)\n",k,j,segx,segy);*/
                        if k > 0:
                            for jj in range( 0, k): 
                                if segment[k].x < segment[jj].x:
                                    tmp = segment[jj]
                                    segment[jj] = segment[k]
                                    segment[k] = tmp

                        #	/* if not the first intersection */
                #	/* if crossing withing range */
                continue
            #		/*next edge */

            if k > 0:
    #/*fprintf(stderr, "%d segments for scanline %d\n",k,i);*/
                for j in range( 0, k, 2): # this one was strict < 
    #/*fprintf(stderr, "segment (%f,%f)-(%f,%f)\n",segment[j].x,segment[j].y,segment[j+1].x,segment[j+1].y);*/
                    p = Coordinate(segment[j].x, segment[j].y)
    #                Pen_action_to_tmpfile(MOVE_TO, &p, scale_flag);
                    plot.append(hpgl.PU([p]))
                    p = Coordinate( segment[j + 1].x, segment[j + 1].y)
    #				Pen_action_to_tmpfile(DRAW_TO, &p, scale_flag);
                    plot.append(hpgl.PD([p]))  

        #			/* next scanline */


#      FILL_VERT:
    def _fill_vert():
        nonlocal pxmin, pxmax, pymin, pymax, polyxmin, polyymin, polyxmax, polyymax
        nonlocal scanx1, scanx2, scany1, scany2, segment, tmp, segx, segy
        nonlocal j,k,jj,kk, numlines, penwidth, rot_ang,pxdiff,pydiff
        nonlocal avx,avy,bvx, bvy,ax,ay,bx,by,atx,aty,btx,bty,mu

        pxmin = point1.x
        pymin = point1.y
        pxmax = polyxmax
        pymax = polyymax

        pydiff = pymax - pymin
        if hatchangle != 0.0: 
            rot_ang = math.tan(math.pi * hatchangle / 180.)
            pxmin = pxmin - rot_ang * pydiff
            pxmax = pxmax + rot_ang * pydiff

        pymin = pymin - 1.
        pymax = pymax + 1.

    #	PlotCmd_to_tmpfile(DEF_LA);
    #	Line_Attr_to_tmpfile(LineAttrEnd, LAE_butt);

        numlines = int(abs(1.0 + (pxmax - pxmin + penwidth) / penwidth))

    #/*fprintf(stderr,"numlines = %d\n",numlines);*/

        pxdiff = 0.0
        if hatchangle != 0.0:
            pxdiff = math.tan(math.pi * hatchangle / 180.) * (pymax - pymin)
        for i in range( 0, numlines + 1): #	/* for all scanlines ... */
            k = -1
            segment = CoordArray()
            scanx1 = pxmin + i *penwidth
            if scanx1 >= pxmax or scanx1 <= pxmin:
                continue
            scanx2 = scanx1 - pxdiff
    #/*		if (scanx2 < polyxmin)
    #			continue;*/
    #/* coefficients for current scan line */
            bx = scanx1
            btx = scanx2
            by = pymin
            bty = pymax
            bvx = btx - bx
            bvy = bty - by

            for j in range(0, numpoints + 1, 2): #	/*for all polygon edges */
                ax = polygon[j].x
                ay = polygon[j].y
                atx = polygon[j + 1].x
                aty = polygon[j + 1].y
                avx = atx - ax
                avy = aty - ay

                if abs(bvy * avx - avy * bvx) < 1.e-8:
                    continue
                mu = (avx * (ay - by) +
                    avy * (bx - ax)) / (bvy * avx - avy * bvx)

    #/*determine coordinates of intersection */
                if mu >= 0. and mu <= 1.01:
                    segx = bx + mu * bvx #	/*x coordinate of intersection */
                    segy = by + mu * bvy #	/*y coordinate of intersection */
                else:
                    continue

                if ((segy < min(polygon[j].y, polygon[j + 1].y) - intersect_skew)
                    or (segy > max(polygon[j].y, polygon[j + 1].y) + intersect_skew)
                    or (segx < min(polygon[j].x, polygon[j + 1].x) - intersect_skew)
                    or (segx > max(polygon[j].x, polygon[j + 1].x) + intersect_skew)):
                    print("intersection  at %f %f is not within (%f,%f)-(%f,%f)\n" % 
                    (segx,segy,polygon[j].x,polygon[j].y,polygon[j+1].x,polygon[j+1].y ))
                else:
                    skip_rest : bool = False
                    for kk in range( 0, k + 1): 
                        if abs(segment[kk].y - segy) < 1.e-8:
                            skip_rest = True
                    if not skip_rest:
                        k = k + 1
                        segment.append(Coordinate(segx, segy))

        #/*fprintf(stderr,"fill: intersection %d with line %d at (%f %f)\n",k,j,segx,segy);*/
                        if k > 0:
                            for jj in range(0, k): # this was a strict <
                                if segment[k].y < segment[jj].y:
                                    tmp = segment[jj]
                                    segment[jj] = segment[k]
                                    segment[k] = tmp
                        #	/* if not the first intersection */
                #	/* if crossing withing range */
                continue
            #		/*next edge */


            if k > 0:
    #/* fprintf(stderr, "%d segments for scanline %d\n",k,i);*/
                for j in range( 0, k, 2):
    #/*fprintf(stderr, "segment (%f,%f)-(%f,%f)\n",segment[j].x,segment[j].y,segment[j+1].x,segment[j+1].y);*/
                    p = Coordinate(segment[j].x, segment[j].y)
    #                Pen_action_to_tmpfile(MOVE_TO, &p, scale_flag);
                    plot.append(hpgl.PU([p]))
                    p = Coordinate( segment[j + 1].x, segment[j + 1].y)
    #               Pen_action_to_tmpfile(DRAW_TO, &p, scale_flag);
                    plot.append(hpgl.PD([p]))

        #			/* next scanline */

#	PEN_W SafePenW = pt.width[1];
#	LineEnds SafeLineEnd = CurrentLineEnd;
#	CurrentLineEnd = LAE_butt;

    plot = [ hpgl.PU() ]

    penwidth = 0.1

#	PlotCmd_to_tmpfile(DEF_PW);
#	Pen_Width_to_tmpfile(1, penwidth);

#	PlotCmd_to_tmpfile(DEF_LA);
#	Line_Attr_to_tmpfile(LineAttrEnd, LAE_round);

    if filltype > 2:
        penwidth = spacing

    polyxmin = 100000.
    polyymin = 100000.
    polyxmax = -100000.
    polyymax = -100000.
    for i in range(0, numpoints+1):          # Check the range

        polyxmin = min(polyxmin, polygon[i].x)
        polyymin = min(polyymin, polygon[i].y)

        polyxmax = max(polyxmax, polygon[i].x)
        polyymax = max(polyymax, polygon[i].y)

    if hatchangle > 89.9 and hatchangle < 180.0:
        hatchangle = hatchangle - 90.
        _fill_vert()
    else:
        _fill_horiz()
        if filltype == 4:
            _fill_vert()

#	CurrentLineEnd = SafeLineEnd;
#	PlotCmd_to_tmpfile(DEF_PW);
#	Pen_Width_to_tmpfile(1, SafePenW);
#	PlotCmd_to_tmpfile(DEF_LA);
#	Line_Attr_to_tmpfile(LineAttrEnd, SafeLineEnd);
    return plot
