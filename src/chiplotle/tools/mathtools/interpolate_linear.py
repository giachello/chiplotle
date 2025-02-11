

def interpolate_linear(y1, y2, mu):
    """Linear interpolate `y1` and `y2` with `mu` normalized ``[0, 1]``.

    Example::

        >>> mathtools.interpolate_linear(0, 1, 0.5)
        0.5
    """

    return y1 * (1 - mu) + y2 * mu
