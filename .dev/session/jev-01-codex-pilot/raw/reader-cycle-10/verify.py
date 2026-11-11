import collections, difflib, hashlib, json, os, sys
from html.parser import HTMLParser
from pathlib import Path
import markdown

ROOT=Path('/home/hruzam/ia-sync')
DEST=ROOT/'.dev/session/jev-01-codex-pilot/raw/reader-cycle-10'
DEMO=Path('/home/hruzam/.local/share/jev-reader-demo-c9wshleb')
sys.path.insert(0,str(ROOT/'zsh/jev'))
import store,reader
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
vault=store.Vault(DEMO/'vault')
before={x['name']:hashlib.sha256(Path(x['ledger']).read_bytes()).hexdigest() for x in manifest['sessions']}
assert all(before[x['name']]==x['ledger_sha256'] for x in manifest['sessions'])
first=manifest['sessions'][0]
with vault.selected(first['session']) as ledger:
 notes=[event for event in ledger.events if event['kind']=='memory']
 source=reader.render(ledger,sequences={e['sequence'] for e in notes})
 assert len(notes)==6 and 'Selected sequences: `2, 3, 4, 5, 6, 7`' in source
 parsed_checks=[]
 for extensions in ([],['fenced_code']):
  p=Parsed(); p.feed(markdown.markdown(source,extensions=extensions))
  assert not {'script','img'} & set(p.tags)
  assert all(reader._text(e['data']['note']['text']) in p.values for e in notes)
  assert all(e['event_id'] in source and e['at'] in source for e in notes)
  slots=[v for e in notes for v in e['actor']['cli_sessions'].values() if v is not None]
  assert all(reader._text(v) in p.values for v in slots)
  parsed_checks.append({'extensions':extensions,'note_texts_preserved':len(notes),
                        'active_script_or_img_elements':sum(t in {'script','img'} for t in p.tags),
                        'nested_cli_values_verified':len(slots),'event_ids_and_timestamps':True})
 (DEST/'six-notes-after.md').write_text(source)
 os.chmod(DEST/'six-notes-after.md',0o600)
with vault.selected(manifest['sessions'][1]['session']) as ledger:
 request=next(e['request_id'] for e in ledger.events if e['kind']=='prepare')
 filtered=reader.render(ledger,request=request)
 assert all(f"### {e['sequence']}. `{e['kind']}`" in filtered for e in ledger.events if e['request_id']==request)
 assert all(f"### {e['sequence']}. `{e['kind']}`" not in filtered for e in ledger.events if e['request_id']!=request)
 for event in ledger.events:
  if event['request_id']!=request: continue
  data=event['data']
  hidden=((data.get('provider') or {}).get('body_base64') if event['kind']=='prepare' else
          data.get('raw_base64') if event['kind'] in {'reply','http'} else None)
  if hidden: assert hidden not in filtered
post={x['name']:hashlib.sha256(Path(x['ledger']).read_bytes()).hexdigest() for x in manifest['sessions']}
assert before==post
files=['zsh/jev/reader.py','zsh/jev/README.md','.dev/session/jev-01-codex-pilot/tests/test_reader.py']
hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}
for i,name in enumerate(files):
 before_text=(DEST/f'before-{i}.txt').read_text().splitlines(keepends=True)
 after_text=(ROOT/name).read_text().splitlines(keepends=True)
 (DEST/f'change-{i}.diff').write_text(''.join(difflib.unified_diff(before_text,after_text,fromfile='before/'+name,tofile='after/'+name)))
result={'parser':'Python-Markdown '+markdown.__version__,'configurations':parsed_checks,'filters_and_payload_omissions':'pass',
        'fixture_hashes_before':before,'fixture_hashes_after':post,'fixture_hashes_unchanged':True,'source_sha256_after':hashes,
        'rendered_source_view':str(DEST/'six-notes-after.md')}
(DEST/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
