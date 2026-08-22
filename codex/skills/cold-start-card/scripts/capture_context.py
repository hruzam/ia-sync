#!/usr/bin/env python3
"""Emit a secret-averse JSON snapshot for a Codex cold-start card."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def run(command: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    output = result.stdout.strip()
    return output or None


def git(command: list[str], root: Path) -> str | None:
    return run(["git", *command], cwd=root)


def git_snapshot(root: Path) -> dict[str, Any]:
    status = git(["status", "--short"], root)
    ignored_candidates = [
        ".dev",
        ".codex/agents",
        ".codex/config.toml",
        ".agents/skills",
        ".claude/agents",
        ".claude/skills",
        "CLAUDE.local.md",
        "GEMINI.md",
    ]
    existing_candidates = [item for item in ignored_candidates if (root / item).exists()]
    ignored_status = (
        git(["status", "--short", "--ignored", "--", *existing_candidates], root)
        if existing_candidates
        else None
    )
    commit_lines = git(
        ["log", "-5", "--date=iso-strict", "--pretty=format:%H%x09%ad%x09%an%x09%s"],
        root,
    )

    commits = []
    for line in (commit_lines or "").splitlines():
        parts = line.split("\t", 3)
        if len(parts) == 4:
            commits.append(dict(zip(("sha", "date", "author", "subject"), parts)))

    return {
        "root": str(root),
        "branch": git(["branch", "--show-current"], root),
        "head": git(["rev-parse", "HEAD"], root),
        "upstream": git(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], root
        ),
        "tracked_state": "dirty" if status else "clean",
        "status": (status or "").splitlines(),
        "ignored_project_state": (ignored_status or "").splitlines(),
        "unstaged_stat": (git(["diff", "--stat"], root) or "").splitlines(),
        "staged_stat": (git(["diff", "--cached", "--stat"], root) or "").splitlines(),
        "recent_commits": commits,
    }


def instruction_files(cwd: Path, root: Path) -> list[str]:
    paths: list[Path] = []
    global_agents = Path.home() / ".codex" / "AGENTS.md"
    if global_agents.is_file():
        paths.append(global_agents)

    ancestors = list(cwd.parents)
    ancestors.insert(0, cwd)
    for directory in reversed(ancestors[: ancestors.index(root.parent)]):
        candidate = directory / "AGENTS.md"
        if candidate.is_file() and candidate not in paths:
            paths.append(candidate)

    for relative in (
        "CLAUDE.md",
        "CLAUDE.local.md",
        "GEMINI.md",
        ".dev/PROJECT.yaml",
        ".codex/config.toml",
    ):
        candidate = root / relative
        if candidate.is_file():
            paths.append(candidate)

    return [str(path) for path in paths]


def read_tail(path: Path, maximum_bytes: int = 8 * 1024 * 1024) -> list[str]:
    with path.open("rb") as handle:
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        offset = max(0, size - maximum_bytes)
        handle.seek(offset)
        if offset:
            handle.readline()
        return handle.read().decode("utf-8", errors="replace").splitlines()


def matching_session(cwd: Path, session_root: Path) -> dict[str, Any] | None:
    if not session_root.is_dir():
        return None

    rollouts = sorted(
        session_root.glob("**/rollout-*.jsonl"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )[:100]

    for rollout in rollouts:
        try:
            with rollout.open(encoding="utf-8") as handle:
                first = json.loads(handle.readline())
        except (OSError, json.JSONDecodeError):
            continue

        payload = first.get("payload", {})
        if first.get("type") != "session_meta" or payload.get("cwd") != str(cwd):
            continue

        model = None
        effort = None
        for line in reversed(read_tail(rollout)):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "turn_context":
                context = event.get("payload", {})
                model = context.get("model")
                effort = context.get("effort")
                break

        return {
            "session_id": payload.get("id"),
            "rollout": str(rollout),
            "started_at": payload.get("timestamp"),
            "originator": payload.get("originator"),
            "cli_version_at_start": payload.get("cli_version"),
            "source": payload.get("source"),
            "model_provider": payload.get("model_provider"),
            "model": model,
            "effort": effort,
        }

    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", default=".", help="Working directory to describe")
    parser.add_argument(
        "--session-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Codex session directory",
    )
    args = parser.parse_args()

    cwd = Path(args.cwd).expanduser().resolve()
    root_text = run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"])
    root = Path(root_text).resolve() if root_text else cwd
    transport = root.with_name(f"{root.name}.devenv")

    result: dict[str, Any] = {
        "schema": "codex-context-capture/v1",
        "captured_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "host": {
            "hostname": socket.gethostname(),
            "logical": os.environ.get("MACHINE_NAME"),
            "platform": platform.platform(),
            "shell": os.environ.get("SHELL"),
        },
        "tools": {
            name: {"path": shutil.which(name), "version": run(version_command)}
            for name, version_command in {
                "codex": ["codex", "--version"],
                "git": ["git", "--version"],
                "rg": ["rg", "--version"],
                "python3": ["python3", "--version"],
                "jq": ["jq", "--version"],
            }.items()
        },
        "cwd": str(cwd),
        "instructions": instruction_files(cwd, root),
        "repository": git_snapshot(root) if root_text else None,
        "codex_session": matching_session(cwd, Path(args.session_root).expanduser()),
        "transport_candidate": git_snapshot(transport) if (transport / ".git").exists() else None,
        "safety": {
            "excluded": [
                "environment values except MACHINE_NAME and SHELL",
                "credentials and authentication state",
                "remote URLs",
                "session transcript content",
                "database contents",
            ]
        },
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
