# AIDEV-grupp1
AIDEV Grupp 1 inlämningsuppgift

BESKRIVNING:
Gissa talet med tabell för highscore, random nummer generator, användare för highscore tabell.
 Klasser som kan användas: game, player, highscore manager, random number, 


Tips på standardbibliotek:
- random - drar det hemliga talet.
- datetime - mät speltid.
- json - spara/läsa highscore

Tips på externabibliotek:
- rich / coloroma - för en lite roligare CLI - färga feedback ('För högt!' i rött, 'Rätt! i grönt)
- requests - om vi vill använda en API

Tips på moduler/mappträd:
guess_number/
 main.py # CLI-start, starta/loopa-spel
 game.py # class game
 player.py # class player
 highscore.py # class HighScoreManager
 utils.py # småhjälp: validering, tidsformatering
tests/
 test_game.py 
 test_highscore.py
 test_utils.py

