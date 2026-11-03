"""Independent offline hashes, preservation and no-dispatch inventory."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=R.parents[1]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
base=json.loads((R/'BASELINE.json').read_text())
protected={p:sha(B/p)==h for p,h in base['old_bed_files'].items() if p not in ('RUNBOOK.md','STATUS.md')}
foreign={p:sha(p)==h for p,h in base['foreign_files'].items()}
journal=Path('/home/hruzam/ia-sync/journal.host-cleanup.md');copy=R/'control/journal.before.bin'
if copy.exists() and sha(copy)==base['foreign_files'][str(journal)]:foreign[str(journal)]=journal.read_bytes().endswith(copy.read_bytes())
pins=json.loads((R/'hold-line/sources.json').read_text())
badpins=[p['path'] for p in pins['files'] if sha(p['path'])!=p['sha256']]
hashes={str(p):sha(p) for p in [R/'CONTRACT.json',R/'hold-line/sources.json',R/'caretaker/run_operations.py',Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')]}
releases={str(p):json.loads(p.read_text())['authorized'] for p in [B/'raw/control/RELEASE.json',R/'control/RELEASE.json']}
asks={}
for root in (B/'raw/caretaker/operations',R/'caretaker/operations'):
 asks[str(root)]=[str(p) for p in root.glob('*.operation.json') if json.loads(p.read_text()).get('kind')=='ask']
result={'old_baseline_count':len(base['old_bed_files']),'protected_count':len(protected),'protected_mismatch':[p for p,v in protected.items() if not v],'foreign_count':len(foreign),'foreign_mismatch':[p for p,v in foreign.items() if not v],'pins_count':len(pins['files']),'pins_mismatch':badpins,'hashes':hashes,'release_authorized':releases,'asks':asks,'ok':all(protected.values()) and all(foreign.values()) and not badpins and not any(releases.values()) and len(asks[str(B/'raw/caretaker/operations')])==1 and not asks[str(R/'caretaker/operations')]}
print(json.dumps(result,indent=2));raise SystemExit(0 if result['ok'] else 1)
