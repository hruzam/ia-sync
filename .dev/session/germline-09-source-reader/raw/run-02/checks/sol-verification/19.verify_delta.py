"""Cycle19 exact-thread delta verification; real subprocess creation remains disabled."""
import contextlib,hashlib,importlib.util,io,json,runpy,subprocess,tempfile
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[1]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
def imp(name,path):
 s=importlib.util.spec_from_file_location(name,path);o=importlib.util.module_from_spec(s);s.loader.exec_module(o);return o
def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value)+'\n')
a=imp('cycle19_adapter',R/'caretaker/run_operations.py');f=imp('cycle19_fixture',R/'repair/test_adapter.py')
expected={'adapter':'bfa6a3fc7c09591881575c87fb8ad5bde066188cc42f814028dbeffff4d77b50','test':'d81a8e51340b2069c50c4fc10dcf4a099946374dc5fd50dbb28503b2e2063023','contract':'84be154eb074088af75f003cd760b0ccb904061afb46851135e8ad4203f1d214','pins':'d72e6b552f7e05e2e5c5657631526b989dea28d2cc3a372919845a1c86ad51db'}
paths={'adapter':R/'caretaker/run_operations.py','test':R/'repair/test_adapter.py','contract':R/'CONTRACT.json','pins':R/'hold-line/sources.json'}
actual={name:sha(path) for name,path in paths.items()};assert actual==expected,actual
old=(R/'checks/frozen-09/run_operations.py').read_bytes();new=paths['adapter'].read_bytes()
assert new==old.replace(b"if thread.get('id') not in (None, thread_id):",b"if thread.get('id') != thread_id:")
rows=[]
for mode in ('missing','wrong','exact'):
 with tempfile.TemporaryDirectory(prefix='g09-cycle19-') as directory:
  root=Path(directory);run,files,vault=f.fixture(root);a.B,a.R=root,run;c=a.contract()
  state={'threadId':'T-exact','lastTurnId':'U-exact'}
  ack=dict(c['bootstrap_ack']['required'],role='researcher',sources=c['bootstrap_ack']['sources']['researcher'])
  text='G09.run-02.R1\nBOOTSTRAP '+json.dumps(ack)+'\nSubstantive answer'
  def receipt(key,text):
   path=a.receipt_path(c,key);out=path.parent/(key+'.stdout');err=path.parent/(key+'.stderr');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text);err.write_text('')
   dump(path,{'kind':key.split('.')[-1],'status':'completed','exit':0,'state_after':state,'outputs':{channel:{'path':str(p),'sha256':sha(p)} for channel,p in [('stdout',out),('stderr',err)]}})
  receipt('run02.R1.ask',text)
  thread={'turns':[{'id':'U-exact','status':'completed','items':[{'type':'agentMessage','text':'commentary'},{'type':'agentMessage','text':text}]}]}
  if mode!='missing':thread['id']='T-exact' if mode=='exact' else 'T-wrong'
  receipt('run02.R1.read',json.dumps({'thread':thread}))
  try:result=a.verify_bootstrap('R1');accepted=True
  except RuntimeError as exc:result=str(exc);accepted=False
  assert accepted==(mode=='exact'),(mode,result)
  if not accepted:assert 'thread identity changed' in result
  rows.append({'case':mode,'accepted':accepted,'result':result})
out,err=io.StringIO(),io.StringIO()
with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):runpy.run_path(str(paths['test']),run_name='__main__')
declared=json.loads(out.getvalue());assert len(declared['checks'])==27 and all(v for _,v in declared['checks'])
tunnel=Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py');assert sha(tunnel)=='e72b072103d3d32e2c26cc11770834bfa331daa84ecc3e0add7b1d56cc2cdf65'
c=json.loads(paths['contract'].read_text());assert c['trial_bus_cycles']=={'C1':'30','I1':'31','C2':'32','I2':'33','C3':'34'}
rounds=json.loads((R/'control/ROUND-MAP.json').read_text())['rounds'];assert {v['cycle']:v['native_bus_cycle'] for v in rounds}=={'R1':'30','A1':'30','R2':'32','A2':'32','A3':'34'}
print(json.dumps({'verdict':'PASS','source_hashes':actual,'source_delta':'exactly one comparison: missing thread.id now refused','independent_cases':rows,'declared_test':declared,'declared_stderr':err.getvalue(),'unchanged_tunnel_sha256':sha(tunnel),'reuse':'Cycle09 transport/boundary/profile/A3 evidence retained. Adapter bytes outside exact verified equality change unchanged.','trial_cycles':c['trial_bus_cycles'],'target_model_turns':0},indent=2))
