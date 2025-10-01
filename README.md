# AIDEV-grupp1
AIDEV Grupp 1 inlämningsuppgift

BESKRIVNING:
- Gissa talet med tabell för highscore, random nummer generator, användare för highscore tabell.
 Klasser som kan användas: game, player, highscore manager, random number, 




Vem gör vad:
- Anton - game.py   # fixa till så att allt fungerar som det ska
- Nicklas - highscore.py




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
