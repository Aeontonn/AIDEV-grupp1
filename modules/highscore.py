# modules/highscore.py
# ------------------------------------------------------------
# Highscore-hanterar för spelet "Gissa nummret"
# Filplacering: /data/highscore.json
# ------------------------------------------------------------

from __future__ import annotations # gör det enklare att skriva typer även om den defineras senare. Ex kan man skriva -> Person: istället för -> "Person":

from pathlib import Path # Path: enkelt och säkert sätt att jobba med fil- och mappvägar.
import json # för att läsa/skriva data i JSON-format.

class HighScoreManager:
    def __init__(self, path: Path | None = None, keep_max: int=50) -> None:
        '''
        Initierar/startar highscore-manager.
        - path: default - /data/highscore.json
        - keep_max: max antal poster vi vill spara
        '''
        
        # bestämmer vart highscore.json filen ska ligga. Om ingen path anges används en standardmapp.
        default_path = Path(__file__).resolve().parent.parent / 'data' / 'highscore.json'
        self.path: Path = Path(path) if path else default_path
        self.keep_max = int(keep_max)
        self._scores: list[dict] = [] # sparar highscore i en dict lista
        
        self._load() # läs in filen (eller skapa tom)
        
    def top(self, n: int = 50) -> list[dict]:
        '''
        Returnerar dom n första resultaten.
        '''
        n = max(0, int(n)) # n är alltid minst 0, så att vi inte får ett negativt index
        return list(self._scores[:n]) # plockar ut en lista från _scores. Returnerar en kopia (list(...)) så att originalet inte kan ändras utifrån.
    
    def add_score(self, player: str, attempts: int) -> None:
        '''
        Lägg till ett resultat i highscore-listan och spara till fil.
        Flera resultat per spelare tilllåts.
        '''
        
        name = (str(player) if player is not None else '').strip() or 'Anonymous'
        try:
            tries = int(attempts)
        except Exception:
            tries = 0
        if tries < 0:
            tries = 0 # så att antal försök inte kan vara negativt
        
        self._scores.append({"player": name, "attempts": tries})
        self._sort_scores() # håller listan kapad till keep_max och sorterad
        self._save() # skriv till highscore.json
    
    # ------------------------- Interna hjälpmetoder -------------------------
    # Nedanför: interna funktioner/metoder som används enbart inom klassen
    
    def _load(self) -> None:
        '''
        Läser in JSON-filen. Skapar en tom fil om den saknas.
        '''
        
        # säkerställer att mappen där filen ska ligga finns (/data/).
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        # om filen inte finns sedan tidigare -> börja med en tom lista och spara en ny fil.
        if not self.path.exists():
            self._scores = []
            self._save()
            return
        
        try:
            # öppna och läs JSON-filen
            with self.path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                
            # vi förväntar oss antingen en dict med "scores"-nyckel eller en ren lista.
            items =data.get('scores') if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = []
                
            # rensa och validera innehållet:
            # - varje post måste vara en dict
            # - innehålla både "player" och "attempts"
            cleaned: list[dict] = []
            for x in items:
                if isinstance(x, dict) and 'player' in x and 'attempts' in x:
                    cleaned.append({"player": str(x["player"]) or "Anonymous", "attempts": int(x["attempts"])})
                    
            # tilldela den rensade listan till _scores
            self._scores = cleaned
            
            # se till att listan alltid är sorterad efter inläsning
            self._sort_scores()
            
        except Exception:
            # Felhantering: Om filen är korrupt eller oläsbar -> börja om på tom lista
            self._scores = []
            self._save()
            self._sort_scores()
            
    def _save(self) -> None:
        '''
        Spara listan till JSON fil som 'scores': [...]
        '''
        
        # packar in listan i en dictionary med nycklens "scores"
        # - filen får en tydlig struktur och blir lättare att bygga ut senare
        payload = {"scores": self._scores}
        
        # öppnar filen i skrivläga ("w") och skriver in JASON-data
        # ensure_ascii=False gör att svenska tecken (å, ä, ö) sparas korrekt
        # indent=2 gör filen mer läsbar för människor.
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            
    def _sort_scores(self) -> None:
        '''
        Sortera highscore-listan efter minst antal försök (ascending).
        - färre "attempts" = bättre resultat.
        - begränsar listan till self.keep_max poster.
        '''
        
        # sorterar listan baserat på attempts, lägst först.
        self._scores.sort(key=lambda x: x['attempts'])
        
        # kapa listan om den är längre än keep_max
        if len(self._scores) > self.keep_max:
            self._scores = self._scores[:self.keep_max]