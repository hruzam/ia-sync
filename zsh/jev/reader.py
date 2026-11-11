#!/usr/bin/env python3
"""Render a verified Jev ledger as a local Markdown reading view.

This reader uses the vault's native replay and never opens, repairs, or changes a ledger.
"""

import argparse
from datetime import datetime, timezone
import html
import os
from pathlib import Path
import re
import stat
import sys
import unicodedata

import kernel
import store


def _text(value):
    """Keep controls visible while leaving ordinary prose readable."""
    return "".join(f"\\u{ord(character):04x}"
                   if unicodedata.category(character) in {"Cc", "Cf", "Cs"} and character not in "\n\t"
                   else character for character in value)


def _key(value):
    """Keep JSON keys in one inert inline-code token."""
    text = _text(value).replace("\n", "\\n").replace("\t", "\\t")
    fence = "`" * max(1, max((len(group) + 1 for group in re.findall(r"`+", text)), default=1))
    return fence + text + fence


def _literal(value, indent):
    text = _text(value)
    # Top-level HTML blocks avoid nested Markdown fence ambiguity. Escape all source HTML;
    # Numeric entities survive tab expansion and fenced-code preprocessing, then decode in the view.
    literal = (html.escape(text, quote=False).replace("\t", "&#9;")
               .replace("`", "&#96;").replace("~", "&#126;"))
    return ["", "<pre>" + literal + "</pre>", ""]


def _scalar(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return None
    return "`" + str(value) + "`"


def _redacted(path, event_kind):
    """Hide only actual encoded payloads and the live-send grant, not similarly named data."""
    return ((event_kind == "prepare" and path == ("provider", "body_base64"))
            or (event_kind in {"reply", "http"} and path == ("raw_base64",))
            or (event_kind == "attempt" and path == ("authorization",)))


def _value(value, indent="", path=(), event_kind=None):
    """Render JSON as an indented, faithful Markdown value tree."""
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            child_path = path + (key,)
            if _redacted(child_path, event_kind):
                lines.append(f"{indent}- {_key(key)}: _omitted from reading view_")
            elif isinstance(item, (dict, list)):
                lines.append(f"{indent}- {_key(key)}:")
                lines.extend(_value(item, indent + "  ", child_path, event_kind))
            elif isinstance(item, str):
                lines.append(f"{indent}- {_key(key)}:")
                lines.extend(_literal(item, indent + "  "))
            else:
                lines.append(f"{indent}- {_key(key)}: {_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for index, item in enumerate(value, 1):
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}- item {index}:")
                lines.extend(_value(item, indent + "  ", path + (str(index - 1),), event_kind))
            elif isinstance(item, str):
                lines.append(f"{indent}- item {index}:")
                lines.extend(_literal(item, indent + "  "))
            else:
                lines.append(f"{indent}- {_scalar(item)}")
        return lines
    if isinstance(value, str):
        return _literal(value, indent)
    return [indent + _scalar(value)]


def render(ledger, request=None, generated_at=None, sequences=None):
    """Return a deterministic local view of already replayed, validated events."""
    selected = [event for event in ledger.events if (request is None or event["request_id"] == request)
                and (sequences is None or event["sequence"] in sequences)]
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    lines = ["# Jev reading view", "", "This is a local derived presentation, not a new Jev reply.", "",
             "## Source", "", f"- Ledger: `{_text(str(ledger.path))}`",
             f"- Session: `{ledger.session_id}`", f"- Filter: `{request or 'all events'}`",
             f"- Selected sequences: `{', '.join(map(str, sorted(sequences))) if sequences is not None else 'all'}`",
             f"- Renderer: `jev-reader/v1`", f"- Generated: `{generated_at}`",
             f"- Verified events shown: `{len(selected)}`"]
    if ledger.tail is not None:
        lines.extend(["", "## Incomplete tail", "", "The native replay preserved a tail diagnostic; it was not repaired."])
        lines.extend(_value(ledger.tail))
    lines.extend(["", "## Event index", "", "Each event is one validated ledger record, in recorded order.", ""])
    for event in selected:
        lines.append(f"- Event {event['sequence']}: `{event['kind']}` · `{event['event_id']}`")
    lines.extend(["", "## Chronology"])
    for event in selected:
        lines.extend(["", f"### {event['sequence']}. `{event['kind']}`", "",
                      f"- Event ID: `{event['event_id']}`", f"- Recorded: `{event['at']}`",
                      f"- Request: `{event['request_id']}`", f"- Previous event: `{event['previous_event_id']}`",
                      "- Recorder:"])
        lines.extend(_value(event["actor"], "  "))
        lines.append("- Data:")
        lines.extend(_value(event["data"], "  ", event_kind=event["kind"]))
    return "\n".join(lines) + "\n"


def read(root, session, request=None):
    """Use Vault.selected so ledger replay and validation happen before rendering."""
    vault = store.Vault(root)
    with vault.selected(session, "main") as ledger:
        if request is not None:
            ledger.request(request)
        return render(ledger, request)


def write_output(path, content):
    """Write only an explicitly named private local view."""
    path = Path(path)
    try:
        parent = path.parent.lstat()
    except OSError:
        raise kernel.Invalid("output parent unavailable") from None
    if (not stat.S_ISDIR(parent.st_mode) or stat.S_ISLNK(parent.st_mode)
            or parent.st_uid != os.getuid() or stat.S_IMODE(parent.st_mode) != 0o700 or path.is_symlink()):
        raise kernel.Invalid("output parent unavailable or output symlink refused")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
        try:
            info = os.fstat(descriptor)
            kernel.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                           and stat.S_IMODE(info.st_mode) == 0o600, "output must be private regular file")
            data = content.encode("utf-8")
            while data:
                count = os.write(descriptor, data)
                kernel.require(count > 0, "private output write failed")
                data = data[count:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        raise kernel.Invalid("private output unavailable") from None
    return path


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise kernel.Invalid("arguments: " + message)


def parser():
    result = Parser(description=__doc__)
    result.add_argument("--root", default="~/.jev")
    result.add_argument("--session", required=True)
    result.add_argument("--request")
    result.add_argument("--output", required=True, help="explicit new private Markdown output path")
    return result


def main(argv=None):
    try:
        args = parser().parse_args(argv)
        content = read(args.root, args.session, args.request)
        print(write_output(args.output, content))
        return 0
    except (kernel.Invalid, OSError, RecursionError) as error:
        print("reader error: " + (str(error) if isinstance(error, kernel.Invalid) else "local read failure"), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
