import sys,os

def guard(event,args):
 if event in ('subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp','socket.connect','socket.bind'):
  raise AssertionError('EXTERNAL EXECUTION FORBIDDEN: '+event)
sys.addaudithook(guard)
"""Execute the staged candidate regression suite in a temporary production layout."""
import contextlib,hashlib,io,json,runpy,subprocess,tempfile
from pathlib import Path
R=Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
with tempfile.TemporaryDirectory(prefix='g09-sol39-suite-') as directory:
 root=Path(directory)/'raw/run-02';source=root/'caretaker/run_operations.py';test=root/'repair/test_adapter.py'
 for destination,origin in ((source,R/'caretaker/run_operations.py'),(test,R/'repair/test_adapter.py')):
  destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(origin.read_bytes())
 out,err=io.StringIO(),io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):runpy.run_path(str(test),run_name='__main__')
 result=json.loads(out.getvalue());assert len(result['checks'])==28 and all(v for _,v in result['checks'])
 print(json.dumps({'applied_sha256':sha(source),'applied_test_sha256':sha(test),'suite':result,'stderr':err.getvalue(),'target_model_turns':0,'verdict':'PASS'},indent=2))
