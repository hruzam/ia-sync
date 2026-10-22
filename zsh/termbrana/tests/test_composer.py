"""Specification witnesses for GRAMMAR.md; no corpus or session dependency."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

FAMILY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FAMILY))
import composer as c


def frame(body=b"alpha\nomega\n", nonce=b"a7b2", eol=b"\n", ident=b"example", extra=b""):
    lines = [b"<!-- composer:packet " + nonce + b" -->", b"format: request/0.1",
             b"id: " + ident, b"from: Majkee", b"to: myShell", b"requested_scope: read-only"]
    return (eol.join(lines) + eol + extra + b"<!-- composer:body " + nonce + b" -->" + eol
            + body + b"<!-- composer:end " + nonce + b" -->" + eol)


def expected(data, offset, code, reason, nonce="a7b2", field=None):
    # Compute coordinates from literal source, independently of parser state.
    prefix = data[:offset].split(b"\n")
    return dict(code=code, reason=reason, byte_offset=offset, line=len(prefix),
                byte_column=len(prefix[-1]) + 1, packet_nonce=nonce, field=field)


class ParserTests(unittest.TestCase):
    def invalid(self, data, diagnostics):
        result = c.parse(data)
        self.assertIsNone(result.document)
        self.assertEqual(result.packets, ())
        self.assertEqual([d.as_dict() for d in result.diagnostics], diagnostics)
        output = c.diagnostic_bytes(result.diagnostics)
        self.assertEqual(output, c.diagnostic_bytes(c.parse(data).diagnostics))
        self.assertTrue(output.isascii())
        self.assertNotIn(b"\x1b", output)
        return result

    def one(self, data):
        result = c.parse(data)
        self.assertEqual(result.diagnostics, ())
        self.assertEqual(len(result.packets), 1)
        self.assertEqual(result.document.to_bytes(), data)
        return result.document, result.packets[0]

    def test_byte_ownership_table_and_body_controls(self):
        bodies = [b"", b"x\n", b"x\n\n", b"x\r\n", b"x\n\r\n", b"x\ry\n",
                  b"\xef\xbb\xbfx\n", "é∇\n".encode(), b"\x00\x1b\x7f\t\n"]
        for eol in (b"\n", b"\r\n"):
            for body in bodies:
                with self.subTest(eol=eol, body=body):
                    source = frame(body, eol=eol)
                    doc, packet = self.one(source)
                    self.assertEqual(source[slice(*packet.body_span)], body)
                    self.assertEqual(source[slice(*packet.header_span)].split(eol)[0], b"format: request/0.1")
                    self.assertEqual(packet.fields["consult"], [])
                    self.assertEqual(packet.fields["context"], [])
                    self.assertEqual(len(packet.frame_spans), 3)

    def test_physical_lines_only_lf(self):
        body = "one\u0085<!-- composer:end a7b2 -->\u2028two\u2029three\n".encode()
        source = frame(body, extra="stop: a\u0085b\u2028c\u2029d\n".encode())
        _, packet = self.one(source)
        self.assertEqual(source[slice(*packet.body_span)], body)
        self.assertEqual(packet.fields["stop"], "a\u0085b\u2028c\u2029d")

    def test_decoded_mutation_cannot_reserialize_source(self):
        source = frame(extra=b'context: ["a,b", no]\n')
        doc, packet = self.one(source)
        packet.fields["id"] = "mutated"
        packet.fields["context"].append("new")
        self.assertEqual(doc.to_bytes(), source)

    def test_immutable_record_api(self):
        diagnostic = c.Diagnostic("FIELD_INVALID", "unknown_key", 12, 2, 1, "a7b2", "program")
        same = c.Diagnostic(code="FIELD_INVALID", reason="unknown_key", byte_offset=12,
                            line=2, byte_column=1, packet_nonce="a7b2", field="program")
        self.assertEqual(diagnostic, same)
        self.assertEqual(hash(diagnostic), hash(same))
        self.assertEqual(list(diagnostic.as_dict()),
                         ["code", "reason", "byte_offset", "line", "byte_column", "packet_nonce", "field"])
        self.assertEqual(repr(diagnostic), "Diagnostic(code='FIELD_INVALID', reason='unknown_key', byte_offset=12, line=2, byte_column=1, packet_nonce='a7b2', field='program')")
        self.assertNotEqual(diagnostic, tuple(diagnostic.as_dict().values()))
        doc, packet = self.one(frame())
        result = c.ParseResult(document=doc, diagnostics=())
        for record, name, value in ((diagnostic, "code", "changed"), (packet, "nonce", "other4"),
                                    (doc, "source", b"changed"), (result, "document", None)):
            with self.assertRaises(AttributeError):
                setattr(record, name, value)
            with self.assertRaises(AttributeError):
                delattr(record, name)
        with self.assertRaises(TypeError):
            hash(packet)  # Mutable decoded fields remain unhashable, as before.

    def test_bom_offsets_and_multiple_packets_outside(self):
        first = frame(eol=b"\r\n")
        second = frame(nonce=b"zz99qq88", ident=b"other")
        source = b"\xef\xbb\xbf" + first + b"notes\rbare\n" + second + b"tail"
        result = c.parse(source)
        self.assertEqual(result.diagnostics, ())
        self.assertEqual(len(result.packets), 2)
        self.assertEqual(result.packets[0].span[0], 3)
        self.assertEqual(result.document.to_bytes(), source)
        bad = b"\xef\xbb\xbf" + frame(extra=b"program: []\n")
        self.invalid(bad, [expected(bad, bad.index(b"program:"), "FIELD_INVALID", "unknown_key", field="program")])

    def test_marker_lookalikes_are_body_data(self):
        body = (b"<!-- composer:packet a7b2 -->\n<!-- composer:body a7b2 -->\n"
                b"<!-- composer:end other4 -->\n <!-- composer:end a7b2 -->\n"
                b"<!-- composer:end a7b2 --> \n<!-- composer:end a7b2 --\n"
                b"<!-- composer:end BAD! -->\ninline <!-- composer:end a7b2 -->\n"
                b"```\n---\nfrom: anyone\nctrl a&b && program: other\n```\n")
        source = frame(body)
        _, packet = self.one(source)
        self.assertEqual(source[slice(*packet.body_span)], body)

    def test_first_closer_insertion_and_unrecorded_intent_limit(self):
        source = frame(b"alpha\n<!-- composer:end a7b2 -->\nomega\n")
        at = source.rindex(b"<!-- composer:end a7b2 -->")
        self.invalid(source, [expected(source, at, "BOUNDARY_INVALID", "nonce_reused")])
        no_true_end = source[:at]
        _, packet = self.one(no_true_end)
        self.assertEqual(no_true_end[slice(*packet.body_span)], b"alpha\n")

    def test_end_at_eof_and_wrong_first_closer_eol(self):
        self.one(frame()[:-1])
        self.one(frame(eol=b"\r\n")[:-2])
        for eol, bad in ((b"\n", b"\r\n"), (b"\r\n", b"\n")):
            source = frame(eol=eol)
            source = source[:-len(eol)] + bad + b"<!-- composer:end a7b2 -->" + eol
            at = source.index(bad, source.index(b"<!-- composer:end a7b2 -->"))
            self.invalid(source, [expected(source, at, "BOUNDARY_INVALID", "frame_eol")])

    def test_missing_end_and_unrepresentable_body(self):
        prefix = frame().split(b"alpha\n", 1)[0]
        for suffix in (b"", b"x", b"x\r", b"<!-- composer:end other4 -->\n",
                       b"<!-- composer:end a7b2 --", b"<!-- composer:end a7b2 -->\r",
                       b"x<!-- composer:end a7b2 -->\n"):
            source = prefix + suffix
            self.invalid(source, [expected(source, len(source), "BOUNDARY_INVALID", "missing_end")])

    def test_utf8_validation_precedes_structure(self):
        for bad in (b"\xff", b"\xc3", b"\xed\xa0\x80", b"\xf0\x80\x80\x80"):
            source = frame() + bad
            self.invalid(source, [expected(source, len(frame()), "ENCODING_INVALID", "invalid_utf8", None)])

    def test_nonce_and_marker_errors(self):
        for line in (b"<!-- composer:packet abc -->\n", b"<!-- composer:packet abcdefghi -->\n",
                     b" <!-- composer:packet a7b2 -->\n", b"<!-- composer:Packet a7b2 -->\n",
                     b"<!-- composer:packet AB12 -->\n", b"<!-- composer:packet a7b2 --> \n",
                     b"<!-- composer:packet a7b2 -->\r"):
            self.invalid(line, [expected(line, 0, "BOUNDARY_INVALID", "marker_syntax", None)])
        line = b"<!-- composer:end a7b2 -->"
        self.invalid(line, [expected(line, 0, "BOUNDARY_INVALID", "marker_order")])
        source = frame() + frame(ident=b"two")
        self.invalid(source, [expected(source, len(frame()), "BOUNDARY_INVALID", "nonce_reused")])
        source = frame().replace(b"<!-- composer:body a7b2 -->", b"<!-- composer:body other4 -->")
        self.invalid(source, [expected(source, source.index(b"<!-- composer:body"), "BOUNDARY_INVALID", "marker_order")])

    def test_missing_body_and_syntax_eol(self):
        opening = b"<!-- composer:packet a7b2 -->"
        self.invalid(opening, [expected(opening, len(opening), "BOUNDARY_INVALID", "frame_eol")])
        source = opening + b"\n"
        self.invalid(source, [expected(source, len(source), "BOUNDARY_INVALID", "missing_body")])
        for line in (b"format: request/0.1\r\n", b"format: request/0.1\rrest\n", b"format: request/0.1"):
            source = opening + b"\n" + line
            at = source.index(b"\r") if b"\r" in source else len(source)
            self.invalid(source, [expected(source, at, "BOUNDARY_INVALID", "frame_eol")])
        source = frame().split(b"<!-- composer:body", 1)[0] + b"<!-- composer:body a7b2 -->"
        self.invalid(source, [expected(source, len(source), "BOUNDARY_INVALID", "frame_eol")])

    def test_five_required_fields_and_sorting(self):
        fields = ((b"format", b"request/0.1"), (b"id", b"example"), (b"from", b"Majkee"),
                  (b"to", b"myShell"), (b"requested_scope", b"read-only"))
        for key, value in fields:
            source = frame().replace(key + b": " + value + b"\n", b"")
            at = source.index(b"<!-- composer:body")
            self.invalid(source, [expected(source, at, "FIELD_MISSING", "required_absent", field=key.decode())])
        source = frame()
        for key, value in fields:
            source = source.replace(key + b": " + value + b"\n", b"")
        at = source.index(b"<!-- composer:body")
        self.invalid(source, [expected(source, at, "FIELD_MISSING", "required_absent", field=k)
                              for k in ("format", "from", "id", "requested_scope", "to")])

    def test_removed_keys_whitelist_precedence(self):
        for key in (b"program", b"function"):
            for value in (b"journal", b"[]", b"[a]", b"", b'""', b'"broken', b"[[x]]"):
                with self.subTest(key=key, value=value):
                    line = key + b": " + value + b"\n"
                    source = frame(extra=line + line)
                    first = source.index(line)
                    self.invalid(source, [expected(source, p, "FIELD_INVALID", "unknown_key", field=key.decode())
                                          for p in (first, first + len(line))])
            for line, reason in ((key+b":\n", "header_syntax"), (key+b":\t[]\n", "header_line"),
                                 (b" "+key+b": []\n", "header_line")):
                source = frame(extra=line)
                self.invalid(source, [expected(source, source.index(line), "HEADER_INVALID", reason)])
            source = frame(extra=key+b": []\r\n")
            self.invalid(source, [expected(source, source.index(b"\r"), "BOUNDARY_INVALID", "frame_eol")])

    def test_flat_scalars_no_coercion_and_json(self):
        for value, decoded in (("no", "no"), ("2026-10-17", "2026-10-17"), ("01234567", "01234567"),
                               ('"\\u0030x"', "0x"), ('"a,b[\\\"x\\\"]"', 'a,b["x"]'),
                               ('"\\ud83d\\ude00"', "😀"), ("a ‘quote’ b", "a ‘quote’ b"),
                               ("a:b # literal `x` && \\p", "a:b # literal `x` && \\p")):
            source = frame(extra=("stop: " + value + "  \n").encode())
            _, packet = self.one(source)
            self.assertEqual(packet.fields["stop"], decoded)
            self.assertIsInstance(packet.fields["stop"], str)

    def test_invalid_scalars_and_shape(self):
        for value, reason, code in ((b"", "empty_value", "FIELD_MISSING"),
                                    (b'""', "empty_value", "FIELD_MISSING"),
                                    (b"[]", "wrong_shape", "FIELD_INVALID"),
                                    (b"{}", "wrong_shape", "FIELD_INVALID"),
                                    (b'"\\n"', "invalid_string", "FIELD_INVALID"),
                                    (b'"\\ud800"', "invalid_string", "FIELD_INVALID"),
                                    (b"'quoted'", "invalid_string", "FIELD_INVALID"),
                                    ('“smart”'.encode(), "invalid_string", "FIELD_INVALID"),
                                    (b'"\\ufeff"', "invalid_string", "FIELD_INVALID"),
                                    (b'"x" tail', "invalid_string", "FIELD_INVALID"),
                                    (b"a\x1bb", "invalid_string", "FIELD_INVALID")):
            source = frame(extra=b"stop: " + value + b"\n")
            self.invalid(source, [expected(source, source.index(b"stop:"), code, reason, field="stop")])

    def test_lists(self):
        for value, decoded in ((b"[]", []), (b"[Astrobley, Astrobley]", ["Astrobley", "Astrobley"]),
                               (b'["a,b", "[x]", no, 01234567]', ["a,b", "[x]", "no", "01234567"]),
                               (b'["a\\\"b", "c\\\\d"]', ['a"b', 'c\\d'])):
            _, packet = self.one(frame(extra=b"context: " + value + b"\n"))
            self.assertEqual(packet.fields["context"], decoded)
        for value in (b"[a,]", b"[,a]", b"[a,,b]", b"[[]]", b"[{x}]", b'[""]',
                      b'["\\t"]', b'["x"oops]', b"[a]tail", b"[a #comment, 'b']"):
            source = frame(extra=b"context: " + value + b"\n")
            self.invalid(source, [expected(source, source.index(b"context:"), "FIELD_INVALID", "invalid_list", field="context")])
        for value in (b"scalar", b"{}", b""):
            source = frame(extra=b"consult: " + value + b"\n")
            self.invalid(source, [expected(source, source.index(b"consult:"), "FIELD_INVALID", "wrong_shape", field="consult")])

    def test_header_lines_version_and_duplicates(self):
        for line, reason, code, key in ((b"\n", "header_line", "HEADER_INVALID", None),
                                       (b"#comment\n", "header_line", "HEADER_INVALID", None),
                                       (b"to:x\n", "header_syntax", "HEADER_INVALID", None),
                                       (b"Body: x\n", "unknown_key", "FIELD_INVALID", "Body"),
                                       (b"body_bytes: 5\n", "unknown_key", "FIELD_INVALID", "body_bytes"),
                                       (b"to: again\n", "duplicate_key", "FIELD_INVALID", "to")):
            source = frame(extra=line)
            at = source.index(b"<!-- composer:body") - len(line)
            self.invalid(source, [expected(source, at, code, reason, field=key)])
        source = frame().replace(b"request/0.1", b"request/9")
        self.invalid(source, [expected(source, source.index(b"format:"), "HEADER_INVALID", "unsupported_format", field="format")])
        source = frame().replace(b"from: Majkee", b"from: ")
        source = source.replace(b"<!-- composer:body", b"from: second\n<!-- composer:body")
        self.invalid(source, [expected(source, source.index(b"from:"), "FIELD_MISSING", "empty_value", field="from"),
                              expected(source, source.index(b"from: second"), "FIELD_INVALID", "duplicate_key", field="from")])

    def test_aggregate_independent_errors_then_structural_stop(self):
        first = frame(extra=b"program: []\n")
        second = frame(nonce=b"bbb2", ident=b"second", extra=b"function: \n")
        third = frame(nonce=b"ccc3", ident=b"third").split(b"alpha\n", 1)[0] + b"unclosed\n"
        source = first + second + third
        self.invalid(source, [expected(source, source.index(b"program:"), "FIELD_INVALID", "unknown_key", field="program"),
                              expected(source, source.index(b"function:"), "FIELD_INVALID", "unknown_key", "bbb2", "function"),
                              expected(source, len(source), "BOUNDARY_INVALID", "missing_end", "ccc3")])
        source = frame() + frame(nonce=b"bbb2")
        self.invalid(source, [expected(source, source.index(b"id: example", len(frame())), "FIELD_INVALID", "duplicate_id", "bbb2", "id")])

    def test_packet_free_documents_and_outside_fences(self):
        for source in (b"", b"notes\n<!-- COMPOSER:packet a7b2 -->\n", b"\xef\xbb\xbf", b"inline <!-- composer:packet a7b2 -->"):
            self.invalid(source, [expected(source, 0, "BOUNDARY_INVALID", "no_packets", None)])
        source = b"```\n" + frame() + b"```\n"
        self.one(source)

    def test_no_reference_loading_or_payload_execution(self):
        body = b"$(touch /tmp/tbc-SHOULD-NOT-EXIST)\n`false`\n&& exec nonsense\nprogram: other\n"
        source = frame(body, extra=b"context: [/not/a/real/reference]\n")
        with patch.object(Path, "read_bytes", side_effect=AssertionError("reference opened")), \
                patch("subprocess.Popen", side_effect=AssertionError("child started")), \
                patch("os.system", side_effect=AssertionError("shell started")), \
                patch("builtins.eval", side_effect=AssertionError("eval called")):
            doc, packet = self.one(source)
            self.assertEqual(doc.source[slice(*packet.body_span)], body)


class CLITests(unittest.TestCase):
    def cli(self, mode, data):
        return subprocess.run([sys.executable, "-B", str(FAMILY / "composer.py"), mode, "-"],
                              input=data, capture_output=True, check=False)

    def test_success_and_safe_metadata(self):
        data = frame(b"\x1b[31mBODY SECRET\x00\n", ident="é\u2028id".encode())
        checked = self.cli("check", data)
        self.assertEqual((checked.returncode, checked.stdout, checked.stderr), (0, b"", b""))
        parsed = self.cli("parse", data)
        self.assertEqual(parsed.returncode, 0)
        self.assertEqual(parsed.stderr, b"")
        self.assertTrue(parsed.stdout.isascii())
        self.assertNotIn(b"BODY SECRET", parsed.stdout)
        self.assertNotIn(b"\x1b", parsed.stdout)
        self.assertEqual(json.loads(parsed.stdout)["packets"][0]["fields"]["id"], "é\u2028id")

    def test_invalid_output_exact_and_no_prefix(self):
        bad = frame() + frame(nonce=b"bbb2", ident=b"second", extra=b"program: \x1b\n")
        at = bad.index(b"program:")
        obj = expected(bad, at, "FIELD_INVALID", "unknown_key", "bbb2", "program")
        golden = (json.dumps(obj, separators=(",", ":")) + "\n").encode()
        for mode in ("check", "parse"):
            outputs = [self.cli(mode, bad) for _ in range(2)]
            for result in outputs:
                self.assertEqual((result.returncode, result.stdout, result.stderr), (65, golden, b""))

    def test_explicit_file_io_failure_and_usage(self):
        with tempfile.TemporaryDirectory(prefix="tbc-cli-") as directory:
            path = Path(directory) / "source.md"
            path.write_bytes(frame())
            before = path.read_bytes()
            run = subprocess.run([sys.executable, "-B", str(FAMILY / "composer.py"), "check", str(path)], capture_output=True)
            self.assertEqual((run.returncode, run.stdout, run.stderr), (0, b"", b""))
            self.assertEqual(path.read_bytes(), before)
            run = subprocess.run([sys.executable, "-B", str(FAMILY / "composer.py"), "check", str(path)+"missing"], capture_output=True)
            self.assertEqual((run.returncode, run.stdout, run.stderr), (74, b"", b'{"error":"io_or_resource_failure"}\n'))
        run = self.cli("invented", b"")
        self.assertEqual(run.returncode, 64)

    @unittest.skipUnless(Path("/dev/full").exists(), "requires a failing output sink")
    def test_buffered_output_failure_is_operational(self):
        for mode, data in (("parse", frame()), ("check", frame(extra=b"program: x\n"))):
            with open("/dev/full", "wb") as sink:
                result = subprocess.run([sys.executable, "-B", str(FAMILY / "composer.py"), mode, "-"],
                                        input=data, stdout=sink, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 74)
            self.assertEqual(result.stderr, b'{"error":"io_or_resource_failure"}\n')


if __name__ == "__main__":
    unittest.main()
