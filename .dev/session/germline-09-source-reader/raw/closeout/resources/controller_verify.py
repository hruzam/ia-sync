"""G09 retirement verification only; no turn, resume, archive or delete methods."""
from pathlib import Path
import hashlib,importlib.util,json,os,time
bed=Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader')
res=bed/'raw/closeout/resources';report=res/'07.archival-and-process-verification.json'
if report.exists():raise RuntimeError('Refuse replay/overwrite')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stat(pid):
 p=Path('/proc')/str(pid)
 try:
  raw=(p/'stat').read_text();fields=raw[raw.rfind(')')+2:].split()
  return {'pid':pid,'ppid':int(fields[1]),'session_id':int(fields[3]),'start_ticks':fields[19],'comm':(p/'comm').read_text().strip(),'pid_namespace':os.readlink(p/'ns/pid')}
 except (OSError,IndexError,ValueError):return None
state={'started_unix':time.time(),'status':'pending','target_model_turns':0,'allowed_RPC_methods':['initialize','thread/list','thread/read'],'checker':stat(os.getpid())}
with report.open('x') as f:json.dump(state,f,indent=2)
spec=importlib.util.spec_from_file_location('g09_closeout_transport','/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
t=m.AppServerTransport(codex_bin='/home/hruzam/.local/bin/codex',cwd=str(bed));thread='01a176f7-532b-7722-9324-0ecb92694073'
try:
 t.start();state['owned_app_server']=stat(t.proc.pid)
 try:
  s=m.Session(t,timeout=30);s.initialize()
  kinds=json.loads(Path('/tmp/g09-R1-appserver-schema/v2/ThreadListParams.json').read_text())['definitions']['ThreadSourceKind']['enum']
  queries=[]
  for archived in (True,False):
   params={'cwd':str(bed),'limit':10,'searchTerm':'G09.R1','archived':archived,'sourceKinds':kinds,'useStateDbOnly':True}
   response=s._await_response(t.request('thread/list',params))
   matches=[x for x in response.get('data',[]) if x.get('id')==thread]
   queries.append({'method':'thread/list','params':params,'matching_known_thread':[{'id':x['id'],'cwd':x.get('cwd'),'status':x.get('status')} for x in matches],'next_cursor_present':bool(response.get('nextCursor'))})
  state['archival_queries']=queries
  raw=s.thread_read(thread,include_turns=True);th=raw['thread']
  state['stored_thread']={'id':th['id'],'cwd':th.get('cwd'),'status':th.get('status'),'turns':[{'id':v['id'],'status':v.get('status')} for v in th.get('turns',[])],'response_sha256':hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()}
  assert len(queries[0]['matching_known_thread'])==1 and not queries[1]['matching_known_thread']
  assert all(x['status']!='inProgress' for x in state['stored_thread']['turns'])
 finally:
  t.close();state['owned_app_server_exit']=t.proc.poll();state['owned_app_server_wait_verified']=t.proc.poll() is not None
 ancestors=set();walk=os.getpid()
 while walk and walk not in ancestors:
  ancestors.add(walk);v=stat(walk);walk=v['ppid'] if v else 0
 candidates=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit() or int(p.name) in ancestors:continue
  try:
   if p.stat().st_uid!=os.getuid():continue
   cmd=(p/'cmdline').read_bytes();cwd=os.readlink(p/'cwd');comm=(p/'comm').read_text().strip()
  except OSError:continue
  scoped=str(bed).encode() in cmd or (cwd==str(bed) and ('codex' in comm or 'python' in comm or 'zsh' in comm))
  if scoped:
   row=stat(int(p.name))
   if row:row.update(cwd=cwd,command_sha256=hashlib.sha256(cmd).hexdigest());candidates.append(row)
 state['host_pid_namespace']=os.readlink('/proc/1/ns/pid');state['checker_in_host_pid_namespace']=state['checker']['pid_namespace']==state['host_pid_namespace']
 state['scoped_process_candidates_after_owned_appserver_close']=candidates
 state['historical_R1_runner_currently_visible']=stat(1319728)
 state['process_qualification']='Host-qualified current observation, never a historical death inference. No processes outside creation custody were signalled. Any remaining scoped candidate has unresolved ownership and requires a hold.'
 state['cleanup_holds']=[] if not candidates and state['checker_in_host_pid_namespace'] else ['Process ownership/visibility requires review; no candidate was terminated.']
 state['status']='completed'
except Exception as exc:state['status']='failed';state['error']=repr(exc)
state['ended_unix']=time.time();state['elapsed_seconds']=round(state['ended_unix']-state['started_unix'],3)
tmp=report.with_suffix('.json.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n');os.replace(tmp,report)
print(json.dumps({'status':state['status'],'cleanup_holds':state.get('cleanup_holds'),'error':state.get('error')}))
