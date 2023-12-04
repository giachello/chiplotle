from pytest import raises

from chiplotle.geometry.core.group import Group
from chiplotle.geometry.core.path import Path


def test_shapes_group_add_01():
    """Group + int is not allowed."""
    a = Group([Path([(1, 2), (3, 4)]), Path([(5, 6), (7, 8)])])
    with raises(TypeError):
        a + 2


def test_shapes_group_add_02():
    """int + Group is not allowed."""
    a = Group([Path([(1, 2), (3, 4)]), Path([(5, 6), (7, 8)])])
    with raises(TypeError):
        2 + a
