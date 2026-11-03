#!/usr/bin/env python3
"""One elevated retry of G09 cycle07's exact read-only R1 metadata check."""
import importlib.util
import json
import os
from pathlib import Path
import time

BED = Path("/home/hruzam/ia-sync/.dev/session/germline-09-source-reader")
OUT = BED / "raw/closeout/sanitation/08.r1-metadata-elevated.json"
THREAD = "01a176f7-532b-7722-9324-0ecb92694073"
TURN = "01a176f7-53a6-7b83-b203-b86b08ec15ac"
SOURCE_KINDS = [
    "cli", "vscode", "exec", "appServer", "subAgent", "subAgentReview",
    "subAgentCompact", "subAgentThreadSpawn", "subAgentOther", "unknown",
]


def selected_thread(raw):
    thread = raw.get("thread") or {}
    return {
        "id": thread.get("id"), "cwd": thread.get("cwd"), "status": thread.get("status"),
        "turns": [{"id": turn.get("id"), "status": turn.get("status")}
                  for turn in (thread.get("turns") or [])],
    }


def main():
    if OUT.exists():
        raise RuntimeError(f"refusing to overwrite receipt: {OUT}")
    result = {
        "schema": "g09-sanitation-cycle07-r1-metadata/v1",
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "allowed_methods": ["initialize", "thread/list", "thread/read"],
        "current_pid_namespace": os.readlink("/proc/self/ns/pid"),
    }
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
        queries = []
        for archived in (True, False):
            params = {
                "cwd": str(BED), "limit": 10, "searchTerm": "G09.R1",
                "archived": archived, "sourceKinds": SOURCE_KINDS,
                "useStateDbOnly": True,
            }
            response = session._await_response(transport.request("thread/list", params))
            matches = [entry for entry in response.get("data", []) if entry.get("id") == THREAD]
            queries.append({
                "query": {"cwd": str(BED), "title_search_term": "G09.R1",
                          "archived": archived, "sourceKinds": SOURCE_KINDS,
                          "useStateDbOnly": True},
                "matching_known_thread": [
                    {"id": entry.get("id"), "cwd": entry.get("cwd"), "status": entry.get("status")}
                    for entry in matches
                ],
                "next_cursor_present": bool(response.get("nextCursor")),
            })
        stored = selected_thread(session.thread_read(THREAD, include_turns=True))
        result.update({
            "archival_queries": queries,
            "stored_thread": stored,
            "expectations_met": bool(queries[0]["matching_known_thread"]) and
                not queries[1]["matching_known_thread"] and stored == {
                    "id": THREAD, "cwd": str(BED), "status": {"type": "notLoaded"},
                    "turns": [{"id": TURN, "status": "interrupted"}],
                },
        })
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        transport.close()
        result["app_server_exit"] = transport.proc.poll() if transport.proc else None
        result["app_server_closed"] = bool(transport.proc and transport.proc.poll() is not None)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"receipt": str(OUT), "error": result.get("error"),
                      "expectations_met": result.get("expectations_met"),
                      "app_server_closed": result["app_server_closed"]}))


if __name__ == "__main__":
    main()
