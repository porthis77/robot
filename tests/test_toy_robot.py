# test_robot_to_string.py
import pytest
from toy_robot import Robot, Table
from toy_robot.command import Position, Direction, Command, CommandType

# -- test __str__

def test_to_string_when_not_placed():
    r = Robot(Table())
    assert str(r) == "Robot not placed"

def test_to_string_after_place():
    r = Robot(Table())
    r.place(Position(1, 2), Direction.NORTH)
    assert str(r) == "Robot at (1,2) facing NORTH"

def test_to_string_after_move_and_turn():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.NORTH)  # start
    r.move()   # -> (0,1)
    r.right()  # EAST
    r.move()   # -> (1,1)
    assert str(r) == "Robot at (1,1) facing EAST"

def test_to_string_after_replacement():
    r = Robot(Table())
    r.place(Position(2, 2), Direction.WEST)
    assert str(r) == "Robot at (2,2) facing WEST"
    r.place(Position(4, 0), Direction.SOUTH)  # re-place should overwrite
    assert str(r) == "Robot at (4,0) facing SOUTH"

def test_to_string_on_edges():
    r = Robot(Table())
    r.place(Position(4, 4), Direction.WEST)   # top-right corner on 5x5
    assert str(r) == "Robot at (4,4) facing WEST"

# -- test execute_command

def test_place_success_returns_true_and_sets_state():
    r = Robot(Table())
    cmd = Command(CommandType.PLACE, x=1, y=2, facing=Direction.EAST)
    ret = r.execute_command(cmd)
    assert ret is True
    assert r.is_placed()
    assert r.pos.x == 1
    assert r.pos.y == 2
    assert r.facing == Direction.EAST

def test_place_out_of_bounds_returns_false_and_not_placed():
    r = Robot(Table())  # default 5x5 => x,y must be in [0..4]
    cmd = Command(CommandType.PLACE, x=5, y=0, facing=Direction.NORTH)
    ret = r.execute_command(cmd)
    assert ret is False
    assert r.is_placed() is False
    assert r.pos is None
    assert r.facing is None

def test_move_before_place_returns_false():
    r = Robot(Table())
    ret = r.execute_command(Command(CommandType.MOVE))
    assert ret is False
    assert r.is_placed() is False

def test_move_after_place_advances_and_returns_true():
    r = Robot(Table())
    r.execute_command(Command(CommandType.PLACE, x=0, y=0, facing=Direction.NORTH))
    ret = r.execute_command(Command(CommandType.MOVE))
    assert ret is True
    assert r.pos.x == 0
    assert r.pos.y == 1
    assert r.facing == Direction.NORTH

def test_left_right_before_place_return_false():
    r = Robot(Table())
    assert r.execute_command(Command(CommandType.LEFT)) is False
    assert r.execute_command(Command(CommandType.RIGHT)) is False
    assert r.is_placed() is False

def test_left_changes_facing_and_returns_true():
    r = Robot(Table())
    r.execute_command(Command(CommandType.PLACE, x=1, y=1, facing=Direction.NORTH))
    ret = r.execute_command(Command(CommandType.LEFT))
    assert ret is True
    assert r.pos.x == 1
    assert r.pos.y == 1
    assert r.facing == Direction.WEST

def test_right_changes_facing_and_returns_true():
    r = Robot(Table())
    r.execute_command(Command(CommandType.PLACE, x=1, y=1, facing=Direction.NORTH))
    ret = r.execute_command(Command(CommandType.RIGHT))
    assert ret is True
    assert r.pos.x == 1
    assert r.pos.y == 1
    assert r.facing == Direction.EAST

def test_report_before_place_returns_none():
    r = Robot(Table())
    ret = r.execute_command(Command(CommandType.REPORT))
    assert ret == 'Robot not placed'

def test_report_after_place_returns_string():
    r = Robot(Table())
    r.execute_command(Command(CommandType.PLACE, x=2, y=3, facing=Direction.SOUTH))
    ret = r.execute_command(Command(CommandType.REPORT))
    assert r.report() == "x:2,y:3,facing:SOUTH"

def test_move_blocked_at_edge_returns_false_and_position_unchanged():
    r = Robot(Table())
    r.execute_command(Command(CommandType.PLACE, x=0, y=4, facing=Direction.NORTH))  # top edge
    before_x, before_y, before_facing = r.pos.x, r.pos.y, r.facing
    ret = r.execute_command(Command(CommandType.MOVE))
    assert ret is False
    assert (r.pos.x, r.pos.y, r.facing) == (before_x, before_y, before_facing)
