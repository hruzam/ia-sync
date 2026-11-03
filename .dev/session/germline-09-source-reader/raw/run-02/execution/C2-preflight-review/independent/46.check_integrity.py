"""Read-only exact-source/pins/preservation-integrity and original artifact checks."""
import hashlib,importlib.util,json
from pathlib import Path
E=Path(__file__).resolve().parent;Q=E.parent;R=Q.parents[1];B=R.parents[1]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(Q/'check_checkpoint.py')=='09ec3f47fe871d58ad8b61f7006c1b671e44497d5ec1f276d617ade6813cf4e7'
approved=read(R/'execution/resume-02/APPLICATION.json')['files']
for x in approved:assert sha(x['actual'])==x['new_sha256']
spec=importlib.util.spec_from_file_location('integrity46',R/'caretaker/run_operations.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);c=a.contract();a.verify_pins(c)
assert len(read(c['files']['pins'])['files'])==35
originals=[]
for variant in ('failed','corrected'):
 for kind in ('py','output'):
  name=f'32.local-preflight-{variant}.{kind}.txt';p=Q/name;original=R/'caretaker/results'/name
  assert sha(p)==sha(original);originals.append({'name':name,'sha256':sha(p)})
for line in (Q/'preflight-sha256.txt').read_text().splitlines():
 digest,path=line.split(None,1);assert sha(Path('/home/hruzam/ia-sync')/path.strip())==digest
before=read(E/'46.before.json')['files'];changed=[p for p,h in before.items() if sha(p)!=h]
allowed={str(B/'STATUS.md'),str(R/'execution/main-intake.json'),str(B/'_bus/32.caretaker.return.md'),str(R/'caretaker/tunnel.auditor.state.json'),str(R/'caretaker/operations/run02.A2.ask.operation.json')}
assert set(changed)<=allowed,changed
hold=read(c['files']['holds']);assert hold['holds']==['C2-caretaker-local-assertion-failure-awaits-Terra-check']
asks=[]
for p in Path(c['files']['operations']).glob('*.operation.json'):
 v=read(p)
 if v.get('kind')=='ask':
  assert a.inspect_receipt(p)['classification']=='completed-and-validated';asks.append({'key':v['key'],'attempt':v['attempt_number']})
assert sorted(x['attempt'] for x in asks)==[1,2,3,4]
assert read(E/'46.actual-checkpoint.json')['status']=='COMPLETED_IDENTITIES_OBSERVED'
assert read(E/'46.actual-checkpoint.json')['dispatch_ready'] is False
print(json.dumps({'verdict':'PASS','checker_sha256':sha(Q/'check_checkpoint.py'),'approved_four_match':True,'pins_match':35,'original_preflight_copies_match':originals,'before_count':len(before),'unchanged_before_count':len(before)-len(changed),'concurrent_expected_changes':[{'path':p,'before_sha256':before[p],'current_sha256':sha(p)} for p in changed],'active_hold':hold['holds'],'asks':sorted(asks,key=lambda x:x['attempt']),'run02_used':4,'cumulative_used':5,'cumulative_ceiling':6,'verification_production_writes':0},indent=2))
