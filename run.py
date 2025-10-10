# för att testa att köra olika filer
from modules.game import Game
from modules.player import Player
from modules.highscore import HighScoreManager

if __name__ == "__main__":
  Game(Player, HighScoreManager).run()