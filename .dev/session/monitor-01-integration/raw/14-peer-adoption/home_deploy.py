import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from datetime import datetime, timezone

home = Path('/home/hruzam')
source = home / 'ia-sync/zsh'
live = home / '.config/zsh'
backup_root = home / '.local/state/ia-sync/backups/monitor-01-cycle14'
files = [
    'system/tailscale.zsh',
    'system/keyboard.zsh',
    'registries/projects.json',
    'registries/ai.json',
    'registries/gen-temple-map.sh',
    'ai/temple-project-map.zsh',
    'ai/rc.sh',
]
target_hashes = [
    'b567e698174c80f81f7bd2498c151f91c599287ed1457763fb8fcd77564eda50',
    'dffd687d66292a3c254296137351356f4f42c2afee9971d63fe4eec106859f7d',
    '6f653dcade66d7b7fb92fc6592879b3baccef51e892ff0f2209ae67c5891222a',
    '3e1ada2e370c3e9bf9270ff927b33e6fb4924fe180fc1ec8446aebdc3c21cfb7',
    '94475a141f282a406b9c571a43234cce69bdb70ea95be6d6465623d5fdda9067',
    '859c9304a7323a3c71662d2e249da5f6da9b8b36154d687d417cd3e80af0ed37',
    '676beac171794e53047c1e2248d1ba53d93ea7d5162b6fc4290ca0663a9500d9',
]
old_hashes = [
    'b34fd852306dd20323cd0c923139b06e0e8645466d4f2736ffc0d88499d3b372',
    '339c1beb193c37ed6c06ca2ed8b2c9a7796e51e05c041c32c0006e6196784cec',
    'a87126ca103231e44f59acfc1cd4cfec86dd88948c5408157454416fe3071e8d',
    'c4b4ea1a2dbf040329d9fb13e96ca8b455d767e5ef8feaf22d6a6ce1223e8a8f',
    'c8f8ab542cd4a9a66d8acdee91f689b330e4d592de037d87a8e741cc1814dd5e',
    'ed7f53ed6a0e079684bfdc0aed1985990d5ff8b47a457c713f34f017a982da0f',
    'ef67eb901fc6d67068785a4b568b4a7c350c5a1309d2406f23d8f7fed9bb1f5d',
]
old_modes = ['0644', '0644', '0644', '0644', '0755', '0600', '0755']
protected = {
    '.config/zsh/config.zsh': 'd406192d5ecdec2737d2e1de27be545375ef9a2397dcb2b735be57c5bfe2605c',
    '.zshrc': 'be95e117045165313886409342cb0a0d5707db78cec6bf429bb74d312ec73cd8',
    '.config/zsh/.config/tailnet.access-controls.json': 'd6a208086517c0bc921d846a7166c417ef8628b12fb9d4d2c5e5e396c57d530d',
}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def mode(p):
    return format(stat.S_IMODE(p.stat().st_mode), '04o')

def no_symlinks(p):
    for q in (p, *p.parents):
        if q.is_symlink():
            raise RuntimeError(f'symlink component: {q}')

def assert_state(base, hashes, modes=None):
    for i, rel in enumerate(files):
        p = base / rel
        no_symlinks(p)
        if not p.is_file() or digest(p) != hashes[i]:
            raise RuntimeError(f'byte mismatch: {p}')
        if modes and mode(p) != modes[i]:
            raise RuntimeError(f'mode mismatch: {p}')

def assert_protected():
    for rel, expected in protected.items():
        p = home / rel
        no_symlinks(p)
        if digest(p) != expected:
            raise RuntimeError(f'protected file changed: {p}')

def rsync(src, dst, dry=False):
    cmd = ['rsync', '-aOiv', '--relative', '--files-from=-']
    if dry:
        cmd.append('--dry-run')
    cmd.extend([str(src) + '/', str(dst) + '/'])
    result = subprocess.run(cmd, input='\n'.join(files) + '\n', text=True,
                            capture_output=True, check=True)
    return result.stdout.strip()

assert_state(source, target_hashes, ['0644', '0644', '0644', '0644', '0755', '0644', '0755'])
assert_state(live, old_hashes, old_modes)
assert_protected()
backup_root.mkdir(parents=True, exist_ok=True)
backup = backup_root / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup.mkdir(mode=0o700)
backup_changes = rsync(live, backup)
assert_state(backup, old_hashes, old_modes)
dry_run = rsync(source, live, dry=True)
assert_state(live, old_hashes, old_modes)
assert_protected()
copy_changes = rsync(source, live)
os.chmod(live / 'ai/temple-project-map.zsh', 0o600)
assert_state(live, target_hashes, old_modes)
assert_protected()
print(json.dumps({
    'backup': str(backup),
    'backup_changes': backup_changes.splitlines(),
    'dry_run': dry_run.splitlines(),
    'copy_changes': copy_changes.splitlines(),
    'target_hashes_verified': True,
    'old_modes_preserved': True,
    'protected_hashes_preserved': True,
}, indent=2))
