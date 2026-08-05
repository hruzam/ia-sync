#!/usr/bin/env python3
"""
palette-help.py — generic live help-renderer for a keyboard.zsh control panel.

Proof-of-mechanism for the A' (palette v2) "frontmatter projection" design:
the alias line's trailing doc-comment is the single source of help text.
This renders the SAME lines palette-map-gen.py already harvests into
palette.map — the `just --list` model, read live at call time, no sidecar,
no persisted artifact.

STDLIB ONLY. Read-only. No network, no subprocess.

Usage:
    python3 palette-help.py <path-to-keyboard.zsh> [--section <name>]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Identical in shape to palette-map-gen.py's ALIAS_RE — name + sq/dq/bare
# body + optional trailing "# comment". A shared single definition is the
# point; kept here as a literal copy (not imported) so this script stays a
# standalone, dependency-free renderer.
ALIAS_RE = re.compile(
    r"""^\s*alias\s+
        (?P<name>[A-Za-z0-9_-]+)
        =
        (?:
            '(?P<sq>[^']*)'
          | "(?P<dq>[^"]*)"
          | (?P<bare>\S+)
        )
        \s*(?:\#\s*(?P<comment>.*))?\s*$
    """,
    re.VERBOSE,
)

# Section-header comment lines of the form "# ── Tailscale ──────"
SECTION_RE = re.compile(r"^\s*#\s*──\s*(?P<title>.*?)\s*──*\s*$")

NO_HELP_MARKER = "(no help)"


def parse(lines: list[str]) -> list[tuple[str, list[tuple[str, str | None]]]]:
    """
    Returns an ordered list of (section_title, [(command, help_or_None), ...]).
    Aliases appearing before any section header are grouped under "" (no title).
    """
    sections: list[tuple[str, list[tuple[str, str | None]]]] = []
    current: list[tuple[str, str | None]] = []
    current_title = ""
    started = False

    for line in lines:
        sm = SECTION_RE.match(line)
        if sm:
            if started or current:
                sections.append((current_title, current))
            current_title = sm.group("title")
            current = []
            started = True
            continue

        am = ALIAS_RE.match(line)
        if am:
            name = am.group("name")
            comment = am.group("comment")
            current.append((name, comment.strip() if comment else None))

    if started or current:
        sections.append((current_title, current))

    return sections


def render(sections: list[tuple[str, list[tuple[str, str | None]]]],
           section_filter: str | None) -> str:
    if section_filter is not None:
        sections = [s for s in sections if s[0] == section_filter]

    out_lines: list[str] = []
    first = True
    for title, rows in sections:
        if not rows:
            continue
        if not first:
            out_lines.append("")
        first = False
        if title:
            out_lines.append(title)

        width = max((len(cmd) for cmd, _ in rows), default=0)
        for cmd, help_str in rows:
            pad = " " * ((width - len(cmd)) + 2)
            help_text = help_str if help_str else NO_HELP_MARKER
            out_lines.append(f"  {cmd}{pad}{help_text}")

    return "\n".join(out_lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generic live help-renderer for a keyboard.zsh control panel."
    )
    parser.add_argument("path", type=Path, help="path to a keyboard.zsh file")
    parser.add_argument("--section", default=None,
                         help="filter to a single section title")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2

    try:
        text = args.path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
        return 2

    if not text.strip():
        print(f"error: file is empty: {args.path}", file=sys.stderr)
        return 2

    lines = text.splitlines()
    sections = parse(lines)
    output = render(sections, args.section)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
