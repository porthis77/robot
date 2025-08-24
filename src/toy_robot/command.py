from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class Position:
    x: int
    y: int

class Direction(Enum):
    NORTH = "NORTH"
    EAST  = "EAST"
    SOUTH = "SOUTH"
    WEST  = "WEST"
    
    def left(self) -> Direction:
        return {
            Direction.NORTH: Direction.WEST,
            Direction.WEST:  Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST:  Direction.NORTH,
        }[self]

    def right(self) -> Direction:
        return {
            Direction.NORTH: Direction.EAST,
            Direction.EAST:  Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST:  Direction.NORTH,
        }[self]

class CommandType(Enum):
    PLACE = auto()
    MOVE = auto()
    LEFT = auto()
    RIGHT = auto()
    REPORT = auto()

@dataclass(frozen=True)
class Command:
    type: CommandType
    x: Optional[int] = None
    y: Optional[int] = None
    facing: Optional[Direction] = None

class CommandParser:
    SIMPLE_CMDS = {
        "MOVE":   CommandType.MOVE,
        "LEFT":   CommandType.LEFT,
        "RIGHT":  CommandType.RIGHT,
        "REPORT": CommandType.REPORT,
    }   

    @staticmethod
    def parse(cmd: str) -> Optional[Command]:
        if not CommandParser.is_valid(cmd):
            return None

        s = cmd.strip().upper()

        # simple commands
        if s in CommandParser.SIMPLE_CMDS:
            return Command(type=CommandParser.SIMPLE_CMDS[s])

        # parse PLACE
        if s.startswith("PLACE"):
            parts = s.split(None, 1)
            arg_str = parts[1]
            tokens = [p.strip() for p in arg_str.split(",")]
            return Command(type=CommandType.PLACE, x=int(tokens[0]), y=int(tokens[1]), facing=Direction[tokens[2]])

    @staticmethod
    def is_valid(cmd: str) -> bool:
        if not isinstance(cmd, str):
            return False

        s = cmd.strip()
        if not s:
            return False
        # treat leading-space comments as comments too: "   # comment"
        if s.startswith("#"):
            return False

        # split on ANY whitespace at most once
        parts = s.split(None, 1)  # e.g. ["PLACE", "1, 2 , NORTH"] or ["MOVE"]
        head = parts[0].upper()

        # simple commands must be alone (no trailing tokens)
        if head in CommandParser.SIMPLE_CMDS:
            return len(parts) == 1

        # PLACE with args
        if head == "PLACE" and len(parts) == 2:
            args = parts[1]
            bits = [p.strip() for p in args.split(",")]
            if len(bits) != 3:
                return False

            x_str, y_str, f_str = bits

            # X,Y must be ints (allow signs like +2, -1)
            try:
                int(x_str)
                int(y_str)
            except ValueError:
                return False

            # Direction must be a valid enum NAME
            if Direction.__members__.get(f_str.upper()) is None:
                return False

            return True

        return False
