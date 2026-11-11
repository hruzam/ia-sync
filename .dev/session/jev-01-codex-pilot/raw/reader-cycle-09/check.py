import collections, fcntl, hashlib, json, os, pty, select, struct, subprocess, sys, termios, time
from pathlib import Path

DEST = Path('/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/raw/reader-cycle-09')
DEMO = Path('/home/hruzam/.local/share/jev-reader-demo-c9wshleb')
sys.path.insert(0, '/home/hruzam/.config/zsh/jev')
import browser, reader
manifest = json.loads((DEMO/'manifest.json').read_text())
vault, sessions = browser.discover(str(DEMO/'vault'))
expected = {x['session']: x for x in manifest['sessions']}
assert len(sessions) == 4 and len(expected) == 4
reports = []
for item in sessions:
    target = expected[item['session']]
    with vault.selected(item['session']) as ledger:
        kinds = dict(collections.Counter(x['kind'] for x in ledger.events))
        digest = hashlib.sha256(ledger.path.read_bytes()).hexdigest()
        assert len(ledger.events) == target['events'] and kinds == target['kinds']
        assert digest == target['ledger_sha256']
        reports.append({'name':target['name'],'session':item['session'],'events':len(ledger.events),
                        'memories':kinds.get('memory',0),'sha256':digest})
index = next(i for i, s in enumerate(sessions) if s['session'] == manifest['sessions'][0]['session'])
env = os.environ.copy(); env.update(TERM='xterm', XDG_RUNTIME_DIR=str(DEST.resolve()))
os.chmod(DEST, 0o700)
m, s = pty.openpty()
fcntl.ioctl(s, termios.TIOCSWINSZ, struct.pack('HHHH',24,80,0,0))
command = ['/usr/bin/python3','-B','/home/hruzam/.config/zsh/jev/browser.py','--root',str(DEMO/'vault')]
process = subprocess.Popen(command,stdin=s,stdout=s,stderr=s,env=env); os.close(s)
transcript=b''
for keys in (b'j'*index, b'\r', b'm', b'a', b'p'):
    time.sleep(.2)
    if keys: os.write(m,keys)
    ready,_,_=select.select([m],[],[],0)
    if ready:
        try: transcript += os.read(m,65536)
        except OSError: pass
while process.poll() is None:
    ready,_,_=select.select([m],[],[],3)
    if not ready:
        process.kill(); raise RuntimeError('PTY timeout')
    try: transcript += os.read(m,65536)
    except OSError: break
process.wait(); os.close(m)
assert process.returncode == 0
views = sorted(DEST.glob('jev-view-*/view.md'), key=lambda p:p.stat().st_mtime_ns)
assert len(views) == 1
view = views[0]; text = view.read_text()
with vault.selected(manifest['sessions'][0]['session']) as ledger:
    notes = [e for e in ledger.events if e['kind']=='memory']
    assert len(notes)==6
    checks=[]
    for event in notes:
        note=event['data']['note']
        result={'sequence':event['sequence'],'event_id':event['event_id'],
                'text_present':reader._text(note['text']) in text,
                'event_id_present':event['event_id'] in text,
                'recorded_time_present':event['at'] in text,
                'author_present':reader._text(note['author']) in text,
                'actor_values_present':all(reader._text(v) in text for v in event['actor'].values() if isinstance(v,str)),
                'refs_present':all(ref in text for ref in note['refs'])}
        assert all(v for k,v in result.items() if k.endswith('_present'))
        checks.append(result)
    assert 'Selected sequences: `2, 3, 4, 5, 6, 7`' in text
    assert text.count('### ') == 6
post = {x['name']:hashlib.sha256(Path(x['ledger']).read_bytes()).hexdigest() for x in manifest['sessions']}
assert all(post[x['name']] == x['ledger_sha256'] for x in manifest['sessions'])
result={'schema':'reader-cycle-09/v1','command':command,'terminal':'PTY 80x24','exit':process.returncode,
        'scenario_order':[x['name'] for x in reports], 'scenario_counts':reports,
        'total_events':sum(x['events'] for x in reports),'total_memories':sum(x['memories'] for x in reports),
        'memory_view':str(view),'memory_view_mode':oct(view.stat().st_mode & 0o777),
        'memory_checks':checks,'ledger_hashes_after':post,'all_hashes_match_manifest':True,
        'terminal_transcript':str(DEST/'pty.raw')}
(DEST/'pty.raw').write_bytes(transcript)
(DEST/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'sessions':len(sessions),'events':result['total_events'],'memories':result['total_memories'],
                  'notes_verified':len(checks),'view':str(view),'ledger_hashes_match':True,'pty_exit':process.returncode},indent=2))
