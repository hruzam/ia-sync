"""Independent applied identities, historical C1, accounting and preservation. Read-only."""
import hashlib,json,importlib.util
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[2];B=R.parents[1];V=E.parent;OLD=V/'before-application'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
proposal=read(R/'execution/A1-race-review/proposal/PROPOSAL.json');application=read(V/'APPLICATION.json');ruling=read(V/'RULING.actual.json')
assert sha(ruling['approved_proposal'])==ruling['proposal_sha256']=='6071a4b8f886ad47985d88fbad1f32e05db17cb6ef262d310b45fa55be4a71f7'
assert application['files']==proposal['files'] and len(application['files'])==4
approved={
 str(R/'caretaker/run_operations.py'):'4a9458a834e6825c8bfad44ec345bdcbd2f8d90483e9e93bdbcbcd1081042ae5',
 str(R/'repair/test_adapter.py'):'01a7a41da29181da64139d69b68afa763d79573c196b1fafede130b767c9e74d',
 str(R/'CONTRACT.json'):'d85068a29acae319710237594822230f1e761bf5df0656a208da14cc10d0216f',
 str(R/'hold-line/sources.json'):'ed61680ac03074e3f77b66a9fa6db474d6363d48ff8374ac1a713530e7f8bbbf'}
for item in application['files']:
 assert sha(item['actual'])==sha(item['candidate'])==item['new_sha256']==approved[item['actual']]
 before=OLD/Path(item['actual']).relative_to(R)
 assert sha(before)==item['old_sha256']
c=read(R/'CONTRACT.json');old_c=read(OLD/'CONTRACT.json');expected=json.loads(json.dumps(old_c));expected['files']['frozen_plan']=str(R/'caretaker/plan.C2.json');assert c==expected
old_source=(OLD/'caretaker/run_operations.py').read_text();new_source=(R/'caretaker/run_operations.py').read_text()
needle='        try:\n            if destination.exists():\n';assert old_source.count(needle)==1 and new_source==old_source.replace(needle,'        try:\n            prior_uncertainty(c)\n            if destination.exists():\n')
pins=read(c['files']['pins']);old_pins=read(OLD/'hold-line/sources.json');assert len(pins['files'])==len(old_pins['files'])==35
assert {x['path'] for x in pins['files']}=={x['path'] for x in old_pins['files']}
old_map={x['path']:x for x in old_pins['files']};rotated=[]
for item in pins['files']:
 assert sha(item['path'])==item['sha256'] and Path(item['path']).stat().st_size==item['bytes']
 if item!=old_map[item['path']]:rotated.append(item['path'])
assert set(rotated)==set(approved)-{str(R/'hold-line/sources.json')}
assert {k:v for k,v in pins.items() if k!='files'}=={k:v for k,v in old_pins.items() if k!='files'}
spec=importlib.util.spec_from_file_location('applied_readonly',R/'caretaker/run_operations.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
a.verify_pins(c)
release=read(c['files']['release']);old_release=read(OLD/'RELEASE.json');assert release['authorized'] is True
for key in ['observed_operator_message','recorded_at','message_reference','maximum_target_ask_attempts','timeout_seconds','named_vaults','delegated_enable_vaults','cumulative_target_ask_ceiling','run01_consumed_attempts']:
 assert release[key]==old_release[key],key
assert release['original_GO_snapshot']==str(OLD/'RELEASE.json')
assert any(x['reference']==str(V/'RULING.actual.json') and x['approved_proposal']==ruling['approved_proposal'] for x in release['operator_rulings'])
a.require_release(c,'ask','researcher');assert read(B/'raw/control/RELEASE.json')['authorized'] is False
assert read(c['files']['holds'])['holds']==['A1-approved-repair-awaits-independent-applied-state-verification']
try:a.require_no_holds(c)
except RuntimeError as exc:assert 'unresolved' in str(exc)
else:raise AssertionError('active hold not enforced')
caretaker=read(OLD/'caretaker.hashes.json');assert len(caretaker)==66
changed=[p for p,h in caretaker.items() if sha(p)!=h];assert not changed,changed
plan=read(R/'caretaker/plan.C1.json');assert sha(R/'caretaker/plan.C1.json')==proposal['preservation']['C1_plan_sha256']
assert plan['contract_sha256']==sha(OLD/'CONTRACT.json') and plan['pins']['sha256']==sha(OLD/'hold-line/sources.json') and set(plan['packets'])=={'R1','A1'}
for cycle,packet in plan['packets'].items():
 assert sha(packet['path'])==packet['sha256']
 item=a.rounds(c)[cycle];assert sha(item['packet_template'])==packet['template_sha256']
 for named in packet['named_inputs']:
  p=Path(named['path']);historical=OLD/p.relative_to(R)
  assert sha(historical if historical.is_file() else p)==named['sha256']
asks=[];enables=[];receipts=[]
for p in sorted(Path(c['files']['operations']).glob('*.operation.json')):
 v=read(p);assert a.inspect_receipt(p)['classification']=='completed-and-validated';receipts.append(p.name)
 if v.get('kind')=='ask':asks.append({'key':v['key'],'attempt_number':v['attempt_number']})
 if '--enable' in v.get('argv',[]):enables.append(v['role'])
assert sorted(asks,key=lambda x:x['attempt_number'])==[{'key':'run02.R1.ask','attempt_number':1},{'key':'run02.A1.ask','attempt_number':2}]
assert sorted(enables)==['auditor','researcher'] and a.ask_count(c)==2
assert c['attempt_budget']['run01_consumed']==1 and c['attempt_budget']['maximum_target_ask_attempts']==5
selected=read(R/'execution/C1.head-selected-verification.json')['identities'];identities=read(R/'caretaker/identities.json')['roles'];observed={}
for role,vault in c['named_vaults'].items():
 state=read(vault);assert state['threadId']==selected[role]['threadId']==identities[role]==proposal['preservation']['role_threads'][role]
 assert state['lastTurnId']==selected[role]['lastTurnId'] and not state.get('inFlightTurnId') and state['threadId']!=c['attempt_budget']['run01_thread']
 observed[role]={'threadId':state['threadId'],'lastTurnId':state['lastTurnId']}
assert len(set(x['threadId'] for x in observed.values()))==2
for p in ['caretaker/plan.C2.json','caretaker/packets/R2.prompt.txt','caretaker/packets/A2.prompt.txt']:assert not (R/p).exists()
before=read(E/'43.before.json')['files'];modified=[p for p,h in before.items() if sha(p)!=h]
head_owned={str(B/'STATUS.md'),str(R/'execution/main-intake.json')};assert set(modified)<=head_owned,modified
concurrent=[{'path':p,'before_sha256':before[p],'current_sha256':sha(p),'owner':'main; ownership confirmed in43 verifier message'} for p in modified]
# Independently reproduce both protected foreign byte reconstructions.
jrec=read(R/'execution/prerequisites/JOURNAL.reconciliation.json');journal=Path(jrec['journal']).read_bytes();assert hashlib.sha256(journal).hexdigest()==jrec['journal_sha256'];data=journal;spans=[]
for x in jrec['additions']:
 addition=Path(x['path']).read_bytes();assert len(addition)==x['bytes'] and hashlib.sha256(addition).hexdigest()==x['sha256'] and journal[x['offset']:x['offset']+len(addition)]==addition;spans.append((x['offset'],len(addition)))
spans.sort();assert all(i+n<=j for (i,n),(j,m) in zip(spans,spans[1:]))
for offset,length in reversed(spans):data=data[:offset]+data[offset+length:]
assert hashlib.sha256(data).hexdigest()==jrec['original_sha256']
prec=read(R/'execution/prerequisites/PULSE.reconciliation.json');pulse=Path(prec['path']).read_bytes();new=Path(prec['new_block']).read_bytes();old=Path(prec['old_block']).read_bytes()
assert hashlib.sha256(pulse).hexdigest()==prec['current_sha256'] and pulse.count(new)==1
assert hashlib.sha256(new).hexdigest()==prec['new_block_sha256'] and hashlib.sha256(old).hexdigest()==prec['old_block_sha256']
assert hashlib.sha256(pulse.replace(new,old,1)).hexdigest()==prec['original_sha256']
print(json.dumps({'verdict':'PASS','approved_four':approved,'pin_count':35,'rotated_pin_entries':rotated,'caretaker_before_snapshot_count':66,'unchanged_historical_caretaker_files':66,'historical_caretaker_mismatches':changed,'approved_adapter_transition_separately_verified':True,'c1_plan_sha256':sha(R/'caretaker/plan.C1.json'),'receipts_verified':len(receipts),'asks':asks,'run02_used':2,'run02_remaining':3,'run01_used':1,'cumulative_used':3,'cumulative_ceiling':6,'enables_consumed_per_role':enables,'identities':observed,'run01_release':False,'run02_release':True,'active_hold_enforced':True,'future_plan_packets_absent':True,'before_files':len(before),'unchanged_before_files':len(before)-len(modified),'concurrent_head_owned_changes':concurrent,'journal_reconstructed_sha256':jrec['original_sha256'],'pulse_reconstructed_sha256':prec['original_sha256'],'target_model_turns':0},indent=2))
