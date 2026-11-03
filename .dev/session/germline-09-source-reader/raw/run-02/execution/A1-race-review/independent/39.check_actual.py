"""Read-only C1 preservation and approved-state hash check. No RPC or subprocess."""
import hashlib,json
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[2]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=read(E/'39.before.json');changed=[p for p,h in before['files'].items() if sha(p)!=h];assert not changed,changed
approved={'adapter':'bfa6a3fc7c09591881575c87fb8ad5bde066188cc42f814028dbeffff4d77b50','test':'d81a8e51340b2069c50c4fc10dcf4a099946374dc5fd50dbb28503b2e2063023','contract':'84be154eb074088af75f003cd760b0ccb904061afb46851135e8ad4203f1d214','pins':'d72e6b552f7e05e2e5c5657631526b989dea28d2cc3a372919845a1c86ad51db'}
paths={'adapter':R/'caretaker/run_operations.py','test':R/'repair/test_adapter.py','contract':R/'CONTRACT.json','pins':R/'hold-line/sources.json'}
assert {k:sha(p) for k,p in paths.items()}==approved
pins=read(paths['pins']);assert all(sha(x['path'])==x['sha256'] for x in pins['files'])
c=read(paths['contract']);plan=read(R/'caretaker/plan.C1.json');assert plan['contract_sha256']==approved['contract'] and plan['pins']['sha256']==approved['pins'] and set(plan['packets'])=={'R1','A1'}
for cycle,packet in plan['packets'].items():
 assert sha(packet['path'])==packet['sha256']
 template=next(x for x in read(c['files']['round_map'])['rounds'] if x['cycle']==cycle)['packet_template'];assert sha(template)==packet['template_sha256']
 assert all(sha(x['path'])==x['sha256'] for x in packet['named_inputs'])
asks=[]
for p in Path(c['files']['operations']).glob('*.operation.json'):
 v=read(p)
 assert v['status']=='completed' and v['exit']==0,(p,v.get('status'))
 assert all(sha(x['path'])==x['sha256'] for x in v['outputs'].values())
 if v.get('kind')=='ask':asks.append({'key':v['key'],'attempt_number':v['attempt_number']})
assert sorted(asks,key=lambda x:x['attempt_number'])==[{'key':'run02.R1.ask','attempt_number':1},{'key':'run02.A1.ask','attempt_number':2}]
selected=read(R/'execution/C1.head-selected-verification.json')['identities'];identities=read(R/'caretaker/identities.json')['roles'];observed={}
for role,vault in c['named_vaults'].items():
 state=read(vault);assert state['threadId']==selected[role]['threadId']==identities[role];assert state['lastTurnId']==selected[role]['lastTurnId'] and not state.get('inFlightTurnId');assert state['threadId']!=c['attempt_budget']['run01_thread'];observed[role]={'threadId':state['threadId'],'lastTurnId':state['lastTurnId']}
assert len(set(v['threadId'] for v in observed.values()))==2
assert not (R/'caretaker/plan.C2.json').exists() and not (R/'caretaker/packets/R2.prompt.txt').exists() and not (R/'caretaker/packets/A2.prompt.txt').exists()
assert read(R/'control/HOLD.json')['holds']
print(json.dumps({'verdict':'PASS','approved_hashes':approved,'critical_files_unchanged':len(before['files']),'pins_match':len(pins['files']),'asks':asks,'identities':observed,'c1_plan_sha256':sha(R/'caretaker/plan.C1.json'),'hold_active':True,'actual_release_authorized':read(R/'control/RELEASE.json')['authorized'],'no_live_future_plan_or_packets':True,'target_model_turns':0},indent=2))
