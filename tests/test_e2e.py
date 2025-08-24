# tests/test_main_cli.py
import builtins
import sys
import io
import os
import pytest

# Import the module under test
import toy_robot.robot as robot


def run_cli(monkeypatch, argv):
    """
    Helper to run main() with a patched argv and capture SystemExit (if any).
    Returns (exit_code, stdout, stderr_like) where stdout is captured print output.
    """
    # Capture printed output via capsys-like StringIO
    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    monkeypatch.setattr(sys, "stderr", buf)
    monkeypatch.setattr(sys, "argv", argv)
    try:
        robot.main()
    except SystemExit as e:
        return e.code, buf.getvalue(), buf.getvalue()
    return 0, buf.getvalue(), buf.getvalue()


def test_main_no_args_shows_usage_and_exits_2(monkeypatch):
    code, out, _ = run_cli(monkeypatch, ["toy_robot.py"])
    assert code == 2
    assert "Usage: python toy_robot.py <commands_file>" in out


def test_main_file_not_found_exits_1(monkeypatch, tmp_path):
    missing = tmp_path / "nope.txt"
    code, out, _ = run_cli(monkeypatch, ["toy_robot.py", str(missing)])
    assert code == 1
    assert f"Error: file not found: {missing}" in out


def test_main_happy_path_prints_progress_and_states(monkeypatch, tmp_path):
    # Prepare a commands file with comments/blank/valid/invalid lines
    cmd_text = "\n".join(
        [
            "# comment line",
            "",
            "PLACE 0,0,NORTH",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT",
            "JUMP 10,10,NORTH",  # invalid → CommandParser.parse returns None
        ]
    )
    fpath = tmp_path / "cmds.txt"
    fpath.write_text(cmd_text)

    code, out, _ = run_cli(monkeypatch, ["toy_robot.py", str(fpath)])
    assert code == 0

    # It should echo each parsed line with a line number header
    assert "[line 3] >>> PLACE 0,0,NORTH" in out
    assert "[line 4] >>> MOVE" in out
    assert "[line 5] >>> LEFT" in out
    assert "[line 6] >>> MOVE" in out
    assert "[line 7] >>> REPORT" in out
    assert "[line 8] >>> JUMP 10,10,NORTH" in out

    # For invalid command
    assert "Invalid command" in out

    # Check the state transitions (old_state/new_state strings come from toy_robot.__str__)
    # After PLACE 0,0,NORTH
    assert "is_command_successful: True, old_state: Robot not placed, new_state: Robot at (0,0) facing NORTH" in out

    # After MOVE from (0,0) NORTH -> (0,1)
    assert "is_command_successful: True, old_state: Robot at (0,0) facing NORTH, new_state: Robot at (0,1) facing NORTH" in out

    # After LEFT NORTH -> WEST (position unchanged)
    assert "is_command_successful: True, old_state: Robot at (0,1) facing NORTH, new_state: Robot at (0,1) facing WEST" in out

    # After MOVE facing WEST at x=0 should be blocked (stays at (0,1))
    # move() returns False when blocked
    assert "is_command_successful: False, old_state: Robot at (0,1) facing WEST, new_state: Robot at (0,1) facing WEST" in out

    # REPORT returns the string from toy_robot.report()
    # Your report() returns "x:<x>,y:<y>,facing:<NAME>"
    assert "is_command_successful: x:0,y:1,facing:WEST" in out


def test_main_handles_only_comments_and_blanks(monkeypatch, tmp_path):
    fpath = tmp_path / "emptyish.txt"
    fpath.write_text("# just a comment\n\n   \n# and another\n")
    code, out, _ = run_cli(monkeypatch, ["toy_robot.py", str(fpath)])
    assert code == 0
    # No “[line ...] >>> ...” lines should appear because all lines are skipped
    assert "[line " not in out
