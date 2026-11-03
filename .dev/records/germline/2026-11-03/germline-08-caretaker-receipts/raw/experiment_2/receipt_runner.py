#!/usr/bin/env python3
"""Deploy-inert, receipt-first runner for the bounded G08 trial."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / "live"
SHIM = "/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh"
CODEX = "/home/hruzam/.local/bin/codex"
PEERS = {"peer-a", "peer-b"}
VERBS = {"open", "ask", "resume"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proc_start(pid):
    try:
        tail = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return tail[19]  # Linux /proc stat field 22 (starttime).
    except (FileNotFoundError, IndexError, OSError):
        return None


def atomic_write(path, value):
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def select_state(path):
    if not path.exists():
        return None
    try:
        state = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {"state": "malformed"}
    if not isinstance(state, dict):
        return {"state": "malformed"}
    return {key: state.get(key) for key in ("threadId", "lastTurnId", "model", "sandbox", "runtime")}


def output_paths(operation, output_dir):
    stem = operation.name.removesuffix(".operation.json")
    return output_dir / f"{stem}.stdout.txt", output_dir / f"{stem}.stderr.txt"


def inspect(operation):
    try:
        receipt = json.loads(operation.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"classification": "unknown", "reason": "missing-or-malformed-receipt"}
    if not isinstance(receipt, dict):
        return {"classification": "unknown", "reason": "missing-or-malformed-receipt", "retryable": False}
    status = receipt.get("status")
    if status == "pending":
        runner = receipt.get("runner")
        runner = runner if isinstance(runner, dict) else {}
        pid = runner.get("pid")
        if isinstance(pid, int) and pid > 0 and runner.get("start") and proc_start(pid) == runner["start"]:
            return {"classification": "running", "retryable": False}
        return {"classification": "unknown", "reason": "dead-or-unverifiable-pending", "retryable": False}
    if status == "failed":
        return {"classification": "failed-with-remote-outcome-unknown", "retryable": False}
    if status != "completed" or receipt.get("exit") != 0:
        return {"classification": "unknown", "reason": "invalid-completed-receipt", "retryable": False}
    outputs = receipt.get("outputs")
    outputs = outputs if isinstance(outputs, dict) else {}
    for kind in ("stdout", "stderr"):
        value = outputs.get(kind)
        value = value if isinstance(value, dict) else {}
        name = value.get("path")
        try:
            valid = isinstance(name, str) and Path(name).is_file() and digest(Path(name)) == value.get("sha256")
        except OSError:
            valid = False
        if not valid:
            return {"classification": "unknown", "reason": f"invalid-{kind}-output", "retryable": False}
    return {"classification": "completed-and-validated", "retryable": False}


def run_operation(operation, argv, output_dir, executor=subprocess.run, before=None, after=None, extra=None):
    """Create the exclusive pending receipt, execute once, then atomically finish it."""
    output_dir.mkdir(parents=True, exist_ok=True)
    stdout_path, stderr_path = output_paths(operation, output_dir)
    pending = {
        "status": "pending",
        "argv": list(argv),
        "started_unix": time.time(),
        "runner": {"pid": os.getpid(), "start": proc_start(os.getpid())},
        "state_before": before() if before else None,
    }
    if extra:
        pending.update(extra)
    try:
        with operation.open("x", encoding="utf-8") as handle:
            json.dump(pending, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        raise RuntimeError(f"refusing existing operation record: {operation}")
    try:
        result = executor(list(argv))
        stdout = result.stdout if isinstance(result.stdout, bytes) else (result.stdout or "").encode()
        stderr = result.stderr if isinstance(result.stderr, bytes) else (result.stderr or "").encode()
        stdout_path.write_bytes(stdout)
        stderr_path.write_bytes(stderr)
        pending.update({
            "status": "completed" if result.returncode == 0 else "failed",
            "ended_unix": time.time(),
            "elapsed_seconds": round(time.time() - pending["started_unix"], 3),
            "exit": result.returncode,
            "outputs": {
                "stdout": {"path": str(stdout_path), "sha256": digest(stdout_path)},
                "stderr": {"path": str(stderr_path), "sha256": digest(stderr_path)},
            },
            "state_after": after() if after else None,
        })
    except Exception as error:
        pending.update({"status": "failed", "ended_unix": time.time(),
                        "elapsed_seconds": round(time.time() - pending["started_unix"], 3),
                        "exception": repr(error), "remote_outcome": "unknown"})
    atomic_write(operation, pending)
    return inspect(operation)


def fixed_argv(root, peer, verb):
    state = root / "live" / f"tunnel.{peer}.state.json"
    base = [SHIM, verb, "--state", str(state)]
    if verb == "open":
        return base + ["--enable", "--sandbox", "read-only", "--cwd", str(root.parents[1]),
                       "--preamble", "none", "--model", "gpt-6.1-sol", "--override", "effort=low"]
    if verb == "ask":
        return base + [(root / "live" / f"{peer}.prompt.txt").read_text()]
    return base


def capture_version():
    result = subprocess.run([CODEX, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {"argv": [CODEX, "--version"], "exit": result.returncode,
            "stdout": result.stdout.decode(errors="replace").strip(),
            "stderr": result.stderr.decode(errors="replace").strip()}


def run_live(peer, verb):
    operation = LIVE / f"{peer}.{verb}.operation.json"
    state = LIVE / f"tunnel.{peer}.state.json"
    state_before = select_state(state)
    precondition = None
    if verb == "open" and state_before is not None:
        precondition = "state already exists without an operation receipt; refusing re-execution"
    elif verb in {"ask", "resume"} and (state_before is None or state_before.get("state") == "malformed"):
        precondition = "missing or malformed state; refusing target invocation"
    version = {"status": "not-run"}
    def executor(argv):
        if precondition:
            return subprocess.CompletedProcess(argv, 11, b"", precondition.encode())
        version.clear()
        version.update(capture_version())  # Pending receipt already exists at this point.
        if version["exit"]:
            return subprocess.CompletedProcess(argv, version["exit"], b"", version["stderr"].encode())
        return subprocess.run(argv, cwd=ROOT.parent, env=dict(os.environ, TUNNEL_CODEX_BIN=CODEX,
                              TUNNEL_CODEX_USAGE="full"), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=False)
    return run_operation(operation, fixed_argv(ROOT, peer, verb), LIVE, executor=executor,
                         before=lambda: state_before, after=lambda: select_state(state),
                         extra={"peer": peer, "verb": verb, "codex_binary": CODEX,
                                "codex_version": version,
                                "precondition": precondition,
                                "requested": {"model": "gpt-6.1-sol", "effort": "low"}})


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("peer", choices=sorted(PEERS))
    run.add_argument("verb", choices=sorted(VERBS))
    check = sub.add_parser("inspect")
    check.add_argument("peer", choices=sorted(PEERS))
    check.add_argument("verb", choices=sorted(VERBS))
    args = parser.parse_args()
    operation = LIVE / f"{args.peer}.{args.verb}.operation.json"
    if args.command == "inspect":
        print(json.dumps(inspect(operation), sort_keys=True))
        return
    try:
        print(json.dumps(run_live(args.peer, args.verb), sort_keys=True))
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
