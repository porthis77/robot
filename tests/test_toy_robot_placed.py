import pytest
from toy_robot import Robot, Table
from toy_robot.command import Position, Direction

def test_place_valid_position_returns_true_and_sets_state():
    r = Robot(Table())
    success = r.place(Position(1, 2), Direction.EAST)

    assert success is True
    assert r._pos == Position(1, 2)
    assert r._facing == Direction.EAST

def test_place_out_of_bounds_returns_false_and_does_not_set_state():
    r = Robot(Table())
    success = r.place(Position(10, 10), Direction.NORTH)

    assert success is False
    assert r._pos is None
    assert r._facing is None

def test_place_on_edge_is_allowed():
    r = Robot(Table())
    success = r.place(Position(4, 4), Direction.SOUTH)  # edge of 5x5 table

    assert success is True
    assert r._pos == Position(4, 4)
    assert r._facing == Direction.SOUTH

def test_repeated_place_overwrites_previous_state():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)
    success = r.place(Position(2, 3), Direction.WEST)

    assert success is True
    assert r._pos == Position(2, 3)
    assert r._facing == Direction.WEST

def test_place_negative_coordinates_is_invalid():
    r = Robot(Table())
    success = r.place(Position(-1, 0), Direction.NORTH)

    assert success is False
    assert r._pos is None
    assert r._facing is None
