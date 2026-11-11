"""Read-only office probe; prints derived diagnostics, never source bodies or keys."""
import base64
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_EVEN
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
BED = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'zsh/jev'))
import provider

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

old = json.loads((BED / 'raw/handoff-check.2026-11-10.json').read_text())
parity = {}
for name, prior in old['source_installed'].items():
    source = sha(ROOT / 'zsh/jev' / name)
    live = sha(Path.home() / '.config/zsh/jev' / name)
    assert source == live == prior['source_sha256'] == prior['installed_sha256']
    parity[name] = source
ledger = Path(old['settings']['ledger'])
before = sha(ledger)
assert before == old['ledger_sha256']
events = [json.loads(line) for line in ledger.read_text().splitlines()]
settings = json.loads(subprocess.check_output([
    sys.executable, '-B', str(ROOT / 'zsh/jev/jev.py'), '--root', old['settings']['root'],
    '--session', old['settings']['session_id'], '--channel', 'main', 'settings']))
assert settings == old['settings']
rid = 'fcf5015cdaa146c5a01ff33fbb6fa9d3'
selected = {e['kind']: e for e in events if e.get('request_id') == rid}
prepared = selected['prepare']['data']['prepared']
response = Path.home() / '.jev/practical-gates-20261110/provider-response.json'
raw = response.read_bytes()
for kind in ('http', 'reply'):
    data = selected[kind]['data']
    assert raw == base64.b64decode(data['raw_base64'])
    assert hashlib.sha256(raw).hexdigest() == data['raw_sha256']
parsed = provider.parse_response(prepared, raw, settings['policy']['allowed_models'])
assert parsed['validation'] == selected['reply']['data']['validation']
assert parsed['receipt'] == selected['reply']['data']['receipt']
assert parsed['validation']['status'] == 'INVALID'
wire = json.loads(raw, parse_float=D, parse_int=D)
# Constructive feasibility examples ONLY: unknown provider precision is not a contract.
witnesses = {
    'S2_maturity': ['.013', '0', '.957', '.030'],
    'S4_maturity': ['.003', '0', '.040', '.957'],
    'S6_maturity': ['.107', '.010', '.883', '0'],
}
rows = []
for qid, answer in wire['answers'].items():
    if answer['type'] != 'score':
        continue
    p = answer['probabilities']
    expected = sum(D(i) * v for i, v in p.items())
    row = {'question': qid, 'score': str(answer['score']), 'weighted': str(expected),
           'scalar_minus_weighted': str(answer['score'] - expected),
           'probability_sum': str(sum(p.values()))}
    if qid in witnesses:
        hidden = list(map(D, witnesses[qid]))
        assert sum(hidden) == 1 and all(0 <= v <= 1 for v in hidden)
        rounded = [v.quantize(D('.01'), rounding=ROUND_HALF_EVEN) for v in hidden]
        assert rounded == [p[str(i)] for i in range(len(hidden))]
        mean = sum(i * v for i, v in enumerate(hidden))
        assert mean.quantize(D('.01'), rounding=ROUND_HALF_EVEN) == answer['score']
        row['hypothetical_nearest_cent_witness'] = {'probabilities': list(map(str, hidden)),
                                                  'unrounded_mean': str(mean)}
    rows.append(row)
lab = Path.home() / 'nabla-lab/session/research-jev-usage/round-2.2026-11-10'
protocol_hash = sha(lab / 'calibration-protocol.md')
assert protocol_hash == 'efbd3e188a04fa9ddf79d8581c676a3654bef1011506f2ab84dfdc5682c8a513'
assert sha(ledger) == before and response.read_bytes() == raw
print(json.dumps({'source_live_unchanged': parity, 'ledger_sha256': before,
    'event_counts': dict(Counter(e['kind'] for e in events)), 'budget': settings['budget'],
    'response_sha256': hashlib.sha256(raw).hexdigest(), 'native_validation': parsed['validation'],
    'native_cost_usd': parsed['cost_usd'], 'scores': rows,
    'calibration_protocol_sha256': protocol_hash,
    'implementation_substrate_sha256': sha(lab / 'implementation-substrate.md'),
    'inference_calls': 0, 'ledger_unchanged': True,
    'rounding_status': 'Hypothesis only; no provider serialization guarantee established'}, indent=2))
