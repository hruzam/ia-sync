"""Private append-only Jev vault. Hashes detect local inconsistency, not forgery."""

from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import base64
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import time
import uuid

import kernel

Invalid = kernel.Invalid
require = kernel.require
ID = re.compile(r"^[0-9a-f]{32}$")
HASH = re.compile(r"^[0-9a-f]{64}$")
MONEY = re.compile(r"^(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,18})?$")
MAX_LEDGER = 64 * 1024 * 1024
MAX_EVENT = 5 * kernel.MAX_BYTES
KINDS = {"open", "prepare", "reply", "interpret", "dispose", "outcome", "memory",
         "select", "attempt", "http", "settle", "uncertain", "recovery"}
ACTOR = {"source": "record", "name": "jev"}
CLI_SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
CLI_SLOTS = ("codex", "claude", "gemini", "controller")
CERTAINTY = {"http": "observed", "reply": "observed", "interpret": "inferred", "uncertain": "unknown"}


def cli_session_id(value):
    require(isinstance(value, str) and CLI_SESSION_ID.fullmatch(value) is not None,
            "CLI session ID: expected 1..128 ASCII letters/digits or . _ : -, starting with letter/digit")
    return value


def validate_actor(value):
    if value == ACTOR:
        return  # Exact legacy shape: do not normalize old events or change their hashes.
    kernel.fields(value, ("source", "name", "cli_sessions", "requester"), path="actor")
    require(value["source"] == ACTOR["source"] and value["name"] == ACTOR["name"], "unknown actor provenance")
    kernel.fields(value["cli_sessions"], CLI_SLOTS, path="actor.cli_sessions")
    require(value["cli_sessions"]["controller"] is None, "controller CLI session is reserved")
    for slot in CLI_SLOTS[:-1]:
        if value["cli_sessions"][slot] is not None:
            cli_session_id(value["cli_sessions"][slot])
    require(value["requester"] in (None, "hlm", "agent"), "requester must be hlm, agent or null")


def actor(cli_sessions=None, requester=None):
    # Direct library calls never inspect runtime environment or inherit opening provenance.
    value = {**ACTOR, "cli_sessions": dict(cli_sessions) if isinstance(cli_sessions, dict) else cli_sessions,
             "requester": requester}
    if cli_sessions is None:
        value["cli_sessions"] = dict.fromkeys(CLI_SLOTS)
    validate_actor(value)
    return value


def money(value):
    require(isinstance(value, str) and MONEY.fullmatch(value) is not None,
            "USD: expected nonnegative decimal string, <=18 integer/fraction digits")
    return Decimal(value)


def decimal_text(value):
    return format(value, "f")


def total(values):
    with localcontext() as context:
        context.prec = 96
        return sum(values, Decimal(0))


def trusted_cost(value):
    """Normalize only bounded exactly representable provider costs."""
    if value is None:
        return None
    try:
        amount = Decimal(value)
        require(amount.is_finite() and amount >= 0, "invalid cost")
        require(amount.adjusted() <= 17 and amount.as_tuple().exponent >= -18,
                "unsupported cost range/precision")
        result = format(amount, "f")
        money(result)
        return result
    except (ValueError, ArithmeticError, Invalid):
        return None


def parse(data):
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=kernel.unique_object,
                           parse_constant=kernel.invalid_constant)
        kernel.finite_json(value)
        return value
    except (ValueError, UnicodeError, RecursionError):
        raise Invalid("invalid JSON bytes") from None


def encode_bytes(data):
    return base64.b64encode(data).decode("ascii")


def decode_bytes(value):
    try:
        require(isinstance(value, str), "expected base64 string")
        return base64.b64decode(value, validate=True)
    except (ValueError, TypeError):
        raise Invalid("invalid base64 bytes") from None


def fsync_dir(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def no_symlinks(path):
    path = Path(os.path.abspath(os.path.expanduser(str(path))))
    for part in (path, *path.parents):
        require(not part.is_symlink(), f"symlink path refused: {part}")
    return path


def private(path, directory=False):
    try:
        info = path.lstat()
    except OSError:
        raise Invalid(f"managed path unavailable: {path}") from None
    require(not stat.S_ISLNK(info.st_mode), f"symlink refused: {path}")
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode),
            f"wrong managed path type: {path}")
    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == (0o700 if directory else 0o600),
            f"insecure managed permissions/owner: {path}")
    require(directory or info.st_nlink == 1, f"linked managed file refused: {path}")


def directory(path, create=False):
    no_symlinks(path)
    if not path.exists() and create:
        require(path.parent.is_dir(), f"missing parent directory: {path.parent}")
        try:
            path.mkdir(mode=0o700)
            fsync_dir(path.parent)
        except FileExistsError:
            pass
    private(path, True)


def file_open(path, create=False):
    no_symlinks(path)
    existed = path.exists()
    if existed:
        private(path)
    try:
        descriptor = os.open(path, os.O_RDWR | os.O_NOFOLLOW | (os.O_CREAT if create else 0), 0o600)
    except OSError:
        raise Invalid(f"managed file unavailable: {path}") from None
    try:
        info = os.fstat(descriptor)
        require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1,
                f"insecure managed file: {path}")
        require(path.stat().st_ino == info.st_ino and path.stat().st_dev == info.st_dev,
                "managed file changed while opening")
        if not existed:
            os.fsync(descriptor)
            fsync_dir(path.parent)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def fields(value, required, optional=()):
    kernel.fields(value, required, optional)


def text(value):
    kernel.string(value, "value")


def identifier(value):
    require(isinstance(value, str) and ID.fullmatch(value), "invalid session/request ID")


def event_hash(event):
    return kernel.digest(kernel.canonical({key: value for key, value in event.items() if key != "event_id"}))


class Ledger:
    def __init__(self, path, root, project_key, engagement_key, caller_actor=None):
        self.actor = parse(kernel.canonical(caller_actor)) if caller_actor is not None else actor()
        validate_actor(self.actor)
        self.path, self.root = path, root
        self.project_key, self.engagement_key = project_key, engagement_key
        self.events, self.tail = [], None
        self.fd = None

    def replay(self):
        os.lseek(self.fd, 0, os.SEEK_SET)
        data = bytearray()
        while len(data) <= MAX_LEDGER:
            chunk = os.read(self.fd, min(65536, MAX_LEDGER + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        require(len(data) <= MAX_LEDGER, "ledger exceeds size bound")
        self.raw = bytes(data)
        self.events, self.tail = [], None
        parts = self.raw.split(b"\n")
        lines = [part + b"\n" for part in parts[:-1]] + ([parts[-1]] if parts[-1] else [])
        offset, index = 0, 0
        while index < len(lines):
            line = lines[index]
            # LF alone is the record delimiter; JSON strings must escape all newlines.
            if not line.endswith(b"\n"):
                self.tail = {"offset": offset, "length": len(line), "sha256": kernel.digest(line),
                             "kind": "missing_lf" if self._valid_unterminated(line) else "malformed"}
                break
            try:
                event = parse(line[:-1])
            except Invalid:
                if index + 1 == len(lines):
                    self.tail = {"offset": offset, "length": len(line), "sha256": kernel.digest(line),
                                 "kind": "malformed"}
                    break
                require(lines[index + 1].endswith(b"\n"), "interrupted recovery: operator investigation required")
                recovery = parse(lines[index + 1][:-1])
                require(lines[index + 1] == kernel.canonical(recovery) + b"\n", "noncanonical recovery")
                require(isinstance(recovery, dict) and recovery.get("kind") == "recovery", "middle ledger corruption")
                self.validate_event(recovery)
                proof = recovery["data"]
                count = proof["length"]
                require(proof["offset"] == offset and count in (len(line), len(line) - 1),
                        "recovery fragment location mismatch")
                require(kernel.digest(line[:count]) == proof["sha256"]
                        and line[count:] in (b"", b"\n"), "recovery fragment hash mismatch")
                self.events.append(recovery)
                offset += len(line) + len(lines[index + 1])
                index += 2
                continue
            self.validate_event(event)
            require(event["kind"] != "recovery", "orphan recovery event")
            require(line == kernel.canonical(event) + b"\n", "noncanonical ledger event")
            self.events.append(event)
            offset += len(line)
            index += 1
        return self

    def _valid_unterminated(self, line):
        try:
            event = parse(line)
        except Invalid:
            return False
        # Valid JSON with invalid hash/semantics is corruption, never a recoverable fragment.
        self.validate_event(event)
        require(event["kind"] != "recovery", "orphan recovery event")
        require(line == kernel.canonical(event), "noncanonical final event")
        return True

    @property
    def session_id(self):
        return self.events[0]["session_id"] if self.events else None

    def by_id(self, event_id, kind=None):
        found = next((event for event in self.events if event["event_id"] == event_id), None)
        require(found is not None and (kind is None or found["kind"] == kind), "unknown event reference")
        return found

    def request(self, request_id):
        identifier(request_id)
        found = next((event for event in self.events if event["kind"] == "prepare"
                      and event["request_id"] == request_id), None)
        require(found is not None, "unknown request")
        return found

    def related(self, request_id, kind):
        return [event for event in self.events if event["request_id"] == request_id and event["kind"] == kind]

    def lineage(self, value):
        fields(value, ("branch", "step", "parent_request_ids"), ("reconsider_of", "retry_of", "reason"))
        text(value["branch"])
        text(value["step"])
        kernel.strings(value["parent_request_ids"], "lineage.parents", unique=True)
        for request_id in value["parent_request_ids"]:
            self.request(request_id)
        for name in ("retry_of", "reconsider_of"):
            if name in value:
                self.request(value[name])
                text(value.get("reason"))
        if "reason" in value:
            text(value["reason"])

    def selection(self, value):
        fields(value, ("policy", "items"), ("labels", "layers"))
        fields(value["policy"], ("id", "version"))
        text(value["policy"]["id"])
        text(value["policy"]["version"])
        require(isinstance(value["items"], list) and value["items"], "selection.items must be nonempty")
        for item in value["items"]:
            fields(item, ("event_id", "excerpt"), ("labels", "layers"))
            source = self.by_id(item["event_id"])
            text(item["excerpt"])
            require(item["excerpt"] in kernel.canonical(source).decode(), "excerpt absent from canonical source")

    def validate_event(self, event):
        fields(event, ("schema", "event_id", "sequence", "at", "session_id", "channel", "request_id",
                       "kind", "actor", "data", "previous_event_id"))
        require(event["schema"] == "jev.event/v1" and isinstance(event["kind"], str) and event["kind"] in KINDS, "unknown event schema/kind")
        require(event["event_id"] == event_hash(event), "event hash mismatch")
        require(type(event["sequence"]) is int and event["sequence"] == len(self.events) + 1,
                "event sequence mismatch")
        require(event["previous_event_id"] == (self.events[-1]["event_id"] if self.events else None),
                "event predecessor mismatch")
        identifier(event["session_id"])
        require(event["channel"] == "main", "unsupported channel")
        validate_actor(event["actor"])
        text(event["at"])
        try:
            require(datetime.fromisoformat(event["at"]).tzinfo is not None, "timestamp requires zone")
        except ValueError:
            raise Invalid("invalid timestamp") from None
        kind, body, request_id = event["kind"], event["data"], event["request_id"]
        require(isinstance(body, dict), "event data must be object")
        require(body.get("certainty") == CERTAINTY.get(kind, "confirmed"), "event claim certainty mismatch")
        body = {key: value for key, value in body.items() if key != "certainty"}
        if not self.events:
            require(kind == "open" and request_id is None, "ledger must begin with opening")
            fields(body, ("root", "project", "bed", "policy"))
            require(body["root"] == str(self.root), "runtime root identity mismatch")
            text(body["project"])
            text(body["bed"])
            require(kernel.digest(body["project"].encode()) == self.project_key
                    and kernel.digest(body["bed"].encode()) == self.engagement_key, "engagement identity mismatch")
            project, bed = Path(body["project"]), Path(body["bed"])
            require(project.is_absolute() and bed.is_relative_to(project), "invalid project/bed identity")
            policy = body["policy"]
            fields(policy, ("budget_usd", "model", "allowed_models"))
            if policy["model"] is not None:
                text(policy["model"])
            if policy["budget_usd"] is not None:
                money(policy["budget_usd"])
            require(isinstance(policy["allowed_models"], list), "models must be list")
            kernel.strings(policy["allowed_models"], "models", unique=True)
            require((policy["model"] is None and not policy["allowed_models"])
                    or policy["model"] in policy["allowed_models"], "invalid model policy")
            return
        require(event["session_id"] == self.session_id and kind != "open", "session/open mismatch")
        if kind in {"memory", "select", "recovery"}:
            require(request_id is None, "nonrequest event has request ID")
        else:
            identifier(request_id)
            if kind != "prepare":
                self.request(request_id)
        if kind == "prepare":
            fields(body, ("prepared", "source", "lineage", "memory_event_id", "selection_event_id",
                          "provider", "upper_bound_usd", "bound_evidence"))
            require(not self.related(request_id, "prepare"), "duplicate preparation")
            prepared = body["prepared"]
            kernel.validate_prepared(prepared)
            require(prepared["request_id"] == request_id and prepared["packet"]["session_id"] == self.session_id
                    and prepared["packet"]["channel"] == "main", "prepared binding mismatch")
            fields(body["source"], ("path", "sha256"))
            text(body["source"]["path"])
            require(isinstance(body["source"]["sha256"], str) and HASH.fullmatch(body["source"]["sha256"]),
                    "invalid source hash")
            if body["lineage"] is not None:
                self.lineage(body["lineage"])
            if body["memory_event_id"] is not None:
                note = self.by_id(body["memory_event_id"], "memory")["data"]["note"]
                require(prepared["packet"].get("memory") == note, "frozen memory mismatch")
            if body["selection_event_id"] is not None:
                selection = self.by_id(body["selection_event_id"], "select")["data"]["selection"]
                expected = {"event_id": body["selection_event_id"], "manifest": selection,
                            "source_events": [self.by_id(item["event_id"]) for item in selection["items"]]}
                require(prepared["packet"]["state"].get("jev_selection") == expected, "frozen selection mismatch")
            if body["upper_bound_usd"] is not None:
                money(body["upper_bound_usd"])
                text(body["bound_evidence"])
            else:
                require(body["bound_evidence"] is None, "bound evidence without bound")
            frozen = body["provider"]
            if frozen is not None:
                fields(frozen, ("method", "endpoint", "headers", "model", "adapter_version", "body_base64", "sha256"))
                require(frozen["method"] == "POST" and frozen["endpoint"] == "https://openrouter.ai/api/alpha/decisions",
                        "invalid provider destination")
                require(frozen["model"] == self.events[0]["data"]["policy"]["model"], "provider model mismatch")
                text(frozen["adapter_version"])
                require(frozen["headers"] == {"Content-Type": "application/json", "Accept": "application/json"},
                        "unexpected provider headers")
                raw = decode_bytes(frozen["body_base64"])
                require(len(raw) <= kernel.MAX_BYTES and kernel.digest(raw) == frozen["sha256"], "provider body hash mismatch")
                import provider
                require(frozen["adapter_version"] == provider.ADAPTER_VERSION,
                        "unsupported frozen provider adapter version")
                require(raw == provider.build_request(prepared["packet"], frozen["model"]),
                        "frozen provider body differs from prepared packet")
            else:
                require(self.events[0]["data"]["policy"]["model"] is None, "missing frozen provider")
        elif kind == "memory":
            fields(body, ("note",))
            fields(body["note"], ("version", "author", "text", "refs"))
            for name in ("version", "author", "text"):
                text(body["note"][name])
            kernel.strings(body["note"]["refs"], "memory.refs", unique=True)
            for reference in body["note"]["refs"]:
                self.by_id(reference)
        elif kind == "select":
            fields(body, ("selection",))
            self.selection(body["selection"])
        elif kind == "reply":
            fields(body, ("source", "raw_base64", "raw_sha256", "receipt", "validation", "http_event_id"))
            require(not self.related(request_id, "reply"), "duplicate terminal receipt")
            raw = decode_bytes(body["raw_base64"])
            require(len(raw) <= kernel.MAX_BYTES and kernel.digest(raw) == body["raw_sha256"], "reply bytes mismatch")
            require(isinstance(body["source"], str) and body["source"] in {"synthetic", "provider"}, "unknown reply source")
            validation = body["validation"]
            fields(validation, ("status", "errors"))
            require(isinstance(validation["status"], str) and validation["status"] in {"VALID", "INVALID"}, "invalid reply validation status")
            kernel.strings(validation["errors"], "validation.errors")
            if body["source"] == "synthetic":
                require(not self.related(request_id, "attempt") and body["http_event_id"] is None,
                        "synthetic reply cannot settle attempt")
                try:
                    expected_receipt = parse(raw)
                    checked = kernel.check(self.request(request_id)["data"]["prepared"], expected_receipt)
                    expected_validation = {key: checked[key] for key in ("status", "errors")}
                except Invalid as error:
                    expected_receipt, expected_validation = None, {"status": "INVALID", "errors": [str(error)]}
                require(body["receipt"] == expected_receipt and validation == expected_validation,
                        "synthetic receipt/validation differs from raw")
            else:
                http = self.by_id(body["http_event_id"], "http")
                require(http["request_id"] == request_id and http["data"]["raw_base64"] == body["raw_base64"],
                        "provider reply HTTP reference mismatch")
                import provider
                parsed = provider.parse_response(self.request(request_id)["data"]["prepared"], raw,
                                                 self.events[0]["data"]["policy"]["allowed_models"])
                require(body["receipt"] == parsed["receipt"] and validation == parsed["validation"],
                        "provider receipt/validation differs from raw")
                if validation["status"] == "VALID":
                    kernel.validate_receipt(self.request(request_id)["data"]["prepared"], body["receipt"])
                    require(body["receipt"]["model"] in self.events[0]["data"]["policy"]["allowed_models"],
                            "reply model outside policy")
        elif kind == "interpret":
            fields(body, ("question_id", "policy", "receipt_event_id", "result"))
            text(body["question_id"])
            receipt = self.by_id(body["receipt_event_id"], "reply") if body["receipt_event_id"] else None
            require(receipt is None or receipt["request_id"] == request_id, "interpret receipt mismatch")
            try:
                if isinstance(body["policy"], dict) and "input_error" in body["policy"]:
                    fields(body["policy"], ("input_error", "path"))
                    text(body["policy"]["input_error"])
                    text(body["policy"]["path"])
                    raise Invalid(body["policy"]["input_error"])
                require(receipt is not None, "no receipt")
                require(receipt["data"]["validation"]["status"] == "VALID", "receipt is invalid")
                expected = kernel.interpret(self.request(request_id)["data"]["prepared"], receipt["data"]["receipt"],
                                            body["question_id"], body["policy"])
            except Invalid as error:
                expected = {"status": "ERROR", "errors": [str(error)], "request_id": request_id,
                            "question_id": body["question_id"], "policy": body["policy"]}
            require(body["result"] == expected, "interpretation result mismatch")
        elif kind == "dispose":
            fields(body, ("decision", "consumer", "reason"))
            require(isinstance(body["decision"], str) and body["decision"] in {"use", "skip", "reconsider"}, "unknown disposition")
            text(body["consumer"])
            kernel.string(body["reason"], "reason", empty=True)
        elif kind == "outcome":
            fields(body, ("observation", "request_event_id"))
            require(isinstance(body["observation"], dict), "outcome must be object")
            require(body["request_event_id"] == self.request(request_id)["event_id"], "outcome request mismatch")
            kernel.strings(body["observation"].get("refs", []), "outcome.refs", unique=True)
            for reference in body["observation"].get("refs", []):
                self.by_id(reference)
        elif kind == "attempt":
            fields(body, ("upper_bound_usd", "approval_sha256", "prepared_event_id"), ("authorization",))
            require(not self.related(request_id, "attempt") and not self.related(request_id, "reply"),
                    "request already attempted/completed")
            prepared = self.request(request_id)
            require(body["prepared_event_id"] == prepared["event_id"] and prepared["data"]["provider"] is not None,
                    "attempt prepared reference mismatch")
            require(body["upper_bound_usd"] == prepared["data"]["upper_bound_usd"], "attempt bound mismatch")
            money(body["upper_bound_usd"])
            require(isinstance(body["approval_sha256"], str) and HASH.fullmatch(body["approval_sha256"]), "invalid approval hash")
            self.admit(body["upper_bound_usd"])
            require(body["approval_sha256"] == self.approval(request_id)[1], "approval hash mismatch")
            if "authorization" in body:
                proof = body["authorization"]
                fields(proof, ("grant", "grant_sha256"))
                require(proof["grant_sha256"] == kernel.digest(kernel.canonical(proof["grant"])),
                        "authorization grant hash mismatch")
                self.validate_send_grant(request_id, proof["grant"], datetime.fromisoformat(event["at"]))
        elif kind == "http":
            fields(body, ("attempt_event_id", "status", "raw_base64", "raw_sha256"))
            attempt = self.by_id(body["attempt_event_id"], "attempt")
            require(attempt["request_id"] == request_id and not self.related(request_id, "http")
                    and not self.related(request_id, "uncertain"), "HTTP transition mismatch")
            require(type(body["status"]) is int and 100 <= body["status"] <= 599, "invalid HTTP status")
            raw = decode_bytes(body["raw_base64"])
            require(len(raw) <= kernel.MAX_BYTES and kernel.digest(raw) == body["raw_sha256"], "HTTP bytes mismatch")
        elif kind == "settle":
            fields(body, ("attempt_event_id", "http_event_id", "cost_usd", "provider_id", "model"))
            attempt, http = self.by_id(body["attempt_event_id"], "attempt"), self.by_id(body["http_event_id"], "http")
            require(attempt["request_id"] == request_id == http["request_id"]
                    and 200 <= http["data"]["status"] < 300 and self.related(request_id, "reply")
                    and not self.related(request_id, "settle") and not self.related(request_id, "uncertain"),
                    "settlement transition mismatch")
            money(body["cost_usd"])
            import provider
            parsed = provider.parse_response(self.request(request_id)["data"]["prepared"],
                                             decode_bytes(http["data"]["raw_base64"]),
                                             self.events[0]["data"]["policy"]["allowed_models"])
            require(trusted_cost(parsed["cost_usd"]) == body["cost_usd"]
                    and parsed["provider_id"] == body["provider_id"] and parsed["model"] == body["model"],
                    "settlement differs from billed response")
            for name in ("provider_id", "model"):
                require(body[name] is None or isinstance(body[name], str), "invalid provider metadata")
        elif kind == "uncertain":
            fields(body, ("attempt_event_id", "reason"))
            require(self.by_id(body["attempt_event_id"], "attempt")["request_id"] == request_id
                    and not self.related(request_id, "settle") and not self.related(request_id, "uncertain"),
                    "uncertain transition mismatch")
            require(isinstance(body["reason"], str) and body["reason"] in {"transport", "unknown_cost", "http_status", "parse"},
                    "invalid uncertainty reason")
            http_events = self.related(request_id, "http")
            require((body["reason"] == "transport" and not http_events)
                    or (body["reason"] != "transport" and http_events), "uncertainty transition mismatch")
            if body["reason"] in {"unknown_cost", "http_status"}:
                require(self.related(request_id, "reply"), "cost uncertainty requires retained reply")
                http = http_events[0]
                successful = 200 <= http["data"]["status"] < 300
                require((body["reason"] == "unknown_cost") == successful, "uncertainty HTTP status mismatch")
                if successful:
                    import provider
                    parsed = provider.parse_response(self.request(request_id)["data"]["prepared"],
                                                     decode_bytes(http["data"]["raw_base64"]),
                                                     self.events[0]["data"]["policy"]["allowed_models"])
                    require(trusted_cost(parsed["cost_usd"]) is None, "known billed cost cannot be made unknown")
        elif kind == "recovery":
            fields(body, ("offset", "length", "sha256", "prefix_event_id", "prefix_sequence"))
            require(type(body["offset"]) is int and body["offset"] >= 0
                    and type(body["length"]) is int and body["length"] > 0
                    and isinstance(body["sha256"], str) and HASH.fullmatch(body["sha256"]), "invalid recovery fragment")
            require(body["prefix_event_id"] == self.events[-1]["event_id"]
                    and type(body["prefix_sequence"]) is int and body["prefix_sequence"] == len(self.events), "recovery prefix mismatch")

    def append(self, kind, body, request_id=None, session_id=None, *, _recovering=False):
        require(kind != "recovery" or _recovering, "recovery requires explicit reconcile")
        if not _recovering:
            self.replay()
        require(self.tail is None, "incomplete tail: explicit reconcile required")
        event = {"schema": "jev.event/v1", "event_id": None, "sequence": len(self.events) + 1,
                 "at": datetime.now(timezone.utc).isoformat(), "session_id": session_id or self.session_id,
                 "channel": "main", "request_id": request_id, "kind": kind, "actor": self.actor,
                 "data": {"certainty": CERTAINTY.get(kind, "confirmed"), **body}, "previous_event_id": self.events[-1]["event_id"] if self.events else None}
        event = parse(kernel.canonical(event))
        event["event_id"] = event_hash(event)
        self.validate_event(event)
        encoded = kernel.canonical(event) + b"\n"
        require(len(encoded) <= MAX_EVENT and len(self.raw) + len(encoded) <= MAX_LEDGER, "ledger/event size bound")
        os.lseek(self.fd, 0, os.SEEK_END)
        self._write(encoded)
        self.raw += encoded
        self.events.append(event)
        return parse(kernel.canonical(event))

    def _write(self, data):
        view = memoryview(data)
        while view:
            count = os.write(self.fd, view)
            require(count > 0, "ledger write failed")
            view = view[count:]
        os.fsync(self.fd)

    def budget(self):
        policy = self.events[0]["data"]["policy"]
        settlements = {event["request_id"]: event for event in self.events if event["kind"] == "settle"}
        attempts = [event for event in self.events if event["kind"] == "attempt"]
        spent = total(money(event["data"]["cost_usd"]) for event in settlements.values())
        outstanding = [event for event in attempts if event["request_id"] not in settlements]
        reserved = total(money(event["data"]["upper_bound_usd"]) for event in outstanding)
        total_usd = money(policy["budget_usd"]) if policy["budget_usd"] is not None else None
        liabilities = [{"request_id": event["request_id"], "attempt_event_id": event["event_id"],
                        "upper_bound_usd": event["data"]["upper_bound_usd"], "status": "UNKNOWN"}
                       for event in outstanding]
        liabilities.extend({"request_id": None, "recovery_event_id": event["event_id"],
                            "upper_bound_usd": None, "status": "UNKNOWN_FRAGMENT"}
                           for event in self.events if event["kind"] == "recovery")
        overrun = [event["request_id"] for event in settlements.values()
                   if money(event["data"]["cost_usd"]) > money(self.related(event["request_id"], "attempt")[0]["data"]["upper_bound_usd"])]
        return {"total_usd": policy["budget_usd"], "spent_usd": decimal_text(spent),
                "reserved_usd": decimal_text(reserved),
                "available_usd": decimal_text(total([total_usd, spent.copy_negate(), reserved.copy_negate()])) if total_usd is not None else None,
                "liabilities": liabilities, "overrun_request_ids": overrun}

    def admit(self, upper_bound):
        bound, budget = money(upper_bound), self.budget()
        require(budget["total_usd"] is not None, "budget is UNSET")
        require(not budget["liabilities"] and not budget["overrun_request_ids"], "unresolved liability or overrun blocks sends")
        require(total([money(budget["spent_usd"]), money(budget["reserved_usd"]), bound]) <= money(budget["total_usd"]),
                "budget upper bound exceeds allowance")

    def approval(self, request_id):
        event = self.request(request_id)
        data = event["data"]
        frozen = data["provider"]
        require(frozen is not None, "request has no frozen provider body")
        require(data["upper_bound_usd"] is not None, "request has no declared upper bound")
        self.admit(data["upper_bound_usd"])
        require(not self.related(request_id, "attempt") and not self.related(request_id, "reply"),
                "request already attempted/completed; prepare a new occurrence with lineage")
        body = decode_bytes(frozen["body_base64"])
        value = {"session_id": self.session_id, "channel": "main", "request_id": request_id,
                 "prepared_event_id": event["event_id"], "provider": frozen,
                 "body_utf8": body.decode("utf-8"), "model_policy": self.events[0]["data"]["policy"],
                 "budget": self.budget(), "upper_bound_usd": data["upper_bound_usd"],
                 "bound_evidence": data["bound_evidence"]}
        return value, kernel.digest(kernel.canonical(value))

    def validate_send_grant(self, request_id, grant, at):
        fields(grant, ("schema", "root", "session_id", "request_id", "approval_sha256", "max_cost_usd",
                       "credential_env", "authorized_by", "authorization_ref", "expires_at"))
        require(grant["schema"] == "jev.send-grant/v1", "unsupported send grant schema")
        require(grant["root"] == str(self.root) and grant["session_id"] == self.session_id
                and grant["request_id"] == request_id, "send grant scope mismatch")
        require(grant["credential_env"] == "JEV_ORAK_KEY" and grant["authorized_by"] == "hlm",
                "send grant credential/authority mismatch")
        reference = grant["authorization_ref"]
        require(isinstance(reference, str) and 1 <= len(reference) <= 2048
                and all(0x20 <= ord(character) <= 0x7e for character in reference)
                and any(character != " " for character in reference), "invalid authorization reference")
        maximum = money(grant["max_cost_usd"])
        frozen_bound = self.request(request_id)["data"]["upper_bound_usd"]
        require(Decimal(0) < maximum <= Decimal("0.02") and maximum == money(frozen_bound),
                "send grant must match positive frozen bound at most 0.02 USD")
        allowance = self.events[0]["data"]["policy"]["budget_usd"]
        require(allowance is not None and money(allowance) <= Decimal("0.02"),
                "delegated engagement allowance exceeds 0.02 USD or is UNSET")
        require(grant["approval_sha256"] == self.approval(request_id)[1], "send grant approval mismatch")
        require(isinstance(grant["expires_at"], str), "send grant expiry must be ISO timestamp")
        try:
            expiry = datetime.fromisoformat(grant["expires_at"])
        except ValueError:
            raise Invalid("send grant expiry must be ISO timestamp") from None
        require(expiry.tzinfo is not None and expiry > at, "send grant expired or lacks timezone")

    def settings(self):
        opened = self.events[0]
        return {"session_id": self.session_id, "channel": "main", "root": str(self.root),
                "project": opened["data"]["project"], "bed": opened["data"]["bed"],
                "policy": opened["data"]["policy"], "budget": self.budget(), "tail": self.tail,
                "ledger": str(self.path)}

    def reconcile(self):
        if self.tail is None:
            return {"status": "CLEAN"}
        tail = dict(self.tail)
        require(self.events, "cannot recover missing opening event")
        os.lseek(self.fd, 0, os.SEEK_END)
        if tail["kind"] == "missing_lf":
            self._write(b"\n")
            self.replay()
            return {"status": "COMPLETED_LF", "tail": tail}
        # Original fragment remains byte-identical. The next event proves its extent.
        separator = b"" if self.raw.endswith(b"\n") else b"\n"
        if separator:
            self._write(separator)
            self.raw += separator
        self.tail = None
        event = self.append("recovery", {"offset": tail["offset"], "length": tail["length"],
                                       "sha256": tail["sha256"], "prefix_event_id": self.events[-1]["event_id"],
                                       "prefix_sequence": len(self.events)}, _recovering=True)
        self.replay()
        return {"status": "RECOVERED_FRAGMENT", "event": event}


class Vault:
    def __init__(self, root, *, cli_sessions=None, requester=None):
        self.actor = actor(cli_sessions, requester)
        self.root = no_symlinks(root)

    def _project(self, key, create=False):
        directory(self.root, create)
        directory(self.root / "projects", create)
        path = self.root / "projects" / key
        directory(path, create)
        return path

    @contextmanager
    def _locked(self, project_key, engagement_key, create=False, shared=False):
        project = self._project(project_key, create)
        lock = project / (engagement_key + ".lock")
        lock_fd = file_open(lock, create)
        ledger_fd = None
        try:
            deadline = time.monotonic() + 2
            while True:
                try:
                    fcntl.flock(lock_fd, (fcntl.LOCK_SH if shared else fcntl.LOCK_EX) | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    require(time.monotonic() < deadline, "session busy: retry the local command later")
                    time.sleep(0.01)
            ledger_fd = file_open(project / (engagement_key + ".jsonl"), create)
            ledger = Ledger(project / (engagement_key + ".jsonl"), self.root, project_key, engagement_key, self.actor)
            ledger.fd = ledger_fd
            ledger.replay()
            yield ledger
        finally:
            if ledger_fd is not None:
                os.close(ledger_fd)
            os.close(lock_fd)

    def open(self, project, bed, budget=None, model=None, allow_models=()):
        project, bed = no_symlinks(project), no_symlinks(bed)
        require(project.is_dir() and bed.is_dir() and bed.is_relative_to(project), "existing project/bed binding required")
        require(project.resolve() == project and bed.resolve() == bed, "canonical project/bed paths required")
        if budget is not None:
            money(budget)
        if model is not None:
            text(model)
        allowed = list(dict.fromkeys([model, *allow_models])) if model is not None else list(allow_models)
        kernel.strings(allowed, "allowed_models", unique=True)
        require(model is not None or not allowed, "allow-model requires model")
        policy = {"budget_usd": budget, "model": model, "allowed_models": allowed}
        project_key, engagement_key = kernel.digest(str(project).encode()), kernel.digest(str(bed).encode())
        with self._locked(project_key, engagement_key, create=True) as ledger:
            if not ledger.events:
                ledger.append("open", {"root": str(self.root), "project": str(project), "bed": str(bed),
                                       "policy": policy}, session_id=uuid.uuid4().hex)
            require(ledger.tail is None, "incomplete opening requires reconciliation")
            require(ledger.events[0]["data"] == {"root": str(self.root), "project": str(project), "bed": str(bed),
                                                "policy": policy, "certainty": "confirmed"}, "opening settings are immutable")
            return ledger.settings()

    def locate(self, session_id):
        identifier(session_id)
        directory(self.root)
        directory(self.root / "projects")
        found = []
        projects = list((self.root / "projects").iterdir())
        require(len(projects) <= 10000, "project lookup bound exceeded")
        for project in projects:
            require(HASH.fullmatch(project.name), "unknown managed project path")
            directory(project)
            paths = list(project.iterdir())
            require(len(paths) <= 20000, "session lookup bound exceeded")
            for path in paths:
                require(path.suffix in {".lock", ".jsonl"} and HASH.fullmatch(path.stem), "unknown managed session path")
                private(path)
                if path.suffix != ".jsonl":
                    continue
                with self._locked(project.name, path.stem, shared=True) as ledger:
                    if ledger.session_id == session_id:
                        found.append((project.name, path.stem))
        require(len(found) == 1, "session missing or duplicate/colliding IDs")
        return found[0]

    @contextmanager
    def selected(self, session_id, channel="main"):
        require(channel == "main", "only channel main is supported")
        keys = self.locate(session_id)
        with self._locked(*keys) as ledger:
            require(ledger.session_id == session_id, "session identity changed")
            yield ledger
