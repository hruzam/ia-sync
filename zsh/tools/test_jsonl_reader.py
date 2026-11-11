"""Synthetic checks; no private source content belongs in these fixtures."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock

import jsonl_reader as reader
import jsonl_browser as browser


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.cache = self.base / "cache"
        self.source = self.base / "input.jsonl"

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = reader.main(["--cache-dir", str(self.cache), *args])
        return code, out.getvalue(), err.getvalue()

    def write(self, values):
        self.source.write_text("\n".join(json.dumps(v, ensure_ascii=False) for v in values) + "\n")

    def test_load_pick_refresh_clear_preserves_source_and_private_modes(self):
        self.write([{"text": "Příliš žluťoučký", "nested": {"a/b": [True, None, 0]}}, "second"])
        original = self.source.read_bytes()
        self.assertEqual(self.run_cli("load", str(self.source))[0], 0)
        self.assertEqual(self.run_cli("pick", "1-2")[0], 0)
        view = self.cache / "view.md"
        text = view.read_text()
        self.assertIn("Příliš žluťoučký", text)
        self.assertIn("/nested/a~1b/0", text)
        self.assertIn("Type: boolean", text)
        self.assertIn(hashlib.sha256(original).hexdigest(), text)
        for path in (view, self.cache / "snapshot.json"):
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.cache.stat().st_mode), 0o700)
        self.assertEqual(self.source.read_bytes(), original)
        self.write(["changed"])
        self.assertIn("second", self.run_cli("list")[1])
        self.assertEqual(self.run_cli("refresh")[0], 0)
        self.assertFalse(view.exists())
        self.assertEqual(self.run_cli("clear")[0], 0)
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_invalid_lines_and_tail_are_explicit(self):
        self.source.write_bytes(b'{"ok": 1}\nnot-json\n\n{"incomplete":')
        self.assertEqual(self.run_cli("load", str(self.source))[0], 0)
        self.assertIn("INVALID", self.run_cli("list")[1])
        self.assertEqual(self.run_cli("pick", "1-4")[0], 0)
        text = (self.cache / "view.md").read_text()
        self.assertIn("invalid lines (not silently repaired): 2, 3, 4", text)
        self.assertEqual(text.count("INVALID JSON"), 3)

    def test_jev_ledger_refused_without_replacing_existing_snapshot(self):
        self.write(["ordinary"])
        self.run_cli("load", str(self.source))
        before = (self.cache / "snapshot.json").read_bytes()
        self.write([{"schema": "jev.event/v1", "kind": "open"}])
        code, _, err = self.run_cli("load", str(self.source))
        self.assertEqual(code, 2)
        self.assertIn("native validated", err)
        self.assertEqual((self.cache / "snapshot.json").read_bytes(), before)

    def test_markup_controls_and_shell_text_are_literal(self):
        hostile = "```\n<script>x</script>\n![remote](https://invalid/a)\n$(touch /tmp/NO)\x1b[31m\u202eevil"
        rendered = reader.render_value({"x\n# heading": hostile})
        self.assertIn("````text", rendered)
        self.assertIn("\\u001b", rendered)
        self.assertIn("\\u202e", rendered)
        self.assertNotIn("\x1b", rendered)
        self.assertIn("$(touch /tmp/NO)", rendered)

    def test_save_never_overwrites_or_follows_destination_symlink(self):
        self.write([{"text": "keep me"}])
        self.run_cli("load", str(self.source))
        self.run_cli("pick", "1")
        target = self.base / "saved.md"
        self.assertEqual(self.run_cli("save", str(target))[0], 0)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
        self.assertEqual(self.run_cli("save", str(target))[0], 2)
        link = self.base / "link"
        link.symlink_to(self.source)
        self.assertEqual(self.run_cli("save", str(link))[0], 2)

    def test_selection_bounds_and_preview_limits(self):
        self.write(list(range(20)))
        self.run_cli("load", str(self.source))
        for selection in ("0", "4-1", "1,21", "all", ""):
            self.assertEqual(self.run_cli("pick", selection)[0], 2)
        self.assertEqual(self.run_cli("list", "--limit", "0")[0], 2)
        preview = self.run_cli("list", "--start", "15", "--limit", "2")[1]
        self.assertIn("   15", preview)
        self.assertIn("   16", preview)
        self.assertNotIn("   17", preview)

    def test_symlink_cache_and_source_in_cache_are_refused(self):
        actual = self.base / "actual"
        actual.mkdir(mode=0o700)
        self.cache.symlink_to(actual, target_is_directory=True)
        self.assertEqual(self.run_cli("clear")[0], 2)
        self.cache.unlink()
        self.cache.mkdir(mode=0o700)
        inside = self.cache / "input.jsonl"
        inside.write_text('"private"\n')
        self.assertEqual(self.run_cli("load", str(inside))[0], 2)

    def test_non_json_constants_invalid_not_numbers(self):
        self.source.write_text("NaN\nInfinity\n")
        self.run_cli("load", str(self.source))
        self.assertEqual(self.run_cli("list")[1].count("INVALID"), 2)

    def test_reading_index_and_safe_search_path(self):
        self.source = self.base / "a 'quoted' name.jsonl"
        self.write([{"text": "first"}, {"text": "second"}])
        self.run_cli("load", str(self.source))
        self.run_cli("pick", "2")
        text = (self.cache / "view.md").read_text()
        self.assertIn("[Source line 2](#source-line-2)", text)
        self.assertNotIn("[Source line 1](#source-line-1)", text)
        self.assertIn("one physical line", text)
        self.assertIn("grep -n -F -- 'SEARCH'", text)
        self.assertIn("'\"'\"'", text)

    def test_browser_lists_directories_and_jsonl_only(self):
        (self.base / 'folder').mkdir()
        self.source.write_text('{}\n')
        (self.base / 'ignore.md').write_text('x')
        (self.base / 'link.jsonl').symlink_to(self.source)
        self.assertEqual([p.name for p in browser.entries(self.base)], ['folder', 'input.jsonl'])

    def test_browser_marks_record_and_creates_view(self):
        self.write([{"text": "selected"}, {"text": "not selected"}])
        screen = mock.Mock()
        screen.getmaxyx.return_value = (24, 100)
        screen.getch.side_effect = [10, ord(' '), ord('p')]
        def cache():
            self.cache.mkdir(mode=0o700, exist_ok=True)
            return self.cache
        with mock.patch.object(browser.curses, 'curs_set'), mock.patch.object(reader, 'cache_path', side_effect=cache):
            result = browser.browse(screen, self.base)
        self.assertEqual(result, self.cache / 'view.md')
        text = result.read_text()
        self.assertIn('selected', text)
        self.assertNotIn('not selected', text)
        self.assertEqual(json.loads((self.cache / 'snapshot.json').read_text())['selected'], [1])


if __name__ == "__main__":
    unittest.main()
