"""Read-only document/preservation check; not implementation verification."""
from pathlib import Path
import hashlib
import json
import re
import yaml

ROOT = Path('/home/hruzam/ia-sync')
BED = ROOT / '.dev/session/jev-01-codex-pilot'
before = json.loads((BED / 'raw/resume-before.2026-10-27.json').read_text())
changed = [name for name, digest in before['files'].items()
           if not (ROOT / name).is_file()
           or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
assert changed == ['.dev/session/jev-01-codex-pilot/STATUS.md'], changed

def snapshot(name):
    return yaml.safe_load((BED / name).read_text().split('```yaml\n', 1)[1].split('```', 1)[0])

assert snapshot('RUNBOOK.md')['gate'] == snapshot('STATUS.md')['gate']
assert {'updated', 'writer', 'host', 'worktree', 'gate', 'checkpoint', 'in_flight',
        'recovery_probe', 'holds', 'next', 'expected'} <= snapshot('STATUS.md').keys()
decision = (BED / 'raw/decision-01.engagement.md').read_text()
assert len(re.findall(r'^- \[ \]', decision, re.M)) == 2
assert not re.search(r'^- \[[xX]\]', decision, re.M)
old = ROOT / '.dev/session/jev-implementation-00-build/raw/majkee-gavels.2026-10-12.md'
assert len(re.findall(r'^## [1-8]\. ', old.read_text(), re.M)) == 8
assert not re.search(r'^- \[[xX]\]', old.read_text(), re.M)
ret = (BED / '_bus/01.verifier.return.md').read_text()
assert re.findall(r'^## (.+)$', ret, re.M) == [
    '1. Files changed', '2. Commands and outcomes', '3. Evidence paths',
    '4. Mismatches discovered', '5. Recommended next task', '6. Remaining uncertainty']
assert not (BED / 'impl').exists() and not (BED / 'tests').exists()
assert not Path('/home/hruzam/.jev').exists()
names = ['STATUS.md', 'raw/design-packet.2026-10-27.md', 'raw/decision-01.engagement.md',
         'raw/oraculum-consult.2026-10-27.md', '_bus/01.cartan.point.md',
         '_bus/01.verifier.return.md', '_bus/01.cartan.verdict.md']
for name in names:
    data = (BED / name).read_bytes()
    assert data.endswith(b'\n') and b'\r' not in data, name
    assert all(line == line.rstrip() for line in data.splitlines()), name
print(json.dumps({
    'result': 'PASS', 'scope': 'packet structure and captured prior-file preservation only',
    'changed_prior_files': changed,
    'old_gavel_sha256': hashlib.sha256(old.read_bytes()).hexdigest(),
    'artifact_sha256': {name: hashlib.sha256((BED / name).read_bytes()).hexdigest()
                        for name in names if name != 'STATUS.md'},
    'implementation_and_runtime_store': 'absent',
}, indent=2))
