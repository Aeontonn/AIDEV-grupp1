# modules/highscore.py
# ------------------------------------------------------------
# Highscore-hanterar för spelet "Gissa nummret"
# Filplacering: /data/highscore.json
# ------------------------------------------------------------

from __future__ import annotations

from pathlib import Path
import json

class HighScoreManager:
    def __init__(self, path: Path | None = None, keep_max: int=50) -> None:
        '''
        Initierar highscore-manager.
        - path: default - /data/highscore.json
        - keep_max: max antal poster vi vill spara
        '''
        
        default_path = Path(__file__).resolve().parent.parent / 'data' / 'highscore.json'
        self.path: Path = Path(path) if path else default_path
        self.keep_max = int(keep_max)
        self._scores: list[dict] = []
        
        self._load() # läs in filen (eller skapa tom)
        
    def top(self, n: int = 50) -> list[dict]:
        '''
        Returnerar dom n första resultaten.
        '''
        n = max(0, int(n))
        return list(self._scores[:n])
    
    # ------------------------- Interna hjälpmetoder -------------------------
    
    def _load(self) -> None:
        '''
        Läs in JSON-filen. Skapa en tom fil om den saknas.
        '''
        
        # Se till att mappen /data finns
        # 
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.path.exists():
            self._scores = []
            self._save()
            return
        
        try:
            with self.path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                
            items =data.get('scores') if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = []
                
            cleaned: list[dict] = []
            for x in items:
                if isinstance(x, dict) and 'player' in x and 'attempts' in x:
                    cleaned.append({"player": str(x["player"]) or "Anonymous", "attempts": int(x["attempts"])})
                    
            self._scores = cleaned
        except Exception:
            # Felhantering: Om filen är korrupt -> börja om på tom lista
            self._scores = []
            self._save()
            
    def _save(self) -> None:
        '''
        Spara listan till JSON fil som 'scores': [...]
        '''
        
        payload = {"scores": self._scores}
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)