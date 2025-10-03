#Imports the colors and icons from the coloricons file in utilities/coloricons.py
from utilities.coloricons import Colors, ICONS, print_color

#The main menu
def display_menu() -> str:
    print_color("\n=== Main Menu ===", Colors.HEADER)
    print(f"1. {ICONS['game']} Play Game")
    print(f"2. {ICONS['trophy']} Highscores")
    print(f"3. {ICONS['menu']} Help")
    print(f"4. {ICONS['exit']} Exit")
    return input(f"{Colors.OKCYAN}Choose an option: {Colors.ENDC}").strip()