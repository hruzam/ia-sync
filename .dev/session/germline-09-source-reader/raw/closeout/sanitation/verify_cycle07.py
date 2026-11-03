#!/usr/bin/env python3
"""G09 cycle07 sanitation: exact R1 metadata and receipt-linked process checks only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time

BED = Path("/home/hruzam/ia-sync/.dev/session/germline-09-source-reader")
OUT = BED / "raw/closeout/sanitation/07.selected-verification.json"
THREAD = "01a176f7-532b-7722-9324-0ecb92694073"
TURN = "01a176f7-53a6-7b83-b203-b86b08ec15ac"
VAULT = BED / "raw/caretaker/tunnel.researcher.state.json"
SOURCE_KINDS = [
    "cli", "vscode", "exec", "appServer", "subAgent", "subAgentReview",
    "subAgentCompact", "subAgentThreadSpawn", "subAgentOther", "unknown",
]
KNOWN_PROCESSES = [
    ("R1-runner", 1319728, "296276499", None),
    ("old-verification-checker", 1923120, "299269158", "python3"),
    ("old-verification-app-server", 1923121, "299269177", "codex"),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proc_identity(pid):
    proc = Path("/proc") / str(pid)
    try:
        raw = (proc / "stat").read_text()
        fields = raw[raw.rfind(")") + 2:].split()
        return {
            "present": True,
            "pid": pid,
            "uid": proc.stat().st_uid,
            "start_ticks": fields[19],
            "comm": (proc / "comm").read_text().strip(),
            "pid_namespace": os.readlink(proc / "ns/pid"),
        }
    except (FileNotFoundError, PermissionError, OSError, IndexError, ValueError):
        return {"present": False, "pid": pid}


def select_thread(raw):
    thread = raw.get("thread") or {}
    return {
        "id": thread.get("id"),
        "cwd": thread.get("cwd"),
        "status": thread.get("status"),
        "turns": [
            {"id": item.get("id"), "status": item.get("status")}
            for item in (thread.get("turns") or [])
        ],
    }


def main():
    if OUT.exists():
        raise RuntimeError(f"refusing to overwrite receipt: {OUT}")
    manifest = json.loads((BED / "raw/closeout/PRESERVATION.run-01.json").read_text())
    unchanged, changed, missing, allowed_removed = [], [], [], []
    for entry in manifest["G09_original_files"]:
        path = BED / entry["path"]
        if not path.exists():
            if entry["retirement_allowed"]:
                allowed_removed.append(entry["path"])
            else:
                missing.append(entry["path"])
        elif digest(path) == entry["sha256"]:
            unchanged.append(entry["path"])
        else:
            changed.append(entry["path"])

    snapshots = {
        "RUNBOOK.run-01.original.md": "de9ae7cc1fddc54a019c3bfc7ecb6739918112420d7e3c67f8cbbed8aafa4fdf",
        "STATUS.run-01.pre-close.md": "bbc0e2dcf14b3a7d74ac02dce553d365a70463e6294f33042be120b187edf200",
        "tunnel.researcher.state.json": "5789ba86f3f79d35fae18fa17a479297ce40c4071cefb93ba81e75226b69e6e9",
    }
    snapshot_result = {
        name: {"present": (BED / "raw/closeout/snapshots" / name).is_file(),
               "sha256": digest(BED / "raw/closeout/snapshots" / name)
                         if (BED / "raw/closeout/snapshots" / name).is_file() else None,
               "expected_sha256": expected}
        for name, expected in snapshots.items()
    }
    release = json.loads((BED / "raw/control/RELEASE.json").read_text())

    result = {
        "schema": "g09-sanitation-cycle07/v1",
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scope": "read-only preservation, exact R1 metadata, and receipt-linked PID checks",
        "actions_beyond_read_only": [],
        "preservation": {
            "manifest_entries": len(manifest["G09_original_files"]),
            "protected_unchanged_count": len(unchanged),
            "protected_changed": changed,
            "protected_missing": missing,
            "allowed_removed": allowed_removed,
            "vault_absent": not VAULT.exists(),
            "vault_lock_absent": not Path(str(VAULT) + ".lock").exists(),
            "snapshots": snapshot_result,
            "release_authorized": release.get("authorized"),
        },
        "current_pid_namespace": os.readlink("/proc/self/ns/pid"),
        "processes": [],
        "r1_metadata": {"allowed_methods": ["initialize", "thread/list", "thread/read"]},
    }
    for role, pid, expected_start, expected_comm in KNOWN_PROCESSES:
        observed = proc_identity(pid)
        observed.update({
            "role": role,
            "expected_start_ticks": expected_start,
            "expected_comm": expected_comm,
            "identity_matches_historical": observed.get("present") and
                observed.get("start_ticks") == expected_start and
                (expected_comm is None or observed.get("comm") == expected_comm),
        })
        result["processes"].append(observed)

    spec = importlib.util.spec_from_file_location(
        "g09_cycle07_transport", "/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    transport = module.AppServerTransport(
        codex_bin="/home/hruzam/.local/bin/codex", cwd=str(BED))
    try:
        transport.start()
        session = module.Session(transport, timeout=30)
        session.initialize()
        lists = []
        for archived in (True, False):
            params = {
                "cwd": str(BED), "limit": 10, "searchTerm": "G09.R1",
                "archived": archived, "sourceKinds": SOURCE_KINDS,
                "useStateDbOnly": True,
            }
            response = session._await_response(transport.request("thread/list", params))
            matches = [item for item in response.get("data", []) if item.get("id") == THREAD]
            lists.append({
                "query": {"cwd": str(BED), "title_search_term": "G09.R1",
                          "archived": archived, "sourceKinds": SOURCE_KINDS,
                          "useStateDbOnly": True},
                "matching_known_thread": [
                    {"id": item.get("id"), "cwd": item.get("cwd"), "status": item.get("status")}
                    for item in matches
                ],
                "next_cursor_present": bool(response.get("nextCursor")),
            })
        selected = select_thread(session.thread_read(THREAD, include_turns=True))
        result["r1_metadata"].update({"archival_queries": lists, "stored_thread": selected})
        result["r1_metadata"]["expectations_met"] = (
            lists[0]["matching_known_thread"] and not lists[1]["matching_known_thread"] and
            selected["id"] == THREAD and
            selected["turns"] == [{"id": TURN, "status": "interrupted"}]
        )
    except Exception as exc:
        result["r1_metadata"]["error"] = repr(exc)
    finally:
        transport.close()
        result["app_server_exit"] = transport.proc.poll() if transport.proc else None
        result["app_server_closed"] = bool(transport.proc and transport.proc.poll() is not None)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "receipt": str(OUT),
        "metadata_error": result["r1_metadata"].get("error"),
        "expectations_met": result["r1_metadata"].get("expectations_met"),
        "actions_beyond_read_only": result["actions_beyond_read_only"],
    }))


if __name__ == "__main__":
    main()
