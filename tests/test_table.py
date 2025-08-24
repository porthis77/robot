import pytest
from toy_robot import Table
from toy_robot.command import Position

@pytest.mark.parametrize("x,y,expected", [
    (0, 0, True),     # bottom-left corner
    (4, 0, True),     # bottom-right corner
    (0, 4, True),     # top-left corner
    (4, 4, True),     # top-right corner
    (5, 4, False),    # just outside right edge
    (4, 5, False),    # just outside top edge
    (-1, 2, False),   # left of board
    (2, -1, False),   # below board
])
def test_default_table_various_points(x, y, expected):
    t = Table()
    assert t.is_valid(Position(x, y)) is expected

def test_custom_table_size():
    t = Table(width=3, height=2)
    # inside
    assert t.is_valid(Position(0, 0))
    assert t.is_valid(Position(2, 1))
   
    # outside
    assert not t.is_valid(Position(3, 1))
    assert not t.is_valid(Position(2, 2))


