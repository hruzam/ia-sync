"""Independent adapter adversarial checks using only temporary data and fake subprocesses."""
import hashlib, importlib.util, json, subprocess, tempfile, threading
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def imp(name,path):
 s=importlib.util.spec_from_file_location(name,path);o=importlib.util.module_from_spec(s);s.loader.exec_module(o);return o
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
a=imp('sol_boundaries',R/'caretaker/run_operations.py');f=imp('sol_fixture',R/'repair/test_adapter.py')
rows=[]
def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def refusal(name,fn,needle=None):
 try:fn()
 except RuntimeError as exc:
  assert needle is None or needle in str(exc),(name,str(exc));rows.append({'check':name,'result':'refused','reason':str(exc)});return
 raise AssertionError(name+' unexpectedly accepted')
def valid_receipt(path,kind='read'):
 out=path.parent/'valid-output';out.write_text('output')
 value={'kind':kind,'status':'completed','exit':0,'outputs':{c:{'path':str(out),'sha256':sha(out)} for c in ('stdout','stderr')}};dump(path,value);return value
with tempfile.TemporaryDirectory(prefix='g09-sol-boundaries-') as directory:
 root=Path(directory);run,files,vault=f.fixture(root);a.B,a.R=root,run
 c=a.contract();c['target_profile']['effort']='high';dump(run/'CONTRACT.json',c)
 release=a.load(files['release']);release['contract_sha256']=sha(run/'CONTRACT.json');dump(files['release'],release)
 calls=[]
 def fake(argv,**kwargs):calls.append(argv);return subprocess.CompletedProcess(argv,0,b'fake',b'')
 a.subprocess.run=fake
 a.compile_packets(['R1'],[])
 for field,bad,needle in [('authorized',False,'not authorized'),('observed_operator_message',None,'operator'),('contract_sha256','0'*64,'contract hash'),('source_manifest_sha256','0'*64,'source-manifest hash')]:
  mutated=dict(release);mutated[field]=bad;dump(files['release'],mutated)
  refusal('release-'+field,lambda:a.run('R1','open'),needle)
 dump(files['release'],release)
 dump(files['holds'],{'run_id':'run-02','holds':['active']});refusal('active-hold-before-effect',lambda:a.run('R1','open'),'unresolved');dump(files['holds'],{'run_id':'run-02','holds':[]})
 assert not calls
 ops=a.operation_dir(c);ops.mkdir(parents=True,exist_ok=True)
 for status in ('pending','failed','malformed'):
  path=a.receipt_path(c,'run02.duplicate')
  if status=='malformed':path.write_text('{')
  else:dump(path,{'kind':'ask','status':status})
  refusal('duplicate-'+status,lambda:a.invoke(c,'run02.duplicate','ask',['fake'],{'kind':'ask','status':'pending','started_unix':0,'started_monotonic':0}),'duplicate')
  refusal('prior-'+status,lambda:a.prior_uncertainty(c),'disposition');path.unlink()
 assert not calls
 # Known interrupted identity remains recoverable while release is revoked.
 dump(vault,{'enabled':True,'model':'gpt-6.1-sol','turnOverrides':{'effort':'high'},'sandbox':{'type':'readOnly','networkAccess':False},'threadId':'T-known','lastTurnId':None,'inFlightTurnId':'U-unknown'})
 a.freeze_identity(c,'researcher','T-known');revoked=dict(release,authorized=False);dump(files['release'],revoked)
 for action in ('read','resume'):
  assert a.run('R1',action)['classification']=='completed-and-validated';rows.append({'check':'revoked-known-interrupted-'+action,'result':'zero-turn-fake-only'})
 value=a.load(vault);value['threadId']='T-drift';dump(vault,value);refusal('changed-known-role-id',lambda:a.run('R1','read'),'frozen role identity')
 value['threadId']=None;dump(vault,value);refusal('missing-role-id',lambda:a.run('R1','read'),'missing known')
 # Concurrent identical key is retained exactly once for every operation kind.
 for path in ops.glob('*.operation.json'):path.unlink()
 for kind in ('read','ask'):
  outcomes=[]
  def reserve():
   try:a.reserve(c,'run02.same-'+kind,kind,{'kind':kind,'status':'pending'});outcomes.append('reserved')
   except RuntimeError:outcomes.append('refused')
  threads=[threading.Thread(target=reserve) for _ in range(8)]
  for t in threads:t.start()
  for t in threads:t.join()
  assert outcomes.count('reserved')==1,(kind,outcomes);rows.append({'check':'same-key-concurrency-'+kind,'result':outcomes})
 for path in ops.glob('*.operation.json'):path.unlink()
 for number in range(5):a.reserve(c,'run02.cap'+str(number),'ask',{'kind':'ask','status':'pending'})
 refusal('sixth-conservative-attempt',lambda:a.reserve(c,'run02.cap6','ask',{'kind':'ask','status':'pending'}),'cap exhausted')
 assert a.ask_count(c)==5
print(json.dumps({'source_sha256':sha(R/'caretaker/run_operations.py'),'target_model_turns':0,'checks':len(rows),'rows':rows},indent=2))
