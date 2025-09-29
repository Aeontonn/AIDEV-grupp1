# highscore.py
# ------------------------------------------------------------
# Enkel highscore-hanterare för ett textbaserat "Gissa numret" spel.
# ------------------------------------------------------------
# Funktioner:
# - Lagra resultat (spelare, antal försök, tid) i en JSON-fil
# - Läsa in resultaten vid start
# - Sortera resultaten: minst försök -> kortast tid -> äldst datum

# Klass?
# - Enkel att använda från menyn: skapa ett HighScoreManager-objekt
# - Håller koll på filväg och intern lista av resultat

# Standardbibliotek vi använder:
# - json (läsa/skriva fil)
# - datetime (tidsstämplar och formatering)
# - pathlib (smidig fil- och mapphantering)

# Exempelanvändning (meny/CLI)
#   from highscores import HighScoreManager
#   hs = HighScoreManager() # skapar data-mapp och fil om de saknas
#   hs.add_score(player='Anna', attempts=5, dureation_seconds=42.3)
#   for rank, name, attempts, duration, date in hs.iter_table_rows(10):
#       print(f'{rank:>2}. {name:<12} {attempts:<3} försök {duration:<6} {date}')

# Tips för presentation:
# - Visa hur vi byggt i små steg (ladda/spara -> sortera -> tabellrader)
# - Poängtera att menyn kan anropa iter_table_rows() för att skriva ut topplistan
# ------------------------------------------------------------

# TODO:
# -
# Fel, problem, svårigheter jag stött på:
# - låg fel med tab i vissa funktioner så fick inte funktionerna att koppla rätt.


# ------------------------------------------------------------

# moduler vi behöver importera

from __future__ import annotations
# Detta gör att vi kan använda "nya" sättet att skriva typ-hintar (ex Path | None).
# Det gör koden mordernare och enklare att läsa

from pathlib import Path
# Path används för att jobba med filer och mappar på ett enkelt sätt.
# Istället för att skriva filvägar som textsträngar kan vi använda Path-objekt som fungerar på alla operativsystem.

from datetime import datetime
# låter oss jobba med datum och tid.
# - skapa tidsstämplar när en score sparas.
# - visa datum i highscore-listan

import json
# json används för att spara och läsa data i JSON-format

# ------------------------------------------------------------

def _now_iso() -> str:
    '''
    Returnera aktuell tid som ISO 8601-sträng.
    '''
    # Den här funktionen fer oss nuvarande tid -> formatera till ISO-sträng (YYYY-MM-DDTHH:MM:SS)
    # Formatet kallas för ISO 8601 - (år-månad-dag "T" Timme:Minut:Sekund)
    return datetime.now().isoformat(timespec='seconds')
    # datetime.now() hämtar nuvarande datum och tid från datorn och rundar av till sekunder

def _format_duration(seconds: float) -> str:
    '''Formatera sekunder till M:SS eller H:MM:SS.'''
    # 1. Avrunda sekunder till heltal
    # 2. Dela upp i minuter och sekunder
    # 3. Om timmar > 0, returnera H:MM:SS, annars M:SS
    total = int(round(seconds))
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f'{h:d}:{m:02d}:{s:02d}'
    return f'{m:d}:{s:02d}'

def _human_date(iso_ts: str) -> str:
    '''
    Plocka ut YYYY-MM-DD från ISO-sträng.
    '''
    # 1. Försök konvertera ISO-strängen till datetime
    # 2. Returnera datumdelen
    # 3. Om fel -> returnera originalsträngen
    try:
        return datetime.fromisoformat(iso_ts).date().isoformat()
    except Exception:
        return iso_ts


class HighScoreManager:
    '''
    Manager för highscore.
    - Laddar highscore från JSON vid init
    - Lägger till nya resultat och sparar direkt
    - Sorterar listan så bästa resultat hmnar överst
    '''
    
    
    def __init__(self, path: Path | None = None, keep_max: int = 100) -> None:
        # 1. Bestäm filväg (standard = /data/highscores.json)
        # 2. Sätt max antal poster
        # 3. Skapa tom lista för resultatet
        # 4. Läs in fil om den finns
        self.path: Path = Path(path) if path else Path(__file__).resolve().parent / 'data' / 'highscores.json'
        self.keep_max = int(keep_max)
        self._scores: list[dict] = []
        self._load()
        
        
    def add_score(self, player: str, attempts: int, duration_seconds: float) -> None:
        '''
        Lägg till nytt resultat och spara till fil.
        '''
        # 1. Rensa spelarens namn (tomt = 'Anonymous')
        # 2. Kontrollera att attempts > 0 och duration >= 0
        # 3. Skapa en dictionary med resultat
        # 4. Lägg till i listan
        # 5. Sortera listan
        # 6. Om listan är för lång -> kapa den
        # 7. Spara listan till fil
        name = (player or '').strip() or 'Anonymous'
        if attempts <= 0:
            raise ValueError('attempts måste vara > 0')
        if duration_seconds < 0:
            raise ValueError('duration_seconds måste vara >=0')
        
        entry = {
            'player': name,
            'attempts': int(attempts),
            'duration_seconds': float(duration_seconds),
            'timestamp': _now_iso(),
        }
        self._scores.append(entry)
        self._sort_in_place()
        if len(self._scores) > self.keep_max:
            self._scores = self._scores[: self.keep_max]
        self._save()
        
        
    def top(self, n: int = 10) -> list[dict]:
        '''
        Returnera dom n (10) bästa resultaten.
        '''
        # ta dom första n (10) resultaten i listan
        n = max(0, int(n))
        return list(self._scores[:n])


    def iter_table_rows(self, n: int = 10):
        '''
        Returnera rader som kan skrivas ut i en tabell.
        Varje rad = (plats, spelare, försök, tid, datum).
        '''
        # 1. Hämta top n (10) resultat
        # 2. För varje resultat:
        #   - skapa tuple med rank + värden
        # 3. Returnera listan av tupler
        rows = []
        for i, s in enumerate(self.top(n), start=1):
            rows.append(
                (str(i), s['player'], str(s['attempts']), _format_duration(s['duration_seconds']), _human_date(s['timestamp']))
            )
        return rows


    def clear(self) -> None:
        '''
        Töm highscorelistan och spara tom fil.
        '''
        # nollställ listan och skriv över listan
        self._score = []
        self._save()
        

    # ---------------------- Intern hjälpmetoder ----------------------
    

    def _sort_in_place(self) -> None:
        '''
        Sortera resultatlistan.
        '''
        # 1. Sortera på attempts (stigande)
        # 2. Om lika -> sortera på duration_seconds (stigande)
        # 3. Om lika -> sortera på timestamp (äldst först)
        self._scores.sort(key=lambda s: (s['attempts'], s['duration_seconds'], s['timestamp']))
        
        
    def _load(self) -> None:
        '''
        Läs in JSON-fil eller skapa tom fil.
        '''
        # 1. Se till att data-mappen finns
        # 2. Om filen inte finns -> skapa en tom lista och spara ny fil
        # 3. Om filen finns -> läs in JSON
        # 4. Städa posterna ( se till att alla nycklar finns)
        # 5. Sortera listan
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exist():
            self._scores = []
            self._save()
            return
        try:
            with self.path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'scores' in data:
                items = data['scores']
            elif isinstance(data, list):
                items = data
            else:
                items = []
            cleaned = []
            for x in items:
                if all(k in x for k in ('player', 'attempts', 'duration_seconds', 'timestamp')):
                    cleaned.append({
                        'player': str(x['player']) or 'Anonymous',
                        'attempts': int(x['attempts']),
                        'duration_seconds': float(x['duration_seconds']),
                        'timestamp': str(x['timestamp']),
                    })
            self._scores = cleaned
            self._sort_in_place()
        except Exception:
            self._scores = []
            self._save()
            
            
    def _save(self) -> None:
        '''
        Skriver listan till JSON-fil.
        '''
        # 1. Skapa dictionary {'scores': lista}
        # 2. Öppna filen i skrivläge
        # 3. Skriva JSON till filen
        payload = {'scores': self._scores}
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)