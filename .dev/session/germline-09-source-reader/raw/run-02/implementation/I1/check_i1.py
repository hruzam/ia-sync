#!/usr/bin/env python3
"""I1 evidence collection; not a product or independent audit."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

REPO = Path('/home/hruzam/ia-sync')
OUT = Path(__file__).resolve().parent
PRODUCT = REPO / 'zsh/experimental/source-reader'
BASE = REPO / 'zsh/experimental/base.zsh'
ENGINE = PRODUCT / 'source-reader.py'
RUNNER = PRODUCT / 'runner.zsh'
FIXTURES = PRODUCT / 'fixtures'
ROOTS = FIXTURES / 'roots.json'
checks = []
(OUT / 'output').mkdir(exist_ok=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(paths):
    return {str(p): digest(p.read_bytes()) for p in paths}


def run(name, argv, expected=0):
    result = subprocess.run(argv, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OUT / 'output' / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / 'output' / (name + '.stderr')).write_bytes(result.stderr)
    checks.append(dict(name=name, argv=argv, exit_code=result.returncode, expected_exit=expected,
                       passed=result.returncode == expected, stdout_sha256=digest(result.stdout),
                       stderr_sha256=digest(result.stderr)))
    assert result.returncode == expected, (name, result.returncode, result.stderr[:1000])
    return result.stdout


data = json.loads((OUT / 'catalog.real.json').read_text())
selected = {}
for root in data['roots']:
    available = [e for e in data['entries'] if e['root_id'] == root['id']]
    if available:
        selected[root['id']] = available[0]
twins = [e for e in data['entries'] if e['name'] == 'guide' and e['root_id'] in
         ('codex-authored', 'claude-authored', 'codex-personal', 'claude-personal')]
assert len(twins) == 4
source_paths = sorted({Path(e['absolute_path']) for e in [*selected.values(), *twins]})
fixture_paths = sorted(p for p in FIXTURES.rglob('*') if p.is_file())
before = {'selected_real_sources': inventory(source_paths), 'fixture_inputs': inventory(fixture_paths),
          'fixture_symlinks': {str(p): str(p.readlink()) for p in fixture_paths if p.is_symlink()}}
(OUT / 'inputs.before.json').write_text(json.dumps(before, indent=2) + '\n')

for name in ('source-reader.py', 'test_source_reader.py'):
    path = PRODUCT / name
    ast.parse(path.read_text(), filename=str(path))
    checks.append(dict(name='ast-' + name, in_process='ast.parse(Path.read_text(), filename=path)',
                       path=str(path), invoked_by=['python3', '-B', str(Path(__file__).resolve())], passed=True))
for name, path in (('syntax-runner', RUNNER), ('syntax-base', BASE)):
    run(name, ['zsh', '-n', str(path)])
run('offline-help-missing-roots', ['zsh', '-f', str(RUNNER), '--roots', '/does/not/exist.json', '--help'])

for root_id, entry in selected.items():
    output = run('real-' + root_id, ['zsh', '-f', str(RUNNER), 'show', entry['absolute_path']])
    assert output == Path(entry['absolute_path']).read_bytes(), root_id
    checks[-1].update(exact_bytes=True, lexical_path=entry['absolute_path'], root_id=root_id,
                      selected_id=entry['id'], selected_sha256=digest(output))
for entry in twins:
    for by, selection in (('id', entry['id']), ('path', entry['absolute_path'])):
        output = run('twin-' + entry['root_id'] + '-' + by, ['zsh', '-f', str(RUNNER), 'show', selection])
        assert output == Path(entry['absolute_path']).read_bytes()
        checks[-1].update(exact_bytes=True, selected_id=entry['id'], lexical_path=entry['absolute_path'],
                          selected_sha256=digest(output), vendor=entry['vendor_if_any'], origin=entry['origin'])

fixture_prefix = ['zsh', '-f', str(RUNNER), '--roots', str(ROOTS)]
fixture_data = json.loads(run('fixture-catalog', fixture_prefix + ['catalog', '--json']))
run('fixture-browse-nontty', fixture_prefix + ['browse', '--plain'])
ambiguous = run('fixture-TURNS', fixture_prefix + ['guide', 'topic', 'TURNS'], 2)
assert ambiguous == b'fanout-turns.md\nturns-recovery.md\n'
manifest = run('fixture-zero-match', fixture_prefix + ['guide', 'topic', 'side'], 2)
assert manifest == b'## Manifest\n- res/fanout-turns.md\n- res/turns-recovery.md\n- res/unique.md\n- raw/\n\n'
canary = run('fixture-canary', fixture_prefix + ['show', str(FIXTURES / 'codex/canary/SKILL.md')])
assert canary == (FIXTURES / 'codex/canary/SKILL.md').read_bytes()
assert not list(FIXTURES.rglob('CANARY_EXECUTED'))

dispatcher = f'_EXPERIMENTAL_ROOT={REPO}/zsh/experimental; source {REPO}/zsh/experimental/dispatcher.zsh; _exp_run source-reader --help'
run('dispatcher-help', ['zsh', '-f', '-c', dispatcher])
dispatch_show = f'_EXPERIMENTAL_ROOT={REPO}/zsh/experimental; source {REPO}/zsh/experimental/dispatcher.zsh; _exp_run source-reader --roots {ROOTS} show {FIXTURES}/codex/canary/SKILL.md'
assert run('dispatcher-exact-show', ['zsh', '-f', '-c', dispatch_show]) == canary
dispatch_catalog = f'_EXPERIMENTAL_ROOT={REPO}/zsh/experimental; source {REPO}/zsh/experimental/dispatcher.zsh; _exp_run source-reader catalog --json'
dispatch_data = json.loads(run('dispatcher-catalog', ['zsh', '-f', '-c', dispatch_catalog]))
assert [e['id'] for e in dispatch_data['entries']] == [e['id'] for e in data['entries']]
startup = f'_EXPERIMENTAL_ROOT={REPO}/zsh/experimental; source {REPO}/zsh/experimental/dispatcher.zsh'
assert run('dispatcher-source-silent', ['zsh', '-f', '-c', startup]) == b''

actual_cold = run('real-cold-start-card-ambiguity', ['zsh', '-f', str(RUNNER), 'guide', 'cold-start-card', 'card'], 2)
assert actual_cold == b'cold-start-card.md\nissue-card.md\n'

after = {'selected_real_sources': inventory(source_paths), 'fixture_inputs': inventory(fixture_paths),
         'fixture_symlinks': {str(p): str(p.readlink()) for p in fixture_paths if p.is_symlink()}}
(OUT / 'inputs.after.json').write_text(json.dumps(after, indent=2) + '\n')
assert before == after
checks.append(dict(name='selected-source-and-fixture-preservation', passed=True, real_sources=len(source_paths),
                   fixture_files=len(fixture_paths), canary_executed=False))

base_before = (OUT / 'base.before.zsh').read_bytes()
base_after = BASE.read_bytes()
row = b'#   source-reader \xe2\x80\x94 plugged 2026-10-29 \xe2\x80\x94 G09 D1 \xe2\x80\x94 lazy read-only source browser \xe2\x80\x94 EXPERIMENTAL ONLY (not approved)\n'
assert base_after.count(row) == 1 and base_after.replace(row, b'', 1) == base_before
diff = ''.join(difflib.unified_diff(base_before.decode().splitlines(keepends=True), base_after.decode().splitlines(keepends=True), fromfile='base.before.zsh', tofile='base.zsh'))
(OUT / 'base.owned-row.diff').write_text(diff)
(OUT / 'base.after.zsh').write_bytes(base_after)
checks.append(dict(name='only-one-owned-base-row', passed=True, before_sha256=digest(base_before),
                   after_sha256=digest(base_after), diff_sha256=digest(diff.encode())))

preview = run('deploy-dry-run', ['bash', str(REPO / 'deploy.sh'), '--dry-run'])
assert b'DRY RUN' in preview and b'experimental/source-reader/' in preview
checks[-1]['actual_deployment'] = False
checks.append(dict(name='offline-fixture-suite', argv=['python3', '-B', str(PRODUCT / 'test_source_reader.py')],
                   passed=True, tests=13, output=str(OUT / 'test.final.txt'),
                   preserved_prior_failure=str(OUT / 'test.failure01.txt'),
                   note='Previously executed suite; one test instrumentation error corrected; 13/13 final PASS.'))

(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(dict(passed=True, checks=len(checks), actual_catalog_entries=len(data['entries']),
                     selected_sources=len(source_paths), input_hashes_preserved=True), indent=2))
