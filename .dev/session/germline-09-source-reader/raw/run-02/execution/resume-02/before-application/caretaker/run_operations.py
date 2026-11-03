#!/usr/bin/env python3
"""Run-02 receipt-first caretaker adapter.  Effects stay closed until a fresh GO."""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

B = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader')
R = B / 'raw/run-02'
SHIM = '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh'
CODEX = '/home/hruzam/.local/bin/codex'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pstart(pid):
    try:
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    except (FileNotFoundError, IndexError, OSError):
        return None


def load(path):
    try:
        value = json.loads(Path(path).read_text())
        return value if isinstance(value, dict) else None
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f'{path.name}.tmp-{os.getpid()}')
    with temporary.open('w') as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def contract():
    value = load(R / 'CONTRACT.json')
    if not value or value.get('schema') != 'g09-run02-contract/v1' or value.get('run_id') != 'run-02':
        raise RuntimeError('missing or invalid run-02 CONTRACT.json')
    return value


def paths():
    c = contract()
    return c, {name: Path(value) for name, value in c['files'].items()}


def rounds(c):
    value = load(c['files']['round_map'])
    if not value or value.get('run_id') != 'run-02':
        raise RuntimeError('missing or invalid run-02 ROUND-MAP.json')
    return {item['cycle']: item for item in value.get('rounds', [])}


def sandbox_ok(value):
    if value == 'read-only':
        return True
    return isinstance(value, dict) and value.get('type') == 'readOnly' and value.get('networkAccess') is False


def state(path):
    value = load(path)
    if value is None:
        return None
    return {key: value.get(key) for key in ('enabled', 'threadId', 'lastTurnId', 'inFlightTurnId', 'model', 'sandbox', 'cwd', 'preamble', 'turnOverrides', 'runtime')}


def verify_pins(c):
    value = load(c['files']['pins'])
    if not value or value.get('run_id') not in (None, 'run-02'):
        raise RuntimeError('missing or invalid run-02 sources pins')
    bad = []
    for item in value.get('files', []):
        try:
            actual = sha(item['path'])
        except OSError:
            actual = None
        if actual != item.get('sha256'):
            bad.append({'path': item.get('path'), 'expected': item.get('sha256'), 'actual': actual})
    pre = value.get('preamble') or {}
    expected_preamble = {'source': c['preamble'].get('source'), 'deployed': c['preamble'].get('warm')}
    for key, expected in expected_preamble.items():
        if pre.get(key) != expected:
            bad.append({'preamble': key, 'expected': expected, 'actual': pre.get(key)})
    if pre.get('source') and pre.get('deployed'):
        try:
            if sha(pre['source']) != sha(pre['deployed']):
                bad.append({'preamble': 'source/deployed', 'expected': sha(pre['source']), 'actual': sha(pre['deployed'])})
        except OSError:
            bad.append({'preamble': 'source/deployed', 'actual': None})
    if bad:
        raise RuntimeError(f'current pin mismatch: {json.dumps(bad, sort_keys=True)}')
    return {'pins': str(c['files']['pins']), 'sha256': sha(c['files']['pins'])}


def require_no_holds(c):
    hold = load(c['files']['holds'])
    if not hold or hold.get('run_id') != 'run-02' or hold.get('holds'):
        raise RuntimeError('unresolved or invalid run-02 HOLD.json')


def require_release(c, action, role):
    release = load(c['files']['release'])
    if not release or release.get('run_id') != 'run-02' or release.get('authorized') is not True:
        raise RuntimeError('fresh run-02 release is not authorized')
    if release.get('operator') != 'Majkee' or not isinstance(release.get('observed_operator_message'), str) or not release['observed_operator_message'].strip() or not isinstance(release.get('operator_message_reference'), str) or not release['operator_message_reference'].strip() or not isinstance(release.get('recorded_at'), str) or not release['recorded_at'].strip():
        raise RuntimeError('release lacks fresh operator message provenance')
    if release.get('contract_sha256') != sha(R / 'CONTRACT.json'):
        raise RuntimeError('release contract hash mismatch')
    if release.get('source_manifest_sha256') != sha(c['files']['pins']):
        raise RuntimeError('release source-manifest hash mismatch')
    if release.get('maximum_target_ask_attempts') != c['attempt_budget']['maximum_target_ask_attempts']:
        raise RuntimeError('release ask cap mismatch')
    if release.get('timeout_seconds') != int(c['timeout_policy']['TUNNEL_CODEX_TIMEOUT']):
        raise RuntimeError('release timeout mismatch')
    if release.get('named_vaults') != c['named_vaults']:
        raise RuntimeError('release vault map mismatch')
    if action == 'open' and c['named_vaults'][role] not in (release.get('delegated_enable_vaults') or []):
        raise RuntimeError(f'release does not delegate enable for {role}')
    return {'release': str(c['files']['release']), 'contract_sha256': release['contract_sha256']}


def operation_dir(c):
    return Path(c['files']['operations'])


def receipt_path(c, key):
    return operation_dir(c) / f'{key}.operation.json'


def inspect_receipt(path):
    value = load(path)
    if value is None:
        return {'classification': 'unknown', 'reason': 'missing-or-malformed-receipt'}
    if value.get('status') == 'pending':
        return {'classification': 'unknown', 'reason': 'pending-submission'}
    if value.get('status') == 'failed':
        return {'classification': 'failed', 'reason': 'command-failed-or-remote-outcome-unknown'}
    if value.get('status') != 'completed' or value.get('exit') != 0:
        return {'classification': 'unknown', 'reason': 'invalid-completed-receipt'}
    for channel in ('stdout', 'stderr'):
        output = (value.get('outputs') or {}).get(channel) or {}
        try:
            valid = isinstance(output.get('path'), str) and sha(output['path']) == output.get('sha256')
        except OSError:
            valid = False
        if not valid:
            return {'classification': 'unknown', 'reason': f'invalid-{channel}-output'}
    return {'classification': 'completed-and-validated'}


def prior_uncertainty(c):
    for path in operation_dir(c).glob('*.operation.json'):
        outcome = inspect_receipt(path)
        if outcome['classification'] in ('unknown', 'failed'):
            raise RuntimeError(f'earlier submission requires head disposition: {path.name} ({outcome["reason"]})')


def ask_count(c):
    count = 0
    for path in operation_dir(c).glob('*.operation.json'):
        value = load(path)
        if value is None:
            raise RuntimeError(f'corrupt receipt blocks cap calculation: {path.name}')
        if value.get('kind') == 'ask':
            count += 1
    return count


def expected_id_path(c):
    return operation_dir(c).parent / 'identities.json'


def freeze_identity(c, role, observed):
    if not observed:
        raise RuntimeError('missing observed thread identity')
    path = expected_id_path(c)
    identities = load(path) or {'schema': 'g09-run02-identities/v1', 'roles': {}}
    previous = identities['roles'].get(role)
    if previous and previous != observed:
        raise RuntimeError(f'cross-role or changed identity for {role}: {previous!r} != {observed!r}')
    for other_role, identity in identities['roles'].items():
        if other_role != role and identity == observed:
            raise RuntimeError(f'cross-role identity collision: {role} and {other_role} both use {observed}')
    identities['roles'][role] = observed
    write(path, identities)


def require_identity(c, role, vault, completed=False, warm=False):
    value = require_profile(c, vault)
    thread_id = value.get('threadId')
    if not thread_id:
        raise RuntimeError('missing known thread identity; refusing invocation')
    identities = load(expected_id_path(c)) or {}
    expected = (identities.get('roles') or {}).get(role)
    if expected != thread_id:
        raise RuntimeError('vault identity does not match frozen role identity')
    if completed and (not value.get('lastTurnId') or value.get('inFlightTurnId')):
        raise RuntimeError('vault lacks completed bootstrap turn; refusing invocation')
    if warm and value.get('preamble') != c['preamble']['warm']:
        raise RuntimeError('warm vault lacks pinned preamble')
    if warm:
        require_bootstrap_receipt(c, role, current=value)
        runtime = value.get('runtime') or {}
        if runtime.get('model') != c['target_profile']['model'] or runtime.get('reasoningEffort') != c['target_profile']['effort'] or not sandbox_ok(runtime.get('sandbox')):
            raise RuntimeError('warm vault lacks observed model/high/read-only runtime')
    return value


def require_profile(c, vault):
    value = state(vault)
    if not value or value.get('model') != c['target_profile']['model'] or not sandbox_ok(value.get('sandbox')):
        raise RuntimeError('vault profile mismatch; refusing invocation')
    if (value.get('turnOverrides') or {}).get('effort') != c['target_profile']['effort']:
        raise RuntimeError('vault lacks intended high reasoning override')
    return value


def bootstrap_receipt_path(c, role):
    return receipt_path(c, f'run02.{role}.bootstrap')


def require_bootstrap_receipt(c, role, current=None):
    receipt = bootstrap_receipt_path(c, role)
    outcome = inspect_receipt(receipt)
    value = load(receipt) or {}
    if outcome['classification'] != 'completed-and-validated' or value.get('verified') is not True:
        raise RuntimeError(f'{role} lacks validated cold bootstrap readback')
    item = rounds(c).get(value.get('cycle')) or {}
    if item.get('mode') != 'cold' or item.get('role') != role:
        raise RuntimeError(f'{role} bootstrap receipt has changed role or non-cold cycle')
    evidence = value.get('evidence') or {}
    for name in ('ask_receipt', 'read_receipt', 'read_stdout'):
        anchor = evidence.get(name) or {}
        try:
            actual = sha(anchor['path'])
        except (KeyError, OSError):
            actual = None
        if actual != anchor.get('sha256'):
            raise RuntimeError(f'{role} bootstrap evidence anchor changed: {name}')
    ask = load(evidence['ask_receipt']['path']) or {}
    read = load(evidence['read_receipt']['path']) or {}
    ask_state = ask.get('state_after') or {}
    if ask_state.get('threadId') != value.get('threadId') or ask_state.get('lastTurnId') != value.get('turnId'):
        raise RuntimeError(f'{role} bootstrap identity no longer matches cold ask receipt')
    stdout = ((read.get('outputs') or {}).get('stdout') or {})
    if stdout.get('path') != evidence['read_stdout'].get('path') or stdout.get('sha256') != evidence['read_stdout'].get('sha256'):
        raise RuntimeError(f'{role} bootstrap read receipt no longer matches frozen stdout')
    expected = dict(c['bootstrap_ack']['required'], role=role, sources=c['bootstrap_ack']['sources'][role])
    if value.get('acknowledgement') != expected or value.get('marker') != f'G09.run-02.{value.get("cycle")}':
        raise RuntimeError(f'{role} bootstrap marker or ACK changed')
    if current is not None and current.get('threadId') != value.get('threadId'):
        raise RuntimeError(f'{role} current vault thread differs from cold bootstrap')


def verify_bootstrap(cycle):
    """Locally validate the cold answer/readback acknowledgement; it makes no model call."""
    c = contract(); item = rounds(c).get(cycle)
    if not item or item.get('mode') != 'cold':
        raise RuntimeError('bootstrap verification is only valid for a cold round')
    pins = verify_pins(c); require_no_holds(c)
    ask_path, read_path = receipt_path(c, f'run02.{cycle}.ask'), receipt_path(c, f'run02.{cycle}.read')
    ask, read = load(ask_path), load(read_path)
    if inspect_receipt(ask_path)['classification'] != 'completed-and-validated' or inspect_receipt(read_path)['classification'] != 'completed-and-validated':
        raise RuntimeError('bootstrap requires validated ask and zero-turn read receipts')
    ask_state = (ask or {}).get('state_after') or {}
    thread_id, turn_id = ask_state.get('threadId'), ask_state.get('lastTurnId')
    if not thread_id or not turn_id or ask_state.get('inFlightTurnId'):
        raise RuntimeError('bootstrap ask receipt lacks completed thread/turn identity')
    stdout = ((read or {}).get('outputs') or {}).get('stdout') or {}
    try:
        readback = json.loads(Path(stdout['path']).read_text())
    except (KeyError, OSError, json.JSONDecodeError) as exc:
        raise RuntimeError('bootstrap read receipt stdout is not JSON readback') from exc
    thread = readback.get('thread') or {}
    if thread.get('id') != thread_id:
        raise RuntimeError('bootstrap readback thread identity changed')
    turn = next((value for value in thread.get('turns') or [] if value.get('id') == turn_id), None)
    if not turn or turn.get('status') != 'completed':
        raise RuntimeError('bootstrap readback lacks completed acknowledged turn')
    texts = [value.get('text') for value in turn.get('items') or [] if value.get('type') == 'agentMessage' and isinstance(value.get('text'), str)]
    if not texts:
        raise RuntimeError('bootstrap readback lacks agent acknowledgement text')
    text = texts[-1]
    lines = text.splitlines()
    marker = f'G09.run-02.{cycle}'
    if not lines or lines[0] != marker or len(lines) < 2 or not lines[1].startswith('BOOTSTRAP '):
        raise RuntimeError('bootstrap marker or ACK line mismatch')
    try:
        acknowledgement = json.loads(lines[1][len('BOOTSTRAP '):])
    except json.JSONDecodeError as exc:
        raise RuntimeError('bootstrap ACK is not JSON') from exc
    expected = dict(c['bootstrap_ack']['required'], role=item['role'], sources=c['bootstrap_ack']['sources'][item['role']])
    if acknowledgement != expected:
        raise RuntimeError('bootstrap ACK does not exactly match role/scope/sources')
    record = {'schema': 'g09-run02-bootstrap/v1', 'key': f'run02.{item["role"]}.bootstrap', 'kind': 'bootstrap', 'status': 'pending',
              'cycle': cycle, 'role': item['role'], 'pins': pins, 'verified': True, 'threadId': thread_id, 'turnId': turn_id,
              'marker': marker, 'acknowledgement': acknowledgement,
              'evidence': {'ask_receipt': {'path': str(ask_path), 'sha256': sha(ask_path)}, 'read_receipt': {'path': str(read_path), 'sha256': sha(read_path)}, 'read_stdout': stdout},
              'started_unix': time.time(), 'started_monotonic': time.monotonic(), 'runner': {'pid': os.getpid(), 'start': pstart(os.getpid())}}
    output_dir = operation_dir(c) / 'output'; output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f'run02.{item["role"]}.bootstrap.stdout.txt'; error = output_dir / f'run02.{item["role"]}.bootstrap.stderr.txt'
    output.write_text(json.dumps({'threadId': thread_id, 'turnId': turn_id, 'marker': marker}, sort_keys=True) + '\n'); error.write_text('')
    record.update(status='completed', exit=0, remote_outcome='readback-validated', outputs={'stdout': {'path': str(output), 'sha256': sha(output)}, 'stderr': {'path': str(error), 'sha256': sha(error)}}, ended_unix=time.time(), ended_monotonic=time.monotonic())
    record['elapsed_seconds'] = round(record['ended_unix'] - record['started_unix'], 3)
    reserve(c, record['key'], 'bootstrap', record)
    return inspect_receipt(bootstrap_receipt_path(c, item['role']))


def require_a3_grant(c):
    grant_path = Path(c['files']['a3_grant'])
    grant = load(grant_path)
    schema = c['a3_grant_schema']
    if not grant or grant.get('schema') != schema['schema'] or grant.get('run_id') != c['run_id'] or grant.get('authorized') is not True or grant.get('authority') != schema['authority']:
        raise RuntimeError('A3 requires explicit audited-change grant')
    i1_path, i2_path = Path(c['files']['i1_manifest']), Path(c['files']['i2_manifest'])
    i1, i2 = load(i1_path), load(i2_path)
    if not i1 or not i2 or i1.get('schema') != c['product_manifest_schema']['schema'] or i2.get('schema') != c['product_manifest_schema']['schema'] or i1.get('run_id') != c['run_id'] or i2.get('run_id') != c['run_id']:
        raise RuntimeError('A3 grant lacks valid frozen I1/I2 manifests')
    before, after = i1.get('audited_files'), i2.get('audited_files')
    changed = grant.get('audited_changed_paths') or []
    if not isinstance(before, dict) or not isinstance(after, dict) or not changed:
        raise RuntimeError('A3 grant lacks audited I1/I2 hash proof')
    if grant.get('i1_manifest') != str(i1_path) or grant.get('i2_manifest') != str(i2_path) or grant.get('i1_manifest_sha256') != sha(i1_path) or grant.get('i2_manifest_sha256') != sha(i2_path) or grant.get('i1_hashes') != before or grant.get('i2_hashes') != after:
        raise RuntimeError('A3 grant does not bind exact I1/I2 manifests and maps')
    differences = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    if sorted(changed) != differences or not differences:
        raise RuntimeError('A3 grant does not prove the exact audited changes')
    paths = c['source_scope']['product_paths']
    if any(not (path.startswith(paths['directory']) or path == paths['maintainer_file']) for path in differences):
        raise RuntimeError('A3 grant changed paths exceed product write scope')
    plan = load(c['files']['frozen_plan']) or {}
    a2 = (plan.get('packets') or {}).get('A2') or {}
    if not any(item.get('path') == str(i1_path) and item.get('sha256') == sha(i1_path) for item in a2.get('named_inputs') or []):
        raise RuntimeError('A3 grant lacks frozen A2 binding to I1 manifest')
    return {'path': str(grant_path), 'sha256': sha(grant_path)}


def compile_packets(cycles, inputs):
    c = contract()
    pins = verify_pins(c)
    all_rounds = rounds(c)
    if not cycles:
        raise RuntimeError('name one or more exact cycles to compile')
    unknown = set(cycles) - set(all_rounds)
    if unknown:
        raise RuntimeError(f'unallowlisted compile cycles: {sorted(unknown)}')
    input_records = []
    for path in inputs:
        path = Path(path)
        if not path.is_file():
            raise RuntimeError(f'missing named compile input {path}')
        input_records.append({'path': str(path), 'sha256': sha(path)})
    binding = '\n'.join(f'- `{item["path"]}` (SHA256 {item["sha256"]})' for item in input_records)
    destination = Path(c['files']['frozen_plan'])
    plan = load(destination)
    if plan is None:
        plan = {'schema': 'g09-run02-plan/v1', 'contract_sha256': sha(R / 'CONTRACT.json'), 'pins': pins, 'packets': {}}
    if plan.get('contract_sha256') != sha(R / 'CONTRACT.json') or plan.get('pins') != pins:
        raise RuntimeError('existing frozen plan has stale contract or pins')
    frozen = plan['packets']
    for cycle in cycles:
        item = all_rounds[cycle]
        source = Path(item['packet_template'])
        if not source.is_file():
            raise RuntimeError(f'missing packet template {source}')
        text = source.read_text()
        for marker in ('@@G09_NAMED_ADAPTER_INPUTS@@', '@@G09_NAMED_PRODUCT_INPUTS@@',
                       '@@G09_NAMED_CHANGED_INPUTS@@', '@@G09_FROZEN_BINDINGS@@'):
            if marker in text:
                if not binding:
                    raise RuntimeError(f'{cycle} requires exact named --input bindings')
                text = text.replace(marker, binding)
        if '@@' in text:
            raise RuntimeError(f'unresolved packet placeholder in {source}')
        packet = Path(item['compiled_packet'])
        if packet.exists() or cycle in frozen:
            raise RuntimeError(f'refusing to replace frozen packet {packet}')
        packet.parent.mkdir(parents=True, exist_ok=True)
        packet.write_text(text)
        frozen[cycle] = {'path': str(packet), 'sha256': sha(packet), 'template_sha256': sha(source),
                         'named_inputs': input_records}
    write(destination, plan)
    return plan


def readiness():
    """Offline structural readiness only; deliberately does not inspect model/profile state."""
    c = contract()
    pins = verify_pins(c)
    require_no_holds(c)
    mapped = rounds(c)
    if set(mapped) != {'R1', 'A1', 'R2', 'A2', 'A3'}:
        raise RuntimeError('run-02 round map is incomplete')
    return {'kind': 'offline-readiness', 'run_id': c['run_id'], 'pins': pins,
            'release_authorized': bool((load(c['files']['release']) or {}).get('authorized')),
            'rounds': sorted(mapped), 'target_model_turns': 0}


def current_packet(c, item):
    plan = load(c['files']['frozen_plan'])
    if not plan or plan.get('contract_sha256') != sha(R / 'CONTRACT.json') or plan.get('pins') != verify_pins(c):
        raise RuntimeError('missing or stale frozen plan')
    frozen = (plan.get('packets') or {}).get(item['cycle'])
    if not frozen or sha(item['packet_template']) != frozen.get('template_sha256') or sha(item['compiled_packet']) != frozen.get('sha256'):
        raise RuntimeError('frozen prompt/template changed; refusing invocation')
    for named in frozen.get('named_inputs') or []:
        try:
            current = sha(named['path'])
        except OSError:
            current = None
        if current != named.get('sha256'):
            raise RuntimeError(f'named frozen input changed: {named.get("path")}')
    return frozen


def reserve(c, key, kind, receipt):
    destination = receipt_path(c, key)
    operation_dir(c).mkdir(parents=True, exist_ok=True)
    def create_once():
        try:
            with destination.open('x') as handle:
                json.dump(receipt, handle, indent=2, sort_keys=True)
                handle.write('\n'); handle.flush(); os.fsync(handle.fileno())
        except FileExistsError as exc:
            raise RuntimeError(f'duplicate or corrupt receipt exists: {destination}') from exc
    if kind == 'ask':
        lock = operation_dir(c) / '.ask-cap.lock'
        try:
            handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise RuntimeError('ask reservation is already in progress') from exc
        try:
            if destination.exists():
                raise RuntimeError(f'duplicate or corrupt receipt exists: {destination}')
            if ask_count(c) >= c['attempt_budget']['maximum_target_ask_attempts']:
                raise RuntimeError('target ask cap exhausted')
            create_once()
        finally:
            os.close(handle)
            try: lock.unlink()
            except FileNotFoundError: pass
    else:
        create_once()
    return destination


def supports_high(models):
    for model in models:
        for effort in model.get('supportedReasoningEfforts') or []:
            if effort == 'high' or (isinstance(effort, dict) and effort.get('reasoningEffort') == 'high'):
                return True
    return False


def require_profile_receipt(c, role):
    receipt = receipt_path(c, f'run02.{role}.profile')
    outcome = inspect_receipt(receipt)
    value = load(receipt) or {}
    if outcome['classification'] != 'completed-and-validated' or not (value.get('profile') or {}).get('supports_high'):
        raise RuntimeError(f'{role} lacks validated zero-turn selected-model/high profile evidence')


def profile(role):
    """Released zero-turn capability evidence; open's preflight does not prove effort support."""
    c = contract()
    if role not in c['named_vaults']:
        raise RuntimeError(f'unallowlisted profile role {role}')
    pins = verify_pins(c)
    require_no_holds(c)
    release = require_release(c, 'profile', role)
    prior_uncertainty(c)
    key = f'run02.{role}.profile'
    receipt = {'schema': 'g09-run02-receipt/v1', 'key': key, 'kind': 'profile', 'status': 'pending',
               'role': role, 'pins': pins, 'release': release,
               'argv': [CODEX, 'app-server', 'model/list (zero-turn JSON-RPC)'], 'started_unix': time.time(),
               'started_monotonic': time.monotonic(), 'runner': {'pid': os.getpid(), 'start': pstart(os.getpid())},
               'timeout_environment': c['timeout_policy'], 'target_model_turns': 0}
    destination = reserve(c, key, 'profile', receipt)
    try:
        source = Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
        spec = importlib.util.spec_from_file_location('run02_tunnel_profile', source)
        tunnel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tunnel)
        transport = tunnel.AppServerTransport(codex_bin=CODEX, cwd=c['cwd'])
        transport.start()
        try:
            session = tunnel.Session(transport, timeout=float(c['timeout_policy']['TUNNEL_CODEX_TIMEOUT']))
            session.initialize()
            models = session.model_list()
        finally:
            transport.close()
        selected = [{key: value.get(key) for key in ('id', 'model', 'supportedReasoningEfforts')}
                    for value in models.get('data', []) if value.get('id') == c['target_profile']['model']]
        supported = supports_high(selected)
        output_dir = operation_dir(c) / 'output'; output_dir.mkdir(parents=True, exist_ok=True)
        stdout = output_dir / f'{key}.stdout.txt'; stderr = output_dir / f'{key}.stderr.txt'
        stdout.write_text(json.dumps({'selected': selected, 'supports_high': supported}, sort_keys=True) + '\n')
        stderr.write_text('')
        receipt.update(status='completed' if supported else 'failed', exit=0 if supported else 11,
                       remote_outcome='reported-capability', profile={'selected': selected, 'supports_high': supported},
                       outputs={'stdout': {'path': str(stdout), 'sha256': sha(stdout)}, 'stderr': {'path': str(stderr), 'sha256': sha(stderr)}})
    except Exception as exc:
        receipt.update(status='failed', exception=repr(exc), remote_outcome='unknown')
    receipt['ended_unix'] = time.time(); receipt['ended_monotonic'] = time.monotonic()
    receipt['elapsed_seconds'] = round(receipt['ended_unix'] - receipt['started_unix'], 3)
    write(destination, receipt)
    return inspect_receipt(destination)


def invoke(c, key, kind, argv, receipt, vault=None):
    destination = reserve(c, key, kind, receipt)
    environment = dict(os.environ, TUNNEL_CODEX_BIN=CODEX, TUNNEL_CODEX_USAGE='full',
                       TUNNEL_CODEX_TIMEOUT=c['timeout_policy']['TUNNEL_CODEX_TIMEOUT'])
    try:
        result = subprocess.run(argv, cwd=c['cwd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=False, env=environment)
        output_dir = operation_dir(c) / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        outputs = {}
        for channel, data in (('stdout', result.stdout or b''), ('stderr', result.stderr or b'')):
            output = output_dir / f'{key}.{channel}.txt'
            output.write_bytes(data)
            outputs[channel] = {'path': str(output), 'sha256': sha(output)}
        receipt.update(status='completed' if result.returncode == 0 else 'failed', exit=result.returncode,
                       remote_outcome='unknown' if result.returncode else 'reported-success', outputs=outputs)
    except Exception as exc:
        receipt.update(status='failed', exception=repr(exc), remote_outcome='unknown')
    receipt['state_after'] = state(vault) if vault else None
    receipt['ended_unix'] = time.time()
    receipt['ended_monotonic'] = time.monotonic()
    receipt['elapsed_seconds'] = round(receipt['ended_unix'] - receipt['started_unix'], 3)
    write(destination, receipt)
    return inspect_receipt(destination)


def run(cycle, action):
    c = contract()
    item = rounds(c).get(cycle)
    if not item:
        raise RuntimeError(f'unallowlisted cycle {cycle}')
    role, vault = item['role'], Path(item['vault'])
    key = f'run02.{cycle}.{action}'
    pins = verify_pins(c)
    if action in ('read', 'resume'):
        before = require_identity(c, role, vault)
        receipt = {'schema': 'g09-run02-receipt/v1', 'key': key, 'kind': action, 'status': 'pending',
                   'cycle': cycle, 'role': role, 'state_before': before, 'pins': pins,
                   'argv': [SHIM, action, '--state', str(vault)], 'started_unix': time.time(),
                   'started_monotonic': time.monotonic(), 'runner': {'pid': os.getpid(), 'start': pstart(os.getpid())},
                   'timeout_environment': c['timeout_policy']}
        return invoke(c, key, action, receipt['argv'], receipt, vault)
    require_no_holds(c)
    release = require_release(c, action, role)
    prior_uncertainty(c)
    if action == 'open':
        if item['mode'] != 'cold':
            raise RuntimeError('only cold role opens are allowed')
        require_profile_receipt(c, role)
        if vault.exists():
            raise RuntimeError('existing vault must be recovered, not reopened')
        argv = [SHIM, 'open', '--state', str(vault), '--enable', '--sandbox', 'read-only', '--cwd', c['cwd'],
                '--preamble', 'none', '--model', c['target_profile']['model'], '--override', 'effort=high']
        before = None
    elif action == 'ask':
        warm = item['mode'] != 'cold'
        before = require_identity(c, role, vault, completed=True, warm=True) if warm else require_profile(c, vault)
        if item['mode'] == 'cold':
            if before.get('threadId') or (load(expected_id_path(c)) or {}).get('roles', {}).get(role):
                raise RuntimeError('cold ask refused on an already-born vault')
            if before.get('preamble') is not None:
                raise RuntimeError('cold ask requires preamble none')
        if cycle == 'A3':
            a3 = require_a3_grant(c)
        frozen = current_packet(c, item)
        argv = [SHIM, 'ask', Path(frozen['path']).read_text(), '--state', str(vault)]
    elif action == 'preamble':
        if item['mode'] != 'cold':
            raise RuntimeError('preamble arming is only valid after a cold round')
        before = require_identity(c, role, vault, completed=True)
        require_bootstrap_receipt(c, role, current=before)
        argv = [SHIM, 'open', '--state', str(vault), '--preamble', c['preamble']['warm']]
    else:
        raise RuntimeError(f'unallowlisted action {action}')
    receipt = {'schema': 'g09-run02-receipt/v1', 'key': key, 'kind': action, 'status': 'pending',
               'cycle': cycle, 'role': role, 'state_before': before, 'pins': pins, 'release': release,
               'argv': argv, 'started_unix': time.time(), 'started_monotonic': time.monotonic(),
               'runner': {'pid': os.getpid(), 'start': pstart(os.getpid())}, 'timeout_environment': c['timeout_policy']}
    if action == 'ask':
        receipt['prompt'] = frozen
        receipt['attempt_number'] = ask_count(c) + 1
        if cycle == 'A3': receipt['a3_grant'] = a3
    outcome = invoke(c, key, action, argv, receipt, vault)
    after = state(vault)
    if after and after.get('threadId'):
        freeze_identity(c, role, after['threadId'])
    return outcome


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('readiness')
    compile = sub.add_parser('compile'); compile.add_argument('cycles', nargs='+'); compile.add_argument('--input', action='append', default=[])
    profile_parser = sub.add_parser('profile'); profile_parser.add_argument('role')
    bootstrap = sub.add_parser('verify-bootstrap'); bootstrap.add_argument('cycle')
    inspect = sub.add_parser('inspect'); inspect.add_argument('key')
    effect = sub.add_parser('run'); effect.add_argument('cycle'); effect.add_argument('action', choices=('open', 'ask', 'preamble', 'read', 'resume'))
    args = parser.parse_args()
    try:
        if args.command == 'readiness': value = readiness()
        elif args.command == 'compile': value = compile_packets(args.cycles, args.input)
        elif args.command == 'profile': value = profile(args.role)
        elif args.command == 'verify-bootstrap': value = verify_bootstrap(args.cycle)
        elif args.command == 'inspect': value = inspect_receipt(receipt_path(contract(), args.key))
        else: value = run(args.cycle, args.action)
        print(json.dumps(value, sort_keys=True))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
