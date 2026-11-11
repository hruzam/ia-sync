import difflib, hashlib, json, sys
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
import markdown

ROOT=Path('/home/hruzam/ia-sync')
DEST=ROOT/'.dev/session/jev-01-codex-pilot/raw/reader-cycle-11'
DEMO=Path('/home/hruzam/.local/share/jev-reader-demo-c9wshleb')
sys.path.insert(0,str(ROOT/'zsh/jev'))
import reader, store
class Parsed(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True); self.tags=[]; self.values=[]; self.current=None
 def handle_starttag(self,tag,attrs):
  self.tags.append(tag)
  if tag=='pre': self.current=[]
 def handle_data(self,data):
  if self.current is not None: self.current.append(data)
 def handle_endtag(self,tag):
  if tag=='pre' and self.current is not None:
   self.values.append(''.join(self.current)); self.current=None
manifest=json.loads((DEMO/'manifest.json').read_text())
before={x['name']:hashlib.sha256(Path(x['ledger']).read_bytes()).hexdigest() for x in manifest['sessions']}
assert all(before[x['name']]==x['ledger_sha256'] for x in manifest['sessions'])
cases=['before\n~~~html\n<script>DEMO_ONLY</script>\n~~~\nafter', 'before\n\n~~~\nliteral\n~~~\n\nafter']
results=[]
for text in cases:
 event={'sequence':1,'kind':'memory','event_id':'fixture','at':'fixture','request_id':None,
        'previous_event_id':None,'actor':{'cli_sessions':{'codex':'fixture-codex'}},'data':{'note':{'text':text}}}
 source=reader.render(SimpleNamespace(events=[event],path='/synthetic',session_id='synthetic',tail=None))
 for ext in ([],['fenced_code']):
  parsed=Parsed(); parsed.feed(markdown.markdown(source,extensions=ext))
  outcome={'text':text,'extensions':ext,'preserved':text in parsed.values,
           'script_elements':parsed.tags.count('script'),'nested_cli_preserved':'fixture-codex' in parsed.values}
  assert outcome['preserved'] and not outcome['script_elements'] and outcome['nested_cli_preserved']
  results.append(outcome)
vault=store.Vault(DEMO/'vault')
with vault.selected(manifest['sessions'][0]['session']) as ledger:
 notes=[e for e in ledger.events if e['kind']=='memory']
 source=reader.render(ledger,sequences={e['sequence'] for e in notes})
 fixture_checks=[]
 for ext in ([],['fenced_code']):
  parsed=Parsed(); parsed.feed(markdown.markdown(source,extensions=ext))
  assert all(reader._text(e['data']['note']['text']) in parsed.values and e['event_id'] in source and e['at'] in source for e in notes)
  slots=[v for e in notes for v in e['actor']['cli_sessions'].values() if v is not None]
  assert all(v in parsed.values for v in slots) and not {'script','img'} & set(parsed.tags)
  fixture_checks.append({'extensions':ext,'preserved_notes':len(notes),'nested_cli_values':len(slots),'script_or_img':0})
after={x['name']:hashlib.sha256(Path(x['ledger']).read_bytes()).hexdigest() for x in manifest['sessions']}
assert before==after
files=['zsh/jev/reader.py','.dev/session/jev-01-codex-pilot/tests/test_reader.py']
hashes={}
for i,name in enumerate(files):
 new=(ROOT/name).read_bytes(); hashes[name]=hashlib.sha256(new).hexdigest()
 old=(DEST/f'before-{i}.txt').read_text().splitlines(keepends=True)
 (DEST/f'change-{i}.diff').write_text(''.join(difflib.unified_diff(old,new.decode().splitlines(keepends=True),fromfile='before/'+name,tofile='after/'+name)))
result={'python_markdown_version':markdown.__version__,'cases':results,'fixture_checks':fixture_checks,
        'fixture_hashes_before':before,'fixture_hashes_after':after,'fixture_hashes_unchanged':True,
        'source_hashes_after':hashes,'installed_reader_sha256':hashlib.sha256(Path('/home/hruzam/.config/zsh/jev/reader.py').read_bytes()).hexdigest()}
(DEST/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
