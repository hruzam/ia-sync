import json
from pathlib import Path
import subprocess

repo = Path('/home/hruzam/ia-sync')
backup = Path('/home/hruzam/.local/state/ia-sync/backups/monitor-01-cycle15/20261112T163955Z')
journal = 'journal.host-cleanup.md'
mail = '_mail/office/inbox/cartan.monitor-ssh-journal.2026-11-12.md'
meta = json.loads((backup / 'metadata.json').read_text())

def git(*args, check=True):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=check)

if git('rev-parse', 'HEAD').stdout.decode().strip() != meta['original_head']:
    raise RuntimeError('HEAD changed after snapshot')
if git('rev-parse', 'origin/main').stdout.decode().strip() != meta['incoming_head']:
    raise RuntimeError('origin/main changed after snapshot')
if git('status', '--porcelain=v1').stdout.decode().splitlines() != meta['tracked_status']:
    raise RuntimeError('worktree changed after snapshot')
if git('write-tree').stdout.decode().strip() != meta['index_tree']:
    raise RuntimeError('index changed after snapshot')
prior = git('rev-parse', '-q', '--verify', 'refs/stash', check=False)
prior_oid = prior.stdout.decode().strip() if prior.returncode == 0 else None
push = git('stash', 'push', '-m', 'monitor-01-cycle15-office-preserve', '--', journal, mail)
oid = git('rev-parse', 'refs/stash').stdout.decode().strip()
if oid == prior_oid:
    raise RuntimeError('path-scoped stash did not create a new object')
paths = git('diff', '--name-only', f'{oid}^1', oid).stdout.decode().splitlines()
if paths != [mail, journal]:
    raise RuntimeError(f'stash paths differ: {paths}')
if git('diff', '--name-only', f'{oid}^1', f'{oid}^2').stdout:
    raise RuntimeError('stash unexpectedly captured staged changes')
if git('rev-list', '--parents', '-n', '1', oid).stdout.decode().split().__len__() != 3:
    raise RuntimeError('stash unexpectedly has untracked parent')
if git('status', '--porcelain=v1').stdout:
    raise RuntimeError('worktree not clean after path-scoped stash')
if git('write-tree').stdout.decode().strip() != meta['index_tree']:
    raise RuntimeError('index changed after stash')
(backup / 'stash.oid').write_text(oid + '\n')
print(json.dumps({'backup': str(backup), 'prior_stash_oid': prior_oid,
                  'stash_oid': oid, 'captured_paths': paths,
                  'push_output': push.stdout.decode().strip(),
                  'worktree_and_index_clean': True}, indent=2))
