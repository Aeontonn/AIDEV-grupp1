"""
Comprehensive test suite for main.py and connected modules.

Run with:
    pytest -v --disable-warnings
"""

import pytest
from unittest.mock import patch
import subprocess


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
    """Simulate running main.py from CLI and exiting."""
    result = subprocess.run(
        ["python", "main.py"],
        input="4\n", text=True, capture_output=True
    )
    assert result.returncode == 0
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
    inputs = iter(["2", "3", "1", "4"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *a, **kw: next(inputs))

    with patch("modules.game.Game.run", return_value=None):
        main()

    captured = capsys.readouterr()
    assert "Welcome" in captured.out
    assert "Goodbye" in captured.out
    
