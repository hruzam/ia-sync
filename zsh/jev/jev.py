#!/usr/bin/env python3
"""Jev: explicit private judgment sessions. Advice never executes actions."""

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import stat
import sys

import kernel
import provider
import store

Invalid = kernel.Invalid
require = kernel.require


def cli_origin(cli=None, session_id=None, environment=None):
    """Resolve only supported observed Codex keys; explicit pairs win entirely."""
    require((cli is None) == (session_id is None), "--cli and --cli-session must be supplied together")
    result = dict.fromkeys(store.CLI_SLOTS)
    if cli is not None:
        require(cli in ("codex", "claude", "gemini"), "unsupported CLI origin")
        result[cli] = store.cli_session_id(session_id)
        return result
    environment = os.environ if environment is None else environment
    detected = []
    for name in ("CODEX_THREAD_ID", "CODEX_SESSION_ID"):
        if name in environment:
            detected.append(store.cli_session_id(environment[name]))
    require(len(detected) < 2 or detected[0] == detected[1], "conflicting observed Codex session IDs")
    if detected:
        result["codex"] = detected[0]
    return result


def read_bytes(path):
    try:
        with Path(path).open("rb") as source:
            raw = source.read(kernel.MAX_BYTES + 1)
    except OSError:
        raise Invalid("input file unavailable") from None
    require(len(raw) <= kernel.MAX_BYTES, "input exceeds byte bound")
    return raw


def prepare(ledger, packet_path, *, lineage=None, memory=None, selection=None,
            upper_bound=None, bound_evidence=None):
    raw = read_bytes(packet_path)
    packet = store.parse(raw)
    # Validate supplied semantics before adding explicitly selected history.
    kernel.validate_packet(packet)
    require(packet["session_id"] == ledger.session_id and packet["channel"] == "main", "packet/session binding mismatch")
    if memory:
        packet["memory"] = copy.deepcopy(ledger.by_id(memory, "memory")["data"]["note"])
    if selection:
        manifest = ledger.by_id(selection, "select")["data"]["selection"]
        require("jev_selection" not in packet["state"], "reserved jev_selection state field")
        packet["state"]["jev_selection"] = {
            "event_id": selection, "manifest": copy.deepcopy(manifest),
            "source_events": [copy.deepcopy(ledger.by_id(item["event_id"])) for item in manifest["items"]]}
    if lineage is not None:
        ledger.lineage(lineage)
    if upper_bound is not None:
        store.money(upper_bound)
        kernel.string(bound_evidence, "bound evidence")
    else:
        require(bound_evidence is None, "bound evidence requires upper bound")
    prepared = kernel.prepare(packet)
    model = ledger.events[0]["data"]["policy"]["model"]
    frozen = None
    if model is not None:
        body = provider.build_request(prepared["packet"], model)
        frozen = {"method": "POST", "endpoint": provider.ENDPOINT, "headers": dict(provider.HEADERS),
                  "model": model, "adapter_version": provider.ADAPTER_VERSION,
                  "body_base64": store.encode_bytes(body), "sha256": kernel.digest(body)}
    event = ledger.append("prepare", {"prepared": prepared,
                          "source": {"path": str(Path(packet_path).absolute()), "sha256": kernel.digest(raw)},
                          "lineage": lineage, "memory_event_id": memory, "selection_event_id": selection,
                          "provider": frozen, "upper_bound_usd": upper_bound, "bound_evidence": bound_evidence},
                          prepared["request_id"])
    return {"request_id": prepared["request_id"], "event": event, "prepared": prepared}


def import_reply(ledger, request_id, path):
    prepared = ledger.request(request_id)["data"]["prepared"]
    raw = read_bytes(path)
    try:
        receipt = store.parse(raw)
        checked = kernel.check(prepared, receipt)
        validation = {key: checked[key] for key in ("status", "errors")}
    except Invalid as error:
        receipt, validation = None, {"status": "INVALID", "errors": [str(error)]}
    return ledger.append("reply", {"source": "synthetic", "raw_base64": store.encode_bytes(raw),
                                   "raw_sha256": kernel.digest(raw), "receipt": receipt,
                                   "validation": validation, "http_event_id": None}, request_id)


def interpret(ledger, request_id, question_id, policy_path):
    prepared = ledger.request(request_id)["data"]["prepared"]
    replies = ledger.related(request_id, "reply")
    reply = replies[0] if replies else None
    policy = None
    try:
        policy = store.parse(read_bytes(policy_path))
        require(reply is not None, "no receipt")
        require(reply["data"]["validation"]["status"] == "VALID", "receipt is invalid")
        result = kernel.interpret(prepared, reply["data"]["receipt"], question_id, policy)
    except Invalid as error:
        # File parse failures are represented by an explicit invalid policy object, so
        # replay can reproduce the error without consulting mutable external files.
        if policy is None:
            policy = {"input_error": str(error), "path": str(Path(policy_path).absolute())}
        result = {"status": "ERROR", "errors": [str(error)], "request_id": request_id,
                  "question_id": question_id, "policy": policy}
    return ledger.append("interpret", {"question_id": question_id, "policy": policy,
                                       "receipt_event_id": reply["event_id"] if reply else None,
                                       "result": result}, request_id)


def approval(ledger, request_id):
    return ledger.approval(request_id)


def guard_human():
    # Cooperative same-user guard. It is deliberately not described as authentication.
    forbidden = {"CI", "CURSOR_AGENT", "GEMINI_CLI", "CLAUDECODE"}
    require(not any(key in forbidden or key.startswith(("CODEX_", "CLAUDE_CODE_"))
                    for key in os.environ), "send refused in agent/tool environment")
    require(sys.stdin.isatty() and sys.stdout.isatty(), "send requires an interactive operator terminal")


def confirm_terminal(value, approval_sha256):
    try:
        with open("/dev/tty", "r+", encoding="utf-8", buffering=1) as terminal:
            terminal.write("Jev saved request (body_utf8 is the complete exact UTF-8 payload):\n")
            terminal.write(kernel.canonical(value).decode("utf-8") + "\n")
            terminal.write("Approval SHA-256: " + approval_sha256 + "\n")
            terminal.write("Type the first 12 hash characters to send once, or Enter to cancel: ")
            terminal.flush()
            answer = terminal.readline(128)
            return answer == approval_sha256[:12] + "\n"
    except OSError:
        raise Invalid("controlling terminal unavailable") from None


def read_credential(path):
    path = store.no_symlinks(path)
    descriptor = None
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1,
                "credential requires owned regular nonsymlink 0600 file")
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        opened = os.fstat(descriptor)
        require((info.st_dev, info.st_ino) == (opened.st_dev, opened.st_ino)
                and opened.st_uid == os.getuid() and stat.S_IMODE(opened.st_mode) == 0o600
                and stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1,
                "credential changed while opening")
        data = os.read(descriptor, 4097)
        require(0 < len(data) <= 4096, "credential size invalid")
        key = data.decode("ascii").removesuffix("\n")
        require(key and all(33 <= ord(character) <= 126 for character in key), "credential format invalid")
        return key
    except (OSError, UnicodeError):
        raise Invalid("credential unavailable or invalid") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def read_send_grant(path):
    path = store.no_symlinks(path)
    descriptor = None
    try:
        store.private(path)
        before = path.lstat()
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        opened = os.fstat(descriptor)
        require(stat.S_ISREG(opened.st_mode) and opened.st_uid == os.getuid()
                and stat.S_IMODE(opened.st_mode) == 0o600 and opened.st_nlink == 1
                and (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
                "send grant changed while opening")
        raw = os.read(descriptor, 16385)
        require(len(raw) <= 16384, "send grant exceeds 16 KiB")
        return store.parse(raw)
    except OSError:
        raise Invalid("send grant unavailable") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def read_env_credential(name):
    require(name == "JEV_ORAK_KEY", "unsupported delegated credential environment name")
    value = os.environ.get(name)
    require(isinstance(value, str) and 1 <= len(value) <= 4096
            and all(0x21 <= ord(character) <= 0x7e for character in value),
            "delegated credential unavailable or invalid")
    return value


def trusted_cost(value):
    return store.trusted_cost(value)


def send(vault, session_id, request_id, credential_file=None, *, authorization_file=None,
         credential_env=None, confirm=None, credential=None, transport=None, guard=None):
    """One lock, one fresh confirmation, one durable attempt, at most one transport.

    Explicit callable seams permit offline tests. The CLI cannot select these seams.
    """
    delegated = authorization_file is not None or credential_env is not None
    require((delegated and authorization_file is not None and credential_env == "JEV_ORAK_KEY"
             and credential_file is None) or (not delegated and credential_file is not None),
            "send requires credential-file OR authorization-file with credential-env JEV_ORAK_KEY")
    if not delegated:
        (guard or guard_human)()
    with vault.selected(session_id, "main") as ledger:
        require(ledger.tail is None, "incomplete tail blocks sends")
        value, approval_hash = approval(ledger, request_id)
        authorization = None
        if delegated:
            grant = read_send_grant(authorization_file)
            ledger.validate_send_grant(request_id, grant, datetime.now(timezone.utc))
            authorization = {"grant": grant, "grant_sha256": kernel.digest(kernel.canonical(grant))}
        elif not (confirm or confirm_terminal)(value, approval_hash):
            return {"status": "CANCELLED", "request_id": request_id, "approval_sha256": approval_hash}
        prepared_event = ledger.request(request_id)
        attempt_data = {"upper_bound_usd": value["upper_bound_usd"], "approval_sha256": approval_hash,
                        "prepared_event_id": prepared_event["event_id"]}
        if authorization is not None:
            attempt_data["authorization"] = authorization
        attempt = ledger.append("attempt", attempt_data, request_id)
        prepared_event = ledger.request(request_id)
        body = store.decode_bytes(prepared_event["data"]["provider"]["body_base64"])
        try:
            key = read_env_credential(credential_env) if delegated else (credential or read_credential)(credential_file)
            status, raw = (transport or provider.post)(body, key)
            require(type(status) is int and 100 <= status <= 599 and isinstance(raw, bytes)
                    and len(raw) <= kernel.MAX_BYTES, "invalid transport return")
            require(not key or key.encode("utf-8") not in raw, "response contains credential material")
            try:
                decoded_json = kernel.canonical(store.parse(raw))
            except Invalid:
                decoded_json = b""
            require(not key or key.encode("utf-8") not in decoded_json,
                    "decoded response contains credential material")
        except Exception:
            event = ledger.append("uncertain", {"attempt_event_id": attempt["event_id"], "reason": "transport"}, request_id)
            return {"status": "UNKNOWN", "request_id": request_id, "event": event, "budget": ledger.budget()}
        # Persist HTTP bytes/status before asking the adapter to interpret anything.
        http = ledger.append("http", {"attempt_event_id": attempt["event_id"], "status": status,
                                     "raw_base64": store.encode_bytes(raw), "raw_sha256": kernel.digest(raw)}, request_id)
        try:
            parsed = provider.parse_response(prepared_event["data"]["prepared"], raw,
                                             ledger.events[0]["data"]["policy"]["allowed_models"])
        except Exception:
            event = ledger.append("uncertain", {"attempt_event_id": attempt["event_id"], "reason": "parse"}, request_id)
            return {"status": "UNKNOWN", "request_id": request_id, "event": event, "budget": ledger.budget()}
        reply = ledger.append("reply", {"source": "provider", "raw_base64": store.encode_bytes(raw),
                                        "raw_sha256": kernel.digest(raw), "receipt": parsed["receipt"],
                                        "validation": parsed["validation"], "http_event_id": http["event_id"]}, request_id)
        cost = trusted_cost(parsed["cost_usd"]) if 200 <= status < 300 else None
        if cost is None:
            event = ledger.append("uncertain", {"attempt_event_id": attempt["event_id"],
                                               "reason": "unknown_cost" if 200 <= status < 300 else "http_status"}, request_id)
            return {"status": "UNKNOWN", "request_id": request_id, "event": event,
                    "reply_event_id": reply["event_id"], "budget": ledger.budget()}
        event = ledger.append("settle", {"attempt_event_id": attempt["event_id"], "http_event_id": http["event_id"],
                                        "cost_usd": cost, "provider_id": parsed["provider_id"], "model": parsed["model"]}, request_id)
        budget = ledger.budget()
        return {"status": "OVERRUN" if budget["overrun_request_ids"] else "SETTLED", "request_id": request_id,
                "event": event, "reply_event_id": reply["event_id"], "validation": parsed["validation"], "budget": budget}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Invalid("arguments: " + message)


def parser():
    result = Parser(description=__doc__)
    result.add_argument("--root", default="~/.jev")
    result.add_argument("--session")
    result.add_argument("--channel")
    result.add_argument("--cli", choices=("codex", "claude", "gemini"))
    result.add_argument("--cli-session")
    result.add_argument("--requester", choices=("hlm", "agent"))
    commands = result.add_subparsers(dest="command", required=True)
    command = commands.add_parser("open")
    command.add_argument("--project", required=True)
    command.add_argument("--bed", required=True)
    command.add_argument("--budget")
    command.add_argument("--model")
    command.add_argument("--allow-model", action="append", default=[])
    commands.add_parser("settings")
    command = commands.add_parser("prepare")
    command.add_argument("packet")
    for flag in ("lineage", "memory", "selection", "upper-bound", "bound-evidence"):
        command.add_argument("--" + flag)
    command = commands.add_parser("import-reply")
    command.add_argument("request")
    command.add_argument("receipt")
    command = commands.add_parser("interpret")
    for argument in ("request", "question", "policy"):
        command.add_argument(argument)
    command = commands.add_parser("dispose")
    command.add_argument("request")
    command.add_argument("decision", choices=("use", "skip", "reconsider"))
    command.add_argument("--consumer", required=True)
    command.add_argument("--reason", default="")
    command = commands.add_parser("outcome")
    command.add_argument("request")
    command.add_argument("file")
    command = commands.add_parser("show")
    command.add_argument("--request")
    commands.add_parser("ref").add_argument("request")
    commands.add_parser("memory").add_argument("file")
    commands.add_parser("select").add_argument("file")
    commands.add_parser("reconcile")
    command = commands.add_parser("send")
    command.add_argument("request")
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--credential-file")
    mode.add_argument("--authorization-file")
    command.add_argument("--credential-env")
    return result


def main(argv=None):
    try:
        args = parser().parse_args(argv)
        vault = store.Vault(args.root, cli_sessions=cli_origin(args.cli, args.cli_session), requester=args.requester)
        if args.command == "open":
            require(args.session is None and args.channel is None, "open takes no session/channel selection")
            result = vault.open(args.project, args.bed, args.budget, args.model, args.allow_model)
        else:
            require(args.session is not None and args.channel == "main", "explicit --session and --channel main required")
            if args.command == "send":
                result = send(vault, args.session, args.request, args.credential_file,
                              authorization_file=args.authorization_file, credential_env=args.credential_env)
            else:
                with vault.selected(args.session, args.channel) as ledger:
                    if args.command == "settings":
                        result = ledger.settings()
                    elif args.command == "show":
                        if args.request:
                            ledger.request(args.request)
                        result = {"session_id": ledger.session_id, "ledger": str(ledger.path), "tail": ledger.tail,
                                  "events": [event for event in ledger.events if not args.request or event["request_id"] == args.request]}
                    elif args.command == "ref":
                        prepared = ledger.request(args.request)
                        replies = ledger.related(args.request, "reply")
                        referenced = replies[-1] if replies else prepared
                        result = {"session_id": ledger.session_id, "request_id": args.request, "tail": ledger.tail,
                                  "ledger": str(ledger.path), "event_id": referenced["event_id"],
                                  "sequence": referenced["sequence"], "kind": referenced["kind"],
                                  "prepared_event_id": prepared["event_id"], "actor": copy.deepcopy(referenced["actor"])}
                    elif args.command == "reconcile":
                        result = ledger.reconcile()
                    elif args.command == "prepare":
                        result = prepare(ledger, args.packet, lineage=kernel.load(args.lineage) if args.lineage else None,
                                         memory=args.memory, selection=args.selection, upper_bound=args.upper_bound,
                                         bound_evidence=args.bound_evidence)
                    elif args.command == "import-reply":
                        result = import_reply(ledger, args.request, args.receipt)
                    elif args.command == "interpret":
                        result = interpret(ledger, args.request, args.question, args.policy)
                    elif args.command == "dispose":
                        result = ledger.append("dispose", {"decision": args.decision, "consumer": args.consumer,
                                                           "reason": args.reason}, args.request)
                    elif args.command == "outcome":
                        result = ledger.append("outcome", {"observation": kernel.load(args.file),
                                                          "request_event_id": ledger.request(args.request)["event_id"]}, args.request)
                    elif args.command == "memory":
                        result = ledger.append("memory", {"note": kernel.load(args.file)})
                    elif args.command == "select":
                        result = ledger.append("select", {"selection": kernel.load(args.file)})
        status = result.get("status")
        if isinstance(result.get("data"), dict):
            status = result["data"].get("result", result["data"].get("validation", {})).get("status", status)
        code = 2 if status in {"ERROR", "INVALID", "UNKNOWN", "OVERRUN"} else 0
    except (Invalid, OSError, RecursionError) as error:
        result = {"status": "ERROR", "errors": [str(error) if isinstance(error, Invalid) else "local persistence/input failure"]}
        code = 2
    print(kernel.canonical(result).decode("utf-8"))
    return code


if __name__ == "__main__":
    sys.exit(main())
