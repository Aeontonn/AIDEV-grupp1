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
# - låg fel med tab innanför klassen så fick inte funktionerna att koppla rätt.


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
    # Gör om ett sekunder till ett bättre tidsformat
    # ex. 65 sek -> 1:05
    # ex. 3725 sek -> 1:02:05 (timmar:minuter:sekunder)
    total = int(round(seconds)) # 1. Avrunda sekunder till heltal
    m, s = divmod(total, 60) # 2. Dela upp i minuter och sekunder -> returnerar (antal_minuter, resterande_sekunder)
    h, m = divmod(m, 60) # 3. Om timmar > 0, returnera H:MM:SS, annars M:SS -> returnerar (antal_timmar, resterande_minuter)
    # 4. om det finns timmar (>0), skriv ut som H:MM:SS
    if h > 0:
        return f'{h:d}:{m:02d}:{s:02d}'
    # 5. annars skriv ut som M:SS
    return f'{m:d}:{s:02d}'

def _human_date(iso_ts: str) -> str:
    '''
    Plocka ut YYYY-MM-DD från en ISO-sträng.
    ex. "2025-09-30T14:23:45" -> "2025-09-30"
    '''
    try: # 1. Försök konvertera ISO-strängen till datetime-objekt.
        dt = datetime.fromisoformat(iso_ts) # fromisoformat kan läsa stränga som "YYYY-MM-DDTHH:MM:SS".
        return dt.date().isoformat # 2. hämtar enbart datum-delen (YYYY-MM-SS) och gör om till sträng
    # 3. Om fel -> returnera originalsträngen
    except Exception:
        return iso_ts


class HighScoreManager:
    '''
    Manager för highscore.
    - Laddar highscore från JSON vid init
    - Lägger till nya resultat och sparar direkt
    - Sorterar listan så bästa resultat hamnar överst
    '''
    
    
    def __init__(self, path: Path | None = None, keep_max: int = 100) -> None:
        '''
        Initiera (starta) HighScoreManager.
        - path: vart highscore.json ska sparas. Om None -> standardmapp "data/highscores.json".
        - keep-max: hur många poster vi max sparar i listan (default = 100).
        '''
        # 1. Bestäm filväg (standard = /data/highscores.json).
        self.path: Path = Path(path) if path else Path(__file__).resolve().parent / 'data' / 'highscores.json'
        # 2. Sätt max antal poster.
        self.keep_max = int(keep_max)
        # 3. Skapa tom lista för resultatet.
        self._scores: list[dict] = []
        # 4. Läs in tidigare resultat från JSON-filen (om den finns).
        # -> om filen inet finns: skapa en tom fil automatiskt.
        self._load()
        
        
    def add_score(self, player: str, attempts: int, duration_seconds: float) -> None:
        '''
        Hjärtat i highscore-hanteringen - varje gång ett spel är klart kallas add_score 
        Lägg till nytt resultat och spara till fil.
        '''
        name = (player or '').strip() or 'Anonymous' # 1. Rensa spelarens namn, om spelaren inte skriver något namn -> använd "Anonymous". strip() tar bort extra mellanslag i början/slutet.
        if attempts <= 0: # 2. Kontrollera att attempts är giltig. - Måste vara större/fler än 0, annars returneras ett ValueError
            raise ValueError('attempts måste vara > 0')
        if duration_seconds < 0: # 3. Kontrollerar att duration_seconds är giltigt. - Måste vara 0 eller större (negativ tid är ogiltigt), annars returneras ett ValueError
            raise ValueError('duration_seconds måste vara >=0')
        
        # 4. Skapa en dictionary {} för resultatet. Sparar spelarens namn, antal försök, tid och en tidsstämpel.
        entry = {
            'player': name,
            'attempts': int(attempts),
            'duration_seconds': float(duration_seconds),
            'timestamp': _now_iso(), # YYYY-MM-DDTHH:MM:SS
        }
        
        self._scores.append(entry) # 5. lägger till resultatet i listan över alla highscores.
        self._sort_in_place() # 6. sorterar listan efter minst antal försök och kortast tid.
        if len(self._scores) > self.keep_max: # 7. om listan har blivit längre an vad vi vill behålla (keep_max) så kapar vi bort dom sämsta resultaten i slutet.
            self._scores = self._scores[: self.keep_max]
        self._save() # 8. sparar hela listan till JSON-filen
        
        
    def top(self, n: int = 10) -> list[dict]:
        '''
        Returnera dom n (10) bästa resultaten från highscore-listan.
        '''
        n = max(0, int(n)) # säkerhetshantering: se till att n alltid är ett heltal och minst 0.
        return list(self._scores[:n]) # returnerar dom n (10) första resultaten från highscore-listan som redan är sorterade via ovan _sort_in_place.


    def iter_table_rows(self, n: int = 10):
        '''
        Returnera rader som kan skrivas ut i en tabell.
        Varje rad = (plats, spelare, försök, tid, datum).
        '''
        # 2. För varje resultat:
        #   - skapa tuple med rank + värden
        # 3. Returnera listan av tupler
        rows = [] # 1. Hämta top n (10) resultat
        for i, s in enumerate(self.top(n), start=1): # 2. gå igenom listan och numrera varje rad med enumerate(). start=1 gör att första platsen får rank 1.
            # 3. skapa en tuple med 5 fält.
            row = (
                str(i), # i = placering (1, 2, 3, ...)
                s['player'], # s['player'] = spelarens namn
                str(s['attempts']), # s['attempts'] = antal försök (omvandlad till sträng)
                _format_duration(s['duration_seconds']), # _formation_duration() = tid formaterad till M:SS eller H:MM:SS
                _human_date(s['timestamp']) # _human_date() = datum (YYYY-MM-DD) från timestamp
            )
            rows.append(row)
            
        return rows # 4. returnerar listan


    def clear(self) -> None:
        '''
        Töm highscorelistan och spara tom fil.
        '''
        self._score = [] # nollställer listan.
        self._save() # sparar den nya listan till JSON-filen.
        

    # ---------------------- Interna hjälpmetoder ----------------------
    

    def _sort_in_place(self) -> None:
        '''
        Sortera resultatlistan så att bästa resultat alltid kommer först.
        Tillkallas varje gång det läggs till eller när resultatet läses in.
        '''
        # Sortera på attempts (stigande)
        # Om lika -> sortera på duration_seconds (stigande)
        # Om lika -> sortera på timestamp (äldst först)
        self._scores.sort(
            key=lambda s: (s['attempts'], s['duration_seconds'], s['timestamp'])
            )
        
        
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