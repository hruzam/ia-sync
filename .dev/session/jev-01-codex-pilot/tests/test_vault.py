"""Temporary-root persistence, concurrency, recovery and integrity acceptance."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

BED = Path(__file__).resolve().parents[1]
SOURCE = BED.parents[2] / "zsh" / "jev"
sys.path.insert(0, str(SOURCE))
import kernel
import store
spec = importlib.util.spec_from_file_location("vault_cli", SOURCE / "jev.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class VaultCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.project = self.work / "project"
        self.bed = self.project / "bed"
        self.bed.mkdir(parents=True)
        self.root = self.work / "vault"
        self.vault = store.Vault(self.root)
        self.settings = self.vault.open(self.project, self.bed)
        self.session = self.settings["session_id"]

    def file(self, name, value, raw=False):
        path = self.work / name
        path.write_bytes(value if raw else kernel.canonical(value))
        return path

    def packet(self):
        packet = kernel.load(BED / "tests/fixtures/brief-missing.json")
        packet["session_id"] = self.session
        return packet

    def prepare(self, **kwargs):
        path = self.file("packet.json", self.packet())
        with self.vault.selected(self.session) as ledger:
            return cli.prepare(ledger, path, **kwargs)

    def receipt(self, prepared):
        expected = kernel.load(BED / "tests/fixtures/expected.json")
        return {"schema": "jev.receipt/v1", "request_id": prepared["request_id"],
                "packet_sha256": prepared["packet_sha256"], "model": expected["model"],
                "answers": expected["answers_by_case"][prepared["packet"]["case_id"]]}

    def run_cli(self, *args, selected=True, expected=0):
        argv = [sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.root)]
        if selected:
            argv += ["--session", self.session, "--channel", "main"]
        result = subprocess.run([*argv, *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)


class VaultTests(VaultCase):
    def test_subprocess_restart_roundtrip_and_exact_reference(self):
        packet = self.file("packet.json", self.packet())
        prepared = self.run_cli("prepare", packet)
        request = prepared["request_id"]
        receipt = self.file("reply.json", self.receipt(prepared["prepared"]))
        reply = self.run_cli("import-reply", request, receipt)
        self.assertEqual(reply["data"]["source"], "synthetic")
        policy = BED / "tests/fixtures/policy.json"
        question = next(q["id"] for q in self.packet()["questions"] if q["type"] == "noul")
        result = self.run_cli("interpret", request, question, policy)
        self.assertIn(result["data"]["result"]["status"], {"NO", "YES", "UNCERTAIN"})
        self.run_cli("dispose", request, "use", "--consumer", "codex")
        self.run_cli("dispose", request, "reconsider", "--consumer", "operator", "--reason", "later evidence")
        outcome = self.file("outcome.json", {"adjudication": "synthetic label", "refs": [reply["event_id"]]})
        self.run_cli("outcome", request, outcome)
        history = self.run_cli("show", "--request", request)
        self.assertEqual([event["kind"] for event in history["events"]],
                         ["prepare", "reply", "interpret", "dispose", "dispose", "outcome"])
        reference = self.run_cli("ref", request)
        self.assertEqual(reference["event_id"], reply["event_id"])
        self.assertEqual(reference["sequence"], 3)
        self.assertEqual(reference["kind"], "reply")
        self.assertEqual(reference["prepared_event_id"], prepared["event"]["event_id"])
        self.assertEqual(Path(reference["ledger"]), Path(self.settings["ledger"]))

    def test_no_creation_on_import_help_absent_read_invalid_id_or_failed_open(self):
        missing = self.work / "missing"
        for arguments in (["--help"], ["--session", "../bad", "--channel", "main", "settings"],
                          ["--session", "0" * 32, "--channel", "main", "show"],
                          ["open", "--project", str(self.project), "--bed", str(self.work)]):
            result = subprocess.run([sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(missing), *arguments],
                                    capture_output=True)
            self.assertEqual(result.returncode, 0 if arguments == ["--help"] else 2)
            self.assertFalse(missing.exists())
        probe = "from unittest.mock import patch; from pathlib import Path; " + \
                "patcher=patch.object(Path, 'home', side_effect=AssertionError('home consulted on import')); " + \
                "patcher.start(); import jev,store,provider"
        result = subprocess.run([sys.executable, "-B", "-c", probe], cwd=SOURCE, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(missing.exists())

    def test_open_immutable_idempotent_and_concurrent_processes(self):
        command = [sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.root), "open",
                   "--project", str(self.project), "--bed", str(self.bed)]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(4)]
        for process in processes:
            out, err = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, err + out)
            self.assertEqual(json.loads(out)["session_id"], self.session)
        with self.assertRaises(store.Invalid):
            self.vault.open(self.project, self.bed, "1")
        self.assertEqual(len(list(self.root.rglob("*.jsonl"))), 1)
        self.assertEqual(len(list(self.root.rglob("*.lock"))), 1)

    def test_concurrent_mutations_have_complete_unique_sequence(self):
        request = self.prepare()["request_id"]
        command = [sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.root),
                   "--session", self.session, "--channel", "main", "dispose", request, "skip", "--consumer"]
        processes = [subprocess.Popen([*command, str(i)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(8)]
        for process in processes:
            out, err = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, out + err)
        with self.vault.selected(self.session) as ledger:
            self.assertEqual([event["sequence"] for event in ledger.events], list(range(1, 11)))
            self.assertEqual(len({event["event_id"] for event in ledger.events}), 10)
            self.assertEqual(len(ledger.related(request, "dispose")), 8)

    def test_private_modes_and_refused_symlink_managed_paths(self):
        for path in [self.root, *self.root.rglob("*")]:
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700 if path.is_dir() else 0o600)
        link = self.work / "alias"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(store.Invalid):
            store.Vault(link)
        ledger = Path(self.settings["ledger"])
        saved = ledger.read_bytes()
        ledger.unlink()
        target = self.file("foreign", saved, raw=True)
        target.chmod(0o600)
        ledger.symlink_to(target)
        with self.assertRaises(store.Invalid):
            with self.vault.selected(self.session):
                pass
        self.assertEqual(target.read_bytes(), saved)

    def test_insecure_existing_root_lock_or_ledger_refused(self):
        for path, restored in [(self.root, 0o700), (Path(self.settings["ledger"]), 0o600),
                               (Path(self.settings["ledger"]).with_suffix(".lock"), 0o600)]:
            with self.subTest(path=path):
                path.chmod(0o755 if path.is_dir() else 0o644)
                with self.assertRaises(store.Invalid):
                    with self.vault.selected(self.session):
                        pass
                self.assertNotEqual(stat.S_IMODE(path.stat().st_mode), restored)
                path.chmod(restored)

    def test_memory_selection_lineage_are_explicit_and_frozen(self):
        first = self.prepare()
        with self.vault.selected(self.session) as ledger:
            note = {"version": "1", "author": "operator", "text": "useful reminder", "refs": [first["event"]["event_id"]]}
            memory = ledger.append("memory", {"note": note})
            selection = {"policy": {"id": "manual", "version": "1"}, "items": [
                {"event_id": first["event"]["event_id"], "excerpt": "brief-check"}], "layers": ["synthetic"]}
            selected = ledger.append("select", {"selection": selection})
        lineage = {"branch": "manual", "step": "2", "parent_request_ids": [first["request_id"]],
                   "reconsider_of": first["request_id"], "reason": "new evidence"}
        later = self.prepare(memory=memory["event_id"], selection=selected["event_id"], lineage=lineage)
        saved = copy.deepcopy(later)
        note["text"] = "mutated"
        selection["items"][0]["excerpt"] = "mutated"
        lineage["step"] = "changed after return"
        # Returned objects cannot mutate durable bytes; replay uses the saved snapshot.
        with self.vault.selected(self.session) as ledger:
            event = ledger.request(later["request_id"])
            self.assertEqual(event, saved["event"])
            self.assertEqual(event["data"]["prepared"]["packet"]["memory"]["text"], "useful reminder")
            self.assertEqual(event["data"]["lineage"]["step"], "2")
        without = self.prepare()
        self.assertNotIn("jev_selection", without["prepared"]["packet"]["state"])
        self.assertNotEqual(without["prepared"]["packet"].get("memory", {}).get("text"), "useful reminder")

    def test_cross_session_references_and_nonexistent_excerpts_refused(self):
        first = self.prepare()
        other_bed = self.project / "other"
        other_bed.mkdir()
        other = self.vault.open(self.project, other_bed)["session_id"]
        with self.vault.selected(other) as ledger:
            with self.assertRaises(store.Invalid):
                ledger.append("memory", {"note": {"version": "1", "author": "operator", "text": "foreign",
                                                  "refs": [first["event"]["event_id"]]}})
            with self.assertRaises(store.Invalid):
                ledger.lineage({"branch": "x", "step": "1", "parent_request_ids": [first["request_id"]]})
        with self.vault.selected(self.session) as ledger:
            with self.assertRaises(store.Invalid):
                ledger.append("select", {"selection": {"policy": {"id": "x", "version": "1"},
                    "items": [{"event_id": first["event"]["event_id"], "excerpt": "not anywhere in canonical bytes 12345"}]}})

    def test_malformed_and_semantically_invalid_receipts_are_losslessly_recorded(self):
        for raw in (b'{"broken":', b'{"schema":"not-a-receipt"}', b'\xff\xfe'):
            request = self.prepare()["request_id"]
            with self.vault.selected(self.session) as ledger:
                event = cli.import_reply(ledger, request, self.file("bad.json", raw, raw=True))
                self.assertEqual(event["data"]["validation"]["status"], "INVALID")
                self.assertEqual(store.decode_bytes(event["data"]["raw_base64"]), raw)
                with self.assertRaises(store.Invalid):
                    cli.import_reply(ledger, request, self.file("again.json", raw, raw=True))
            with self.vault.selected(self.session) as ledger:
                self.assertEqual(len(ledger.related(request, "reply")), 1)

    def test_interpret_errors_still_have_policy_question_request_receipt_references(self):
        prepared = self.prepare()
        request = prepared["request_id"]
        with self.vault.selected(self.session) as ledger:
            result = cli.interpret(ledger, request, "unknown", self.file("bad-policy", b'{', raw=True))
            self.assertEqual(result["data"]["result"]["status"], "ERROR")
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.events[-1], result)

    def test_missing_lf_read_prefix_reconcile_then_append(self):
        result = self.prepare()
        path = Path(self.settings["ledger"])
        full = path.read_bytes()
        path.write_bytes(full[:-1])
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.tail["kind"], "missing_lf")
            self.assertEqual(len(ledger.events), 1)
            with self.assertRaises(store.Invalid):
                ledger.append("memory", {"note": {"version": "1", "author": "x", "text": "x", "refs": []}})
            self.assertEqual(ledger.reconcile()["status"], "COMPLETED_LF")
            self.assertEqual(path.read_bytes(), full)
        with self.vault.selected(self.session) as ledger:
            self.assertIsNone(ledger.tail)
            self.assertEqual(ledger.request(result["request_id"]), result["event"])

    def test_malformed_tail_recovery_preserves_exact_bytes_and_proof(self):
        request = self.prepare()["request_id"]
        path = Path(self.settings["ledger"])
        prefix = path.read_bytes()
        fragment = b'{"partial":"\xff trailing'
        with path.open("ab") as output:
            output.write(fragment)
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.tail["kind"], "malformed")
            result = ledger.reconcile()
            proof = result["event"]["data"]
            self.assertEqual(proof["offset"], len(prefix))
            self.assertEqual(proof["length"], len(fragment))
            self.assertEqual(proof["sha256"], hashlib.sha256(fragment).hexdigest())
            ledger.append("dispose", {"decision": "skip", "consumer": "operator", "reason": ""}, request)
        self.assertTrue(path.read_bytes().startswith(prefix + fragment + b"\n"))
        with self.vault.selected(self.session) as ledger:
            self.assertIsNone(ledger.tail)
            self.assertEqual(ledger.events[-2]["kind"], "recovery")
            self.assertEqual(ledger.budget()["liabilities"][-1]["status"], "UNKNOWN_FRAGMENT")

    def test_middle_corruption_unknown_recovery_and_hash_semantic_tamper_fail_closed(self):
        self.prepare()
        path = Path(self.settings["ledger"])
        original = path.read_bytes()
        opening, preparation = original.splitlines(keepends=True)
        for broken in (opening + b'{bad}\n' + preparation,
                       opening + preparation + b'{bad}\n{"kind":"recovery"',
                       opening + preparation + b'{bad}\n[]\n',
                       opening + preparation.replace(b'"kind":"prepare"', b'"kind":"dispose"')):
            with self.subTest(broken=broken[-80:]):
                path.write_bytes(broken)
                with self.assertRaises(store.Invalid):
                    with self.vault.selected(self.session):
                        pass
                self.assertEqual(path.read_bytes(), broken)
        event = json.loads(preparation)
        event["data"]["prepared"]["packet"]["target"] = "edited but event hash updated"
        event["event_id"] = store.event_hash(event)
        path.write_bytes(opening + kernel.canonical(event) + b"\n")
        with self.assertRaises(store.Invalid):
            with self.vault.selected(self.session):
                pass

    def test_duplicate_session_id_in_another_engagement_refused(self):
        other_bed = self.project / "other"
        other_bed.mkdir()
        other = self.vault.open(self.project, other_bed)
        path = Path(other["ledger"])
        event = json.loads(path.read_bytes())
        event["session_id"] = self.session
        event["event_id"] = store.event_hash(event)
        path.write_bytes(kernel.canonical(event) + b"\n")
        with self.assertRaisesRegex(store.Invalid, "duplicate"):
            with self.vault.selected(self.session):
                pass

    def test_decimal_exactness_and_invalid_amounts(self):
        for invalid in ("-1", "NaN", "Infinity", True, 1, "1e-2", ".1", "0.0000000000000000001", "1000000000000000000"):
            with self.subTest(value=invalid), self.assertRaises(store.Invalid):
                store.money(invalid)
        amount = "999999999999999999.999999999999999999"
        self.assertEqual(store.decimal_text(store.total([store.money(amount), store.money("0.000000000000000001")])),
                         "1000000000000000000.000000000000000000")


if __name__ == "__main__":
    unittest.main()
