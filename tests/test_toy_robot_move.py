import pytest
from toy_robot import Robot, Table
from toy_robot.command import Position, Direction

def test_move_ignored_when_not_is_placed():
    r = Robot(Table())
    success = r.move()  # should not crash or change state

    assert success is False
    assert r._pos is None
    assert r._facing is None
    assert r.is_placed() is False

@pytest.mark.parametrize(
    "start_pos, facing, expected_pos",
    [
        (Position(1, 1), Direction.NORTH, Position(1, 2)),
        (Position(1, 1), Direction.EAST,  Position(2, 1)),
        (Position(1, 1), Direction.SOUTH, Position(1, 0)),
        (Position(1, 1), Direction.WEST,  Position(0, 1)),
    ],
)
def test_move_one_step_interior(start_pos, facing, expected_pos):
    r = Robot(Table())
    assert r.place(start_pos, facing)
    success = r.move()

    assert success is True
    assert r._pos == expected_pos
    assert r._facing == facing  # move doesn't change facing

@pytest.mark.parametrize(
    "start_pos, facing",
    [
        (Position(0, 4), Direction.NORTH),  # top edge
        (Position(4, 0), Direction.EAST),   # right edge
        (Position(0, 0), Direction.SOUTH),  # bottom edge
        (Position(0, 0), Direction.WEST),   # left edge
    ],
)
def test_move_at_boundary_is_ignored(start_pos, facing):
    r = Robot(Table())  # default 5x5 (0..4)
    assert r.place(start_pos, facing)
    before = r._pos
    success = r.move()

    assert success is False
    assert r._pos == before  # unchanged
    assert r._facing == facing


def test_multiple_moves_stop_at_edge():
    r = Robot(Table())
    r.place(Position(0, 0), Direction.EAST)
    for _ in range(10):  # more than enough to hit the edge
        r.move()
    # should stop at x=4 on a 5x5 table
    assert r._pos == Position(4, 0)
    assert r._facing == Direction.EAST
