from pathlib import Path
from clear import clear
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import json

console = Console()

class Player:
    def __init__(self):
        """ Allow player to choose an existing username or create a new one. Stored in /data/users.json as a list. """
        data_dir = Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        self.username_file = data_dir / "users.json"
        self.name = self._choose_username()

    def _load_usernames(self):
        # load usernames from file or return empty list if there are no users
        if not self.username_file.exists():
            return []
        try:
            data = json.loads(self.username_file.read_text(encoding="utf-8"))
            # return if theres a list
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def _save_usernames(self, usernames):
        """save list of usernames to JSON file."""
        self.username_file.write_text(json.dumps(usernames, ensure_ascii=False, indent=2), encoding="utf-8")

    def _choose_username(self) -> str:
        """Let user select existing player or create a new one."""
        usernames = self._load_usernames()
        console.print(Panel.fit("[bold cyan]Välkommen till spelet![/bold cyan]"))

        if usernames:
            console.print("[green]Befintliga spelare:[/green]")
            for i, name in enumerate(usernames, 1):
                console.print(f"{i}. {name}")
            console.print(f"{len(usernames)+1}. ➕ Skapa ny spelare")

        choice = Prompt.ask(
            "[cyan]Välj en spelare (skriv siffra)[/cyan]",
            choices=[str(i) for i in range(1, len(usernames) + 2)],
        )

        if int(choice) <= len(usernames):
            selected = usernames[int(choice) - 1]
            console.print(f"[green]Välkommen tillbaka, {selected}! 👋[/green]")
            return selected

        """Skapa ny spelare"""
        new_name = Prompt.ask("[cyan]Skriv ditt nya användarnamn[/cyan]").strip() or "Player"
        if new_name not in usernames:
            usernames.append(new_name)
            self._save_usernames(usernames)
            console.print(f"[green]Ny spelare skapad: {new_name}![/green]")
        clear()
        return new_name

    def __str__(self):
        return self.name
