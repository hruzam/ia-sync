"""Bounded, zero-model-turn metadata/read probe for the single failed G09 R1 attempt."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time

BED = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader')
HERE = Path(__file__).resolve().parent
REPORT = HERE / 'identity-recovery.json'
BIN = '/home/hruzam/.local/bin/codex'
RECEIPT = BED / 'raw/caretaker/operations/R1.ask.operation.json'
VAULT = BED / 'raw/caretaker/tunnel.researcher.state.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def user_text(item):
    parts = item.get('content') or []
    return '\n'.join(x.get('text', '') for x in parts if isinstance(x, dict) and x.get('type') == 'text')

def main():
    if REPORT.exists():
        raise RuntimeError('Refusing to overwrite a prior recovery observation')
    receipt = json.loads(RECEIPT.read_text())
    expected = Path(receipt['prompt']['path']).read_text()
    before = {'receipt_sha256': digest(RECEIPT.read_bytes()), 'vault_sha256': digest(VAULT.read_bytes())}
    spec = importlib.util.spec_from_file_location('diagnostic_transport', '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    schema = json.loads(Path('/tmp/g09-R1-appserver-schema/v2/ThreadListParams.json').read_text())
    kinds = schema['definitions']['ThreadSourceKind']['enum']
    transport = module.AppServerTransport(codex_bin=BIN, cwd=str(BED))
    report = {'kind': 'bounded protocol metadata recovery', 'target_model_turns': 0,
              'forbidden_methods': ['thread/start', 'thread/resume', 'turn/start', 'turn/steer'],
              'evidence_before': before, 'queries': [], 'candidates': [], 'reads': []}
    transport.start()
    try:
        session = module.Session(transport, timeout=30)
        session.initialize()
        candidates = {}
        for search in ('G09.R1', None):
            params = {'cwd': str(BED), 'limit': 10, 'sortKey': 'created_at',
                      'sortDirection': 'desc', 'sourceKinds': kinds, 'useStateDbOnly': True,
                      'archived': False}
            if search:
                params['searchTerm'] = search
            request = transport.request('thread/list', params)
            start = time.monotonic()
            result = session._await_response(request)
            accepted = []
            for thread in result.get('data', []):
                created = thread.get('createdAt', 0)
                in_window = isinstance(created, (int, float)) and receipt['started_unix'] - 10 <= created <= receipt['ended_unix'] + 10
                exact_cwd = thread.get('cwd') == str(BED)
                marker = 'G09.R1' in (thread.get('preview') or '')
                if exact_cwd and in_window:
                    selected = {k: thread.get(k) for k in ('id', 'createdAt', 'updatedAt', 'cwd', 'source', 'status', 'modelProvider')}
                    selected['preview_has_expected_marker'] = marker
                    candidates[thread['id']] = selected
                    accepted.append(thread['id'])
            report['queries'].append({'method': 'thread/list', 'params': params,
                                      'elapsed_seconds': round(time.monotonic() - start, 3),
                                      'returned_count': len(result.get('data', [])),
                                      'next_cursor_present': bool(result.get('nextCursor')),
                                      'accepted_ids': accepted})
            if candidates:
                break
        report['candidates'] = list(candidates.values())
        if len(candidates) > 3:
            report['hold'] = 'Too many candidates; no history read or selection performed'
        else:
            for identity in candidates:
                raw = session.thread_read(identity, include_turns=True)
                thread = raw.get('thread') or {}
                turns = []
                for turn in thread.get('turns', []):
                    items = turn.get('items') or []
                    users = [user_text(item) for item in items if item.get('type') == 'userMessage']
                    messages = [item for item in items if item.get('type') == 'agentMessage']
                    commands = [item for item in items if item.get('type') == 'commandExecution']
                    selected = {'id': turn.get('id'), 'status': turn.get('status'),
                                'item_types': dict(Counter(item.get('type') for item in items)),
                                'exact_prompt_match': expected in users,
                                'user_text_hashes': [digest(x.encode()) for x in users],
                                'expected_prompt_sha256': digest(expected.encode()),
                                'error': turn.get('error'),
                                'command_metadata': [{k: item.get(k) for k in ('status', 'exitCode', 'durationMs')} | {'command_sha256': digest((item.get('command') or '').encode())} for item in commands],
                                'agent_messages': [{'phase': item.get('phase'), 'bytes': len((item.get('text') or '').encode()),
                                                    'sha256': digest((item.get('text') or '').encode()),
                                                    'has_expected_marker': (item.get('text') or '').startswith('G09.R1')}
                                                   for item in messages]}
                    replies = [item.get('text') or '' for item in messages if item.get('phase') == 'final_answer']
                    selected['completed_final_response_present'] = turn.get('status') == 'completed' and bool(replies)
                    if selected['exact_prompt_match'] and replies:
                        reply = replies[-1]
                        selected['selected_task_reply'] = reply if len(reply) <= 16000 else None
                        selected['selected_task_reply_bytes'] = len(reply.encode())
                    elif selected['exact_prompt_match']:
                        commentary = [item.get('text') or '' for item in messages if (item.get('text') or '').startswith('G09.R1')]
                        if commentary:
                            selected['marker_bearing_commentary'] = commentary[-1]
                            selected['marker_bearing_commentary_bytes'] = len(commentary[-1].encode())
                    turns.append(selected)
                report['reads'].append({'method': 'thread/read', 'thread_id': identity,
                                        'thread_status': thread.get('status'), 'turn_count': len(turns),
                                        'turns': turns, 'read_response_canonical_json_sha256': digest(json.dumps(raw, sort_keys=True).encode())})
    except Exception as error:
        report['error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        transport.close()
    report['evidence_after'] = {'receipt_sha256': digest(RECEIPT.read_bytes()), 'vault_sha256': digest(VAULT.read_bytes())}
    report['original_evidence_unchanged'] = report['evidence_after'] == before
    matches = [(read['thread_id'], turn['id'], turn['status']) for read in report['reads']
               for turn in read['turns'] if turn['exact_prompt_match']]
    report['exact_prompt_matches'] = matches
    with REPORT.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'queries': report['queries'], 'candidates': report['candidates'],
                      'exact_prompt_matches': matches, 'error': report.get('error'),
                      'original_evidence_unchanged': report['original_evidence_unchanged']}, indent=2))

if __name__ == '__main__':
    main()
