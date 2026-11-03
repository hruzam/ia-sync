"""Execute the staged candidate regression suite in a temporary production layout."""
import contextlib,hashlib,io,json,runpy,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
with tempfile.TemporaryDirectory(prefix='g09-sol39-suite-') as directory:
 root=Path(directory)/'raw/run-02';source=root/'caretaker/run_operations.py';test=root/'repair/test_adapter.py'
 for destination,origin in ((source,R/'candidate/run_operations.py'),(test,R/'candidate/test_adapter.py')):
  destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(origin.read_bytes())
 out,err=io.StringIO(),io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):runpy.run_path(str(test),run_name='__main__')
 result=json.loads(out.getvalue());assert len(result['checks'])>=27 and all(v for _,v in result['checks'])
 print(json.dumps({'candidate_sha256':sha(source),'candidate_test_sha256':sha(test),'suite':result,'stderr':err.getvalue(),'target_model_turns':0,'verdict':'PASS'},indent=2))
