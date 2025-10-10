# ui/highscore_ui.py

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from modules.highscore import HighScoreManager

def show_highscore(n: int = 5, console: Console | None = None) -> None:
    '''
    Hämtar top n från HighScoreManager och skriver en Rich-tabell.
    UI-presentationen hålls utanför datalagret.
    '''
    
    console = console or Console(emoji=True)
    hs = HighScoreManager()
    top_scores = hs.top(n)
    
    table = Table(
        title='🏆 Highscore',
        box=box.ROUNDED,
        header_style='bold',
        show_lines=False,
        expand=False
    )
    table.add_column('#', justify='right', style='dim')
    table.add_column('Spelare', justify='left')
    table.add_column('Försök', justify='right')
    
    for i, item in enumerate(top_scores, start=1):
        name = str(item['player']) or 'Anonymous'
        attempts = int(item['attempts'])
        
        if i == 1:
            medal, color = '🥇', 'gold1'
        elif i == 2:
            medal, color = '🥈', 'silver'
        elif i == 3:
            medal, color = '🥉', 'dark_orange'
        else:
            medal, color = str(i), 'white'
            
        table.add_row(
            Text(str(medal), style=f"bold {color}"),
            Text(name, style=('bold ' + color) if i <= 3 else 'white'),
            Text(str(attempts), style=color if i <= 3 else 'cyan'),
        )
        
    console.print(table)