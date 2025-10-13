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
    
def test_add_score_appends_sorts_and_keep_max(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=2)
        
    hsm.add_score('Nicklas', 7)
    hsm.add_score('Anna', 3)
    hsm.add_score('Kalle', 10)
        
    # endast top-2 ska vara kvar, sorterade på attempts stigande
    top = hsm.top(10)
    assert len(top) == 2
    assert [e['player'] for e in top] == ['Anna', 'Nicklas']
    assert [e['attempts'] for e in top] == [3, 7]
        
def test_add_score_persists_to_file(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=50)
    
    hsm.add_score('Anna', 3)
    hsm.add_score('Nicklas', 7)
    
    #läs tillbaka från fil och veriefiera att det sparats är sorterat
    data = json.loads(path.read_text(encoding='utf-8'))
    assert 'scores' in data
    assert [e['player'] for e in data['scores']] == ['Anna', 'Nicklas']
    assert [e['attempts'] for e in data['scores']] == [3, 7]
    
def test_add_score_allows_duplicate_players(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=50)
    
    hsm.add_score('Nicklas', 7)
    hsm.add_score('Nicklas', 4)
    hsm.add_score('Nicklas', 10)
    
    top = hsm.top(10)
    # alla 3 resultat ska vara kvar
    assert [e['attempts'] for e in top] == [4, 7, 10]
    assert all(e['player'] == 'Nicklas' for e in top)
    
def test_top_returns_copy_not_reference(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=50)
    
    hsm.add_score('Anna', 3)
    scores_copy =hsm.top(1)
    scores_copy[0]['attempts'] == 999 # manipulera kopian
    
    # original data ska vara opåverkat
    assert hsm.top(1)[0]['attempts'] == 3
    
def test_add_score_normalizes_inputs(tmp_path):
    path = tmp_path / 'hs.json'
    hsm = HighScoreManager(path=path, keep_max=50)
    
    hsm.add_score('  ', -5) # tomt namn + negativa försök
    hsm.add_score(None, '4') # None-name + försök som sträng
    hsm.add_score('Åsa', 2) # svenska tecken
    
    top = hsm.top(10)
    # första 2 posterna ska normaliseras till Anonymous/0 och Anonymous/4
    # och allt ska vara sorterat på attempts
    assert [e['attempts'] for e in top] == [0, 2, 4]
    assert top[0]['player'] == 'Anonymous'
    assert top[1]['player'] == 'Åsa'
    assert top[2]['player'] == 'Anonymous'
    
    # säkertställ att filen sparar å/ä/ö korrekt
    data = json.loads(path.read_text(encoding='utf-8'))
    assert any(e['player'] == 'Åsa' for e in data['scores'])
    
def test_init_creates_file_if_missing(tmp_path):
    path = tmp_path / 'hs.json'
    assert not path.exists()
    _ = HighScoreManager(path=path, keep_max=50)
    # _load() ska ha skapat filen direkt
    assert path.exists()
    
def test_load_accepts_plain_list_format(tmp_path):
    # highscore-filen kan vara en ren lista, inte bara {'scores': [...]}
    path = tmp_path / 'hs.json'
    payload = [
        {'player': 'C', 'attempts': 5},
        {'player': 'A', 'attempts': 8},
        {'player': 'B', 'attempts': 1},
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding='utf-8')
    
    hsm = HighScoreManager(path=path, keep_max=50)
    assert [e['player'] for e in hsm.top(3)] == ['B', 'C', 'A']
    assert [e['attempts'] for e in hsm.top(3)] == [1, 5, 8]