"""Native Jev Markdown reader acceptance with a temporary private vault."""

import hashlib
from html.parser import HTMLParser
import importlib.util
import sys
import tempfile
from pathlib import Path
import unittest
from unittest import mock
from types import SimpleNamespace
import markdown

BED = Path(__file__).resolve().parents[1]
SOURCE = BED.parents[2] / "zsh" / "jev"
sys.path.insert(0, str(SOURCE))
import kernel
import store
cli_spec = importlib.util.spec_from_file_location("reader_cli", SOURCE / "jev.py")
cli = importlib.util.module_from_spec(cli_spec)
cli_spec.loader.exec_module(cli)
reader_spec = importlib.util.spec_from_file_location("reader", SOURCE / "reader.py")
reader = importlib.util.module_from_spec(reader_spec)
reader_spec.loader.exec_module(reader)
import browser


class ParsedView(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.values, self.current = [], [], None

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'pre':
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == 'pre' and self.current is not None:
            self.values.append(''.join(self.current))
            self.current = None


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.project = self.work / "project"
        self.bed = self.project / "bed"
        self.bed.mkdir(parents=True)
        self.root = self.work / "vault"
        self.vault = store.Vault(self.root)
        self.session = self.vault.open(self.project, self.bed)["session_id"]
        packet = kernel.load(BED / "tests/fixtures/brief-missing.json")
        packet["session_id"] = self.session
        packet["target"] = "hostile `text`\x1b[2J stays data"
        packet_path = self.work / "packet.json"
        packet_path.write_bytes(kernel.canonical(packet))
        with self.vault.selected(self.session) as ledger:
            self.prepared = cli.prepare(ledger, packet_path)
            reply = {"schema": "jev.receipt/v1", "request_id": self.prepared["request_id"],
                     "packet_sha256": self.prepared["prepared"]["packet_sha256"], "model": "synthetic",
                     "answers": [{"id": "missing", "type": "noul", "probability": 0.5}]}
            reply_path = self.work / "reply.json"
            reply_path.write_bytes(kernel.canonical(reply))
            cli.import_reply(ledger, self.prepared["request_id"], reply_path)
        self.ledger = next(self.root.rglob("*.jsonl"))

    def test_native_replay_renders_questions_results_provenance_and_keeps_bytes(self):
        before = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        content = reader.read(self.root, self.session, self.prepared["request_id"])
        after = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertIn("# Jev reading view", content)
        self.assertIn("`prepare`", content)
        self.assertIn("`reply`", content)
        self.assertIn("`questions`", content)
        self.assertIn("`answers`", content)
        self.assertIn(self.prepared["request_id"], content)
        self.assertIn("\\u001b", content)
        self.assertNotIn("body_base64", content)

    def test_output_is_explicit_private_markdown(self):
        content = reader.read(self.root, self.session)
        output_root = self.work / "views"
        output_root.mkdir(mode=0o700)
        output = output_root / "view.md"
        self.assertEqual(reader.write_output(output, content), output)
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        self.assertEqual(output.read_text(), content)
        with self.assertRaises(kernel.Invalid):
            reader.write_output(output, "must not overwrite")
        self.assertEqual(output.read_text(), content)

    def test_output_requires_private_parent_and_cli_requires_explicit_path(self):
        self.work.chmod(0o755)
        with self.assertRaises(kernel.Invalid):
            reader.write_output(self.work / "not-private.md", "view")
        with self.assertRaises(kernel.Invalid):
            reader.parser().parse_args(["--session", self.session])

    def test_contextual_redaction_keeps_evidence_and_preserves_literal_text(self):
        view = "\n".join(reader._value({"authorization": {"grant": "secret"},
                                          "raw_base64": "payload", "body_base64": "request"},
                                         event_kind="attempt"))
        self.assertNotIn("secret", view)
        evidence = "\n".join(reader._value({"evidence": {"authorization": "ordinary evidence", "body_base64": "ordinary text"}},
                                              event_kind="prepare"))
        self.assertIn("ordinary evidence", evidence)
        self.assertIn("ordinary text", evidence)
        literal = "\n".join(reader._value({"unsafe``key\n<script>alert(1)</script>": "first\n\tsecond\n"}))
        self.assertIn("```unsafe``key\\n<script>alert(1)</script>```", literal)
        self.assertIn("first\n&#9;second\n", literal)

    def test_full_render_keeps_nested_untrusted_content_inert_and_readable(self):
        note = 'Příliš 日本語\n\tIndented\n\n```sh\n</pre><script>alert(1)</script>\n```\n\x1b[31m'
        hostile_key = 'unsafe``key\n<script>alert(2)</script>'
        event = {'sequence': 2, 'kind': 'memory', 'event_id': 'event-2', 'at': 'recorded-time',
                 'request_id': None, 'previous_event_id': 'event-1',
                 'actor': {'cli_sessions': {'codex': 'original-codex', 'claude': 'original-claude',
                                            'gemini': None, 'controller': None},
                           'name': 'jev', 'requester': 'author', 'source': 'record'},
                 'data': {'note': {'text': note, hostile_key: '<img src=x onerror=alert(3)>'}}}
        ledger = SimpleNamespace(events=[event], path=self.ledger, session_id=self.session, tail=None)
        source = reader.render(ledger, sequences={2})
        for extensions in ([], ['fenced_code']):
            parsed = ParsedView()
            parsed.feed(markdown.markdown(source, extensions=extensions))
            self.assertFalse({'script', 'img'} & set(parsed.tags), extensions)
            self.assertIn(reader._text(note), parsed.values, extensions)
            self.assertIn('<img src=x onerror=alert(3)>', parsed.values, extensions)
            self.assertIn('original-codex', parsed.values, extensions)
            self.assertIn('original-claude', parsed.values, extensions)
            self.assertIn('Selected sequences: `2`', source)
            self.assertIn('event-2', source)

    def test_full_event_tilde_fences_preserve_decoded_text(self):
        cases = ['before\n~~~html\n<script>DEMO_ONLY</script>\n~~~\nafter',
                 'before\n\n~~~\nliteral\n~~~\n\nafter']
        for text in cases:
            event = {'sequence': 1, 'kind': 'memory', 'event_id': 'fixture', 'at': 'fixture',
                     'request_id': None, 'previous_event_id': None,
                     'actor': {'cli_sessions': {'codex': 'original-codex'}},
                     'data': {'note': {'text': text}}}
            ledger = SimpleNamespace(events=[event], path=self.ledger, session_id=self.session, tail=None)
            source = reader.render(ledger)
            for extensions in ([], ['fenced_code']):
                parsed = ParsedView()
                parsed.feed(markdown.markdown(source, extensions=extensions))
                self.assertIn(text, parsed.values, (text, extensions))
                self.assertNotIn('script', parsed.tags, (text, extensions))
                self.assertIn('original-codex', parsed.values, (text, extensions))
                self.assertIn('fixture', source)

    def test_missing_vault_is_not_created(self):
        missing = self.work / "missing"
        with self.assertRaises(kernel.Invalid):
            reader.read(missing, "0" * 32)
        self.assertFalse(missing.exists())

    def test_browser_discovers_and_composes_selected_verified_event(self):
        before = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        vault, sessions = browser.discover(self.root)
        self.assertEqual(sessions[0]['session'], self.session)
        self.assertEqual(sessions[0]['bed'], str(self.bed))
        screen = mock.Mock()
        screen.getmaxyx.return_value = (24, 120)
        screen.getch.side_effect = [10, browser.curses.KEY_DOWN, ord(' '), ord('p')]
        runtime = self.work / 'runtime'
        runtime.mkdir(mode=0o700)
        with mock.patch.object(browser.curses, 'curs_set'), mock.patch.dict('os.environ', {'XDG_RUNTIME_DIR': str(runtime)}):
            result = browser.browse(screen, vault, sessions)
        text = result.read_text()
        self.assertIn('Selected sequences: `2`', text)
        self.assertIn('`prepare`', text)
        self.assertNotIn('### 3.', text)
        self.assertEqual(result.stat().st_mode & 0o777, 0o600)
        self.assertEqual(before, hashlib.sha256(self.ledger.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
