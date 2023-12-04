from chiplotle.hpgl.commands import SI
import pytest


def test_SI_01():
    """SI has default values."""
    t = SI()
    assert t.format == b"SI;"


def test_SI_02():
    t = SI(3, 2)
    assert t.format == b"SI3.00,2.00;"


def test_SI_03():
    t = SI(3)
    with pytest.raises(Warning):
        t.format
