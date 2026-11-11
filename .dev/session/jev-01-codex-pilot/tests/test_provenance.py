"""Caller provenance only: temporary roots, explicit context, no provider calls."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest import mock

from test_vault import BED, SOURCE, VaultCase, cli
import kernel
import store


def slots(**values):
    return {**dict.fromkeys(store.CLI_SLOTS), **values}


def expected_actor(requester=None, **values):
    return {**store.ACTOR, "cli_sessions": slots(**values), "requester": requester}


class ProvenanceTests(VaultCase):
    def invoke(self, *arguments, origin=(), requester=None, environment=None, selected=True, code=0, root=None):
        environment = {key: value for key, value in os.environ.items()
                       if key not in ("CODEX_THREAD_ID", "CODEX_SESSION_ID")} if environment is None else environment
        command = [sys.executable, "-B", str(SOURCE / "jev.py"), "--root", str(root or self.root)]
        if selected:
            command += ["--session", self.session, "--channel", "main"]
        command += list(origin)
        if requester is not None:
            command += ["--requester", requester]
        result = subprocess.run([*command, *map(str, arguments)], env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_direct_store_defaults_unknown_and_copies_supplied_origin(self):
        with mock.patch.dict(os.environ, {"CODEX_THREAD_ID": "observed-runtime", "CODEX_SESSION_ID": "different-runtime"}):
            prepared = self.prepare()
        self.assertEqual(prepared["event"]["actor"], expected_actor())
        supplied = slots(codex="Original.ID:Case-1")
        caller = store.Vault(self.root, cli_sessions=supplied, requester="hlm")
        supplied["codex"] = "mutated-after-construction"
        with caller.selected(self.session) as ledger:
            event = ledger.append("dispose", {"decision": "use", "consumer": "head", "reason": ""}, prepared["request_id"])
        self.assertEqual(event["actor"], expected_actor("hlm", codex="Original.ID:Case-1"))
        event["actor"]["cli_sessions"]["codex"] = "mutated-return"
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.events[-1]["actor"], expected_actor("hlm", codex="Original.ID:Case-1"))

    def test_explicit_each_cli_and_requester_are_independent(self):
        packet = self.file("packet.json", self.packet())
        for brand, requester in (("codex", "hlm"), ("claude", "agent"), ("gemini", None)):
            with self.subTest(brand=brand):
                prepared = self.invoke("prepare", packet, origin=("--cli", brand, "--cli-session", brand + ":ID.1"),
                                       requester=requester)
                self.assertEqual(prepared["event"]["actor"], expected_actor(requester, **{brand: brand + ":ID.1"}))
                self.assertNotEqual(prepared["request_id"], brand + ":ID.1")
        unbranded = self.invoke("prepare", packet, requester="hlm")
        self.assertEqual(unbranded["event"]["actor"], expected_actor("hlm"))

    def test_opening_origin_is_not_inherited_by_later_unknown_caller(self):
        other = self.project / "other"
        other.mkdir()
        opening = self.invoke("open", "--project", self.project, "--bed", other, selected=False,
                              origin=("--cli", "claude", "--cli-session", "opening"), requester="hlm")
        self.session = opening["session_id"]
        packet = self.file("later.json", self.packet())
        prepared = self.invoke("prepare", packet)
        self.assertEqual(prepared["event"]["actor"], expected_actor())
        history = self.invoke("show")
        self.assertEqual(history["events"][0]["actor"], expected_actor("hlm", claude="opening"))
        # Immutable opening settings exclude the identity of today's caller.
        reopened = self.invoke("open", "--project", self.project, "--bed", other, selected=False,
                               origin=("--cli", "gemini", "--cli-session", "reopener"))
        self.assertEqual(reopened["session_id"], self.session)

    def test_codex_detection_fallback_equal_pair_and_unknown_other_environment(self):
        for environment, detected in (({}, None), ({"CODEX_THREAD_ID": "thread"}, "thread"),
                                      ({"CODEX_SESSION_ID": "fallback"}, "fallback"),
                                      ({"CODEX_THREAD_ID": "same", "CODEX_SESSION_ID": "same"}, "same"),
                                      ({"CLAUDE_UNKNOWN_ID": object(), "GEMINI_UNKNOWN_ID": object()}, None)):
            with self.subTest(environment=list(environment)):
                self.assertEqual(cli.cli_origin(environment=environment), slots(codex=detected))
        packet = self.file("observed.json", self.packet())
        environment = {**os.environ, "CODEX_THREAD_ID": "observed-case", "CODEX_SESSION_ID": "observed-case"}
        prepared = self.invoke("prepare", packet, environment=environment, requester="hlm")
        self.assertEqual(prepared["event"]["actor"], expected_actor("hlm", codex="observed-case"))

    def test_explicit_pair_never_reads_or_validates_ambient_origin(self):
        class UnreadableEnvironment:
            def __contains__(self, key):
                raise AssertionError("explicit pair consulted ambient environment")
        self.assertEqual(cli.cli_origin("gemini", "Explicit.ID", UnreadableEnvironment()), slots(gemini="Explicit.ID"))
        environment = {**os.environ, "CODEX_THREAD_ID": "", "CODEX_SESSION_ID": "invalid/ambient"}
        packet = self.file("explicit.json", self.packet())
        prepared = self.invoke("prepare", packet, origin=("--cli", "claude", "--cli-session", "explicit-override"),
                               environment=environment)
        self.assertEqual(prepared["event"]["actor"], expected_actor(claude="explicit-override"))

    def test_ids_exact_ascii_grammar_without_normalization(self):
        for valid in ("A", "0", "Case.ID:_-09", "x" * 128):
            self.assertEqual(store.cli_session_id(valid), valid)
        invalid_ids = ("", " x", "x ", "x\n", "x\x00", "x/y", "x+y", "_x", "-x", ":x", ".x", "á", "x" * 129, True, 1)
        for invalid in invalid_ids:
            with self.subTest(value=invalid), self.assertRaises(kernel.Invalid):
                store.cli_session_id(invalid)
        for environment in ({"CODEX_THREAD_ID": ""}, {"CODEX_SESSION_ID": " "},
                            {"CODEX_THREAD_ID": "ok", "CODEX_SESSION_ID": ""},
                            {"CODEX_THREAD_ID": "Case", "CODEX_SESSION_ID": "case"}):
            with self.subTest(environment=environment), self.assertRaises(kernel.Invalid):
                cli.cli_origin(environment=environment)

    def test_invalid_cli_origins_refuse_before_any_vault_creation(self):
        missing = self.work / "must-not-be-created"
        opening = ("open", "--project", self.project, "--bed", self.bed)
        for origin in (("--cli", "codex"), ("--cli-session", "unpaired"),
                       ("--cli", "controller", "--cli-session", "reserved"),
                       ("--cli", "codex", "--cli-session", "bad/value"),
                       ("--requester", "human")):
            self.invoke(*opening, origin=origin, root=missing, selected=False, code=2)
            self.assertFalse(missing.exists())
        environment = {**os.environ, "CODEX_THREAD_ID": "one", "CODEX_SESSION_ID": "two"}
        self.invoke(*opening, environment=environment, root=missing, selected=False, code=2)
        self.assertFalse(missing.exists())

    def test_extended_actor_schema_rejects_invalid_shapes_and_preserves_legacy(self):
        valid = expected_actor("agent", codex="valid")
        store.validate_actor(valid)
        store.validate_actor(copy.deepcopy(store.ACTOR))
        invalid = [None, [], {**store.ACTOR, "requester": None}, {**valid, "extra": None},
                   {**valid, "source": "inferred"}, {**valid, "requester": "human"},
                   {**valid, "requester": True}, {**valid, "cli_sessions": None}]
        for bad_slots in ({}, {**slots(), "other": None}, {**slots(), "controller": "reserved"},
                          {**slots(), "codex": False}, {**slots(), "claude": "wrong/value"}):
            invalid.append({**valid, "cli_sessions": bad_slots})
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(kernel.Invalid):
                store.validate_actor(value)
        # Rehashing malformed provenance cannot bypass semantic replay.
        path = Path(self.settings["ledger"])
        opening = json.loads(path.read_bytes())
        opening["actor"] = {**valid, "cli_sessions": {**slots(), "controller": "forbidden"}}
        opening["event_id"] = store.event_hash(opening)
        path.write_bytes(kernel.canonical(opening) + b"\n")
        with self.assertRaises(kernel.Invalid):
            with self.vault.selected(self.session):
                pass

    def test_cross_client_reply_ref_and_consumers_retain_each_event_actor(self):
        packet = self.file("packet.json", self.packet())
        prepared = self.invoke("prepare", packet, origin=("--cli", "codex", "--cli-session", "preparing"), requester="hlm")
        request = prepared["request_id"]
        before_reply = self.invoke("ref", request, origin=("--cli", "gemini", "--cli-session", "reader"))
        self.assertEqual(before_reply["actor"], expected_actor("hlm", codex="preparing"))
        response = self.file("response.json", self.receipt(prepared["prepared"]))
        reply = self.invoke("import-reply", request, response,
                            origin=("--cli", "claude", "--cli-session", "reply-recorder"), requester="agent")
        referenced = self.invoke("ref", request, origin=("--cli", "gemini", "--cli-session", "reader"), requester="hlm")
        self.assertEqual(referenced["event_id"], reply["event_id"])
        self.assertEqual(referenced["actor"], expected_actor("agent", claude="reply-recorder"))
        consumer = self.invoke("dispose", request, "skip", "--consumer", "operator", requester="hlm")
        self.assertEqual(consumer["actor"], expected_actor("hlm"))
        question = next(q["id"] for q in prepared["prepared"]["packet"]["questions"] if q["type"] == "noul")
        interpretation = self.invoke("interpret", request, question, BED / "tests/fixtures/policy.json",
                                     origin=("--cli", "gemini", "--cli-session", "interpreter"))
        self.assertEqual(interpretation["actor"], expected_actor(gemini="interpreter"))
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.request(request)["actor"], expected_actor("hlm", codex="preparing"))
            self.assertEqual(ledger.related(request, "reply")[0]["actor"], referenced["actor"])

    def test_selection_embeds_original_provenance_and_current_consumer_actor(self):
        packet = self.file("packet.json", self.packet())
        prepared = self.invoke("prepare", packet, origin=("--cli", "claude", "--cli-session", "source"))
        request = prepared["request_id"]
        reply = self.invoke("import-reply", request, self.file("response.json", self.receipt(prepared["prepared"])),
                            origin=("--cli", "codex", "--cli-session", "original"), requester="hlm")
        selection = self.file("selection.json", {"policy": {"id": "explicit", "version": "1"}, "items": [
            {"event_id": reply["event_id"], "excerpt": reply["event_id"]}]})
        selected = self.invoke("select", selection, origin=("--cli", "gemini", "--cli-session", "selector"))
        later = self.invoke("prepare", packet, "--selection", selected["event_id"],
                            origin=("--cli", "claude", "--cli-session", "consumer"), requester="agent")
        embedded = later["prepared"]["packet"]["state"]["jev_selection"]["source_events"][0]
        self.assertEqual(embedded, reply)
        self.assertEqual(embedded["actor"], expected_actor("hlm", codex="original"))
        self.assertEqual(later["event"]["actor"], expected_actor("agent", claude="consumer"))

    def test_legacy_ledger_bytes_and_ref_actor_remain_exact_after_new_append(self):
        prepared = self.prepare()
        with self.vault.selected(self.session) as ledger:
            cli.import_reply(ledger, prepared["request_id"], self.file("response.json", self.receipt(prepared["prepared"])))
        path = Path(self.settings["ledger"])
        events = [json.loads(line) for line in path.read_bytes().splitlines()]
        previous = None
        for event in events:
            event["actor"] = dict(store.ACTOR)
            event["previous_event_id"] = previous
            event["event_id"] = store.event_hash(event)
            previous = event["event_id"]
        legacy = b"".join(kernel.canonical(event) + b"\n" for event in events)
        path.write_bytes(legacy)
        referenced = self.invoke("ref", prepared["request_id"], origin=("--cli", "codex", "--cli-session", "new-reader"))
        self.assertEqual(referenced["actor"], store.ACTOR)
        self.assertNotIn("cli_sessions", referenced["actor"])
        self.assertNotIn("requester", referenced["actor"])
        self.assertEqual(path.read_bytes(), legacy)
        appended = self.invoke("dispose", prepared["request_id"], "use", "--consumer", "new-consumer",
                               origin=("--cli", "gemini", "--cli-session", "new-writer"), requester="hlm")
        self.assertTrue(path.read_bytes().startswith(legacy))
        self.assertEqual(appended["actor"], expected_actor("hlm", gemini="new-writer"))
