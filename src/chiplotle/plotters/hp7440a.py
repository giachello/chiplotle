"""
 *  This file is part of chiplotle.
 *
 *  http://music.columbia.edu/cmc/chiplotle
"""
from chiplotle.plotters.drawingplotter import _DrawingPlotter


class HP7440A(_DrawingPlotter):
    def __init__(self, ser, **kwargs):
        self.allowedHPGLCommands = (
            "\x1b.",
            "CA", "CP", "CS", "DC", "DF", "DI", "DP", "DR", "IM", "IN", "IP", "IW", "LB", "LT", "OA",
            "OC", "OD", "OE", "OF", "OH", "OI", "OO", "OP", "OS", "OW", "PA", "PD", "PR", "PU", "RO",
            "SA", "SC", "SI", "SL", "SM", "SP", "SR", "SS", "TL", "UC", "VS", "XT", "YT",
        )
        _DrawingPlotter.__init__(self, ser, **kwargs)
        self.type = "HP7440A"
