#!/usr/bin/env python3
"""Create an isolated SYNTHETIC Jev reader playground; never send or use credentials."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BED = Path(__file__).resolve().parents[1]
SOURCE = BED.parents[2] / 'zsh' / 'jev'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', type=Path, default=Path.home() / '.local/share',
                        help='existing parent; creates a new private demo directory each run')
    args = parser.parse_args()
    os.umask(0o077)
    home = Path(tempfile.mkdtemp(prefix='jev-reader-demo-', dir=args.parent))
    root, project, inputs, views = (home / name for name in ('vault', 'synthetic-project', 'inputs', 'views'))
    for directory in (project, inputs, views):
        directory.mkdir(mode=0o700)
    # Do not inherit credentials or ambiguous controller identity into fixture commands.
    environment = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL') if key in os.environ}
    counter = 0

    def document(value):
        nonlocal counter
        counter += 1
        path = inputs / f'{counter:03}.json'
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        return str(path)

    def call(session, *words, cli='codex', expected=0):
        command = [sys.executable, '-B', str(SOURCE / 'jev.py'), '--root', str(root),
                   '--cli', cli, '--cli-session', f'SYNTHETIC-{cli}-reader-demo', '--requester', 'agent']
        if session:
            command += ['--session', session, '--channel', 'main']
        result = subprocess.run(command + list(map(str, words)), env=environment,
                                capture_output=True, text=True, timeout=20)
        if result.returncode != expected:
            raise RuntimeError(f'{words[0]} exited {result.returncode}: {result.stderr} {result.stdout}')
        return json.loads(result.stdout)

    def note(session, text, refs=(), cli='codex'):
        return call(session, 'memory', document({'version': 'synthetic-reader-demo/v1',
                    'author': f'SYNTHETIC {cli} fixture author',
                    'text': '[SYNTHETIC — invented reader test; not Jev inference]\n' + text,
                    'refs': list(refs)}), cli=cli)

    sessions = []
    for name in ('01-memory-notes', '02-mixed-judgments', '03-invalid-reply', '04-no-memory'):
        bed = project / name
        bed.mkdir(mode=0o700)
        opened = call(None, 'open', '--project', project, '--bed', bed)
        sessions.append({'name': name, 'session': opened['session_id'], 'ledger': opened['ledger']})
    a, b, c, d = [entry['session'] for entry in sessions]
    n1 = note(a, 'DECISION: CSV input uses comma delimiters.\nKeep original row order.\nStatus: accepted for this fictional example.')
    note(a, 'OPEN: maximum input size is unspecified.\nNext action: ask the fictional task owner; do not invent a limit.', [n1['event_id']], 'claude')
    note(a, 'CORRECTION: the fixture now uses semicolon delimiters.\nThis note supersedes the earlier comma decision; both remain readable.', [n1['event_id']], 'gemini')
    note(a, 'Unicode and multiline fixture:\nPříliš žluťoučký kůň. Ελληνικά. 日本語.\n\tIndented detail.\n\nSecond paragraph.')
    note(a, 'Literal display fixture, never execute:\n```sh\necho DEMO_ONLY\n```\n<script>DEMO_ONLY</script>\nESC stays visible: \x1b[31mDEMO\x1b[0m')
    note(a, 'Long note for navigation and composition:\n' + '\n'.join(f'{i:02}. Fictional observation {i}; verification is still pending.' for i in range(1, 31)))

    initial = note(b, 'CONTEXT: review a fictional importer brief. An unfinished task may be explicitly accounted for.')
    packet = json.loads((BED / 'tests/fixtures/brief-missing.json').read_text())
    packet['session_id'] = b
    packet['state']['fixture_notice'] = 'SYNTHETIC; all scores invented for renderer testing'
    prepared = call(b, 'prepare', document(packet), '--memory', initial['event_id'])
    request = prepared['request_id']
    receipt = {'schema': 'jev.receipt/v1', 'request_id': request,
               'packet_sha256': prepared['prepared']['packet_sha256'], 'model': 'synthetic-reader-demo/v1',
               'answers': [
                   {'id': 'missing', 'type': 'noul', 'probability': 0.55},
                   {'id': 'action', 'type': 'choice', 'value': 'clarify',
                    'probabilities': {'clarify': 0.7, 'proceed': 0.3}, 'confidence': 0.6},
                   {'id': 'coverage', 'type': 'score', 'value': 0.5,
                    'probabilities': {'0': 0.6, '1': 0.3, '2': 0.1, '3': 0}, 'confidence': 0.5}]}
    reply = call(b, 'import-reply', request, document(receipt))
    policy = document({'id': 'synthetic-demo-thresholds', 'version': '1', 'low': 0.2, 'high': 0.8})
    interpreted = call(b, 'interpret', request, 'missing', policy)
    assert interpreted['data']['result']['status'] == 'UNCERTAIN'
    call(b, 'dispose', request, 'reconsider', '--consumer', 'synthetic-reader', '--reason', 'SYNTHETIC: missing constraints')
    call(b, 'outcome', request, document({'fixture': 'SYNTHETIC', 'assessment': 'Fictional reviewer asks for missing limits.',
                                        'refs': [reply['event_id']]}), cli='claude')
    correction = note(b, 'LATER REVIEW: keep this case open; the 0.55 is invented, not measured calibration.', [reply['event_id']], 'claude')
    call(b, 'prepare', document(packet), '--memory', correction['event_id'], '--lineage', document({
        'branch': 'synthetic-followup', 'step': '1', 'parent_request_ids': [request],
        'reconsider_of': request, 'reason': 'SYNTHETIC follow-up; deliberately no reply'}))
    note(b, 'FOLLOW-UP pending: the second preparation has no reply. Missing response must not display as zero.', [correction['event_id']], 'gemini')

    note(c, 'INVALID OBSERVATION fixture: retain the failure, do not present it as valid advice.')
    packet['session_id'] = c
    packet.pop('memory', None)
    bad_prepared = call(c, 'prepare', document(packet))
    bad = call(c, 'import-reply', bad_prepared['request_id'], document({'fixture': 'SYNTHETIC invalid receipt'}), expected=2)
    assert bad['data']['validation']['status'] == 'INVALID'
    note(c, 'Malformed typed receipt was retained as synthetic evidence. No successful judgment is available.', [bad['event_id']])
    # Session d intentionally contains only its opening event.
    manifest = {'schema': 'jev.reader-demo/v1', 'notice': 'SYNTHETIC ONLY; no credentials, network or provider calls',
                'home': str(home), 'root': str(root), 'sessions': sessions}
    for entry in sessions:
        history = call(entry['session'], 'show')
        counts = Counter(e['kind'] for e in history['events'])
        entry.update(events=len(history['events']), memories=counts['memory'], kinds=dict(counts),
                     ledger_sha256=hashlib.sha256(Path(entry['ledger']).read_bytes()).hexdigest())
        assert history['tail'] is None
        assert not any(e['kind'] in ('attempt', 'http', 'settle') for e in history['events'])
    assert [s['memories'] for s in sessions] == [6, 3, 2, 0]
    (home / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (home / 'README.md').write_text('# Synthetic Jev reader playground\n\nAll content is invented. No provider calls.\n\n'
        f'Open: `jev-browse --root {root}`\n\n'
        'Enter opens a session; m switches memory/all; a marks visible records; p composes; q quits.\n'
        'Start with 01-memory-notes. Marks persist across filter changes; reopen a session for a fresh selection.\n'
        '04-no-memory intentionally has no notes. Source ledgers stay private and unchanged by reading.\n'
        'Browser compositions are temporary; explicit saved views can go in the private views/ directory.\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
