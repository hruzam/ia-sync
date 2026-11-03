"""Zero-model-turn capability check; retains no account/auth payload."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
BIN = '/home/hruzam/.local/bin/codex'
spec = importlib.util.spec_from_file_location('trial_transport', '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
transport_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport_module)
os.environ['TUNNEL_CODEX_BIN'] = BIN
transport = transport_module.AppServerTransport(codex_bin=BIN, cwd=str(HERE.parents[1]))
transport.start()
try:
    session = transport_module.Session(transport)
    session.initialize()
    models = session.model_list()
    selected = [m for m in models.get('data', []) if m.get('id') == 'gpt-6.1-sol']
    fields = ('id', 'model', 'defaultReasoningEffort', 'supportedReasoningEfforts')
    record = {'binary': BIN, 'version': subprocess.check_output([BIN, '--version'], text=True).strip(),
              'selected': [{k: m.get(k) for k in fields} for m in selected], 'target_turns': 0}
finally:
    transport.close()
with (HERE / 'profile-capability.json').open('x') as handle:
    json.dump(record, handle, indent=2)
    handle.write('\n')
print(json.dumps(record))
