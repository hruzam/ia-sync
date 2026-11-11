"""Actual zsh attachment checks, with temporary vaults and no provider calls."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[4]
SOURCE = REPO / "zsh" / "jev"


@unittest.skipUnless(shutil.which("zsh"), "zsh is required for shell verification")
class ShellTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="jev shell proof-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        project = self.root / "project"
        bed = project / "bed"
        bed.mkdir(parents=True)
        self.vault = self.root / "vault"
        result = subprocess.run(
            [sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.vault),
             "open", "--project", str(project), "--bed", str(bed)],
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.session = json.loads(result.stdout)["session_id"]

    def shell(self, script, root=None):
        return subprocess.run(
            ["zsh", "-f", "-c", script, "jev-proof", str(SOURCE / "base.zsh"),
             str(root or self.vault), self.session], text=True, capture_output=True)

    def test_attachment_scope_failure_preservation_and_detach(self):
        result = self.shell('''
unset JEV_ROOT JEV_SESSION JEV_CHANNEL
source "$1" || exit
source "$1" || exit
[[ ${aliases[jev]} == _jev ]] || exit 10
_jev_use "$2" "$3" >/dev/null || exit
_jev settings || exit
_jev --root "$2" settings >/dev/null 2>&1 && exit 11
_jev_use "$2" bad-id >/dev/null 2>&1 && exit 12
[[ $JEV_SESSION == "$3" ]] || exit 13
_jev_off || exit
[[ -z ${JEV_SESSION:-} && -z ${JEV_CHANNEL:-} && -z ${JEV_ROOT:-} ]] || exit 14
_jev settings >/dev/null 2>&1 && exit 15
exit 0
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        settings = json.loads(result.stdout)
        self.assertEqual(settings["session_id"], self.session)
        self.assertIsNone(settings["budget"]["total_usd"])

    def test_source_is_silent_inert_and_symlink_root_refuses(self):
        missing = self.root / "not-created"
        result = self.shell('''
unset JEV_ROOT JEV_SESSION JEV_CHANNEL
source "$1" || exit
source "$1" || exit
export JEV_ROOT="$2"
_jev --help >/dev/null
''', missing)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout + result.stderr, "")
        self.assertFalse(missing.exists())
        linked = self.root / "alias"
        linked.symlink_to(self.vault, target_is_directory=True)
        result = self.shell('source "$1"; _jev_use "$2" "$3"', linked)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stdout)

    def test_provenance_globals_route_open_help_and_selected_operations(self):
        second_bed = self.root / "project" / "second"
        second_bed.mkdir()
        fixture = REPO / ".dev/session/jev-01-codex-pilot/tests/fixtures/brief-missing.json"
        packet = json.loads(fixture.read_bytes())
        packet["session_id"] = self.session
        (self.root / "packet.json").write_text(json.dumps(packet))
        result = self.shell('''
unset JEV_ROOT JEV_SESSION JEV_CHANNEL
source "$1" || exit
export JEV_ROOT="$2"
_jev --cli codex --cli-session Shell.Open --requester hlm open \
  --project "${2:h}/project" --bed "${2:h}/project/second" || exit
_jev --cli=gemini --cli-session=Help.Session --requester=hlm --help >/dev/null || exit
_jev --cli claude --cli-session Help.Request prepare --help >/dev/null || exit
_jev_use "$2" "$3" >/dev/null || exit
_jev --cli claude --cli-session Shell.Prepare --requester agent prepare "${2:h}/packet.json" || exit
_jev --cli=gemini --cli-session=Shell.Reader --requester=hlm settings || exit
_jev --cli codex --cli-session Shell.Reopen --requester hlm open \
  --project "${2:h}/project" --bed "${2:h}/project/bed" || exit
_jev --cli gemini --cli-session Block.Override --root "$2" settings >/dev/null 2>&1 && exit 20
exit 0
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        opening, prepared, settings, reopened = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertNotEqual(opening["session_id"], self.session)
        self.assertEqual(prepared["event"]["actor"]["cli_sessions"]["claude"], "Shell.Prepare")
        self.assertEqual(prepared["event"]["actor"]["requester"], "agent")
        self.assertEqual(settings["session_id"], self.session)
        self.assertEqual(reopened["session_id"], self.session)
        events = [json.loads(line) for line in Path(opening["ledger"]).read_bytes().splitlines()]
        self.assertEqual(events[0]["actor"]["cli_sessions"]["codex"], "Shell.Open")
        self.assertEqual(events[0]["actor"]["requester"], "hlm")

    def test_unattached_explicit_selectors_and_invalid_provenance_do_not_attach(self):
        result = self.shell('''
unset JEV_ROOT JEV_SESSION JEV_CHANNEL
source "$1" || exit
_jev --cli gemini --cli-session Explicit.Session --requester hlm \
  --root "$2" --session "$3" --channel main settings || exit
_jev --cli codex --cli-session Unattached.Session settings >/dev/null 2>&1 && exit 20
[[ -z ${JEV_ROOT:-} && -z ${JEV_SESSION:-} && -z ${JEV_CHANNEL:-} ]] || exit 21
_jev --cli codex --cli-session 'bad/value' --root "$2" \
  --session "$3" --channel main settings >/dev/null 2>&1 && exit 22
exit 0
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["session_id"], self.session)


if __name__ == "__main__":
    unittest.main()
