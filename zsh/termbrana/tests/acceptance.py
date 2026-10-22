#!/usr/bin/env python3
"""Explicit test tooling: frozen references in, evidence directory out. Not runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import composer
from test_composer import expected, frame

# Independent frozen source facts, not merely trust in the supplied inventory.
REFERENCES = (
    ("raw/EXCHANGE.md", 0, 10307, "dde73d06a5710ce1fd512bb33b21e1460c1533644510d53f3b40319ed15b7379", "dde73d06a5710ce1fd512bb33b21e1460c1533644510d53f3b40319ed15b7379"),
    ("raw/sella-v.0.1/EXCHANGE.md", 0, 8459, "1d19e0077002a70fb9f12e7fee7fa29295a457a5201a8e60688943ff5a0fdffd", "1d19e0077002a70fb9f12e7fee7fa29295a457a5201a8e60688943ff5a0fdffd"),
    ("raw/sella-v.0.1/brief.oraculum.sella-v.0.1.md", 0, 5499, "8299e178bf9754a1353ec1193e74930ee4161b2d06b9925ebc2dd54b5649818d", "8299e178bf9754a1353ec1193e74930ee4161b2d06b9925ebc2dd54b5649818d"),
    ("raw/journal.2026-10-16.md", 2061, 16595, "456d1c5eefb142beb4b07f20dcf1463d3ea0a82c690c8f0ac7f4f13b3a6b8337", "dc1590fb2f935a6ae05efd10e32847d28a9ab3831ef2d35de85d4212dd124e54"),
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bed", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    fixtures = out / "fixtures"
    fixtures.mkdir(exist_ok=True)
    family = Path(__file__).resolve().parents[1]
    records = []
    inventory = json.loads((args.bed / "evidence/corpus-inventory.cartan.json").read_text())["items"]
    source_before = {}
    bodies, wrapped = [], []

    def compare(name, expected_bytes, actual):
        wanted, got = out / (name + ".expected"), out / (name + ".actual")
        wanted.write_bytes(expected_bytes)
        got.write_bytes(actual)
        command = ["cmp", "--", str(wanted), str(got)]
        result = subprocess.run(command, capture_output=True)
        records.append(dict(command=command, exit=result.returncode))
        assert result.returncode == 0, name

    def cli(name, data, code=0, diagnostics=b""):
        path = fixtures / (name + ".md")
        path.write_bytes(data)
        command = [sys.executable, "-B", str(family / "composer.py"), "check", str(path)]
        runs = [subprocess.run(command, capture_output=True) for _ in range(2)]
        for result in runs:
            assert (result.returncode, result.stdout, result.stderr) == (code, diagnostics, b""), name
        records.append(dict(command=command, repeats=2, exit=code,
                            stdout_sha256=digest(runs[0].stdout), stderr=""))
        if code:
            compare(name + ".diagnostics", diagnostics, runs[0].stdout)
        return path

    for index, (relative, start, end, source_hash, body_hash) in enumerate(REFERENCES):
        path = args.bed / relative
        raw = path.read_bytes()
        item = inventory[index]
        assert (item["body_byte_start_inclusive"], item["body_byte_end_exclusive"]) == (start, end)
        assert item["source_sha256"] == source_hash and item["body_sha256"] == body_hash
        assert digest(raw) == source_hash
        body = raw[start:end]
        assert digest(body) == body_hash and body.endswith(b"\n")
        if index == 3:
            lines = raw.split(b"\n")
            assert b"\n".join(lines[38:407]) + b"\n" == body
            assert lines[407].startswith(b"# 2. JEV")
        source_before[str(path)] = source_hash
        bodies.append(body)
        for label, eol in (("lf", b"\n"), ("crlf", b"\r\n")):
            nonce = ("r%dzz" % index).encode()
            assert b"<!-- composer:end " + nonce + b" -->" not in body
            data = frame(body, nonce=nonce, eol=eol, ident=("source-%d" % index).encode())
            result = composer.parse(data)
            assert not result.diagnostics and len(result.packets) == 1
            packet = result.packets[0]
            compare("corpus-%d-%s.body" % (index, label), body, data[slice(*packet.body_span)])
            compare("corpus-%d-%s.packet" % (index, label), data, data[slice(*packet.span)])
            compare("corpus-%d-%s.document" % (index, label), data, result.document.to_bytes())
            cli("corpus-%d-%s" % (index, label), data)
            if (index % 2 == 0) == (label == "lf"):
                wrapped.append(data)
    mixed = b"\xef\xbb\xbfoutside\n" + b"notes between\n".join(wrapped) + b"outside tail"
    result = composer.parse(mixed)
    assert len(result.packets) == 4 and not result.diagnostics
    compare("mixed.document", mixed, result.document.to_bytes())
    for index, packet in enumerate(result.packets):
        compare("mixed-%d.body" % index, bodies[index], mixed[slice(*packet.body_span)])
        compare("mixed-%d.packet" % index, wrapped[index], mixed[slice(*packet.span)])
    cli("corpus.mixed", mixed)

    handwritten = args.bed / "evidence/fixtures/packet.handwritten.v4.md"
    data = handwritten.read_bytes()
    source_before[str(handwritten)] = digest(data)
    result = composer.parse(data)
    assert not result.diagnostics and len(result.packets) == 1
    start = data.index(b"<!-- composer:body hand4z -->\n") + len(b"<!-- composer:body hand4z -->\n")
    end = data.index(b"\n<!-- composer:end hand4z -->") + 1
    compare("handwritten.body", data[start:end], data[slice(*result.packets[0].body_span)])
    compare("handwritten.document", data, result.document.to_bytes())
    cli("handwritten", data)

    grammar = (args.bed / "evidence/grammar.builder.v4.md").read_text()
    example_section = grammar.split("## 7. Complete examples", 1)[1].split("## 8.", 1)[0]
    examples = re.findall(r"```text\n(.*?)```", example_section, re.S)
    assert len(examples) == 4
    for index in (0, 1, 3):
        data = examples[index].encode()
        result = composer.parse(data)
        assert not result.diagnostics and len(result.packets) == 1
        compare("grammar-example-%d.document" % index, data, result.document.to_bytes())
        cli("grammar-example-%d" % index, data)

    cases = []
    old_fixture = args.bed / "evidence/fixtures/packet.handwritten.v3.md"
    old = old_fixture.read_bytes()
    source_before[str(old_fixture)] = digest(old)
    cases.append(("historical-v3", old,
                  [expected(old, old.index(key+b": "), "FIELD_INVALID", "unknown_key", "hand7z", key.decode())
                   for key in (b"program", b"function")]))
    for key in (b"program", b"function"):
        for number, value in enumerate((b"journal", b"[]", b"[x]", b"", b'""', b'"broken', b"[[x]]")):
            line = key + b": " + value + b"\n"
            data = frame(extra=line + line)
            at = data.index(line)
            cases.append((key.decode()+str(number), data,
                          [expected(data, p, "FIELD_INVALID", "unknown_key", field=key.decode())
                           for p in (at, at+len(line))]))
    data = frame(b"alpha\n<!-- composer:end a7b2 -->\nomega\n")
    cases.append(("insertion", data, [expected(data, data.rindex(b"<!-- composer:end"), "BOUNDARY_INVALID", "nonce_reused")]))
    data = frame().replace(b"<!-- composer:end a7b2 -->\n", b"<!-- composer:end a7b2 -->\r\n<!-- composer:end a7b2 -->\n")
    cases.append(("first-wrong-eol", data, [expected(data, data.index(b"\r"), "BOUNDARY_INVALID", "frame_eol")]))
    data = frame() + b"\xff"
    cases.append(("invalid-utf8", data, [expected(data, len(data)-1, "ENCODING_INVALID", "invalid_utf8", None)]))
    data = frame(b"x")
    cases.append(("no-final-body-lf", data, [expected(data, len(data), "BOUNDARY_INVALID", "missing_end")]))
    for key in (b"format", b"id", b"from", b"to", b"requested_scope"):
        lines = frame().split(b"\n")
        data = b"\n".join(line for line in lines if not line.startswith(key+b": "))
        cases.append(("missing-"+key.decode(), data, [expected(data, data.index(b"<!-- composer:body"), "FIELD_MISSING", "required_absent", field=key.decode())]))
    for name, data, objects in cases:
        golden = b"".join((json.dumps(obj, separators=(",", ":"))+"\n").encode() for obj in objects)
        result = composer.parse(data)
        assert result.document is None and result.packets == ()
        assert composer.diagnostic_bytes(result.diagnostics) == golden
        cli("negative-"+name, data, 65, golden)

    sentinel = out / "must-not-exist"
    assert not sentinel.exists()
    payload = ("$(touch %s)\n`touch %s`\n&& exec false\nprogram: text\n" % (sentinel, sentinel)).encode()
    data = frame(payload, extra=b"context: [/does/not/exist]\n")
    cli("non-execution", data)
    assert not sentinel.exists()
    for path, before in source_before.items():
        assert digest(Path(path).read_bytes()) == before
    report = dict(reference_identities=source_before, journal_extent=[2061,16595],
                  body_bytes=sum(map(len, bodies)), commands=records,
                  sentinel_absent=True, source_unchanged=True,
                  valid_serialized_bytes=len(mixed), status="PASS")
    (out / "acceptance.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status":"PASS", "cmp_checks":sum(r["command"][0]=="cmp" for r in records),
                      "cli_cases":sum("repeats" in r for r in records), "body_bytes":report["body_bytes"]}))


if __name__ == "__main__":
    main()
