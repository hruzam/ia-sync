#!/usr/bin/env python3
"""Narrow I2 builder evidence; independent A3/P7 remain separate gates."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

REPO = Path('/home/hruzam/ia-sync')
OUT = Path(__file__).resolve().parent
I1 = OUT.parent / 'I1'
PRODUCT = REPO / 'zsh/experimental/source-reader'
RUNNER = PRODUCT / 'runner.zsh'
ROOTS = PRODUCT / 'fixtures/roots.json'
LINKED = PRODUCT / 'fixtures/codex/linked/SKILL.md'
TARGET = PRODUCT / 'fixtures/claude/guide/SKILL.md'
checks = []
(OUT / 'output').mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, argv):
    result = subprocess.run(argv, cwd=REPO, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OUT / 'output' / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / 'output' / (name + '.stderr')).write_bytes(result.stderr)
    checks.append(dict(name=name, argv=argv, exit_code=result.returncode,
                       passed=result.returncode == 0,
                       stdout_sha256=hashlib.sha256(result.stdout).hexdigest(),
                       stderr_sha256=hashlib.sha256(result.stderr).hexdigest()))
    assert result.returncode == 0, (name, result.stderr)
    return result.stdout


for name in ('source-reader.py', 'test_source_reader.py'):
    path = PRODUCT / name
    ast.parse(path.read_text(), filename=str(path))
    checks.append(dict(name='syntax-' + name, passed=True,
                       in_process='ast.parse(Path.read_text(), filename=path)', path=str(path)))
run('syntax-runner', ['zsh', '-n', str(RUNNER)])

prefix = ['zsh', '-f', str(RUNNER), '--roots', str(ROOTS)]
data = json.loads(run('fixture-catalog-json', prefix + ['catalog', '--json']))
old_data = json.loads((I1 / 'output/fixture-catalog.stdout').read_text())
assert data == old_data
checks[-1]['unchanged_I1_catalog_metadata'] = True
linked = next(e for e in data['entries'] if e['absolute_path'] == str(LINKED))
expected_label_end = f'{LINKED} → {TARGET}'
for name, args in (('fixture-terminal-catalog', ['catalog']), ('fixture-terminal-browse', ['browse', '--plain'])):
    body = run(name, prefix + args)
    row = next(line for line in body.decode().splitlines() if line.startswith(linked['id'] + '\t'))
    assert row.split('\t')[2:4] == ['codex', 'authored']
    assert row.endswith(expected_label_end)
    checks[-1]['linked_label'] = row

for method, selection in (('path', str(LINKED)), ('id', linked['id'])):
    body = run('fixture-linked-show-' + method, prefix + ['show', selection])
    assert body == TARGET.read_bytes()
    checks[-1]['exact_selected_bytes'] = True

setup = f'_EXPERIMENTAL_ROOT={REPO}/zsh/experimental; source {REPO}/zsh/experimental/dispatcher.zsh; '
commands = {
    'dispatcher-help': setup + '_exp_run source-reader --help',
    'dispatcher-catalog': setup + f'_exp_run source-reader --roots {ROOTS} catalog',
    'dispatcher-show': setup + f'_exp_run source-reader --roots {ROOTS} show {LINKED}',
}
for name, command in commands.items():
    output = run(name, ['zsh', '-f', '-c', command])
    if name == 'dispatcher-catalog':
        assert expected_label_end.encode() in output
    if name == 'dispatcher-show':
        assert output == TARGET.read_bytes()
    checks[-1]['builder_only_P7_evidence'] = True

i1 = json.loads((I1 / 'MANIFEST.json').read_text())
before = json.loads((OUT / 'BEFORE-I2.json').read_text())
after = {str(p): sha(p) for p in sorted([p for p in PRODUCT.rglob('*') if p.is_file()] + [REPO / 'zsh/experimental/base.zsh'])}
changed = sorted(p for p in set(after) | set(i1['audited_files']) if after.get(p) != i1['audited_files'].get(p))
assert changed == [str(PRODUCT / 'source-reader.py'), str(PRODUCT / 'test_source_reader.py')]
change_map = {}
for path in changed:
    old = Path(before['files'][path]['snapshot'])
    new = Path(path)
    diff = ''.join(difflib.unified_diff(old.read_text().splitlines(keepends=True), new.read_text().splitlines(keepends=True), fromfile='I1/' + str(new.relative_to(REPO)), tofile='I2/' + str(new.relative_to(REPO))))
    diff_path = OUT / (new.name + '.I1-to-I2.diff')
    diff_path.write_text(diff)
    change_map[path] = dict(before_sha256=i1['audited_files'][path], after_sha256=after[path],
                            before_snapshot=str(old), diff=str(diff_path), diff_sha256=sha(diff_path))

for source, info in before['files'].items():
    snapshot = Path(info['snapshot'])
    assert sha(snapshot) == info['sha256']
    assert (str(snapshot.readlink()) if snapshot.is_symlink() else None) == info['symlink_target']
    if source not in changed:
        assert sha(Path(source)) == info['sha256']
checks.append(dict(name='I1-snapshots-and22-unchanged-product-files', passed=True,
                   snapshots=24, changed_files=2, base_unchanged=True, fixture_files_unchanged=19))
i1_evidence = json.loads((OUT / 'I1.evidence.before.json').read_text())
assert all(sha(Path(path)) == expected for path, expected in i1_evidence.items())
assert {str(p) for p in I1.rglob('*') if p.is_file()} == set(i1_evidence)
checks.append(dict(name='I1-evidence-byte-preservation', passed=True, files=len(i1_evidence)))

(OUT / 'CHANGE-MAP.json').write_text(json.dumps(change_map, indent=2) + '\n')
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(dict(passed=True, checks=len(checks), changed_files=changed,
                     snapshots_verified=24, I1_evidence_preserved=True, base_unchanged=True), indent=2))
