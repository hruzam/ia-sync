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
  11 usage error (bad args, unknown verb, invalid sandbox value)
  20 spawn-fail (codex binary not found / app-server process would not start)
  30 protocol-error (JSON-RPC transport broke: bad JSON, EOF, timeout, error reply)
  40 turn-error (turn/start|steer returned an error, the turn ended non-"completed",
     or steer had no recorded turn id to target)
  50 reconcile-mismatch (thread/read(includeTurns=true) does not contain the turn we
     just drove, or disagrees with what turn/completed reported)
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


class AppServerTransport:
    """One `codex app-server --stdio` subprocess, newline-delimited JSON-RPC 2.0."""

    def __init__(self, codex_bin=None):
        self.codex_bin = codex_bin or os.environ.get("TUNNEL_CODEX_BIN", "codex")
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

    def thread_start(self, model=None, sandbox="read-only"):
        params = {"sandbox": sandbox, "approvalPolicy": "never"}
        if model:
            params["model"] = model
        rid = self.t.request("thread/start", params)
        return self._await_response(rid)

    def thread_resume(self, thread_id):
        rid = self.t.request("thread/resume", {"threadId": thread_id})
        return self._await_response(rid)

    def thread_read(self, thread_id, include_turns=True):
        rid = self.t.request("thread/read", {"threadId": thread_id, "includeTurns": include_turns})
        return self._await_response(rid)

    def drive_turn(self, thread_id, text, expected_turn_id=None):
        """turn/start (expected_turn_id is None) or turn/steer (expected_turn_id given
        — the ID of the turn this same shim already recorded), then consume streamed
        notifications until turn/completed for this thread. Returns
        (turn_id, completed_turn_dict, final_agent_text)."""
        user_input = [{"type": "text", "text": text}]
        if expected_turn_id is None:
            rid = self.t.request("turn/start", {"threadId": thread_id, "input": user_input})
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
            elif method == "turn/completed" and params.get("threadId") == thread_id:
                completed_turn = params.get("turn", {})
            # every other notification (turn/started, item/started, token-usage, ...)
            # is dropped — v0 only needs the final read-back, not the live stream.

        if completed_turn.get("id") != turn_id:
            raise TurnError(f"turn/completed reported id={completed_turn.get('id')!r}, expected {turn_id!r}")
        if completed_turn.get("status") != "completed":
            raise TurnError(
                f"turn {turn_id} ended with status={completed_turn.get('status')!r}: "
                f"{completed_turn.get('error')}"
            )

        final_text = agent_texts[-1] if agent_texts else ""
        return turn_id, completed_turn, final_text

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

    state = load_state(args.state)

    if state is None:
        # Zero-turn preflight only — deliberately NO thread/start (see THREAD BIRTH
        # note above the exit-code table). This spawns app-server, confirms the
        # handshake + account/model surface work, then persists threadId: null.
        transport = AppServerTransport()
        transport.start()
        try:
            session = Session(transport)
            session.initialize()
            session.account_read()
            session.model_list()
        finally:
            transport.close()
        state = {
            "enabled": True,
            "threadId": None,
            "lastTurnId": None,
            "model": args.model,
            "sandbox": args.sandbox,
            "created": now_iso(),
        }
        save_state(args.state, state)
        print(
            f"open: enabled (model={state['model']}, sandbox={state['sandbox']}); "
            "no thread yet — thread will be born on first send"
        )
        return

    if state.get("threadId") is None:
        print("open: already enabled; no thread yet — thread will be born on first send")
        return

    # An existing, already-born thread: liveness-probe it (unchanged behavior).
    transport = AppServerTransport()
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        resumed = session.thread_resume(state["threadId"])
        thread = resumed.get("thread", {})
        print(f"open: resumed existing thread {state['threadId']} (status={thread.get('status')})")
    finally:
        transport.close()


def _require_state(args):
    state = load_state(args.state)
    if state is None:
        raise UsageError(f"no state file at {args.state} — run 'open --enable' first")
    return state


def _require_thread(state):
    if not state.get("threadId"):
        raise NoThreadError("no thread yet — run 'send' first (thread is born on first send)")
    return state["threadId"]


def cmd_send(args):
    state = _require_state(args)
    transport = AppServerTransport()
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        if state.get("threadId") is None:
            # Thread birth: thread/start then turn/start in THIS SAME connection —
            # Cartan's proven continuous sequence — so the rollout exists before any
            # other verb (running in its own fresh subprocess) could try to resume it.
            start = session.thread_start(model=state.get("model"), sandbox=state.get("sandbox", "read-only"))
            thread = start.get("thread", {})
            thread_id = thread.get("id")
            if not thread_id:
                raise ProtocolError(f"thread/start did not return a thread id: {start}")
            state["threadId"] = thread_id
            state["model"] = start.get("model") or state.get("model")
            state["sandbox"] = start.get("sandbox") or state.get("sandbox")
        else:
            thread_id = state["threadId"]
            session.thread_resume(thread_id)
        thread_id = state["threadId"]
        turn_id, turn, text = session.drive_turn(thread_id, args.text)
        session.reconcile(thread_id, turn_id)
    finally:
        transport.close()
    state["lastTurnId"] = turn_id
    save_state(args.state, state)
    print(text)


def cmd_steer(args):
    state = _require_state(args)
    thread_id = _require_thread(state)
    if not state.get("lastTurnId"):
        raise TurnError("no lastTurnId recorded in state — nothing to steer (run 'send' first)")
    transport = AppServerTransport()
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        session.thread_resume(thread_id)
        turn_id, turn, text = session.drive_turn(thread_id, args.text, expected_turn_id=state["lastTurnId"])
        session.reconcile(thread_id, turn_id)
    finally:
        transport.close()
    state["lastTurnId"] = turn_id
    save_state(args.state, state)
    print(text)


def cmd_read(args):
    state = _require_state(args)
    thread_id = _require_thread(state)
    transport = AppServerTransport()
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
    transport = AppServerTransport()
    transport.start()
    try:
        session = Session(transport)
        session.initialize()
        result = session.thread_resume(thread_id)
    finally:
        transport.close()
    thread = result.get("thread", {})
    print(f"resume: thread {thread_id} status={thread.get('status')}")


def build_parser():
    parser = argparse.ArgumentParser(prog="tunnel-codex.py", add_help=True)
    sub = parser.add_subparsers(dest="verb", required=True)

    p_open = sub.add_parser("open")
    p_open.add_argument("--state", required=True)
    p_open.add_argument("--sandbox", default="read-only")
    p_open.add_argument("--model", default=None)
    p_open.set_defaults(func=cmd_open)

    p_send = sub.add_parser("send")
    p_send.add_argument("text")
    p_send.add_argument("--state", required=True)
    p_send.set_defaults(func=cmd_send)

    p_steer = sub.add_parser("steer")
    p_steer.add_argument("text")
    p_steer.add_argument("--state", required=True)
    p_steer.set_defaults(func=cmd_steer)

    p_read = sub.add_parser("read")
    p_read.add_argument("--state", required=True)
    p_read.set_defaults(func=cmd_read)

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
