# AIDEV-grupp1
AIDEV Grupp 1 inlämningsuppgift

BESKRIVNING:
- Gissa talet med tabell för highscore, random nummer generator, användare för highscore tabell.
 Klasser som kan användas: game, player, highscore manager, random number, 




Vem gör vad:
- Anton - game.py   # fixa till så att allt fungerar som det ska
- Nicklas - highscore.py
- Ali - player.py
- Constantine main.py





Tips på standardbibliotek:
- random - drar det hemliga talet.
- datetime - mät speltid.
- json - spara/läsa highscore


Tips på externabibliotek:
- rich / colorama - för en lite roligare CLI - färga feedback ('För högt!' i rött, 'Rätt! i grönt)
- requests - om vi vill använda en API


Tips på moduler/mappträd:
- guess_number/
 - main.py # CLI-start, starta/loopa-spel
 - game.py # class game
 - player.py # class player
 - highscore.py # class HighScoreManager
 - utils.py # småhjälp: validering, tidsformatering
- tests/
 - test_game.py 
 - test_highscore.py
 - test_utils.py
- README.md
- requirements.txt


README - vad som ska stå
1. BESKRIVNING
2. Installation:
3. Körning:
4. Filer & ansvar: Lista vem i gruppen som gjort vad
5. Testning: PyTest
6. Konfiguration: Var ligger highscores.json, hur byter man språk/tema, env-variabler (om vi använder API).


VERSIONSHANTERING (Git/GitHub)
- Arbetsflöde: skydda main-branch -> jobba i feature-branches (ex. feat/highscores), gör Pull Requests och code reviews.
- Commits: Använd korta, meningsfulla meddelanden

 VERSION
- 0.1 Tillägg av mappar för olika moduler/utilities etc. Bättre struktur, lägg gärna in filerna i respektive mapp
- 0.1.1 Strukturerade allting om lite granna, istället för att ha modules/game, modules/menu etc. så lägger vi .py filerna direkt i modules mappen, jag addade oxå __init__.py i mapparna då det kan vara bra och ha för de som använder äldre versioner av python.
- 0.1.2 Gjorde ändringar på game.py. Fixade ett par fel som te.x att spelet krashar när man skriver någonting som inte är en siffra, och så fixade jag så att spelet inte fastnar i en loop om man gissar ett tal över 100 eller under 1. Lade också till en modul som enkelt kollar om man har skrivit ett nummer ller inte.
- 0.1.3 Fixade så att game.py fungerar tillsammans med highscore.py
- 0.2 Skapade main.py, menu.py och coloricons.py. Tog bort onödiga .md filer i alla mappar(krävs att man skapar dessa tomma filer för att kunna skapa mapp, då tomma mappar inte går att skapa i github utan kräver åtminstone en fil i dem, dont ask why.. XD)
- 0.3 En grym upgrade, behöver inte menu och coloricons längre då allting ingår i nya externa bibliotek rich(pip install rich) och allting för menyn ingår i main.py
- 0.3.1 Skapade requirements.txt med alla libraries och versionerna, förutom rich så finns tinydb för det behövs för .json filerna i data mappen. Installera dessa i gitbash med pip install -r requirements.txt
- 0.4 Skapade Test mapp, där alla lägger sina test filer, dvs med pytest

