import builtins
from unittest.mock import patch
from modules.game import Game


def test_game_win(monkeypatch):
    # Mocka HighScoreManager så att den inte läser/skriv filer
    with patch("modules.game.HighScoreManager") as MockHS:
        # skapa en fejkad instans som används i spelet
        mock_hs = MockHS.return_value
        mock_hs._scores = []
        mock_hs._sort_scores = lambda: None
        mock_hs._save = lambda: None

        # fixa slumpen
        with patch("modules.game.random.randint", return_value=50):
            # användaren gissar rätt direkt
            with patch("modules.game.get_number", side_effect=[50]):
                # mocka Prompt.ask (för att hoppa över Richs input)
                with patch("modules.game.Prompt.ask", return_value="Testspelare"):
                    # mocka input (för frågan 'vill du spela igen?' och avslut)
                    inputs = iter(["nej", ""])
                    monkeypatch.setattr(builtins, "input", lambda *_, **__: next(inputs))

                    # kör spelet
                    game = Game()
                    game.run()

                    # kontrollera att poängen sparades rätt i mocken
                    last_score = mock_hs._scores[-1]
                    assert last_score["player"] == "Testspelare"
                    assert last_score["attempts"] == 1
