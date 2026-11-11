"""Synthetic wire fixtures and mocked transport only; no provider invocation."""

import copy
from decimal import Decimal
import json
import os
from pathlib import Path
import ssl
import sys
import unittest
from unittest.mock import Mock, patch

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE.parents[2] / "zsh" / "jev"
sys.path.insert(0, str(SOURCE))
import kernel
import provider


def packet():
    return json.loads((BASE / "tests/fixtures/brief-missing.json").read_text())


def wire():
    return {"id": "synthetic-generation", "model": "synthetic/model-pinned",
            "provider": "SYNTHETIC", "usage": {"cost": 0.000019992, "input_tokens": 9},
            "answers": {
                "missing": {"type": "noul", "noul": 0.8},
                "action": {"type": "choice", "choice": "clarify", "confidence": 0.6,
                           "probabilities": {"clarify": 0.8, "proceed": 0.2}},
                "coverage": {"type": "score", "score": 0.5, "confidence": 0.2,
                             "legend": {"0": "zero constraints", "1": "one constraint",
                                        "2": "two constraints", "3": "three constraints"},
                             "probabilities": {"0": 0.5, "1": 0.5, "2": 0, "3": 0}}}}


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.packet = packet()
        self.prepared = kernel.prepare(self.packet)
        self.wire = wire()
        self.models = [self.wire["model"]]

    def parse(self, response=None):
        return provider.parse_response(self.prepared,
                                       json.dumps(response or self.wire).encode(), self.models)

    def test_build_preserves_complete_packet_and_pins_model(self):
        original = copy.deepcopy(self.packet)
        body = provider.build_request(self.packet, self.models[0])
        parsed = json.loads(body)
        self.assertEqual(parsed["model"], self.models[0])
        self.assertEqual(parsed["state"], original)
        self.assertEqual(parsed["provider"], {"allow_fallbacks": False})
        self.assertEqual(body, kernel.canonical(parsed))
        self.assertEqual(self.packet, original)
        self.assertEqual(parsed["questions"]["missing"],
                         {"type": "noul", "instructions": original["questions"][0]["text"]})
        self.assertEqual(parsed["questions"]["action"]["criteria"],
                         {"clarify": "clarify", "proceed": "proceed"})
        self.assertEqual(parsed["questions"]["coverage"]["criteria"],
                         original["questions"][2]["levels"])
        self.packet["memory"]["text"] = "Later mutation"
        self.assertEqual(json.loads(body)["state"], original)

    def test_provider_limits_and_invalid_packet_fail_before_transport(self):
        for field, size in (("options", 256), ("levels", 11)):
            source = packet()
            target = next(q for q in source["questions"] if field in q)
            target[field] = [str(i) for i in range(size)]
            with self.subTest(field=field), self.assertRaises(kernel.Invalid):
                provider.build_request(source, self.models[0])
        self.packet["state"]["large"] = "x" * kernel.MAX_BYTES
        with self.assertRaises(kernel.Invalid):
            provider.build_request(self.packet, self.models[0])
        with self.assertRaises(kernel.Invalid):
            provider.build_request(packet(), "")
        source = packet()
        source["state"]["padding"] = "x" * (kernel.MAX_BYTES - len(kernel.canonical(source)) - 30)
        kernel.validate_packet(source)
        with self.assertRaises(kernel.Invalid):
            provider.build_request(source, self.models[0])
        source = packet()
        source["questions"][1]["options"] = [str(i) for i in range(255)]
        source["questions"][2]["levels"] = [str(i) for i in range(10)]
        self.assertLessEqual(len(provider.build_request(source, self.models[0])), kernel.MAX_BYTES)

    def test_valid_mixed_mapping_preserves_bytes_and_supplied_statistics(self):
        raw = b" \n" + json.dumps(self.wire).encode() + b"\n"
        saved = bytes(raw)
        result = provider.parse_response(self.prepared, raw, self.models)
        self.assertEqual(result["validation"], {"status": "VALID", "errors": []})
        self.assertEqual(result["cost_usd"], "0.000019992")
        self.assertEqual(result["provider_id"], "synthetic-generation")
        self.assertEqual(result["receipt"]["request_id"], self.prepared["request_id"])
        self.assertEqual(result["receipt"]["packet_sha256"], self.prepared["packet_sha256"])
        self.assertEqual(result["receipt"]["answers"][0]["probability"], 0.8)
        self.assertEqual(result["receipt"]["answers"][1]["value"], "clarify")
        self.assertEqual(result["receipt"]["answers"][1]["confidence"], 0.6)
        self.assertEqual(result["receipt"]["answers"][2]["value"], 0.5)
        kernel.validate_receipt(self.prepared, result["receipt"])
        self.assertEqual(raw, saved)

    def test_exact_decimal_cost_independent_of_invalid_advice_and_model(self):
        self.wire["answers"]["missing"]["noul"] = 9
        self.wire["model"] = "unapproved/model"
        raw = json.dumps(self.wire).replace("1.9992e-05", "0.12345678901234567890123456789")
        result = provider.parse_response(self.prepared, raw.encode(), self.models)
        self.assertEqual(result["validation"]["status"], "INVALID")
        self.assertEqual(result["cost_usd"], "0.12345678901234567890123456789")
        self.wire["model"] = self.models[0]
        result = self.parse()
        self.assertEqual(result["validation"]["status"], "INVALID")
        self.assertIsNotNone(result["receipt"])
        self.assertEqual(Decimal(result["cost_usd"]), Decimal("0.000019992"))
        raw = json.dumps(wire()).replace('"noul": 0.8', '"noul": 1e999')
        result = provider.parse_response(self.prepared, raw.encode(), self.models)
        self.assertEqual(result["validation"]["status"], "INVALID")
        self.assertEqual(result["cost_usd"], "0.000019992")

    def test_cost_missing_or_invalid_never_becomes_zero(self):
        for usage in ({}, {"cost": None}, {"cost": True}, {"cost": -1}, {"cost": "0.3"}):
            with self.subTest(usage=usage):
                self.wire["usage"] = usage
                result = self.parse()
                self.assertIsNone(result["cost_usd"])
                self.assertEqual(result["validation"]["status"], "VALID")
        self.wire["usage"] = {"cost": 0}
        self.assertEqual(self.parse()["cost_usd"], "0")
        self.wire["usage"] = {"cost": 1}
        raw = json.dumps(self.wire).replace('"cost": 1', '"cost": 1e1000000')
        self.assertEqual(provider.parse_response(self.prepared, raw.encode(), self.models)
                         ["cost_usd"], "1E+1000000")

    def test_exact_answer_keys_types_confidence_and_legend(self):
        changes = [
            lambda w: w["answers"].pop("missing"),
            lambda w: w["answers"].update(extra={"type": "noul", "noul": 0.5}),
            lambda w: w["answers"]["missing"].update(type="choice"),
            lambda w: w["answers"]["missing"].update(noul=True),
            lambda w: w["answers"]["missing"].update(confidence=1),
            lambda w: w["answers"]["action"].pop("confidence"),
            lambda w: w["answers"]["action"].update(confidence=2),
            lambda w: w["answers"]["action"].update(choice="proceed"),
            lambda w: w["answers"]["action"]["probabilities"].update(clarify=0.7),
            lambda w: w["answers"]["coverage"].update(score=1),
            lambda w: w["answers"]["coverage"]["legend"].update({"1": "changed"}),
            lambda w: w["answers"]["coverage"]["legend"].update({"4": "extra"}),
        ]
        for change in changes:
            candidate = wire()
            change(candidate)
            with self.subTest(change=change):
                result = self.parse(candidate)
                self.assertEqual(result["validation"]["status"], "INVALID")
                self.assertEqual(result["cost_usd"], "0.000019992")

    def test_bad_json_duplicates_nonfinite_and_bounds_return_structured_invalid(self):
        raws = [b"{", b"\xff", b"[]", b"null", b'{"a":1,"a":2}',
                b'{"usage":{"cost":NaN}}', b'{"usage":{"cost":Infinity}}',
                b'{"usage":{"cost":1e9999999999999999999999999999}}',
                b"x" * (kernel.MAX_BYTES + 1), "not bytes"]
        for raw in raws:
            with self.subTest(raw=str(raw)[:40]):
                result = provider.parse_response(self.prepared, raw, self.models)
                self.assertEqual(result["validation"]["status"], "INVALID")
                self.assertTrue(result["validation"]["errors"])
                self.assertIsNone(result["receipt"])
                self.assertIsNone(result["cost_usd"])

    def test_bad_prepared_or_model_policy_never_validates_advice(self):
        raw = json.dumps(self.wire).encode()
        for prepared in (None, {}, {**self.prepared, "packet_sha256": "tampered"}):
            self.assertEqual(provider.parse_response(prepared, raw, self.models)
                             ["validation"]["status"], "INVALID")
        for models in (None, [], "synthetic/model-pinned", [True], ["different/model"]):
            result = provider.parse_response(self.prepared, raw, models)
            self.assertEqual(result["validation"]["status"], "INVALID")
            self.assertEqual(result["cost_usd"], "0.000019992")

    def test_optional_remote_metadata_and_unsupported_outer_shape(self):
        self.wire.pop("id")
        self.wire.pop("provider")
        result = self.parse()
        self.assertEqual(result["validation"]["status"], "VALID")
        self.assertIsNone(result["provider_id"])
        direct_shape = {"results": self.wire["answers"], "model": self.models[0],
                        "usage": {"cost": 0.1}}
        result = self.parse(direct_shape)
        self.assertEqual(result["validation"]["status"], "INVALID")
        self.assertEqual(result["cost_usd"], "0.1")
        self.wire["id"] = "\ud800"
        result = self.parse()
        self.assertEqual(result["validation"]["status"], "INVALID")
        self.assertIsNone(result["provider_id"])


class TransportTests(unittest.TestCase):
    def test_fixed_single_post_exact_bytes_tls_and_environment_proxy_ignored(self):
        raw = b"  {\"synthetic\":true}\n"
        connection = Mock()
        connection.getresponse.return_value.status = 302
        connection.getresponse.return_value.read.return_value = raw
        body = b'{ "exact body" : "never reserialized" }'
        with patch.dict(os.environ, {"HTTPS_PROXY": "http://invalid.example:9"}), \
                patch.object(provider.http.client, "HTTPSConnection", return_value=connection) as factory:
            self.assertEqual(provider.post(body, "SYNTHETIC-KEY", timeout=7), (302, raw))
        factory.assert_called_once()
        self.assertEqual(factory.call_args.args, ("openrouter.ai",))
        self.assertEqual(factory.call_args.kwargs["timeout"], 7)
        context = factory.call_args.kwargs["context"]
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        connection.request.assert_called_once_with(
            "POST", "/api/alpha/decisions", body=body,
            headers={**provider.HEADERS, "Authorization": "Bearer SYNTHETIC-KEY"})
        connection.getresponse.return_value.read.assert_called_once_with(kernel.MAX_BYTES + 1)
        connection.close.assert_called_once()

    def test_oversize_and_network_errors_fail_once_with_no_key_in_error(self):
        for phase in ("oversize", "request", "getresponse", "read", "constructor", "provider-error"):
            connection = Mock()
            connection.getresponse.return_value.read.return_value = b"x" * 9
            key = "SYNTHETIC-SECRET-DO-NOT-PRINT"
            failure = OSError("failure contains " + key)
            if phase == "request":
                connection.request.side_effect = failure
            elif phase == "provider-error":
                connection.request.side_effect = provider.ProviderError(key)
            elif phase == "getresponse":
                connection.getresponse.side_effect = failure
            elif phase == "read":
                connection.getresponse.return_value.read.side_effect = failure
            with self.subTest(phase=phase), patch.object(
                    provider.http.client, "HTTPSConnection", return_value=connection,
                    side_effect=failure if phase == "constructor" else None) as factory:
                with self.assertRaises(provider.ProviderError) as raised:
                    provider.post(b"{}", key, max_bytes=8)
                self.assertNotIn(key, str(raised.exception))
                factory.assert_called_once()
                self.assertLessEqual(connection.request.call_count, 1)
                if phase != "constructor":
                    connection.close.assert_called_once()

    def test_invalid_arguments_never_create_connection(self):
        cases = [("{}", "key", {}), (b"{}", "key\nheader", {}),
                 (b"{}", "", {}), (b"{}", "key", {"timeout": 0}),
                 (b"{}", "key", {"timeout": float("nan")}),
                 (b"{}", "key", {"max_bytes": True}),
                 (b"x" * (kernel.MAX_BYTES + 1), "key", {})]
        with patch.object(provider.http.client, "HTTPSConnection") as factory:
            for body, key, options in cases:
                with self.subTest(options=options), self.assertRaises(provider.ProviderError):
                    provider.post(body, key, **options)
            factory.assert_not_called()


if __name__ == "__main__":
    unittest.main()
