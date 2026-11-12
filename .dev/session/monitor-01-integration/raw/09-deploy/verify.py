#!/usr/bin/env python3
"""Read-only exact-file checks for monitor cycle 09; writes JSON to stdout."""

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


BED = Path(__file__).resolve().parent
SOURCE = Path("/home/hruzam/ia-sync/zsh")
LIVE = Path("/home/hruzam/.config/zsh")
REPO = SOURCE.parent
POLICY = LIVE / ".config/tailnet.access-controls.json"
FILES = (BED / "files.txt").read_text().splitlines()
STAGE = sys.argv[1]
if STAGE not in {"pre", "post"}:
    raise SystemExit("usage: verify.py pre|post")


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metadata(path):
    if not path.exists():
        return {"exists": False}
    mode = stat.S_IMODE(path.stat().st_mode)
    return {"exists": True, "sha256": digest(path.read_bytes()), "mode": format(mode, "04o")}


def no_symlink_components(path):
    part = Path(path.anchor)
    for name in path.parts[1:]:
        part /= name
        if part.is_symlink():
            raise RuntimeError(f"symlink component: {part}")


head = git("rev-parse", "HEAD").decode().strip()
if not head.startswith("d9af9d1"):
    raise RuntimeError(f"unexpected source HEAD: {head}")
if git("status", "--porcelain", "--", *("zsh/" + item for item in FILES)).strip():
    raise RuntimeError("unexpected source edits in allowlist")
rows = []
for relative in FILES:
    if relative.startswith("/") or ".." in Path(relative).parts:
        raise RuntimeError(f"unsafe relative path: {relative}")
    source = SOURCE / relative
    live = LIVE / relative
    no_symlink_components(source)
    no_symlink_components(live)
    if not source.is_file() or (live.exists() and not live.is_file()):
        raise RuntimeError(f"unexpected file type: {relative}")
    source_meta = metadata(source)
    committed = digest(git("show", f"HEAD:zsh/{relative}"))
    baseline = digest(git("show", f"cefe109:zsh/{relative}"))
    if source_meta["sha256"] != committed:
        raise RuntimeError(f"source differs from HEAD: {relative}")
    live_meta = metadata(live)
    if STAGE == "pre" and live_meta["exists"] and live_meta["sha256"] not in {baseline, committed}:
        raise RuntimeError(f"third-state live drift: {relative}")
    if STAGE == "post" and live_meta != source_meta:
        raise RuntimeError(f"live/source mismatch: {relative}: {live_meta} != {source_meta}")
    rows.append({"relative": relative, "source": source_meta, "baseline_sha256": baseline, "live": live_meta})
no_symlink_components(POLICY)
if not POLICY.is_file():
    raise RuntimeError("policy file absent")
result = {"stage": STAGE, "head": head, "policy_sha256": digest(POLICY.read_bytes()), "files": rows}
print(json.dumps(result, indent=2))
