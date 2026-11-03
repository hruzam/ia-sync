"""Offline fake-transport checks for durable send/ask identities and timeout diagnostics."""
import importlib.util
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
spec = importlib.util.spec_from_file_location('tunnel_checkpoint_tested', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeTransport:
    def __init__(self):
        self.events, self.request_id, self.closed = [], 0, False

    def start(self): pass
    def close(self): self.closed = True
    def notify(self, *args): pass
    def respond_error(self, *args): pass

    def request(self, method, params):
        self.request_id += 1
        response = {'initialize': {}, 'thread/start': {'thread': {'id': 'T-fake'}, 'model': 'gpt-6.1-sol', 'sandbox': 'read-only'},
                    'turn/start': {'turn': {'id': 'U-fake'}}}.get(method)
        if response is None: raise AssertionError(method)
        self.events.append({'id': self.request_id, 'result': response})
        return self.request_id

    def next_message(self, timeout):
        if self.events: return self.events.pop(0)
        raise module.TransportTimeout('fake quiet queue')


def run(verb):
    original = module.AppServerTransport
    fake = FakeTransport()
    module.AppServerTransport = lambda **kwargs: fake
    with tempfile.TemporaryDirectory(prefix='g09-checkpoint-') as directory:
        state_path = Path(directory) / 'state.json'
        state_path.write_text(json.dumps({'enabled': True, 'threadId': None, 'lastTurnId': None,
                                          'model': 'gpt-6.1-sol', 'sandbox': 'read-only'}) + '\n')
        try:
            getattr(module, f'cmd_{verb}')(SimpleNamespace(state=str(state_path), text='offline fake only'))
        except module.ProtocolError as exc:
            error = str(exc)
        else:
            raise AssertionError('expected timeout')
        state = json.loads(state_path.read_text())
    module.AppServerTransport = original
    assert fake.closed
    assert state['threadId'] == 'T-fake' and state['inFlightTurnId'] == 'U-fake'
    assert state['lastTurnId'] is None
    assert 'phase=turn/completed' in error and 'configured_budget=' in error and 'last_event_age=' in error
    assert 'threadId=T-fake' in error and 'turnId=U-fake' in error
    return {'verb': verb, 'state': state, 'error': error}


if __name__ == '__main__':
    rows = [run('send'), run('ask')]
    print(json.dumps({'target_model_turns': 0, 'checks': len(rows), 'rows': rows}, indent=2))
