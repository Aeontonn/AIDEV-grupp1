from rich.console import Console
from rich.prompt import Prompt
from modules.highscore import HighScoreManager

console = Console()


class Player:
    def init(self):
        self.username = None

    def create_username(self):
        username = Prompt.ask("Enter a unique username 👤").strip()
        highscores = HighScoreManager()
        existing_usernames = [s["player"] for s in highscores.top(1000)]

        if username in existing_usernames:
            console.print("Username already exists. Try again.", style="bold red")
        else:
            self.username = username
            console.print(f"Welcome, {username}! 🎉", style="bold green")