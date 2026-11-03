"""Verify exact proposal metadata and C1-preserving compile in a temporary path overlay."""
import copy,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
from types import ModuleType
E=Path(__file__).resolve().parent;REVIEW=E.parent;R=REVIEW.parents[1]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
p=REVIEW/'proposal';expected={'adapter':'4a9458a834e6825c8bfad44ec345bdcbd2f8d90483e9e93bdbcbcd1081042ae5','test':'01a7a41da29181da64139d69b68afa763d79573c196b1fafede130b767c9e74d','contract':'d85068a29acae319710237594822230f1e761bf5df0656a208da14cc10d0216f','pins':'ed61680ac03074e3f77b66a9fa6db474d6363d48ff8374ac1a713530e7f8bbbf'}
files={'adapter':REVIEW/'candidate/run_operations.py','test':REVIEW/'candidate/test_adapter.py','contract':p/'CONTRACT.proposed.json','pins':p/'sources.proposed.json'};assert {k:sha(v) for k,v in files.items()}==expected
actual_c=read(R/'CONTRACT.json');new_c=read(files['contract']);single=copy.deepcopy(actual_c);single['files']['frozen_plan']=str(R/'caretaker/plan.C2.json');assert new_c==single
old_pins=read(R/'hold-line/sources.json');new_pins=read(files['pins']);oldmeta=copy.deepcopy(old_pins);newmeta=copy.deepcopy(new_pins);oldmeta.pop('files');newmeta.pop('files');assert oldmeta==newmeta
assert len(old_pins['files'])==len(new_pins['files'])==35
expected_inputs={str(R/'caretaker/run_operations.py'):files['adapter'],str(R/'repair/test_adapter.py'):files['test'],str(R/'CONTRACT.json'):files['contract']};changed=[]
for old,new in zip(old_pins['files'],new_pins['files']):
 assert old['path']==new['path']
 if old!=new:
  target=expected_inputs[new['path']];assert new==dict(old,sha256=sha(target),bytes=target.stat().st_size);changed.append(new['path'])
 else:assert sha(old['path'])==old['sha256']
assert set(changed)==set(expected_inputs)
proposal=read(p/'PROPOSAL.json');assert proposal['applied'] is False
for row in proposal['files']:assert sha(row['actual'])==row['old_sha256'] and sha(row['candidate'])==row['new_sha256']
pending=read(p/'RELEASE.pending-ruling.json');assert pending['authorized'] is False and pending['proposal_only'] is True and pending['operator_ruling_reference'] is None
assert pending['contract_sha256']==expected['contract'] and pending['source_manifest_sha256']==expected['pins'] and pending['named_vaults']==actual_c['named_vaults']
assert proposal['preservation']['run02_attempts']==2 and proposal['preservation']['run02_remaining']==3
assert sha(proposal['pending_release']['path'])==proposal['pending_release']['sha256'] and sha(proposal['patch']['path'])==proposal['patch']['sha256']
original=(REVIEW/'run_operations.frozen.bfa6a3fc.py').read_bytes();needle=b"        try:\n            if destination.exists():\n";assert original.count(needle)==1
assert files['adapter'].read_bytes()==original.replace(needle,b"        try:\n            prior_uncertainty(c)\n            if destination.exists():\n")
with tempfile.TemporaryDirectory(prefix='g09-sol39-transition-') as directory:
 shadow=Path(directory)/'raw/run-02';shutil.copytree(R/'caretaker',shadow/'caretaker')
 def relocate(v):
  if isinstance(v,str) and v.startswith(str(R)+'/'):return str(shadow)+v[len(str(R)):]
  if isinstance(v,list):return [relocate(x) for x in v]
  if isinstance(v,dict):return {k:relocate(x) for k,x in v.items()}
  return v
 c=relocate(new_c);c['cwd']=str(shadow.parents[1]);dump(shadow/'CONTRACT.json',c)
 dump(shadow/'control/ROUND-MAP.json',relocate(read(R/'control/ROUND-MAP.json')))
 dump(shadow/'control/RELEASE.json',relocate(pending));dump(shadow/'control/HOLD.json',read(R/'control/HOLD.json'))
 for key,destination in [('adapter',shadow/'caretaker/run_operations.py'),('test',shadow/'repair/test_adapter.py')]:destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(files[key].read_bytes())
 overlay=copy.deepcopy(new_pins)
 for item in overlay['files']:
  original_path=Path(item['path']);destination=Path(relocate(str(original_path)))
  if destination!=original_path:
   if not destination.exists():destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(original_path.read_bytes())
   item.update(path=str(destination),sha256=sha(destination),bytes=destination.stat().st_size)
 dump(shadow/'hold-line/sources.json',overlay)
 a=ModuleType('independent_future_plan');a.__file__=str(shadow/'caretaker/run_operations.py');exec(compile(Path(a.__file__).read_bytes(),a.__file__,'exec'),a.__dict__);a.B,a.R=shadow.parents[1],shadow
 before={str(x):sha(x) for x in (shadow/'caretaker').rglob('*') if x.is_file()};assert not Path(c['files']['frozen_plan']).exists();assert a.ask_count(c)==2
 # Explicit fake D1/I1 inputs; no actual product paths are created or executed.
 fake_inputs=[shadow/'control/DECISION.01.md',shadow/'control/CONTRACT.01.json',shadow/'implementation/I1/MANIFEST.json',shadow/'implementation/I1/fixture.data']
 for number,path in enumerate(fake_inputs):path.parent.mkdir(parents=True,exist_ok=True);path.write_text('fake frozen input '+str(number)+'\n')
 plan=a.compile_packets(['R2','A2'],[str(x) for x in fake_inputs]);assert set(plan['packets'])=={'R2','A2'}
 for cycle in ('R2','A2'):a.current_packet(c,a.rounds(c)[cycle])
 assert a.ask_count(c)==2 and all(sha(path)==h for path,h in before.items())
 c2=Path(c['files']['frozen_plan']);c2_bytes=c2.read_bytes()
 try:a.compile_packets(['R1'],[])
 except RuntimeError as exc:assert 'replace frozen packet' in str(exc)
 else:raise AssertionError('historical R1 packet regenerated')
 assert c2.read_bytes()==c2_bytes and all(sha(path)==h for path,h in before.items())
 migration={'c1_plan_sha256':sha(shadow/'caretaker/plan.C1.json'),'existing_caretaker_files_preserved':len(before),'new_plan_rounds':sorted(plan['packets']),'new_plan_binds_rotated_overlay_pins':plan['pins']==a.verify_pins(c),'asks_before':2,'asks_after':a.ask_count(c),'old_cold_packet_regeneration_refused':True,'new_profile_enable_ask_calls':0,'overlay_note':'Only temp path relocation and matching overlay hashes differ from exact staged metadata; actual35-entry proposal verified separately above.'}
print(json.dumps({'verdict':'PASS','proposal_hashes':expected,'source_manifest_changed_paths':changed,'contract_changed_fields':['files.frozen_plan'],'pending_release_authorized':False,'migration':migration,'target_model_turns':0},indent=2))
