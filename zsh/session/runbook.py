#!/usr/bin/env python3
"""runbook.py — session-scope runbook browser. v0.3 (tree + content pane, 2026-09-10)

Browse .dev/session/ beds: D1 list with gate-state, D2 sectioned view
(STATUS / _bus/ / RUNBOOK / bed-root files / raw/) with foldable groups,
internal reader, print-buffer pane, and base colors.

Invoke via:  python3 runbook.py [--root <.dev/session path>]
Root resolution: --root > $RB_ROOT (config default bench) > walk-up.

v0.3 layout: LEFT = one tree (beds → STATUS/_bus/RUNBOOK/files/raw branches),
RIGHT = pure content pane (bed node → cold-start overview; file → document;
group → listing). Fixed strip on top of content: next: (+ raw in_flight when
flagged). Narrow terminals (<60 cols): the focused pane takes the whole screen.
Place memory (selected node, expanded branches) is host-local UI state.

Keybinds:
  ↑ ↓ PgUp/PgDn move tree cursor / scroll content (by focus; g/G in content)
  → ←           expand / collapse (← also: to parent, or content → tree)
  Enter / Space toggle branch · on a file: focus the content pane
  Tab           switch pane tree ↔ content
  J / K         jump between beds
  1–5           jump to bed part (STATUS / _bus / RUNBOOK / files / raw)
  F             fold/unfold the selected bed
  e             open in $EDITOR (GUI editors detach; TUI stays)
  y             copy selection path to clipboard (fallback: print buffer)
  B             presence board modal · m / u attach / detach selected bed
  p             collect path into print buffer · b toggle buffer pane
  ? h           open the named-scope help navigator
  H             hide / show the bottom hint belt (remembered)
  r             reload all beds · q / Esc quit (buffer prints to scroll-back)

Board CLI (same grammar core as the TUI):
  runbook.py board list
  runbook.py board mark --bed <path> [--workspace <path>] [--seat S] [--note N]
  runbook.py board unmark [--id ID | --bed <path>]
Contract: ~/reposoma/raw.guides/runbook/res/presence-board.md — advisory only.
"""

import argparse
import curses
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# ESCDELAY must be set before curses.initscr(). 25 ms split arrow-key escape
# sequences under terminal multiplexers, making an arrow look like Esc/close.
os.environ.setdefault("ESCDELAY", "250")


# ── Small helpers (cs-palette pattern, stdlib only) ──────────────────────────

def clipped(value, width):
    if width <= 0:
        return ""
    if len(value) <= width:
        return value
    if width == 1:
        return "…"
    return value[: width - 1] + "…"


def safe_add(screen, row, col, value, attr=0, width=None):
    h, w = screen.getmaxyx()
    if row < 0 or row >= h or col < 0 or col >= w:
        return
    avail = w - col
    if width is not None:
        avail = min(avail, max(0, width))
    if avail <= 0:
        return
    try:
        screen.addnstr(row, col, value, avail, attr)
    except curses.error:
        pass


def wrap_line(raw, width):
    """WRITELN law: wrap, never clip body text. No hyphen breaks; long words wrap."""
    if not raw.strip():
        return [""]
    return textwrap.wrap(
        raw,
        width=max(1, width),
        break_on_hyphens=False,
        break_long_words=True,
    ) or [""]


# ── Colors ───────────────────────────────────────────────────────────────────

CP = {}  # name -> curses attr (color_pair); stays {} when colors unavailable


def init_colors():
    if not curses.has_colors():
        return
    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        return
    palette_pairs = [
        ("header", curses.COLOR_CYAN),     # section headers, md headings
        ("accent", curses.COLOR_YELLOW),   # next: strip, json, buffer
        ("good", curses.COLOR_GREEN),      # → state, done boxes, sh/py/zsh
        ("warn", curses.COLOR_RED),        # ! state
        ("meta", curses.COLOR_MAGENTA),    # yaml, keys
    ]
    for i, (name, fg) in enumerate(palette_pairs, start=1):
        try:
            curses.init_pair(i, fg, -1)
            CP[name] = curses.color_pair(i)
        except curses.error:
            CP[name] = 0


def c(name, extra=0):
    return CP.get(name, 0) | extra


STATE_STYLE = {  # gate state char -> (color name, extra attr)
    "!": ("warn", curses.A_BOLD),
    "→": ("good", 0),
    "·": ("accent", 0),
    "?": (None, curses.A_DIM),
}

EXT_STYLE = {  # file suffix -> (color name, extra attr)
    ".json": ("accent", 0),
    ".yaml": ("meta", 0),
    ".yml": ("meta", 0),
    ".zsh": ("good", 0),
    ".sh": ("good", 0),
    ".py": ("good", 0),
    ".kdl": ("meta", 0),
}


def attr_for_file(path):
    name, extra = EXT_STYLE.get(path.suffix.lower(), (None, 0))
    return c(name, extra) if name else extra


YAML_KEY_RE = re.compile(r"^\s*[\w@`][\w@`_.-]*:(\s|$)")


def md_line_attr(raw, in_fence):
    """Attr for one source line of a document body (markdown-biased)."""
    s = raw.lstrip()
    if s.startswith("```"):
        return curses.A_DIM
    if in_fence:
        if YAML_KEY_RE.match(s):
            return c("meta")
        return 0
    if s.startswith("#"):
        return c("header", curses.A_BOLD)
    if s.startswith("- [x]"):
        return c("good")
    if s.startswith(">"):
        return curses.A_DIM
    if s.startswith("---") and s.strip("- ") == "":
        return curses.A_DIM
    return 0


# ── Frontmatter reader (fenced ```yaml + --- fallback) ───────────────────────

def read_fenced_block(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.search(r"^```ya?ml\s*\n(.*?)^```", text, re.M | re.S)
    if m:
        return m.group(1)
    m = re.search(r"^---\s*\n(.*?)^---", text, re.M | re.S)
    if m:
        return m.group(1)
    return None


BLOCK_SCALAR = re.compile(r"^[>|][+-]?\s*$")


def _collect_block_scalar(lines, key_idx, key_indent, limit=20):
    """Collect a YAML block scalar's continuation lines (>-, >, |, |-, …).
    Returns the folded one-line text (strip display collapses newlines anyway)."""
    parts = []
    for line in lines[key_idx + 1: key_idx + 1 + limit]:
        if not line.strip():
            continue  # paragraph break inside the block — keep folding
        indent = len(line) - len(line.lstrip())
        if indent <= key_indent:
            break  # dedent ends the block
        parts.append(line.strip())
    return " ".join(parts)


def flat_keys(block):
    result = {}
    if not block:
        return result
    lines = block.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)`?(\w[\w_-]*):`?\s*(.*)", line)
        if not m:
            continue
        indent, key, val = len(m.group(1)), m.group(2), m.group(3).strip()
        if BLOCK_SCALAR.match(val):
            val = _collect_block_scalar(lines, i, indent)
        result[key] = val.strip().strip('"').strip("'")
    return result


def extract_next(path):
    """Extract next: from STATUS. Flat key → regex fallback → —."""
    if path is None or not path.is_file():
        return "—"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "—"
    block = read_fenced_block(path)
    if block:
        val = flat_keys(block).get("next", "")
        if val:
            return val
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)`?next:`?\s*(.*)", line)
        if m:
            val = m.group(2).strip()
            if BLOCK_SCALAR.match(val):
                val = _collect_block_scalar(lines, i, len(m.group(1)))
            val = val.strip().strip('"').strip("'")
            if val:
                return val
    return "—"


def _inflight_idle(raw):
    return raw is None or raw.lower() in ("none", "", "false", "no")


def extract_in_flight_raw(path):
    """Raw in_flight: value, or None. Reader stays strict: only canonical
    `none` (or empty/false/no) is idle — never guesses at prefixes. The raw
    value is displayed so a human sees WHY a bed is flagged."""
    if path is None or not path.is_file():
        return None
    block = read_fenced_block(path)
    if not block:
        return None
    return flat_keys(block).get("in_flight") or None


# ── Bed discovery ─────────────────────────────────────────────────────────────

def find_root(explicit):
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_dir() else None
    env = os.environ.get("RB_ROOT")
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".dev" / "session"
        if candidate.is_dir() and candidate.parent.name == ".dev":
            return candidate
    return None


def find_status(bed):
    for name in ("STATUS.md", "status.md", "Status.md"):
        p = bed / name
        if p.is_file():
            return p
    return None


def find_runbook(bed):
    for name in ("RUNBOOK.md", "runbook.md"):
        p = bed / name
        if p.is_file():
            return p
    return None


def bed_state(rb_path, st_path):
    if rb_path is None:
        return "?"
    if st_path is None:
        return "·"
    if not _inflight_idle(extract_in_flight_raw(st_path)):
        return "!"
    return "→"


def load_beds(root):
    beds = []
    try:
        children = sorted(root.iterdir())
    except OSError:
        return beds
    for child in children:
        if not child.is_dir() or child.name.startswith("."):
            continue
        rb = find_runbook(child)
        st = find_status(child)
        drift = "~" if (st and st.name != "STATUS.md") else ""
        beds.append({
            "path": child,
            "slug": child.name + drift,
            "state": bed_state(rb, st),
            "status_path": st,
            "runbook_path": rb,
            "next_line": extract_next(st),
            "in_flight_raw": extract_in_flight_raw(st),
        })
    return beds


# ── Document rendering (wrapped lines with per-line attrs) ───────────────────

def render_file_lines(path, width):
    """Wrapped (text, attr) tuples for a document body. Fence-state aware."""
    if path is None or not path.is_file():
        return [("—", curses.A_DIM)]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [("(read error)", c("warn"))]
    out = []
    in_fence = False
    for raw in text.splitlines():
        attr = md_line_attr(raw, in_fence)
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
        for piece in wrap_line(raw, width):
            out.append((piece, attr))
    return out or [("", 0)]


def list_dir(path):
    if path is None or not path.is_dir():
        return []
    try:
        return sorted([p for p in path.iterdir() if p.is_file()], key=lambda p: p.name)
    except OSError:
        return []


def bed_root_items(bed):
    exclude = {"RUNBOOK.md", "runbook.md", "STATUS.md", "status.md", "Status.md"}
    try:
        return sorted(
            [p for p in bed.iterdir()
             if p.is_file() and p.name not in exclude and not p.name.startswith(".")],
            key=lambda p: p.name,
        )
    except OSError:
        return []


# ── Cold-start cards — the entrance into live sessions ──────────────────────
# One-authority law (cold-start GUIDE): the card is a TRANSFER POINTER, never a
# second doing-state. This client only reads: opening a card never archives it,
# never launches anything. Folder = state: card/ = live · routines/ = recurring
# · archive/ = drained. A card whose target is not under this root is "missing
# here" — elsewhere, not finished.

def cs_vault_dir():
    return Path(os.environ.get("RB_CS_VAULT", "~/reposoma/_cold-start")).expanduser()


CS_STATES = (("card", "live"), ("routines", "routine"), ("archive", "archived"))
CS_BADGE = {"live": "CS", "routine": "RT", "archived": "AR"}


def load_cs_cards():
    """All vault cards. {"path", "state", "targets": [expanded Paths]} — targets
    from runbook:/root: keys and ~-anchored pointers: list items (tolerant
    matcher: cards written by different seats point differently)."""
    out = []
    for sub, state in CS_STATES:
        d = cs_vault_dir() / sub
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            block = read_fenced_block(p) or ""
            targets = set()
            fk = flat_keys(block)
            for key in ("runbook", "root"):
                v = fk.get(key, "")
                if v.startswith("~"):
                    targets.add(v)
            for m in re.finditer(r"^\s*-\s+(~/[^\s]+)", block, re.M):
                targets.add(m.group(1))
            # umbrella + order keys: frontmatter preferred, filename-law fallback
            stem = re.sub(r"^(CS|RT)\.", "", p.name[:-3])
            dm = re.search(r"\.(\d{4}-\d{2}-\d{2})$", stem)
            fdate = dm.group(1) if dm else ""
            slug = stem[: -11] if dm else stem
            out.append({"path": p, "state": state,
                        "targets": [Path(os.path.expanduser(t)) for t in targets],
                        "project": fk.get("project") or re.split(r"[-.]", slug)[0],
                        "date": fk.get("date") or fdate,
                        "resume": fk.get("resume", "")})
    return out


def card_matches_bed(card, bed_path):
    """Attached iff any card pointer equals the bed dir or lies inside it."""
    b = str(bed_path)
    for t in card["targets"]:
        s = str(t)
        if s == b or s.startswith(b + "/"):
            return True
    return False


def card_attr(state):
    return {"live": c("accent"), "routine": c("meta"),
            "archived": curses.A_DIM}.get(state, 0)


def archive_card(card):
    """The drain move (Cinderella lifecycle): consumed card → archive/.
    Explicit operator act only — never automatic. Reversible by mv back."""
    if card["state"] == "routine":
        raise SystemExit("routines never archive (vault law)")
    if card["state"] == "archived":
        raise SystemExit("already archived")
    dst_dir = cs_vault_dir() / "archive"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / card["path"].name
    if dst.exists():
        raise SystemExit(f"archive/ already holds {dst.name} — resolve by hand")
    card["path"].rename(dst)
    return dst


# ── Tree model (v0.3) — left pane = one tree, right pane = pure content ──────
#
# Node: {"kind": "bed"|"group"|"file"|"info", "key", "label", "attr",
#        "path", "bed", "depth", "expandable"}
# Keys are stable strings ("<slug>", "<slug>/bus", "<slug>/bus/<file>") — they
# drive the expanded-set and host-local place memory.

BED_PARTS = ["status", "bus", "runbook", "files", "raw"]  # 1–5 jump order


def group_files(bed, part):
    if part == "bus":
        return list_dir(bed["path"] / "_bus")
    if part == "raw":
        return list_dir(bed["path"] / "raw")
    if part == "files":
        return bed_root_items(bed["path"])
    return []


def bed_children(bed):
    """(kind, part, label, path) for an expanded bed — STATUS · _bus/ · RUNBOOK
    · bed files · raw/. Absence renders dim info, never hidden (gap = signal)."""
    st, rb = bed["status_path"], bed["runbook_path"]
    return [
        ("file", "status", st.name, st) if st else ("info", "status", "no STATUS", None),
        ("group", "bus", "_bus/", bed["path"] / "_bus"),
        ("file", "runbook", rb.name, rb) if rb else ("info", "runbook", "no RUNBOOK", None),
        ("group", "files", "bed files", bed["path"]),
        ("group", "raw", "raw/", bed["path"] / "raw"),
    ]


def build_tree(beds, expanded, cards=None):
    """Visible tree nodes in draw order. Twig markers baked into labels."""
    nodes = []
    for bed in beds:
        bkey = bed["slug"]
        twig = "▾" if bkey in expanded else "▸"
        # badge slot BEFORE the name — always visible even when the slug clips
        mark = "●" if bed.get("marked") else " "
        cname, extra = STATE_STYLE.get(bed["state"], (None, 0))
        nodes.append({"kind": "bed", "key": bkey,
                      "label": f"{twig} [{bed['state']}]{mark} {bed['slug']}",
                      "attr": (c(cname, extra) if cname else extra),
                      "path": bed["path"], "bed": bed, "depth": 0, "expandable": True})
        if bkey not in expanded:
            continue
        for kind, part, label, path in bed_children(bed):
            gkey = f"{bkey}/{part}"
            if kind == "group":
                files = group_files(bed, part)
                gtwig = "▾" if gkey in expanded else "▸"
                nodes.append({"kind": "group", "key": gkey,
                              "label": f"{gtwig} {label} ({len(files)})",
                              "attr": c("header"), "path": path, "bed": bed,
                              "depth": 1, "expandable": True})
                if gkey in expanded:
                    for f in files:
                        nodes.append({"kind": "file", "key": f"{gkey}/{f.name}",
                                      "label": f.name, "attr": attr_for_file(f),
                                      "path": f, "bed": bed, "depth": 2,
                                      "expandable": False})
            elif kind == "file":
                nodes.append({"kind": "file", "key": gkey, "label": label,
                              "attr": attr_for_file(path), "path": path,
                              "bed": bed, "depth": 1, "expandable": False})
            else:
                nodes.append({"kind": "info", "key": gkey, "label": label,
                              "attr": curses.A_DIM, "path": None, "bed": bed,
                              "depth": 1, "expandable": False})
        # cs cards matched to this bed (live + routines; archive stays in vault)
        if cards:
            matched = [cd for cd in cards if cd["state"] != "archived"
                       and card_matches_bed(cd, bed["path"])]
            if matched:
                ckey = f"{bkey}/cs"
                ctwig = "▾" if ckey in expanded else "▸"
                nodes.append({"kind": "csgroup", "key": ckey,
                              "label": f"{ctwig} cs cards ({len(matched)})",
                              "attr": c("accent"), "path": None, "bed": bed,
                              "depth": 1, "expandable": True, "cards": matched})
                if ckey in expanded:
                    for cd in matched:
                        nodes.append({"kind": "card", "key": f"{ckey}/{cd['path'].name}",
                                      "label": f"{CS_BADGE[cd['state']]} {cd['path'].name}",
                                      "attr": card_attr(cd["state"]), "path": cd["path"],
                                      "bed": bed, "depth": 2, "expandable": False,
                                      "card": cd})

    # vault node — the entrance: every card, with its landing when one exists here
    if cards:
        counts = {s: sum(1 for cd in cards if cd["state"] == s)
                  for s in ("live", "routine", "archived")}
        vtwig = "▾" if "_cold-start" in expanded else "▸"
        nodes.append({"kind": "vault", "key": "_cold-start",
                      "label": (f"{vtwig} ≋ cold-start ({counts['live']} live · "
                                f"{counts['routine']} rt · {counts['archived']} arch)"),
                      "attr": c("header", curses.A_BOLD), "path": cs_vault_dir(),
                      "bed": None, "depth": 0, "expandable": True})
        if "_cold-start" in expanded:
            # umbrellas: project: key (or filename-slug derivation), newest-first
            groups = {}
            for cd in cards:
                groups.setdefault(cd["project"], []).append(cd)

            def newest(proj):
                return max((x["date"] or "") for x in groups[proj])

            for proj in sorted(groups, key=newest, reverse=True):
                grp = sorted(groups[proj], key=lambda x: x["date"] or "",
                             reverse=True)
                gkey = f"_cold-start/{proj}"
                gtwig = "▾" if gkey in expanded else "▸"
                nodes.append({"kind": "csgroup", "key": gkey,
                              "label": f"{gtwig} {proj} ({len(grp)})",
                              "attr": c("header"), "path": None, "bed": None,
                              "depth": 1, "expandable": True, "cards": grp})
                if gkey not in expanded:
                    continue
                for cd in grp:
                    landing = None
                    for bed in beds:
                        if card_matches_bed(cd, bed["path"]):
                            landing = bed
                            break
                    suffix = f" → {landing['slug']}" if landing else ""
                    nodes.append({"kind": "card",
                                  "key": f"{gkey}/{cd['path'].name}",
                                  "label": f"{CS_BADGE[cd['state']]} {cd['path'].name}{suffix}",
                                  "attr": card_attr(cd["state"]), "path": cd["path"],
                                  "bed": landing, "depth": 2, "expandable": False,
                                  "card": cd})
    return nodes


def render_overview(bed, width, board_recs=None):
    """Right-pane composed view for a bed node — the 30-second cold-start read."""
    lines = []

    def add(text, attr=0):
        for piece in wrap_line(text, width):
            lines.append((piece, attr))

    add(f"{bed['slug']}  [{bed['state']}]", curses.A_BOLD)
    add(str(bed["path"]), curses.A_DIM)
    lines.append(("", 0))
    add(f"next: {bed['next_line']}", c("accent", curses.A_BOLD))
    raw = bed.get("in_flight_raw")
    if not _inflight_idle(raw):
        add(f"in_flight: {raw}", c("warn", curses.A_BOLD))
    lines.append(("", 0))
    recs = board_recs if board_recs is not None else load_board()
    mine = [r for r in recs
            if r["state"] == "valid" and r["fields"]["host"] == local_host()
            and os.path.expanduser(r["fields"]["bed"]) == str(bed["path"])]
    if mine:
        add("board attachments:", c("header", curses.A_BOLD))
        for r in mine:
            f = r["fields"]
            own = "*" if r["own"] else " "
            note = f" · {f['note']}" if f.get("note") else ""
            add(f"  [{age_label(record_age_seconds(f))}]{own}{f['seat']}@{f['host']}{note}",
                c("accent") if r["own"] else 0)
        lines.append(("", 0))
    add(f"_bus/ {len(list_dir(bed['path'] / '_bus'))} · "
        f"files {len(bed_root_items(bed['path']))} · "
        f"raw/ {len(list_dir(bed['path'] / 'raw'))}", curses.A_DIM)
    return lines


BUS_NAME = re.compile(r"^(\d+)\.([A-Za-z0-9_-]+)\.(.+)\.md$")


def render_bus_group(bed, width):
    """Cycle-grouped receipt view (D — display-only). Presence facts only:
    kinds listed per cycle; a verdict FILE existing or not is stated, never
    interpreted (cycle-23 lesson: a filename is not a verdict)."""
    files = list_dir(bed["path"] / "_bus")
    lines = [(f"_bus/ — {len(files)} files", c("header", curses.A_BOLD)), ("", 0)]
    cycles = {}
    other = []
    for f in files:
        m = BUS_NAME.match(f.name)
        if m:
            cycles.setdefault(int(m.group(1)), []).append((m.group(2), m.group(3), f))
        else:
            other.append(f)
    # head-review aid, observational: cycles where a return file exists and no
    # verdict file does. States file-absence only — no pass/fail/await claim.
    open_ret = [n for n, items in sorted(cycles.items())
                if any("return" in k for _, k, _ in items)
                and not any("verdict" in k for _, k, _ in items)]
    if open_ret:
        for piece in wrap_line("return file present · no verdict file: cycle "
                               + ", ".join(str(n) for n in open_ret), width):
            lines.append((piece, c("accent")))
        lines.append(("", 0))
    for n in sorted(cycles, reverse=True):  # newest cycle first — orient order
        lines.append((f"#{n}", c("header", curses.A_BOLD)))
        for seat, kind, f in sorted(cycles[n], key=lambda x: x[2].name):
            for piece in wrap_line(f"  {kind:<9} {seat} · {f.name}", width):
                lines.append((piece, attr_for_file(f)))
    if other:
        lines.append(("unnumbered", curses.A_DIM))
        for f in other:
            lines.append((f"  {f.name}", curses.A_DIM))
    if not files:
        lines.append(("  —", curses.A_DIM))
    return lines


def render_selection(node, width):
    """Right-pane content for the selected tree node. Recomputed per draw —
    small files, and it makes every view live on the 1 s tick."""
    if node is None:
        return [("—", curses.A_DIM)]
    if node["kind"] == "bed":
        return render_overview(node["bed"], width)
    if node["kind"] == "file":
        return render_file_lines(node["path"], width)
    if node["kind"] == "group":
        part = node["key"].rsplit("/", 1)[-1]
        if part == "bus":
            return render_bus_group(node["bed"], width)
        files = group_files(node["bed"], part)
        out = [(node["label"].lstrip("▸▾ "), c("header", curses.A_BOLD)), ("", 0)]
        for f in files:
            out.append((f"  {f.name}", attr_for_file(f)))
        if not files:
            out.append(("  —", curses.A_DIM))
        return out
    if node["kind"] == "card":
        cd = node["card"]
        out = [(f"{cd['state'].upper()} card · {cd['path'].name}",
                c("header", curses.A_BOLD))]
        tb = node.get("bed")
        out.append((f"lands here: {tb['slug']} (Enter jumps to it)" if tb else
                    "target missing here — elsewhere, not finished",
                    c("good") if tb else c("warn")))
        if cd.get("resume"):
            for piece in wrap_line(f"resume: {cd['resume']}", width):
                out.append((piece, c("accent", curses.A_BOLD)))
            out.append(("  (R copies it — paste into your target window)",
                        curses.A_DIM))
        out.append(("", 0))
        return out + render_file_lines(cd["path"], width)
    if node["kind"] == "csgroup":
        out = [(node["label"].lstrip("▸▾ "), c("header", curses.A_BOLD)), ("", 0)]
        for cd in node.get("cards", []):
            d = f" · {cd['date']}" if cd.get("date") else ""
            out.append((f"  {CS_BADGE[cd['state']]} {cd['path'].name}{d}",
                        card_attr(cd["state"])))
        return out
    if node["kind"] == "vault":
        return ([("cold-start vault — the session entrance", c("header", curses.A_BOLD)),
                 (str(node["path"]), curses.A_DIM), ("", 0),
                 ("card/ = live glue · routines/ = recurring · archive/ = drained.", 0),
                 ("Enter on a card jumps to its bed here; a card whose target is", 0),
                 ("not under this root is missing HERE — elsewhere, not finished.", 0),
                 ("Opening a card never archives it and never launches anything.", curses.A_DIM)])
    return [(node["label"], curses.A_DIM)]


# ── Place memory (host-local UI prefs — never project state) ─────────────────

def ui_state_path():
    base = os.environ.get("RB_STATE", "~/.local/state/session-board")
    return Path(base).expanduser() / "ui.json"


def load_ui_state(root):
    import json
    try:
        d = json.loads(ui_state_path().read_text(encoding="utf-8"))
        if d.get("root") == str(root):
            return d
    except (OSError, ValueError):
        pass
    return {}


def save_ui_state(root, selected_key, expanded, tree_right=False, split=40,
                  belt=True):
    import json
    try:
        p = ui_state_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"root": str(root), "selected": selected_key,
                                 "expanded": sorted(expanded),
                                 "tree_right": tree_right,
                                 "split": split, "belt": belt}), encoding="utf-8")
    except OSError:
        pass


# ── Clipboard (relay prep — copying claims nothing: no sent/read/accepted) ───

def copy_to_clipboard(text):
    """Try wayland/X clipboard tools; return tool name, or None → caller falls
    back to the print buffer (terminal-print fallback is always available)."""
    for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"]):
        try:
            p = subprocess.run(cmd, input=text.encode("utf-8"), timeout=3,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if p.returncode == 0:
                return cmd[0]
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None


# ── Mtime tracking ────────────────────────────────────────────────────────────

def mtime_ns(path):
    if path and path.is_file():
        try:
            return path.stat().st_mtime_ns
        except OSError:
            pass
    return 0


def bus_key(bed_path):
    bus = bed_path / "_bus"
    if not bus.is_dir():
        return ()
    try:
        return tuple(sorted(p.name for p in bus.iterdir() if p.is_file()))
    except OSError:
        return ()


# ── Presence board — presence-board/v1 client ────────────────────────────────
# Contract: ~/reposoma/raw.guides/runbook/res/presence-board.md (gaveled 2026-09-09,
# reposoma 0f48dce). Advisory only: records inform, never command or authorize.
# This client renders and writes records; it never auto-deletes, repairs, or
# infers liveness. Own-attachment memory is machine-local state, never synced.

BOARD_KEYS = ["schema", "attachment_id", "seat", "host", "workspace", "bed", "attached_at"]
BOARD_ROW = re.compile(r'^([a-z_]+): "([^"\\\x00-\x1f\x7f]*)"$')
BOARD_TS = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)"
    r"(Z|[+-](?:0\d|1[0-4]):[0-5]\d)$")
BOARD_FILENAME = re.compile(r"^presence\.[0-9a-f]{32}\.md$")


def board_dir():
    return Path(os.environ.get("RB_BOARD", "~/reposoma/_active")).expanduser()


def local_host():
    return os.environ.get("MACHINE_NAME", "") or "unknown"


def own_state_path():
    base = os.environ.get("RB_STATE", "~/.local/state/session-board")
    return Path(base).expanduser() / "own.tsv"


def load_own_ids():
    p = own_state_path()
    out = {}
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                out[parts[0]] = parts[1]  # id -> bed pointer
    return out


def save_own_ids(ids):
    p = own_state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(f"{i}\t{b}\n" for i, b in ids.items()), encoding="utf-8")


def to_tilde(path):
    s = str(Path(path).expanduser().resolve())
    home = str(Path.home())
    return "~" + s[len(home):] if s.startswith(home) else s


def board_now_stamp():
    import datetime
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sanitize_note(note):
    return re.sub(r'[\x00-\x1f\x7f"\\]', "", note or "").strip()


def compose_record(seat, host, workspace, bed, note=""):
    """Compose a byte-valid presence-board/v1 record + its attachment id."""
    import secrets
    aid = secrets.token_hex(16)
    lines = [
        "---",
        'schema: "presence-board/v1"',
        f'attachment_id: "{aid}"',
        f'seat: "{seat}"',
        f'host: "{host}"',
        f'workspace: "{workspace}"',
        f'bed: "{bed}"',
        f'attached_at: "{board_now_stamp()}"',
    ]
    note = sanitize_note(note)
    if note:
        lines.append(f'note: "{note}"')
    lines.append("---")
    return aid, "\n".join(lines) + "\n"


def parse_record(text, fname):
    """Strict presence-board/v1 parse. Returns (state, reason, fields|None).
    state: 'valid' | 'malformed'. Never guesses; reports reason."""
    import datetime
    try:
        if "\r" in text or text.startswith("﻿"):
            return "malformed", "CRLF or BOM framing", None
        if not (text.startswith("---\n") and text.endswith("\n---\n")):
            return "malformed", "frontmatter framing", None
        if "<<<<<<<" in text or ">>>>>>>" in text:
            return "malformed", "conflict markers", None
        rows = [BOARD_ROW.match(l) for l in text[4:-5].split("\n")]
        if not all(rows) or len(rows) not in (7, 8):
            return "malformed", "row grammar or count", None
        names = [r.group(1) for r in rows]
        want = BOARD_KEYS + ["note"] if len(rows) == 8 else BOARD_KEYS
        if names != want:
            return "malformed", "key order or unknown key", None
        v = {r.group(1): r.group(2) for r in rows}
        if v["schema"] != "presence-board/v1":
            return "malformed", "schema", None
        if not re.fullmatch(r"[0-9a-f]{32}", v["attachment_id"]) \
                or fname != f"presence.{v['attachment_id']}.md":
            return "malformed", "filename/ID mismatch", None
        for k in ("seat", "host"):
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", v[k]):
                return "malformed", f"{k} grammar", None
        for k in ("workspace", "bed"):
            if not v[k].startswith("~/"):
                return "malformed", f"{k} pointer", None
        t = BOARD_TS.match(v["attached_at"])
        if not t:
            return "malformed", "timestamp grammar", None
        if t.group(7) not in ("Z",) and t.group(7).startswith(("+14", "-14")) \
                and not t.group(7).endswith(":00"):
            return "malformed", "offset range", None
        try:
            datetime.date(int(t.group(1)), int(t.group(2)), int(t.group(3)))
        except ValueError:
            return "malformed", "calendar date", None
        return "valid", "", v
    except Exception as e:  # never crash a reader on hostile bytes
        return "malformed", f"parse error: {e}", None


def record_age_seconds(fields):
    """Seconds since attached_at, or None for unparseable/future (renders unknown)."""
    import datetime
    try:
        dt = datetime.datetime.fromisoformat(fields["attached_at"])
        delta = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
        return None if delta < 0 else delta
    except (ValueError, KeyError):
        return None


def age_label(secs):
    if secs is None:
        return "?"
    if secs < 3600:
        return f"{int(secs // 60)}m"
    if secs < 86400:
        return f"{int(secs // 3600)}h"
    return f"{int(secs // 86400)}d"


def load_board():
    """All records on the board, parsed strictly. Sorted newest-first by name-set."""
    d = board_dir()
    out = []
    if not d.is_dir():
        return out
    own = load_own_ids()
    try:
        files = sorted(p for p in d.iterdir() if p.is_file())
    except OSError:
        return out
    for p in files:
        if not BOARD_FILENAME.match(p.name):
            continue  # foreign files are not records; ignore silently
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            out.append({"state": "malformed", "reason": "unreadable bytes",
                        "path": p, "fields": None, "own": False})
            continue
        state, reason, fields = parse_record(text, p.name)
        aid = fields["attachment_id"] if fields else p.name[len("presence."):-3]
        out.append({"state": state, "reason": reason, "path": p,
                    "fields": fields, "own": aid in own})
    return out


def board_key():
    d = board_dir()
    if not d.is_dir():
        return ()
    try:
        return tuple(sorted(p.name for p in d.iterdir() if p.is_file()))
    except OSError:
        return ()


def board_mark(bed, workspace=None, seat=None, note=""):
    """Attach: exclusive-create one record. Returns (id, path). Raises on failure."""
    bed_p = Path(bed).expanduser()
    if not bed_p.is_dir():
        raise SystemExit(f"rb-mark: bed is not a directory: {bed}")
    if workspace is None:
        # git toplevel of the bed, else the bed's own tree root guess
        import subprocess as sp
        r = sp.run(["git", "-C", str(bed_p), "rev-parse", "--show-toplevel"],
                   capture_output=True, text=True)
        workspace = r.stdout.strip() if r.returncode == 0 else str(bed_p)
    seat = seat or os.environ.get("RB_SEAT", "") or "majkee"
    d = board_dir()
    d.mkdir(parents=True, exist_ok=True)
    for _ in range(3):  # fresh-ID retry per contract
        aid, record = compose_record(seat, local_host(), to_tilde(workspace),
                                     to_tilde(bed_p), note)
        # self-check: never write a contract-invalid record (e.g. a bed outside ~
        # cannot be ~-anchored; bad seat/host grammar; etc.)
        state, reason, _ = parse_record(record, f"presence.{aid}.md")
        if state != "valid":
            raise SystemExit(f"rb-mark: refusing to write invalid record ({reason})")
        target = d / f"presence.{aid}.md"
        try:
            fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            continue  # collision: fresh ID, new filename — never touch the existing
        try:
            os.write(fd, record.encode("utf-8"))  # single write
        finally:
            os.close(fd)
        own = load_own_ids()
        own[aid] = to_tilde(bed_p)
        save_own_ids(own)
        return aid, target
    raise SystemExit("rb-mark: exclusive creation failed 3 times")


def board_unmark(aid=None, bed=None):
    """Detach own record(s). Explicit id, or all own records for a bed pointer.
    Only removes files whose id is in own state — never another owner's record."""
    own = load_own_ids()
    if aid:
        targets = [aid] if aid in own else []
        if not targets:
            raise SystemExit(f"rb-unmark: {aid} is not an own attachment (ownership law)")
    elif bed:
        want = to_tilde(Path(bed).expanduser())
        targets = [i for i, b in own.items() if b == want]
        if not targets:
            raise SystemExit(f"rb-unmark: no own attachment for bed {want}")
    else:
        targets = list(own.keys())
        if not targets:
            raise SystemExit("rb-unmark: no own attachments recorded")
    removed = []
    for i in targets:
        p = board_dir() / f"presence.{i}.md"
        try:
            p.unlink()
        except FileNotFoundError:
            pass  # already swept; still drop from own state
        own.pop(i, None)
        removed.append(i)
    save_own_ids(own)
    return removed


def board_list_plain():
    recs = load_board()
    if not recs:
        print(f"board empty — {board_dir()}")
        return 0
    for r in recs:
        if r["state"] == "valid":
            f = r["fields"]
            mark = "*" if r["own"] else " "
            note = f' · {f.get("note")}' if f.get("note") else ""
            print(f"[{age_label(record_age_seconds(f)):>3}]{mark}{f['seat']}@{f['host']} "
                  f"· {f['bed']}{note}")
        else:
            print(f"[ ! ] malformed: {r['path'].name} — {r['reason']}")
    return 0


# ── Curses escapes ───────────────────────────────────────────────────────────

GUI_EDITORS = {"subl", "code", "kate", "gedit"}  # detach — no curses escape needed


def open_editor(screen, path):
    editor = os.environ.get("EDITOR") or os.environ.get("PREFERRED_EDITOR") or "vi"
    name = os.path.basename(editor.split()[0])
    try:
        if name in GUI_EDITORS:
            subprocess.Popen([editor, str(path)], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"→ {name}: {Path(path).name}"  # informational, TUI stays live
        curses.def_prog_mode()
        curses.endwin()
        try:
            rc = subprocess.call([editor, str(path)])
        finally:
            curses.reset_prog_mode()
            screen.refresh()
        return None if rc == 0 else f"{name} exited {rc}"
    except OSError as e:
        return f"editor error ({name}): {e}"


# ── Board modal (advisory display only — no action derives from what it shows) ─

def board_lines(recs, sel_idx, width):
    """Wrapped display lines grouped by workspace (the natural convergence key —
    sessions sharing a workspace ARE the working group). Grouping is display-only
    and derived — no schema field. Returns (lines, head_line_of_selection)."""
    lines = []
    sel_head = 0
    groups = {}
    invalid = []
    for i, r in enumerate(recs):
        if r["state"] == "valid":
            groups.setdefault(r["fields"]["workspace"], []).append(i)
        else:
            invalid.append(i)

    def emit(text, attr):
        for piece in wrap_line(text, width):
            lines.append((piece, attr))

    for ws in sorted(groups):
        idxs = groups[ws]
        n = len(idxs)
        emit(f"{ws} — {n} session{'s' if n != 1 else ''}",
             c("header", curses.A_BOLD))
        for i in idxs:
            r = recs[i]
            f = r["fields"]
            secs = record_age_seconds(f)
            attr = c("accent") if r["own"] else 0
            if secs is not None and secs > 86400:
                attr |= curses.A_DIM  # display-only staleness, client policy
            if i == sel_idx:
                sel_head = len(lines)
                attr |= curses.A_REVERSE
            own_mark = "*" if r["own"] else " "
            bed_tail = f["bed"].rsplit("/", 1)[-1]
            note = f" · {f['note']}" if f.get("note") else ""
            emit(f"  [{age_label(secs):>3}]{own_mark}{f['seat']}@{f['host']}"
                 f" · {bed_tail}{note}", attr | curses.A_BOLD)
            emit(f"        bed: {f['bed']}", attr)
        lines.append(("", 0))
    if invalid:
        emit("invalid records", c("warn", curses.A_BOLD))
        for i in invalid:
            r = recs[i]
            attr = c("warn") | (curses.A_REVERSE if i == sel_idx else 0)
            if i == sel_idx:
                sel_head = len(lines)
            emit(f"  [ ! ] {r['path'].name} — {r['reason']}", attr)
        lines.append(("", 0))
    if not lines:
        lines = [("— board empty —", curses.A_DIM)]
    return lines, sel_head


def board_view(screen):
    """Row-cursor board. Returns a bed Path to land on (Enter on a valid
    local-host record), else None. Landing is navigation, never an action."""
    sel = 0
    offset = 0
    while True:
        h, w = screen.getmaxyx()
        recs = load_board()  # recomputed per draw → live on the 1s tick
        sel = max(0, min(sel, len(recs) - 1)) if recs else 0
        body_w = max(1, w - 2)
        lines, sel_head = board_lines(recs, sel if recs else -1, body_w)

        body_h = max(1, h - 2)
        if sel_head < offset:  # keep the selected record's head visible
            offset = sel_head
        elif sel_head >= offset + body_h:
            offset = sel_head - body_h + 1
        offset = max(0, min(offset, max(0, len(lines) - body_h)))

        screen.erase()
        title = clipped(f" presence board · {board_dir()} · {len(recs)} records ", w)
        safe_add(screen, 0, 0, title + " " * max(0, w - len(title)),
                 curses.A_REVERSE | curses.A_BOLD, w)
        for i, (text, attr) in enumerate(lines[offset: offset + body_h]):
            safe_add(screen, 1 + i, 1, text, attr, body_w)
        hint = (" ↑↓ record · Enter land on its bed · * own · grouped by workspace · "
                "advisory only · q back ")
        safe_add(screen, h - 1, 0, clipped(hint, w), curses.A_REVERSE, w)
        screen.refresh()

        try:
            key = screen.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            return None
        if key == curses.KEY_UP:
            sel = max(0, sel - 1)
        elif key == curses.KEY_DOWN:
            sel = min(max(0, len(recs) - 1), sel + 1)
        elif key == curses.KEY_PPAGE:
            sel = max(0, sel - 5)
        elif key == curses.KEY_NPAGE:
            sel = min(max(0, len(recs) - 1), sel + 5)
        elif key in ("\n", "\r", curses.KEY_ENTER):
            if recs and recs[sel]["state"] == "valid":
                f = recs[sel]["fields"]
                if f["host"] == local_host():
                    return Path(os.path.expanduser(f["bed"]))
        elif key in ("q", "Q", "\x1b", curses.KEY_LEFT, "B", "b"):
            return None
        elif key == curses.KEY_RESIZE:
            pass


def buffer_view(screen, buffer_lines):
    """Print-buffer maintainer — inspect, remove single lines, clear. Mutates
    the list in place; whatever survives prints to scroll-back at quit."""
    sel = 0
    offset = 0
    while True:
        h, w = screen.getmaxyx()
        sel = max(0, min(sel, len(buffer_lines) - 1)) if buffer_lines else 0
        body_w = max(1, w - 2)

        lines = []
        heads = []
        for i, entry in enumerate(buffer_lines):
            heads.append(len(lines))
            attr = c("accent") | (curses.A_REVERSE if i == sel else 0)
            for piece in wrap_line(f"{i + 1:2d}. {entry}", body_w):
                lines.append((piece, attr))
        if not lines:
            lines = [("— buffer empty —", curses.A_DIM)]

        body_h = max(1, h - 2)
        sel_head = heads[sel] if heads else 0
        if sel_head < offset:
            offset = sel_head
        elif sel_head >= offset + body_h:
            offset = sel_head - body_h + 1
        offset = max(0, min(offset, max(0, len(lines) - body_h)))

        screen.erase()
        title = clipped(f" print buffer · {len(buffer_lines)} lines — survivors print at quit ", w)
        safe_add(screen, 0, 0, title + " " * max(0, w - len(title)),
                 curses.A_REVERSE | curses.A_BOLD, w)
        for i, (text, attr) in enumerate(lines[offset: offset + body_h]):
            safe_add(screen, 1 + i, 1, text, attr, body_w)
        hint = " ↑↓ select · x remove line · X clear all · y copy line · q back "
        safe_add(screen, h - 1, 0, clipped(hint, w), curses.A_REVERSE, w)
        screen.refresh()

        try:
            key = screen.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            return
        if key == curses.KEY_UP:
            sel = max(0, sel - 1)
        elif key == curses.KEY_DOWN:
            sel = min(max(0, len(buffer_lines) - 1), sel + 1)
        elif key in ("x", curses.KEY_DC) and buffer_lines:
            del buffer_lines[sel]
        elif key == "X":
            buffer_lines.clear()
        elif key == "y" and buffer_lines:
            copy_to_clipboard(buffer_lines[sel])
        elif key in ("q", "Q", "\x1b", curses.KEY_LEFT, "P", "b"):
            return
        elif key == curses.KEY_RESIZE:
            pass


def help_dir():
    return Path(__file__).resolve().parent / "help"


def load_help_scopes(root=None):
    """Discover named help scopes from help/<scope>/HELP.md."""
    base = Path(root) if root is not None else help_dir()
    try:
        paths = sorted(base.glob("*/HELP.md"), key=lambda p: p.parent.name.casefold())
    except OSError:
        return []
    return [{"name": path.parent.name, "path": path} for path in paths]


def help_tokens(query):
    """Forgiving case-insensitive AND tokens, with duplicates removed."""
    return tuple(dict.fromkeys(re.findall(r"\w+", query.casefold())))


def help_line_attr(raw, in_fence, matched=False):
    """Help-only orientation layered on the existing Markdown palette."""
    if matched:
        return c("accent", curses.A_BOLD | curses.A_REVERSE)
    s = raw.lstrip()
    base = md_line_attr(raw, in_fence)
    if s.startswith("```"):
        return base
    if in_fence and s:
        return c("good")
    if re.match(r"(?:[-*+] |\d+[.)] )", s):
        return c("meta")
    if "`" in raw:
        return c("accent")
    return base


def render_help_lines(path, width, tokens=(), landed_line=None):
    """Wrapped help lines as (text, attr, source-line), preserving search landings."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return [("(read error)", c("warn"), 0)]
    out = []
    in_fence = False
    for line_no, raw in enumerate(source, start=1):
        folded = raw.casefold()
        matched = line_no == landed_line or bool(tokens) \
            and all(token in folded for token in tokens)
        attr = help_line_attr(raw, in_fence, matched)
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
        for piece in wrap_line(raw, width):
            out.append((piece, attr, line_no))
    return out or [("", 0, 0)]


def search_help(scopes, query, scope_index=None):
    """Search one/all scopes; every token must occur on the same source line."""
    tokens = help_tokens(query)
    if not tokens:
        return []
    indices = range(len(scopes)) if scope_index is None else (scope_index,)
    results = []
    for idx in indices:
        scope = scopes[idx]
        try:
            source = scope["path"].read_text(
                encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        heading = scope["name"]
        for line_no, raw in enumerate(source, start=1):
            stripped = raw.strip()
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip() or heading
            if all(token in raw.casefold() for token in tokens):
                results.append({"scope": scope["name"], "scope_index": idx,
                                "line": line_no, "heading": heading,
                                "text": stripped or "(blank)"})
    return results


def render_help_results(results, width, selected):
    """Wrapped scope/context result rows plus each result's head-line index."""
    if not results:
        return [("no matches", c("warn", curses.A_BOLD))], []
    lines, heads = [], []
    for idx, result in enumerate(results):
        heads.append(len(lines))
        label = (f"{result['scope']} · {result['heading']} · "
                 f"L{result['line']} · {result['text']}")
        attr = c("accent", curses.A_BOLD) if idx == selected else c("header")
        if idx == selected:
            attr |= curses.A_REVERSE
        lines.extend((piece, attr) for piece in wrap_line(label, width))
    return lines, heads


def help_query(win, label):
    """One-line curses query prompt. Esc cancels without closing help."""
    chars = []
    while True:
        h, w = win.getmaxyx()
        text = f" {label}: {''.join(chars)}"
        safe_add(win, h - 1, 0, " " * w, curses.A_REVERSE, w)
        safe_add(win, h - 1, 0, clipped(text, w), curses.A_REVERSE, w)
        win.refresh()
        try:
            key = win.get_wch()
        except curses.error:
            continue
        if key in ("\n", "\r", curses.KEY_ENTER):
            return "".join(chars).strip()
        if key == "\x1b":
            return None
        if key in ("\b", "\x7f", curses.KEY_BACKSPACE):
            if chars:
                chars.pop()
        elif isinstance(key, str) and key.isprintable():
            chars.append(key)


def help_view(screen, start_theme=0):
    """`?` overlay: dynamic named scopes, responsive tree/content navigation,
    and current/all-scope search. Read-only; outer TUI state is untouched."""
    scopes = load_help_scopes()
    scope_idx = max(0, min(start_theme, len(scopes) - 1)) if scopes else 0
    scope_off = 0
    focus = "scopes"
    off = 0
    results = None
    result_idx = 0
    query = ""
    search_all = False
    active_tokens = ()
    landed_line = None
    win = None
    win_geom = None

    while True:
        h, w = screen.getmaxyx()
        win_h = min(h, max(8, int(h * 0.9)))
        win_w = min(w, max(24, int(w * 0.9)))
        y0 = max(0, (h - win_h) // 2)
        x0 = max(0, (w - win_w) // 2)
        geom = (win_h, win_w, y0, x0)
        if win is None or geom != win_geom:
            win = curses.newwin(*geom)
            win.keypad(True)
            win.timeout(-1)
            win_geom = geom

        inner_w = max(1, win_w - 2)
        body_h = max(0, win_h - 2)
        wide = inner_w >= 58
        max_name = max((len(scope["name"]) for scope in scopes), default=8)
        scope_w = min(max(12, max_name + 4), max(12, inner_w // 3))
        content_col = 1 + scope_w + 1 if wide else 1
        content_w = max(1, win_w - content_col - 1)

        if scopes:
            scope = scopes[scope_idx]
            if results is None:
                content = render_help_lines(scope["path"], content_w,
                                            active_tokens, landed_line)
                if landed_line is not None:
                    off = next((i for i, item in enumerate(content)
                                if item[2] == landed_line), off)
                    landed_line = None
                right_lines = [(text, attr) for text, attr, _ in content]
                heads = []
            else:
                right_lines, heads = render_help_results(results, content_w, result_idx)
                if heads:
                    target = heads[result_idx]
                    if target < off:
                        off = target
                    elif target >= off + max(1, body_h):
                        off = target - max(1, body_h) + 1
        else:
            right_lines, heads = [("no help scopes found", c("warn"))], []

        off = max(0, min(off, max(0, len(right_lines) - body_h)))
        if scope_idx < scope_off:
            scope_off = scope_idx
        elif scope_idx >= scope_off + max(1, body_h):
            scope_off = scope_idx - max(1, body_h) + 1

        win.erase()
        try:
            win.box()
        except curses.error:
            pass
        scope_name = scopes[scope_idx]["name"] if scopes else "empty"
        if results is not None:
            mode = f"search {'all' if search_all else scope_name}: {query}"
        elif query:
            mode = f"{scope_name} · match: {query}"
        else:
            mode = scope_name
        title = clipped(f" help · {mode} ", win_w)
        safe_add(win, 0, max(0, (win_w - len(title)) // 2), title,
                 c("header", curses.A_BOLD), win_w)

        show_scopes = wide or focus == "scopes"
        show_content = wide or focus == "content"
        if show_scopes:
            draw_w = scope_w if wide else inner_w
            for row, (idx, scope) in enumerate(enumerate(
                    scopes[scope_off: scope_off + body_h], start=scope_off), start=1):
                selected = idx == scope_idx
                marker = "▸" if selected else "·"
                attr = c("header", curses.A_BOLD if selected else 0)
                if selected and focus == "scopes":
                    attr |= curses.A_REVERSE
                safe_add(win, row, 1, clipped(f"{marker} {scope['name']}", draw_w),
                         attr, draw_w)
        if wide:
            sep_col = 1 + scope_w
            for row in range(1, 1 + body_h):
                safe_add(win, row, sep_col, "│", curses.A_DIM)
        if show_content:
            draw_col = content_col if wide else 1
            draw_w = content_w if wide else inner_w
            for row, (text, attr) in enumerate(
                    right_lines[off: off + body_h], start=1):
                if focus == "content" and row == 1 and not wide:
                    attr |= curses.A_BOLD
                safe_add(win, row, draw_col, text, attr, draw_w)

        if results is not None:
            hint = " ↑↓ result · Enter land · Ctrl-F scope · F all · ← scopes · q close "
        else:
            hint = " ↑↓ select/scroll · Enter/→ open · Tab focus · Ctrl-F scope · F all · q close "
        safe_add(win, win_h - 1, 0, clipped(hint, win_w), curses.A_REVERSE, win_w)
        win.refresh()

        try:
            key = win.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            return

        if key in ("q", "Q", "\x1b"):
            return
        if key in ("\x06", "F"):
            label = "find all scopes" if key == "F" else "find current scope"
            entered = help_query(win, label)
            if entered:
                query = entered
                search_all = key == "F"
                active_tokens = help_tokens(entered)
                results = search_help(scopes, entered,
                                      None if key == "F" else scope_idx)
                result_idx = 0
                off = 0
                focus = "content"
            continue
        if key == "\t":
            focus = "content" if focus == "scopes" else "scopes"
            continue
        if key in ("[", "]") and scopes:
            step = -1 if key == "[" else 1
            scope_idx = (scope_idx + step) % len(scopes)
            results, query, active_tokens, off = None, "", (), 0
            focus = "content"
            continue

        if focus == "scopes":
            old_scope = scope_idx
            if key == curses.KEY_UP and scopes:
                scope_idx = max(0, scope_idx - 1)
                off = 0
            elif key == curses.KEY_DOWN and scopes:
                scope_idx = min(len(scopes) - 1, scope_idx + 1)
                off = 0
            elif key == curses.KEY_PPAGE and scopes:
                scope_idx = max(0, scope_idx - max(1, body_h))
                off = 0
            elif key == curses.KEY_NPAGE and scopes:
                scope_idx = min(len(scopes) - 1, scope_idx + max(1, body_h))
                off = 0
            elif key in ("\n", "\r", " ", curses.KEY_ENTER, curses.KEY_RIGHT):
                results, query, active_tokens, off = None, "", (), 0
                focus = "content"
            if scope_idx != old_scope and results is None:
                query, active_tokens = "", ()
        elif results is not None:
            if key == curses.KEY_UP and results:
                result_idx = max(0, result_idx - 1)
            elif key == curses.KEY_DOWN and results:
                result_idx = min(len(results) - 1, result_idx + 1)
            elif key == curses.KEY_PPAGE and results:
                result_idx = max(0, result_idx - max(1, body_h // 2))
            elif key == curses.KEY_NPAGE and results:
                result_idx = min(len(results) - 1,
                                 result_idx + max(1, body_h // 2))
            elif key in ("\n", "\r", curses.KEY_ENTER, curses.KEY_RIGHT) and results:
                result = results[result_idx]
                scope_idx = result["scope_index"]
                landed_line = result["line"]
                results = None
                off = 0
            elif key == curses.KEY_LEFT:
                focus = "scopes"
        else:
            if key == curses.KEY_UP:
                off = max(0, off - 1)
            elif key == curses.KEY_DOWN:
                off += 1
            elif key == curses.KEY_PPAGE:
                off = max(0, off - max(1, body_h))
            elif key == curses.KEY_NPAGE:
                off += max(1, body_h)
            elif key == "g":
                off = 0
            elif key == "G":
                off = 10 ** 9
            elif key == curses.KEY_LEFT:
                focus = "scopes"


def refresh_bed_marks(beds):
    """Set bed['marked'] from valid local-host board records. Display-only."""
    pointers = set()
    for r in load_board():
        if r["state"] == "valid" and r["fields"]["host"] == local_host():
            try:
                pointers.add(str(Path(os.path.expanduser(r["fields"]["bed"])).resolve()))
            except OSError:
                pass
    for b in beds:
        try:
            b["marked"] = str(b["path"].resolve()) in pointers
        except OSError:
            b["marked"] = False


# ── Draw (v0.3) ───────────────────────────────────────────────────────────────

BELT_TEXT = " h / ? help · H hide this belt "


def main_heights(height, buffer_lines, show_buffer, belt=False):
    """Bottom rows: optional 1-row hint belt (last row), then an open buffer
    above it. Belt off = main layout reclaims every row (small-screen law)."""
    belt_h = 1 if (belt and height >= 2) else 0
    raw_buf_h = (1 + min(len(buffer_lines), 4)) if (show_buffer and buffer_lines) else 0
    buf_h = min(raw_buf_h, max(0, height - belt_h))
    return max(0, height - buf_h - belt_h), buf_h


def draw(screen, nodes, cursor, tree_off, focus, content, content_off,
         sel_bed, buffer_lines, show_buffer, message, tree_right=False, split=40,
         belt=False):
    screen.erase()
    h, w = screen.getmaxyx()
    body_h, buf_h = main_heights(h, buffer_lines, show_buffer, belt)

    # narrow (<60 cols): the focused pane takes the whole screen — the detail
    # view never disappears with the layout (small-screen law)
    wide = w >= 60
    if wide:
        tree_w = max(1, int(w * split / 100))
        if tree_right:  # mirrored view (v key): content left, tree column right
            tree_col = w - tree_w
            sep_col = tree_col - 1
            content_col = 0
            content_w = max(1, sep_col)
        else:
            tree_col = 0
            sep_col = tree_w
            content_col = tree_w + 1
            content_w = max(1, w - content_col)
        show_tree, show_content = True, True
    else:
        tree_col, content_col, tree_w, content_w = 0, 0, w, w
        sep_col = None
        show_tree = (focus == "tree")
        show_content = not show_tree

    # ── tree (labels left-aligned in the column, depth stairs) ──
    if show_tree:
        for i, n in enumerate(nodes[tree_off: tree_off + body_h]):
            abs_i = tree_off + i
            sel = curses.A_REVERSE if abs_i == cursor else 0
            if focus == "tree" and abs_i == cursor:
                sel |= curses.A_BOLD
            safe_add(screen, i, tree_col,
                     clipped("  " * n["depth"] + n["label"], tree_w),
                     n["attr"] | sel, tree_w)
        if wide and sep_col is not None:
            for row in range(body_h):
                safe_add(screen, row, sep_col, "│", curses.A_DIM)

    # ── content (strip + body) ──
    if show_content:
        col = content_col
        right_w = content_w
        strip_h = 0
        if sel_bed:
            safe_add(screen, 0, col,
                     clipped(f"next: {sel_bed['next_line']}", right_w),
                     c("accent", curses.A_BOLD), right_w)
            strip_h = 1
            raw = sel_bed.get("in_flight_raw")
            if not _inflight_idle(raw):
                safe_add(screen, 1, col,
                         clipped(f"in_flight: {raw}", right_w),
                         c("warn", curses.A_BOLD), right_w)
                strip_h = 2
        c_body = max(0, body_h - strip_h)
        c_off = max(0, min(content_off, max(0, len(content) - c_body)))
        for i, (text, attr) in enumerate(content[c_off: c_off + c_body]):
            safe_add(screen, strip_h + i, col, text, attr, right_w)

    # ── buffer pane ──
    if buf_h:
        brow = body_h
        label = f"─ buffer ({len(buffer_lines)}) — printed at quit "
        safe_add(screen, brow, 0, clipped(label + "─" * max(0, w - len(label)), w),
                 c("accent", curses.A_BOLD), w)
        for i, bl in enumerate(buffer_lines[-(buf_h - 1):]):
            safe_add(screen, brow + 1 + i, 0, clipped("  " + bl, w), c("accent"), w)

    # ── hint belt (last row, H toggles) ──
    if belt and h >= 2:
        safe_add(screen, h - 1, 0, clipped(BELT_TEXT.ljust(w), w), curses.A_REVERSE, w)

    # Feedback overlays row 0 for one tick; it never reserves a row or reflows.
    if message:
        safe_add(screen, 0, 0, clipped(f" {message} ", w),
                 c("accent", curses.A_BOLD | curses.A_REVERSE), w)

    screen.refresh()


# ── TUI loop (v0.3 — tree + content) ─────────────────────────────────────────

def palette(screen, beds, root, tree_right=None):
    """Returns the print buffer (list of str) for scroll-back print at quit."""
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    init_colors()
    screen.keypad(True)
    screen.timeout(1000)  # 1s tick; mtime-gated reload

    ui = load_ui_state(root)
    if tree_right is None:  # CLI flag wins; else remembered preference
        tree_right = bool(ui.get("tree_right", False))
    split = min(80, max(20, int(ui.get("split", 40))))
    belt = bool(ui.get("belt", True))  # hint belt on by default; H toggles, remembered
    arm_archive = None  # two-press confirm for the drain move
    expanded = set(ui.get("expanded", []))
    cursor = 0
    tree_off = 0
    content_off = 0
    focus = "tree"
    message = ""
    buffer_lines = []
    show_buffer = False
    last_sel_key = None
    last_st_mtime = 0
    last_bus_key = ()
    last_board_key = None

    refresh_bed_marks(beds)
    cards = load_cs_cards()
    nodes = build_tree(beds, expanded, cards)
    if ui.get("selected"):
        for i, n in enumerate(nodes):
            if n["key"] == ui["selected"]:
                cursor = i
                break

    def sel_node():
        return nodes[cursor] if (nodes and cursor < len(nodes)) else None

    def content_width():
        _, w = screen.getmaxyx()
        return max(1, w - int(w * split / 100) - 1) if w >= 60 else w

    def body_height():
        h, _ = screen.getmaxyx()
        body_h, _ = main_heights(h, buffer_lines, show_buffer, belt)
        return max(1, body_h)

    def rebuild(keep_key=None):
        nonlocal nodes, cursor
        want = keep_key or (nodes[cursor]["key"] if nodes and cursor < len(nodes) else None)
        nodes = build_tree(beds, expanded, cards)
        if want:
            for i, n in enumerate(nodes):
                if n["key"] == want:
                    cursor = i
                    break
        cursor = max(0, min(cursor, len(nodes) - 1)) if nodes else 0

    def ensure_visible():
        nonlocal tree_off
        bh = body_height()
        if cursor < tree_off:
            tree_off = cursor
        elif cursor >= tree_off + bh:
            tree_off = cursor - bh + 1

    def refresh_bed_truth(bed):
        bed["next_line"] = extract_next(bed["status_path"])
        bed["in_flight_raw"] = extract_in_flight_raw(bed["status_path"])
        bed["state"] = bed_state(bed["runbook_path"], bed["status_path"])

    def jump_bed(direction):
        nonlocal cursor
        i = cursor + direction
        while 0 <= i < len(nodes):
            if nodes[i]["kind"] == "bed":
                cursor = i
                return
            i += direction

    def parent_index():
        n = sel_node()
        if not n or n["depth"] == 0:
            return None
        i = cursor - 1
        while i >= 0:
            if nodes[i]["depth"] < n["depth"]:
                return i
            i -= 1
        return None

    while True:
        node = sel_node()
        bed = node["bed"] if node else None

        # selection change → content restarts at top; bed-tick trackers reset
        key_now = node["key"] if node else None
        if key_now != last_sel_key:
            content_off = 0
            last_sel_key = key_now
            if bed:
                last_st_mtime = mtime_ns(bed["status_path"])
                last_bus_key = bus_key(bed["path"])

        # 1s tick — mtime-gated truth refresh for the selected bed + board
        if bed:
            if mtime_ns(bed["status_path"]) != last_st_mtime \
                    or bus_key(bed["path"]) != last_bus_key:
                refresh_bed_truth(bed)
                last_st_mtime = mtime_ns(bed["status_path"])
                last_bus_key = bus_key(bed["path"])
                rebuild()
        bkey = board_key()
        if bkey != last_board_key:
            refresh_bed_marks(beds)
            last_board_key = bkey
            rebuild()

        content = render_selection(node, content_width())
        draw(screen, nodes, cursor, tree_off, focus, content, content_off,
             bed, buffer_lines, show_buffer, message, tree_right, split, belt)
        message = ""

        try:
            key = screen.get_wch()
        except curses.error:
            continue  # timeout tick
        except KeyboardInterrupt:
            break

        if key != "A":
            arm_archive = None  # any other key disarms the drain confirm
        node = sel_node()
        cur_path = node["path"] if node else None

        if key == curses.KEY_RESIZE:
            ensure_visible()

        elif key == "\t":
            focus = "content" if focus == "tree" else "tree"

        elif key in ("q", "Q", "\x1b"):
            break

        elif key == "r":
            for b in beds:
                refresh_bed_truth(b)
            refresh_bed_marks(beds)
            cards = load_cs_cards()
            rebuild()
            message = "reloaded (beds + board + vault)"

        elif key == "R":  # card's resume: → clipboard; paste into target window
            if node and node["kind"] == "card" and node["card"].get("resume"):
                cmd = node["card"]["resume"]
                tool = copy_to_clipboard(cmd)
                if tool:
                    message = f"resume copied via {tool} — paste into your window"
                else:
                    buffer_lines.append(cmd)
                    show_buffer = True
                    message = "no clipboard — resume buffered"
            elif node and node["kind"] == "card":
                message = "this card has no resume: key"
            else:
                message = "R copies a card's resume: — select a card first"

        elif key == "b":
            show_buffer = not show_buffer

        elif key == "P":
            buffer_view(screen, buffer_lines)
            if not buffer_lines:
                show_buffer = False

        elif key in ("?", "h"):
            help_view(screen)  # overlay only — touches no outer state

        elif key == "H":
            belt = not belt
            ensure_visible()
            message = "hint belt " + ("on" if belt else "off — H brings it back")

        elif key == "v":
            tree_right = not tree_right
            message = "tree column: " + ("right" if tree_right else "left")

        elif key == "<":
            split = max(20, split - 5)
            message = f"tree column {split}%"

        elif key == ">":
            split = min(80, split + 5)
            message = f"tree column {split}%"

        elif key == "A":  # drain move (Cinderella): consumed card → archive/
            if node and node["kind"] == "card":
                if arm_archive == node["key"]:
                    arm_archive = None
                    try:
                        dst = archive_card(node["card"])
                        cards = load_cs_cards()
                        rebuild()
                        message = f"drained → archive/{dst.name} (mv back to restore)"
                    except SystemExit as e:
                        message = str(e)
                else:
                    arm_archive = node["key"]
                    message = "archive this card (drain move)? press A again to confirm"
            else:
                message = "A archives a consumed card — select a card first"

        elif key == "B":
            land = board_view(screen)
            refresh_bed_marks(beds)
            rebuild()
            if land is not None:
                landed = False
                for i2, n2 in enumerate(nodes):
                    if n2["kind"] == "bed" and n2["path"] == land:
                        cursor = i2
                        ensure_visible()
                        message = f"→ landed: {n2['bed']['slug']}"
                        landed = True
                        break
                if not landed:
                    message = "record's bed is not in this tree (other root)"

        elif key == "J":
            jump_bed(+1)
            ensure_visible()

        elif key == "K":
            jump_bed(-1)
            ensure_visible()

        elif isinstance(key, str) and key in "12345" and bed:
            bkey_slug = bed["slug"]
            if bkey_slug not in expanded:
                expanded.add(bkey_slug)
                rebuild(keep_key=f"{bkey_slug}/{BED_PARTS[int(key) - 1]}")
            else:
                rebuild(keep_key=f"{bkey_slug}/{BED_PARTS[int(key) - 1]}")
            ensure_visible()

        elif key == "m" and bed:
            try:
                aid, _ = board_mark(str(bed["path"]))
                refresh_bed_marks(beds)
                rebuild()
                message = f"attached {aid[:8]}… to board"
            except SystemExit as e:
                message = str(e)

        elif key == "u" and bed:
            try:
                removed = board_unmark(bed=str(bed["path"]))
                refresh_bed_marks(beds)
                rebuild()
                message = f"detached {len(removed)} own record(s)"
            except SystemExit as e:
                message = str(e)

        elif key == "p":
            target = str(cur_path) if cur_path else (str(bed["path"]) if bed else "")
            if target:
                buffer_lines.append(target)
                show_buffer = True
                message = f"buffered ({len(buffer_lines)})"

        elif key == "y":
            target = str(cur_path) if cur_path else (str(bed["path"]) if bed else "")
            if target:
                tool = copy_to_clipboard(target)
                if tool:
                    message = f"copied via {tool}"
                else:
                    buffer_lines.append(target)
                    show_buffer = True
                    message = "no clipboard tool — buffered instead"

        elif key == "Y":  # relay prep: exact content, formatting preserved —
            # copying creates no sent/read/accepted claim
            if node and node["kind"] in ("file", "card") \
                    and cur_path and cur_path.is_file():
                try:
                    text = cur_path.read_text(encoding="utf-8", errors="replace")
                except OSError as e:
                    message = f"read error: {e}"
                else:
                    tool = copy_to_clipboard(text)
                    message = (f"content copied via {tool} ({len(text)} chars)"
                               if tool else
                               "no clipboard tool — open with e and copy there")
            else:
                message = "Y copies file content — select a file or card"

        elif key in ("e", "E"):
            target = None
            if node and node["kind"] in ("file", "card"):
                target = cur_path
            elif bed:
                target = bed["runbook_path"] or bed["status_path"]
            if target:
                err = open_editor(screen, target)
                if err:
                    message = err
            else:
                message = "nothing editable here"

        # --- tree focus ---
        elif focus == "tree":
            if key == curses.KEY_UP:
                cursor = max(0, cursor - 1)
                ensure_visible()
            elif key == curses.KEY_DOWN:
                cursor = min(max(0, len(nodes) - 1), cursor + 1)
                ensure_visible()
            elif key == curses.KEY_PPAGE:
                cursor = max(0, cursor - body_height())
                ensure_visible()
            elif key == curses.KEY_NPAGE:
                cursor = min(max(0, len(nodes) - 1), cursor + body_height())
                ensure_visible()
            elif key == curses.KEY_RIGHT:
                if node and node["expandable"]:
                    if node["key"] not in expanded:
                        expanded.add(node["key"])
                        rebuild()
                    elif cursor + 1 < len(nodes) \
                            and nodes[cursor + 1]["depth"] > node["depth"]:
                        cursor += 1  # already open → step into first child
                    ensure_visible()
                elif node and node["kind"] in ("file", "card"):
                    focus = "content"
            elif key == curses.KEY_LEFT:
                if node and node["expandable"] and node["key"] in expanded:
                    expanded.discard(node["key"])
                    rebuild()
                else:
                    pi = parent_index()
                    if pi is not None:
                        cursor = pi
                ensure_visible()
            elif key in ("\n", "\r", " ", curses.KEY_ENTER):
                if node and node["kind"] == "card":
                    tb = node.get("bed")
                    if tb:  # the entrance: land on the card's bed in this tree
                        for i2, n2 in enumerate(nodes):
                            if n2["kind"] == "bed" and n2["bed"] is tb:
                                cursor = i2
                                ensure_visible()
                                message = f"→ landed: {tb['slug']}"
                                break
                    else:
                        focus = "content"
                        message = "card target missing here — elsewhere, not finished"
                elif node and node["expandable"]:
                    if node["key"] in expanded:
                        expanded.discard(node["key"])
                    else:
                        expanded.add(node["key"])
                    rebuild()
                    ensure_visible()
                elif node and node["kind"] == "file":
                    focus = "content"
            elif key in ("F", "f") and bed:
                if bed["slug"] in expanded:
                    expanded.discard(bed["slug"])
                else:
                    expanded.add(bed["slug"])
                rebuild(keep_key=bed["slug"])
                ensure_visible()

        # --- content focus ---
        elif focus == "content":
            if key == curses.KEY_UP:
                content_off = max(0, content_off - 1)
            elif key == curses.KEY_DOWN:
                content_off += 1
            elif key == curses.KEY_PPAGE:
                content_off = max(0, content_off - body_height())
            elif key == curses.KEY_NPAGE:
                content_off += body_height()
            elif key == "g":
                content_off = 0
            elif key == "G":
                content_off = 10 ** 9  # draw clamps to end
            elif key == curses.KEY_LEFT:
                focus = "tree"

    save_ui_state(root, last_sel_key, expanded, tree_right, split, belt)
    return buffer_lines


# ── Entry ─────────────────────────────────────────────────────────────────────

def run_on_tty(root, tree_right=None):
    beds = load_beds(root)
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as e:
        print(f"rb-open: cannot open /dev/tty: {e}", file=sys.stderr)
        return 2
    saved_in = os.dup(0)
    saved_out = os.dup(1)
    screen = None
    buffer_lines = []
    try:
        os.dup2(tty_fd, 0)
        os.dup2(tty_fd, 1)
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        buffer_lines = palette(screen, beds, root, tree_right) or []
    finally:
        if screen:
            try:
                screen.keypad(False)
                curses.nocbreak()
                curses.echo()
                curses.endwin()
            except curses.error:
                pass
        os.dup2(saved_in, 0)
        os.dup2(saved_out, 1)
        os.close(saved_in)
        os.close(saved_out)
        os.close(tty_fd)
    if buffer_lines:
        print("── rb buffer ──")
        for line in buffer_lines:
            print(line)
    return 0


def board_cli(argv):
    parser = argparse.ArgumentParser(prog="runbook.py board",
                                     description="presence-board/v1 client (advisory)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="render all records; * marks own attachments")
    pm = sub.add_parser("mark", help="attach: exclusive-create one record")
    pm.add_argument("--bed", required=True)
    pm.add_argument("--workspace", default=None)
    pm.add_argument("--seat", default=None)
    pm.add_argument("--note", default="")
    pu = sub.add_parser("unmark", help="detach own record(s) — never another owner's")
    pu.add_argument("--id", default=None)
    pu.add_argument("--bed", default=None)
    args = parser.parse_args(argv)
    if args.cmd == "list":
        return board_list_plain()
    if args.cmd == "mark":
        aid, path = board_mark(args.bed, args.workspace, args.seat, args.note)
        print(f"attached: {aid}\n{path}")
        return 0
    if args.cmd == "unmark":
        removed = board_unmark(aid=args.id, bed=args.bed)
        for i in removed:
            print(f"detached: {i}")
        return 0
    return 1


def selftest():
    """Sandboxed selftest — temp tree + temp board, zero touches outside it.
    Covers the truth-display regression class (next: block scalars, in_flight
    raw flag), help/search/layout behavior, gate states, D2 build/fold, and the
    full board contract cycle."""
    import tempfile
    failures = []

    def check(label, cond):
        print(("PASS  " if cond else "FAIL  ") + label)
        if not cond:
            failures.append(label)

    with tempfile.TemporaryDirectory(prefix="rb-selftest.") as td:
        root = Path(td) / ".dev" / "session"
        # bed-a: canonical — fenced yaml, flat quoted next, in_flight none
        a = root / "bed-a"; (a / "_bus").mkdir(parents=True)
        (a / "RUNBOOK.md").write_text("# RUNBOOK\n```yaml\ngoal: test\n```\n")
        (a / "STATUS.md").write_text(
            '# S\n```yaml\nnext: "do the thing"\nin_flight: none\n```\n')
        (a / "_bus" / "01.seat.point.md").write_text("x\n")
        (a / "_bus" / "01.other.return.md").write_text("y\n")
        (a / "_bus" / "02.seat.point.md").write_text("z\n")
        (a / "_bus" / "02.seat.verdict.md").write_text("w\n")
        (a / "_bus" / "02.other.return.md").write_text("v\n")
        (a / "_bus" / "freeform-note.md").write_text("n\n")
        # bed-b: RUNBOOK only → ·
        b = root / "bed-b"; b.mkdir()
        (b / "RUNBOOK.md").write_text("# R\n")
        # bed-c: empty → ?
        (root / "bed-c").mkdir()
        # bed-d: lowercase status (drift), folded next: >-, non-canon in_flight → ! + ~
        d = root / "bed-d"; d.mkdir()
        (d / "RUNBOOK.md").write_text("# R\n")
        (d / "status.md").write_text(
            "# S\n```yaml\nnext: >-\n  first folded line\n  second folded line\n"
            "in_flight: none — but with a trailing comment\n```\n")

        beds = {x["path"].name: x for x in load_beds(root)}
        check("gate states → · ? !", [beds[k]["state"] for k in
              ("bed-a", "bed-b", "bed-c", "bed-d")] == ["→", "·", "?", "!"])
        check("lowercase drift marker ~", beds["bed-d"]["slug"] == "bed-d~")
        check("flat quoted next", beds["bed-a"]["next_line"] == "do the thing")
        check("folded >- next resolved",
              beds["bed-d"]["next_line"] == "first folded line second folded line")
        check("in_flight raw carried",
              beds["bed-d"]["in_flight_raw"] == "none — but with a trailing comment")
        check("canonical none idle", _inflight_idle(beds["bed-a"]["in_flight_raw"]))
        check("non-canon flags active", not _inflight_idle(beds["bed-d"]["in_flight_raw"]))

        blist = list(beds.values())
        check("tree collapsed = one node per bed",
              len(build_tree(blist, set())) == 4)
        keys = [n["key"] for n in build_tree(blist, {"bed-a"})]
        check("bed expand shows five parts",
              all(f"bed-a/{s}" in keys for s in BED_PARTS))
        keys2 = [n["key"] for n in build_tree(blist, {"bed-a", "bed-a/bus"})]
        check("group expand lists bus file", "bed-a/bus/01.seat.point.md" in keys2)
        ov = render_overview(beds["bed-a"], 60, board_recs=[])
        check("overview carries next", any("do the thing" in t for t, _ in ov))

        # Belt off: main layout reclaims every row. Belt on: exactly one row.
        check("belt off reclaims all footer rows",
              main_heights(10, [], False) == (10, 0))
        check("only open buffer reserves bottom rows",
              main_heights(10, ["a", "b"], True) == (7, 3))
        check("hint belt reserves exactly one row",
              main_heights(10, [], False, belt=True) == (9, 0))
        check("belt + buffer stack without overlap",
              main_heights(10, ["a", "b"], True, belt=True) == (6, 3))
        check("belt yields on a 1-row screen",
              main_heights(1, [], False, belt=True) == (1, 0))

        # Dynamic help scopes + forgiving current/all-scope AND search.
        help_root = Path(td) / "help"
        (help_root / "alpha").mkdir(parents=True)
        (help_root / "beta").mkdir()
        (help_root / "alpha" / "HELP.md").write_text(
            "# Alpha\n\n- list orientation\n\n```\nA key row\n```\n")
        (help_root / "beta" / "HELP.md").write_text(
            "# Beta\n\n## Presence\n\nPresence board records are advisory.\n")
        scopes = load_help_scopes(help_root)
        check("help scopes discovered from folders",
              [scope["name"] for scope in scopes] == ["alpha", "beta"])
        check("current-scope search stays scoped",
              search_help(scopes, "presence records", 0) == [])
        found = search_help(scopes, "PRESENCE records")
        check("all-scope search is case-insensitive AND",
              len(found) == 1 and found[0]["scope"] == "beta")
        check("search result carries heading context",
              found[0]["heading"] == "Presence" and found[0]["line"] == 5)
        check("AND search rejects partial token sets",
              search_help(scopes, "presence missing") == [])
        rendered = render_help_lines(scopes[1]["path"], 80,
                                     help_tokens("presence records"))
        matched = next(item for item in rendered if item[2] == 5)
        check("search landing line is visibly highlighted",
              bool(matched[1] & curses.A_REVERSE))

        saved_cp = CP.copy()
        CP.update({"header": 1, "accent": 2, "good": 3, "meta": 4})
        try:
            attrs = {"heading": help_line_attr("# Head", False),
                     "list": help_line_attr("- item", False),
                     "code": help_line_attr("key row", True)}
            check("help heading/list/code colors differ",
                  len(set(attrs.values())) == 3)
        finally:
            CP.clear()
            CP.update(saved_cp)

        # Help keeps one keypad-enabled window across ordinary/navigation keys.
        class FakeHelpWindow:
            def __init__(self):
                self.keys = iter(("x", curses.KEY_RIGHT, "q"))
                self.refreshes = 0
                self.keypad_enabled = False
                self.timeout_ms = None

            def getmaxyx(self):
                return (20, 64)

            def erase(self):
                pass

            def box(self):
                pass

            def keypad(self, enabled):
                self.keypad_enabled = enabled

            def timeout(self, delay):
                self.timeout_ms = delay

            def addnstr(self, *_args):
                pass

            def refresh(self):
                self.refreshes += 1

            def get_wch(self):
                return next(self.keys)

        fake_help_win = FakeHelpWindow()
        newwin_calls = []
        real_newwin = curses.newwin
        curses.newwin = lambda *args: newwin_calls.append(args) or fake_help_win
        try:
            help_view(fake_help_win)
        finally:
            curses.newwin = real_newwin
        check("help window stable across input", len(newwin_calls) == 1
              and fake_help_win.refreshes == 3)
        check("help window decodes navigation keys", fake_help_win.keypad_enabled
              and fake_help_win.timeout_ms == -1)

        # D — receipt navigation (display-only)
        busv = [t for t, _ in render_bus_group(beds["bed-a"], 70)]
        check("bus cycles grouped newest-first",
              busv.index("#2") < busv.index("#1"))
        check("open-return presence fact surfaced",
              any(t.endswith("no verdict file: cycle 1") for t in busv))
        check("cycle with verdict not flagged",
              not any("cycle 1, 2" in t or "cycle 2" in t for t in busv))
        check("unnumbered bus file surfaced not hidden",
              any("freeform-note.md" in t for t in busv))

        # board contract cycle in sandbox (HOME retargeted so ~-anchoring works)
        os.environ["RB_BOARD"] = str(Path(td) / "_active")
        os.environ["RB_STATE"] = str(Path(td) / "state")
        os.environ.setdefault("MACHINE_NAME", "selftest")
        saved_home = os.environ["HOME"]
        os.environ["HOME"] = td
        try:
            try:
                board_mark("/etc", seat="selftest")
                check("outside-~ bed refused", False)
            except SystemExit:
                check("outside-~ bed refused", True)
            aid, rpath = board_mark(str(a), seat="selftest", note='q"uo\\te stripped')
            rec_text, rec_name = rpath.read_text(), rpath.name
            state, reason, fields = parse_record(rec_text, rec_name)
            check("board record valid", state == "valid")
            check("note sanitized", '"' not in fields.get("note", '"'))
            check("own flagged", load_board()[0]["own"])
            try:
                board_unmark(aid="f" * 32); check("foreign unmark rejected", False)
            except SystemExit:
                check("foreign unmark rejected", True)
            board_unmark(aid=aid)
            check("detach empties board", load_board() == [])
            bad = Path(os.environ["RB_BOARD"]) / ("presence." + "a" * 32 + ".md")
            bad.write_text("---\nschema: \"presence-board/v1\"\n---\n")
            check("malformed reported not hidden",
                  [r["state"] for r in load_board()] == ["malformed"])
            check("calendar 02-30 rejected", parse_record(rec_text.replace(
                fields["attached_at"][:10], "2026-02-30"), rec_name)[0] == "malformed")

            # cold-start entrance (HOME still sandboxed → ~ resolves into td)
            vault = Path(td) / "vault"
            (vault / "card").mkdir(parents=True)
            (vault / "archive").mkdir()
            os.environ["RB_CS_VAULT"] = str(vault)
            (vault / "card" / "CS.hit.2026-09-10.md").write_text(
                "---\nkind: cold-start-card\nproject: testproj\ndate: 2026-09-10\n"
                'resume: "claude --resume abc123"\n'
                "runbook: ~/.dev/session/bed-a/RUNBOOK.md\n---\nbody\n")
            (vault / "card" / "CS.miss.md").write_text(
                "---\nkind: cold-start-card\nroot: ~/elsewhere\n---\nbody\n")
            (vault / "archive" / "CS.old.md").write_text(
                "---\nkind: cold-start-card\n---\nx\n")
            cards = load_cs_cards()
            check("vault loads three cards", len(cards) == 3)
            hit = next(cd for cd in cards if "hit" in cd["path"].name)
            check("card matches bed via runbook pointer",
                  card_matches_bed(hit, beds["bed-a"]["path"]))
            check("umbrella from project: key", hit["project"] == "testproj")
            check("resume extracted", hit["resume"] == "claude --resume abc123")
            miss0 = next(cd for cd in cards if "miss" in cd["path"].name)
            check("umbrella derived from slug", miss0["project"] == "miss")
            vt = build_tree(blist, {"_cold-start"}, cards)
            check("vault groups under umbrellas",
                  any(n["kind"] == "csgroup" and n["key"] == "_cold-start/testproj"
                      for n in vt))
            miss = next(cd for cd in cards if cd["path"].name == "CS.miss.md")
            check("unmatched card stays unmatched",
                  not card_matches_bed(miss, beds["bed-a"]["path"]))
            check("archived state carried",
                  next(cd for cd in cards
                       if cd["path"].name == "CS.old.md")["state"] == "archived")
            t2 = build_tree(blist, {"bed-a"}, cards)
            check("bed grows cs group", any(n["key"] == "bed-a/cs" for n in t2))
            vkids = [n for n in build_tree(
                blist, {"_cold-start", "_cold-start/testproj",
                        "_cold-start/miss", "_cold-start/old"}, cards)
                if n["kind"] == "card"]
            check("vault card carries landing arrow",
                  any("→ bed-a" in n["label"] for n in vkids))
            check("missing-here card carries no landing",
                  any(n["label"].endswith("CS.miss.md") and n["bed"] is None
                      for n in vkids))
            # drain move + guards
            (vault / "routines").mkdir()
            (vault / "routines" / "RT.daily.md").write_text("---\nkind: routine\n---\nx\n")
            cards3 = load_cs_cards()
            rt = next(cd for cd in cards3 if cd["state"] == "routine")
            try:
                archive_card(rt)
                check("routine archive refused", False)
            except SystemExit:
                check("routine archive refused", True)
            hit3 = next(cd for cd in cards3 if "hit" in cd["path"].name)
            dst = archive_card(hit3)
            check("drain moves card to archive/", dst.exists()
                  and not hit3["path"].exists())
            check("drained card reloads as archived",
                  next(cd for cd in load_cs_cards()
                       if "hit" in cd["path"].name)["state"] == "archived")
        finally:
            os.environ["HOME"] = saved_home

    print(("SELFTEST PASS" if not failures else
           f"SELFTEST FAIL — {len(failures)}: {failures}"))
    return 0 if not failures else 1


def main():
    if sys.argv[1:2] == ["board"]:
        return board_cli(sys.argv[2:])
    if sys.argv[1:2] == ["selftest"]:
        return selftest()
    parser = argparse.ArgumentParser(description="session browser (rb-open)")
    parser.add_argument("--root", default=None, help="explicit .dev/session/ path")
    parser.add_argument("--right", action="store_true", default=None,
                        help="tree column on the right (mirror view; v toggles live)")
    args = parser.parse_args()
    root = find_root(args.root)
    if root is None:
        print("rb-open: could not locate .dev/session/ — pass --root or set $RB_ROOT",
              file=sys.stderr)
        return 1
    return run_on_tty(root, True if args.right else None)


if __name__ == "__main__":
    raise SystemExit(main())
