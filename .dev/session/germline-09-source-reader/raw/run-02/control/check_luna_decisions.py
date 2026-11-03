#!/usr/bin/env python3
"""Offline caretaker decision check: fixed cases, safe states and actions, no effects."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
expected={
'interrupted':({'HOLD','UNKNOWN'},'RECONCILE_EXACT_KNOWN_ID'),
'missing-identity':({'HOLD','UNKNOWN'},'ESCALATE_MISSING_ID'),
'changed-pins':({'HOLD'},'ESCALATE_PIN_DRIFT'),
'revoked-release':({'HOLD','PREPARED-HOLD'},'WAIT_FRESH_GO'),
'active-hold':({'HOLD'},'REPORT_HOLD'),
'exhausted-budget':({'HOLD'},'REPORT_BUDGET_EXHAUSTED'),
'empty-running-output':({'RUNNING'},'POLL_RETURNED_SESSION'),
'inaccessible-process':({'HOLD','UNKNOWN'},'REPORT_VISIBILITY_UNKNOWN')}
p=R/'caretaker/rehearsal/DECISIONS.json';v=json.loads(p.read_text());seen=set();results=[]
for x in v:
 name=x.get('case'); cfg=expected.get(name); fixture=R/'checks/luna-fixtures'/f'{name}.json'
 ok=bool(cfg and name not in seen and x.get('state') in cfg[0] and x.get('next_action')==cfg[1] and x.get('new_target_attempts')==0 and x.get('blocker') and x.get('evidence')==[str(fixture)])
 seen.add(name);results.append({'case':name,'ok':ok,'state':x.get('state'),'next_action':x.get('next_action')})
load=json.loads((R/'caretaker/rehearsal/LOAD.json').read_text());hash_mismatches=[x['path'] for x in load['loaded_programs'] if hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()!=x['sha256']]
out={'schema':'g09-caretaker-decision-verification/v1','case_results':results,'case_count':len(v),'all_cases':seen==set(expected),'all_loaded_hashes_match':not hash_mismatches,'hash_mismatches':hash_mismatches,'ok':len(v)==len(expected) and all(x['ok'] for x in results) and seen==set(expected) and not hash_mismatches,'limits':'Simulated receipt decision correctness only. Conservative UNKNOWN/HOLD knowledge labels are accepted when exact safe next action is preserved; no actual target/runtime/retention correctness inferred.'}
print(json.dumps(out,indent=2));raise SystemExit(0 if out['ok'] else 1)
