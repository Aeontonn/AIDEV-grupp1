# ui/highscore_ui.py

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from modules.highscore import HighScoreManager # hämtar klassen HighScoreManager

def show_highscore(n: int = 5, console: Console | None = None) -> None:
    '''
    Visar highscore-tabellen i terminalen.
    
    - n: hur många toppresultat som ska visas.
    - console: valfri Rich-Console att skriva till. Om inget skickas in
      skapar funktionen en egen. På så sätt kan UI testas eller återanvändas
      utan att HighScoreManager blandas in i utskriften.
    
    Notera: UI (presentation) och data (HighScoreMAnager) hålls isär.
    '''
    
    # Använd den Console som eventuellt skickats in, annars skapa en ny.
    # emoji=True gör att medalj-emojis visas snyggt i stödjande terminaler.
    console = console or Console(emoji=True)
    
    # Skapa manager och hämta topp n resultat.
    # Antas returnera en lista av dictar, t.ex.:
    # [{"player": "Test", "attempts": 3}, ...]
    hs = HighScoreManager()
    top_scores = hs.top(n)
    
    # UI för tabellen (ram, title, stil m.m.)
    table = Table(
        title='🏆 Highscore',
        box=box.ROUNDED,
        header_style='bold',
        show_lines=False,
        expand=False
    )
    
    # Lägg till kolumner: plats, spelarnamn, antal försök
    table.add_column('#', justify='right', style='dim')
    table.add_column('Spelare', justify='left')
    table.add_column('Försök', justify='right')
    
    # Fyll tabellen med rader
    for i, item in enumerate(top_scores, start=1):
        # Säkerställ sträng/int och ge standardnamn om tomt
        name = str(item['player']) or 'Anonymous'
        attempts = int(item['attempts'])
        
        # Välj medalj + färg för topp 3, annars platsnummer
        if i == 1:
            medal, color = '🥇', 'gold1'
        elif i == 2:
            medal, color = '🥈', 'silver'
        elif i == 3:
            medal, color = '🥉', 'dark_orange'
        else:
            medal, color = str(i), 'white'
            
        # Lägg in en rad i tabellen med lite färg/stil
        table.add_row(
            Text(str(medal), style=f"bold {color}"),
            Text(name, style=('bold ' + color) if i <= 3 else 'white'),
            Text(str(attempts), style=color if i <= 3 else 'cyan'),
        )
           
    # Skriv ut till konsolen
    console.print(table)