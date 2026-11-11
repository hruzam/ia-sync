"""Synthetic one-use grants through native production CLI; never real credentials/HTTP."""

from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest import mock

from test_vault import SOURCE, VaultCase, cli
import test_send
import kernel
import provider
import store


class DelegatedTests(VaultCase):
    wire = test_send.SendTests.wire

    def setUp(self):
        super().setUp()
        self.root = self.work / "delegated-vault"
        self.vault = store.Vault(self.root)
        self.settings = self.vault.open(self.project, self.bed, "0.02", "synthetic/model")
        self.session = self.settings["session_id"]
        self.fake_key = "synthetic-delegated-not-a-real-key-0123456789"
        self.environment = {"CODEX_THREAD_ID": "Synthetic.Delegated.Caller", "JEV_ORAK_KEY": self.fake_key}

    def request(self, bound="0.02"):
        return self.prepare(upper_bound=bound, bound_evidence="synthetic conservative grant bound")

    def grant(self, prepared, **changes):
        with self.vault.selected(self.session) as ledger:
            digest = ledger.approval(prepared["request_id"])[1]
        value = {"schema": "jev.send-grant/v1", "root": str(self.root), "session_id": self.session,
                 "request_id": prepared["request_id"], "approval_sha256": digest,
                 "max_cost_usd": prepared["event"]["data"]["upper_bound_usd"], "credential_env": "JEV_ORAK_KEY",
                 "authorized_by": "hlm", "authorization_ref": "  synthetic observed operator approval  ",
                 "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()}
        value.update(changes)
        return value

    def grant_file(self, grant, name="grant.json", raw=None):
        path = self.file(name, raw if raw is not None else grant, raw=raw is not None)
        path.chmod(0o600)
        return path

    def arguments(self, prepared, grant_file):
        return ["--root", str(self.root), "--session", self.session, "--channel", "main", "--cli", "codex",
                "--cli-session", "Synthetic.Delegated.Caller", "--requester", "hlm", "send", prepared["request_id"],
                "--authorization-file", str(grant_file), "--credential-env", "JEV_ORAK_KEY"]

    def invoke(self, prepared, grant_file, *, response=None, post=None, environment=None, code=0):
        response = self.wire(prepared["prepared"], cost="0.001") if response is None else response
        output = io.StringIO()
        post = mock.Mock(return_value=(200, response)) if post is None else post
        with mock.patch.object(cli.os, "environ", self.environment if environment is None else environment), \
                mock.patch.object(provider, "post", post), redirect_stdout(output):
            result = cli.main(self.arguments(prepared, grant_file))
        self.assertEqual(result, code, output.getvalue())
        self.assertNotIn(self.fake_key, output.getvalue())
        return json.loads(output.getvalue()), post

    def assert_no_attempt(self, request_id):
        with self.vault.selected(self.session) as ledger:
            self.assertFalse(ledger.related(request_id, "attempt"))

    def record_attempt(self, prepared, grant):
        with self.vault.selected(self.session) as ledger:
            return ledger.append("attempt", {"upper_bound_usd": prepared["event"]["data"]["upper_bound_usd"],
                "approval_sha256": grant["approval_sha256"], "prepared_event_id": prepared["event"]["event_id"],
                "authorization": {"grant": grant, "grant_sha256": kernel.digest(kernel.canonical(grant))}},
                prepared["request_id"])

    def test_native_valid_grant_exact_body_proof_actor_and_env_read_after_fsync(self):
        prepared = self.request()
        grant = self.grant(prepared)
        path = self.grant_file(grant)
        original = path.read_bytes()
        reads = []
        test = self
        class ObservedEnvironment(dict):
            def get(self, name, default=None):
                if name == "JEV_ORAK_KEY":
                    events = [json.loads(line) for line in Path(test.settings["ledger"]).read_bytes().splitlines()]
                    test.assertEqual(events[-1]["kind"], "attempt")
                    test.assertEqual(events[-1]["data"]["authorization"]["grant"], grant)
                    reads.append(name)
                return super().get(name, default)
        with mock.patch.object(cli, "guard_human", side_effect=AssertionError("delegated mode used manual guard")), \
                mock.patch.object(cli, "confirm_terminal", side_effect=AssertionError("delegated mode asked manual confirmation")):
            result, post = self.invoke(prepared, path, environment=ObservedEnvironment(self.environment))
        self.assertEqual(result["status"], "SETTLED")
        self.assertEqual(reads, ["JEV_ORAK_KEY"])
        post.assert_called_once_with(store.decode_bytes(prepared["event"]["data"]["provider"]["body_base64"]), self.fake_key)
        self.assertEqual(path.read_bytes(), original)
        with self.vault.selected(self.session) as ledger:
            attempt = ledger.related(prepared["request_id"], "attempt")[0]
            self.assertEqual(attempt["data"]["authorization"], {"grant": grant, "grant_sha256": kernel.digest(kernel.canonical(grant))})
            self.assertEqual(attempt["data"]["authorization"]["grant"]["authorization_ref"], grant["authorization_ref"])
            for kind in ("attempt", "http", "reply", "settle"):
                event = ledger.related(prepared["request_id"], kind)[0]
                self.assertEqual(event["actor"]["cli_sessions"]["codex"], "Synthetic.Delegated.Caller")
                self.assertEqual(event["actor"]["requester"], "hlm")
        self.assertNotIn(self.fake_key.encode(), Path(self.settings["ledger"]).read_bytes())

    def test_real_mode_parser_rejects_mixed_incomplete_and_unknown_env_before_access(self):
        prepared = self.request()
        base = self.arguments(prepared, self.work / "never-opened")
        invalid = [base[:-2], base + ["--credential-file", "dummy"],
                   base[:-2] + ["--credential-env", "OTHER_KEY"],
                   base[:-4] + ["--credential-env", "JEV_ORAK_KEY"],
                   base[:-4] + ["--credential-file", "dummy", "--credential-env", "JEV_ORAK_KEY"]]
        for arguments in invalid:
            output = io.StringIO()
            with self.subTest(arguments=arguments[-4:]), mock.patch.object(cli.os, "environ", self.environment), \
                    mock.patch.object(cli, "read_send_grant") as read_grant, \
                    mock.patch.object(cli, "read_env_credential") as read_key, \
                    mock.patch.object(provider, "post") as post, redirect_stdout(output):
                self.assertEqual(cli.main(arguments), 2)
                read_grant.assert_not_called()
                read_key.assert_not_called()
                post.assert_not_called()
        self.assert_no_attempt(prepared["request_id"])

    def test_invalid_grant_scope_fields_hash_amount_expiry_refuse_before_key(self):
        prepared = self.request()
        cases = [{"schema": "bad"}, {"root": str(self.root) + "/."}, {"session_id": "0" * 32},
                 {"request_id": "0" * 32}, {"approval_sha256": "0" * 64}, {"max_cost_usd": "0"},
                 {"max_cost_usd": "0.021"}, {"max_cost_usd": "0.01"}, {"max_cost_usd": True},
                 {"credential_env": "OTHER_KEY"}, {"authorized_by": "agent"}, {"expires_at": "not-a-date"},
                 {"expires_at": "2020-01-01T00:00:00+00:00"}, {"expires_at": "2099-01-01T00:00:00"},
                 {"expires_at": None}, {"extra": True}]
        original = self.grant(prepared)
        missing = dict(original)
        del missing["authorization_ref"]
        grants = [{**original, **changes} for changes in cases] + [missing]
        for grant in grants:
            with self.subTest(changes={k:v for k,v in grant.items() if original.get(k)!=v}), \
                    mock.patch.object(cli, "read_env_credential") as read_key:
                path = self.grant_file(grant)
                result, post = self.invoke(prepared, path, code=2)
                self.assertEqual(result["status"], "ERROR")
                read_key.assert_not_called()
                post.assert_not_called()
                self.assert_no_attempt(prepared["request_id"])

    def test_authorization_ref_exact_ascii_bounds_without_normalization(self):
        prepared = self.request()
        for invalid in ("", " " * 2048, "x" * 2049, "x\n", "x\t", "x\x7f", "é", None, True):
            grant = self.grant(prepared, authorization_ref=invalid)
            with self.subTest(value=invalid), mock.patch.object(cli, "read_env_credential") as read_key:
                _, post = self.invoke(prepared, self.grant_file(grant), code=2)
                read_key.assert_not_called()
                post.assert_not_called()
        valid_grants = [self.grant(prepared, authorization_ref=valid) for valid in ("!", "x" * 2048, "  exact spaces  ")]
        with self.vault.selected(self.session) as ledger:
            for grant in valid_grants:
                ledger.validate_send_grant(prepared["request_id"], grant, datetime.now(timezone.utc))
        self.assert_no_attempt(prepared["request_id"])

    def test_private_grant_file_modes_links_owner_size_json_and_open_race(self):
        prepared = self.request()
        path = self.grant_file(self.grant(prepared))
        path.chmod(0o644)
        with mock.patch.object(cli, "read_env_credential") as read_key:
            _, post = self.invoke(prepared, path, code=2)
            read_key.assert_not_called()
            post.assert_not_called()
        path.chmod(0o600)
        linked = self.work / "grant-symlink"
        linked.symlink_to(path)
        with self.assertRaises(kernel.Invalid):
            cli.read_send_grant(linked)
        hardlink = self.work / "grant-hardlink"
        os.link(path, hardlink)
        with self.assertRaises(kernel.Invalid):
            cli.read_send_grant(path)
        hardlink.unlink()
        with mock.patch.object(store.os, "getuid", return_value=-1), self.assertRaises(kernel.Invalid):
            cli.read_send_grant(path)
        for raw in (b"x" * 16385, b'{"broken":', b'{"schema":"one","schema":"two"}', b'[]'):
            with mock.patch.object(cli, "read_env_credential") as read_key:
                _, post = self.invoke(prepared, self.grant_file(None, raw=raw), code=2)
                read_key.assert_not_called()
                post.assert_not_called()
        alternate = self.grant_file(self.grant(prepared), "other-grant.json")
        real_open = os.open
        with mock.patch.object(cli.os, "open", side_effect=lambda *a, **k: real_open(alternate, os.O_RDONLY)), \
                self.assertRaisesRegex(kernel.Invalid, "changed while opening"):
            cli.read_send_grant(path)
        self.assert_no_attempt(prepared["request_id"])

    def test_allowance_above_cap_and_zero_frozen_bound_refuse(self):
        zero = self.request("0")
        with mock.patch.object(cli, "read_env_credential") as key:
            _, post = self.invoke(zero, self.grant_file(self.grant(zero)), code=2)
            key.assert_not_called()
            post.assert_not_called()
        other_bed = self.project / "larger"
        other_bed.mkdir()
        self.settings = self.vault.open(self.project, other_bed, "0.03", "synthetic/model")
        self.session = self.settings["session_id"]
        prepared = self.request()
        with mock.patch.object(cli, "read_env_credential") as key:
            _, post = self.invoke(prepared, self.grant_file(self.grant(prepared)), code=2)
            key.assert_not_called()
            post.assert_not_called()
        self.assert_no_attempt(prepared["request_id"])

    def test_reused_grant_different_request_and_changed_current_budget_reject(self):
        first = self.request("0.01")
        first_grant = self.grant(first)
        second = self.request("0.01")
        with mock.patch.object(cli, "read_env_credential") as key:
            _, post = self.invoke(second, self.grant_file(first_grant), code=2)
            key.assert_not_called()
            post.assert_not_called()
        second_grant = self.grant(second)
        self.assertEqual(self.invoke(second, self.grant_file(second_grant))[0]["status"], "SETTLED")
        with mock.patch.object(cli, "read_env_credential") as key:
            result, post = self.invoke(first, self.grant_file(first_grant), code=2)
            self.assertIn("approval mismatch", result["errors"][0])
            key.assert_not_called()
            post.assert_not_called()
        self.assert_no_attempt(first["request_id"])

    def test_repeat_and_crash_consumption_never_read_key_or_call_again(self):
        prepared = self.request()
        grant = self.grant(prepared)
        path = self.grant_file(grant)
        self.record_attempt(prepared, grant)
        with mock.patch.object(cli, "read_env_credential") as key:
            _, post = self.invoke(prepared, path, code=2)
            key.assert_not_called()
            post.assert_not_called()
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.budget()["reserved_usd"], "0.02")
            self.assertEqual(len(ledger.related(prepared["request_id"], "attempt")), 1)
        self.assertTrue(path.is_file())

    def test_invalid_or_missing_env_consumes_attempt_and_retains_unknown(self):
        for index, value in enumerate((None, "", " padded", "trailing ", "line\n", "tab\t", "é", "x" * 4097)):
            if index:
                other = self.project / str(index)
                other.mkdir()
                self.settings = self.vault.open(self.project, other, "0.02", "synthetic/model")
                self.session = self.settings["session_id"]
            prepared = self.request()
            environment = {"CODEX_THREAD_ID": "Synthetic.Delegated.Caller"}
            if value is not None:
                environment["JEV_ORAK_KEY"] = value
            result, post = self.invoke(prepared, self.grant_file(self.grant(prepared)), environment=environment, code=2)
            self.assertEqual(result["status"], "UNKNOWN")
            self.assertTrue(result["budget"]["liabilities"])
            post.assert_not_called()
            with mock.patch.object(cli, "read_env_credential") as key:
                _, post = self.invoke(prepared, self.work / "grant.json", code=2)
                key.assert_not_called()
                post.assert_not_called()
        with mock.patch.object(cli.os, "environ", {"JEV_ORAK_KEY": "x" * 4096}):
            self.assertEqual(len(cli.read_env_credential("JEV_ORAK_KEY")), 4096)
            with self.assertRaises(kernel.Invalid):
                cli.read_env_credential("OTHER_KEY")

    def test_transport_unknown_is_secret_safe_and_never_retried(self):
        prepared = self.request()
        path = self.grant_file(self.grant(prepared))
        failing = mock.Mock(side_effect=RuntimeError("untrusted exception " + self.fake_key))
        result, _ = self.invoke(prepared, path, post=failing, code=2)
        self.assertEqual(result["status"], "UNKNOWN")
        failing.assert_called_once()
        self.assertNotIn(self.fake_key.encode(), Path(self.settings["ledger"]).read_bytes())
        _, post = self.invoke(prepared, path, code=2)
        post.assert_not_called()

    def test_changed_frozen_payload_rejects_stale_grant_even_with_valid_local_hashes(self):
        prepared = self.request()
        grant_file = self.grant_file(self.grant(prepared))
        path = Path(self.settings["ledger"])
        events = [json.loads(line) for line in path.read_bytes().splitlines()]
        changed = events[-1]["data"]["prepared"]
        changed["packet"]["state"]["changed_after_grant"] = "synthetic mutation"
        changed.update(kernel.packet_hashes(changed["packet"]))
        frozen = events[-1]["data"]["provider"]
        body = provider.build_request(changed["packet"], frozen["model"])
        frozen.update(body_base64=store.encode_bytes(body), sha256=kernel.digest(body))
        events[-1]["event_id"] = store.event_hash(events[-1])
        path.write_bytes(b"".join(kernel.canonical(event) + b"\n" for event in events))
        with mock.patch.object(cli, "read_env_credential") as key:
            result, post = self.invoke(prepared, grant_file, code=2)
            self.assertIn("approval mismatch", result["errors"][0])
            key.assert_not_called()
            post.assert_not_called()
        self.assert_no_attempt(prepared["request_id"])

    def test_native_crash_after_consumption_blocks_second_invocation(self):
        prepared = self.request()
        grant_file = self.grant_file(self.grant(prepared))
        with mock.patch.object(cli, "read_env_credential", side_effect=SystemExit("synthetic abrupt exit")), \
                mock.patch.object(provider, "post") as post, self.assertRaises(SystemExit):
            self.invoke(prepared, grant_file)
        post.assert_not_called()
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(ledger.events[-1]["kind"], "attempt")
            self.assertEqual(ledger.budget()["reserved_usd"], "0.02")
        with mock.patch.object(cli, "read_env_credential") as key:
            _, post = self.invoke(prepared, grant_file, code=2)
            key.assert_not_called()
            post.assert_not_called()

    def test_delegated_json_escaped_secret_echo_is_withheld_after_one_mock_call(self):
        prepared = self.request()
        path = self.grant_file(self.grant(prepared))
        escaped = "".join("\\u%04x" % ord(character) for character in self.fake_key).encode()
        raw = self.wire(prepared["prepared"], cost="0.001").replace(b"synthetic-generation", escaped)
        result, post = self.invoke(prepared, path, response=raw, code=2)
        self.assertEqual(result["status"], "UNKNOWN")
        post.assert_called_once()
        with self.vault.selected(self.session) as ledger:
            self.assertFalse(ledger.related(prepared["request_id"], "http"))
            self.assertFalse(ledger.related(prepared["request_id"], "reply"))
        self.assertNotIn(self.fake_key.encode(), Path(self.settings["ledger"]).read_bytes())
        self.assertNotIn(escaped, Path(self.settings["ledger"]).read_bytes())

    def test_replay_checks_expiry_at_event_time_not_current_clock(self):
        prepared = self.request()
        grant = self.grant(prepared)
        self.record_attempt(prepared, grant)
        class FutureClock(datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2099, 1, 1, tzinfo=timezone.utc)
        with mock.patch.object(store, "datetime", FutureClock):
            with self.vault.selected(self.session) as ledger:
                self.assertEqual(len(ledger.related(prepared["request_id"], "attempt")), 1)
        path = Path(self.settings["ledger"])
        events = [json.loads(line) for line in path.read_bytes().splitlines()]
        events[-1]["at"] = (datetime.fromisoformat(grant["expires_at"]) + timedelta(seconds=1)).isoformat()
        events[-1]["event_id"] = store.event_hash(events[-1])
        path.write_bytes(b"".join(kernel.canonical(event) + b"\n" for event in events))
        with self.assertRaisesRegex(kernel.Invalid, "expired"):
            with self.vault.selected(self.session):
                pass

    def test_rehashed_proof_tamper_cannot_bypass_replay_validation(self):
        prepared = self.request()
        grant = self.grant(prepared)
        self.record_attempt(prepared, grant)
        path = Path(self.settings["ledger"])
        original = path.read_bytes()
        for field, value, rehash_proof in (("authorized_by", "agent", True), ("root", "/wrong", True),
                                           ("max_cost_usd", "0.021", True), ("authorization_ref", "forged", False)):
            events = [json.loads(line) for line in original.splitlines()]
            proof = events[-1]["data"]["authorization"]
            proof["grant"][field] = value
            if rehash_proof:
                proof["grant_sha256"] = kernel.digest(kernel.canonical(proof["grant"]))
            events[-1]["event_id"] = store.event_hash(events[-1])
            path.write_bytes(b"".join(kernel.canonical(event) + b"\n" for event in events))
            with self.subTest(field=field), self.assertRaises(kernel.Invalid):
                with self.vault.selected(self.session):
                    pass

    def test_concurrent_native_processes_make_at_most_one_mocked_call(self):
        prepared = self.request()
        grant_file = self.grant_file(self.grant(prepared))
        response = self.file("wire-response.json", self.wire(prepared["prepared"], cost="0.001"), raw=True)
        calls = self.work / "mock-call-count"
        script = '''import sys,time
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,sys.argv[1])
import jev,provider
response=Path(sys.argv[2]).read_bytes()
def fake_post(body,key):
    with open(sys.argv[3],'ab') as output:
        output.write(b'called\\n')
    time.sleep(0.1)
    return 200,response
with patch.object(provider,'post',fake_post):
    raise SystemExit(jev.main(sys.argv[4:]))
'''
        arguments = [sys.executable, "-B", "-c", script, str(SOURCE), str(response), str(calls),
                     *self.arguments(prepared, grant_file)]
        processes = [subprocess.Popen(arguments, env=self.environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = []
        for process in processes:
            output, error = process.communicate(timeout=15)
            self.assertFalse(error, error)
            self.assertNotIn(self.fake_key.encode(), output)
            results.append(process.returncode)
        self.assertEqual(sorted(results), [0, 2])
        self.assertEqual(calls.read_bytes().splitlines(), [b"called"])
        with self.vault.selected(self.session) as ledger:
            self.assertEqual(len(ledger.related(prepared["request_id"], "attempt")), 1)

    def test_manual_production_guard_remains_active_with_new_mode_available(self):
        prepared = self.request()
        args = self.arguments(prepared, "unused")[:-4] + ["--credential-file", "missing"]
        output = io.StringIO()
        with mock.patch.object(cli.os, "environ", self.environment), mock.patch.object(cli, "read_credential") as key, \
                mock.patch.object(provider, "post") as post, redirect_stdout(output):
            self.assertEqual(cli.main(args), 2)
        self.assertIn("agent/tool environment", output.getvalue())
        key.assert_not_called()
        post.assert_not_called()
        self.assert_no_attempt(prepared["request_id"])
