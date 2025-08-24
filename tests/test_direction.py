import pytest

from toy_robot.command import Direction

def test_left_turn():
    assert Direction.NORTH.left() == Direction.WEST
    assert Direction.WEST.left() == Direction.SOUTH
    assert Direction.SOUTH.left() == Direction.EAST
    assert Direction.EAST.left() == Direction.NORTH

def test_right_turn():
    assert Direction.NORTH.right() == Direction.EAST
    assert Direction.EAST.right() == Direction.SOUTH
    assert Direction.SOUTH.right() == Direction.WEST
    assert Direction.WEST.right() == Direction.NORTH
