#!/usr/bin/env bash
# Offline task-card intake: never reads credentials or sends a provider request.
set -euo pipefail
if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo 'Usage: bash prepare-task.sh CASE.json [hlm|agent]' >&2
  exit 2
fi
task_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python3 -B - "$task_dir" "$1" "${2:-}" <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

task_dir = Path(sys.argv[1])
repo = task_dir.parents[3]
sys.path.insert(0, str(repo / 'zsh/jev'))
import kernel

source = Path(sys.argv[2]).resolve(strict=True)
requester = sys.argv[3]
if requester not in ('', 'hlm', 'agent'):
    raise ValueError('requester must be hlm or agent when supplied')
packet = kernel.load(source)
kernel.validate_packet(packet)
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
run = Path(tempfile.mkdtemp(prefix='jev-task-'))
project = run / 'project'
bed = project / 'offline-bed'
bed.mkdir(parents=True)
base = [sys.executable, '-B', str(repo / 'zsh/jev/jev.py'), '--root', str(run / 'vault')]
if requester:
    base += ['--requester', requester]

def invoke(arguments):
    result = subprocess.run([*base, *arguments], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return json.loads(result.stdout)

try:
    opened = invoke(['open', '--project', str(project), '--bed', str(bed)])
    packet['session_id'] = opened['session_id']
    packet['channel'] = 'main'
    bound = run / 'bound-case.json'
    bound.write_bytes(kernel.canonical(packet) + b'\n')
    base += ['--session', opened['session_id'], '--channel', 'main']
    prepared = invoke(['prepare', str(bound)])
    request = prepared['request_id']
    result = {
        'schema': 'jev.offline-task-result/v1',
        'status': 'PREPARED_OFFLINE',
        'source_card': str(source), 'source_sha256': source_hash,
        'binding_note': 'Only session_id/channel rebound to a disposable main-stream session.',
        'run_directory': str(run), 'bound_case': str(bound),
        'request_id': request, 'reference': invoke(['ref', request]),
        'settings': invoke(['settings']),
        'history': invoke(['show', '--request', request]),
        'provider_calls': 0, 'judgment': None,
    }
    result_path = run / 'result.json'
    result_path.write_text(json.dumps(result, indent=2) + '\n')
    result_path.chmod(0o600)
    print(result_path)
except Exception:
    print('Offline run evidence retained at: ' + str(run), file=sys.stderr)
    raise
PY
