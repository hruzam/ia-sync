"""Independent bootstrap/profile/A3 checks, using temp receipts and fake JSON-RPC only."""
import hashlib,importlib.util,json,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def imp(name,path):
 s=importlib.util.spec_from_file_location(name,path);o=importlib.util.module_from_spec(s);s.loader.exec_module(o);return o
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
a=imp('sol_bootstrap',R/'caretaker/run_operations.py');f=imp('sol_bootstrap_fixture',R/'repair/test_adapter.py')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value)+'\n')
def setup(root):
 run,files,vault=f.fixture(root);a.B,a.R=root,run;c=a.contract();c['target_profile']['effort']='high';dump(run/'CONTRACT.json',c)
 release=a.load(files['release']);release['contract_sha256']=sha(run/'CONTRACT.json');dump(files['release'],release)
 return run,files,vault,c
def receipt(c,key,text,after=None):
 path=a.receipt_path(c,key);out=path.parent/(key+'.stdout');err=path.parent/(key+'.stderr');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text);err.write_text('')
 value={'kind':key.split('.')[-1],'status':'completed','exit':0,'state_after':after,'outputs':{channel:{'path':str(p),'sha256':sha(p)} for channel,p in [('stdout',out),('stderr',err)]}};dump(path,value);return path
rows=[]
for mode in ('valid-multiple-messages','wrong-role','wrong-thread','interrupted','missing-marker','anchor-tamper'):
 with tempfile.TemporaryDirectory(prefix='g09-sol-ack-') as directory:
  run,files,vault,c=setup(Path(directory));state={'enabled':True,'threadId':'T-ack','lastTurnId':'U-ack','model':'gpt-6.1-sol','turnOverrides':{'effort':'high'},'sandbox':{'type':'readOnly','networkAccess':False}}
  ack=dict(c['bootstrap_ack']['required'],role='researcher',sources=c['bootstrap_ack']['sources']['researcher'])
  if mode=='wrong-role':ack['role']='auditor'
  final=('bad' if mode=='missing-marker' else 'G09.run-02.R1')+'\nBOOTSTRAP '+json.dumps(ack)+'\nSubstantive answer'
  ask=receipt(c,'run02.R1.ask',final,state)
  readback={'thread':{'id':'T-other' if mode=='wrong-thread' else 'T-ack','turns':[{'id':'U-ack','status':'interrupted' if mode=='interrupted' else 'completed','items':[{'type':'agentMessage','text':'initial commentary'},{'type':'agentMessage','text':final}]}]}}
  receipt(c,'run02.R1.read',json.dumps(readback),state)
  if mode in ('valid-multiple-messages','anchor-tamper'):
   assert a.verify_bootstrap('R1')['classification']=='completed-and-validated';a.require_bootstrap_receipt(c,'researcher',state)
   if mode=='valid-multiple-messages':
    dump(vault,state);a.freeze_identity(c,'researcher','T-ack');a.compile_packets(['R2'],[])
    def fake(argv,**kwargs):
     current=a.load(vault)
     if argv[1]=='open':current.update(preamble=c['preamble']['warm'],runtime={'model':'gpt-6.1-sol','reasoningEffort':'high','sandbox':{'type':'readOnly','networkAccess':False}})
     if argv[1]=='ask':current['lastTurnId']='U-warm'
     dump(vault,current);return subprocess.CompletedProcess(argv,0,b'fake answer',b'')
    a.subprocess.run=fake
    assert a.run('R1','preamble')['classification']=='completed-and-validated'
    assert a.run('R2','ask')['classification']=='completed-and-validated'
    rows.append({'check':'validated-bootstrap-preamble-and-warm-real-run-fake-only','pass':True})
   if mode=='anchor-tamper':
    value=json.loads(ask.read_text());value['extra']='modified';dump(ask,value)
    try:a.require_bootstrap_receipt(c,'researcher',state)
    except RuntimeError as exc:assert 'anchor changed' in str(exc)
    else:raise AssertionError('anchor tamper accepted')
  else:
   try:a.verify_bootstrap('R1')
   except RuntimeError as exc:pass
   else:raise AssertionError(mode+' accepted')
  rows.append({'check':'bootstrap-'+mode,'pass':True})
# Exercise real profile() and Session initialize/model_list with a fake transport.
original_spec=importlib.util.spec_from_file_location
transports=[]
class FakeTransport:
 def __init__(self,**kwargs):self.counter=0;self.events=[];self.closed=False;transports.append(self)
 def start(self):pass
 def close(self):self.closed=True
 def notify(self,*args):pass
 def request(self,method,params):
  assert method in ('initialize','model/list'),method
  self.counter+=1;value={} if method=='initialize' else {'data':[{'id':'gpt-6.1-sol','supportedReasoningEfforts':[{'reasoningEffort':'high'}]}]};self.events.append({'id':self.counter,'result':value});return self.counter
 def next_message(self,timeout):assert timeout<=1800;return self.events.pop(0)
def profile_spec(name,path,*args,**kwargs):
 spec=original_spec(name,path,*args,**kwargs)
 if name=='run02_tunnel_profile':
  loader=spec.loader
  class Proxy:
   def create_module(self,spec):return None
   def exec_module(self,module):loader.exec_module(module);module.AppServerTransport=FakeTransport
  spec.loader=Proxy()
 return spec
importlib.util.spec_from_file_location=profile_spec
with tempfile.TemporaryDirectory(prefix='g09-sol-profile-') as directory:
 run,files,vault,c=setup(Path(directory));result=a.profile('researcher');assert result['classification']=='completed-and-validated' and transports[-1].closed
 assert a.load(a.receipt_path(c,'run02.researcher.profile'))['profile']['selected'][0]['id']=='gpt-6.1-sol'
 try:a.profile('researcher')
 except RuntimeError:pass
 else:raise AssertionError('second profile attempt accepted')
 assert len(transports)==1;rows.append({'check':'real-profile-fake-session-selected-high-one-attempt-cleanup','pass':True})
importlib.util.spec_from_file_location=original_spec
with tempfile.TemporaryDirectory(prefix='g09-sol-a3-') as directory:
 run,files,vault,c=setup(Path(directory));base='/home/hruzam/ia-sync/zsh/experimental/base.zsh'
 c['source_scope']['product_paths']={'directory':'/home/hruzam/ia-sync/zsh/experimental/source-reader/','maintainer_file':base};dump(run/'CONTRACT.json',c)
 before={base:hashlib.sha256(b'before').hexdigest()};after={base:hashlib.sha256(b'after').hexdigest()}
 for path,stage,values in [(files['i1_manifest'],'I1',before),(files['i2_manifest'],'I2',after)]:dump(path,{'schema':'g09-product-manifest/v1','run_id':'run-02','stage':stage,'audited_files':values})
 dump(files['frozen_plan'],{'packets':{'A2':{'named_inputs':[{'path':str(files['i1_manifest']),'sha256':sha(files['i1_manifest'])}]}}})
 grant={'schema':'g09-a3-grant/v1','run_id':'run-02','authorized':True,'authority':'Cartan','i1_manifest':str(files['i1_manifest']),'i1_manifest_sha256':sha(files['i1_manifest']),'i2_manifest':str(files['i2_manifest']),'i2_manifest_sha256':sha(files['i2_manifest']),'i1_hashes':before,'i2_hashes':after,'audited_changed_paths':[base]};dump(files['a3_grant'],grant)
 assert a.require_a3_grant(c);rows.append({'check':'exact-granted-maintainer-file-a3-accepted','pass':True})
 grant['i2_hashes']={base:'bogus'};dump(files['a3_grant'],grant)
 try:a.require_a3_grant(c)
 except RuntimeError as exc:assert 'bind exact' in str(exc)
 else:raise AssertionError('invented map accepted')
 rows.append({'check':'a3-invented-map-refused','pass':True})
print(json.dumps({'source_sha256':sha(R/'caretaker/run_operations.py'),'target_model_turns':0,'checks':len(rows),'rows':rows},indent=2))
