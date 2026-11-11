#!/usr/bin/env python3
"""Offline Jev packet kernel. No provider adapter, transport or runtime store."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import uuid

MAX_BYTES = 1024 * 1024
MAX_QUESTIONS = 20
TOLERANCE = 1e-6


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def fields(value, required, optional=(), path="object"):
    require(isinstance(value, dict), f"{path}: expected object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    require(not missing, f"{path}: missing fields {sorted(missing)}")
    require(not extra, f"{path}: unknown fields {sorted(extra)}")


def string(value, path, empty=False):
    require(isinstance(value, str), f"{path}: expected string")
    require(empty or bool(value.strip()), f"{path}: expected nonempty string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise Invalid(f"{path}: invalid Unicode") from None


def strings(value, path, minimum=0, unique=False):
    require(isinstance(value, list), f"{path}: expected list")
    require(len(value) >= minimum, f"{path}: needs at least {minimum} entries")
    for index, item in enumerate(value):
        string(item, f"{path}[{index}]")
    require(not unique or len(set(value)) == len(value), f"{path}: duplicate entries")


def number(value, path, low=0, high=1):
    require(type(value) in (int, float), f"{path}: expected number, not boolean")
    require(type(value) is int or math.isfinite(value), f"{path}: nonfinite number")
    require(low <= value <= high, f"{path}: outside [{low}, {high}]")


def finite_json(value, path="input"):
    if isinstance(value, dict):
        for key, item in value.items():
            string(key, f"{path} key", empty=True)
            finite_json(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            finite_json(item, f"{path}[{index}]")
    elif isinstance(value, str):
        string(value, path, empty=True)
    elif isinstance(value, float):
        require(math.isfinite(value), f"{path}: nonfinite number")
    else:
        require(value is None or type(value) in (int, bool), f"{path}: invalid JSON value")


def canonical(value):
    finite_json(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON: duplicate object key {key!r}")
        result[key] = value
    return result


def invalid_constant(value):
    raise Invalid(f"JSON: invalid constant {value}")


def load(path):
    try:
        with Path(path).open("rb") as source:
            data = source.read(MAX_BYTES + 1)
        require(len(data) <= MAX_BYTES, f"{path}: exceeds {MAX_BYTES} bytes")
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                           parse_constant=invalid_constant)
        finite_json(value)
        return value
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise Invalid(f"{path}: cannot read JSON ({type(error).__name__})") from None
    except ValueError as error:
        if isinstance(error, Invalid):
            raise
        raise Invalid(f"{path}: invalid JSON number") from None


def validate_packet(packet):
    fields(packet, ("schema", "case_id", "target", "related_case_group", "session_id",
                    "channel", "protocol", "state", "evidence", "missing_evidence",
                    "questions"), ("memory",), "packet")
    require(packet["schema"] == "jev.case/v1", "packet.schema: unsupported schema")
    for name in ("case_id", "target", "related_case_group", "session_id", "channel"):
        string(packet[name], f"packet.{name}")
    require(packet["channel"] == "main", "packet.channel: only main is supported")
    fields(packet["protocol"], ("id", "version"), path="packet.protocol")
    for name in ("id", "version"):
        string(packet["protocol"][name], f"packet.protocol.{name}")
    require(isinstance(packet["state"], dict), "packet.state: expected object")
    require(isinstance(packet["evidence"], list), "packet.evidence: expected list")
    evidence_ids = set()
    for index, item in enumerate(packet["evidence"]):
        path = f"packet.evidence[{index}]"
        fields(item, ("id", "ref", "text"), path=path)
        for name in ("id", "ref", "text"):
            string(item[name], f"{path}.{name}", empty=name == "text")
        require(item["id"] not in evidence_ids, f"{path}.id: duplicate evidence ID")
        evidence_ids.add(item["id"])
    strings(packet["missing_evidence"], "packet.missing_evidence")
    questions = packet["questions"]
    require(isinstance(questions, list), "packet.questions: expected list")
    require(1 <= len(questions) <= MAX_QUESTIONS, "packet.questions: needs 1..20 entries")
    question_ids = set()
    for index, question in enumerate(questions):
        path = f"packet.questions[{index}]"
        require(isinstance(question, dict), f"{path}: expected object")
        kind = question.get("type")
        require(kind in ("choice", "noul", "score"), f"{path}.type: unsupported type")
        extra = {"choice": ("options",), "noul": (), "score": ("levels",)}[kind]
        fields(question, ("id", "type", "text", "rubric_version", "predicate_meaning") + extra,
               path=path)
        for name in ("id", "text", "rubric_version", "predicate_meaning"):
            string(question[name], f"{path}.{name}")
        require(question["id"] not in question_ids, f"{path}.id: duplicate question ID")
        question_ids.add(question["id"])
        if extra:
            strings(question[extra[0]], f"{path}.{extra[0]}", minimum=2, unique=True)
    if "memory" in packet:
        note = packet["memory"]
        fields(note, ("version", "author", "text", "refs"), path="packet.memory")
        for name in ("version", "author", "text"):
            string(note[name], f"packet.memory.{name}")
        strings(note["refs"], "packet.memory.refs")
    require(len(canonical(packet)) <= MAX_BYTES, "packet: exceeds byte bound")


def packet_hashes(packet):
    return {
        "packet_sha256": digest(canonical(packet)),
        "evidence_sha256": {item["id"]: digest(item["text"].encode("utf-8"))
                            for item in packet["evidence"]},
        "memory_sha256": digest(canonical(packet["memory"])) if "memory" in packet else None,
    }


def prepare(packet):
    validate_packet(packet)
    frozen = json.loads(canonical(packet))
    result = {"schema": "jev.prepared/v1", "request_id": uuid.uuid4().hex,
              "packet": frozen, **packet_hashes(frozen)}
    require(len(canonical(result)) + 1 <= MAX_BYTES, "prepared: exceeds byte bound with metadata")
    return result


def validate_prepared(prepared):
    fields(prepared, ("schema", "request_id", "packet", "packet_sha256",
                      "evidence_sha256", "memory_sha256"), path="prepared")
    require(prepared["schema"] == "jev.prepared/v1", "prepared.schema: unsupported schema")
    string(prepared["request_id"], "prepared.request_id")
    validate_packet(prepared["packet"])
    expected = packet_hashes(prepared["packet"])
    for name, value in expected.items():
        require(prepared[name] == value, f"prepared.{name}: hash mismatch")
    require(len(canonical(prepared)) <= MAX_BYTES, "prepared: exceeds byte bound")


def distribution(answer, keys, path):
    probabilities = answer["probabilities"]
    fields(probabilities, keys, path=f"{path}.probabilities")
    for key, value in probabilities.items():
        number(value, f"{path}.probabilities.{key}")
    require(abs(sum(probabilities.values()) - 1) <= TOLERANCE,
            f"{path}.probabilities: sum differs from 1")
    return probabilities


def validate_receipt(prepared, receipt):
    validate_prepared(prepared)
    fields(receipt, ("schema", "request_id", "packet_sha256", "model", "answers"),
           path="receipt")
    require(receipt["schema"] == "jev.receipt/v1", "receipt.schema: unsupported schema")
    for name in ("request_id", "packet_sha256"):
        require(receipt[name] == prepared[name], f"receipt.{name}: correlation mismatch")
    string(receipt["model"], "receipt.model")
    require(isinstance(receipt["answers"], list), "receipt.answers: expected list")
    questions = {q["id"]: q for q in prepared["packet"]["questions"]}
    seen = set()
    for index, answer in enumerate(receipt["answers"]):
        path = f"receipt.answers[{index}]"
        require(isinstance(answer, dict), f"{path}: expected object")
        string(answer.get("id"), f"{path}.id")
        qid = answer["id"]
        require(qid in questions, f"{path}.id: unrequested question")
        require(qid not in seen, f"{path}.id: duplicate answer")
        seen.add(qid)
        question = questions[qid]
        kind = question["type"]
        extras = ("probability",) if kind == "noul" else ("value", "probabilities")
        fields(answer, ("id", "type") + extras,
               ("confidence",) if kind != "noul" else (), path)
        require(answer["type"] == kind, f"{path}.type: mismatches question")
        if "confidence" in answer:
            number(answer["confidence"], f"{path}.confidence")
        if kind == "noul":
            number(answer["probability"], f"{path}.probability")
        elif kind == "choice":
            probabilities = distribution(answer, question["options"], path)
            string(answer["value"], f"{path}.value")
            require(answer["value"] in probabilities, f"{path}.value: unknown option")
            require(max(probabilities.values()) - probabilities[answer["value"]] <= TOLERANCE,
                    f"{path}.value: not a maximizing option")
        else:
            keys = [str(i) for i in range(len(question["levels"]))]
            probabilities = distribution(answer, keys, path)
            highest = len(keys) - 1
            number(answer["value"], f"{path}.value", high=highest)
            expected = sum(i * probabilities[str(i)] for i in range(len(keys)))
            require(abs(expected - answer["value"]) <= TOLERANCE * max(1, highest),
                    f"{path}.value: differs from expected rubric index")
    require(seen == questions.keys(), f"receipt.answers: missing IDs {sorted(questions.keys() - seen)}")


def check(prepared, receipt):
    try:
        validate_receipt(prepared, receipt)
    except Invalid as error:
        return {"status": "INVALID", "errors": [str(error)], "receipt": receipt}
    return {"status": "VALID", "errors": [], "receipt": receipt}


def interpret(prepared, receipt, question_id, policy):
    validate_receipt(prepared, receipt)
    fields(policy, ("id", "version", "low", "high"), path="policy")
    for name in ("id", "version"):
        string(policy[name], f"policy.{name}")
    for name in ("low", "high"):
        number(policy[name], f"policy.{name}")
    require(policy["low"] < policy["high"], "policy: low must be below high")
    question = next((q for q in prepared["packet"]["questions"] if q["id"] == question_id), None)
    require(question is not None, "question: unknown question ID")
    require(question["type"] == "noul", "question: interpretation requires Noul")
    answer = next(a for a in receipt["answers"] if a["id"] == question_id)
    probability = answer["probability"]
    decision = "NO" if probability <= policy["low"] else (
        "YES" if probability >= policy["high"] else "UNCERTAIN")
    return {"status": decision, "request_id": prepared["request_id"],
            "packet_sha256": prepared["packet_sha256"], "question_id": question_id,
            "probability": probability, "policy": json.loads(canonical(policy))}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Invalid(f"arguments: {message}")


def main(argv=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("prepare").add_argument("packet")
    command = commands.add_parser("check")
    command.add_argument("prepared")
    command.add_argument("receipt")
    command = commands.add_parser("interpret")
    for name in ("prepared", "receipt", "question", "policy"):
        command.add_argument(name)
    error_context = {}
    try:
        args = parser.parse_args(argv)
        if args.command == "prepare":
            result = prepare(load(args.packet))
        elif args.command == "check":
            result = check(load(args.prepared), load(args.receipt))
        else:
            error_context = {
                "request_id": None, "packet_sha256": None, "question_id": args.question,
                "policy": None, "prepared_validation": "UNAVAILABLE",
                "policy_validation": "UNVALIDATED",
                "input_files": {name: getattr(args, name)
                                for name in ("prepared", "receipt", "policy")},
            }
            prepared = load(args.prepared)
            error_context["prepared_validation"] = "INVALID"
            validate_prepared(prepared)
            error_context.update(request_id=prepared["request_id"],
                                 packet_sha256=prepared["packet_sha256"],
                                 prepared_validation="VALID")
            policy = load(args.policy)
            error_context["policy"] = policy
            result = interpret(prepared, load(args.receipt), args.question, policy)
    except (Invalid, RecursionError) as error:
        result = {"status": "ERROR", "errors": [str(error) if isinstance(error, Invalid)
                                                 else "input: nesting is too deep"],
                  **error_context}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(",", ":")))
    return 2 if result.get("status") in ("INVALID", "ERROR") else 0


if __name__ == "__main__":
    sys.exit(main())
