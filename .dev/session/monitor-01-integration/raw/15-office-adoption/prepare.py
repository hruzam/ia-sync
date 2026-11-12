import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from datetime import datetime, timezone

repo = Path('/home/hruzam/ia-sync')
journal = 'journal.host-cleanup.md'
mail = '_mail/office/inbox/cartan.monitor-ssh-journal.2026-11-12.md'
paths = [journal, mail]
backup_root = Path('/home/hruzam/.local/state/ia-sync/backups/monitor-01-cycle15')

def git(*args, check=True):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=check)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def added_lines(before, after):
    old = before.splitlines(keepends=True)
    new = after.splitlines(keepends=True)
    added = []
    for tag, start, end, new_start, new_end in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        if tag != 'insert':
            raise RuntimeError(f'non-insertion journal change: {tag}')
        added.extend(new[new_start:new_end])
    return added

head = git('rev-parse', 'HEAD').stdout.decode().strip()
origin = git('rev-parse', 'origin/main').stdout.decode().strip()
branch = git('symbolic-ref', '--short', 'HEAD').stdout.decode().strip()
staged = git('diff', '--cached', '--name-only').stdout
status = git('status', '--porcelain=v1', '-uno').stdout.decode().splitlines()
if head != 'f2578a5646f130ddcd0117682dda3a857d64b811' or branch != 'main':
    raise RuntimeError('unexpected office HEAD/branch')
if origin != 'b962110f2f7798defd578371a846d1d6429d6cd5':
    raise RuntimeError('incoming main changed; review needed')
if staged or status != [' D ' + mail, ' M ' + journal]:
    raise RuntimeError(f'unexpected index/worktree state: staged={staged!r}, status={status!r}')
if git('merge-base', '--is-ancestor', 'HEAD', 'origin/main', check=False).returncode != 0:
    raise RuntimeError('office HEAD is not ancestor of origin/main')
local = (repo / journal).read_bytes()
if sha(local) != 'b478fc5f65d09eaf67a41ef8d3d0ab205b82cc61e7780f4cf3e72504b6d24f6e':
    raise RuntimeError('journal changed since head review')
if (repo / mail).exists():
    raise RuntimeError('consumed mail reappeared')
base = git('show', f'HEAD:{journal}').stdout
incoming = git('show', f'origin/main:{journal}').stdout
if sha(incoming) != '994b2aa0ad3fdca82a7d1791dbf5e8e91cc5ae9745ca717fbc5025bfe44876c4':
    raise RuntimeError('incoming journal changed since review')
local_add = added_lines(base, local)
if len(local_add) != 15:
    raise RuntimeError(f'local note has {len(local_add)} lines, expected 15')
backup_root.mkdir(parents=True, exist_ok=True)
backup = backup_root / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup.mkdir(mode=0o700)
(backup / 'journal.local').write_bytes(local)
os.chmod(backup / 'journal.local', stat.S_IMODE((repo / journal).stat().st_mode))
(backup / 'journal.base').write_bytes(base)
(backup / 'journal.incoming').write_bytes(incoming)
(backup / 'mail.original').write_bytes(git('show', f'HEAD:{mail}').stdout)
(backup / 'local.diff.binary').write_bytes(git('diff', '--binary', '--', *paths).stdout)
merge = subprocess.run(['git', 'merge-file', '-p', str(backup / 'journal.local'),
                        str(backup / 'journal.base'), str(backup / 'journal.incoming')],
                       capture_output=True)
if merge.returncode != 0:
    raise RuntimeError(f'journal scratch merge returned {merge.returncode}')
merged = merge.stdout
(backup / 'journal.expected-merged').write_bytes(merged)
merged_add = added_lines(incoming, merged)
if merged_add != local_add or sha(merged) != '358b853d1a24dfd0c872bd304e1575629b51eaa126208d97d706f27107173bba':
    raise RuntimeError('merged result differs from reviewed 15-line insertion')
metadata = {
    'backup': str(backup), 'original_head': head, 'incoming_head': origin,
    'index_tree': git('write-tree').stdout.decode().strip(),
    'journal_local_sha256': sha(local), 'journal_mode': format(stat.S_IMODE((repo / journal).stat().st_mode), '04o'),
    'mail_absent': True, 'mail_original_sha256': sha((backup / 'mail.original').read_bytes()),
    'binary_diff_sha256': sha((backup / 'local.diff.binary').read_bytes()),
    'merged_journal_sha256': sha(merged), 'local_note_lines': len(local_add),
    'tracked_status': status,
}
(backup / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(json.dumps(metadata, indent=2))
