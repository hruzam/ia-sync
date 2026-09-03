"""Shared read/write helpers for the cold-start vault tools.

Used by cs-palette.py (explorer + mover) and temple-cs-manage.zsh (CLI flags).
Read helpers are the original contract; move_card() was added when cs-palette.py
gained move capability (merged from cs-manage-palette.py, 2026-09-03).

Folder = state discipline (raw.guides/cold-start-card/GUIDE.md): the physical
folder a card lives in IS its state. move_card() does a plain os.rename() —
no frontmatter rewriting, ever.
"""

import os

STATE_DIRS = {"card": "card", "routines": "routines", "archive": "archive"}


def list_state(vault_root, state):
    """Return [(filename, fullpath, mtime)] for .md files directly under
    vault_root/<state-dir>. Missing dir / unreadable entries degrade to []."""
    subdir = STATE_DIRS[state]
    dir_path = os.path.join(vault_root, subdir)
    rows = []
    try:
        entries = os.listdir(dir_path)
    except OSError:
        return rows
    for name in entries:
        if not name.endswith(".md"):
            continue
        full = os.path.join(dir_path, name)
        if not os.path.isfile(full):
            continue
        try:
            mtime = os.path.getmtime(full)
        except OSError:
            mtime = 0
        rows.append((name, full, mtime))
    return rows


def move_card(vault_root, fullpath, dest_state):
    """Move a card from its current location to the dest_state directory.

    dest_state is a STATE_DIRS key: 'card', 'routines', or 'archive'.
    Returns (new_fullpath, None) on success; (None, error_str) on failure.
    Never rewrites frontmatter — folder = state discipline.
    """
    dest_dirname = STATE_DIRS.get(dest_state)
    if not dest_dirname:
        return None, f"unknown state: {dest_state!r}"
    dest_dir = os.path.join(vault_root, dest_dirname)
    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.basename(fullpath)
    dest_path = os.path.join(dest_dir, filename)
    if os.path.normpath(fullpath) == os.path.normpath(dest_path):
        return fullpath, None  # already there — not an error
    if os.path.exists(dest_path):
        return None, f"destination already exists: {dest_path}"
    try:
        os.rename(fullpath, dest_path)
        return dest_path, None
    except OSError as error:
        return None, str(error)


def read_frontmatter_block(fullpath):
    """Return the raw frontmatter block (verbatim lines between the --- fences,
    fences excluded) or None if the file has no leading frontmatter (legacy
    card, or an unterminated fence — both degrade to "no frontmatter")."""
    try:
        with open(fullpath, "r", encoding="utf-8") as source:
            lines = source.readlines()
    except OSError:
        return None
    if not lines or lines[0].rstrip("\n") != "---":
        return None
    block = []
    for line in lines[1:]:
        if line.rstrip("\n") == "---":
            return "".join(block)
        block.append(line)
    return None


def parse_flat_keys(frontmatter_text):
    """Extract flat top-level `key: value` pairs from a frontmatter block.
    Skips indented / list-item lines (e.g. `pointers:` sub-bullets) — only the
    shared cross-brand contract's flat keys are tooling-visible by design."""
    keys = {}
    if not frontmatter_text:
        return keys
    for line in frontmatter_text.splitlines():
        if not line or line[0] in (" ", "\t", "-"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key:
            keys[key] = value
    return keys


def first_prompt_block(fullpath):
    """Return the content of the first `###### prompt` fenced ```text block in
    the file body, or None if no such block exists."""
    try:
        with open(fullpath, "r", encoding="utf-8") as source:
            text = source.read()
    except OSError:
        return None
    marker = "###### prompt"
    marker_index = text.find(marker)
    if marker_index == -1:
        return None
    after_marker = text[marker_index + len(marker):]
    fence_start = after_marker.find("```text")
    if fence_start == -1:
        return None
    after_fence = after_marker[fence_start + len("```text"):]
    fence_end = after_fence.find("```")
    if fence_end == -1:
        return None
    return after_fence[:fence_end].strip("\n")
