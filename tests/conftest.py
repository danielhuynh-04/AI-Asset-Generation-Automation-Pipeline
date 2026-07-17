"""conftest.py — Pytest fixtures shared across all test files"""
import sys
from pathlib import Path

# Ensure src is on PATH for all tests
sys.path.insert(0, str(Path(__file__).parent / "src"))
