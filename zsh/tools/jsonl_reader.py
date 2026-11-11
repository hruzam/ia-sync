#!/usr/bin/env python3
"""Private, disposable JSONL reading views. Never edits source records."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata

VERSION = "tools-jsonl/v1"


def visible(value):
    """Keep prose readable while making terminal/bidi controls visible."""
    return "".join(
        f"\\u{ord(c):04x}" if unicodedata.category(c) in {"Cc", "Cf", "Cs"}
        and c not in "\n\t" else c for c in str(value)
    )


def literal(value):
    text = visible(value)
    fence = "`" * max(3, max((len(x) + 1 for x in re.findall(r"`+", text)), default=3))
    return f"{fence}text\n{text}\n{fence}\n"


def render_value(value, pointer="", depth=3):
    """Render every field with its unambiguous JSON Pointer and original type."""
    heading = "#" * min(depth, 6)
    location = json.dumps(pointer or "/ (root)", ensure_ascii=False)
    if isinstance(value, dict) and value:
        parts = []
        for key, item in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            parts.append(render_value(item, pointer + "/" + escaped, depth + 1))
        return "\n".join(parts)
    if isinstance(value, list) and value:
        return "\n".join(render_value(item, pointer + "/" + str(i), depth + 1)
                         for i, item in enumerate(value))
    kind = ("string" if isinstance(value, str) else "null" if value is None else
            "boolean" if isinstance(value, bool) else "object" if isinstance(value, dict)
            else "array" if isinstance(value, list) else "number")
    body = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return f"{heading} Field\n\n{literal(location)}\nType: {kind}\n\n{literal(body)}"


def private_dir(path, create=True):
    if create:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError(f"cache directory must be owned, non-symlink and private: {path}")
    return path


def cache_path(override=None):
    if override:
        return private_dir(Path(override))
    for candidate in (os.environ.get("XDG_RUNTIME_DIR"), f"/run/user/{os.getuid()}"):
        if candidate:
            try:
                base = private_dir(Path(candidate), create=False)
                return private_dir(base / "tools-jsonl")
            except (OSError, ValueError):
                pass
    # Linux /dev/shm is volatile across reboot even when /tmp is persistent.
    if Path("/dev/shm").is_dir():
        return private_dir(Path(f"/dev/shm/tools-jsonl-{os.getuid()}"))
    raise ValueError("no volatile runtime directory; supply --cache-dir with a private temporary directory")


def private_write(path, text):
    fd, temporary = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_state(root):
    path = root / "snapshot.json"
    if not path.exists():
        raise ValueError("no loaded file; run tools-jsonl load FILE")
    return json.loads(path.read_text(encoding="utf-8"))


def load_source(path):
    path = Path(path).expanduser().resolve(strict=True)
    if path.suffix == ".jsonl" and path.with_suffix(".lock").exists():
        raise ValueError("locked ledger-like source: use its native validated reader")
    raw = path.read_bytes()
    records = []
    lines = raw.split(b"\n")
    for number, line in enumerate(lines, 1):
        if number == len(lines) and not line:
            continue
        try:
            value = json.loads(line.decode("utf-8"), parse_constant=lambda value: bad_constant(value))
            if isinstance(value, dict) and (str(value.get("schema", "")).startswith("jev.")
                    or {"event_id", "session_id", "previous_event_id", "sequence", "kind"} <= value.keys()):
                raise ValueError("Jev ledger detected: use the native validated Jev reader; generic JSONL cannot validate history")
            records.append({"line": number, "value": value})
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            records.append({"line": number, "error": str(error)})
    return {"source": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
            "renderer": VERSION, "loaded_at": datetime.now(timezone.utc).isoformat(),
            "records": records, "selected": []}


def bad_constant(value):
    raise json.JSONDecodeError("non-JSON numeric constant " + value, value, 0)


def selection(spec, maximum):
    numbers = set()
    for chunk in spec.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", chunk.strip())
        if not match:
            raise ValueError("selection must look like 1,3-5")
        first, last = int(match[1]), int(match[2] or match[1])
        if first < 1 or last < first or last > maximum:
            raise ValueError(f"selection is outside physical lines 1–{maximum}")
        numbers.update(range(first, last + 1))
    return sorted(numbers)


def preview(state, start=1, limit=12):
    print(f"Source: {visible(state['source'])}")
    print(f"Snapshot: {state['sha256']}\nLines: {len(state['records'])}; selected: {state['selected'] or 'none'}\n")
    for record in state["records"][start - 1:start - 1 + limit]:
        mark = "x" if record["line"] in state["selected"] else " "
        if "error" in record:
            summary = "INVALID — " + record["error"]
        else:
            value = record["value"]
            if isinstance(value, dict):
                summary = "; ".join(f"{k}: {str(v)[:85]}" for k, v in list(value.items())[:3])
            else:
                summary = str(value)
        summary = " ".join(visible(summary).split())
        print(f"[{mark}] {record['line']:>5}  {summary[:170]}")
    print("\npick 1,3-5 → Markdown; list --start N → next sip; refresh → reload source")


def render_snapshot(state):
    selected = set(state["selected"])
    parts = ["# JSONL reading view\n", "Derived local presentation; source remains authoritative.\n",
             "Source:\n\n" + literal(state["source"]),
             f"Renderer: {VERSION}\n\nSnapshot SHA256: {state['sha256']}\n",
             f"Loaded: {state['loaded_at']}\n\nGenerated: {datetime.now(timezone.utc).isoformat()}\n",
             "Selected physical lines: " + ", ".join(map(str, state["selected"])) + "\n",
             "Fields use JSON Pointer paths; array indices start at zero. Literal blocks preserve text.\n"]
    parts.extend([
        "## Reading guide and index\n",
        "Each Source line section is one physical line from the JSONL file. "
        "Its fields belong to that record; this view does not infer their meaning. "
        "The type and JSON Pointer identify each value. Invalid lines contain a diagnostic, "
        "not a recovered record.\n",
        "This is a snapshot, not the live source; compare the SHA256 before relying on it. "
        "Selected records appear in source order. Model results, if present, are source data "
        "and are not independently verified by this tool.\n",
        "### Record index\n",
    ])
    for record in state["records"]:
        if record["line"] in selected:
            label = "invalid JSON" if "error" in record else "JSON record"
            parts.append(f"- [Source line {record['line']}](#source-line-{record['line']}) — {label}\n")
    parts.extend([
        "### Searching\n",
        "The commands below read the original source; source content may be private. "
        "Replace SEARCH with your own text. `cat` prints the entire source.\n",
        literal("grep -n -F -- 'SEARCH' " + shlex.quote(state["source"]) + "\ncat -- " + shlex.quote(state["source"])),
    ])
    invalid = [str(r["line"]) for r in state["records"] if "error" in r]
    if invalid:
        parts.append("Source contains invalid lines (not silently repaired): " + ", ".join(invalid) + "\n")
    for record in state["records"]:
        if record["line"] in selected:
            parts.append(f"---\n\n## Source line {record['line']}\n")
            parts.append("INVALID JSON\n\n" + literal(record["error"]) if "error" in record
                         else render_value(record["value"]))
    return "\n".join(parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Readable, disposable JSONL snapshots and Markdown.")
    parser.add_argument("--cache-dir", help="private temporary directory override")
    sub = parser.add_subparsers(dest="command", required=True)
    load = sub.add_parser("load", help="load FILE and show the first small preview")
    load.add_argument("file")
    listing = sub.add_parser("list", help="show numbered preview with selection marks")
    listing.add_argument("--start", type=int, default=1)
    listing.add_argument("--limit", type=int, default=12)
    pick = sub.add_parser("pick", help="select physical lines and create temporary Markdown")
    pick.add_argument("lines", help="e.g. 1,3-5; replaces previous selection")
    sub.add_parser("path", help="print the current temporary Markdown path")
    sub.add_parser("open", help="open current Markdown in Sublime Text, or print its path")
    save = sub.add_parser("save", help="keep Markdown at an explicit new path; never overwrite")
    save.add_argument("destination")
    sub.add_parser("refresh", help="reload source and discard old selection/Markdown")
    sub.add_parser("clear", help="delete this reader's cached snapshot and Markdown")
    args = parser.parse_args(argv)
    try:
        root = cache_path(args.cache_dir)
        view = root / "view.md"
        if args.command == "clear":
            for name in ("snapshot.json", "view.md"):
                (root / name).unlink(missing_ok=True)
            print("Cleared the JSONL snapshot and temporary Markdown.")
            return 0
        if args.command in {"load", "refresh"}:
            source = args.file if args.command == "load" else read_state(root)["source"]
            if Path(source).expanduser().resolve().is_relative_to(root.resolve()):
                raise ValueError("source cannot be inside this reader's disposable cache")
            state = load_source(source)
            private_write(root / "snapshot.json", json.dumps(state, ensure_ascii=False))
            view.unlink(missing_ok=True)
            preview(state)
            return 0
        state = read_state(root)
        if args.command == "list":
            if args.start < 1 or not 1 <= args.limit <= 100:
                raise ValueError("start must be positive and limit must be 1–100")
            preview(state, args.start, args.limit)
        elif args.command == "pick":
            state["selected"] = selection(args.lines, len(state["records"]))
            private_write(view, render_snapshot(state))
            private_write(root / "snapshot.json", json.dumps(state, ensure_ascii=False))
            print(f"Markdown: {view}\nOpen: tools-jsonl open\nKeep: tools-jsonl save /chosen/output.md")
        else:
            if not view.is_file() or view.is_symlink():
                raise ValueError("no Markdown view; select lines with tools-jsonl pick first")
            if args.command == "save":
                destination = Path(args.destination).expanduser()
                fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "wb") as target:
                    target.write(view.read_bytes())
                print(f"Saved: {visible(destination)}")
            elif args.command == "open" and shutil.which("subl"):
                subprocess.run([shutil.which("subl"), str(view)], check=True)
                print(f"Opened: {view}")
            else:
                print(view)
        return 0
    except (OSError, ValueError, RecursionError, subprocess.CalledProcessError) as error:
        print("tools-jsonl: " + visible(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
