#!/usr/bin/env python3
"""Termbrana request/0.1: inert bytes-in parser. Wire contract: GRAMMAR.md."""

import json
import re
import sys


REQUIRED = ("format", "id", "from", "to", "requested_scope")
LIST_KEYS = frozenset(("consult", "context"))
ALLOWED = frozenset(REQUIRED + ("consult", "context", "in_reply_to", "expected_return", "stop"))
MARKER = re.compile(rb"<!-- composer:(packet|body|end) ([a-z0-9]{4,8}) -->")
HEADER = re.compile(rb"([A-Za-z][A-Za-z0-9_]*): (.*)")
SMART_QUOTES = "\u2018\u2019\u201c\u201d"


class _FrozenRecord:
    """Small immutable attribute records without reflection/import-time setup."""

    def _initialize(self, values):
        for name in self._record_fields:
            object.__setattr__(self, name, values[name])

    def __setattr__(self, name, value):
        raise AttributeError(f"cannot assign to field {name!r}")

    def __delattr__(self, name):
        raise AttributeError(f"cannot delete field {name!r}")

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return all(getattr(self, name) == getattr(other, name) for name in self._record_fields)

    def __hash__(self):
        return hash(tuple(getattr(self, name) for name in self._record_fields))

    def __repr__(self):
        fields = ", ".join(f"{name}={getattr(self, name)!r}" for name in self._record_fields)
        return f"{type(self).__name__}({fields})"


class Diagnostic(_FrozenRecord):
    _record_fields = ("code", "reason", "byte_offset", "line", "byte_column", "packet_nonce", "field")
    code: str
    reason: str
    byte_offset: int
    line: int
    byte_column: int
    packet_nonce: str | None
    field: str | None

    def __init__(self, code, reason, byte_offset, line, byte_column, packet_nonce, field):
        self._initialize(locals())

    def as_dict(self):
        return dict(vars(self))


class Packet(_FrozenRecord):
    _record_fields = ("nonce", "fields", "span", "header_span", "body_span", "frame_spans")
    nonce: str
    fields: dict
    span: tuple[int, int]
    header_span: tuple[int, int]
    body_span: tuple[int, int]
    frame_spans: tuple[tuple[int, int], ...]

    def __init__(self, nonce, fields, span, header_span, body_span, frame_spans):
        self._initialize(locals())

    def metadata(self):
        return dict(nonce=self.nonce, fields=self.fields, span=self.span,
                    header_span=self.header_span, body_span=self.body_span,
                    frame_spans=self.frame_spans)


class Document(_FrozenRecord):
    _record_fields = ("source", "packets")
    source: bytes
    packets: tuple[Packet, ...]

    def __init__(self, source, packets):
        self._initialize(locals())

    def to_bytes(self):
        """Copy retained spans, including all outside bytes; never serialize fields."""
        spans = []
        previous = 0
        for packet in self.packets:
            start, end = packet.span
            spans.extend((self.source[previous:start], self.source[start:end]))
            previous = end
        spans.append(self.source[previous:])
        return b"".join(spans)


class ParseResult(_FrozenRecord):
    _record_fields = ("document", "diagnostics")
    document: Document | None
    diagnostics: tuple[Diagnostic, ...]

    def __init__(self, document, diagnostics):
        self._initialize(locals())

    @property
    def packets(self):
        return self.document.packets if self.document is not None else ()


class _ValueError(ValueError):
    pass


def _decoded_string(value):
    if not value:
        raise _ValueError("empty_value")
    if any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF
           or c == "\ufeff" for c in value):
        raise _ValueError("invalid_string")
    return value


def _scalar(source):
    if source.startswith('"'):
        try:
            value = json.loads(source)
        except (ValueError, RecursionError):
            raise _ValueError("invalid_string") from None
        return _decoded_string(value)
    _decoded_string(source)
    if any(c in "\"'[]{}" for c in source) or source[0] in SMART_QUOTES or source[-1] in SMART_QUOTES:
        raise _ValueError("invalid_string")
    return source


def _list(source):
    if not source.endswith("]"):
        raise _ValueError("invalid_list")
    inside = source[1:-1]
    if not inside.strip(" "):
        return []
    items = []
    index = 0
    decoder = json.JSONDecoder()
    try:
        while index < len(inside):
            while index < len(inside) and inside[index] == " ":
                index += 1
            if index == len(inside):
                raise _ValueError("invalid_list")
            if inside[index] == '"':
                value, index = decoder.raw_decode(inside, index)
                items.append(_decoded_string(value))
            else:
                end = inside.find(",", index)
                if end == -1:
                    end = len(inside)
                items.append(_scalar(inside[index:end].strip(" ")))
                index = end
            while index < len(inside) and inside[index] == " ":
                index += 1
            if index == len(inside):
                return items
            if inside[index] != ",":
                raise _ValueError("invalid_list")
            index += 1
        raise _ValueError("invalid_list")
    except (ValueError, RecursionError):
        raise _ValueError("invalid_list") from None


def _lines(data):
    """LF alone splits physical lines. Bare CR and Unicode separators do not."""
    start = 0
    while start < len(data):
        lf = data.find(b"\n", start)
        if lf == -1:
            yield start, len(data), data[start:], b""
            return
        content_end = lf - 1 if lf > start and data[lf - 1] == 13 else lf
        yield start, lf + 1, data[start:content_end], data[content_end:lf + 1]
        start = lf + 1


def parse(data: bytes) -> ParseResult:
    """Validate a complete saved document. Invalid input never exposes packets."""
    if not isinstance(data, bytes):
        raise TypeError("parse requires bytes")
    errors = []

    def error(code, reason, offset, nonce=None, field=None):
        line = data.count(b"\n", 0, offset) + 1
        column = offset - data.rfind(b"\n", 0, offset)
        errors.append(Diagnostic(code, reason, offset, line, column, nonce, field))

    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        error("ENCODING_INVALID", "invalid_utf8", exc.start)
        return ParseResult(None, tuple(errors))

    state = "outside"
    nonce = None
    used_nonces = set()
    used_ids = set()
    packets = []
    fields = {}
    seen = set()
    frame_eol = b""
    opening_start = opening_end = body_marker_start = body_start = 0
    stopped = False

    def bad_eol(start, end, content, actual, expected):
        # A bare CR in an ordinary header line is an invalid syntax EOL.
        cr = content.find(b"\r")
        if cr != -1:
            return start + cr
        if not actual:
            return end
        if actual != expected:
            return end - len(actual)
        return None

    for start, end, content, eol in _lines(data):
        if start == 0 and content.startswith(b"\xef\xbb\xbf"):
            content = content[3:]
            start += 3  # BOM remains outside; offsets/columns include its bytes.

        if state == "body":
            if content != b"<!-- composer:end " + nonce.encode("ascii") + b" -->":
                continue
            if eol and eol != frame_eol:
                error("BOUNDARY_INVALID", "frame_eol", end - len(eol), nonce)
                stopped = True
                break
            packets.append(Packet(nonce, dict(consult=[], context=[]) | fields, (opening_start, end),
                                  (opening_end, body_marker_start), (body_start, start),
                                  ((opening_start, opening_end),
                                   (body_marker_start, body_start), (start, end))))
            state = "outside"
            nonce = None
            continue

        marker_like = content.lstrip(b" \t").startswith(b"<!-- composer:")
        marker = MARKER.fullmatch(content)
        if marker_like and marker is None:
            error("BOUNDARY_INVALID", "marker_syntax", start, nonce)
            stopped = True
            break
        if marker is not None:
            kind = marker[1].decode("ascii")
            found = marker[2].decode("ascii")
            if state == "outside":
                if found in used_nonces:
                    error("BOUNDARY_INVALID", "nonce_reused", start, found)
                elif kind != "packet":
                    error("BOUNDARY_INVALID", "marker_order", start, found)
                elif not eol:
                    error("BOUNDARY_INVALID", "frame_eol", end, found)
                else:
                    nonce = found
                    used_nonces.add(found)
                    frame_eol = eol
                    opening_start, opening_end = start, end
                    fields, seen = {}, set()
                    state = "header"
                    continue
            else:
                if kind != "body" or found != nonce:
                    error("BOUNDARY_INVALID", "marker_order", start, nonce)
                elif eol != frame_eol:
                    error("BOUNDARY_INVALID", "frame_eol", end - len(eol), nonce)
                else:
                    for field in REQUIRED:
                        if field not in seen:
                            error("FIELD_MISSING", "required_absent", start, nonce, field)
                    body_marker_start, body_start = start, end
                    state = "body"
                    continue
            stopped = True
            break

        if state == "outside":
            continue

        eol_error = bad_eol(start, end, content, eol, frame_eol)
        if eol_error is not None:
            error("BOUNDARY_INVALID", "frame_eol", eol_error, nonce)
            stopped = True
            break
        if not content or content.startswith((b" ", b"\t", b"#")) or b"\t" in content:
            error("HEADER_INVALID", "header_line", start, nonce)
            continue
        match = HEADER.fullmatch(content)
        if match is None:
            error("HEADER_INVALID", "header_syntax", start, nonce)
            continue
        key = match[1].decode("ascii")
        if key not in ALLOWED:
            error("FIELD_INVALID", "unknown_key", start, nonce, key)
            continue
        if key in seen:
            error("FIELD_INVALID", "duplicate_key", start, nonce, key)
            continue
        seen.add(key)
        source = match[2].decode("utf-8").strip(" ")
        if (key in LIST_KEYS and not source.startswith("[")) or (
                key not in LIST_KEYS and source.startswith(("[", "{"))):
            error("FIELD_INVALID", "wrong_shape", start, nonce, key)
            continue
        try:
            value = _list(source) if key in LIST_KEYS else _scalar(source)
        except _ValueError as exc:
            reason = str(exc)
            error("FIELD_MISSING" if reason == "empty_value" else "FIELD_INVALID",
                  reason, start, nonce, key)
            continue
        fields[key] = value
        if key == "format" and value != "request/0.1":
            error("HEADER_INVALID", "unsupported_format", start, nonce, key)
        if key == "id":
            if value in used_ids:
                error("FIELD_INVALID", "duplicate_id", start, nonce, key)
            used_ids.add(value)

    if not stopped:
        if state == "header":
            error("BOUNDARY_INVALID", "missing_body", len(data), nonce)
        elif state == "body":
            error("BOUNDARY_INVALID", "missing_end", len(data), nonce)
        elif not packets:
            error("BOUNDARY_INVALID", "no_packets", 0)
    errors.sort(key=lambda d: (d.byte_offset, d.code, d.reason, d.field or ""))
    if errors:
        return ParseResult(None, tuple(errors))
    return ParseResult(Document(data, tuple(packets)), ())


def diagnostic_bytes(diagnostics):
    """Safe ASCII JSONL, fixed keys/order, no raw input text or paths."""
    return b"".join((json.dumps(d.as_dict(), ensure_ascii=True, separators=(",", ":"))
                     + "\n").encode("ascii") for d in diagnostics)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (1, 2) or args[0] not in ("check", "parse"):
        sys.stderr.write("usage: composer.py {check|parse} [FILE|-]\n")
        return 64
    try:
        if len(args) == 1 or args[1] == "-":
            data = sys.stdin.buffer.read()
        else:
            with open(args[1], "rb") as source:
                data = source.read()
        result = parse(data)
        if result.diagnostics:
            sys.stdout.buffer.write(diagnostic_bytes(result.diagnostics))
            sys.stdout.flush()
            return 65
        if args[0] == "parse":
            summary = dict(packets=[p.metadata() for p in result.packets])
            sys.stdout.write(json.dumps(summary, ensure_ascii=True, separators=(",", ":")) + "\n")
            sys.stdout.flush()
        return 0
    except (OSError, MemoryError, OverflowError):
        # Close a failed buffered sink here, so interpreter shutdown cannot retry
        # its flush and replace operational exit 74 with shutdown exit 120.
        try:
            sys.stdout.close()
        except OSError:
            pass
        try:
            sys.stderr.write('{"error":"io_or_resource_failure"}\n')
            sys.stderr.flush()
        except OSError:
            try:
                sys.stderr.close()
            except OSError:
                pass
        return 74


if __name__ == "__main__":
    sys.exit(main())
