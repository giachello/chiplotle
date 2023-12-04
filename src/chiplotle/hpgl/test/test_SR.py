from chiplotle.hpgl.commands import SR
import pytest


def test_SR_01():
    """SR can be initialized empty."""
    t = SR()
    assert t.format == b"SR;"


def test_SR_02():
    t = SR(3, 2)
    assert t.format == b"SR3.00,2.00;"


def test_SR_03():
    t = SR(3)
    with pytest.raises(Warning):
        t.format
