"""Offline staged proof for the A1 uncertainty/reservation race; no real subprocesses."""
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import threading
from pathlib import Path
from types import ModuleType

SOURCE = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02/caretaker/run_operations.py')
PATCH = Path(__file__).with_name('reserve-prior-uncertainty.patch')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def load_variant(candidate):
    text = SOURCE.read_text()
    needle = "        try:\n            if destination.exists():\n"
    replacement = "        try:\n            prior_uncertainty(c)\n            if destination.exists():\n"
    assert text.count(needle) == 1
    if candidate:
        assert PATCH.read_text().count('+            prior_uncertainty(c)') == 1
        text = text.replace(needle, replacement)
    module = ModuleType('run02_candidate' if candidate else 'run02_original')
    module.__file__ = str(SOURCE)
    exec(compile(text, str(SOURCE), 'exec'), module.__dict__)
    return module


def fixture(module, root):
    run = root / 'raw/run-02'; packet = run / 'packets/R1.md'; packet.parent.mkdir(parents=True)
    packet.write_text('offline packet\n')
    pre = root / 'pre.md'; pre.write_text('pre\n')
    files = {'release': run / 'control/RELEASE.json', 'holds': run / 'control/HOLD.json',
             'pins': run / 'hold-line/sources.json', 'round_map': run / 'control/ROUND-MAP.json',
             'operations': run / 'caretaker/operations', 'frozen_plan': run / 'caretaker/plan.C1.json',
             'adapter': SOURCE, 'decision': run / 'control/DECISION.01.md',
             'product_contract': run / 'control/CONTRACT.01.json', 'a3_grant': run / 'control/A3.GRANT.json',
             'i1_manifest': run / 'implementation/I1/MANIFEST.json', 'i2_manifest': run / 'implementation/I2/MANIFEST.json'}
    vaults = {'researcher': run / 'caretaker/tunnel.researcher.state.json', 'auditor': run / 'caretaker/tunnel.auditor.state.json'}
    contract = {'schema': 'g09-run02-contract/v1', 'run_id': 'run-02', 'cwd': str(root),
                'target_profile': {'model': 'gpt-6.1-sol', 'effort': 'high'}, 'attempt_budget': {'maximum_target_ask_attempts': 5},
                'timeout_policy': {'TUNNEL_CODEX_TIMEOUT': '1800'}, 'files': {key: str(value) for key, value in files.items()},
                'named_vaults': {key: str(value) for key, value in vaults.items()}, 'preamble': {'source': str(pre), 'warm': str(pre)}}
    dump(run / 'CONTRACT.json', contract)
    dump(files['pins'], {'run_id': 'run-02', 'files': [{'path': str(packet), 'sha256': digest(packet)}], 'preamble': {'source': str(pre), 'deployed': str(pre)}})
    dump(files['holds'], {'run_id': 'run-02', 'holds': []})
    rounds = []
    for cycle, role in (('R1', 'researcher'), ('A1', 'auditor')):
        rounds.append({'cycle': cycle, 'role': role, 'mode': 'cold', 'packet_template': str(packet),
                       'compiled_packet': str(run / f'caretaker/packets/{cycle}.prompt.txt'), 'vault': str(vaults[role])})
        target = Path(rounds[-1]['compiled_packet']); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(packet.read_text())
    dump(files['round_map'], {'run_id': 'run-02', 'rounds': rounds})
    dump(files['frozen_plan'], {'contract_sha256': digest(run / 'CONTRACT.json'), 'pins': {'pins': str(files['pins']), 'sha256': digest(files['pins'])},
                                'packets': {item['cycle']: {'path': item['compiled_packet'], 'sha256': digest(item['compiled_packet']), 'template_sha256': digest(packet), 'named_inputs': []} for item in rounds}})
    release = {'run_id': 'run-02', 'authorized': True, 'operator': 'Majkee', 'observed_operator_message': 'fake GO', 'operator_message_reference': 'fake', 'recorded_at': '2026-10-27T00:00:00+01:00',
               'contract_sha256': digest(run / 'CONTRACT.json'), 'source_manifest_sha256': digest(files['pins']), 'maximum_target_ask_attempts': 5, 'timeout_seconds': 1800,
               'named_vaults': contract['named_vaults'], 'delegated_enable_vaults': list(contract['named_vaults'].values())}
    dump(files['release'], release)
    for vault in vaults.values(): dump(vault, {'enabled': True, 'model': 'gpt-6.1-sol', 'sandbox': 'read-only', 'threadId': None, 'lastTurnId': None, 'preamble': None, 'turnOverrides': {'effort': 'high'}})
    module.B, module.R = root, run
    return contract, files


def race(candidate):
    module = load_variant(candidate)
    original_popen, original_run, original_packet = module.subprocess.Popen, module.subprocess.run, module.current_packet
    with tempfile.TemporaryDirectory(prefix='g09-race-') as directory:
        contract, files = fixture(module, Path(directory)); starts, errors = [], {}
        release_a1, a1_waiting = threading.Event(), threading.Event()
        def packet_gate(c, item):
            if item['cycle'] == 'A1':
                a1_waiting.set(); release_a1.wait(timeout=2)
            return original_packet(c, item)
        def fake_run(argv, **kwargs):
            starts.append(argv[1])
            return subprocess.CompletedProcess(argv, 17 if argv[1] == 'ask' and 'researcher' in argv[-1] else 0, b'', b'fake')
        module.current_packet, module.subprocess.run = packet_gate, fake_run
        module.subprocess.Popen = lambda *a, **k: (_ for _ in ()).throw(AssertionError('Popen forbidden'))
        def call(cycle):
            try: module.run(cycle, 'ask')
            except RuntimeError as exc: errors[cycle] = str(exc)
        a1 = threading.Thread(target=call, args=('A1',)); a1.start(); assert a1_waiting.wait(timeout=2)
        r1 = threading.Thread(target=call, args=('R1',)); r1.start(); r1.join(timeout=2); release_a1.set(); a1.join(timeout=2)
        module.subprocess.Popen, module.subprocess.run, module.current_packet = original_popen, original_run, original_packet
        operations = sorted(path.name for path in files['operations'].glob('*.operation.json'))
    return {'candidate': candidate, 'fake_subprocess_starts': starts, 'errors': errors, 'operations': operations,
            'a1_dispatched': starts.count('ask') == 2, 'a1_receipt_created': 'run02.A1.ask.operation.json' in operations}


def cap_checks():
    module = load_variant(False)
    with tempfile.TemporaryDirectory(prefix='g09-cap-') as directory:
        contract, files = fixture(module, Path(directory)); c = module.contract()
        for number in range(5): module.reserve(c, f'run02.cap{number}', 'ask', {'kind': 'ask', 'status': 'pending'})
        kinds = [module.load(path).get('kind') for path in files['operations'].glob('*.operation.json')]
        try: module.reserve(c, 'run02.cap6', 'ask', {'kind': 'ask', 'status': 'pending'})
        except RuntimeError as exc: sixth = str(exc)
        else: raise AssertionError('sixth kind:ask reservation unexpectedly succeeded')
    return {'five_kinds': kinds, 'sixth_refusal': sixth}


def concurrent_cap_check():
    module = load_variant(False)
    with tempfile.TemporaryDirectory(prefix='g09-concurrent-cap-') as directory:
        contract, files = fixture(module, Path(directory)); c = module.contract()
        for number in range(4): module.reserve(c, f'run02.concurrent{number}', 'ask', {'kind': 'ask', 'status': 'pending'})
        barrier, results = threading.Barrier(2), []
        def reserve_one(number):
            barrier.wait()
            try:
                module.reserve(c, f'run02.concurrent-extra{number}', 'ask', {'kind': 'ask', 'status': 'pending'})
                results.append('reserved')
            except RuntimeError as exc:
                results.append(f'refused:{exc}')
        workers = [threading.Thread(target=reserve_one, args=(number,)) for number in (1, 2)]
        [worker.start() for worker in workers]; [worker.join(timeout=2) for worker in workers]
        receipts = [module.load(path) for path in files['operations'].glob('*.operation.json')]
    return {'outcomes': results, 'ask_receipts': len(receipts), 'all_kind_ask': all(value.get('kind') == 'ask' for value in receipts)}


if __name__ == '__main__':
    original, candidate, cap, concurrent = race(False), race(True), cap_checks(), concurrent_cap_check()
    assert original['a1_dispatched'] and original['a1_receipt_created']
    assert not candidate['a1_dispatched'] and not candidate['a1_receipt_created']
    assert cap['five_kinds'] == ['ask'] * 5 and 'cap exhausted' in cap['sixth_refusal']
    assert concurrent['outcomes'].count('reserved') == 1 and len(concurrent['outcomes']) == 2
    assert concurrent['ask_receipts'] == 5 and concurrent['all_kind_ask']
    print(json.dumps({'source_sha256': digest(SOURCE), 'patch_sha256': digest(PATCH), 'target_model_turns': 0,
                      'original': original, 'candidate': candidate, 'cap': cap, 'concurrent_cap': concurrent}, indent=2, sort_keys=True))
