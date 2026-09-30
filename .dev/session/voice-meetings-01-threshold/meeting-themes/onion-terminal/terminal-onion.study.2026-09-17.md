# The Terminal Onion — a layer map for observing agent CLI sessions

_Author: Nabla · 2026-09-17 · Released chapter by chapter on Majkee's request.
Substrate + architecture were buffered in voice; this is the condensation to disk._

**Purpose.** A cartography of everything between the kernel and an agent CLI (Claude Code and
its siblings), asking one question at every layer: *what can be observed here, how, and what has
already been lost by the time it arrives?* The map is the goal. Two things fall out of it as
byproducts: (a) a **lens rack** — a set of small observer processes, one per layer, arranged in
multiplexer panes; (b) a **context bus** between sessions that survives window shifts.

**Provenance flags** (project convention): `[MEASURED]` documented/verified behaviour ·
`[INFERRED]` reasoning from first principles · `[OPEN]` unresolved · `[NABLA]` my design opinion ·
`[VERIFIED 2026-09-17]` volatile fact checked against current docs today ·
`[TIMELESS]` UNIX/POSIX behaviour that does not change.

**Chapter plan**
- **0. The map** — the onion, the observability matrix, the three design rules _(released)_
- **1. Bedrock: kernel, processes, descriptors, PTY, signals** — where truth lives _(released)_
- 2. The multiplexer: session registry and survival layer (tmux, Zellij)
- 3. The vertical: how one byte and one signal travel through the stack, and where they die
- 4. The agent CLI: hooks, transcripts, session files — the semantic layer
- 5. The lens rack: architecture of the observer (stateless lenses, one stateful picker, JSONL truth)
- 6. The context bus: passing state between sessions as a byproduct of 4+5
- 7. Reading the board with an AI: filtered slices, not firehoses

---

## Chapter 0 — The map

### 0.1 The onion

Read top-down as "meaning → bytes → facts". Each layer only sees what the layer above it chose
to emit. Nothing is ever recovered going downward.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ L5  AGENT CLI  (claude, codex, gemini …)                                  │
│     semantic events: hooks, transcript JSONL, session state, subagents   │
│     ── richest layer; only one that knows WHAT happened ──               │
├──────────────────────────────────────────────────────────────────────────┤
│ L4  TERMINAL UI / RENDERER (the CLI's own TUI, Ink/ratatui/…)             │
│     turns semantic state into ANSI escape streams; meaning flattens HERE │
├──────────────────────────────────────────────────────────────────────────┤
│ L3  MULTIPLEXER  (tmux / zellij server)                                   │
│     owns sessions, panes, layout; outlives your window; holds the PTYs   │
├──────────────────────────────────────────────────────────────────────────┤
│ L2  PTY PAIR  (/dev/ptmx master ↔ /dev/pts/N slave) + line discipline     │
│     bytes only; ISIG turns ^C into SIGINT; no idea what output "means"    │
├──────────────────────────────────────────────────────────────────────────┤
│ L1  PROCESS TREE + FILE DESCRIPTORS                                       │
│     who spawned whom; what each one holds open (files, pipes, sockets)   │
├──────────────────────────────────────────────────────────────────────────┤
│ L0  KERNEL  (scheduler, signals, wait/exit status, /proc)                 │
│     liveness, death, exit codes — facts, never interpretation            │
└──────────────────────────────────────────────────────────────────────────┘
        ▲ your terminal emulator / phone client attaches at L3, sees L2 bytes
```

The mobile client (Termux, whatever holds the phone) is *not a layer*: it is a client of L3,
receiving the L2 byte stream. That is why it is invariant to window shifts — nothing below L3
knows the window exists. `[TIMELESS]`

### 0.2 The observability matrix

| Layer | What you can read | Push (reactive) or Pull (poll)? | What is already lost |
|---|---|---|---|
| L5 agent CLI | hook JSON on stdin, transcript JSONL, session dir, `stream-json` output | **Push** (hooks) + file tail | nothing — this is the source |
| L4 renderer | nothing directly; it is code inside the CLI process | — | intent (it only emits paint instructions) |
| L3 multiplexer | pane/session lifecycle, layout, rendered viewport (`zellij subscribe`, `tmux pipe-pane`, hooks) | Push (events) + Pull (`list-panes`) | semantics; you get *rendered lines* |
| L2 PTY | raw byte stream (via multiplexer or `script`/`ptrace`) | Push (read on master) | structure — everything is one byte stream; stdout/stderr already merged |
| L1 process/fd | `/proc/PID/{status,fd,fdinfo,cmdline,cwd,environ}`, `lsof`, `ss` | **Pull** (snapshot) + inotify/fanotify on files | causality (you see *that* a socket is open, not *why*) |
| L0 kernel | `SIGCHLD`, `wait4` status, `/proc/PID/stat`, `pidfd`, ptrace, eBPF | Push (signals, pidfd) + Pull | meaning entirely; only facts |

`[MEASURED]` for the L5 row — verified today against the Claude Code hooks reference (see
Chapter 4 for the full event list). `[TIMELESS]` for L0–L2.

### 0.3 Three design rules that fall out of the map `[NABLA]`

1. **Tap high where meaning still exists; tap low only for liveness and truth-checking.**
   The L5 `Stop` hook answers "the turn ended". `SIGCHLD` answers "the process died". These are
   different questions; never use one to approximate the other.
2. **Events are append-only facts; state is always a snapshot.** A hook event happened and will
   never change — stream it, append it. The process tree, open fds, layout — only ever true *now*
   — re-read on a tick, and if you want history, append the snapshot *as an event*.
3. **The JSONL lines are the truth; the board is a disposable projection.** (Your
   derived-is-disposable invariant, applied to observation.) Never let the UI become the store.

### 0.4 Two fresh findings that change the plan `[VERIFIED 2026-09-17]`

- **Zellij now has a top-level `zellij subscribe` command** that streams one or more panes'
  rendered viewport to stdout as raw text or NDJSON (`pane_update` / `pane_closed`), across
  sessions with `--session`. That is an L3 tap that already speaks line-oriented text — exactly
  the shape the lens rack wants. It does *not* give semantics (it is the viewport), but it gives
  a reactive pane-change doorbell with zero plumbing.
- **Claude Code hooks have grown to ~35 lifecycle events**, three cadences (per session, per turn,
  per tool call) plus standalone async events (`CwdChanged`, `FileChanged`, `SubagentStart/Stop`,
  `PreCompact/PostCompact`, `Notification`…). Every hook receives `session_id`, `cwd`,
  `transcript_path`, `permission_mode`, `hook_event_name` on stdin — and inside subagents also
  `agent_id`/`agent_type`. **Caveat:** the transcript file is written asynchronously and may lag;
  for the final assistant text use `last_assistant_message` on `Stop`, not the transcript.
  Hooks run *without a controlling terminal* (cannot write `/dev/tty`) — which is fine for us,
  they should only ever append to a file.

---

## Chapter 1 — Bedrock: kernel, processes, descriptors, PTY, signals

Everything in this chapter is `[TIMELESS]` POSIX/Linux behaviour unless flagged. No research was
burned on it; it does not change.

### 1.1 The process tree — who exists

Every process has a PID, a parent (PPID), a session (SID) and a process group (PGID). A terminal
session is literally a *session* in the kernel sense: `setsid()` creates it, and exactly one
process group in it is the **foreground** group of the controlling terminal. That is the whole
mechanism behind "^C kills the running command but not the shell".

Under a multiplexer the tree looks like this (real shape, PIDs invented):

```
systemd(1)
└─ zellij --server(4120)         ← the survivor; owns the PTY masters
   ├─ zsh(4133)                   pane 1, /dev/pts/3
   │  └─ claude(4201)             the agent CLI
   │     ├─ node … mcp-server(4230)   stdio MCP child, talks over pipes
   │     └─ sh -c "npm test"(4402)     a Bash-tool child, short-lived
   └─ zsh(4140)                   pane 2, /dev/pts/4
      └─ tail -F events.jsonl(4155)   a lens
zellij(4990) ── unix socket ──▶ zellij --server(4120)   ← your phone's attach client
```

Observation points:
- `/proc/PID/status` → `PPid`, `NSpid`, `Threads`, `SigCgt/SigBlk` (which signals it *catches*).
- `/proc/PID/stat` field 3 → state letter (`R S D Z T`), field 6 → session id, field 8 → tty_nr.
- `/proc/PID/cwd`, `/proc/PID/cmdline`, `/proc/PID/environ` (own user only).
- `ps -o pid,ppid,pgid,sid,tty,stat,comm --forest` gives the tree in one shot.

**The key problem Majkee named:** the raw tree is unreadable; the *filter* is the design. The
anchor is the L5 event: a hook gives you `session_id` + `cwd` + (implicitly) the CLI's own PID
via `$PPID` of the hook process. From that PID walk *descendants only*:

```sh
# descendants of $ROOT, one line each — the filtered slice an AI can actually read
descend() { echo "$1"; for c in $(pgrep -P "$1"); do descend "$c"; done; }
descend "$ROOT" | xargs -I{} sh -c 'printf "%s %s %s\n" {} "$(readlink /proc/{}/cwd)" "$(tr "\0" " " </proc/{}/cmdline | cut -c1-80)"'
```

Five lines instead of a hundred. `[NABLA]`

### 1.2 File descriptors — what each one is holding

`/proc/PID/fd/` is a directory of symlinks: `0 → /dev/pts/3`, `3 → socket:[81234]`,
`5 → pipe:[81250]`, `7 → /home/m/.claude/projects/…/transcript.jsonl`. `/proc/PID/fdinfo/N`
adds the current file offset (`pos:`) — which is how you can tell a writer is *actively
appending* to a transcript without reading the file.

This is the **discovery lens**. You do not know in advance what a CLI opens; you look at the
table and anything surprising becomes the next dedicated lens:

- `socket:[inode]` → resolve with `ss -xp` (unix) or `ss -tp` (tcp) → *that* is the MCP or
  API channel.
- `pipe:[inode]` shared by two PIDs → those two are talking; the pipe inode is the join key.
- a regular file under `~/.claude/` or `~/.config/…` opened `O_APPEND` → a log or transcript
  you can `tail -F` for free.
- `anon_inode:[eventpoll]`, `inotify` → the process is itself watching something.

Snapshot commands: `ls -l /proc/PID/fd`, `lsof -p PID`, `lsof -U` (all unix sockets),
`ss -xap`. Reactive alternative for *files*: `inotifywait -m` on the directory — that turns
"a new transcript appeared" into a push event.

Honest limits `[MEASURED]`: you see the *descriptor*, not the traffic. Reading actual bytes
through someone else's fd needs `strace -p PID -e trace=read,write` (ptrace; slows the target;
needs `ptrace_scope` permitting) or eBPF. Both are diagnostic tools, not lenses to leave running.

### 1.3 The PTY pair — the projection surface

A pseudo-terminal is two ends of one kernel object:

```
      (multiplexer / emulator)                          (shell, CLI)
  master fd  ◄── read: what the app wrote ──┐   ┌── /dev/pts/N  stdin/stdout/stderr
  /dev/ptmx  ── write: keystrokes ─────────►│ N │◄──────────────────────────────────
                                            └─┬─┘
                                    line discipline (N_TTY)
                          termios: ICANON, ECHO, ISIG, OPOST, ONLCR …
```

What the line discipline does to your data, and why it matters for observation:
- **ISIG**: byte `0x03` arriving on the master is *not delivered as a byte*; it is converted into
  `SIGINT` to the foreground process group. A control character became a signal. This is the
  first place in the stack where "data" turns into "event". (Interactive TUIs usually switch to
  raw mode and receive `0x03` as data instead — then *they* decide what ^C means.)
- **OPOST/ONLCR**: `\n` from the app becomes `\r\n` on the master. What you scrape is not what
  the program wrote.
- **stdout and stderr are the same fd target** (`/dev/pts/N`). By the time bytes reach the master
  they are one interleaved stream. The stdout/stderr distinction is *lost at L2* — you can only
  get it back by capturing above the PTY (pipes, `script`-style wrappers per stream) or from the
  program itself (L5).
- **ECHO**: keystrokes appear in the master's read stream because the tty echoed them, not
  because the program printed them. Scraped transcripts contain the user's input *once as echo*,
  which is not the same as knowing the program *received* it.

So the PTY is a **rendering surface**: what you read from the master is what a terminal would
*paint*. It is exactly as much "the process" as a photograph of a screen. `[TIMELESS]`

Where you can read it: the multiplexer already holds the master, so `tmux pipe-pane -o 'cat >>
pane.raw'` or `zellij subscribe --pane-id terminal_N` are the cheap taps. Below the multiplexer,
`script -f` and `ptrace`-based tools can interpose. Nobody else can read a master they do not
hold — the kernel does not broadcast tty traffic.

### 1.4 Signals — the doorbells the kernel actually rings

| Signal / event | Who sends | What it honestly tells you |
|---|---|---|
| `SIGCHLD` to parent | kernel, on child exit/stop/continue | "something happened to a child" — parent must `waitpid` to learn what |
| exit status via `wait4` | kernel | `WIFEXITED`+code, or `WIFSIGNALED`+signal — *how* it died |
| `SIGINT` / `SIGTERM` / `SIGHUP` | tty (ISIG), user, multiplexer on detach | intent to interrupt/terminate; the target may catch and ignore |
| `SIGWINCH` | tty on resize | the window changed — pure L2/L3 noise for observation, but proves the emulator↔pty link is alive |
| `SIGPIPE` | kernel, write to a closed pipe | the reader went away — a *death-of-consumer* signal |
| `pidfd_open` + poll `[Linux ≥5.3]` | kernel | a pollable fd that becomes readable when *that* PID exits — the clean way to watch a process you did not spawn |

Things the kernel will never tell you: that "output finished", that a prompt is waiting, that a
tool call started. Those are L5 facts. Rule 1 again.

Practical pattern: your lens for a pane you did not spawn is `pidfd` (or, in shell, `tail
--pid=PID -f /dev/null` which polls) plus reading `/proc/PID/stat` for the state letter.
For processes you *do* spawn from the rack, `trap CHLD` in the shell or `waitpid` in Rust — and
append the exit fact as an event line.

### 1.5 The vertical — one keystroke and one byte through the stack `[TIMELESS]`

Downward (input):
```
phone touch → Termux draws & emits byte → ssh/mosh → zellij attach client
→ unix socket → zellij server → write(master) → line discipline
→ (ISIG? → SIGINT to fg pgrp)  else → slave read() by claude → its TUI event loop
```
Upward (output):
```
claude write(1, "…")  → slave → OPOST → master read() by zellij server
→ zellij's own grid/terminal-state model (re-parses ANSI!) → repaint diff
→ unix socket → attach client → ssh → Termux renders
```
Note the middle: the multiplexer **re-parses** the escape stream into its own screen model and
re-emits *its* rendering. What your phone shows is a re-rendering of a rendering. Two layers of
projection, each lossy in its own way (scrollback limits, unsupported sequences). Any observer
placed at the phone sees the least; any observer at L5 sees the most. Chapter 3 will walk each
signal path in detail.

### 1.6 Chapter 1 verdict

- L0–L2 give **facts and bytes**, never meaning. `[TIMELESS]`
- The only L1 tool worth keeping *running* is the filtered descendant walk + fd snapshot on a
  tick; everything heavier (ptrace, eBPF) is a hand-held magnifier, not a lens in the rack.
  `[NABLA]`
- The stdout/stderr distinction and the "data vs signal" boundary are both decided *at the PTY*;
  if you need either, capture above it. `[TIMELESS]`

---

_Next release on request: Chapter 2 (multiplexer taps — `zellij subscribe`, plugin
`PaneUpdate`/`CommandPaneExited`, tmux `pipe-pane`/hooks/control-mode) or Chapter 4 (the full
Claude Code hook event catalogue and the transcript format, verified today). Say which._

---

## Chapter 4 — The agent CLI: hooks, transcripts, session files (the semantic layer)

_Released 2026-09-17, out of order on purpose: this is the only layer that knows **what** happened.
Verified against the Claude Code hooks reference today; other agent CLIs (Codex, Gemini) will get a
comparison table when we do them. Flag: `[VERIFIED 2026-09-17]` unless marked otherwise._

### 4.0 Bridge — why this chapter dissolves the older questions

In voice you asked: *can I catch text parts, events, interactions, instead of reading the PTY
transcript?* Chapters 0–1 said: below L5 there are only bytes and facts. This chapter is the
answer to "then where is the meaning?" — **the CLI hands it to you, on stdin, as JSON, at every
lifecycle point, before it is ever painted.** You do not scrape; you subscribe. Everything in
Chapters 1–3 becomes a *cross-check* on this stream, not a substitute for it.

### 4.1 The hook mechanism — what a hook physically is

A hook is a user-defined handler that Claude Code runs at a named lifecycle point. Five handler
types exist: `command` (shell), `http` (POST), `mcp_tool`, `prompt`, `agent`. For the lens rack
only `command` matters — it is a process that receives **JSON on stdin**, and speaks back via
**exit code + JSON on stdout**.

```
claude (L5)                         your hook (a lens)
  │ event fires, matcher matches
  ├── spawn: sh -c "hook.sh"  ──── stdin: {"session_id":…,"hook_event_name":…,…}
  │                                   │ append one line to events.jsonl
  │                                   │ exit 0   (no decision)  ← observer posture
  │◄── stdout JSON / exit 2 ───────── (exit 2 = block/veto; only for policy hooks)
  ▼ continues
```

Facts that shape the design:
- **No controlling terminal.** Hooks run in their own session; `/dev/tty` is unavailable. They
  cannot draw. They can only write files or talk to sockets. → *A hook is a sensor, never a UI.*
- **All matching hooks run in parallel**, one process each. → keep them tiny; `jq -c . >> file`.
- **Exit 0 + empty stdout = "I have nothing to say."** That is the observer's whole contract.
  Exit 2 blocks (where the event is blockable). Exit 1 is a *non-blocking error* that shows a
  notice in the transcript — so a buggy lens is visible but harmless.
- **Timeouts:** default 600 s for command hooks, lowered to 30 s on `UserPromptSubmit`, 10 s on
  `MessageDisplay`; `SessionEnd` hooks share a 1.5 s budget. A lens that appends a line never
  approaches these. `async: true` exists for anything longer.
- **Scope:** `~/.claude/settings.json` (all projects) / `.claude/settings.json` (project, commitable)
  / `.claude/settings.local.json`. Hooks from settings also fire inside **subagents**, carrying
  `agent_id` + `agent_type`.
- `/hooks` inside Claude Code is a read-only browser of what is configured — useful to verify
  the rack is wired.

### 4.2 The common envelope — every event carries this

| Field | Use for the rack |
|---|---|
| `session_id` | **the join key** for everything — directory name, filter for the process walk |
| `prompt_id` | per-turn UUID; correlates with OpenTelemetry `prompt.id` |
| `transcript_path` | where the JSONL lives → the file to `tail -F` / inotify |
| `cwd` | follows `cd` and worktrees (`${CLAUDE_PROJECT_DIR}` does *not* — it stays at start) |
| `scratchpad_dir` | the session's temp working dir — a place to watch for surprise files |
| `permission_mode` | `default`/`plan`/`acceptEdits`/`auto`/`dontAsk`/`bypassPermissions` |
| `effort` | `{level: low…max}` on tool-context events |
| `hook_event_name` | the event type — your lens's dispatch key |
| `agent_id`, `agent_type` | present only inside subagents — lets the board draw the subtree |

Plus the hook process's own `$PPID` = the CLI's PID `[INFERRED — POSIX; hook is a direct child
via sh -c, so the CLI PID is one or two hops up; verify with /proc/$PPID/comm]`. That is the
anchor for the Chapter 1 descendant walk. Nothing else on the system links "this pane" to "this
session_id" — **this is the seam where L5 meaning meets L1 facts.**

### 4.3 The event catalogue, grouped by what the rack should do with it

**Per session** — open/close the session directory
- `SessionStart` (matcher: `startup|resume|clear|compact|fork`) — may carry `model`
- `SessionEnd` (matcher: `clear|resume|logout|prompt_input_exit|other`)
- `Setup` (`--init`/`--maintenance`, CI only)

**Per turn** — the doorbell you asked for
- `UserPromptSubmit` — the human spoke; stdout here is *added to Claude's context*
- `UserPromptExpansion` — a slash command expanded
- `Stop` — **the honest end-of-turn**; carries `last_assistant_message`. Do **not** read the
  transcript for this: the file is written asynchronously and may lag the turn.
- `StopFailure` (matcher: `rate_limit|overloaded|authentication_failed|billing_error|
  server_error|max_output_tokens|…`) — output ignored except `terminalSequence`

**Per tool call** — the activity stream
- `PreToolUse` / `PostToolUse` / `PostToolUseFailure` — `tool_name`, `tool_input`, `tool_use_id`;
  matcher on tool name, `if` filter on arguments (`Bash(git *)`, `Edit(*.ts)`)
- `PostToolBatch` — a parallel batch resolved, before the next model call
- `PermissionRequest` / `PermissionDenied` — the CLI is *waiting on the human* / auto-denied
- MCP tools appear as `mcp__<server>__<tool>`; `mcp__.*` catches all of them

**Structure changes** — redraw the tree
- `SubagentStart` / `SubagentStop` (matcher: agent type)
- `TaskCreated` / `TaskCompleted`, `TeammateIdle` (agent teams)
- `WorktreeCreate` / `WorktreeRemove`
- `CwdChanged`, `DirectoryAdded`, `FileChanged` (matcher = literal filenames to watch)

**Context lifecycle** — the memory events
- `PreCompact` / `PostCompact` (matcher: `manual|auto`) — **this is where context is lost**; the
  rack should log it loudly. Directly relevant to the context bus (Chapter 6).
- `InstructionsLoaded` (matcher: `session_start|nested_traversal|path_glob_match|include|compact`)
  — which CLAUDE.md / rules entered context, and when
- `ConfigChange`, `PreModelSwitch` / `PostModelSwitch` (from_model → to_model)

**Display / attention**
- `Notification` (matcher: `permission_prompt|idle_prompt|agent_needs_input|agent_completed|…`)
  — the CLI *wants a human*; this is the one you route to the phone
- `MessageDisplay` — fires while assistant text streams; 10 s timeout; display-only
- `Elicitation` / `ElicitationResult` — an MCP server asked the user something

Three cadences, ~35 events. For a first rack: `SessionStart`, `SessionEnd`, `UserPromptSubmit`,
`Stop`, `PreToolUse`, `PostToolUse(Failure)`, `SubagentStart/Stop`, `Notification`,
`PreCompact/PostCompact`. Ten. `[NABLA]`

### 4.4 The universal lens hook — one script, every event

```json
{ "hooks": {
    "SessionStart": [{"hooks":[{"type":"command","command":"~/.rack/lens-append.sh","args":[]}]}],
    "Stop":         [{"hooks":[{"type":"command","command":"~/.rack/lens-append.sh","args":[]}]}],
    "PreToolUse":   [{"hooks":[{"type":"command","command":"~/.rack/lens-append.sh","args":[]}]}]
    /* … repeat per event; matcher omitted = fire on all */
}}
```

```sh
#!/bin/sh
# ~/.rack/lens-append.sh — the only writer of this session's event file (one-writer invariant)
in=$(cat)
sid=$(printf '%s' "$in" | jq -r .session_id)
d="$HOME/.rack/sessions/$sid"; mkdir -p "$d"
printf '%s' "$in" | jq -c --arg ts "$(date -u +%FT%TZ)" --arg pid "$PPID" \
   '. + {ts:$ts, cli_pid:$pid}' >> "$d/events.jsonl"
exit 0
```

Exec form (`"args": []`) so no shell re-parses the path. Exit 0, empty stdout: the CLI never
learns the lens exists. Everything else in the rack is a *reader* of `events.jsonl`.

### 4.5 The transcript — the other file, and why it is second

`transcript_path` points at `~/.claude/projects/<cwd-slug>/<session>.jsonl`. It is the full
conversation as one JSON object per line (user/assistant messages with `uuid`, `parentUuid`,
`sessionId`, `timestamp`, tool_use / tool_result blocks) `[INFERRED · training-era — shape known,
exact field names not re-verified today; treat as "inspect before parsing"]`.

Why it is the *second* source, not the first:
1. **It lags.** Documented: written asynchronously; may not contain the current turn when a hook fires.
2. **It is a braid you did not weave.** Subagents get their own transcripts; `stream-json`
   (`claude -p --output-format stream-json`) is a *third* representation. The docs warn not to
   mix them up.
3. **It is Anthropic's file.** Format can change under you; your `events.jsonl` cannot.

Use it for what hooks do not carry: full assistant text mid-turn, token/usage fields, replay.
Tap it with `tail -F` (survives rotation) or `inotifywait -e modify`. Never let a lens *write* it.

### 4.6 What the CLI still does not tell you — the residual for L0–L3

- **Is the process alive right now?** Hooks are silent when the CLI hangs, is `kill -9`'d, or the
  API stalls. → `pidfd` / `/proc/PID/stat` (Ch. 1).
- **What is it holding open?** MCP sockets, scratch files, the API connection. → fd snapshot (Ch. 1).
- **Which pane, which window?** Hooks know `session_id`; only the multiplexer knows `pane_id`.
  The bridge is the PID: multiplexer `list-panes -F '#{pane_pid}'` ↔ hook `$PPID` ancestry. (Ch. 2)
- **What did the human actually see?** Only the rendered viewport knows — `zellij subscribe`. (Ch. 2)

That residual is the *entire* justification for the lower lenses. Not more.

### 4.7 Chapter 4 verdict

- The CLI is a **push source of typed events with a stable join key.** Scraping the PTY for
  semantics is now strictly worse than subscribing. `[VERIFIED 2026-09-17]`
- The observer contract is one sentence: *read stdin, append a line, exit 0, say nothing.* `[NABLA]`
- `Stop` + `last_assistant_message` is the end-of-turn doorbell; `SIGCHLD`/`pidfd` is the
  death doorbell; the transcript is neither. Rule 1 from Chapter 0, now with named sources.
- `PreCompact`/`PostCompact` are the events the context bus will be built around — the only
  moment the CLI tells you *memory is about to be lost*.

---

## Chapter 2 — The multiplexer: session registry and survival layer

_Released 2026-09-18. tmux material is `[TIMELESS]` (stable for a decade+); Zellij material is
`[VERIFIED 2026-09-17]` where it says so and `[OPEN]` where I could not confirm._

### 2.0 What the multiplexer is, in one sentence

A **detached server process that owns the PTY masters** and lets any number of clients attach,
detach, and reattach to a screen model it maintains itself. Everything else — panes, tabs,
layouts — is bookkeeping around that one fact.

```
                 ┌──────────────── server (survives) ────────────────┐
  client A ──uds─┤  session "larva"                                   │
  (desktop)      │   ├─ tab 1 ─ pane terminal_1  ── master ── pts/3 ─ zsh ─ claude
  client B ──uds─┤   │        └ pane terminal_2  ── master ── pts/4 ─ zsh ─ tail -F …
  (phone/ssh)    │   └─ tab 2 ─ pane plugin_3    (a Zellij plugin = WASM, no PTY)
                 │  screen model: grid per pane, scrollback, cursor, title             │
                 └───────────────────────────────────────────────────┘
```

Consequences you get for free `[TIMELESS]`:
- **Window-shift invariance.** Clients are ephemeral; the process tree hangs off the server.
  Closing the phone client changes nothing below the socket.
- **Two clients, one truth.** Both see the same screen model; a resize on one may resize the
  other (tmux: smallest client wins unless `window-size` says otherwise).
- **The server is the only holder of the master fd.** Any byte-level tap goes *through* the
  server's API, or it does not exist.

### 2.1 What the multiplexer knows — and does not

| It knows | It does not know |
|---|---|
| pane ↔ tty (`/dev/pts/N`) ↔ the *shell's* PID it spawned | the CLI's `session_id` |
| pane title, current command name (from the fg process) | what a tool call is |
| the rendered grid + scrollback per pane | stdout vs stderr (merged at L2) |
| pane opened / exited / closed, exit status | why it exited |
| which clients are attached, from where | who the human is |

So the multiplexer is the **registry** (which panes exist, which is alive, which is attached) and
the **viewport source** (what the human actually saw). It is *not* the semantic source. Chapter
0, rule 1.

### 2.2 The PID ↔ pane bridge — closing Chapter 4's open seam

Two identities must be joined: the CLI's `session_id` (L5, from hooks) and the pane (L3). There is
no shared key. The join goes through the kernel, twice:

```
hook stdin ─▶ session_id                    multiplexer ─▶ pane_id
hook $PPID ─▶ …ancestry… ─▶ claude PID      pane_pid (tmux) = the shell PID
readlink /proc/<claude>/fd/0 ─▶ /dev/pts/N  #{pane_tty} (tmux) = /dev/pts/N
                    └────────── join on pts/N, or on "claude PID is a descendant of pane_pid" ──┘
```

**tmux** exposes both sides directly `[TIMELESS]`:
```sh
tmux list-panes -a -F '#{session_name} #{window_index}.#{pane_index} #{pane_id} #{pane_pid} #{pane_tty} #{pane_current_command}'
```
From the hook side: `readlink /proc/$PPID/fd/0` (or walk up until `comm` = `claude`), then match
`pane_tty`. One `join` on the tty string. Robust across restarts because the tty is assigned by
the kernel at pane creation and never changes for the pane's life.

**Zellij** `[VERIFIED 2026-09-18]` — resolved, and simpler than tmux: every terminal pane
exports **`$ZELLIJ_PANE_ID`** (and `$ZELLIJ_SESSION_NAME`) into its shell's environment. The CLI
inherits it; the hook inherits it from the CLI. So the hook already *holds* the join key:

```sh
# inside lens-append.sh — no discovery, no tty scan
jq -c --arg pane "terminal_${ZELLIJ_PANE_ID:-?}" --arg zs "${ZELLIJ_SESSION_NAME:-?}" \
   '. + {pane_id:$pane, zellij_session:$zs}'
```
On the registry side, `zellij action list-panes --json` returns per pane `id`, `is_plugin`,
`is_focused`, `title`, `tab_id`, `tab_name`, `pane_command`, `pane_cwd` (+ geometry). Join on
`terminal_<id>`. `PaneInfo` in the plugin API carries the same identity fields but no PID/tty —
you do not need them.

Edge `[INFERRED]`: a CLI started *outside* the pane's shell (e.g. `zellij run -- claude` as a
command pane) should still carry the var since the server sets it per pane; verify once with
`env | grep ZELLIJ` from a hook. If a pane is missing it, fall back to naming the pane at launch.

**Verdict:** on tmux the bridge is a format string; on Zellij it is `$ZELLIJ_PANE_ID`. Either
way the rack never *guesses* the pane from viewport text.

### 2.3 Taps — reactive vs polled, per multiplexer

**tmux** `[TIMELESS]`
- `pipe-pane -o 'cat >> $d/pane.raw'` — copies the pane's *output* byte stream (post-line-
  discipline, pre-render) to a command. Reactive, cheap. The only place below L5 to get the raw
  escape stream.
- `set-hook -g pane-died / pane-exited / window-linked / client-attached / client-detached
  'run-shell "…"'` — lifecycle doorbells. Reactive.
- `tmux -CC` control mode — a *client* that receives the server's events as a text protocol
  (`%output %pane-id …`, `%window-add`, `%exit`) on stdout. This is the closest tmux has to
  `zellij subscribe`; one process, all panes, line-oriented. Reactive.
- `capture-pane -p -S -` — the rendered grid + scrollback. Polled.
- `wait-for` — a named signal channel *between* shell scripts via the server; a free
  synchronisation primitive for lenses that must not overlap.

**Zellij**
- `zellij [--session S] subscribe --pane-id terminal_N --format json` — NDJSON stream of
  `pane_update` (full viewport on change, `is_initial` on first delivery) and `pane_closed`.
  Cross-session. Exits when all subscribed panes die. `[VERIFIED 2026-09-17]` This is the
  reactive viewport tap.
- Plugin API events `[VERIFIED 2026-09-17]` (WASM plugin, `subscribe(&[EventType::…])`,
  permission `ReadApplicationState`): `PaneUpdate(PaneManifest)`, `TabUpdate`, `SessionUpdate`,
  `CommandPaneOpened/Exited`, `PaneClosed`, `CwdChanged`, `PaneRenderReport`, `ListClients`,
  `FileSystemCreate/Update/Delete` (in the Zellij cwd), `RunCommandResult`. A plugin is the
  *in-process* registry — but it is a Rust→WASM build, which is Phase C weight. For the first
  rack, `subscribe` + `zellij action list-clients`/`dump-screen` polling is enough. `[NABLA]`
- `zellij pipe` — a message bus *into* plugins from the CLI. Not an observation tap; a control one.
  Keep it out of the read-only board.

### 2.4 What the viewport tap is good for — and the trap

`subscribe`/`pipe-pane`/`-CC` give you **what the human saw**. Legitimate uses:
- the *display lens*: a compact mirror of a pane on the phone without attaching to it;
- **spinner/idle detection** when a CLI emits no hook (Codex, a plain build) — "viewport
  unchanged for N s while the process is alive" is a real signal, assembled from L3 + L1;
- forensic replay of a session where hooks were not yet wired.

The trap: parsing viewport lines for *semantics* ("it printed `✔ Done`") is regex over paint.
It breaks on the first UI change and it cannot see stderr. If you catch yourself writing that
regex for a CLI that has hooks, stop — Chapter 4 already has the event.

### 2.5 The multiplexer as the rack's *host*, not just a source

Two roles, do not conflate them:
- **Source**: the session panes it observes (registry + viewport).
- **Host**: the panes the lenses *run in*. A layout file (`tmux` script / Zellij KDL) that opens
  `events` / `tree` / `fds` / `viewport` panes side by side is the "app". No framework.

One rule `[NABLA]`: the rack's own panes must be **in a different session (or at least a
different tab)** from the observed ones, so that a lens crashing, resizing, or being closed never
touches the observed pane's tty. Same server is fine; same window is not.

### 2.6 Chapter 2 verdict

- Multiplexer = registry + viewport + survival. Never semantics. `[TIMELESS]`
- The session↔pane join runs through the kernel (`pane_tty`/`pane_pid`) on tmux; on Zellij it is
  an inherited environment variable (`$ZELLIJ_PANE_ID`). Zellij is the easier target here.
  `[VERIFIED 2026-09-18]`
- Reactive taps exist on both (`-CC`, hooks, `subscribe`); the first rack needs only
  `subscribe` (or `pipe-pane`) + a polled `list-panes`. `[NABLA]`

---

## Chapter 5 — The lens rack: architecture, language, routing

_Released 2026-09-18. This is Phase B (bare-metal architecture), not Phase C: shapes, data flow,
invariants, and the language argument. No implementation code beyond illustrative lines.
Flag `[NABLA]` throughout unless stated — this chapter is opinion with reasons; kick it._

### 5.0 The shape in one picture

```
 OBSERVED (Zellij session "work")             RACK (Zellij session "rack", separate)
 ┌───────────────────────────┐                ┌───────────────────────────────────────┐
 │ pane terminal_1: claude   │─hook stdin──▶  │ lens-append.sh  (per event, exits)     │
 │ pane terminal_2: codex    │                │        │ append                          │
 │ pane terminal_3: build    │                │        ▼                                │
 └───────────┬───────────────┘                │ ~/.rack/sessions/<sid>/events.jsonl    │◀─┐
             │ zellij subscribe (viewport)     │ ~/.rack/sessions/<sid>/tree.jsonl      │  │
             │ zellij action list-panes --json │ ~/.rack/sessions/<sid>/fds.jsonl       │  │
             │ /proc walk anchored on cli_pid  │ ~/.rack/sessions/<sid>/view.ndjson     │  │
             ▼                                │        ▲ writers: one lens per file     │  │
       polled lenses (tick)  ─────────────────┘        │                                │  │
                                              │  ┌─────┴──────┐   ┌──────────────────┐ │  │
                                              │  │ rack-board │◀──│ rack-pick (state)│─┘  │
                                              │  │ (render)   │   │ writes selected  │    │
                                              │  └────────────┘   └──────────────────┘    │
                                              │  detail panes: tail -F ... | jq filter ◀──┘
                                              └───────────────────────────────────────┘
```

Four component classes, and only four:
1. **Sensors** — hook scripts. Spawned by the CLI, append one line, exit. Zero residency.
2. **Pollers** — `tree`, `fds`, `registry`, `view`. Long-running loops; each owns one file.
3. **Readers** — `tail -F | jq` pipelines rendering into panes. Stateless, killable, restartable.
4. **The picker** — the single stateful process. Holds "what is selected", publishes it as a file.

Everything is a process that reads text and writes text. The multiplexer layout is the "app".

### 5.1 Routing = the filesystem

There is no message broker, no socket server, no registry service. Routing is *where a file is*:

```
~/.rack/
├── sessions/
│   └── <session_id>/            ← keyed by the L5 join key
│       ├── meta.json            ← pane_id, zellij_session, cwd, cli_pid, started (written once by SessionStart)
│       ├── events.jsonl         ← sensor output, append-only, THE truth
│       ├── tree.jsonl           ← poller snapshots-as-events: {ts, pids:[…]}
│       ├── fds.jsonl            ← poller snapshots: {ts, pid, fds:[…]}
│       └── view.ndjson          ← zellij subscribe passthrough (viewport)
├── selected                     ← picker output: one line, "<session_id> <lens> [pid]"
└── lenses/                      ← the rack's own programs (versioned in git)
```

Routing rules:
- **Sensor → file**: by `session_id` from stdin. Directory creation is the sensor's only side effect.
- **Poller → file**: one poller per lens type per *session*, started by the board when a new
  session directory appears (inotify on `~/.rack/sessions/`). A poller reads `meta.json` for its
  anchor (`cli_pid`, `pane_id`) and never guesses.
- **Reader ← file**: readers watch `selected`; when it changes they re-exec themselves against the
  new path. A reader is `exec tail -F "$dir/$lens.jsonl" | jq -r "$FILTER"` — its whole state is
  its argv.
- **Cross-session** (the context bus, Ch. 6): a reader that tails *two* session dirs. Routing is
  a glob. Nothing new.

Why this beats a broker: every hop is inspectable with `cat`, every producer can be replaced by
`echo`, and a crash loses nothing because the files are the state. Your one-writer-per-file
invariant is satisfied structurally — each file has exactly one process class that appends.

### 5.2 Events vs snapshots — the two line shapes

Two record kinds only, both NDJSON, both with `ts` first:

```json
{"ts":"…","kind":"event","src":"hook","hook_event_name":"PreToolUse","session_id":"…","pane_id":"terminal_1",…}
{"ts":"…","kind":"snap","src":"tree","session_id":"…","pids":[{"pid":4201,"comm":"claude","cwd":"…"},…]}
```

`event` lines are facts and are never rewritten. `snap` lines are the poller's answer to "what was
true at `ts`" — also never rewritten, because *that it was true at ts* is itself a fact (Ch. 0
rule 2). A board that wants "current state" reads the **last** `snap` line; one that wants history
reads them all. Same file, two projections, no schema change.

Diffing is a *reader* concern: `jq -s 'map(.pids|map(.pid)) | [.[-2], .[-1]] | …'` shows what
appeared/vanished between the last two ticks. The poller stays dumb.

### 5.3 Language — the argument, not just the verdict

| Component | Language | Why, and why not the alternative |
|---|---|---|
| Sensors | POSIX sh + jq | Must start in ms, run in parallel, never need a runtime. A Rust binary here is *fine* but buys nothing; Python costs 30–80 ms per fire × every event. |
| Pollers | sh + jq (+ `zellij`, `pgrep`, `readlink`) | They're glue over `/proc` and CLI JSON. When one needs real parsing (e.g. `TIOCGPTN`), it becomes a Rust helper *for that one job*. |
| Readers | `tail`/`jq`/`awk` | They are the UNIX pipeline. Replaceable per pane, per whim. |
| Picker + board | **Rust** | The only stateful piece; wants a real event loop (`inotify` + stdin keys), a proper TUI grid (ratatui or plain ANSI), a single static binary that runs on the phone under Termux. Not Python: no venv, no startup, no GIL surprises with inotify. Not Go: fine, but you already think in Rust and the Zellij plugin path (5.6) is Rust anyway. Not JS: nothing here is a browser. |

The rule that produced the table: **a language earns its place only when a component needs
residency or a grid.** Everything else is text through pipes.

Rejected outright, with reasons:
- **A daemon "rackd"** that all lenses talk to → recreates a broker, reintroduces a single writer
  bottleneck, and makes `cat` useless. The filesystem already is the daemon.
- **SQLite as the store** → derived-is-disposable says fine *as an index*, but not as the store;
  add it later as a reader that ingests JSONL, if querying ever needs it.
- **A full TUI framework for all panes** → one stateful pane, not five. The multiplexer is the
  window manager; don't build a second one inside a pane.
- **Sublime / an editor as the board** → an editor owns the window; here the multiplexer must.
  (Sublime *is* a good `events.jsonl` reader, though — open the file, syntax-highlight JSON, done.)

### 5.4 The picker — designing the one stateful thing

Responsibility: hold `(session_id, lens, optional pid)`, react to keys, publish to `~/.rack/selected`
atomically (`tmp` + `rename`, your two-simplex commit). Nothing else.

```
 keys: j/k move · Enter drill (session → lens → pid) · Esc up · r refresh registry
 inputs: ~/.rack/sessions/*/meta.json (registry), last snap of tree.jsonl (pids)
 output: ~/.rack/selected   (one line, rewritten atomically)
 side effects: none — detail panes react to `selected` via inotify and re-exec
```

Why publish via file instead of signalling readers directly: readers then need *no* knowledge of
the picker's existence; a reader is testable with `echo "sid tree 4201" > ~/.rack/selected`.
And the picker can die and restart without anyone noticing — its state is one line on disk.

Tension I'm not hiding `[OPEN]`: drill-down into *live* things (a pid's fd table) means a detail
pane that re-polls on select. That's a poller spawned on demand, i.e. the picker or board must
spawn processes. Keep that in the board (Rust), not the picker; the picker stays a pure
"write selection" program. Split them if it keeps the picker under ~300 lines.

### 5.5 Extensibility — adding a lens for an unknown stream

The discovery loop, as a procedure:
1. `fds` snap shows `socket:[81234]` on `claude` you can't account for.
2. `ss -xp | grep 81234` → it's the MCP server stdio? No — it's a unix socket to `~/.something/ipc`.
3. Write `lenses/ipc-tail.sh`: `socat -u UNIX-LISTEN…` or `strace -e read -p PID` for *one look*.
4. If it earns permanence: it becomes `ipc.jsonl` in the session dir, one more `--lens` name the
   picker offers, one more pane in the layout. Nothing in the core changes.

A lens is "a program that writes `<name>.jsonl` into a session dir". That's the plugin interface.
No registration, no schema beyond `ts` + `kind`.

### 5.6 The Zellij-plugin path (later, not first)

Everything above works with Zellij as a *host* and `subscribe`/`list-panes` as *taps*. A WASM plugin
(Rust, `zellij-tile`) would give the board an in-process registry via `PaneUpdate` and a native
pane instead of a Rust TUI in a terminal pane. Do it **only** if polling `list-panes` proves too
coarse or the board wants Zellij-native focus/highlight. It changes nothing in the file layout — the
plugin would be one more writer of `registry.jsonl`. Phase C+1, not Phase C.

### 5.7 Weight

- Sensors: 1 script, ~15 lines. Hook config: ~40 lines of JSON.
- Pollers: 3 scripts (`tree`, `fds`, `view`), ~30 lines each.
- Layout: 1 KDL file, ~40 lines.
- Picker: Rust, ~300 lines. Board: Rust, ~400 lines (or `jq`+`watch` for v0 and skip Rust entirely).
- **v0 without any Rust: an afternoon.** v1 with picker+board: a weekend.

### 5.8 What can still go wrong `[NABLA — honest list]`

- **File growth.** `events.jsonl` for a long session is tens of MB. Readers `tail`, so it's fine;
  rotation is `SessionEnd` → `mv` to `archive/`. Never truncate a live file.
- **Hook parallelism.** Two hooks appending to the same file from parallel processes: `O_APPEND`
  writes under `PIPE_BUF` (4 KiB) are atomic on Linux; a single `jq -c` line is under that. Lines
  over 4 KiB (huge `tool_input`) *can* interleave. Either truncate `tool_input` in the sensor or
  write per-hook files and merge on read. Decide in Phase C.
- **Transcript lag** (Ch. 4) — never let a reader treat the transcript as current.
- **Phone.** Termux runs `tail`, `jq`, a static Rust binary. It does not run a WASM Zellij plugin
  from your laptop. The file-based design is what keeps the phone a first-class reader.
- **Non-hook CLIs** (Codex, plain builds): only L1–L3 lenses. Idle/spinner detection from
  viewport-unchanged + process-alive is the best you get. Accept it; don't regex the paint.

### 5.9 Chapter 5 verdict

- Four component classes; the filesystem is the router; one stateful process. `[NABLA]`
- sh+jq everywhere except the grid; Rust for the grid. No daemon, no broker, no DB-as-store.
- v0 is buildable today with zero compilation. That's the Phase C entry point.

---

## Chapter 3 — The vertical: how one byte and one signal travel, and where they die

_Released 2026-09-18. Almost entirely `[TIMELESS]`; this is the connective tissue you said you
lost in voice. Read it as a set of traces, each one a single thing crossing the stack._

### 3.0 The rule of the vertical

Going **down** (kernel → CLI), data gets *typed*: bytes become signals, signals become events,
events become meaning. Going **up** (CLI → screen), data gets *flattened*: meaning becomes paint.
The stack is not symmetric. Observation must enter at the point where the thing you care about
still has its type. `[TIMELESS]`

### 3.1 Trace A — a keystroke `^C` from the phone

```
1. Termux: touch → byte 0x03 → local pty → ssh/mosh client → TCP
2. sshd → zellij attach client (a process on your host) → unix socket → zellij server
3. zellij server: write(master_fd, "\x03")
4. line discipline (N_TTY) on pts/N:
     ├─ if ISIG && c_cc[VINTR]==0x03 && !raw:  kill(-fg_pgrp, SIGINT); byte DROPPED
     └─ if raw mode (TUI):                      byte delivered to slave read()
5a. SIGINT path: every process in the foreground pgrp gets it.
     - claude's TUI (raw mode) usually never takes 5a; it takes 5b.
     - a `sh -c "npm test"` child spawned by claude IS in some pgrp — which one depends on
       whether claude called setpgid for it. [INFERRED — check /proc/<child>/stat pgid]
5b. raw path: claude's event loop reads 0x03, decides: cancel turn / second ^C exits.
     → emits (maybe) a `Stop`-class hook, or a `SessionEnd` with reason … 
```
Where it dies: at step 4 the byte either becomes a signal or stays a byte; **you cannot observe
which from outside the process** — only `stty -a < /dev/pts/N` tells you the current mode.
Observable downstream: `SessionEnd`/`Stop` hook (L5) or `SIGCHLD` in the shell (L0). `[TIMELESS]`

### 3.2 Trace B — a line of assistant output

```
1. claude: has a semantic thing: {type:"text", content:"…"}   ← meaning exists here
2. its renderer (Ink/ratatui-class): diff → "\x1b[3;1H\x1b[2K…text…"   ← meaning gone, paint remains
3. write(1, buf)  →  slave /dev/pts/N  →  OPOST: "\n"→"\r\n"
4. master read() by zellij server → *its* vt parser → grid cells updated
5. zellij: (a) emits `pane_update` to `subscribe` clients — full viewport text
           (b) diff-renders to attached clients → unix socket → ssh → Termux vt parser → pixels
```
Same content, five representations: struct → escape stream → cooked bytes → grid → pixels.
Observation points and what they carry:
- L5 hook `MessageDisplay` (streaming) / `Stop.last_assistant_message` (final): **the struct**.
- L2 via `pipe-pane`: **the escape stream** (only tmux exposes raw; Zellij gives step 5a's grid).
- L3 via `subscribe`: **the grid as text** — what a human would read, minus color.
- Phone: pixels. Nothing to tap.

### 3.3 Trace C — a tool call (`Bash`) end to end

```
model → tool_use block → claude: PreToolUse hook ──(exit 0)──▶ fork/exec sh -c "…"
   ├─ child fds: 0←/dev/null or pipe, 1→pipe, 2→pipe  (NOT the pty: claude captures output)
   ├─ child runs; kernel: new PID, pgid; /proc appears        ← tree lens sees it here
   ├─ child exits → SIGCHLD → claude waitpid → exit status
   └─ claude: PostToolUse (or PostToolUseFailure) hook with tool_response
model ← tool_result
```
Important: the tool's stdout **never touches the pty**. It goes into a pipe held by claude, is
captured, and appears on screen only as the CLI's *rendering* of it. So the viewport lens sees a
truncated, formatted echo; the `PostToolUse` hook sees the real `tool_response`; the fd lens sees
the pipe while it exists. Three different truths — pick by question. `[MEASURED]` for the hook
side; `[INFERRED]` for the exact fd wiring (verify with `ls -l /proc/<child>/fd` during a slow tool).

### 3.4 Trace D — a hook's own signal path (why it can't draw)

```
claude: fork → setsid()? (own session, no ctty) → exec sh -c hook.sh
  fds: 0 = pipe (JSON), 1 = pipe (read back), 2 = pipe (shown as notice on exit 1)
  no /dev/tty → open("/dev/tty") fails → any TUI attempt dies
  timeout → SIGKILL from claude (600 s default)
```
`[MEASURED]` (docs: no controlling terminal). Consequence for the rack: a hook that wants to
*notify the phone* must write a file or hit a socket; it cannot ring a bell in a pane. The bell is
a reader tailing `events.jsonl` for `Notification`.

### 3.5 Trace E — a detach / window shift

```
Termux app backgrounded → TCP idles → (mosh: nothing; ssh: eventually dies)
sshd child exits → zellij attach client gets SIGHUP → exits
zellij server: client removed; panes untouched; no signal reaches pts/N
claude: sees nothing. A SIGWINCH may arrive later when a smaller client attaches.
```
The only process that ever learns you left is the attach client. That is the whole proof of
window-shift invariance, and why the rack must never run *inside* the attach client's process
tree. `[TIMELESS]`

### 3.6 Trace F — a compaction (memory loss, from the inside)

```
context near limit → claude: PreCompact hook {trigger:"auto"|"manual"}   ← last moment full context exists
  → summarisation call → new context
  → PostCompact hook
  → transcript continues (new lines reference the summary)
```
Nothing in L0–L3 moves. No signal, no fd change, no viewport event beyond a status line. This is
the clearest case of "meaning exists only at L5": the most important state transition in an
agent session is invisible to every lower lens. Chapter 6 is built on this trace. `[VERIFIED
2026-09-17]` for the hook names.

### 3.7 The lossy-point table

| Boundary | What is lost crossing it | Recover by |
|---|---|---|
| CLI struct → renderer | type, structure, tool/result linkage | hooks / stream-json |
| renderer → pty (OPOST) | exact bytes (`\n`), stdout/stderr split | capture above pty (pipes) |
| pty → multiplexer grid | escape sequences, scrollback beyond limit, colors (in `subscribe`) | tmux `pipe-pane` raw |
| multiplexer → client | nothing new; but *rate* (repaint coalescing) | irrelevant for observation |
| byte → signal (ISIG) | the byte itself | nothing — it's a different type now |
| child → parent (`wait`) | everything but exit status | the child's own logs / hooks |
| compaction | the context | `PreCompact` is the only warning |

---

## Chapter 6 — The context bus: passing state between sessions as a byproduct

_Released 2026-09-18. `[NABLA]` design, resting on `[VERIFIED]` hooks. Your stated aim: pass part
of the context between two sessions, under your control, invariant to window shifts._

### 6.0 What "context" means here — three things, not one

1. **Conversation context** — what the model currently holds (volatile, lost at compaction).
2. **Session facts** — cwd, files touched, tools run, decisions (durable, already in `events.jsonl`).
3. **Intent** — what the human wants the *next* session to know (nothing produces this
   automatically; it must be written).

The bus must carry 2 and 3. It cannot carry 1 (no API dumps the live context), and it should not
try — that is the transcript's job, and the transcript lags.

### 6.1 The two moments the bus should fire

- **`PreCompact`** — the CLI is about to forget. The hook's stdout is *not* injected here, but the
  hook can write a **checkpoint**: a distilled file the *next* turn can be told to read.
- **`SessionStart` with matcher `resume|compact|clear`** — stdout of this hook **is added to
  context**. This is the injection point. The hook reads the latest checkpoint(s) and prints them.

Together they are a loop that survives compaction *and* session restarts without the human doing
anything — which is exactly your "scheduled rotation as metabolic norm" from the larva
principles, instantiated on the CLI's own lifecycle events.

### 6.2 The bus is a directory

```
~/.rack/bus/
├── <session_id>/
│   ├── checkpoint.2026-09-18T10:14:03Z.md    ← written at PreCompact / on demand
│   └── intent.md                              ← written by the human (or by a Stop hook on request)
└── links/
    └── <session_B> -> ../<session_A>          ← "B should read A's checkpoints" — a symlink
```
Routing again is the filesystem: session B's `SessionStart` hook prints the newest checkpoint of
every session it is linked to. Linking is `ln -s`. Unlinking is `rm`. Control stays in your hands
and is auditable with `ls -l`.

### 6.3 Who writes the checkpoint — the honest problem `[OPEN]`

`PreCompact` runs a *shell script*, not the model. The script can:
- (cheap) copy the last N `events.jsonl` lines + `meta.json` into a checkpoint — **facts only**;
- (richer) ask the model itself: use a `prompt`/`agent` hook type, or spawn `claude -p "summarise
  for handoff…" --resume <sid>` — costs tokens and time inside a hook timeout.

Pushback on the rich path: a summary produced *while the context is at its limit* is your
"Last Standing Man" anti-pattern — the degraded agent writing its own obituary. Prefer the cheap
path continuously (every `Stop` appends a one-line "turn summary" from `last_assistant_message`)
so `PreCompact` only has to *point*, not *produce*. That matches the principle you already hold:
decouple checkpointing from the handoff signal.

### 6.4 Control surface

- Read-only by default: the bus never writes into a session's *transcript*.
- Injection only via `SessionStart` stdout, bounded (cap at N KB; the hook truncates).
- Every injection is itself logged as an event (`{"kind":"event","src":"bus","injected":…}`) so the
  board shows *what B was told* — no invisible context.

### 6.5 Chapter 6 verdict

- The bus is a byproduct: two hooks and a directory of symlinks on top of the rack. `[NABLA]`
- It carries facts and intent, never the live context. `PreCompact` points; `Stop` accumulates.
- Injection happens at exactly one documented place (`SessionStart` stdout). `[VERIFIED 2026-09-17]`

---

## Chapter 7 — Reading the board with an AI: filtered slices, not firehoses

_Released 2026-09-18. Short by design._

### 7.0 The problem restated

You said it: a hundred lines of `ps` is useless to you and worse for a model. The value of the
rack for an AI reader is not access — the files are plain text — it is **pre-filtered scope**.

### 7.1 Three slices, each a jq one-liner, each a file the AI can be pointed at

- **"What happened in session X in the last 10 turns?"** → `events.jsonl` filtered to
  `UserPromptSubmit|Stop|PostToolUse(Failure)`, `tool_input` truncated to 200 chars, last 10
  `prompt_id`s. Typically < 4 KB.
- **"What is X holding right now?"** → last `snap` of `tree.jsonl` + last `snap` of `fds.jsonl`,
  descendants of `cli_pid` only, sockets resolved via `ss`. Typically < 1 KB.
- **"Why did X stall?"** → last `Notification`, last `PermissionRequest`, last `StopFailure`,
  viewport-unchanged-since from `view.ndjson`, process state letter from `/proc`. < 1 KB.

Make each slice a script in `lenses/slice-*.sh` that writes `~/.rack/slices/<name>.<sid>.md`. Then
"talk to a CLI about the demo" is `claude "read ~/.rack/slices/stall.<sid>.md and tell me what you
see"` — or better, a `SessionStart` hook in a *reader* session that injects the slice. Same bus.

### 7.2 Two rules for AI readers

1. **The AI reads slices, never the raw files, unless it asks.** Raw is for `tail`, `grep`, you.
2. **A reader session is itself a session** — it gets its own `session_id`, its own `events.jsonl`,
   and shows up on the board. Observing the observer is free; you'll want it the first time a
   reader misreads a slice.

### 7.3 Chapter 7 verdict

Slices are the API. They are derived (rebuildable from the roll), small, and text. That is the
entire integration surface between the rack and any model — yours, mine, ChatGPT's.

---

## Closing — the plan as a whole

```
truth:     events.jsonl (L5 sensors)  +  *.jsonl snaps (L1/L3 pollers)     ← append-only roll
projection: board / detail panes / slices                                   ← disposable
control:   picker → selected ; bus → links + SessionStart injection         ← files, auditable
host:      Zellij "rack" session, separate from observed sessions
```
Phase C entry: v0 = sensor script + hook JSON + 3 pollers + KDL layout + 3 slice scripts.
No compilation. Then we sit on whichever part you choose.
