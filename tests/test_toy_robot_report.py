import pytest
from toy_robot import Robot, Table
from toy_robot.command import Position, Direction

def test_report_returns_none_if_not_placed():
    r = Robot(Table())
    assert r.report() == "Robot not placed"

def test_report_after_valid_place():
    r = Robot(Table())
    r.place(Position(1, 2), Direction.NORTH)
    assert r.report() == "x:1,y:2,facing:NORTH"

def test_report_after_move_and_turns():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)
    r.move()        # -> (0,1)
    r.right()       # facing EAST
    r.move()        # -> (1,1)
    assert r.report() == "x:1,y:1,facing:EAST"

def test_report_updates_after_replacement():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)
    r.place(Position(2, 3), Direction.WEST)
    assert r.report() == "x:2,y:3,facing:WEST"
