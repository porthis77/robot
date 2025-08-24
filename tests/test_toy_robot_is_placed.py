import pytest
from toy_robot import Robot, Table
from toy_robot.command import Position, Direction

def test_robot_not_is_placed_initially():
    r = Robot(Table())
    assert r.is_placed() is False

def test_robot_becomes_is_placed_after_valid_place():
    r = Robot(Table())
    success = r.place(Position(0, 0), Direction.NORTH)
    assert success is True
    assert r.is_placed() is True

def test_robot_not_is_placed_if_place_out_of_bounds():
    r = Robot(Table())
    success = r.place(Position(10, 10), Direction.NORTH)
    assert success is False
    assert r.is_placed() is False

def test_replacing_still_results_in_is_placed():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)
    r.place(Position(2, 2), Direction.WEST)
    assert r.is_placed() is True
    assert r.pos == Position(2, 2)
    assert r.facing == Direction.WEST
