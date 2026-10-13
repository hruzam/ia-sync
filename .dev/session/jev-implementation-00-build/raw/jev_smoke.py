#!/usr/bin/env python3
"""Synthetic, read-only Jev API smoke test. Python 3.10+, standard library only.

Default/--dry-run: print the synthetic request; no network or credentials needed.
--self-test: exercise response validation with local fixtures; no network.
--live: make exactly one request to TypeSafe using TYPESAFE_API_KEY.

No tool execution, file collection, hooks, or installation. Not a security gate.
API contract checked against https://docs.typesafe.ai/api on 2026-09-24.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from typing import Any

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"
MAX_RESPONSE_BYTES = 1_048_576
PRICE_PER_MILLION_INPUT_TOKENS = 0.042  # Published 2026-09-24; not a billing guarantee.


def payload() -> dict[str, Any]:
    return {
        "model": MODEL,
        "state": {
            "goal": "Fix the failing unit test for parse_quantity.",
            "recent_attempts": [
                {"action": "Run the same unit test without editing code", "result": "Same assertion failure"}
                for _ in range(3)
            ],
            "candidate_context": "tests/test_quantity.py contains the failing assertion and expected behavior.",
        },
        "questions": {
            "next_step": {
                "type": "choice",
                "instructions": "Which next step best advances the stated goal given the recent attempts?",
                "criteria": {
                    "inspect": "Inspect the implementation and failing test before trying another fix.",
                    "repeat": "Repeat the identical test without changing or inspecting anything.",
                    "ask": "Ask the user for missing requirements needed to choose a next step.",
                },
            },
            "repeated_failure": {
                "type": "noul",
                "instructions": "Do the recent attempts repeat the same action and failure without evidence of progress?",
            },
            "context_relevance": {
                "type": "score",
                "instructions": "How useful is candidate_context for the stated goal?",
                "criteria": [
                    "Unrelated to the goal.",
                    "Useful background but not direct evidence.",
                    "Direct evidence for diagnosing the failing test.",
                ],
            },
        },
    }


def require_number(value: Any, name: str, low: float, high: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: expected a number")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name}: number too large") from exc
    if not math.isfinite(number) or not low <= number <= high:
        raise ValueError(f"{name}: number outside valid range")
    return number


def distribution(value: Any, keys: set[str], name: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{name}: unexpected probability keys")
    total = sum(require_number(v, name, 0, 1) for v in value.values())
    if abs(total - 1.0) > 0.01:
        raise ValueError(f"{name}: probabilities do not sum approximately to one")


def validate(result: Any) -> None:
    if not isinstance(result, dict) or not isinstance(result.get("model"), str) or not result["model"]:
        raise ValueError("response: missing model identifier")
    if result["model"] != MODEL:
        raise ValueError("response: unexpected model version")
    answers = result.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("response: missing answers")
    for key, expected_type in (("next_step", "choice"), ("repeated_failure", "noul"), ("context_relevance", "score")):
        if not isinstance(answers.get(key), dict) or answers[key].get("type") != expected_type:
            raise ValueError(f"{key}: missing answer or wrong type")
    choice = answers["next_step"]
    if choice.get("choice") not in {"inspect", "repeat", "ask"}:
        raise ValueError("next_step: unexpected choice")
    require_number(choice.get("confidence"), "next_step.confidence", 0, 1)
    distribution(choice.get("probabilities"), {"inspect", "repeat", "ask"}, "next_step.probabilities")
    require_number(answers["repeated_failure"].get("noul"), "repeated_failure.noul", 0, 1)
    score = answers["context_relevance"]
    expected_legend = {str(i): text for i, text in enumerate(payload()["questions"]["context_relevance"]["criteria"])}
    if score.get("legend") != expected_legend:
        raise ValueError("context_relevance: missing or unexpected legend")
    require_number(score.get("score"), "context_relevance.score", 0, 2)
    require_number(score.get("confidence"), "context_relevance.confidence", 0, 1)
    distribution(score.get("probabilities"), {"0", "1", "2"}, "context_relevance.probabilities")
    usage = result.get("usage")
    if not isinstance(usage, dict):
        raise ValueError("response: missing usage")
    for name in ("input_tokens", "output_tokens"):
        value = usage.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"usage.{name}: expected a nonnegative integer")


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def live() -> int:
    key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not key:
        print("Missing TYPESAFE_API_KEY. No request was sent.", file=sys.stderr)
        return 2
    body = json.dumps(payload(), allow_nan=False).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT, data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"},
    )
    # Direct HTTPS, normal certificate validation, no redirects or automatic retries.
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), NoRedirects(),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
    )
    started = time.monotonic()
    try:
        with opener.open(request, timeout=10) as response:
            if response.headers.get_content_type() != "application/json":
                raise ValueError("response: expected application/json")
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ValueError("response: too large")
        result = json.loads(raw)
        validate(result)
    except urllib.error.HTTPError as exc:
        # Do not print request headers or response bodies, which can echo input.
        print(f"HTTP {exc.code}: request failed; response body omitted. No retry.", file=sys.stderr)
        return 3
    except (urllib.error.URLError, OSError, ValueError, TypeError):
        print("Network, timeout, or response-validation failure. No retry; no permission granted.", file=sys.stderr)
        return 3
    print(json.dumps({
        "status": "schema_smoke_passed",
        "semantic_accuracy_verified": False,
        "permission_granted": False,
        "requested_model": MODEL,
        "resolved_model": result["model"],
        "latency_ms": round((time.monotonic() - started) * 1000, 2),
        "usage": result["usage"],
        "estimated_input_cost_usd": round(result["usage"]["input_tokens"] * PRICE_PER_MILLION_INPUT_TOKENS / 1_000_000, 10),
        "price_reference_date": "2026-09-24",
        "answers": result["answers"],
    }, indent=2, allow_nan=False))
    return 0


def self_test() -> int:
    fixture = {
        "model": MODEL,
        "answers": {
            "next_step": {"type": "choice", "choice": "inspect", "confidence": 1.0, "probabilities": {"inspect": 1.0, "repeat": 0.0, "ask": 0.0}},
            "repeated_failure": {"type": "noul", "noul": 0.99},
            "context_relevance": {"type": "score", "score": 2.0, "legend": {str(i): text for i, text in enumerate(payload()["questions"]["context_relevance"]["criteria"])}, "confidence": 1.0, "probabilities": {"0": 0.0, "1": 0.0, "2": 1.0}},
        },
        "usage": {"input_tokens": 400, "output_tokens": 60},
    }
    validate(fixture)
    cases: list[Any] = [None, {}, {"model": MODEL}, {"model": MODEL, "answers": {}}]
    for path, value in [
        (("answers", "next_step", "choice"), "execute_shell"),
        (("answers", "repeated_failure", "noul"), float("nan")),
        (("answers", "repeated_failure", "noul"), True),
        (("answers", "repeated_failure", "noul"), -0.1),
        (("answers", "context_relevance", "score"), 3.0),
        (("answers", "next_step", "confidence"), 1.1),
        (("answers", "next_step", "probabilities"), {"inspect": 1.0}),
        (("usage", "input_tokens"), True),
    ]:
        bad = copy.deepcopy(fixture)
        parent = bad
        for component in path[:-1]:
            parent = parent[component]
        parent[path[-1]] = value
        cases.append(bad)
    for index, bad in enumerate(cases):
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"Invalid fixture {index} was accepted")
    print(f"PASS: 1 valid and {len(cases)} invalid local fixtures; no network calls.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="print synthetic payload only (default)")
    mode.add_argument("--self-test", action="store_true", help="run offline schema fixtures")
    mode.add_argument("--live", action="store_true", help="send one synthetic request; may incur API charges")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.live:
        return live()
    print(json.dumps(payload(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
