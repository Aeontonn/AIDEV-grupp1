#Importing all the necessary modules/functions/libraries that are needed for the program to work
from main.modules.player import create_username
from main.modules.game import Game
from main.modules.highscore import HighScoreManager
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

#This class allows the use of colored text, icons etc.
console = Console()

#Main funtion
def main():
    console.print("[green]Welcome to this superduper awesome guessing game![/green]")
    username = create_username()

    #Start of the loop
    while True:
        
        # Display the menu panel
        console.print(
            Panel(
                "\n1. 🎮 [bold cyan]Play the superduper awesome Game[/bold cyan]"
                "\n2. 🏆 [bold yellow]Highscores table[/bold yellow]"
                "\n3. 📜 [bold blue]Bruh need help![/bold blue]"
                "\n4. 🚪 [bold magenta]Exit here![/bold magenta]",
                title="[bold cyan]Main Menu[/bold cyan]",
                expand=False
            )
        )

        # Prompts the user to choose
        choice = Prompt.ask(
            "[cyan]Choose one of the following options please![/cyan]",
            choices=["1", "2", "3", "4"],
            default="1"
        )

        # All the menu options as well as a warning if you type the wrong number
        if choice == "1":
            Game(username)
        elif choice == "2":
            HighScoreManager()
        elif choice == "3":
            console.print("[cyan]Help: Type a number between 1-50(easy), 1-75(medium) or 1-100(hard). You have 10 guesses in total. The fewer attempts, the higher your score! Scores depend on difficulty and time![/cyan]")
        elif choice == "4":
            console.print("[cyan]Goodbye![/cyan]")
            break
        else:
            console.print("[red]Bruh learn to read and/or type.. Please choose again.[/red]")

if __name__ == "__main__":
    main()