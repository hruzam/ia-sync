"""OpenRouter Decisions adapter; importing this module performs no I/O."""

from decimal import Decimal
import http.client
import json
import math
import ssl

import kernel

ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
ADAPTER_VERSION = "jev.openrouter-decisions/v1"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class ProviderError(ValueError):
    pass


def build_request(packet, model):
    """Freeze a complete explicit packet into a canonical provider body."""
    kernel.validate_packet(packet)
    kernel.string(model, "provider.model")
    questions = {}
    for question in packet["questions"]:
        kind = question["type"]
        mapped = {"type": kind, "instructions": question["text"]}
        if kind == "choice":
            kernel.require(len(question["options"]) <= 255,
                           "provider.choice: exceeds 255 options")
            mapped["criteria"] = {option: option for option in question["options"]}
        elif kind == "score":
            kernel.require(len(question["levels"]) <= 10,
                           "provider.score: exceeds 10 levels")
            mapped["criteria"] = question["levels"]
        questions[question["id"]] = mapped
    body = kernel.canonical({"model": model, "questions": questions, "state": packet,
                             "provider": {"allow_fallbacks": False}})
    kernel.require(len(body) <= kernel.MAX_BYTES, "provider body: exceeds byte bound")
    return body


def parse_response(prepared, raw_bytes, allowed_models):
    """Map an OpenRouter body; cost is independent of typed-advice validity.

    The caller retains the original bytes and decides whether the HTTP status is trusted.
    Correlation fields are local mappings, not provider-authenticated echoes.
    """
    result = {"receipt": None, "validation": {"status": "INVALID", "errors": []},
              "cost_usd": None, "provider_id": None, "model": None}
    try:
        kernel.require(isinstance(raw_bytes, bytes), "response: expected bytes")
        kernel.require(len(raw_bytes) <= kernel.MAX_BYTES, "response: exceeds byte bound")
        text = raw_bytes.decode("utf-8")
        exact = json.loads(text, object_pairs_hook=kernel.unique_object,
                           parse_float=Decimal, parse_constant=kernel.invalid_constant)
        # Keep the original numeric token precision for accounting. The second parse supplies
        # ordinary JSON numbers to the existing kernel, without changing the raw bytes.
        wire = json.loads(text, object_pairs_hook=kernel.unique_object,
                          parse_constant=kernel.invalid_constant)
    except (ValueError, UnicodeError, RecursionError, ArithmeticError):
        result["validation"]["errors"] = ["response: invalid, duplicate-key or oversized JSON"]
        return result

    if isinstance(wire, dict):
        for source, destination in (("model", "model"), ("id", "provider_id")):
            value = wire.get(source)
            if isinstance(value, str):
                try:
                    kernel.string(value, f"response.{source}")
                    result[destination] = value
                except kernel.Invalid:
                    pass
        usage = exact.get("usage")
        if isinstance(usage, dict):
            cost = usage.get("cost")
            if type(cost) in (int, Decimal):
                amount = Decimal(cost)
                if amount.is_finite() and amount >= 0:
                    result["cost_usd"] = str(amount)

    try:
        kernel.validate_prepared(prepared)
        kernel.require(isinstance(allowed_models, (list, tuple, set, frozenset)),
                       "provider model policy: expected explicit collection")
        kernel.require(bool(allowed_models), "provider model policy: empty allow-list")
        for model in allowed_models:
            kernel.string(model, "provider allowed model")
        kernel.fields(wire, ("answers", "model", "usage"), ("id", "provider"), "response")
        kernel.string(wire["model"], "response.model")
        kernel.require(wire["model"] in allowed_models, "response.model: not allowed")
        kernel.require(isinstance(wire["usage"], dict), "response.usage: expected object")
        for name in ("id", "provider"):
            if name in wire:
                kernel.string(wire[name], f"response.{name}")
        questions = prepared["packet"]["questions"]
        kernel.fields(wire["answers"], [q["id"] for q in questions], path="response.answers")
        answers = []
        for question in questions:
            qid, kind = question["id"], question["type"]
            answer = wire["answers"][qid]
            value_key = {"noul": "noul", "choice": "choice", "score": "score"}[kind]
            required = ("type", value_key)
            if kind != "noul":
                required += ("probabilities", "confidence")
            if kind == "score":
                required += ("legend",)
            kernel.fields(answer, required, path=f"response.answers.{qid}")
            kernel.require(answer["type"] == kind, f"response.answers.{qid}: type mismatch")
            if kind == "score":
                legend = {str(i): level for i, level in enumerate(question["levels"])}
                kernel.require(answer["legend"] == legend,
                               f"response.answers.{qid}.legend: rubric mismatch")
            mapped = {"id": qid, "type": kind,
                      "probability" if kind == "noul" else "value": answer[value_key]}
            if kind != "noul":
                mapped.update(probabilities=answer["probabilities"],
                              confidence=answer["confidence"])
            answers.append(mapped)
        result["receipt"] = {"schema": "jev.receipt/v1",
                             "request_id": prepared["request_id"],
                             "packet_sha256": prepared["packet_sha256"],
                             "model": wire["model"], "answers": answers}
        kernel.validate_receipt(prepared, result["receipt"])
    except (kernel.Invalid, TypeError, ValueError, RecursionError, OverflowError) as error:
        result["validation"]["errors"] = [str(error) if isinstance(error, kernel.Invalid)
                                           else "response: invalid typed content"]
        return result
    result["validation"] = {"status": "VALID", "errors": []}
    return result


def post(body_bytes, key, *, timeout=30, max_bytes=1048576):
    """One fixed-endpoint HTTPS POST; no environment proxy, redirects or retries."""
    if (not isinstance(body_bytes, bytes) or len(body_bytes) > kernel.MAX_BYTES or
            not isinstance(key, str) or not key or
            any(ord(character) < 33 or ord(character) > 126 for character in key) or
            type(timeout) not in (int, float) or timeout <= 0 or
            (type(timeout) is float and not math.isfinite(timeout)) or
            type(max_bytes) is not int or not 0 < max_bytes <= kernel.MAX_BYTES):
        raise ProviderError("provider transport: invalid arguments")
    connection = None
    try:
        connection = http.client.HTTPSConnection("openrouter.ai", timeout=timeout,
                                                 context=ssl.create_default_context())
        connection.request("POST", "/api/alpha/decisions", body=body_bytes,
                           headers={**HEADERS, "Authorization": "Bearer " + key})
        response = connection.getresponse()
        raw = response.read(max_bytes + 1)
        status = response.status
    except Exception:
        # Never include HTTP, TLS or OS exception text: it may contain the bearer key.
        raise ProviderError("provider transport failed; remote completion is unknown") from None
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
    if len(raw) > max_bytes:
        raise ProviderError("provider response: exceeds byte bound; remote completion is unknown")
    return status, raw
