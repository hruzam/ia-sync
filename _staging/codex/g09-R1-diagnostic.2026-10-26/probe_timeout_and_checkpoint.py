"""Real shim logic with fake clock/transport; test candidate identity checkpoint offline."""
import contextlib
import copy
import difflib
import hashlib
import io
import json
from pathlib import Path
import queue
from types import ModuleType, SimpleNamespace

HERE = Path(__file__).resolve().parent
SOURCE = Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
BASE = SOURCE.read_text()
NEEDLE = '            thread_id = _birth_or_resume(session, state)\n'
REPLACEMENT = (NEEDLE + '            # Preserve birth identity for read-only recovery if the first turn fails.\n'
               '            # lastTurnId remains unchanged until successful completion/reconciliation.\n'
               '            save_state(args.state, state)\n')
assert BASE.count(NEEDLE) == 2
CANDIDATE = BASE.replace(NEEDLE, REPLACEMENT)

class Clock:
    value = 0.0
    def time(self):
        return self.value

def run_probe(text, verb, failure_phase):
    module = ModuleType('offline_shim_probe')
    module.__file__ = str(SOURCE)
    exec(compile(text, str(SOURCE), 'exec'), module.__dict__)
    real_transport = module.AppServerTransport
    real_session = module.Session
    clock = Clock()
    module.time = clock
    durable = {'enabled': True, 'threadId': None, 'lastTurnId': None, 'model': 'gpt-6.1-sol',
               'sandbox': 'read-only', 'turnOverrides': {'effort': 'high'}}
    memory = copy.deepcopy(durable)
    saves = []
    released = []

    class FakeQueue:
        def __init__(self):
            self.events = []
        def get(self, timeout):
            event = self.events.pop(0)
            if event == 'progress':
                clock.value += 115.87593173980713
                return json.dumps({'method': 'item/started', 'params': {}})
            if event == 'timeout':
                clock.value += timeout
                raise queue.Empty()
            return json.dumps(event)

    class FakeTransport:
        def __init__(self):
            self._out_q = FakeQueue()
            self.next_id = 0
            self.closed = False
        def start(self):
            pass
        def close(self):
            self.closed = True
        def _stderr_tail(self):
            return ''
        def notify(self, *args):
            pass
        def respond_error(self, *args):
            raise AssertionError('No server requests in this probe')
        def next_message(self, timeout):
            return real_transport.next_message(self, timeout)
        def request(self, method, params):
            self.next_id += 1
            rid = self.next_id
            if method == 'initialize':
                response = {}
            elif method == 'thread/start':
                response = {'thread': {'id': 'T-offline'}, 'model': 'gpt-6.1-sol',
                            'sandbox': {'type': 'readOnly', 'networkAccess': False}}
            elif method == 'turn/start':
                if failure_phase == 'turn-start-ack':
                    self._out_q.events += ['progress', 'timeout']
                    return rid
                response = {'turn': {'id': 'U-offline'}}
            elif method == 'thread/read':
                assert failure_phase == 'reconcile-ack'
                self._out_q.events += ['progress', 'timeout']
                return rid
            else:
                raise AssertionError(method)
            self._out_q.events.append({'id': rid, 'result': response})
            if method == 'turn/start':
                if failure_phase == 'turn-completed':
                    self._out_q.events += ['progress', 'timeout']
                else:
                    self._out_q.events.append({'method': 'turn/completed', 'params': {
                        'threadId': 'T-offline', 'turn': {'id': 'U-offline', 'status': 'completed'}}})
            return rid

    transport = FakeTransport()
    module.AppServerTransport = lambda **kwargs: transport
    module.Session = lambda t: real_session(t, timeout=120.0)
    module._require_state = lambda args: memory
    module._acquire_turn_lock = lambda path: 'offline-lock'
    module._release_turn_lock = lambda lock: released.append(lock)
    def save(path, value):
        durable.clear()
        durable.update(copy.deepcopy(value))
        saves.append(copy.deepcopy(value))
    module.save_state = save
    error = None
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            getattr(module, 'cmd_' + verb)(SimpleNamespace(state='/not-written', text='offline task'))
        except module.ProtocolError as exc:
            error = str(exc)
    assert error and '4.124068260192871s' in error
    assert clock.value == 120.0 and transport.closed and released
    return {'verb': verb, 'failure_phase': failure_phase, 'error': error,
            'elapsed_fake_seconds': clock.value, 'memory_thread_id': memory['threadId'],
            'durable_thread_id': durable['threadId'], 'durable_last_turn_id': durable['lastTurnId'],
            'save_calls': len(saves), 'transport_closed': transport.closed,
            'lock_released': bool(released)}

def main():
    results = []
    for variant, text in [('original', BASE), ('candidate-not-applied', CANDIDATE)]:
        for verb in ('ask', 'send'):
            for phase in ('turn-start-ack', 'turn-completed', 'reconcile-ack'):
                row = run_probe(text, verb, phase)
                row['variant'] = variant
                assert row['durable_thread_id'] == (None if variant == 'original' else 'T-offline')
                assert row['durable_last_turn_id'] is None
                results.append(row)
    diff = ''.join(difflib.unified_diff(BASE.splitlines(True), CANDIDATE.splitlines(True),
                                        fromfile='a/zsh/ai/tunnel-codex.py', tofile='b/zsh/ai/tunnel-codex.py'))
    with (HERE / 'identity-checkpoint.candidate.patch').open('x') as handle:
        handle.write(diff)
    record = {'source_sha256': hashlib.sha256(BASE.encode()).hexdigest(),
              'source_unchanged': SOURCE.read_text() == BASE,
              'app_server_processes': 0, 'target_model_turns': 0,
              'checks_passed': len(results), 'results': results,
              'candidate_limit': 'Preserves known thread identity only; no completed result is fabricated. Does not fix deadline policy, phase diagnostics, or adapter guards.'}
    with (HERE / 'offline-checkpoint-probes.json').open('x') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    print(json.dumps({k: record[k] for k in ('source_unchanged', 'app_server_processes', 'target_model_turns', 'checks_passed', 'candidate_limit')}))

if __name__ == '__main__':
    main()
