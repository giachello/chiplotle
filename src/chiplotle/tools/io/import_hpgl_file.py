from chiplotle.tools.hpgltools.inflate_hpgl_string import inflate_hpgl_string


def import_hpgl_file(filename, filter_commands=None):
    """Reads a text HPGL file and "inflates" it by creating
    Chiplotle-HPGL class instances of the found HPGL commands.

    Example::

        chiplotle> square = import_hpgl_file('examples/square.hpgl')
        chiplotle> square
        [SP(pen=1), PU(xy=[ 100.  100.]), PD(xy=[ 200.  100.]),
        PD(xy=[ 200.  200.]), PD(xy=[ 100.  200.]),
        PD(xy=[ 100.  100.]), SP(pen=0)]
    """

    with open(filename, "r", encoding="utf8") as f:
        file_contents = f.read()
        return inflate_hpgl_string(file_contents, filter_commands)
