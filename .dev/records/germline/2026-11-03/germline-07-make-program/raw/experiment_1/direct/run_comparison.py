#!/usr/bin/env python3
"""Two explicitly authorized comparison turns; never repeats an invocation."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

BED = Path('/home/hruzam/ia-sync/.dev/session/germline-07-make-program')
HOME_DIR = BED / 'raw/experiment_1/direct'
CARETAKER = BED / 'raw/experiment_1/caretaker'
SHIM = '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_peer(peer):
    operation = HOME_DIR / (peer + '.operation.json')
    if operation.exists():
        raise RuntimeError('Refusing to repeat operation: ' + str(operation))
    state_path = CARETAKER / ('tunnel.' + peer + '.state.json')
    state_before = json.loads(state_path.read_text())
    initial = json.loads((CARETAKER / (peer + '.ask.receipt.json')).read_text())
    if initial['exit'] != 0 or state_before['threadId'] != initial['state']['threadId']:
        raise RuntimeError('Unverified target identity: ' + peer)
    if state_before['runtime']['sandbox'].get('type') != 'readOnly':
        raise RuntimeError('Effective read-only sandbox not established: ' + peer)
    text = (CARETAKER / ('prompt.' + peer + '.txt')).read_text()
    old = 'experiment_1.' + peer + '.initial'
    new = 'experiment_1.' + peer + '.direct'
    if text.count(old) != 1:
        raise RuntimeError('Unexpected initial marker: ' + peer)
    text = text.replace(old, new)
    text += ('\nClarification: read-only file-inspection commands such as rg, sed and cat are '
             'permitted for the named sources. Do not execute the inspected code/examples or '
             'launch any additional agent, model CLI, daemon, or service.\n')
    prompt_path = HOME_DIR / (peer + '.prompt.txt')
    prompt_path.write_text(text)
    stdout_path = HOME_DIR / (peer + '.stdout.txt')
    stderr_path = HOME_DIR / (peer + '.stderr.txt')
    argv = [SHIM, 'ask', '--state', str(state_path), text]
    record = {'peer': peer, 'status': 'pending', 'argv': argv,
              'prompt': {'path': str(prompt_path), 'sha256': digest(prompt_path)},
              'state_before': state_before, 'started_unix': time.time()}
    with operation.open('x') as handle:
        json.dump(record, handle, indent=2)
    result = subprocess.run(argv, cwd=BED,
                            env=dict(os.environ, TUNNEL_CODEX_USAGE='full'),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_path.write_text(result.stdout)
    stderr_path.write_text(result.stderr)
    record.update(status='completed', ended_unix=time.time(), exit=result.returncode,
                  stdout={'path': str(stdout_path), 'sha256': digest(stdout_path)},
                  stderr={'path': str(stderr_path), 'sha256': digest(stderr_path)},
                  state_after=json.loads(state_path.read_text()))
    record['elapsed_seconds'] = round(record['ended_unix'] - record['started_unix'], 3)
    operation.write_text(json.dumps(record, indent=2) + '\n')
    return {'peer': peer, 'exit': result.returncode,
            'elapsed_seconds': record['elapsed_seconds'],
            'thread_id': record['state_after']['threadId'],
            'turn_id': record['state_after']['lastTurnId'],
            'stdout_path': str(stdout_path), 'result': result.stdout}

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        for record in pool.map(run_peer, ['peer-a', 'peer-b']):
            print(json.dumps(record, ensure_ascii=False), flush=True)
