import random
from .get_number import get_number  # för om användaren skriver ett ord / bokstäver istället för en siffra
from .highscore import HighScoreManager
from .player import Player
from .clear import clear
from rich.console import Console
from rich.prompt import Prompt
# from rich.text import Text
from rich.panel import Panel

console = Console()

class Game:
    clear()
    def __init__(self, player, highscore_manager):
        self.hs = highscore_manager
        self.answer = "ja"
        self.player = player

    def run(self):
        clear()
        print("\n\n")
        while self.answer == "ja":
            number = random.randint(1, 100)
    
            # för att hålla i highscore.
            x = 0
            console.print(Panel.fit("🎯 [bold cyan]Gissa talet![/bold cyan]\n"
                    "Du ska nu försöka gissa talet från [green]1[/green] till [green]100[/green]. Lycka till!", border_style="green"))
    
            # för att få användarens tal.
            user_num = get_number("\nSkriv in ett tal: ")
    
            # koden för att kolla vilket tal och hur nära.
            while number != user_num:
            
                # ifall de skriver ett tal öber 100.
                if user_num > 100:
                    x = x + 1 # lägga på ett poäng för en gissning.
                    if x > 10: # om de har gissat fler än 10 gånger så bryts spelet. (kan höjas eller sänkas senare)
                        break
                    console.print("❌ [#ff6a00]Du valde ett tal över 100.[/#ff6a00] Välj ett nytt tal mellan 1 och 100.")
                    user_num = get_number("\nSkriv in ett nytt tal: ") # så att loopen inte fortsätter tills man förlorar om man gissar för högt nummer
    
                # ifall de skriver att tal under 1.
                elif user_num < 1:
                    x = x + 1 # lägga på ett poäng för en gissning.
                    if x > 10: # om de har gissat fler än 10 gånger så bryts spelet. (kan höjas eller sänkas senare)
                        break
                    console.print("❌ [#ff6a00]Du valde ett tal under 1.[/#ff6a00] Välj ett nytt tal mellan 1 och 100.")
                    user_num = get_number("\nSkriv in ett nytt tal: ") # så att loopen inte fortsätter tills man förlorar om man gissar för lågt nummer
    
                elif user_num < number:
                    x = x + 1
                    if x > 10:
                        break
                    elif abs(user_num - number) <= 4: # för att kolla om gissningen är nära.
                        console.print("[bold magenta]Du är nära men inte riktigt där![/bold magenta]")
                    console.print("❌ [#ff0033]Ditt tal är för litet![/#ff0033]")
                    user_num = get_number("\nGissa ett större tal: ")
    
                elif user_num > number:
                    x = x + 1
                    if x > 10:
                        break
                    elif abs(user_num - number) <= 4:
                        console.print("[bold magenta]Du är nära men inte riktigt där![/bold magenta]")
                    console.print("❌ [#ff0033]Ditt tal är för stort![/#ff0033]")
                    user_num = get_number("\nGissa ett mindre tal: ")
                else:
                    x = x + 1 
                    break
                
            # om användaren gissade 10 gånger så avslutas spelet och skriver ut det här meddelandet.
            if x >= 10:
                console.print("\n💀 [#ff0033]Game Over![/#ff0033] Du gissade 10 gånger. Försök igen!")
    
            #  om användaren vinner och gissar talet under 10 gissningar så skrivs det här ut.
            else:
                x += 1 # om spelaren gissar rätt på första försöket
                console.print(Panel.fit(f"🎉 Grattis [bold green]{self.player.name}[/bold green]! "
                        f"Du gissade rätt på [yellow]{x}[/yellow] gånger! 🏆",
                        border_style="green")) # skriver också ut hur många gissningar det tog.
    
            # lägger till resultatet i highscore filen
            self.hs._scores.append({"player": self.player.name, "attempts": x})
            self.hs._sort_scores()
            self.hs._save()
    
            self.answer = input("\nVill du spela igen? Svara 'Ja' eller om du vill gå tillbaka till menyn tryck Enter\n")
            self.answer = self.answer.lower()
            clear()
    
    
        console.print("[bold cyan]Tack för att du spelade![/bold cyan]")
        print("\n\n")
    