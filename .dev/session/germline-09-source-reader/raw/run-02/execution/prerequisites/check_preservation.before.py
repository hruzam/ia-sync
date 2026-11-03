#!/usr/bin/env python3
"""Offline preservation check; no file writes or target access."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]; B=R.parents[1]
v=json.loads((R/'BASELINE.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
old={p:sha(B/p)==h for p,h in v['old_bed_files'].items() if p not in v['allowed_old_bed_edits']}
foreign={p:sha(Path(p))==h for p,h in v['foreign_files'].items()}
# Authorized journal insertion preserves every original byte in its original order.
journal=Path('/home/hruzam/ia-sync/journal.host-cleanup.md')
receipt=R/'checks/JOURNAL.preservation.json'
if receipt.is_file():
 change=json.loads(receipt.read_text()); data=journal.read_bytes(); entry=Path(change['inserted_entry']).read_bytes(); offset=change['offset']
 foreign[str(journal)]=(data[offset:offset+len(entry)]==entry and hashlib.sha256(data[:offset]+data[offset+len(entry):]).hexdigest()==v['foreign_files'][str(journal)])
releases={p:json.loads((B/p).read_text()).get('authorized') is False for p in ['raw/control/RELEASE.json','raw/run-02/control/RELEASE.json']}
result={'protected_old_count':len(old),'old_mismatches':[p for p,ok in old.items() if not ok],'foreign_count':len(foreign),'foreign_mismatches':[p for p,ok in foreign.items() if not ok],'releases_false':releases,'ok':all(old.values()) and all(foreign.values()) and all(releases.values())}
print(json.dumps(result,indent=2)); raise SystemExit(0 if result['ok'] else 1)
