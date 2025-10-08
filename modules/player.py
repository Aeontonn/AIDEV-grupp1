from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class Player:
    def init(self):
        """
        Create or load player's username from /data/user.txt
        """
        data_dir = Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.username_file = data_dir / "user.txt"
        self.name = self._get_username()

    def _get_username(self) -> str:
        """
        Load existing username, or prompt to create a new one.
        """
        if self.username_file.exists():
            username = self.username_file.read_text(encoding="utf-8").strip()
            if username:
                console.print(f"[green]Welcome back, {username}! 👋[/green]")
                return username

        username = Prompt.ask("[cyan]Enter your username[/cyan]").strip() or "Player"
        self.username_file.write_text(username, encoding="utf-8")
        console.print(f"[green]Username saved as {username}![/green]")
        return username

    def str(self):
        return self.name