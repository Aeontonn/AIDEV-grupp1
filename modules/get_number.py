#   funktion för att snabbt kolla så att användaren skrev ett nummer istället för bokstäver

def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Oj! Du råkade skriva bokstäver eller ett ord istället för ett nummer. Försök igen!")