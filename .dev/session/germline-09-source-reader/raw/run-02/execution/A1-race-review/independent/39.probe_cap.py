"""Independent candidate cap checks: valid kind:ask receipts with truthful outcomes."""
import hashlib,importlib.util,json,subprocess,tempfile,threading
from pathlib import Path
from types import ModuleType
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
s=importlib.util.spec_from_file_location('cap_fixture',R/'test_reservation_race.py');fixture=importlib.util.module_from_spec(s);s.loader.exec_module(fixture)
a=ModuleType('cap_candidate');a.__file__=str(R/'candidate/run_operations.py');exec(compile(Path(a.__file__).read_bytes(),a.__file__,'exec'),a.__dict__)
rows=[]
def completed(path,c):
 output=Path(c['files']['operations'])/'valid-output.txt';output.parent.mkdir(parents=True,exist_ok=True);output.write_text('valid fake completed output')
 a.write(path,{'kind':'ask','status':'completed','exit':0,'outputs':{channel:{'path':str(output),'sha256':sha(output)} for channel in ('stdout','stderr')}})
with tempfile.TemporaryDirectory(prefix='g09-sol39-sequential-') as directory:
 c,files=fixture.fixture(a,Path(directory))
 for number in range(5):
  path=a.reserve(c,'sequential-'+str(number),'ask',{'kind':'ask','status':'pending'});completed(path,c)
  assert a.ask_count(c)==number+1
 try:a.reserve(c,'sequential-sixth','ask',{'kind':'ask','status':'pending'})
 except RuntimeError as exc:assert str(exc)=='target ask cap exhausted';refusal=str(exc)
 else:raise AssertionError('sixth reservation accepted')
 assert not a.receipt_path(c,'sequential-sixth').exists()
 rows.append({'case':'sequential-five-valid-completed-asks-sixth-cap-branch','ask_count':a.ask_count(c),'refusal':refusal})
with tempfile.TemporaryDirectory(prefix='g09-sol39-concurrent-') as directory:
 c,files=fixture.fixture(a,Path(directory))
 for number in range(4):completed(a.reserve(c,'initial-'+str(number),'ask',{'kind':'ask','status':'pending'}),c)
 barrier=threading.Barrier(2);outcomes=[]
 def reserve_one(number):
  barrier.wait(timeout=3)
  try:
   p=a.reserve(c,'concurrent-'+str(number),'ask',{'kind':'ask','status':'pending'});completed(p,c);outcomes.append({'outcome':'reserved'})
  except RuntimeError as exc:outcomes.append({'outcome':'refused','reason':str(exc)})
 workers=[threading.Thread(target=reserve_one,args=(n,)) for n in (1,2)]
 for t in workers:t.start()
 for t in workers:t.join(timeout=3);assert not t.is_alive()
 assert sum(x['outcome']=='reserved' for x in outcomes)==1 and len(outcomes)==2
 assert a.ask_count(c)==5
 values=[a.load(p) for p in files['operations'].glob('*.operation.json')];assert len(values)==5 and all(x.get('kind')=='ask' for x in values)
 rows.append({'case':'concurrent-at-four','outcomes':outcomes,'ask_count':5,'all_receipts_kind_ask':True,'note':'Concurrent refusal may be lock, prior pending uncertainty, or cap; sequential check separately proves cap branch.'})
print(json.dumps({'candidate_sha256':sha(R/'candidate/run_operations.py'),'checks':rows,'target_model_turns':0,'verdict':'PASS'},indent=2))
