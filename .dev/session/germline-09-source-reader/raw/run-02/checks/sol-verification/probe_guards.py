"""Independent temporary/fake regression probes. Never invokes a model or shim."""
import importlib.util
import hashlib
import json
import tempfile
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parents[2]
SOURCE = RUN / 'caretaker/run_operations.py'

def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + '\n')

def blocked(*args, **kwargs): raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run = blocked
subprocess.Popen = blocked
adapter = import_file('independent_adapter', SOURCE)
fixtures = import_file('fixture_helpers', RUN/'repair/test_adapter.py')
results = []

def check(name, callback):
    try:
        value = callback()
        results.append({'check': name, 'guarded': value is True, 'detail': value})
    except Exception as exc:
        results.append({'check': name, 'guarded': False, 'exception': repr(exc)})

def expect_refusal(fn):
    try: fn()
    except RuntimeError as exc: return True
    return False

def case(name, callback):
    with tempfile.TemporaryDirectory(prefix='g09-sol-') as directory:
        root = Path(directory)
        run, files, vault = fixtures.fixture(root)
        adapter.B, adapter.R = root, run
        calls = []
        def fake(argv, **kwargs):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 0, b'fake output', b'')
        adapter.subprocess.run = fake
        callback(root, run, files, vault, calls)

def input_change(root, run, files, vault, calls):
    extra=root/'named.txt'; extra.write_text('before')
    adapter.compile_packets(['R1'], [str(extra)])
    extra.write_text('after')
    check('changed-named-input-refused', lambda: expect_refusal(lambda: adapter.current_packet(adapter.contract(), adapter.rounds(adapter.contract())['R1'])))

def grant(root, run, files, vault, calls):
    dump(files['a3_grant'], {'authorized':True,'authority':'Cartan','i1_hashes':{},'i2_hashes':{'nonexistent':'bogus'},'audited_changed_paths':['nonexistent']})
    check('unanchored-a3-proof-refused', lambda: expect_refusal(lambda: adapter.require_a3_grant(adapter.contract())))

def bootstrap(root, run, files, vault, calls):
    dump(vault, {'enabled':True,'model':'gpt-6.1-sol','sandbox':{'type':'readOnly','networkAccess':False},'threadId':'T-test','lastTurnId':'U-test'})
    adapter.freeze_identity(adapter.contract(),'researcher','T-test')
    check('unacknowledged-bootstrap-preamble-refused', lambda: expect_refusal(lambda: adapter.run('R1','preamble')))

for name, callback in [('input',input_change),('a3',grant),('bootstrap',bootstrap)]: case(name,callback)
print(json.dumps({'source_sha256':digest(SOURCE),'target_model_turns':0,'results':results},indent=2))
