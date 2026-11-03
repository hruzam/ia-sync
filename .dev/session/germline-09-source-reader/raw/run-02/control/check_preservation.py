#!/usr/bin/env python3
"""Current G09 preservation check; exact evidence reconstruction, no file writes or target access."""
from pathlib import Path
import argparse,hashlib,json
R=Path(__file__).resolve().parents[1];B=R.parents[1]
p=argparse.ArgumentParser();p.add_argument('--release-mode',choices=['pre-release','run02-authorized'],default='pre-release');args=p.parse_args()
v=json.loads((R/'BASELINE.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
old={name:sha(B/name)==digest for name,digest in v['old_bed_files'].items() if name not in v['allowed_old_bed_edits']}
foreign={name:sha(Path(name))==digest for name,digest in v['foreign_files'].items()}
journal=Path('/home/hruzam/ia-sync/journal.host-cleanup.md');reconciliation=R/'execution/prerequisites/JOURNAL.reconciliation.json';journal_result=None
if reconciliation.is_file():
 rec=json.loads(reconciliation.read_text());original=journal.read_bytes();data=original;valid=(hashlib.sha256(original).hexdigest()==rec['journal_sha256']);spans=[]
 for item in rec['additions']:
  entry=Path(item['path']).read_bytes();offset=item['offset'];valid=valid and len(entry)==item['bytes'] and hashlib.sha256(entry).hexdigest()==item['sha256'] and original[offset:offset+len(entry)]==entry;spans.append((offset,len(entry)))
 spans.sort();valid=valid and all(a+n<=z for (a,n),(z,_) in zip(spans,spans[1:]))
 for offset,length in reversed(spans):data=data[:offset]+data[offset+length:]
 reconstructed=hashlib.sha256(data).hexdigest();valid=valid and reconstructed==rec['original_sha256']==v['foreign_files'][str(journal)];foreign[str(journal)]=valid;journal_result={'reconciliation':str(reconciliation),'reconstructed_sha256':reconstructed,'ok':valid}
else:
 receipt=R/'checks/JOURNAL.preservation.json'
 if receipt.is_file():
  change=json.loads(receipt.read_text());data=journal.read_bytes();entry=Path(change['inserted_entry']).read_bytes();offset=change['offset'];foreign[str(journal)]=(data[offset:offset+len(entry)]==entry and hashlib.sha256(data[:offset]+data[offset+len(entry):]).hexdigest()==v['foreign_files'][str(journal)])
pulse=Path('/home/hruzam/ia-sync/pulse.md');pulse_receipt=R/'execution/prerequisites/PULSE.reconciliation.json'
if pulse_receipt.is_file():
 rec=json.loads(pulse_receipt.read_text());data=pulse.read_bytes();new=Path(rec['new_block']).read_bytes();old_block=Path(rec['old_block']).read_bytes();valid=(hashlib.sha256(data).hexdigest()==rec['current_sha256'] and hashlib.sha256(new).hexdigest()==rec['new_block_sha256'] and hashlib.sha256(old_block).hexdigest()==rec['old_block_sha256'] and data.count(new)==1);reconstructed=data.replace(new,old_block,1);foreign[str(pulse)]=valid and hashlib.sha256(reconstructed).hexdigest()==rec['original_sha256']==v['foreign_files'][str(pulse)]
release_values={name:json.loads((B/name).read_text()).get('authorized') for name in ['raw/control/RELEASE.json','raw/run-02/control/RELEASE.json']}
release_ok=release_values['raw/control/RELEASE.json'] is False and release_values['raw/run-02/control/RELEASE.json'] is (args.release_mode=='run02-authorized')
result={'protected_old_count':len(old),'old_mismatches':[name for name,ok in old.items() if not ok],'foreign_count':len(foreign),'foreign_mismatches':[name for name,ok in foreign.items() if not ok],'journal_reconciliation':journal_result,'release_mode':args.release_mode,'releases_authorized':release_values,'release_state_matches':release_ok,'ok':all(old.values()) and all(foreign.values()) and release_ok}
print(json.dumps(result,indent=2));raise SystemExit(0 if result['ok'] else 1)
