# B0 Codex native-hook qualification — cycle 04

POINT: `/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/_bus/04.cartan-muticula.point.md`

Fixture: `/tmp/muticula-b0-codex-ki5dIN/fixture` (new Git repository, no stage or commit).
Runtime: Codex CLI `0.156.1`, pinned `gpt-5.6-terra` with `model_reasoning_effort="high"`.
Official native references fetched 2026-09-25:

- <https://learn.chatgpt.com/docs/hooks>
- <https://learn.chatgpt.com/docs/config-schema.json>

The probes used seven model-backed main threads and one actual child. Three fault cases share
one exec thread, and missing-script plus shell coverage share another; they do not prove
fresh-session independence. A folder-trust screen and an invalid exec flag both failed before
thread creation. No transport, deployment, product source, commit, staging, or push occurred.

## Isolation and configuration

- Exec cases used `--ignore-user-config --ignore-rules --ephemeral`, `-C <fixture>`,
  `sandbox=workspace-write`, `approval_policy="never"`, inline hook config, and the native
  one-invocation `--dangerously-bypass-hook-trust`. Authentication came from the existing
  runtime. `HOME` remained `/home/hruzam`; `CODEX_HOME` remained unset/default.
- Interactive cases used a private PTY, `--no-daemon`, `-C <fixture>`, workspace-write,
  approval `never`, an inline hook, and invocation-level `hooks.state={...enabled=false}` for
  the three pre-existing lifecycle hooks. Their commands and state IDs are in each
  `logs/*.invocation.json`; no global hook command or credential is copied here.
- Interactive CLI has no `--ignore-user-config`. The fixture initially reached a folder-trust
  prompt. Supplying `projects={"<fixture>"={trust_level="trusted"}}` with `-c` bypassed the
  prompt, but Codex later **persisted that project entry into `~/.codex/config.toml`**. Thus the
  TUI isolation attempt was not persistence-safe. After all probes stopped, the lane removed
  exactly that fixture block and verified the fixture path absent from persisted config and
  hooks. Post-rollback hashes: `config.toml`
  `1d2e712c6393422e645ef8849c2aa24bf9192306cc5f8f8e02ab9c8470fc6358`;
  `hooks.json` `d3eee6d9c7dbd9a2daf5df1dded872347603c6ea55518e74000c7db39896bbe8`.
  The persistence side effect still means this mechanism cannot claim clean TUI isolation.
- Hook matcher was `^apply_patch$`; timeout was two seconds. `hook.py` logs native stdin before
  deciding. The disabled case added native `--disable hooks`. The missing case configured the
  literal nonexistent `/tmp/muticula-b0-codex-ki5dIN/does-not-exist.py`.

## Result matrix

| # | Mode / trigger | Observed result | Evidence |
|---|---|---|---|
| 1 | Interactive healthy: held then unheld `apply_patch` | Held call displayed `Blocked by hook` with fixture reason and did not mutate; unheld call succeeded in the same TUI. This distinguishes hook denial from sandbox/permission denial. | `logs/01-interactive.typescript`, `.hook-events.jsonl`, `.invocation.json` |
| 2 | Interactive parent spawns one worker; child patches held | One worker `agent_id=01a0d653-5337-74d1-bb86-d3c453c59def`; child call was denied. `SubagentStart` and child `PreToolUse` carried that `agent_id` and `agent_type=worker`; both used parent `session_id=01a0d653-4172-7c81-9133-823bac5c9847` and parent turn id, while `transcript_path` pointed at the child rollout. | `logs/02-child.typescript`, `.hook-events.jsonl`, `.invocation.json` |
| 3 | Exec; hook sleeps 5 s with timeout 2 s | **Fail open:** `held-timeout.txt` changed to `TIMEOUT_CASE`; file-change item completed. | grouped `logs/03-05-faults.*`; hook record `effective_mode=timeout`; invocation before/after hashes |
| 4 | Exec; hook exits 1 without decision | **Fail open:** `held-exit1.txt` changed to `EXIT1_CASE`; file-change item completed. | grouped `logs/03-05-faults.*`; `effective_mode=exit1`; hashes |
| 5 | Exec; hook emits `{this-is-not-json` | **Fail open:** `held-malformed.txt` changed to `MALFORMED_CASE`; file-change item completed. | grouped `logs/03-05-faults.*`; `effective_mode=malformed`; hashes |
| 6 | Exec; configured hook command does not exist | **Fail open:** `held-missing.txt` changed to `MISSING_CASE`. No fixture hook log exists because the script never ran. | grouped `logs/06-08-missing-shell.*`; invocation command and hashes |
| 7 | Exec; native `--disable hooks` | Hook did not run; no case event log exists; held mutation completed to `DISABLED_CASE`. | `logs/07-disabled.*`; invocation argv, JSONL and hashes |
| 8 | Exec; Bash redirection while guard matches only `apply_patch` | Outside guard coverage: `/usr/bin/zsh -c "printf 'SHELL_CASE\\n' > held-shell.txt"` exited 0 and changed the file. | grouped `logs/06-08-missing-shell.*`; command-execution JSONL and hashes |

Cases 3–6 produced no case-specific hook failure message in Codex exec JSONL or stderr; the
native file-change result and changed hash are the observable outcome. These results qualify a
synchronous advisory guard only. They do not prove strict all-writer coverage, atomic
reservations, product readiness, or a fail-closed policy boundary.

## Event and scope facts

- Actual payload event key is `hook_event_name`. `PreToolUse` includes `session_id`, `turn_id`,
  `tool_name`, `tool_use_id`, `tool_input.command`, cwd, model, permission mode and transcript.
- In the child case, both `SubagentStart` and child `PreToolUse` include `agent_id` and
  `agent_type`; the child reuses the parent session/turn coordinates.
- `apply_patch` coverage does not cover Bash redirection. The official hook guide also says
  `write_stdin` does not create another `PreToolUse`, so session continuation is not an event
  boundary.

## Fixture-preflight failures kept separate from runtime findings

1. `logs/preflight-interactive.*`: the draft guard checked `event`; actual stdin used
   `hook_event_name`, so both edits passed. This is a fixture bug.
2. `logs/preflight-substring-interactive.*`: a substring test for `held.txt` also matched
   `unheld.txt`, so both calls were denied. This is a fixture bug. The final guard uses an exact
   token boundary, and `logs/hook-smoke.jsonl` preserves held-deny/unheld-allow smoke inputs.
3. `logs/preflight-cli-parse.*`: the first exec wrapper used unsupported exec flag
   `--ask-for-approval`; Codex exited 2 before creating a thread. The final wrapper uses
   `-c approval_policy="never"`.

The exact scripts, prompts, native JSONL, PTY typescripts, invocations, before/after hashes and
final sentinels are all in this directory. Raw TUI transcripts include ANSI terminal control
bytes; their SHA-256 values are recorded in `MANIFEST.sha256`.
