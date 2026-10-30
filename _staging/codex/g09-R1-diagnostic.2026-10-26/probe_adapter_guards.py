"""Pure guard probes; no real dispatch, release/vault edit or transport call."""
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/caretaker/run_operations.py')
spec = importlib.util.spec_from_file_location('adapter_under_probe', SOURCE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

def rejection(path, require_turn=False, preamble=None):
    try:
        adapter.check_state(path, require_turn, preamble)
    except RuntimeError as error:
        return str(error)
    return None

def main():
    with tempfile.TemporaryDirectory(prefix='g09-guard-probe-') as directory:
        root = Path(directory)
        state = root / 'state.json'
        state.write_text(json.dumps({'model': 'gpt-6.1-sol',
            'sandbox': {'type': 'readOnly', 'networkAccess': False},
            'runtime': {'model': 'gpt-6.1-sol', 'sandbox': {'type': 'readOnly', 'networkAccess': False}},
            'threadId': 'T-offline', 'lastTurnId': 'U-offline'}))
        structured = rejection(state, True)
        assert structured and 'profile mismatch' in structured
        state.write_text(json.dumps({'model': 'gpt-6.1-sol', 'sandbox': 'read-only',
                                    'threadId': 'T-recovered', 'lastTurnId': None,
                                    'preamble': adapter.PRE}))
        identity_only = rejection(state, True, adapter.PRE)
        assert identity_only and 'lacks completed first turn' in identity_only
        packet = root / 'R1.prompt.txt'
        packet.write_text('offline packet; never sent')
        observed = []
        adapter.PKT = root
        adapter.pins = lambda: observed.append('pins') or {'release_ok': False, 'all_pinned_files_match': False}
        adapter.check_state = lambda *args: {'threadId': None, 'lastTurnId': None}
        adapter.invoke = lambda *args, **kwargs: observed.append('invoke-stub') or {'classification': 'failed'}
        adapter.run('R1', 'ask')
        assert observed == ['invoke-stub']
        record = {'kind': 'offline adapter integration guards', 'target_model_turns': 0,
                  'structured_readonly_state_rejected': structured,
                  'identity_only_read_resume_guard_rejected': identity_only,
                  'dispatch_stub_reached_without_pin_release_recheck': True,
                  'calls_observed': observed,
                  'scope': 'Pure functions and stubbed invocation only; actual G09 files untouched.'}
    with (HERE / 'adapter-guard-probes.json').open('x') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    print(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
