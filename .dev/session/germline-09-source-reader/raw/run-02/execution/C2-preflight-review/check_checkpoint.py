#!/usr/bin/env python3
"""Read-only C2 metadata/packet checkpoint. PENDING is never dispatch readiness."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
def blocked(*args, **kwargs):
    raise RuntimeError('subprocess execution is blocked')
subprocess.Popen = subprocess.run = subprocess.call = subprocess.check_call = subprocess.check_output = blocked
os.system = os.popen = blocked
R = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/raw/run-02')
CA = R / 'caretaker'
spec = importlib.util.spec_from_file_location('g09_adapter_readonly', CA / 'run_operations.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
EXPECTED = {'researcher': '01a17a86-873c-72b0-8787-932736a0f7d9',
            'auditor': '01a17a89-cc0a-7053-b9b2-e5bdac784fe4'}
def req(condition, message):
    if not condition:
        raise RuntimeError(message)
def receipt(cycle, kind):
    path = CA / 'operations' / f'run02.{cycle}.{kind}.operation.json'
    return path, a.load(path)
def validated(path, value):
    req(value is not None and a.inspect_receipt(path)['classification'] == 'completed-and-validated', f'{path.name} not completed and hash validated')
def runtime(s, role):
    req(s and s.get('threadId') == EXPECTED[role], f'{role} thread mismatch')
    rt = s.get('runtime') or {}
    req(s.get('model') == 'gpt-6.1-sol' and (s.get('turnOverrides') or {}).get('effort') == 'high' and a.sandbox_ok(s.get('sandbox')), f'{role} profile mismatch')
    req(rt.get('model') == 'gpt-6.1-sol' and rt.get('reasoningEffort') == 'high' and a.sandbox_ok(rt.get('sandbox')) and rt.get('approvalPolicy') == 'never' and rt.get('cwd') == str(R.parents[1]), f'{role} observed runtime mismatch')
def main():
    c = a.contract(); rounds = a.rounds(c)
    req((a.load(CA / 'identities.json') or {}).get('roles') == EXPECTED, 'role identity anchors differ')
    manifest_path = R / 'implementation/I1/MANIFEST.json'
    manifest = a.load(manifest_path) or {}
    audited = manifest.get('audited_files') or {}
    req(len(audited) == 24 and all(a.sha(path) == digest for path, digest in audited.items()), 'product manifest hash mismatch')
    req(manifest_path.read_bytes() == (R / 'implementation/I1/manifest.json').read_bytes(), 'product manifest aliases differ')
    packets = {}
    for cycle in ('R2','A2'):
        packet = a.current_packet(c, rounds[cycle])
        req(packet.get('named_inputs'), f'{cycle} has no named inputs')
        packets[cycle] = {'sha256': packet['sha256'], 'named_inputs_checked': len(packet['named_inputs'])}
    result = {'product_hashes_checked': len(audited), 'manifest_aliases_equal': True, 'packets': packets, 'roles': {}, 'dispatch_ready': False, 'subprocess_blocked': True}
    for cycle, role in [('R2','researcher'), ('A2','auditor')]:
        vault = a.state(CA / f'tunnel.{role}.state.json'); runtime(vault, role)
        a.require_bootstrap_receipt(c, role, current=vault)
        rp, resume = receipt(cycle, 'resume'); validated(rp, resume)
        historical = resume.get('state_after') or {}; runtime(historical, role)
        req(resume.get('kind') == 'resume' and resume.get('role') == role and not historical.get('inFlightTurnId'), f'{cycle} historical resume invalid')
        ap, ask = receipt(cycle, 'ask'); req(ask and ask.get('kind') == 'ask' and ask.get('role') == role, f'{cycle} ask missing/wrong role')
        runtime(ask.get('state_before'), role)
        req((ask['state_before'].get('lastTurnId')) == historical.get('lastTurnId'), f'{cycle} ask does not follow historical resume')
        info = {'threadId': EXPECTED[role], 'historical_resume_turn': historical.get('lastTurnId'), 'ask_attempt': ask.get('attempt_number')}
        if ask.get('status') == 'pending':
            req(cycle == 'A2' and ask.get('attempt_number') == 4, 'unexpected pending ask')
            info.update({'outcome': 'PENDING_OR_UNKNOWN', 'in_flight_turn': vault.get('inFlightTurnId'), 'completed_identity': False})
        else:
            validated(ap, ask)
            readpath, read = receipt(cycle, 'read'); validated(readpath, read)
            req(read.get('kind') == 'read' and read.get('role') == role, f'{cycle} read wrong role')
            states = [ask.get('state_after'), read.get('state_before'), read.get('state_after'), vault]
            for s in states: runtime(s, role)
            turn = (states[0] or {}).get('lastTurnId')
            req(turn and all(s.get('lastTurnId') == turn and not s.get('inFlightTurnId') for s in states), f'{cycle} completed ask/read/vault identity mismatch')
            output = read['outputs']['stdout']
            readback = json.loads(Path(output['path']).read_text())
            thread = readback.get('thread') or {}
            matches = [t for t in thread.get('turns', []) if t.get('id') == turn]
            req(thread.get('id') == EXPECTED[role] and len(matches) == 1 and matches[0].get('status') == 'completed', f'{cycle} readback lacks exact completed thread/turn')
            info.update({'outcome':'COMPLETED_READBACK', 'completed_turn':turn, 'completed_identity':True, 'historical_equals_current': historical.get('lastTurnId') == turn})
        result['roles'][cycle] = info
    result['status'] = 'PENDING_OR_UNKNOWN' if not result['roles']['A2']['completed_identity'] else 'COMPLETED_IDENTITIES_OBSERVED'
    result['note'] = 'Metadata and packet check only; no authorization or dispatch readiness inferred.'
    print(json.dumps(result, indent=2)); return 2 if result['status'] == 'PENDING_OR_UNKNOWN' else 0
if __name__ == '__main__':
    try: sys.exit(main())
    except Exception as exc:
        print(json.dumps({'status':'CHECK_FAILED', 'dispatch_ready':False, 'error':str(exc)}, indent=2)); sys.exit(1)
