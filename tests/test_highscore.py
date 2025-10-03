# tests/test_highscore.py
import json
from modules.highscore import HighScoreManager

def test_sorting_by_attempts(tmp_path):
    # använder temporär fil så att vi inte rör riktig data
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=50)
    
    # osorterade resultat
    hsm._scores = [
        {'player': 'Nicklas', 'attempts': 7},
        {'player': 'Anna', 'attempts': 3},
        {'player': 'Kalle', 'attempts': 10},
    ]
    
    # kör sorteringen
    hsm._sort_scores()
    
    # varifiera att attempts är stigande
    assert [e['attempts'] for e in hsm._scores] == [3, 7, 10]
    assert [e['player'] for e in hsm._scores] == ['Anna', 'Nicklas', 'Kalle']
    
def test_keep_max_limit(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=2)
    
    hsm._scores = [
        {'player': 'Nicklas', 'attempts': 7},
        {'player': 'Anna', 'attempts': 3},
        {'player': 'Kalle', 'attempts': 10},
    ]
    
    hsm._sort_scores()
    
    # bara dom 2 bästa ska vara kvar och i rätt ordning
    assert len(hsm._scores) == 2
    assert [e['player'] for e in hsm._scores] == ['Anna', 'Nicklas']
    assert [e['attempts'] for e in hsm._scores] == [3, 7]
    
def test_load_sorts_on_init(tmp_path):
    # skapa en JSON-fil med osorterad data
    path = tmp_path / 'hs.json'
    payload = {
        'scores': [
            {'player': 'A', 'attempts': 8},
            {'player': 'B', 'attempts': 1},
            {'player': 'C', 'attempts': 5},
        ]
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding='utf-8')
    
    # init ska läsa in och (numrera) sortera direkt via _sort_scores()
    hsm = HighScoreManager(path=path, keep_max=50)
    
    # top(3) ska vara sorterade enligt attempts
    assert [e['player'] for e in hsm.top(3)] == ['B', 'C', 'A']
    assert [e['attempts'] for e in hsm.top(3)] == [1, 5, 8]