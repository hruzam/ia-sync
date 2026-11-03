"""Run the declared fake tests with real subprocess creation disabled."""
import contextlib,hashlib,io,json,runpy,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def blocked(*args,**kwargs):raise AssertionError('REAL SUBPROCESS FORBIDDEN BY INDEPENDENT VERIFIER')
subprocess.run=blocked;subprocess.Popen=blocked
rows=[]
for path in [R/'repair/test_adapter.py',R/'repair/test_tunnel_checkpoints.py']:
 out=io.StringIO();err=io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):runpy.run_path(str(path),run_name='__main__')
 rows.append({'test':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'stdout':json.loads(out.getvalue()),'stderr':err.getvalue()})
print(json.dumps({'target_model_turns':0,'results':rows},indent=2))
