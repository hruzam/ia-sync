import sys,os

def guard(event,args):
 if event in ('subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp','socket.connect','socket.bind'):
  raise AssertionError('EXTERNAL EXECUTION FORBIDDEN: '+event)
sys.addaudithook(guard)
"""Independent actual run/invoke/reserve race and recovery probe: fake/temp only."""
import hashlib,importlib.util,json,subprocess,tempfile,threading
from pathlib import Path
from types import ModuleType
REVIEW=Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02/execution/A1-race-review')
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
spec=importlib.util.spec_from_file_location('race_fixture',REVIEW/'test_reservation_race.py');fixture_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture_module)
def load(path):
 obj=ModuleType('independent_'+path.parent.name);obj.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),obj.__dict__);return obj
def one(path):
 a=load(path);events=[];barrier=threading.Event();release=threading.Event();errors={};timeouts=[]
 with tempfile.TemporaryDirectory(prefix='g09-sol39-race-') as directory:
  c,files=fixture_module.fixture(a,Path(directory));original_packet=a.current_packet
  def current_packet(c,item):
   if item['cycle']=='A1':
    barrier.set()
    if not release.wait(3):raise AssertionError('deterministic gate timeout')
   return original_packet(c,item)
  def fake(argv,**kwargs):
   verb=argv[1];events.append({'verb':verb,'vault':argv[-1]})
   if verb=='ask' and 'researcher' in argv[-1]:
    p=Path(argv[-1]);v=a.load(p);v.update(threadId='T-failed',inFlightTurnId='U-unknown');a.write(p,v)
    return subprocess.CompletedProcess(argv,17,b'',b'fake failure')
   return subprocess.CompletedProcess(argv,0,b'fake only',b'')
  a.current_packet=current_packet;a.subprocess.run=fake
  def ask(cycle):
   try:a.run(cycle,'ask')
   except Exception as exc:errors[cycle]=repr(exc)
  stale=threading.Thread(target=ask,args=('A1',));stale.start();assert barrier.wait(3)
  first=threading.Thread(target=ask,args=('R1',));first.start();first.join(3);assert not first.is_alive();release.set();stale.join(3);assert not stale.is_alive()
  asks_before_recovery=[x for x in events if x['verb']=='ask'];second=a.receipt_path(c,'run02.A1.ask').exists()
  receipts={p.name:a.load(p) for p in files['operations'].glob('*.operation.json')}
  # Failed submission and release revocation must not close exact identity-only recovery.
  rel=a.load(files['release']);rel['authorized']=False;a.write(files['release'],rel)
  recovery=[]
  for action in ('read','resume'):
   value=a.run('R1',action);assert value['classification']=='completed-and-validated';recovery.append(action)
  return {'source_sha256':digest(path),'fake_ask_starts':len(asks_before_recovery),'second_receipt_created':second,'errors':errors,'receipt_statuses':{p:v.get('status') for p,v in receipts.items()},'ask_count':a.ask_count(c),'identity_only_recovery_with_failed_prior_and_revoked_release':recovery,'fake_process_events':events}
original=one(REVIEW/'run_operations.frozen.bfa6a3fc.py');candidate=one(Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02/caretaker/run_operations.py'))
assert original['fake_ask_starts']==2 and original['second_receipt_created'] and original['ask_count']==2
assert candidate['fake_ask_starts']==1 and not candidate['second_receipt_created'] and candidate['ask_count']==1
assert 'earlier submission requires head disposition' in candidate['errors']['A1']
print(json.dumps({'original':original,'applied':candidate,'target_model_turns':0,'verdict':'PASS'},indent=2))
