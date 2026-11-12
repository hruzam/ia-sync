# Claude-side programmatic channels: research note

2026-11-12 · trajectory (Claude Code 2.1.286 running) · sources: code.claude.com/docs/en/{headless, sessions,
cli-reference, cross-session-messaging, channels, agent-teams, hooks, hooks-guide, agent-sdk/streaming-input,
agent-sdk/sessions}, fetched 2026-11-12 by a docs subagent; local `claude --help` probe by trajectory.
Evidence note, not a VERDICT. Items marked *inference* are untested.

## Findings

| # | channel | status | what it gives | limit for us |
|---|---|---|---|---|
| 1 | **cross-session messaging** `ListAgents` / `SendMessage` | documented, GA Linux ≥2.1.224 | an idle recipient **starts a turn** with the message. Plain text, cannot approve permissions. Inbound gated by `crossSessionInbound` (accept/hold/refuse) | Claude↔Claude only. Tool not visible in this session's toolset (to verify) |
| 2 | session inbox socket `CLAUDE_CODE_MESSAGING_SOCKET` (+ `_TOKEN`) | partly documented: scripts/hooks may post; the auth line is documented, the payload is not | non-TTY doorbell into a live session | token exported only to that session's hooks/Bash children. An external Codex process has none. Do not share it via the public repo |
| 3 | `claude agents --json` | documented "for scripting; no TTY" | lists interactive and background sessions with **state** (`busy` / idle / `blocked`) | read-only. Replaces screen parsing for "is the Claude receiver idle?" |
| 4 | `claude -p --resume <id> "…"` | supported | appends a turn to the same transcript. Against a **background** session (`--bg`) it becomes its next turn | concurrent with a live TUI on a non-background session: no guarantee, treat as unsafe |
| 5 | `--input-format stream-json` / Agent SDK streaming input | supported | the intended programmatic session (long-lived, turns over stdin) | its own process. Does not attach to an existing TUI. FIFO feeding is *inference* |
| 6 | hooks `asyncRewake` (exit 2 wakes Claude, stderr → reminder) | documented | a TTY-free doorbell: a watcher hook on a FIFO | *inference*, untested. Must be started by a hook in the receiving session |
| 7 | agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) | experimental | lead ↔ teammates mailbox | one interactive lead only. Mailbox files are internal, never write them |
| 8 | Channels (MCP push, `--channels`) | research preview | event push into a session | allowlisted plugins, claude.ai auth |
| 9 | Remote Control | supported | remote driving | goes through Anthropic servers. Not a local channel |

## What it means for this trial

- **Codex → Claude** works today through tmux (3/3 in cycle 03). Native candidates: (4) only if the Claude seat runs as a
  background session; (6) an asyncRewake FIFO doorbell (needs a test); (2) no, because there is no token for an external process.
- **Claude → Codex** is the BLOCKED direction. Nothing on the Claude side solves it. It depends on what Codex offers inbound
  (app-server JSON-RPC, `codex queue`, Codex↔Codex messaging). That is cartan's research half.
- **Idle detection for a Claude receiver:** use (3) instead of footer parsing. This alone removes all three Claude-side refusals.
- **Claude ↔ Claude** (e.g. home↔office trajectories): (1) is the native answer, if the tool is enabled. It supersedes tmux for that pair.

## Open checks (cheap, next cycle)

1. Is `SendMessage`/`ListAgents` available to this seat (`/status` peer address, settings)? Test one Claude→Claude message.
2. asyncRewake FIFO doorbell: one SessionStart hook, one write, observe wake. Isolated session only.
3. `claude agents --json` state values while busy / idle / waiting-permission. Record the exact strings.
