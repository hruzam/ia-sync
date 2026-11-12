#!/usr/bin/env python3
"""Read-only seven-file peer source/live metadata; no file contents are printed."""

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


home = Path("/home/hruzam")
repo = home / "ia-sync"
live = home / ".config/zsh"
files = (
    "system/tailscale.zsh", "system/keyboard.zsh", "registries/projects.json",
    "registries/ai.json", "registries/gen-temple-map.sh",
    "ai/temple-project-map.zsh", "ai/rc.sh",
)


def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metadata(path):
    if not path.exists():
        return {"exists": False}
    return {
        "exists": True,
        "sha256": digest(path.read_bytes()),
        "mode": format(stat.S_IMODE(path.stat().st_mode), "04o"),
    }


def symlink_components(path):
    current = Path(path.anchor)
    found = []
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            found.append(str(current))
    return found


rows = []
for relative in files:
    source = repo / "zsh" / relative
    destination = live / relative
    rows.append({
        "relative": relative,
        "source": metadata(source),
        "source_head_sha256": digest(git("show", f"HEAD:zsh/{relative}")),
        "target_origin_sha256": digest(git("show", f"origin/main:zsh/{relative}")),
        "live": metadata(destination),
        "source_symlinks": symlink_components(source),
        "live_symlinks": symlink_components(destination),
    })

old_ai = json.loads((live / "registries/ai.json").read_text())
new_projects = json.loads(git("show", "origin/main:zsh/registries/projects.json"))
fallback = old_ai["remote-control"]["projects"]["nabla-lab"].get("path")
other = {}
for relative in (".config/zsh/config.zsh", ".zshrc", ".config/zsh/.config/tailnet.access-controls.json"):
    other[relative] = metadata(home / relative)

print(json.dumps({
    "hostname": subprocess.check_output(["hostname", "-s"], text=True).strip(),
    "head": git("rev-parse", "HEAD").decode().strip(),
    "origin_main": git("rev-parse", "origin/main").decode().strip(),
    "files": rows,
    "old_nabla_lab_fallback": fallback,
    "new_nabla_lab_path": new_projects["projects"]["nabla-lab"],
    "fallback_code_present": "projects[$p].path" in (live / "ai/rc.sh").read_text(),
    "protected_live": other,
}, indent=2))
