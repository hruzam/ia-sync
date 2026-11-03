"""Independent exact-checker mocked negative cases: immutable byte snapshots, no dispatch."""
import contextlib,copy,hashlib,importlib.util,io,json,os,subprocess,sys
from pathlib import Path
R=Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02');Q=R/'execution/C2-preflight-review';E=Path(__file__).resolve().parent
SOURCE=Q/'check_checkpoint.py'
def digest(data):return hashlib.sha256(data).hexdigest()
assert digest(SOURCE.read_bytes())=='09ec3f47fe871d58ad8b61f7006c1b671e44497d5ec1f276d617ade6813cf4e7'
def guard(event,args):
 if event in ('subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp','socket.connect','socket.bind'):raise AssertionError('EXTERNAL EXECUTION BLOCKED')
sys.addaudithook(guard)
spec=importlib.util.spec_from_file_location('checker46',SOURCE);checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
try:subprocess.run(['FORBIDDEN'])
except RuntimeError as exc:assert 'blocked' in str(exc)
else:raise AssertionError('subprocess unblocked')
a=checker.a
original_bytes=Path.read_bytes;original_text=Path.read_text
# Snapshot all local trial receipts and declared input bytes before mocking. No writes.
base={str(p):original_bytes(p) for p in R.rglob('*') if p.is_file() and E not in p.parents}
for p in json.loads(base[str(R/'hold-line/sources.json')])['files']:base[p['path']]=original_bytes(Path(p['path']))
for p in json.loads(base[str(R/'implementation/I1/MANIFEST.json')])['audited_files']:base[p]=original_bytes(Path(p))
contract=json.loads(base[str(R/'CONTRACT.json')]);plan=json.loads(base[contract['files']['frozen_plan']])
for packet in plan['packets'].values():
 for x in packet['named_inputs']:base[x['path']]=original_bytes(Path(x['path']))
# Explicit preamble source/deployed may be outside the bed.
for p in [contract['preamble']['source'],contract['preamble']['warm']]:base[p]=original_bytes(Path(p))
view={}
def fake_bytes(path):
 key=str(path)
 if key not in view:raise FileNotFoundError(key)
 return view[key]
def fake_text(path,encoding=None,errors=None):return fake_bytes(path).decode(encoding or 'utf-8',errors or 'strict')
Path.read_bytes=fake_bytes;Path.read_text=fake_text
ops=R/'caretaker/operations';askp=str(ops/'run02.A2.ask.operation.json');readp=str(ops/'run02.A2.read.operation.json');vaultp=str(R/'caretaker/tunnel.auditor.state.json')
def get(m,p):return json.loads(m[str(p)])
def put(m,p,v):m[str(p)]=(json.dumps(v,sort_keys=True)+'\n').encode()
def change(m,p,fn):v=get(m,p);fn(v);put(m,p,v)
def evaluate(m):
 global view
 view=m;out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):code=checker.main()
  result=json.loads(out.getvalue());return code,result
 except Exception as exc:return 1,{'status':'CHECK_FAILED','dispatch_ready':False,'error':str(exc)}
# Complete only mocked A2 metadata, while preserving exact ask-before/historical resume.
complete=copy.deepcopy(base);ask=get(complete,askp);s=copy.deepcopy(ask['state_before']);s.update(lastTurnId='U46-completed',inFlightTurnId=None)
turn=s['lastTurnId'];thread=checker.EXPECTED['auditor'];ask.update(status='completed',exit=0,state_after=s)
stdout='/tmp/g09-46-virtual-A2.stdout.json';stderr='/tmp/g09-46-virtual-A2.stderr.txt'
put(complete,stdout,{'thread':{'id':thread,'turns':[{'id':turn,'status':'completed'}]}});complete[stderr]=b''
outputs={k:{'path':p,'sha256':digest(complete[p])} for k,p in [('stdout',stdout),('stderr',stderr)]}
ask['outputs']=copy.deepcopy(outputs);put(complete,askp,ask)
read={'kind':'read','role':'auditor','cycle':'A2','status':'completed','exit':0,'state_before':s,'state_after':s,'outputs':copy.deepcopy(outputs)};put(complete,readp,read);put(complete,vaultp,s)
rows=[]
def test(name,m,expected,needle=None):
 code,result=evaluate(m);assert code==expected,(name,code,result)
 assert result['dispatch_ready'] is False,(name,result)
 if needle:assert needle in result.get('error',''),(name,result)
 rows.append({'case':name,'exit':code,'status':result['status'],'dispatch_ready':result['dispatch_ready'],'error':result.get('error')})
test('fully-matching-mocked-completed-checkpoint-still-no-dispatch',complete,0)
pending=copy.deepcopy(complete);change(pending,askp,lambda v:v.update(status='pending',attempt_number=4));test('pending-A2-never-complete-or-ready',pending,2)
for status in ['failed','unknown','interrupted']:
 m=copy.deepcopy(complete);change(m,askp,lambda v,status=status:v.update(status=status));test(status+'-A2-refused',m,1,'not completed')
for label,path,state_key in [('ask-new-thread',askp,'state_after'),('read-before-thread',readp,'state_before'),('read-after-thread',readp,'state_after')]:
 m=copy.deepcopy(complete);change(m,path,lambda v,k=state_key:v[k].update(threadId='T-wrong'));test(label,m,1,'thread mismatch')
m=copy.deepcopy(complete);change(m,vaultp,lambda v:v.update(threadId='T-wrong'));test('vault-thread-mismatch',m,1,'thread mismatch')
for label,path,state_key in [('ask-new-turn',askp,'state_after'),('read-before-turn',readp,'state_before'),('read-after-turn',readp,'state_after')]:
 m=copy.deepcopy(complete);change(m,path,lambda v,k=state_key:v[k].update(lastTurnId='U-wrong'));test(label,m,1,'identity mismatch')
m=copy.deepcopy(complete);change(m,vaultp,lambda v:v.update(inFlightTurnId='U-pending'));test('completed-vault-still-in-flight',m,1,'identity mismatch')
m=copy.deepcopy(complete);change(m,askp,lambda v:v['state_before'].update(lastTurnId='U-stale'));test('ask-before-not-historical-resume',m,1,'does not follow historical')
m=copy.deepcopy(complete);del m[readp];test('completed-ask-without-read-refused',m,1,'not completed')
def rehash_readback(m,fn):
 v=get(m,stdout);fn(v);put(m,stdout,v)
 for p in (askp,readp):change(m,p,lambda v:v['outputs']['stdout'].update(sha256=digest(m[stdout])))
for label,fn in [('wrong-readback-thread',lambda v:v['thread'].update(id='T-wrong')),('wrong-readback-turn',lambda v:v['thread']['turns'][0].update(id='U-wrong')),('incomplete-readback-turn',lambda v:v['thread']['turns'][0].update(status='inProgress')),('duplicate-readback-turn',lambda v:v['thread']['turns'].append(copy.deepcopy(v['thread']['turns'][0])))]:
 m=copy.deepcopy(complete);rehash_readback(m,fn);test(label,m,1,'readback lacks exact')
m=copy.deepcopy(complete);m[stdout]+=b'corrupt';test('ask-output-hash-mismatch',m,1,'not completed')
product=next(iter(get(complete,R/'implementation/I1/MANIFEST.json')['audited_files']));m=copy.deepcopy(complete);m[product]+=b'changed';test('product-hash-mismatch',m,1,'product manifest hash mismatch')
named=plan['packets']['A2']['named_inputs'][0]['path'];m=copy.deepcopy(complete);m[named]+=b'changed';test('named-input-hash-mismatch',m,1)
m=copy.deepcopy(complete);m[str(R/'implementation/I1/manifest.json')]+=b'changed';test('manifest-alias-mismatch',m,1,'aliases differ')
# Reproduce precisely the old checkpoint error independently from its scripts.
r2resume=get(base,ops/'run02.R2.resume.operation.json')['state_after'];r2ask=get(base,ops/'run02.R2.ask.operation.json')['state_after'];r2read=get(base,ops/'run02.R2.read.operation.json')['state_after']
assert r2resume['lastTurnId']!=r2ask['lastTurnId']==r2read['lastTurnId']
stale_failure=False
try:assert r2resume['lastTurnId']==r2ask['lastTurnId']
except AssertionError:stale_failure=True
assert stale_failure
Path.read_bytes=original_bytes;Path.read_text=original_text
print(json.dumps({'candidate_sha256':digest(original_bytes(SOURCE)),'verdict':'PASS','checks':rows,'test_count':len(rows),'subprocess_blocked':True,'os_external_guard':True,'stale_assertion_reproduced':stale_failure,'R2_historical_resume_turn':r2resume['lastTurnId'],'R2_completed_ask_read_turn':r2ask['lastTurnId'],'production_writes':0,'model_turns':0},indent=2))
