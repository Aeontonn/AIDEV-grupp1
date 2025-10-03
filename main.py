#Importing all the necessary modules/functions that are needed for the program to work
from main.modules.users import create_username
from main.modules.game import superduperguess_game
from main.modules.scores import show_scoreboard
from main.modules.menu import display_menu
from main.utilities.coloricons import print_color, Colors

#The entry point menu and choices given to the player
def main():
    print_color("Welcome to this superduper awesome guessing game!", Colors.OKGREEN)
    username = create_username()
#A loop where player gets to choose different options
    while True:
        choice = display_menu()

        if choice == "1":
            superduperguess_game(username)
        elif choice == "2":
            show_scoreboard()
        elif choice == "3":
            print_color("Type a number between 1-50(easy), 1-75(medium) or 1-100(hard). You have 10 guesses in total. The fewer attempts, the higher your score!", Colors.OKBLUE)
        elif choice == "4":
            print_color("Goodbye!", Colors.WARNING)
            break
        else:
            print_color("Invalid option. Please choose again.", Colors.FAIL) 
            #If player chooses wrong number you get a warning and get to choose again

if __name__ == "__main__":
    main()