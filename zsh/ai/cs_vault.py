"""Shared read-only helpers for the cold-start vault tools.

Used by cs-palette.py (explorer) and cs-manage-palette.py (mover backend).
Read-only by design: this module never writes or moves a file — folder = state
(raw.guides/cold-start-card/GUIDE.md), and the actual mv lives in the zsh
wrappers (cs-palette.zsh / temple-cs-manage.zsh) so the vault path resolution
(temple-project-map cascade) and the filesystem mutation both stay out of the
curses layer. Parses ONLY the shared frontmatter contract (flat keys) — the
GUIDE is schema-of-record; Codex evidence keys below the shared block are
never surfaced here.
"""

import os

STATE_DIRS = {"card": "card", "routine": "routines", "archive": "archive"}


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
