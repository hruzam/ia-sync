#!/usr/bin/env python3
"""tunnel-codex.py — JSON-RPC mechanics for the termbrana 03-tunnel v0 Codex shim.

SPEC (verbatim call sequence + curvature findings this file implements):
  ~/ia-sync/session/rellays-calude-codex/CARTAN-ORACULUM-tunnel-verdict.2026-09-02.md

PROTOCOL PIN: codex-cli 0.152.1-observed, protocol experimental — upgrade = tested
migration (curvature 3 in the verdict above; `codex app-server --help` still labels the
command [experimental] on this release). Method names, required fields, and the sandbox
enum below were cross-checked 2026-09-02 against a local, ZERO-QUOTA run of
`codex app-server generate-json-schema --experimental` on this exact binary (no live
model call — schema generation is a static introspection command). This is a live-schema
pin, not a copy of the docs prose, which curvature 1 in the verdict file shows is stale
for the sandbox enum (docs show legacy camelCase `workspaceWrite`; 0.152.1 only accepts
the CLI-form values baked into SANDBOX_VALUES below).

Transport: newline-delimited JSON-RPC 2.0 over the stdio of a freshly spawned
`codex app-server --stdio` process — one subprocess per verb invocation, no daemon
(RUNBOOK constraint). Confirmed by binary-string inspection of the 0.152.1 release:
"JSON-RPC message exceeds the limit of ... bytes" is a per-line reader cap; no
Content-Length/LSP-style framing strings are wired to the stdio transport (the
Content-Length hits in the binary belong to the unrelated bundled HTTP/2 client).

Sibling: tunnel-codex.zsh is the operator/agent entry — it owns the Law 2.4 enable gate,
the state-file existence check, verb/enum validation, and dispatches here for the actual
protocol mechanics. This file does not gate; it assumes the caller already decided the
verb is allowed to run.

EXIT CODES (must match tunnel-codex.zsh's contract exactly — see that file's header):
  0  ok
  11 usage error (bad args, unknown verb, invalid sandbox value, --cwd not a directory)
  61 turn-in-flight (BRICK-01: another send/ask/steer on this same vault is still
     running — <state>.lock is held by a live pid. Never two turns on one head. A lock
     whose pid is dead is stale residue and is removed automatically; it is OURS, unlike
     ~/.codex/thread-writer-locks/ which is Codex's and is never touched)
  20 spawn-fail (codex binary not found / app-server process would not start)
  30 protocol-error (JSON-RPC transport broke: bad JSON, EOF, timeout, error reply)
  40 turn-error (turn/start|steer returned an error, the turn ended non-"completed",
     or steer had no recorded turn id to target)
  50 reconcile-mismatch (thread/read(includeTurns=true) does not contain the turn we
     just drove, or disagrees with what turn/completed reported; `ask` also raises this
     when its streamed agent text and its thread/read read-back text disagree)
  12 no-thread (verb needs a live threadId — state["threadId"] is null because no
     'send' has run yet; thread birth happens on first send, not on open — see
     THREAD BIRTH note below)
  13 state-not-specified (no --state and no $TUNNEL_CODEX_STATE — enforced by the
     tunnel-codex.zsh gate before this script is even invoked; see that file's header,
     STATE PATH SELECTION. --state is `required=True` here as the second line of
     defense, but the zsh wrapper is the one that names both mechanisms and refuses
     cleanly with nothing created.)

THREAD BIRTH (fix, 2026-09-03, t3 FAIL evidence): on codex-cli 0.152.1, a zero-turn
`thread/start` allocates a thread id + writer-lock but writes NO rollout file — the
rollout is written on the first *turn*. Since every shim verb is its own
`codex app-server --stdio` subprocess, a stored threadId with no rollout fails every
later `thread/resume` with -32600 "no rollout found". `open --enable` therefore no
longer calls `thread/start` at all; it only preflights (initialize/account/model) and
persists `threadId: null`. The thread is born inside `send`'s own connection, in the
same process as the `turn/start` that immediately follows it (Cartan's proven
continuous sequence) — so a rollout always exists before any other verb can try to
resume it.

STDOUT PURITY (Sella L4 / one-return-channel law, added 2026-09-03): every narrative
print in this file (open's "enabled"/"resumed" lines, resume's liveness line) goes to
stderr. Only `send`/`ask`/`steer`'s driven agent-message text, `read`'s raw JSON, and
the trailing `[usage: {...}]` tail reach stdout. `close`/`status` are zsh-local (see
tunnel-codex.zsh) and follow the same rule there.

USAGE TAIL (added 2026-09-03): `turn/completed` itself carries no usage/token fields on
this pinned schema (cross-checked against a local, zero-quota
`codex app-server generate-json-schema --experimental` run, v2/TurnCompletedNotification
— `{threadId, turn}` only, and `Turn` has no usage field). The real token-usage carrier
is the sibling notification `thread/tokenUsage/updated`
(`{threadId, turnId, tokenUsage: {last, total, modelContextWindow}}`,
v2/ThreadTokenUsageUpdatedNotification) — previously dropped by drive_turn's "every
other notification ... is dropped" catch-all. `drive_turn` now records the latest one
seen for this thread before `turn/completed` fires and returns it; `send`/`ask`/`steer`
append it as the final stdout line via `_format_usage_tail`. If the app-server never
emits one for a turn, the tail is `[usage: unavailable]` and a stderr note names why —
never silently omitted (codex-run.zsh convention, same file family).

MODEL STAMP (fix, 2026-09-03): `open --enable`'s zero-turn preflight already called
`model/list` but discarded the result, so a caller who omitted `--model` got a state
file (and banner) stamped `model=None`. `model/list` returns `{data: [Model, ...]}`
where each `Model` carries `isDefault` (v2/ModelListResponse, v2/Model in the same
generated schema) — `open` now resolves the account default from that response
(falling back to `data[0]` if no entry is flagged default) whenever `--model` is not
given, and persists/prints the resolved id instead of `None`.
"""

import argparse
import datetime
import json
import os
import queue
import subprocess
import sys
import threading
import time

EXIT_OK = 0
EXIT_USAGE = 11
EXIT_SPAWN_FAIL = 20
EXIT_PROTOCOL_ERROR = 30
EXIT_TURN_ERROR = 40
EXIT_RECONCILE_MISMATCH = 50
EXIT_NO_THREAD = 12
# BRICK-01 (2026-10-03, Protocol 1 prep): one turn in flight per vault. send/ask/steer
# take <state>.lock (own pid) for the whole verb; a second caller on the same vault
# refuses with this code instead of racing a second turn onto the same head.
EXIT_TURN_IN_FLIGHT = 61
# Reserved, not raised from here: the zsh wrapper (tunnel-codex.zsh) refuses with this
# code BEFORE ever invoking this script if neither --state nor $TUNNEL_CODEX_STATE was
# given — see that file's STATE PATH SELECTION section. Kept here so the two exit-code
# tables never drift out of sync.
EXIT_STATE_NOT_SPECIFIED = 13

# CLI-form values only (curvature 1, verdict file) — camelCase docs-prose values are
# deliberately NOT accepted here; 0.152.1 rejects them at the app-server boundary.
SANDBOX_VALUES = ("read-only", "workspace-write", "danger-full-access")

CLIENT_INFO = {"name": "ia-sync-tunnel-codex", "version": "0.1.0"}
DEFAULT_TIMEOUT = float(os.environ.get("TUNNEL_CODEX_TIMEOUT", "120"))


class TunnelError(Exception):
    """Base for every error this script raises; carries its own exit code."""

    def __init__(self, exit_code, message):
        super().__init__(message)
        self.exit_code = exit_code


class UsageError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_USAGE, message)


class SpawnFailError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_SPAWN_FAIL, message)


class ProtocolError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_PROTOCOL_ERROR, message)


class TurnError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_TURN_ERROR, message)


class ReconcileMismatch(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_RECONCILE_MISMATCH, message)


class NoThreadError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_NO_THREAD, message)


class TurnInFlightError(TunnelError):
    def __init__(self, message):
        super().__init__(EXIT_TURN_IN_FLIGHT, message)


# --- BRICK-01 helpers -------------------------------------------------------------
# Per-vault turn lock (ours). Path = <state>.lock, content = our pid. Taken for the
# whole of send/ask/steer; refused (exit 61) while a LIVE pid holds it; a dead pid is
# stale residue from a killed driver and is cleared. O_EXCL makes acquisition atomic.

def _turn_lock_path(state_path):
    return state_path + ".lock"


def _pid_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _acquire_turn_lock(state_path):
    lock = _turn_lock_path(state_path)
    for _ in range(2):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                with open(lock, "r", encoding="utf-8") as f:
                    pid = int((f.read() or "0").strip() or "0")
            except (OSError, ValueError):
                pid = 0
            if pid and _pid_alive(pid):
                raise TurnInFlightError(
                    f"turn already in flight on this vault (pid {pid} holds {lock}); "
                    "never two turns on one head — wait for it, or `tun read` to reconcile"
                )
            # stale: holder is dead — clear and retry once
            try:
                os.unlink(lock)
            except FileNotFoundError:
                pass
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"{os.getpid()}\n")
        return lock
    raise TurnInFlightError(f"could not acquire {lock} after clearing a stale holder")


def _release_turn_lock(lock):
    try:
        os.unlink(lock)
    except FileNotFoundError:
        pass


# Codex-owned writer lock — READ-ONLY existence check, advisory only. Present means
# another client (typically an interactive `codex` TUI) MAY hold this thread; it may
# also be residue after a crash. We never block on it and never remove it (GUIDE
# §Limits, @Cartan 2026-09-03). The operator's discipline for a bound head is: the
# interactive session releases before the tunnel sends; `tun read` reconciles after.

def _codex_writer_lock_path(thread_id):
    home = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
    return os.path.join(home, "thread-writer-locks", f"{thread_id}.lock")


def _warn_if_writer_lock(thread_id):
    p = _codex_writer_lock_path(thread_id)
    if os.path.exists(p):
        print(
            f"tunnel-codex.py: NOTE — Codex writer-lock present for thread {thread_id} "
            f"({p}). Another client may hold this thread, or this is residue. Proceeding; "
            "the lock is Codex-owned and is never touched by this shim.",
            file=sys.stderr,
        )


# Persist what the SERVER reports about the thread after thread/start or thread/resume —
# the effective sandbox / effort / cwd / model and which instruction files it loaded.
# `tun status` otherwise only echoes our saved intent (Cartan audit 2026-10-03).

def _stamp_runtime(state, resp):
    rt = {}
    for key in ("sandbox", "reasoningEffort", "cwd", "model", "instructionSources", "approvalPolicy"):
        if key in resp:
            rt[key] = resp.get(key)
    if rt:
        rt["observedAt"] = now_iso()
        state["runtime"] = rt


class AppServerTransport:
    """One `codex app-server --stdio` subprocess, newline-delimited JSON-RPC 2.0."""

    def __init__(self, codex_bin=None, cwd=None):
        self.codex_bin = codex_bin or os.environ.get("TUNNEL_CODEX_BIN", "codex")
        # BRICK-01: spawn directory = the thread's workspace root for a NEW thread and
        # the directory Codex discovers AGENTS.md from. Previously inherited from
        # wherever the caller happened to be — which made head identity accidental.
        self.cwd = cwd
        self.proc = None
        self._next_id = 1
        self._out_q = queue.Queue()
        self._err_lines = []
        self._reader = None
        self._err_reader = None

    def start(self):
        try:
            self.proc = subprocess.Popen(
                [self.codex_bin, "app-server", "--stdio"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=self.cwd,
            )
        except (FileNotFoundError, PermissionError, OSError) as exc:
            raise SpawnFailError(
                f"could not spawn '{self.codex_bin} app-server --stdio': {exc}"
            ) from exc

        self._reader = threading.Thread(target=self._pump_stdout, daemon=True)
        self._reader.start()
        self._err_reader = threading.Thread(target=self._pump_stderr, daemon=True)
        self._err_reader.start()

        # Catch the "binary exists but exits immediately" spawn-fail shape too.
        time.sleep(0.05)
        if self.proc.poll() is not None and self.proc.returncode != 0:
            raise SpawnFailError(
                f"'{self.codex_bin} app-server --stdio' exited immediately "
                f"(code {self.proc.returncode}); stderr: {self._stderr_tail()}"
            )

    def _pump_stdout(self):
        try:
            for line in self.proc.stdout:
                line = line.strip()
                if line:
                    self._out_q.put(line)
        finally:
            self._out_q.put(None)  # EOF sentinel

    def _pump_stderr(self):
        for line in self.proc.stderr:
            self._err_lines.append(line.rstrip("\n"))

    def _stderr_tail(self, n=20):
        return "\n".join(self._err_lines[-n:])

    def _write(self, payload):
        try:
            self.proc.stdin.write(json.dumps(payload) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise ProtocolError(
                f"failed writing to app-server stdin: {exc}; "
                f"stderr tail: {self._stderr_tail()}"
            ) from exc

    def request(self, method, params):
        rid = self._next_id
        self._next_id += 1
        msg = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            msg["params"] = params
        self._write(msg)
        return rid

    def notify(self, method, params=None):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._write(msg)

    def respond_error(self, request_id, message, code=-32000):
        # Best-effort unblock for an unsolicited server->client request (see
        # Session._auto_decline). If this write itself fails we are already in a
        # protocol-error state elsewhere, so failures here are swallowed on purpose.
        try:
            self._write({"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}})
        except ProtocolError:
            pass

    def next_message(self, timeout):
        try:
            line = self._out_q.get(timeout=timeout)
        except queue.Empty:
            raise ProtocolError(
                f"timed out after {timeout}s waiting for app-server output; "
                f"stderr tail: {self._stderr_tail()}"
            )
        if line is None:
            raise ProtocolError(f"app-server closed stdout (EOF); stderr tail: {self._stderr_tail()}")
        try:
            return json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProtocolError(f"non-JSON line from app-server: {line!r} ({exc})") from exc

    def close(self):
        if self.proc is None:
            return
        try:
            if self.proc.stdin:
                self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


class Session:
    """Higher-level calls matching Cartan's proven sequence, one per transport."""

    def __init__(self, transport, timeout=DEFAULT_TIMEOUT):
        self.t = transport
        self.timeout = timeout

    def _await_response(self, request_id):
        deadline = time.time() + self.timeout
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise ProtocolError(f"timed out waiting for response id={request_id}")
            msg = self.t.next_message(remaining)
            if "id" in msg and msg.get("id") == request_id and ("result" in msg or "error" in msg):
                if "error" in msg:
                    raise ProtocolError(f"app-server returned a JSON-RPC error for id={request_id}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg and "id" in msg:
                # Unsolicited server->client request (e.g. an approval prompt). v0 runs
                # sandbox=<given>/approvalPolicy="never" (Cartan's proven config), so this
                # should be unreachable in practice; decline rather than hang forever.
                self._auto_decline(msg)
                continue
            # Notification unrelated to what we're waiting for (e.g. a stray
            # thread/tokenUsage/updated) — drop it and keep waiting.

    def _auto_decline(self, server_request):
        rid = server_request.get("id")
        if rid is not None:
            self.t.respond_error(rid, "tunnel-codex v0 has no interactive approval surface")

    def initialize(self):
        rid = self.t.request("initialize", {"clientInfo": CLIENT_INFO})
        result = self._await_response(rid)
        self.t.notify("initialized")
        return result

    def account_read(self):
        rid = self.t.request("account/read", {"refreshToken": False})
        return self._await_response(rid)

    def model_list(self):
        rid = self.t.request("model/list", {})
        return self._await_response(rid)

    def thread_start(self, model=None, sandbox="read-only", cwd=None):
        params = {"sandbox": sandbox, "approvalPolicy": "never"}
        if model:
            params["model"] = model
        if cwd:
            # BRICK-01: explicit workspace root on birth. NOT sent on thread/resume —
            # a bound/existing thread keeps the cwd it was born with.
            params["cwd"] = cwd
        rid = self.t.request("thread/start", params)
        return self._await_response(rid)

    def thread_resume(self, thread_id):
        rid = self.t.request("thread/resume", {"threadId": thread_id})
        return self._await_response(rid)

    def thread_read(self, thread_id, include_turns=True):
        rid = self.t.request("thread/read", {"threadId": thread_id, "includeTurns": include_turns})
        return self._await_response(rid)

    def drive_turn(self, thread_id, text, expected_turn_id=None, overrides=None):
        """turn/start (expected_turn_id is None) or turn/steer (expected_turn_id given
        — the ID of the turn this same shim already recorded), then consume streamed
        notifications until turn/completed for this thread. Returns
        (turn_id, completed_turn_dict, final_agent_text, token_usage_or_None).
        token_usage is the most recent `thread/tokenUsage/updated` notification body
        seen for this thread before turn/completed fired (turn/completed itself carries
        no usage fields on the pinned schema — see USAGE TAIL note in this file's
        header); None if the app-server never emitted one for this turn."""
        user_input = [{"type": "text", "text": text}]
        if expected_turn_id is None:
            params = {"threadId": thread_id, "input": user_input}
            if overrides:
                # TURN OVERRIDES (2026-10-09): open-time intent, sent on every turn/start.
                # Server semantics: "for this turn and subsequent turns" — they PERSIST in
                # the thread; clearing the vault field does not revert the thread.
                params.update(overrides)
                print(f"tunnel-codex.py: turn overrides {json.dumps(overrides, sort_keys=True)} sent", file=sys.stderr)
            rid = self.t.request("turn/start", params)
        else:
            rid = self.t.request(
                "turn/steer",
                {"threadId": thread_id, "expectedTurnId": expected_turn_id, "input": user_input},
            )
        start_result = self._await_response(rid)
        turn = start_result.get("turn", {})
        turn_id = turn.get("id")
        if not turn_id:
            raise TurnError(f"app-server did not return a turn id: {start_result}")

        agent_texts = []
        completed_turn = None
        token_usage = None
        deadline = time.time() + self.timeout

        while completed_turn is None:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise ProtocolError(f"timed out waiting for turn/completed on turn {turn_id}")
            msg = self.t.next_message(remaining)

            if "id" in msg and "method" in msg:
                self._auto_decline(msg)
                continue

            method = msg.get("method")
            params = msg.get("params", {}) or {}
            if method == "item/completed":
                item = params.get("item", {}) or {}
                if item.get("type") == "agentMessage" and "text" in item:
                    agent_texts.append(item["text"])
            elif method == "thread/tokenUsage/updated" and params.get("threadId") == thread_id:
                token_usage = params.get("tokenUsage")
            elif method == "turn/completed" and params.get("threadId") == thread_id:
                completed_turn = params.get("turn", {})
            # every other notification (turn/started, item/started, ...) is dropped —
            # v0 only needs the final read-back, not the live stream.

        if completed_turn.get("id") != turn_id:
            raise TurnError(f"turn/completed reported id={completed_turn.get('id')!r}, expected {turn_id!r}")
        if completed_turn.get("status") != "completed":
            raise TurnError(
                f"turn {turn_id} ended with status={completed_turn.get('status')!r}: "
                f"{completed_turn.get('error')}"
            )

        final_text = agent_texts[-1] if agent_texts else ""
        return turn_id, completed_turn, final_text, token_usage

    def reconcile(self, thread_id, turn_id):
        """thread/read(includeTurns=true) durable-reconciliation channel (verdict file)."""
        result = self.thread_read(thread_id, include_turns=True)
        thread = result.get("thread", {})
        turns = thread.get("turns", [])
        match = next((t for t in turns if t.get("id") == turn_id), None)
        if match is None:
            raise ReconcileMismatch(
                f"thread/read(includeTurns=true) for {thread_id} does not contain turn {turn_id}"
            )
        if match.get("status") != "completed":
            raise ReconcileMismatch(
                f"thread/read shows turn {turn_id} status={match.get('status')!r}, expected 'completed'"
            )
        return result


def _default_model_id(models_result):
    """Resolve the account default model id from a model/list result
    (`{data: [Model, ...]}`, each Model optionally carrying `isDefault`), falling back
    to the first listed model if none is flagged default. Returns None if data is
    empty/absent — callers still stamp state honestly rather than fabricate an id."""
    data = (models_result or {}).get("data") or []
    for model in data:
        if model.get("isDefault"):
            return model.get("id")
    return data[0].get("id") if data else None


def _extract_agent_text(read_result, turn_id):
    """Pull the last agentMessage item's text for turn_id out of a
    thread/read(includeTurns=true) result — the 'ask' verb's read-back side of its
    streamed-vs-read-back verification. Returns None if the turn isn't present (should
    not happen here: reconcile() already validated presence before this is called)."""
    thread = read_result.get("thread", {})
    turns = thread.get("turns", [])
    match = next((t for t in turns if t.get("id") == turn_id), None)
    if match is None:
        return None
    items = match.get("items", []) or []
    texts = [item.get("text", "") for item in items if item.get("type") == "agentMessage"]
    return texts[-1] if texts else ""


def _format_usage_tail(usage):
    """Render the final usage stdout line. BRICK-01b (2026-10-03): shape is chosen by
    $TUNNEL_CODEX_USAGE —
      compact (default)  [usage: ctx=<last.inputTokens>/<modelContextWindow> (<pct>%) out=<n>]
                         — the one number that matters (occupancy = last.input / window),
                         never `total` (cumulative billing, the trap that rotates threads early)
      full               [usage: {...}] — the raw thread/tokenUsage/updated payload (pre-brick shape)
      off                no tail line at all (returns None; callers skip the print)
    Never silent on absence in compact/full: a stderr note explains, then
    '[usage: unavailable]'."""
    mode = (os.environ.get("TUNNEL_CODEX_USAGE") or "compact").strip().lower()
    if mode == "off":
        return None
    if not usage:
        print(
            "tunnel-codex.py: no thread/tokenUsage/updated notification observed for this "
            "turn before turn/completed — usage unavailable",
            file=sys.stderr,
        )
        return "[usage: unavailable]"
    if mode == "full":
        return "[usage: " + json.dumps(usage, separators=(",", ":"), ensure_ascii=False) + "]"
    last = usage.get("last") or {}
    win = usage.get("modelContextWindow")
    inp = last.get("inputTokens")
    out = last.get("outputTokens")
    pct = f"{100.0 * inp / win:.1f}%" if isinstance(inp, (int, float)) and win else "?"
    return f"[usage: ctx={inp}/{win} ({pct}) out={out}]"


def load_state(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(path, state):
    # Audited 2026-09-03 (Cartan safe-order fix): `path` here is always the caller's
    # explicitly provided --state/TUNNEL_CODEX_STATE value — argparse requires --state
    # on every verb and the zsh wrapper refuses (exit 13) before ever invoking this
    # script if neither --state nor $TUNNEL_CODEX_STATE was given. This makedirs may
    # therefore only ever create the parent of a path the caller named on purpose; it
    # must never run against a hardcoded/default path.
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_open(args):
    if args.sandbox not in SANDBOX_VALUES:
        raise UsageError(f"--sandbox must be one of {SANDBOX_VALUES}, got {args.sandbox!r}")

    # BRICK-01: --cwd must be an existing directory; it is stored and used as the
    # app-server spawn dir on every verb and as thread/start.cwd on birth.
    cwd = None
    if getattr(args, "cwd", None):
        cwd = os.path.abspath(os.path.expanduser(args.cwd))
        if not os.path.isdir(cwd):
            raise UsageError(f"--cwd is not a directory: {cwd}")

    preamble = _resolve_preamble_arg(getattr(args, "preamble", None))
    ov_merge, ov_clear = _parse_overrides(getattr(args, "override", None))

    state = load_state(args.state)

    if state is not None and (ov_merge is not None):
        _apply_overrides(state, ov_merge, ov_clear)
        save_state(args.state, state)

    if state is not None and preamble is not None:
        # Existing vault: record/clear the preamble (local only; the thread is untouched).
        if preamble == "none":
            state.pop("preamble", None)
            print("open: preamble cleared", file=sys.stderr)
        else:
            state["preamble"] = preamble
            print(f"open: preamble set to {preamble}", file=sys.stderr)
        save_state(args.state, state)

    if state is not None and getattr(args, "thread", None):
        # BRICK-01 guard: a vault already addressing a thread never silently re-targets.
        # Binding is a birth-time declaration; to point this handle elsewhere, `close`
        # it first (the orphan-guard prints the old thread's re-bind command).
        raise UsageError(
            f"vault already holds thread {state.get('threadId')} — `--thread` is only valid "
            "when creating a vault; run 'close' first to release it"
        )

    if state is None:
        # Zero-turn preflight only — deliberately NO thread/start (see THREAD BIRTH
        # note above the exit-code table). This spawns app-server, confirms the
        # handshake + account/model surface work, then persists threadId: null —
        # or, with --thread (BRICK-01 bind), the operator-named EXISTING threadId.
        transport = AppServerTransport(cwd=cwd)
        transport.start()
        try:
            session = Session(transport)
            session.initialize()
            session.account_read()
            models = session.model_list()
        finally:
            transport.close()
        # Model stamp fix (2026-09-03): resolve the account default from model/list
        # instead of discarding it — args.model still wins when the caller passed one.
        resolved_model = args.model or _default_model_id(models)
        state = {
            "enabled": True,
            "threadId": None,
            "lastTurnId": None,
            "model": resolved_model,
            "sandbox": args.sandbox,
            "created": now_iso(),
        }
        if cwd:
            state["cwd"] = cwd
        if preamble and preamble != "none":
            state["preamble"] = preamble
        if ov_merge is not None:
            _apply_overrides(state, ov_merge, ov_clear)
        bound = getattr(args, "thread", None)
        if bound:
            # BIND — reading (C) of the Protocol 1 handoff: the head is an existing
            # stored thread (e.g. an interactive cSharp session). No thread/resume here:
            # binding is a local declaration, and a resume while the interactive client
            # still holds the thread would race its writer-lock. The liveness probe is
            # the operator's explicit `tun resume` AFTER that client has released.
            state["threadId"] = bound
            state["bound"] = True
            state["boundAt"] = now_iso()
            _warn_if_writer_lock(bound)
        save_state(args.state, state)
        if bound:
            print(
                f"open: enabled and BOUND to existing thread {bound} "
                f"(model={state['model']}, sandbox intent={state['sandbox']}"
                f"{', cwd=' + cwd if cwd else ''}); first send/resume will thread/resume it — "
                "ensure any interactive client has released it first",
                file=sys.stderr,
            )
        else:
            print(
                f"open: enabled (model={state['model']}, sandbox={state['sandbox']}"
                f"{', cwd=' + cwd if cwd else ''}); "
                "no thread yet — thread will be born on first send",
                file=sys.stderr,
            )
        return

    if cwd and state.get("cwd") != cwd:
        # Re-open with a different --cwd on an existing vault: record it (used as spawn
        # dir); a born thread's own cwd is not changed by this.
        state["cwd"] = cwd
        save_state(args.state, state)
        print(f"open: cwd updated to {cwd} (spawn dir; a born thread keeps its own cwd)", file=sys.stderr)

    if state.get("threadId") is None:
        print(
            "open: already enabled; no thread yet — thread will be born on first send",
            file=sys.stderr,
        )
        return

    # An existing, already-born thread: liveness-probe it (unchanged behavior) and
    # BRICK-01: persist the server-reported runtime policy from the resume response.
    _warn_if_writer_lock(state["threadId"])
    transport = AppServerTransport(cwd=state.get("cwd"))
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        resumed = session.thread_resume(state["threadId"])
        thread = resumed.get("thread", {})
        print(
            f"open: resumed existing thread {state['threadId']} (status={thread.get('status')})",
            file=sys.stderr,
        )
    finally:
        transport.close()
    _stamp_runtime(state, resumed)
    save_state(args.state, state)


# PREAMBLE (2026-10-08, field finding nablarva-X1 T13): a vault may name a preamble file at
# open time (law 2.4: intent is an open-time act). Its text is prepended to every
# send/ask/steer, so a standing turn rule ("you are oriented; read only what is named")
# cannot be forgotten per message. Measured cause it answers: a bound head re-read its whole
# read order on many tunnel turns (30-42 kB per batch). Missing file at turn time = loud
# refusal before any spawn (exit 11), never a silent drop.

def _resolve_preamble_arg(value):
    if value is None:
        return None
    if value == "none":
        return "none"
    path = os.path.abspath(os.path.expanduser(value))
    if not os.path.isfile(path):
        raise UsageError(f"--preamble is not a readable file: {path}")
    return path


def _apply_preamble(state, text):
    path = state.get("preamble")
    if not path:
        return text
    try:
        with open(path, "r", encoding="utf-8") as f:
            pre = f.read().strip()
    except OSError as exc:
        raise UsageError(
            f"vault preamble {path} unreadable ({exc}) — no turn sent; fix the file or "
            "`open --preamble none` to clear it"
        ) from exc
    if not pre:
        return text
    print(f"tunnel-codex.py: preamble {path} ({len(pre)} chars) prepended", file=sys.stderr)
    return f"{pre}\n\n---\n\n{text}"


OVERRIDE_KEYS = ("model", "effort", "approvalPolicy", "approvalsReviewer", "summary")


def _parse_overrides(items):
    """--override key=value (repeatable) → (dict_to_merge, clear_all). Empty value
    (key=) removes that key; the single word 'none' clears every override. Keys are
    the turn/start override fields of the 0.162 schema (TurnStartParams)."""
    if not items:
        return None, False
    merge, clear = {}, False
    for it in items:
        if it == "none":
            clear = True
            continue
        if "=" not in it:
            raise UsageError(f"--override expects key=value or 'none', got {it!r}")
        k, v = it.split("=", 1)
        if k not in OVERRIDE_KEYS:
            raise UsageError(f"--override key must be one of {OVERRIDE_KEYS}, got {k!r}")
        merge[k] = v
    return merge, clear


def _apply_overrides(state, merge, clear):
    cur = {} if clear else dict(state.get("turnOverrides") or {})
    for k, v in (merge or {}).items():
        if v == "":
            cur.pop(k, None)
        else:
            cur[k] = v
    if cur:
        state["turnOverrides"] = cur
    else:
        state.pop("turnOverrides", None)
    print(f"open: turn overrides now {json.dumps(cur, sort_keys=True) if cur else 'none'}"
          " (sent on every send/ask; they persist in the thread once sent)", file=sys.stderr)


def _require_state(args):
    state = load_state(args.state)
    if state is None:
        raise UsageError(f"no state file at {args.state} — run 'open --enable' first")
    return state


def _require_thread(state):
    if not state.get("threadId"):
        raise NoThreadError("no thread yet — run 'send' first (thread is born on first send)")
    return state["threadId"]


def _birth_or_resume(session, state):
    """BRICK-01: shared birth/resume for send/ask. Birth = thread/start (+cwd) then the
    caller's turn/start in the SAME connection (Cartan's proven continuous sequence).
    Resume = thread/resume of the saved/bound threadId. Either way the server-reported
    runtime policy is stamped into state. Returns thread_id."""
    if state.get("threadId") is None:
        start = session.thread_start(
            model=state.get("model"),
            sandbox=state.get("sandbox", "read-only"),
            cwd=state.get("cwd"),
        )
        thread = start.get("thread", {})
        thread_id = thread.get("id")
        if not thread_id:
            raise ProtocolError(f"thread/start did not return a thread id: {start}")
        state["threadId"] = thread_id
        state["model"] = start.get("model") or state.get("model")
        state["sandbox"] = start.get("sandbox") or state.get("sandbox")
        _stamp_runtime(state, start)
    else:
        thread_id = state["threadId"]
        _warn_if_writer_lock(thread_id)
        resumed = session.thread_resume(thread_id)
        _stamp_runtime(state, resumed)
    return state["threadId"]


def cmd_send(args):
    state = _require_state(args)
    text_out = _apply_preamble(state, args.text)
    lock = _acquire_turn_lock(args.state)
    try:
        transport = AppServerTransport(cwd=state.get("cwd"))
        transport.start()
        try:
            session = Session(transport)
            session.initialize()
            thread_id = _birth_or_resume(session, state)
            turn_id, turn, text, usage = session.drive_turn(thread_id, text_out, overrides=state.get("turnOverrides"))
            session.reconcile(thread_id, turn_id)
        finally:
            transport.close()
        state["lastTurnId"] = turn_id
        save_state(args.state, state)
    finally:
        _release_turn_lock(lock)
    print(text)
    tail = _format_usage_tail(usage)
    if tail is not None:
        print(tail)


def cmd_steer(args):
    state = _require_state(args)
    thread_id = _require_thread(state)
    if not state.get("lastTurnId"):
        raise TurnError("no lastTurnId recorded in state — nothing to steer (run 'send' first)")
    text_out = _apply_preamble(state, args.text)
    lock = _acquire_turn_lock(args.state)
    try:
        _warn_if_writer_lock(thread_id)
        transport = AppServerTransport(cwd=state.get("cwd"))
        transport.start()
        try:
            session = Session(transport)
            session.initialize()
            resumed = session.thread_resume(thread_id)
            _stamp_runtime(state, resumed)
            turn_id, turn, text, usage = session.drive_turn(
                thread_id, text_out, expected_turn_id=state["lastTurnId"]
            )
            session.reconcile(thread_id, turn_id)
        finally:
            transport.close()
        state["lastTurnId"] = turn_id
        save_state(args.state, state)
    finally:
        _release_turn_lock(lock)
    print(text)
    # Kept consistent with send/ask under the one-return-channel law: steer drives a
    # turn the same way send does, so it gets the same usage tail even though it isn't
    # separately enumerated in the send/ask/read stdout list.
    tail = _format_usage_tail(usage)
    if tail is not None:
        print(tail)


def cmd_ask(args):
    """send + reconcile in one call: performs the full send (thread birth or resume),
    drives the turn, then thread/read(includeTurns=true) reconciliation, and VERIFIES
    the streamed agent text matches the read-back text for that turn. On match: prints
    the verified text + usage tail to stdout, exit 0. On mismatch: raises
    ReconcileMismatch (exit 50) with both texts named on stderr — never silently picks
    one. Same Law 2.4 gates as every other verb (enforced by the caller before this
    function runs): no auto-enable, no state-path default."""
    state = _require_state(args)
    text_out = _apply_preamble(state, args.text)
    lock = _acquire_turn_lock(args.state)
    try:
        transport = AppServerTransport(cwd=state.get("cwd"))
        transport.start()
        try:
            session = Session(transport)
            session.initialize()
            thread_id = _birth_or_resume(session, state)
            turn_id, turn, streamed_text, usage = session.drive_turn(thread_id, text_out, overrides=state.get("turnOverrides"))
            read_result = session.reconcile(thread_id, turn_id)
        finally:
            transport.close()
        state["lastTurnId"] = turn_id
        save_state(args.state, state)
    finally:
        _release_turn_lock(lock)

    readback_text = _extract_agent_text(read_result, turn_id)

    if streamed_text != readback_text:
        raise ReconcileMismatch(
            f"ask verify failed for turn {turn_id} — streamed and read-back text "
            f"disagree: streamed={streamed_text!r} read-back={readback_text!r}"
        )

    print(streamed_text)
    tail = _format_usage_tail(usage)
    if tail is not None:
        print(tail)


def cmd_read(args):
    state = _require_state(args)
    thread_id = _require_thread(state)
    # BRICK-01: same spawn dir as every other verb (read creates nothing; consistency only).
    transport = AppServerTransport(cwd=state.get("cwd"))
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        result = session.thread_read(thread_id, include_turns=True)
    finally:
        transport.close()
    print(json.dumps(result, indent=2))


def cmd_resume(args):
    state = _require_state(args)
    thread_id = _require_thread(state)
    _warn_if_writer_lock(thread_id)
    transport = AppServerTransport(cwd=state.get("cwd"))
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        result = session.thread_resume(thread_id)
    finally:
        transport.close()
    # BRICK-01: `tun resume` is the operator's liveness probe for a bound head — persist
    # what the server reports (effective sandbox/effort/cwd, loaded instruction files)
    # so the next `tun status` shows runtime truth as of this contact.
    _stamp_runtime(state, result)
    save_state(args.state, state)
    thread = result.get("thread", {})
    rt = state.get("runtime", {})
    print(
        f"resume: thread {thread_id} status={thread.get('status')} "
        f"sandbox={rt.get('sandbox')} effort={rt.get('reasoningEffort')} cwd={rt.get('cwd')} "
        f"instructionSources={rt.get('instructionSources')}",
        file=sys.stderr,
    )


def cmd_compact(args):
    """thread/compact/start on the bound thread (2026-10-09, PAD J probe on 0.162): the
    server runs compaction as a turn — turn/started … turn/completed (≈43 s observed) —
    and keeps the thread id. NO thread/compacted notification arrives on this connection;
    turn/completed is the completion signal. Takes the turn lock (it is a turn). Banner-only:
    stdout stays empty; stderr reports duration; the next send/ask shows the new ctx."""
    state = _require_state(args)
    thread_id = _require_thread(state)
    lock = _acquire_turn_lock(args.state)
    t0 = time.time()
    try:
        _warn_if_writer_lock(thread_id)
        transport = AppServerTransport(cwd=state.get("cwd"))
        transport.start()
        try:
            session = Session(transport, timeout=max(DEFAULT_TIMEOUT, 600.0))
            session.initialize()
            resumed = session.thread_resume(thread_id)
            _stamp_runtime(state, resumed)
            rid = transport.request("thread/compact/start", {"threadId": thread_id})
            session._await_response(rid)
            deadline = time.time() + session.timeout
            turn_id = None
            while True:
                remaining = deadline - time.time()
                if remaining <= 0:
                    raise ProtocolError(f"compact: no turn/completed within {session.timeout:.0f}s — run 'read' before retrying")
                msg = transport.next_message(remaining)
                if "method" in msg and "id" in msg:
                    session._auto_decline(msg)
                    continue
                m, prm = msg.get("method"), msg.get("params") or {}
                if prm.get("threadId") not in (None, thread_id):
                    continue
                if m == "turn/started":
                    turn_id = (prm.get("turn") or {}).get("id")
                elif m == "turn/completed":
                    turn = prm.get("turn") or {}
                    if turn.get("status") != "completed":
                        raise TurnError(f"compact turn ended {turn.get('status')}: {turn.get('error')}")
                    turn_id = turn.get("id") or turn_id
                    break
        finally:
            transport.close()
    finally:
        _release_turn_lock(lock)
    state["lastCompactAt"] = now_iso()
    save_state(args.state, state)
    print(f"compact: thread {thread_id} compacted in {time.time() - t0:.0f}s (turn {turn_id}); "
          "id kept — the next send/ask shows the new ctx", file=sys.stderr)


def build_parser():
    parser = argparse.ArgumentParser(prog="tunnel-codex.py", add_help=True)
    sub = parser.add_subparsers(dest="verb", required=True)

    p_open = sub.add_parser("open")
    p_open.add_argument("--state", required=True)
    p_open.add_argument("--sandbox", default="read-only")
    p_open.add_argument("--model", default=None)
    # BRICK-01
    p_open.add_argument("--thread", default=None, help="bind this vault to an EXISTING stored threadId")
    p_open.add_argument("--cwd", default=None, help="workspace root: app-server spawn dir + thread/start.cwd on birth")
    p_open.add_argument("--preamble", default=None, help="file prepended to every send/ask/steer ('none' clears)")
    p_open.add_argument("--override", action="append", default=None,
                        help="turn/start override key=value (model|effort|approvalPolicy|approvalsReviewer|summary); key= removes; 'none' clears all")
    p_open.set_defaults(func=cmd_open)

    p_send = sub.add_parser("send")
    p_send.add_argument("text")
    p_send.add_argument("--state", required=True)
    p_send.set_defaults(func=cmd_send)

    p_steer = sub.add_parser("steer")
    p_steer.add_argument("text")
    p_steer.add_argument("--state", required=True)
    p_steer.set_defaults(func=cmd_steer)

    p_ask = sub.add_parser("ask")
    p_ask.add_argument("text")
    p_ask.add_argument("--state", required=True)
    p_ask.set_defaults(func=cmd_ask)

    p_read = sub.add_parser("read")
    p_read.add_argument("--state", required=True)
    p_read.set_defaults(func=cmd_read)

    p_compact = sub.add_parser("compact")
    p_compact.add_argument("--state", required=True)
    p_compact.set_defaults(func=cmd_compact)

    p_resume = sub.add_parser("resume")
    p_resume.add_argument("--state", required=True)
    p_resume.set_defaults(func=cmd_resume)

    return parser


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        sys.exit(EXIT_USAGE if code == 2 else code)

    try:
        args.func(args)
    except TunnelError as exc:
        print(f"tunnel-codex.py: {exc}", file=sys.stderr)
        sys.exit(exc.exit_code)
    except Exception as exc:  # unexpected — still fail loud with a distinct, documented code
        print(f"tunnel-codex.py: unexpected error: {exc}", file=sys.stderr)
        sys.exit(EXIT_PROTOCOL_ERROR)

    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
