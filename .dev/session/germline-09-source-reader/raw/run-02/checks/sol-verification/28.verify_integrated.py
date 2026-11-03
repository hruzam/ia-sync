"""Final integrated artifact gate: offline reads only, no source-test reruns or processes."""
import hashlib,json
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[1];B=R.parents[1]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
previous=read(E/'19.delta.json');c=read(R/'CONTRACT.json');pins=read(R/'hold-line/sources.json')
paths={'adapter':R/'caretaker/run_operations.py','test':R/'repair/test_adapter.py','contract':R/'CONTRACT.json','pins':R/'hold-line/sources.json'}
hashes={k:sha(p) for k,p in paths.items()};assert hashes==previous['source_hashes'];assert len(pins['files'])==35
assert all(sha(x['path'])==x['sha256'] for x in pins['files'])
tunnel=Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py');assert sha(tunnel)==previous['unchanged_tunnel_sha256']
handoff=(R/'HANDOFF.md').read_text();assert all(h in handoff for h in hashes.values() if h!=hashes['test'])
assert all(p in handoff for p in c['named_vaults'].values())
assert c['attempt_budget']['maximum_target_ask_attempts']==5 and c['attempt_budget']['run01_consumed']==1
assert c['timeout_policy']['TUNNEL_CODEX_TIMEOUT']=='1800' and c['timeout_policy']['native_poll_seconds']==30
assert c['trial_bus_cycles']=={'C1':'30','I1':'31','C2':'32','I2':'33','C3':'34'}
assert all(term in handoff for term in ('not GO','PRODUCT is UNVERIFIED','per RPC/turn-completion phase','not a whole-command deadline','No retries' if 'No retries' in handoff else 'no retries','cycles30–34','Medium caretaker comparison is deferred','retained context remain unverified'))
releases={str(p):read(p)['authorized'] for p in (B/'raw/control/RELEASE.json',R/'control/RELEASE.json')};assert not any(releases.values())
assert read(R/'control/HOLD.json')['holds']==[]
assert all(not Path(p).exists() for p in c['named_vaults'].values())
asks={str(p):[str(x) for x in p.glob('*.operation.json') if read(x).get('kind')=='ask'] for p in (B/'raw/caretaker/operations',R/'caretaker/operations')}
assert len(asks[str(B/'raw/caretaker/operations')])==1 and not asks[str(R/'caretaker/operations')]
baseline=read(R/'BASELINE.json');protected={p:sha(B/p)==h for p,h in baseline['old_bed_files'].items() if p not in ('RUNBOOK.md','STATUS.md')};assert len(protected)==97 and all(protected.values())
journal=Path('/home/hruzam/ia-sync/journal.host-cleanup.md');jr=read(R/'checks/JOURNAL.preservation.json');data=journal.read_bytes();entry=Path(jr['inserted_entry']).read_bytes();offset=jr['offset']
assert len(entry)==jr['inserted_bytes'] and data[offset:offset+len(entry)]==entry
original=data[:offset]+data[offset+len(entry):];original_hash=hashlib.sha256(original).hexdigest();assert original_hash==baseline['foreign_files'][str(journal)]==jr['original_sha256'];assert sha(journal)==jr['final_sha256']
foreign={p:sha(p)==h for p,h in baseline['foreign_files'].items() if p!=str(journal)};assert len(foreign)==8 and all(foreign.values())
expected={'interrupted':({'HOLD','UNKNOWN'},'RECONCILE_EXACT_KNOWN_ID'),'missing-identity':({'HOLD','UNKNOWN'},'ESCALATE_MISSING_ID'),'changed-pins':({'HOLD'},'ESCALATE_PIN_DRIFT'),'revoked-release':({'HOLD','PREPARED-HOLD'},'WAIT_FRESH_GO'),'active-hold':({'HOLD'},'REPORT_HOLD'),'exhausted-budget':({'HOLD'},'REPORT_BUDGET_EXHAUSTED'),'empty-running-output':({'RUNNING'},'POLL_RETURNED_SESSION'),'inaccessible-process':({'HOLD','UNKNOWN'},'REPORT_VISIBILITY_UNKNOWN')}
decisions=read(R/'caretaker/rehearsal/DECISIONS.json');assert len(decisions)==8 and {x['case'] for x in decisions}==set(expected)
pairs=[]
for decision in decisions:
 name=decision['case'];path=R/'checks/luna-fixtures'/f'{name}.json';fixture=read(path);states,action=expected[name]
 assert fixture['simulated'] is True and fixture['target_turns']==0 and decision['state'] in states and decision['next_action']==action and decision['new_target_attempts']==0 and decision['evidence']==[str(path)] and decision['blocker']
 pairs.append({'case':name,'fixture_sha256':sha(path),'state':decision['state'],'next_action':action,'safe_no_replay':True})
loaded=read(R/'caretaker/rehearsal/LOAD.json');assert all(sha(x['path'])==x['sha256'] for x in loaded['loaded_programs'])
capture26=read(R/'caretaker/rehearsal/COMMANDS.json');assert 'not independently captured' in capture26['readiness']['exit_code_basis']
capture27=read(R/'caretaker/rehearsal-27/COMMAND.json');assert capture27['observed'] is True and capture27['exit_code']==2 and capture27['output_combined']=='unresolved or invalid run-02 HOLD.json\n'
final=read(R/'checks/FINAL.readiness.json');final_stdout=json.loads(final['stdout']);assert final['exit_code']==0 and final['release_authorized'] is False and final_stdout['release_authorized'] is False and final_stdout['pins']['sha256']==hashes['pins']
assert 'disposition: REVISE' in (B/'_bus/26.cartan.verdict.md').read_text() and 'disposition: ACCEPT' in (B/'_bus/27.cartan.verdict.md').read_text()
print(json.dumps({'verdict':'PASS','source_hashes':hashes,'handoff_sha256':sha(R/'HANDOFF.md'),'pins':35,'source_tests_reused':'cycle19 exact hashes; no broad reruns','releases_authorized':releases,'technical_holds':[],'role_vaults':0,'asks':asks,'protected_old_files':len(protected),'other_foreign_files':len(foreign),'journal_reconstruction_sha256':original_hash,'journal_final_sha256':sha(journal),'caretaker_fixture_decisions':pairs,'loaded_hashes_match':True,'capture26':'expected exit2 only; wrapper failure preserved','capture27':'observed exit2 with combined output','parent_final_readiness':'observed exit0/release false','target_model_turns':0,'limits':'Offline artifact/simulated decision gate only; actual GO, live availability, product, retention and High-versus-Medium performance not established.'},indent=2))
