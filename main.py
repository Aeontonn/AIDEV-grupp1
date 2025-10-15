#Importing all the necessary modules/functions/libraries that are needed for the program to work
from modules.player import Player
from modules.game import Game
from modules.highscore import HighScoreManager
from ui.highscore_ui import show_highscore
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from modules.clear import clear

#This class allows the use of colored text, icons etc.
console = Console()

#Main funtion
def main():
    print("\n\n")
    console.print("[green]Välkommen till gissa talet![/green]")
    highscore_manager = HighScoreManager()
    player = None

    #Start of the loop
    while True:
        
        # Display the menu panel
        console.print(
            Panel(
                "\n1. 🎮 [bold cyan]Spela spelet![/bold cyan]"
                "\n2. 🏆 [bold yellow]Highscores tabell[/bold yellow]"
                "\n3. 📜 [bold blue]Hjälp![/bold blue]"
                "\n4. 🚪 [bold magenta]Avsluta![/bold magenta]",
                title="[bold cyan]Main Menu[/bold cyan]",
                expand=False
            )
        )

        # Prompts the user to choose
        print("\n")
        choice = Prompt.ask(
            "[cyan]Snälla välj ett av valen![/cyan]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        clear()

        # All the menu options as well as a warning if you type the wrong number
        if choice == "1":
            print("\n\n")
            if player is None:
                player = Player()
            Game(player, highscore_manager).run()
        elif choice == "2":
            print("\n\n")
            show_highscore()
            print("\n\n")
        elif choice == "3":
            print("\n\n")
            console.print("[cyan]Hjälp: Du har totalt 10 försök. Ju färre försök, desto högre poäng![/cyan]")
            print("\n\n")
        elif choice == "4":
            print("\n\n")
            console.print("[cyan]Hejdå![/cyan]")
            print("\n\n")
            break
        else:
            console.print("[red]Bruh learn to read and/or type.. Please choose again.[/red]")

if __name__ == "__main__":
    main()