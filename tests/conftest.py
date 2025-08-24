# tests/conftest.py
import sys
from pathlib import Path

# add <repo>/src to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
