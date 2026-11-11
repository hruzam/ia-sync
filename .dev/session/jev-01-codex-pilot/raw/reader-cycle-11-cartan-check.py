"""Independent cycle11 checks; no peer evidence/source or ledger writes."""
import difflib
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import markdown

BED = Path(__file__).resolve().parents[1]
REPO = BED.parents[2]
sys.path.insert(0, str(REPO / 'zsh/jev'))
import reader
import store

class Parsed(HTMLParser):
    def __init__(self):
        super().__init__(); self.values = []; self.current = None; self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'pre': self.current = []
    def handle_data(self, data):
        if self.current is not None: self.current.append(data)
    def handle_endtag(self, tag):
        if tag == 'pre' and self.current is not None:
            self.values.append(''.join(self.current)); self.current = None

files = ['zsh/jev/reader.py', '.dev/session/jev-01-codex-pilot/tests/test_reader.py']
peer = BED / 'raw/reader-cycle-11'
for i, name in enumerate(files):
    before = (peer / f'before-{i}.txt').read_text().splitlines(keepends=True)
    after = (REPO / name).read_text().splitlines(keepends=True)
    expected = ''.join(difflib.unified_diff(before, after, fromfile='before/'+name, tofile='after/'+name))
    assert expected == (peer / f'change-{i}.diff').read_text()
manifest = json.loads(Path('/home/hruzam/.local/share/jev-reader-demo-c9wshleb/manifest.json').read_text())
vault = store.Vault(manifest['root'])
with vault.selected(manifest['sessions'][0]['session']) as ledger:
    notes = [e for e in ledger.events if e['kind'] == 'memory']
    source = reader.render(ledger, sequences={e['sequence'] for e in notes})
    for ext in ([], ['fenced_code']):
        parsed = Parsed(); parsed.feed(markdown.markdown(source, extensions=ext))
        assert not {'script', 'img'} & set(parsed.tags)
        assert all(reader._text(e['data']['note']['text']) in parsed.values for e in notes)
for entry in manifest['sessions']:
    assert hashlib.sha256(Path(entry['ledger']).read_bytes()).hexdigest() == entry['ledger_sha256']
cases = []
for text in ['before\n~~~html\n<script>DEMO_ONLY</script>\n~~~\nafter',
             'before\n\n~~~\nliteral\n~~~\n\nafter']:
    event = {'sequence': 1, 'kind': 'memory', 'event_id': 'fixture', 'at': 'fixture',
             'request_id': None, 'previous_event_id': None, 'actor': {}, 'data': {'note': {'text': text}}}
    source = reader.render(SimpleNamespace(events=[event], path='/synthetic', session_id='synthetic', tail=None))
    for ext in ([], ['fenced_code']):
        parsed = Parsed(); parsed.feed(markdown.markdown(source, extensions=ext))
        cases.append({'text': text, 'extensions': ext, 'preserved': text in parsed.values,
                      'pre_values': parsed.values, 'active_script': 'script' in parsed.tags})
result = {'parser': markdown.__version__, 'scope_diffs_match': True,
          'six_original_notes_preserved': True, 'fixture_hashes_unchanged': True,
          'tilde_fence_cases': cases,
          'source_sha256': hashlib.sha256((REPO / 'zsh/jev/reader.py').read_bytes()).hexdigest(),
          'installed_sha256': hashlib.sha256(Path('/home/hruzam/.config/zsh/jev/reader.py').read_bytes()).hexdigest()}
assert all(c['preserved'] and not c['active_script'] for c in cases)
print(json.dumps(result, indent=2))
