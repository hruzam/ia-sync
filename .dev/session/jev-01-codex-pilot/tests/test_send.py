"""Offline sends only: injected confirmation, dummy credential and mocked transport."""

from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest import mock
import unittest

from test_vault import VaultCase, SOURCE, cli
import kernel
import provider
import store


class SendTests(VaultCase):
    def setUp(self):
        super().setUp()
        self.root = self.work / "send-vault"
        self.vault = store.Vault(self.root)
        self.settings = self.vault.open(self.project, self.bed, "1.000000000000000001", "synthetic/model")
        self.session = self.settings["session_id"]
        self.calls = []
        self.fake_key = "synthetic-never-real-credential-material-0123456789"

    def make_request(self, bound="0.25"):
        return self.prepare(upper_bound=bound, bound_evidence="synthetic offline conservative bound")

    def wire(self, prepared, cost="0.1", model="synthetic/model", invalid=False):
        internal = self.receipt(prepared)
        by_id = {question["id"]: question for question in prepared["packet"]["questions"]}
        answers = {}
        for answer in internal["answers"]:
            kind = answer["type"]
            mapped = {"type": kind, {"noul": "noul", "choice": "choice", "score": "score"}[kind]:
                      answer["probability" if kind == "noul" else "value"]}
            if kind != "noul":
                mapped.update(probabilities=answer["probabilities"], confidence=answer.get("confidence", 0.5))
            if kind == "score":
                mapped["legend"] = {str(i): label for i, label in enumerate(by_id[answer["id"]]["levels"])}
            answers[answer["id"]] = mapped
        if invalid:
            answers = {}
        value = {"model": model, "id": "synthetic-generation", "answers": answers, "usage": {}}
        raw = kernel.canonical(value)
        # Preserve exact numeric cost token (including exponent and long precision).
        return raw.replace(b'"usage":{}', b'"usage":{"cost":' + cost.encode() + b'}') if cost is not None else raw

    def invoke(self, prepared, raw=None, status=200, **seams):
        if raw is None:
            raw = self.wire(prepared["prepared"])
        def confirm(value, digest):
            self.calls.append(("confirm", digest, value))
            return True
        def credential(path):
            self.calls.append(("credential", str(path)))
            # Fresh replay proves the reservation is on disk before credential/transport.
            events = [json.loads(line) for line in Path(self.settings["ledger"]).read_bytes().splitlines()]
            self.assertEqual(events[-1]["kind"], "attempt")
            return self.fake_key
        def transport(body, key):
            self.calls.append(("transport", body, key))
            return status, raw
        defaults = {"confirm": confirm, "credential": credential, "transport": transport, "guard": lambda: None}
        defaults.update(seams)
        return cli.send(self.vault, self.session, prepared["request_id"], self.work / "never-read-real-credential", **defaults)

    def test_success_exact_saved_bytes_and_distinct_confirmation_per_request(self):
        hashes = []
        for _ in range(2):
            prepared = self.make_request()
            expected_bytes = store.decode_bytes(prepared["event"]["data"]["provider"]["body_base64"])
            # Changing the input file after prepare cannot change transport.
            self.file("packet.json", b'{"edited":true}', raw=True)
            result = self.invoke(prepared)
            self.assertEqual(result["status"], "SETTLED")
            self.assertEqual(result["validation"]["status"], "VALID")
            confirm, credential, transport = self.calls[-3:]
            self.assertEqual([entry[0] for entry in (confirm, credential, transport)], ["confirm", "credential", "transport"])
            self.assertEqual(transport[1], expected_bytes)
            self.assertEqual(confirm[2]["body_utf8"].encode(), expected_bytes)
            hashes.append(confirm[1])
        self.assertNotEqual(*hashes)
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(Decimal(ledger.budget()["spent_usd"]), Decimal("0.2"))
            self.assertEqual(ledger.budget()["reserved_usd"], "0")
            self.assertFalse(ledger.budget()["liabilities"])
            self.assertEqual([event["kind"] for event in ledger.events][-4:], ["attempt", "http", "reply", "settle"])

    def test_cancel_and_guard_rejection_touch_neither_credential_nor_transport(self):
        prepared = self.make_request()
        credential, transport = mock.Mock(side_effect=AssertionError("credential touched")), mock.Mock(side_effect=AssertionError("transport touched"))
        result = self.invoke(prepared, confirm=lambda value, digest: False, credential=credential, transport=transport)
        self.assertEqual(result["status"], "CANCELLED")
        def reject():
            raise kernel.Invalid("agent refused")
        with self.assertRaises(kernel.Invalid):
            self.invoke(prepared, guard=reject, credential=credential, transport=transport)
        credential.assert_not_called()
        transport.assert_not_called()
        with self.vault.selected(self.session) as ledger:
            self.assertFalse(ledger.related(prepared["request_id"], "attempt"))

    def test_production_agent_and_noninteractive_guards_before_credentials(self):
        prepared = self.make_request()
        with mock.patch.dict(os.environ, {"CODEX_THREAD_ID": "synthetic"}, clear=True), \
                mock.patch.object(cli, "read_credential") as credential, mock.patch.object(provider, "post") as transport:
            with self.assertRaisesRegex(kernel.Invalid, "agent"):
                cli.send(self.vault, self.session, prepared["request_id"], "nonexistent")
            credential.assert_not_called()
            transport.assert_not_called()
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(cli.sys.stdin, "isatty", return_value=False):
            with self.assertRaisesRegex(kernel.Invalid, "terminal"):
                cli.guard_human()
        result = subprocess.run([sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.root),
                                 "--session", self.session, "--channel", "main", "send", prepared["request_id"],
                                 "--credential-file", str(self.work / "missing")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("credential unavailable", result.stdout)
        self.assertEqual(len(self.run_cli("show")["events"]), 2)

    def test_no_yes_or_persisted_approval_flag(self):
        prepared = self.make_request()
        for flag in ("--yes", "--approve", "--approval-hash"):
            result = self.run_cli("send", prepared["request_id"], "--credential-file", "dummy", flag, expected=2)
            self.assertEqual(result["status"], "ERROR")

    def test_unset_budget_missing_bound_and_exceeded_allowance_reject_before_spies(self):
        confirm, credential, transport = mock.Mock(), mock.Mock(), mock.Mock()
        for prepared in (self.prepare(), self.make_request("2")):
            with self.assertRaises(kernel.Invalid):
                self.invoke(prepared, confirm=confirm, credential=credential, transport=transport)
        other = self.project / "unset"
        other.mkdir()
        settings = self.vault.open(self.project, other, model="synthetic/model")
        packet = self.packet()
        packet["session_id"] = settings["session_id"]
        with self.vault.selected(settings["session_id"]) as ledger:
            prepared = cli.prepare(ledger, self.file("unset.json", packet), upper_bound="0.01", bound_evidence="synthetic")
        with self.assertRaisesRegex(kernel.Invalid, "UNSET"):
            cli.send(self.vault, settings["session_id"], prepared["request_id"], "dummy", guard=lambda: None,
                     confirm=confirm, credential=credential, transport=transport)
        confirm.assert_not_called()
        credential.assert_not_called()
        transport.assert_not_called()

    def test_transport_unknown_is_durable_blocks_all_sends_and_synthetic_settlement(self):
        prepared = self.make_request()
        def broken(body, key):
            raise RuntimeError("untrusted exception contains " + key)
        result = self.invoke(prepared, transport=broken)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["budget"]["reserved_usd"], "0.25")
        self.assertEqual(result["budget"]["spent_usd"], "0")
        self.assertNotIn(self.fake_key, kernel.canonical(result).decode())
        self.assertNotIn(self.fake_key.encode(), Path(self.settings["ledger"]).read_bytes())
        next_request = self.make_request()
        with self.assertRaisesRegex(kernel.Invalid, "liability"):
            self.invoke(next_request)
        with self.vault.selected(self.session) as ledger:
            with self.assertRaises(kernel.Invalid):
                cli.import_reply(ledger, prepared["request_id"], self.file("synthetic", self.receipt(prepared["prepared"])))
        self.assertEqual([item[0] for item in self.calls], ["confirm", "credential"])

    def test_crash_after_attempt_retains_unknown_reservation_after_restart(self):
        prepared = self.make_request()
        with self.vault.selected(self.session) as ledger:
            approval = ledger.approval(prepared["request_id"])
            ledger.append("attempt", {"upper_bound_usd": "0.25", "approval_sha256": approval[1],
                                      "prepared_event_id": prepared["event"]["event_id"]}, prepared["request_id"])
        settings = self.run_cli("settings")
        self.assertEqual(settings["budget"]["reserved_usd"], "0.25")
        self.assertEqual(settings["budget"]["liabilities"][0]["status"], "UNKNOWN")
        with self.assertRaises(kernel.Invalid):
            self.invoke(prepared)

    def test_missing_malformed_and_unrepresentable_cost_preserve_raw_and_block(self):
        for index, cost in enumerate((None, '"bad"', "-1", "1e100000", "1e-100000")):
            # Each uncertain attempt needs a separate immutable engagement for this fixture.
            if index:
                bed = self.project / str(index)
                bed.mkdir()
                self.settings = self.vault.open(self.project, bed, "1", "synthetic/model")
                self.session = self.settings["session_id"]
            prepared = self.make_request()
            raw = self.wire(prepared["prepared"], cost=cost)
            result = self.invoke(prepared, raw=raw)
            self.assertEqual(result["status"], "UNKNOWN")
            with self.vault.selected(self.session) as ledger:
                self.assertEqual(store.decode_bytes(ledger.related(prepared["request_id"], "http")[0]["data"]["raw_base64"]), raw)
                self.assertEqual(store.decode_bytes(ledger.related(prepared["request_id"], "reply")[0]["data"]["raw_base64"]), raw)
                self.assertTrue(ledger.budget()["liabilities"])

    def test_invalid_advice_and_model_still_settle_valid_billed_cost(self):
        for bad_model, invalid in (("synthetic/model", True), ("unallowed/model", False)):
            prepared = self.make_request()
            raw = self.wire(prepared["prepared"], cost="0.100000000000000001", model=bad_model, invalid=invalid)
            result = self.invoke(prepared, raw=raw)
            self.assertEqual(result["status"], "SETTLED")
            self.assertEqual(result["validation"]["status"], "INVALID")
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.budget()["spent_usd"], "0.200000000000000002")
            self.assertFalse(ledger.budget()["liabilities"])

    def test_http_non2xx_cost_never_trusted_or_retried(self):
        prepared = self.make_request()
        transport = mock.Mock(return_value=(302, self.wire(prepared["prepared"], cost="0")))
        result = self.invoke(prepared, transport=transport)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["budget"]["spent_usd"], "0")
        transport.assert_called_once()
        with self.assertRaises(kernel.Invalid):
            self.invoke(prepared)
        transport.assert_called_once()

    def test_actual_overrun_recorded_without_clamping_and_blocks_future_send(self):
        prepared = self.make_request("0.01")
        result = self.invoke(prepared, raw=self.wire(prepared["prepared"], cost="1.1"))
        self.assertEqual(result["status"], "OVERRUN")
        self.assertEqual(result["budget"]["spent_usd"], "1.1")
        self.assertEqual(result["budget"]["available_usd"], "-0.099999999999999999")
        self.assertEqual(result["budget"]["overrun_request_ids"], [prepared["request_id"]])
        with self.assertRaisesRegex(kernel.Invalid, "overrun"):
            self.invoke(self.make_request("0"))

    def test_duplicate_send_rejected_and_intentional_retry_is_new_occurrence_with_lineage(self):
        prepared = self.make_request()
        self.invoke(prepared)
        calls = len(self.calls)
        with self.assertRaises(kernel.Invalid):
            self.invoke(prepared)
        self.assertEqual(len(self.calls), calls)
        retry = self.prepare(upper_bound="0.25", bound_evidence="synthetic", lineage={
            "branch": "repeat", "step": "2", "parent_request_ids": [prepared["request_id"]],
            "retry_of": prepared["request_id"], "reason": "fresh synthetic sample"})
        self.assertNotEqual(retry["request_id"], prepared["request_id"])
        self.assertEqual(self.invoke(retry)["status"], "SETTLED")

    def test_credential_permissions_nonsymlink_and_ambient_key_never_used(self):
        path = self.file("dummy-key", self.fake_key.encode(), raw=True)
        path.chmod(0o600)
        self.assertEqual(cli.read_credential(path), self.fake_key)
        path.chmod(0o644)
        with self.assertRaises(kernel.Invalid):
            cli.read_credential(path)
        path.chmod(0o600)
        link = self.work / "key-link"
        link.symlink_to(path)
        with self.assertRaises(kernel.Invalid):
            cli.read_credential(link)
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": self.fake_key}):
            with self.assertRaises(kernel.Invalid):
                cli.read_credential(self.work / "missing-key")

    def test_lock_held_through_confirmation_and_attempt_settlement(self):
        prepared = self.make_request()
        def confirm(value, digest):
            result = self.run_cli("settings", expected=2)
            self.assertIn("busy", result["errors"][0])
            return True
        self.assertEqual(self.invoke(prepared, confirm=confirm)["status"], "SETTLED")

    def test_json_escaped_credential_echo_is_withheld_with_unknown_liability(self):
        prepared = self.make_request()
        escaped = "".join("\\u%04x" % ord(character) for character in self.fake_key).encode()
        raw = self.wire(prepared["prepared"]).replace(b"synthetic-generation", escaped)
        self.assertNotIn(self.fake_key.encode(), raw)
        self.assertEqual(json.loads(raw)["id"], self.fake_key)
        result = self.invoke(prepared, raw=raw)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertTrue(result["budget"]["liabilities"])
        self.assertNotIn(self.fake_key, kernel.canonical(result).decode())
        self.assertNotIn(self.fake_key.encode(), Path(self.settings["ledger"]).read_bytes())
        self.assertNotIn(escaped, Path(self.settings["ledger"]).read_bytes())
        with self.vault.selected(self.session) as ledger:
            self.assertFalse(ledger.related(prepared["request_id"], "http"))
            self.assertFalse(ledger.related(prepared["request_id"], "reply"))
            self.assertEqual(ledger.related(prepared["request_id"], "uncertain")[0]["data"]["reason"], "transport")

    def test_mocked_send_records_current_caller_without_relabelling_preparer(self):
        prepared = self.make_request()
        self.vault = store.Vault(self.root, cli_sessions={"codex": "Send.Caller", "claude": None,
                                                       "gemini": None, "controller": None}, requester="hlm")
        self.assertEqual(self.invoke(prepared)["status"], "SETTLED")
        with self.vault.selected(self.session) as ledger:
            self.assertIsNone(ledger.request(prepared["request_id"])["actor"]["requester"])
            for kind in ("attempt", "http", "reply", "settle"):
                event = ledger.related(prepared["request_id"], kind)[0]
                self.assertEqual(event["actor"]["cli_sessions"]["codex"], "Send.Caller")
                self.assertEqual(event["actor"]["requester"], "hlm")

    def test_hlm_and_explicit_cli_flags_do_not_bypass_production_agent_guard(self):
        prepared = self.make_request()
        result = subprocess.run([sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(self.root),
                                 "--session", self.session, "--channel", "main", "--cli", "claude",
                                 "--cli-session", "Explicit.Caller", "--requester", "hlm", "send",
                                 prepared["request_id"], "--credential-file", str(self.work / "missing-key")],
                                env={**os.environ, "CODEX_THREAD_ID": "guard-still-applies"},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("agent/tool environment", result.stdout)
        self.assertNotIn("credential unavailable", result.stdout)
        with self.vault.selected(self.session) as ledger:
            self.assertFalse(ledger.related(prepared["request_id"], "attempt"))

    def test_replay_rejects_semantically_forged_cost_even_with_rehashed_event(self):
        prepared = self.make_request()
        self.invoke(prepared)
        path = Path(self.settings["ledger"])
        events = [json.loads(line) for line in path.read_bytes().splitlines()]
        events[-1]["data"]["cost_usd"] = "0"
        events[-1]["event_id"] = store.event_hash(events[-1])
        path.write_bytes(b"".join(kernel.canonical(event) + b"\n" for event in events))
        with self.assertRaisesRegex(kernel.Invalid, "billed response"):
            with self.vault.selected(self.session):
                pass


if __name__ == "__main__":
    unittest.main()
