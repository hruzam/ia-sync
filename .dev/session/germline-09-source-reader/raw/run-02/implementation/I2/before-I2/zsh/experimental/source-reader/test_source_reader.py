#!/usr/bin/env python3
"""Offline acceptance checks using immutable fixtures; never execute source bodies."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
ENGINE = HERE / "source-reader.py"
SPEC = importlib.util.spec_from_file_location("source_reader", ENGINE)
READER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READER)


def roots():
    data = json.loads((FIXTURES / "roots.json").read_text())["roots"]
    for root in data:
        root["absolute_path"] = str(FIXTURES / Path(root["absolute_path"]).name)
    return data


def inventory():
    return {str(path.relative_to(FIXTURES)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in FIXTURES.rglob("*") if path.is_file()}


class ReaderAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = inventory()
        cls.data = READER.catalog(roots())
        # The immutable audit map is source-tree specific. Tests relocate it in memory.
        cls.runner = [sys.executable, "-B", str(ENGINE), "--roots", str(FIXTURES / "roots.json")]

    @classmethod
    def tearDownClass(cls):
        if inventory() != cls.before:
            raise AssertionError("fixture inputs changed")
        if list(FIXTURES.rglob("CANARY_EXECUTED")):
            raise AssertionError("source instruction executed")

    def cli(self, *args):
        return subprocess.run(self.runner + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def test_offline_help_never_discovers(self):
        with mock.patch.object(READER, "load_roots", side_effect=AssertionError("help must not discover")):
            with mock.patch.object(sys, "argv", [str(ENGINE), "--roots", "/no/such/config", "--help"]):
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as result:
                    READER.main()
        self.assertEqual(result.exception.code, 0)

    def test_catalog_metadata_not_bodies(self):
        real_open = Path.open
        reads = []
        configured_roots = roots()

        class MetadataOnly:
            def __init__(self, path, *args, **kwargs):
                self.path = path
                self.stream = real_open(path, *args, **kwargs)

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.stream.close()

            def readline(self, size):
                self.assert_no_chapter()
                line = self.stream.readline(size)
                reads.append(line)
                return line

            def assert_no_chapter(self):
                if self.path.parent.name == "res":
                    raise AssertionError("catalog read chapter contents")

        with mock.patch.object(Path, "read_bytes", side_effect=AssertionError("catalog read a body")):
            with mock.patch.object(Path, "open", lambda path, *args, **kwargs: MetadataOnly(path, *args, **kwargs)):
                data = READER.catalog(configured_roots)
        self.assertNotIn(b"GUIDE_BODY_NOT_IN_CATALOG\n", reads)
        text = json.dumps(data)
        self.assertNotIn("SELECTED_BODY", text)
        self.assertNotIn("INSTRUCTION:", text)
        self.assertIn("activation unknown", data["notice"])
        self.assertTrue(all(e["activation"] == "unknown" for e in data["entries"]))

    def test_discovery_bounds_and_gaps(self):
        entries = self.data["entries"]
        paths = {e["absolute_path"] for e in entries}
        self.assertNotIn(str(FIXTURES / "codex/deep/hidden/SKILL.md"), paths)
        self.assertNotIn(str(FIXTURES / "guides/topic/raw/side.md"), paths)
        self.assertNotIn(str(FIXTURES / "germline/tunnel/NEVER.md"), paths)
        status = {r["id"]: r["availability"] for r in self.data["roots"]}
        self.assertEqual(status["empty-fixture"], "empty")
        self.assertEqual(status["missing-fixture"], "missing")
        self.assertEqual({e["family"] for e in entries}, {"skill", "guide", "germline"})
        self.assertTrue(any(e["root_id"] == "sync-fixture" for e in entries))
        self.assertEqual(READER.catalog([])["entries"], [])

    def test_unreadable_root_disclosed(self):
        with mock.patch.object(READER, "children", side_effect=PermissionError("fixture unreadable")):
            data = READER.catalog(roots()[:1])
        self.assertEqual(data["roots"][0]["availability"], "unreadable")
        self.assertTrue(data["gaps"])

    def test_duplicates_ids_paths_and_bytes(self):
        twins = [e for e in self.data["entries"] if Path(e["absolute_path"]).parent.name == "guide" and e["source_file_kind"] == "native SKILL.md"]
        self.assertGreaterEqual(len(twins), 3)
        self.assertEqual(len({e["id"] for e in self.data["entries"]}), len(self.data["entries"]))
        again = READER.catalog(roots())
        self.assertEqual([e["id"] for e in self.data["entries"]], [e["id"] for e in again["entries"]])
        for entry in twins:
            for selection in (entry["id"], entry["absolute_path"]):
                result = self.cli("show", selection)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, Path(entry["absolute_path"]).read_bytes())
                self.assertEqual(hashlib.sha256(result.stdout).hexdigest(), hashlib.sha256(Path(entry["absolute_path"]).read_bytes()).hexdigest())
        linked = next(e for e in self.data["entries"] if "/linked/" in e["absolute_path"])
        self.assertEqual(linked["symlink_target"], str(FIXTURES / "claude/guide/SKILL.md"))
        self.assertEqual(self.cli("show", linked["id"]).stdout, (FIXTURES / "claude/guide/SKILL.md").read_bytes())

    def test_show_rejects_name_and_uncataloged_path(self):
        for selection in ("guide", str(FIXTURES / "guides/topic/raw/side.md")):
            result = self.cli("show", selection)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"")

    def test_canary_is_inert_data(self):
        path = FIXTURES / "codex/canary/SKILL.md"
        result = self.cli("show", str(path))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, path.read_bytes())
        self.assertFalse((FIXTURES / "CANARY_EXECUTED").exists())

    def test_guide_slug_and_unique_chapter(self):
        for args, path in ((("guide", "topic"), "guides/topic/GUIDE.md"), (("guide", "topic", "UNIQUE"), "guides/topic/res/unique.md")):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, (FIXTURES / path).read_bytes())
            self.assertIn(b"verified 2000-01-01 is stale", result.stderr)

    def test_guide_ambiguity_no_bodies(self):
        result = self.cli("guide", "topic", "TURNS")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"fanout-turns.md\nturns-recovery.md\n")
        self.assertNotIn(b"CHAPTER_BODY", result.stdout)

    def test_guide_zero_match_manifest_only_no_side_resolution(self):
        for query in ("missing", "side"):
            result = self.cli("guide", "topic", query)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"## Manifest\n- res/fanout-turns.md\n- res/turns-recovery.md\n- res/unique.md\n- raw/\n\n")
            self.assertNotIn(b"NOT_MANIFEST", result.stdout)
            self.assertNotIn(b"NEVER_AUTO_RESOLVE_SIDE", result.stdout)

    def test_guide_catalog_and_unknown_slug(self):
        for args, code in ((("guide",), 0), (("guide", "absent"), 2)):
            result = self.cli(*args)
            self.assertEqual(result.returncode, code)
            self.assertIn(b"Fixture guide", result.stdout)
            self.assertIn(b"fanout-turns.md", result.stdout)
            self.assertNotIn(b"GUIDE_BODY_NOT_IN_CATALOG", result.stdout)

    def test_noninteractive_browse_plain_and_roots_option(self):
        for args in (("browse",), ("browse", "--plain"), ("catalog", "--json", "--roots", str(FIXTURES / "roots.json"))):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b"activation unknown", result.stdout)
            self.assertNotIn(b"SELECTED_BODY", result.stdout)

    def test_plain_terminal_selection_keeps_stdout_exact(self):
        source_input = io.StringIO("1\n")
        source_input.isatty = lambda: True
        output = io.BytesIO()
        target = io.TextIOWrapper(output, encoding="utf-8")
        with mock.patch.object(sys, "stdin", source_input), mock.patch.object(sys, "stdout", target):
            with contextlib.redirect_stderr(io.StringIO()) as terminal:
                code = READER.browse(self.data, True)
        target.flush()
        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), Path(self.data["entries"][0]["absolute_path"]).read_bytes())
        self.assertIn("Read number", terminal.getvalue())
        target.detach()


if __name__ == "__main__":
    unittest.main(verbosity=2)
