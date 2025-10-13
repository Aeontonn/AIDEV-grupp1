"""
Comprehensive test suite for main.py and connected modules.

Run with:
    pytest -v --disable-warnings -s
"""

import pytest
from unittest.mock import patch
import subprocess
import os


# ────────────────────────────────────────────────
#  1️⃣  IMPORT TESTS
# ────────────────────────────────────────────────

def test_imports_ok():
    """Ensure all key modules and symbols import successfully."""
    from main import main
    from modules.player import Player
    from modules.game import Game
    from modules.highscore import HighScoreManager
    from ui.highscore_ui import show_highscore

    assert callable(main)
    assert hasattr(Player, "__init__")
    assert hasattr(Game, "run")
    assert callable(show_highscore)
    assert hasattr(HighScoreManager, "_save")


# ────────────────────────────────────────────────
#  2️⃣  CLI EXECUTION TEST (END-TO-END)
# ────────────────────────────────────────────────


def test_cli_run_exit():
    project_root = os.path.dirname(os.path.dirname(__file__))
    main_path = os.path.join(project_root, "main.py")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # ensures subprocess uses UTF-8

    result = subprocess.run(
        ["python", main_path],
        input="4\n",
        capture_output=True,
        text=True,
        env=env,
        encoding="utf-8"  # 👈 explicitly decode stdout/stderr as UTF-8
    )

    print("\n--- STDOUT ---")
    print(result.stdout)
    print("--- STDERR ---")
    print(result.stderr)

    assert result.returncode == 0, f"Non-zero exit ({result.returncode}): {result.stderr}"
    assert "Goodbye" in result.stdout


# ────────────────────────────────────────────────
#  3️⃣  EXIT BEHAVIOR
# ────────────────────────────────────────────────

def test_exit_message(monkeypatch, capsys):
    """Ensure exit message appears."""
    from main import main
    inputs = iter(["4"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *a, **kw: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Goodbye" in captured.out


# ────────────────────────────────────────────────
#  4️⃣  STRESS TEST / REPEATED LOOP
# ────────────────────────────────────────────────

def test_multiple_menu_loops(monkeypatch, capsys):
    """Simulate navigating through multiple menu options before exit."""
    from main import main

    # Add more fake inputs (safe fallback to avoid StopIteration)
    inputs = iter(["2", "3", "1", "4"])

    def fake_prompt(*args, **kwargs):
        try:
            return next(inputs)
        except StopIteration:
            return "4"  # Always exit gracefully if we run out

    monkeypatch.setattr("rich.prompt.Prompt.ask", fake_prompt)

    # Patch the Game.run method so it doesn’t actually start a real game
    with patch("modules.game.Game.run", return_value=None):
        main()

    captured = capsys.readouterr()
    assert "Welcome" in captured.out
    assert "Goodbye" in captured.out