# evidence — cost-free checks run on office, 2026-10-03 (supports trajectory.handoff.2026-10-03.md)

`host: office (hruzam-120922) — php74 present, valet present, RAM fingerprint = office, MACHINE_NAME=office`
`codex-cli: 0.159.3 · shim: ia-sync zsh/ai/tunnel-codex.{py,zsh,selftest.zsh} @ 5a0a59f, compose == live`
`quota spent: zero. No thread born, no table enabled, no deploy, no commit.`

## E1 — Cartan's commit claims, verified against history

| claim | observed |
|---|---|
| T1 docs in reposoma `fb0cb15` | yes — `res/settings.md` +14/−3, `res/user-run.md` +19/−5 |
| T1 host facts in ia-sync `5af457f` | yes — `AGENTS.md`, `.gitignore`, old `STATUS.md` (majkee's "home->office" sync commit) |
| vault untracking `d2f8734` | yes — both `tunnel*.state.json` deleted from index; rule still in `.gitignore` |
| last shim commit `5a0a59f` | yes — nothing after it touches `zsh/ai/tunnel-codex.*` |
| card now in `_cold-start/archive/` | yes; `card/` path absent. Not moved by this seat. |

## E2 — protocol surface regenerated on 0.159.3 (`codex app-server generate-json-schema`)

- `ThreadStartParams`: 15 fields — `approvalPolicy approvalsReviewer baseInstructions config cwd developerInstructions ephemeral model modelProvider personality sandbox serviceName serviceTier sessionStartSource threadSource`. (My 0.154.0 handoff said 16; treat that as a miscount — every field Protocol 1 needs is present.)
- `TurnStartParams`: 17 fields, now including `disabledPluginIds`; `effort`, `model`, `cwd`, `sandboxPolicy` all still per-turn.
- `SandboxMode` enum unchanged: `read-only | workspace-write | danger-full-access`.
- `WorkspaceWriteSandboxPolicy` knobs unchanged: `writableRoots excludeSlashTmp excludeTmpdirEnvVar networkAccess`.
- `thread/setName`, `thread/list`, `ThreadStartResponse.instructionSources` all present.

## E3 — `codex app-server --stdio -c …` acceptance (JSON-RPC `initialize` only)

```
baseline                                              HANDSHAKE-OK
-c model_reasoning_effort="low"                       HANDSHAKE-OK
-c sandbox_mode="workspace-write"                     HANDSHAKE-OK
-c sandbox_workspace_write.writable_roots=["~/.cache"] HANDSHAKE-OK
-c profile="x"   → rc=1  "legacy `profile = "x"` config is no longer supported; use `--profile x`"
```
Same shape as 0.154.0. NOT re-verified here: the `--profile`-does-not-apply-to-`app-server` string
(binary path differs on this install; not located). Acceptance at handshake ≠ a born thread
honouring the value — still unproven, see handoff §4.

## E4 — exit codes, live (`status` is zsh-local, no app-server spawn)

```
TUNNEL_CODEX_STATE=/nonexistent/dir/tunnel.state.json … status   → exit 10  (refused — no state file; run open --enable)
<no --state, no env> … status                                    → exit 13  (state-not-specified)
```
Cartan is right: explicit-but-missing path is **10**. The predecessor STATUS `recovery_probe` step (3)
reads 13 for that case — wrong.

## E5 — timeout path, from source (`zsh/ai/tunnel-codex.py`)

- `DEFAULT_TIMEOUT = float(os.environ.get("TUNNEL_CODEX_TIMEOUT", "120"))` (line 115) — the
  "configurable wait" that the 2026-09-10 observation lists as a v1 candidate already existed.
- Both wait loops compute `remaining = deadline - time.time()` and call `next_message(remaining)`
  (lines 289–292, 369–372). `next_message` raises `ProtocolError(f"timed out after {timeout}s …")`
  where `timeout` **is that remaining value** (lines 246–253).
- Therefore the 09-10 messages `timed out after 6.025s` / `27.18s` mean *≈114 s / ≈93 s had already
  elapsed*, not that the shim gave up after 6 s. Finding F1's magnitude was wrong; its direction
  (120 s < a web-search turn) stands.
- `main` maps `TunnelError → exc.exit_code` (line 743–745) and `ProtocolError` carries 30. Line 243
  swallows `ProtocolError` inside the unsolicited-server-request handler; whether the 09-10 runs
  exited 0 through that path or the observation misread the exit is **unverified** here.

## E6 — fixture selftest on office

`zsh ~/.config/zsh/ai/tunnel-codex.selftest.zsh` → `64/64 tunnel-codex self-tests passed`.
Gates wiring/logic only, not the live protocol (L8).

## E7 — host state relevant to Protocol 1

- No tunnel vault on office: `~/.local/state/tunnel/` absent (relocation never shipped);
  bed `tunnel-02-programmatic-scaling/` holds no `*.state.json`.
- Office runs a managed app-server **daemon** from a `0.160.0` package alongside the `0.159.3` CLI.
  The tunnel spawns its own `codex app-server --stdio` subprocess per verb and does not use that
  daemon — but two Codex releases are live on this host; L8 re-verification must name which one a
  given proof ran against.
- `~/.codex/thread-writer-locks/` is non-empty (interactive Codex activity on this host). Not
  inspected further; never to be touched (GUIDE §Limits, @Cartan 2026-09-03).

## E8 — predecessor STATUS statements that are stale (named, not obeyed)

| line | says | truth |
|---|---|---|
| `checkpoint:` | "No T-task started yet" | T1 ran 2026-09-18 and is committed |
| ledger T1 | "DONE … Uncommitted" | committed (`5af457f`, `fb0cb15`) |
| `worktree:` | HEAD `9f6ff85` / `5c796df` | office HEAD `2a8bc2a`; bed has untracked `raw/` (majkee's drawings) |
| `recovery_probe` (3) | exit 13 = no vault bound | 13 only when no path given; explicit missing path = 10 |
| `next:` | probe with `writable_roots=["<tmp dir>"]` | invalid probe — `/tmp` is default-writable under workspace-write |
