"""Read-only C1 plan validator: frozen adapter pure helpers, subprocess creation blocked."""
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parents[3]
SOURCE = RUN / 'caretaker/run_operations.py'


def blocked(*args, **kwargs):
    raise AssertionError('subprocess creation is forbidden in C1 plan validation')


subprocess.run = blocked
subprocess.Popen = blocked
spec = importlib.util.spec_from_file_location('g09_run02_adapter', SOURCE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
adapter.subprocess.run = blocked
adapter.subprocess.Popen = blocked

c = adapter.contract()
mapped = adapter.rounds(c)
validated = {cycle: adapter.current_packet(c, mapped[cycle]) for cycle in ('R1', 'A1')}
report = {
    'schema': 'g09-run02-c1-pure-validation/v1',
    'subprocess_blocked': True,
    'target_model_turns': 0,
    'adapter': {'path': str(SOURCE), 'sha256': adapter.sha(SOURCE)},
    'contract_sha256': adapter.sha(RUN / 'CONTRACT.json'),
    'pins': adapter.verify_pins(c),
    'plan': {'path': c['files']['frozen_plan'], 'sha256': adapter.sha(c['files']['frozen_plan'])},
    'packets': validated,
}
print(json.dumps(report, indent=2, sort_keys=True))
