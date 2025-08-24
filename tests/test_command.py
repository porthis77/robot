# test_command_is_valid_exhaustive.py
import pytest
from toy_robot.command import *  # uses your src/toy_robot/command.py

@pytest.mark.parametrize("line", 
[
    "MOVE", "LEFT", "RIGHT", "REPORT",
    " move", "LEFT  ", "  right ", "\tREPORT\t",
    "MoVe", "lEfT", "Right", "rePort",
    "\nMOVE\n", " \t LEFT \t ",
])
def test_simple_commands_valid(line):
    assert CommandParser.is_valid(line) is True

@pytest.mark.parametrize("line", [
    "", "   ", "\t", "\n",
    "# comment", "  # another comment",
    "MOVEE", "LE FFT", "RE POR T",
    "REPORT NOW",   # extra token
    "MOVE 1",       # unexpected arg
])
def test_simple_commands_invalid(line):
    assert CommandParser.is_valid(line) is False


# ---------- PLACE: VALID FORMS ----------
@pytest.mark.parametrize("line", [
    # minimal spacing
    "PLACE 0,0,NORTH",
    # various spaces around commas
    "PLACE 1, 2, WEST",
    "PLACE  1 ,2 ,EAST",
    "PLACE  1 ,  2 ,  SOUTH  ",
    # tabs/newlines around the args
    "PLACE\t3,4,NORTH",
    "  PLACE\t 4 ,\t 0 ,\t WEST  ",
    "PLACE 2,3,\nEAST".replace("\n", ""),  # still no whitespace in args list
    # signs and negatives
    "PLACE -1,0,NORTH",
    "PLACE 0,-2,SOUTH",
    "PLACE +2,+3,EAST",  # int("+2") is valid in Python
    # mixed case direction
    "PLACE 4,4,nOrth",
    "place 1,2,west",
])
def test_place_valid(line):
    assert CommandParser.is_valid(line) is True


# ---------- PLACE: INVALID FORMS (STRUCTURE) ----------

@pytest.mark.parametrize("line", [
    "PLACE",                    # no args
    "PLACE   ",                 # no args
    "PLACE 1,2",                # missing direction
    "PLACE 1,2,",               # trailing comma, missing direction
    "PLACE , , ",               # empty parts
    "PLACE 1 2 NORTH",          # spaces instead of commas
    "PLACE 1;2;NORTH",          # wrong delimiter
    "PLACE 1,2,NORTH,EXTRA",    # too many parts
    "PLACE ,2,NORTH",           # missing X
    "PLACE 1,,NORTH",           # missing Y
    "PLACE 1,2, NORTH WEST",    # two-word direction
    "PLACE1,2,NORTH",           # no space after PLACE (we require one)
    " PLACE1,2,NORTH",          # still no separating whitespace
])
def test_place_invalid_structure(line):
    assert CommandParser.is_valid(line) is False


# ---------- PLACE: INVALID TYPES / VALUES ----------

@pytest.mark.parametrize("line", [
    "PLACE x,2,NORTH",      # non-int X
    "PLACE 1,y,NORTH",      # non-int Y
    "PLACE 1,2,UP",         # invalid direction
    "PLACE 1,2,NORTHEAST",  # invalid direction
    "PLACE 1,2,NO RTH",     # split direction token
    "PLACE 1.0,2,NORTH",    # float not allowed
    "PLACE 1,2.5,NORTH",
])
def test_place_invalid_values(line):
    assert CommandParser.is_valid(line) is False


# ---------- EDGES AROUND WHITESPACE SPLIT ----------

@pytest.mark.parametrize("line, expected", [
    ("PLACE 1,2,NORTH", True),
    ("PLACE    1,2,NORTH", True),
    ("PLACE\t1,2,NORTH", True),
    ("  PLACE   1, 2 ,  NORTH  ", True),
    ("PLACE", False),                 # ensures split(None,1) yields only ["PLACE"]
    ("PLACE    ", False),
])
def test_place_split_behavior_via_validator(line, expected):
    assert CommandParser.is_valid(line) is expected


# ---------- COMMENT & BLANK HANDLING ----------

@pytest.mark.parametrize("line", [
    "#PLACE 0,0,NORTH",
    "# MOVE",
    "   # indented",
    "\t# tab comment",
])
def test_comments(line):
    assert CommandParser.is_valid(line) is False

# ----------------- SIMPLE COMMANDS -----------------

@pytest.mark.parametrize(
    "line, expected_type",
    [
        ("MOVE", CommandType.MOVE),
        ("LEFT", CommandType.LEFT),
        ("RIGHT", CommandType.RIGHT),
        ("REPORT", CommandType.REPORT),
        (" move ", CommandType.MOVE),
        ("\tLEFT\t", CommandType.LEFT),
        ("rIgHt", CommandType.RIGHT),
        ("  report  ", CommandType.REPORT),
    ],
)
def test_parse_simple_commands(line, expected_type):
    cmd = CommandParser.parse(line)
    assert cmd is not None
    assert isinstance(cmd, Command)
    assert cmd.type == expected_type
    # Simple commands should not set PLACE-specific fields
    assert cmd.x is None
    assert cmd.y is None
    assert cmd.facing is None

# ----------------- PLACE (VALID) -----------------

@pytest.mark.parametrize(
    "line, x, y, facing",
    [
        ("PLACE 0,0,NORTH", 0, 0, Direction.NORTH),
        ("PLACE 1, 2, WEST", 1, 2, Direction.WEST),
        ("PLACE  1 ,2 ,EAST", 1, 2, Direction.EAST),
        ("PLACE\t3,4,SOUTH", 3, 4, Direction.SOUTH),
        ("  PLACE   4 ,  0 ,  WEST  ", 4, 0, Direction.WEST),
        ("place 2,3,east", 2, 3, Direction.EAST),
        ("PLACE -1,0,NORTH", -1, 0, Direction.NORTH),
        ("PLACE 0,-2,SOUTH", 0, -2, Direction.SOUTH),
        ("PLACE +2,+3,EAST", 2, 3, Direction.EAST),  # int('+2') works
    ],
)
def test_parse_place_valid(line, x, y, facing):
    cmd = CommandParser.parse(line)
    assert cmd is not None
    assert isinstance(cmd, Command)
    assert cmd.type == CommandType.PLACE
    assert cmd.x == x
    assert cmd.y == y
    assert cmd.facing == facing

# ----------------- INVALID INPUTS -----------------

@pytest.mark.parametrize(
    "line",
    [
        "", "   ", "\n", "\t",
        "# comment", "   # another",
        "MOVEE", "REPORT NOW", "LEFT 90",
        "PLACE", "PLACE   ",
        "PLACE 1,2", "PLACE 1,2,", "PLACE , , ",
        "PLACE 1 2 NORTH", "PLACE 1;2;NORTH",
        "PLACE 1,2,NORTH,EXTRA",
        "PLACE ,2,NORTH", "PLACE 1,,NORTH",
        "PLACE x,2,NORTH", "PLACE 1,y,NORTH",
        "PLACE 1,2,UP", "PLACE 1,2,NORTHEAST", "PLACE 1,2, NORTH WEST",
        "PLACE 1.0,2,NORTH", "PLACE 1,2.5,NORTH",
        "PLACE1,2,NORTH",  # no space after PLACE (based on current rules)
    ],
)
def test_parse_invalid_returns_none(line):
    assert CommandParser.parse(line) is None    
