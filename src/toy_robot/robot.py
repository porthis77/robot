# toy_robot.py
from __future__ import annotations
from dataclasses import dataclass
import re
import sys
from typing import Iterable, List, Optional
from .command import Position, Direction, Command, CommandType, CommandParser

@dataclass(frozen=True)
class Table:
    width: int = 5
    height: int = 5

    def is_valid(self, pos: Position) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height
        
class Robot:

    MOVE_OFFSETS = {
        Direction.NORTH: (0, 1),
        Direction.EAST:  (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST:  (-1, 0),
    }

    def __init__(self, table: Table):
        self._table = table
        self._pos: Optional[Position] = None
        self._facing: Optional[Direction] = None

    @property
    def pos(self) -> Optional[Position]:
        """Current position (x, y) of the robot, or None if not placed."""
        return self._pos

    @property
    def facing(self) -> Optional[Direction]:
        """Current facing direction of the robot, or None if not placed."""
        return self._facing

    def is_placed(self) -> bool:
        return self._pos is not None and self._facing is not None

    def place(self, pos: Position, facing: Direction) -> bool:
        if self._table.is_valid(pos):
            self._pos = pos
            self._facing = facing
            return True

        return False

    def left(self) -> bool:
        if self.is_placed():
            self._facing = self._facing.left()
            return True

        return False    

    def right(self) -> bool:
        if self.is_placed():
            self._facing = self._facing.right()
            return True

        return False

    def move(self) -> bool:
        if not self.is_placed():
            return False

        dx, dy = self.MOVE_OFFSETS[self._facing]
        nxt = Position(self._pos.x + dx, self._pos.y + dy)
        if self._table.is_valid(nxt):
            self._pos = nxt 
            return True

        return False

    def report(self) -> Optional[str]:
        if not self.is_placed():
            return "Robot not placed"
        return f"x:{self._pos.x},y:{self._pos.y},facing:{self._facing.name}"

    def __str__(self):
        if not self.is_placed():
            return "Robot not placed"
        return f"Robot at ({self._pos.x},{self._pos.y}) facing {self._facing.name}"        

    def execute_command(self, cmd: Command):
        """
        Execute a single Command on the given robot.
        Side-effects:
        - Mutates robot state
        - Appends to outputs list if REPORT is executed
        """
        if cmd.type == CommandType.PLACE:
            return self.place(Position(cmd.x, cmd.y), cmd.facing)
        elif cmd.type == CommandType.MOVE:
            return self.move()
        elif cmd.type == CommandType.LEFT:
            return self.left()
        elif cmd.type == CommandType.RIGHT:
            return self.right()
        elif cmd.type == CommandType.REPORT:
            return self.report()


# --- read file input, for each line, print input, output, and state
def main():
    if len(sys.argv) < 2:
        print("Usage: python toy_robot.py <commands_file>")
        sys.exit(2)

    path = sys.argv[1]
    robot = Robot(Table())

    try:
        with open(path, "r") as f:
            for lineno, raw in enumerate(f, start=1):
                #print(f'is_placed: {robot.is_placed()}')
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue

                cmd = CommandParser.parse(line)
                print(f"[line {lineno}] >>> {line}")

                if cmd is None:
                    print("Invalid command")
                    print("-" * 40)
                    continue

                old_state = str(robot)
                result = robot.execute_command(cmd)
                new_state = str(robot)

                print(f"is_command_successful: {result}, old_state: {old_state}, new_state: {new_state}")
                print("-" * 40)

    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
