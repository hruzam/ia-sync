"""Offline run-02 adapter tests: fake subprocesses, temporary controls, zero model calls."""
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import threading
from pathlib import Path

SOURCE = Path(__file__).parents[1] / 'caretaker/run_operations.py'
spec = importlib.util.spec_from_file_location('run02_adapter_tested', SOURCE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def fixture(root):
    run = root / 'raw/run-02'
    pre = root / 'pre.md'; pre.write_text('preamble\n')
    packet = run / 'packets/R1.md'; packet.parent.mkdir(parents=True); packet.write_text('G09.run-02.R1\n')
    vault = run / 'caretaker/tunnel.researcher.state.json'
    files = {'release': run / 'control/RELEASE.json', 'holds': run / 'control/HOLD.json',
             'pins': run / 'hold-line/sources.json', 'round_map': run / 'control/ROUND-MAP.json',
             'operations': run / 'caretaker/operations', 'adapter': SOURCE,
             'frozen_plan': run / 'caretaker/plan.C1.json', 'decision': run / 'control/DECISION.01.md',
             'product_contract': run / 'control/CONTRACT.01.json', 'a3_grant': run / 'control/A3.GRANT.json',
             'i1_manifest': run / 'implementation/I1/MANIFEST.json', 'i2_manifest': run / 'implementation/I2/MANIFEST.json'}
    contract = {'schema': 'g09-run02-contract/v1', 'run_id': 'run-02', 'cwd': str(root),
                'target_profile': {'model': 'gpt-6.1-sol', 'effort': 'high'}, 'attempt_budget': {'maximum_target_ask_attempts': 5},
                'timeout_policy': {'TUNNEL_CODEX_TIMEOUT': '1800'},
                'files': {key: str(value) for key, value in files.items()},
                'named_vaults': {'researcher': str(vault), 'auditor': str(run / 'caretaker/tunnel.auditor.state.json')},
                'preamble': {'source': str(pre), 'deployed': str(pre), 'warm': str(pre)},
                'bootstrap_ack': {'required': {'run_id': 'run-02', 'scope': 'G09-source-reader-read-only'},
                                  'sources': {'researcher': ['brief-r', 'acceptance', 'source-map'], 'auditor': ['brief-a', 'acceptance', 'source-map']}},
                'source_scope': {'product_paths': {'directory': '/home/hruzam/ia-sync/zsh/experimental/source-reader/', 'maintainer_file': '/home/hruzam/ia-sync/zsh/experimental/base.zsh', 'maintainer_write_scope': 'one row'}},
                'a3_grant_schema': {'schema': 'g09-a3-grant/v1', 'authority': 'Cartan'},
                'product_manifest_schema': {'schema': 'g09-product-manifest/v1'}}
    dump(run / 'CONTRACT.json', contract)
    dump(files['pins'], {'schema': 'pins/v1', 'run_id': 'run-02', 'files': [{'path': str(packet), 'sha256': digest(packet)}],
                         'preamble': {'source': str(pre), 'deployed': str(pre)}})
    dump(files['holds'], {'schema': 'g09-hold/v1', 'run_id': 'run-02', 'holds': []})
    dump(files['round_map'], {'run_id': 'run-02', 'rounds': [
        {'cycle': 'R1', 'role': 'researcher', 'mode': 'cold', 'packet_template': str(packet),
         'compiled_packet': str(run / 'caretaker/packets/R1.prompt.txt'), 'vault': str(vault)},
        {'cycle': 'A1', 'role': 'auditor', 'mode': 'cold', 'packet_template': str(packet),
         'compiled_packet': str(run / 'caretaker/packets/A1.prompt.txt'), 'vault': contract['named_vaults']['auditor']},
        {'cycle': 'R2', 'role': 'researcher', 'mode': 'warm', 'packet_template': str(packet),
         'compiled_packet': str(run / 'caretaker/packets/R2.prompt.txt'), 'vault': str(vault)},
        {'cycle': 'A2', 'role': 'auditor', 'mode': 'warm', 'packet_template': str(packet),
         'compiled_packet': str(run / 'caretaker/packets/A2.prompt.txt'), 'vault': contract['named_vaults']['auditor']},
        {'cycle': 'A3', 'role': 'auditor', 'mode': 'warm-conditional', 'packet_template': str(packet),
         'compiled_packet': str(run / 'caretaker/packets/A3.prompt.txt'), 'vault': contract['named_vaults']['auditor']}]})
    release = {'run_id': 'run-02', 'authorized': True, 'operator': 'Majkee', 'observed_operator_message': 'fake operator GO',
               'operator_message_reference': 'fake test transcript', 'recorded_at': '2026-10-26T00:00:00Z', 'contract_sha256': digest(run / 'CONTRACT.json'),
               'source_manifest_sha256': digest(files['pins']), 'maximum_target_ask_attempts': 5, 'timeout_seconds': 1800,
               'named_vaults': contract['named_vaults'], 'delegated_enable_vaults': list(contract['named_vaults'].values())}
    dump(files['release'], release)
    return run, files, vault


def expect_error(callback, needle):
    try:
        callback()
    except RuntimeError as exc:
        assert needle in str(exc), exc
    else:
        raise AssertionError(f'expected {needle!r}')


def main():
    checks = []
    original_root, original_run = adapter.B, adapter.R
    original_run_call = adapter.subprocess.run
    with tempfile.TemporaryDirectory(prefix='g09-run02-') as directory:
        root = Path(directory); run, files, vault = fixture(root)
        adapter.B, adapter.R = root, run
        calls = []
        def fake_run(argv, **kwargs):
            calls.append((argv, kwargs))
            state_path = Path(argv[argv.index('--state') + 1])
            current = adapter.load(state_path) or {'enabled': True, 'model': 'gpt-6.1-sol', 'sandbox': {'type': 'readOnly', 'networkAccess': False}, 'turnOverrides': {'effort': 'high'}}
            if argv[1] == 'ask': current.update(threadId='T-researcher', lastTurnId='U-researcher')
            if argv[1] == 'open' and '--enable' in argv: current.update(threadId=None, lastTurnId=None)
            dump(state_path, current)
            return subprocess.CompletedProcess(argv, 0, b'fake stdout', b'fake stderr')
        adapter.subprocess.run = fake_run
        adapter.compile_packets(['R1'], [])
        frozen_packet = run / 'caretaker/packets/R1.prompt.txt'
        frozen_packet.write_text('changed')
        expect_error(lambda: adapter.current_packet(adapter.contract(), adapter.rounds(adapter.contract())['R1']), 'frozen prompt')
        frozen_packet.write_text((run / 'packets/R1.md').read_text())
        checks.append(('changed-frozen-prompt-refused', True))
        named = run / 'named-input.txt'; named.write_text('first')
        plan = adapter.load(files['frozen_plan']); plan['packets']['R1']['named_inputs'] = [{'path': str(named), 'sha256': digest(named)}]; dump(files['frozen_plan'], plan)
        named.write_text('changed')
        expect_error(lambda: adapter.current_packet(adapter.contract(), adapter.rounds(adapter.contract())['R1']), 'named frozen input changed')
        named.write_text('first')
        checks.append(('changed-named-input-refused', True))
        release = adapter.load(files['release']); release['authorized'] = False; dump(files['release'], release)
        expect_error(lambda: adapter.profile('researcher'), 'not authorized')
        checks.append(('profile-requires-release-before-model-list', not calls))
        release['authorized'] = True; dump(files['release'], release)
        expect_error(lambda: adapter.require_profile_receipt(adapter.contract(), 'researcher'), 'lacks validated')
        checks.append(('open-profile-prerequisite-refused', True))
        profile_output = run / 'profile-output.txt'; profile_output.write_text('{}')
        dump(adapter.receipt_path(adapter.contract(), 'run02.researcher.profile'), {'kind': 'profile', 'status': 'completed', 'exit': 0,
            'profile': {'supports_high': True}, 'outputs': {channel: {'path': str(profile_output), 'sha256': digest(profile_output)} for channel in ('stdout', 'stderr')}})
        adapter.run('R1', 'open')
        adapter.run('R1', 'ask')
        identity = adapter.load(adapter.expected_id_path(adapter.contract()))['roles']['researcher']
        checks.append(('cold-open-and-ask-real-invoke-boundary', identity == 'T-researcher' and len(calls) == 2 and calls[0][1]['env']['TUNNEL_CODEX_TIMEOUT'] == '1800'))
        expect_error(lambda: adapter.run('R1', 'ask'), 'cold ask refused')
        checks.append(('cold-replay-refused', True))
        adapter.run('R1', 'read')
        checks.append(('identity-only-read-with-structured-readonly', calls[-1][0][1] == 'read'))
        read_receipt = adapter.load(adapter.receipt_path(adapter.contract(), 'run02.R1.read'))
        acknowledgement = {'run_id': 'run-02', 'role': 'researcher', 'scope': 'G09-source-reader-read-only', 'sources': ['brief-r', 'acceptance', 'source-map']}
        readback = {'thread': {'id': 'T-researcher', 'turns': [{'id': 'U-researcher', 'status': 'completed', 'items': [{'type': 'agentMessage', 'text': 'stale commentary'}, {'type': 'agentMessage', 'text': 'G09.run-02.R1\nBOOTSTRAP ' + json.dumps(acknowledgement, separators=(',', ':'))}]}]}}
        read_output = Path(read_receipt['outputs']['stdout']['path'])
        def set_readback(value):
            read_output.write_text(json.dumps(value))
            read_receipt['outputs']['stdout']['sha256'] = digest(read_output)
            dump(adapter.receipt_path(adapter.contract(), 'run02.R1.read'), read_receipt)
        missing_thread = json.loads(json.dumps(readback)); del missing_thread['thread']['id']
        set_readback(missing_thread)
        expect_error(lambda: adapter.verify_bootstrap('R1'), 'thread identity changed')
        checks.append(('missing-bootstrap-readback-thread-refused', True))
        wrong_thread = json.loads(json.dumps(readback)); wrong_thread['thread']['id'] = 'T-wrong'
        set_readback(wrong_thread)
        expect_error(lambda: adapter.verify_bootstrap('R1'), 'thread identity changed')
        checks.append(('wrong-bootstrap-readback-thread-refused', True))
        set_readback(readback)
        adapter.verify_bootstrap('R1')
        checks.append(('exact-bootstrap-ack-and-readback-validated', True))
        ask_path = adapter.receipt_path(adapter.contract(), 'run02.R1.ask'); saved_ask = ask_path.read_text()
        altered_ask = json.loads(saved_ask); altered_ask['state_after']['lastTurnId'] = 'U-tampered'; dump(ask_path, altered_ask)
        expect_error(lambda: adapter.require_bootstrap_receipt(adapter.contract(), 'researcher'), 'evidence anchor changed')
        ask_path.write_text(saved_ask)
        checks.append(('tampered-bootstrap-anchor-refused', True))
        bound = adapter.load(vault); bound['threadId'] = 'T-wrong'; dump(vault, bound)
        expect_error(lambda: adapter.require_bootstrap_receipt(adapter.contract(), 'researcher', current=adapter.state(vault)), 'current vault thread differs')
        bound['threadId'] = 'T-researcher'; dump(vault, bound)
        checks.append(('changed-bootstrap-vault-thread-refused', True))
        no_identity = adapter.load(vault); no_identity['threadId'] = None; dump(vault, no_identity)
        expect_error(lambda: adapter.run('R1', 'read'), 'missing known thread identity')
        checks.append(('missing-identity-recovery-refused', True))
        no_identity['threadId'] = 'T-researcher'; dump(vault, no_identity)
        expect_error(lambda: adapter.freeze_identity(adapter.contract(), 'auditor', 'T-researcher'), 'cross-role identity collision')
        checks.append(('cross-role-identity-refused', True))
        expect_error(lambda: adapter.freeze_identity(adapter.contract(), 'researcher', 'T-changed'), 'changed identity')
        checks.append(('changed-role-identity-refused', True))
        state = adapter.load(vault); state['lastTurnId'] = None; dump(vault, state)
        expect_error(lambda: adapter.run('R2', 'ask'), 'lacks completed bootstrap')
        checks.append(('warm-requires-completed-bootstrap', True))
        state.update(lastTurnId='U-researcher', preamble=str(root / 'pre.md'), runtime={}); dump(vault, state)
        expect_error(lambda: adapter.run('R2', 'ask'), 'lacks observed model/high/read-only runtime')
        checks.append(('warm-requires-observed-runtime', True))
        dump(files['holds'], {'run_id': 'run-02', 'holds': [{'reason': 'active'}]})
        expect_error(lambda: adapter.run('R1', 'preamble'), 'unresolved')
        checks.append(('active-hold-refused-before-effect', len(calls) == 3))
        dump(files['holds'], {'run_id': 'run-02', 'holds': []})
        release = adapter.load(files['release']); release['authorized'] = False; dump(files['release'], release)
        expect_error(lambda: adapter.run('A1', 'open'), 'not authorized')
        checks.append(('revoked-release-refused-before-effect', len(calls) == 3))
        release['authorized'] = True; dump(files['release'], release)
        pins = adapter.load(files['pins']); pins['files'][0]['sha256'] = '0' * 64; dump(files['pins'], pins)
        expect_error(adapter.readiness, 'pin mismatch')
        checks.append(('changed-pin-refused', True))
        pins['files'][0]['sha256'] = digest(run / 'packets/R1.md'); dump(files['pins'], pins)
        release['source_manifest_sha256'] = digest(files['pins']); dump(files['release'], release)
        c = adapter.contract(); ops = adapter.operation_dir(c); ops.mkdir(parents=True, exist_ok=True)
        for number in range(5): dump(ops / f'cap{number}.operation.json', {'kind': 'ask', 'status': 'completed', 'exit': 0,
            'outputs': {'stdout': {'path': str(run / 'packets/R1.md'), 'sha256': digest(run / 'packets/R1.md')}, 'stderr': {'path': str(run / 'packets/R1.md'), 'sha256': digest(run / 'packets/R1.md')}}})
        expect_error(lambda: adapter.reserve(c, 'run02.cap', 'ask', {'status': 'pending'}), 'cap exhausted')
        checks.append(('exhausted-cap-refused', True))
        for path in ops.glob('*.operation.json'): path.unlink()
        (ops / 'corrupt.operation.json').write_text('{')
        expect_error(lambda: adapter.ask_count(c), 'corrupt receipt')
        checks.append(('corrupt-receipt-count-refused', True))
        (ops / 'corrupt.operation.json').unlink()
        product_path = '/home/hruzam/ia-sync/zsh/experimental/source-reader/reader.py'
        i1 = {'schema': 'g09-product-manifest/v1', 'run_id': 'run-02', 'audited_files': {product_path: '1'}}
        i2 = {'schema': 'g09-product-manifest/v1', 'run_id': 'run-02', 'audited_files': {product_path: '2'}}
        dump(files['i1_manifest'], i1); dump(files['i2_manifest'], i2)
        plan = adapter.load(files['frozen_plan']); plan['packets']['A2'] = {'named_inputs': [{'path': str(files['i1_manifest']), 'sha256': digest(files['i1_manifest'])}]}; dump(files['frozen_plan'], plan)
        grant = {'schema': 'g09-a3-grant/v1', 'run_id': 'run-02', 'authorized': True, 'authority': 'Cartan',
                 'i1_manifest': str(files['i1_manifest']), 'i1_manifest_sha256': digest(files['i1_manifest']),
                 'i2_manifest': str(files['i2_manifest']), 'i2_manifest_sha256': digest(files['i2_manifest']),
                 'i1_hashes': i1['audited_files'], 'i2_hashes': i2['audited_files'], 'audited_changed_paths': [product_path]}
        dump(files['a3_grant'], grant)
        checks.append(('conditional-a3-grant-proof', bool(adapter.require_a3_grant(c))))
        grant['audited_changed_paths'] = [] ; dump(files['a3_grant'], grant)
        expect_error(lambda: adapter.require_a3_grant(c), 'lacks audited')
        checks.append(('conditional-a3-unchanged-refused', True))
        results = []
        def reserve_one(key):
            try: adapter.reserve(c, key, 'ask', {'status': 'pending'}); results.append('reserved')
            except RuntimeError: results.append('refused')
        for number in range(4): dump(ops / f'parallel{number}.operation.json', {'kind': 'ask', 'status': 'completed', 'exit': 0,
            'outputs': {'stdout': {'path': str(run / 'packets/R1.md'), 'sha256': digest(run / 'packets/R1.md')}, 'stderr': {'path': str(run / 'packets/R1.md'), 'sha256': digest(run / 'packets/R1.md')}}})
        threads = [threading.Thread(target=reserve_one, args=(f'parallel-{number}',)) for number in (1, 2)]
        [thread.start() for thread in threads]; [thread.join() for thread in threads]
        checks.append(('concurrent-reservation-never-exceeds-cap', results.count('reserved') == 1 and results.count('refused') == 1))
        for path in ops.glob('*.operation.json'): path.unlink()
        duplicate = []
        def reserve_duplicate():
            try: adapter.reserve(c, 'run02.same-key', 'read', {'status': 'pending'}); duplicate.append('reserved')
            except RuntimeError: duplicate.append('refused')
        threads = [threading.Thread(target=reserve_duplicate) for _ in range(2)]
        [thread.start() for thread in threads]; [thread.join() for thread in threads]
        checks.append(('concurrent-duplicate-key-never-overwrites', duplicate.count('reserved') == 1 and duplicate.count('refused') == 1))
        def failed_run(argv, **kwargs): return subprocess.CompletedProcess(argv, 17, b'', b'failed')
        adapter.subprocess.run = failed_run
        receipt = {'status': 'pending', 'started_unix': 0, 'started_monotonic': 0}
        outcome = adapter.invoke(c, 'run02.command-failed', 'read', ['fake', 'read'], receipt)
        checks.append(('nonzero-command-is-remote-unknown', outcome['classification'] == 'failed' and receipt['remote_outcome'] == 'unknown'))
    adapter.B, adapter.R, adapter.subprocess.run = original_root, original_run, original_run_call
    assert all(value for _, value in checks), (checks, results)
    print(json.dumps({'target_model_turns': 0, 'checks': checks}, indent=2))


if __name__ == '__main__':
    main()
