#!/usr/bin/env python3
"""Remove only the fixture trust entry accidentally persisted by the B0 TUI."""

import os
import stat
import tempfile
from pathlib import Path


path = Path("/home/hruzam/.codex/config.toml")
block = (
    '\n[projects."/tmp/muticula-b0-codex-ki5dIN/fixture"]\n'
    'trust_level = "trusted"\n'
)
text = path.read_text(encoding="utf-8")
if text.count(block) != 1:
    raise SystemExit(f"refusing rollback: expected one exact block, found {text.count(block)}")
updated = text.replace(block, "", 1)
mode = stat.S_IMODE(path.stat().st_mode)
fd, temp_name = tempfile.mkstemp(prefix="config.toml.muticula-rollback.", dir=path.parent)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temp_name, mode)
    os.replace(temp_name, path)
finally:
    if os.path.exists(temp_name):
        os.unlink(temp_name)
print("removed exactly one muticula fixture trust block")
