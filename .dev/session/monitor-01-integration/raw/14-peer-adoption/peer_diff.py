#!/usr/bin/env python3
"""Read-only bounded diff of allowed live files against peer HEAD source."""

import difflib
import subprocess
from pathlib import Path


repo = Path("/home/hruzam/ia-sync")
live = Path("/home/hruzam/.config/zsh")
files = (
    "system/tailscale.zsh", "system/keyboard.zsh", "registries/projects.json",
    "registries/ai.json", "registries/gen-temple-map.sh",
    "ai/temple-project-map.zsh", "ai/rc.sh",
)
for relative in files:
    old = subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:zsh/{relative}"], text=True)
    current = (live / relative).read_text()
    lines = list(difflib.unified_diff(old.splitlines(), current.splitlines(),
                                      fromfile=f"HEAD:zsh/{relative}",
                                      tofile=f"live:{relative}", lineterm="", n=1))
    if lines:
        print("\n".join(lines))
