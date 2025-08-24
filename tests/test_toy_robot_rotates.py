import pytest
from toy_robot.robot import Robot, Table
from toy_robot.command import Position, Direction

def test_left_turn_changes_direction():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)

    r.left()
    assert r._facing == Direction.WEST

    r.left()
    assert r._facing == Direction.SOUTH

    r.left()
    assert r._facing == Direction.EAST

    r.left()
    assert r._facing == Direction.NORTH  # full cycle

def test_right_turn_changes_direction():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)

    r.right()
    assert r._facing == Direction.EAST

    r.right()
    assert r._facing == Direction.SOUTH

    r.right()
    assert r._facing == Direction.WEST

    r.right()
    assert r._facing == Direction.NORTH  # full cycle

def test_turns_ignored_if_not_placed():
    r = Robot(Table())
    # robot not placed
    r.left()
    assert r._facing is None
    assert r._pos is None
        
    r.right()
    assert r._facing is None
    assert r._pos is None
