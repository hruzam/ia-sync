"""Parent's independent zero-target-turn reconciliation; persist selected fields only."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / 'live'
SHIM = '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh'
ENV = dict(os.environ, TUNNEL_CODEX_BIN='/home/hruzam/.local/bin/codex')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def call(verb, state):
    argv = [SHIM, verb, '--state', str(state)]
    start = time.monotonic()
    run = subprocess.run(argv, cwd=ROOT.parents[1], env=ENV, capture_output=True)
    return run, {'argv': argv, 'exit': run.returncode,
                 'elapsed_seconds': round(time.monotonic() - start, 3),
                 'stdout_sha256': sha(run.stdout), 'stderr_sha256': sha(run.stderr),
                 'stderr': run.stderr.decode(errors='replace')}

def verify():
    target = ROOT / 'verification.json'
    if target.exists():
        raise RuntimeError('Refusing to overwrite prior verification evidence')
    contract = json.loads((ROOT / 'contract.json').read_text())
    hashes = [{'path': row['path'], 'matches': sha(Path(row['path']).read_bytes()) == row['sha256']}
              for row in contract['files']]
    if not all(row['matches'] for row in hashes):
        raise RuntimeError('Frozen trial input drift; no protocol operation performed')
    rows = []
    for peer in ('peer-a', 'peer-b'):
        state_path = LIVE / f'tunnel.{peer}.state.json'
        before = json.loads(state_path.read_text())
        if not before.get('threadId'):
            raise RuntimeError('No known thread to read; no resend: ' + peer)
        resume, resume_record = call('resume', state_path)
        state = json.loads(state_path.read_text())
        read, read_record = call('read', state_path)
        record = {'peer': peer, 'resume': resume_record, 'read': read_record,
                  'runtime': state.get('runtime'), 'state_thread_id': state.get('threadId'),
                  'state_last_turn_id': state.get('lastTurnId'),
                  'identity_unchanged': before.get('threadId') == state.get('threadId')}
        if read.returncode == 0:
            thread = json.loads(read.stdout)['thread']
            turns = thread.get('turns', [])
            latest = turns[-1] if turns else {}
            items = latest.get('items', [])
            replies = [i.get('text', '') for i in items if i.get('type') == 'agentMessage']
            reply = replies[-1] if replies else ''
            stdout_path = LIVE / f'{peer}.ask.stdout.txt'
            output = stdout_path.read_text()
            stored, separator, usage_tail = output.rpartition('\n[usage: ')
            if not separator:
                stored, usage = output.rstrip('\n'), None
            else:
                usage = json.loads(usage_tail.strip().removesuffix(']'))
            commands = [i for i in items if i.get('type') == 'commandExecution']
            task_source = ('/home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md' if peer == 'peer-a'
                           else '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
            task_commands = [i for i in commands if task_source in i.get('command', '')]
            record.update(thread_id=thread.get('id'), turn_count=len(turns),
                          turn_id=latest.get('id'), turn_status=latest.get('status'),
                          agent_reply=reply, reply_sha256=sha(reply.encode()),
                          stored_stdout_sha256=sha(stdout_path.read_bytes()),
                          exact_reply_match=reply == stored,
                          marker_matches=reply.startswith(f'experiment_2.{peer}.low\n'),
                          final_word_count=len(reply.split()), usage=usage,
                          item_types=dict(Counter(i.get('type') for i in items)),
                          command_count=len(commands), task_source_command_count=len(task_commands),
                          task_commands=[{'command': i.get('command'), 'exitCode': i.get('exitCode'),
                                          'output_lines': len((i.get('aggregatedOutput') or '').splitlines())}
                                         for i in task_commands])
        rows.append(record)
    ids = [row.get('thread_id') for row in rows]
    old_ids = ['01a1694a-7bdd-7d70-913d-d3dcef66c8ac', '01a1694b-0c61-76f0-897c-fc3c66f665c0']
    result = {'experiment': 'experiment_2', 'verified_by': 'Cartan', 'source_hashes': hashes,
              'rows': rows, 'distinct_new_ids': bool(all(ids) and len(set(ids)) == 2 and not set(ids) & set(old_ids)),
              'additional_target_turns': 0, 'whole_route_usage': 'unavailable'}
    with target.open('x') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'distinct_new_ids': result['distinct_new_ids'], 'rows': [
        {k: row.get(k) for k in ('peer', 'resume', 'runtime', 'turn_count', 'turn_status',
                                  'exact_reply_match', 'marker_matches', 'final_word_count',
                                  'task_source_command_count')} for row in rows]}, indent=2))

if __name__ == '__main__':
    verify()
