import random
import Modules.get_number as get_number  # för om användaren skriver ett ord / bokstäver istället för en siffra

highscore = []

answer = "ja"

while answer == "ja":
    number = random.randint(1, 100)
    
    # för att hålla i highscore.
    x = 0
    
    print("Gissa talet!\nDu ska nu försöka att gissa talet mellan 1 och 100. Lycka till!")

    # för att få användarens tal.
    user_num = get_number.get_number("\nSkriv in ett tal: ")

    # koden för att kolla vilket tal och hur nära.
    while number != user_num:
        
        # ifall de skriver ett tal öber 100.
        if user_num > 100:
            x = x + 1 # lägga på ett poäng för en gissning.
            if x > 10: # om de har gissat fler än 10 gånger så bryts spelet. (kan höjas eller sänkas senare)
                break
            print("Du valde ett tal över 100. Välj ett nytt tal mellan 1 och 100.")
            user_num = get_number.get_number("\nSkriv in ett nytt tal: ") # så att loopen inte fortsätter tills man förlorar om man gissar för högt nummer
        
        # ifall de skriver att tal under 1.
        elif user_num < 1:
            x = x + 1 # lägga på ett poäng för en gissning.
            if x > 10: # om de har gissat fler än 10 gånger så bryts spelet. (kan höjas eller sänkas senare)
                break
            print("Du valde ett tal under 1. Välj ett nytt tal mellan 1 och 100.")
            user_num = get_number.get_number("\nSkriv in ett nytt tal: ") # så att loopen inte fortsätter tills man förlorar om man gissar för lågt nummer
            
        elif user_num < number:
            x = x + 1
            if x > 10:
                break
            elif abs(user_num - number) <= 4: # för att kolla om gissningen är nära.
                print("Du är nära men inte riktigt där!")
            print("Ditt tal är för litet.")
            user_num = get_number.get_number("\nGissa ett större tal: ")
        
        elif user_num > number:
            x = x + 1
            if x > 10:
                break
            elif abs(user_num - number) <= 4:
                print("Du är nära men inte riktigt där!")
            print("Ditt tal är för stort.")
            user_num = get_number.get_number("\nGissa ett mindre tal: ")
        else:
            x = x + 1 
            break
    
    # om användaren gissade 10 gånger så avslutas spelet och skriver ut det här meddelandet.
    if x >= 10:
        print("\nGame Over! Du gissade 10 gånger. Försök Igen!")
        
    #  om användaren vinner och gissar talet under 10 gissningar så skrivs det här ut.
    else:
        print("Grattis! Du gissade rätt!")
        print("Du gissade", x, "Gånger\n") # skriver också ut hur många gissningar det tog.
    answer = input("\nVill du spela igen? Svara 'Ja' eller 'Nej'\n")
    answer = answer.lower()
    highscore.append(x) # spara highscore.
    
print("Tack för att du spelade!\n\nDina rekord är")

#  för att skriva rekorden finare och i rätt ordning
highscore.sort()

print("______")
for i in enumerate(highscore):
    print(i[0]+1, ':', i[1])
print("______")

avsluta = input("\nTryck enter för att avsluta spelet.")
