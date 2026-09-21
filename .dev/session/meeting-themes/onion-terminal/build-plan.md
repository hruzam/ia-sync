# unilarvatrix — build plan (v0 → v1)

_Nabla · 2026-09-18 · Companion to `docs/terminal-onion.study.2026-09-17.md` (the study).
Format: each step is a stone — self-contained, has a DONE test, and a "hand to CLI" line you can
paste into Claude Code if you pick it up cold. Flags as in the study._

Short name: `ulx`. Repo: `~/unikuklatrix/unilarvatrix/`. Data: XDG (`~/.config/ulx`, `~/.local/state/ulx`).

---

## Phase 0 — Ground (no code)

### 0.1 Repo
- `git init`; layout: `README.md docs/ docs/reports/ lenses/ slices/ hooks/ layouts/ src/`
- Move the study into `docs/`.
- **DONE:** `git log` has one commit "ground".
- **Hand to CLI:** "Create this directory layout in the current repo, move ../study file to docs/, commit as 'ground'."

### 0.2 Probes — close the study's `[INFERRED]` flags on this machine
Run inside a live Claude Code session in a Zellij pane.
- **P1 hop count + pane key:** temporary `PreToolUse` hook that appends `$PPID`, `/proc/$PPID/comm`,
  grandparent comm, and `env | grep ZELLIJ` to `/tmp/probe.out`. Run one tool.
- **P2 tool-child wiring:** run `sleep 30` via the Bash tool; from another pane
  `ls -l /proc/<pid>/fd` and pgid/sid from `/proc/<pid>/stat`.
- **P3 command pane env:** `zellij run -- sh -c 'env | grep ZELLIJ > /tmp/cmdpane.out'`.
- Write `docs/reports/<date>.probe-results.md` with raw output + one verdict line per probe.
- **DONE:** the report exists and answers: (a) how many hops from hook to `claude`; (b) whether tool
  children get pipes (not the pty) and which pgid; (c) whether `ZELLIJ_PANE_ID` is set in command panes.
- **Hand to CLI:** "Read docs/terminal-onion.study.*.md §4.2, §3.3, §2.2. Help me run the three probes
  described there and write docs/reports/<today>.probe-results.md."

---

## Phase 1 — v0 sensors (sh + jq, no compilation)

### 1.1 `lenses/append.sh` — the universal hook sensor
- Reads stdin JSON; derives `session_id`; `mkdir -p $XDG_STATE_HOME/ulx/sessions/<sid>`;
  appends one `{"ts","kind":"event","src":"hook",...}` line stamped with `cli_pid` (per P1),
  `pane_id` (`terminal_$ZELLIJ_PANE_ID`), `zellij_session`. Exit 0, empty stdout.
- On `SessionStart`: also write `meta.json` (cwd, pane, cli_pid, started).
- `tool_input` truncated to N chars (default 2000) so one line stays under `PIPE_BUF`.
- **DONE:** `echo '{"session_id":"t1","hook_event_name":"Stop"}' | lenses/append.sh` produces
  `~/.local/state/ulx/sessions/t1/events.jsonl` with one valid line (`jq . <` passes).
- **Hand to CLI:** "Implement lenses/append.sh per study §4.4 and §5.2, POSIX sh + jq only."

### 1.2 `hooks/claude.json` — the fragment
- Registers `append.sh` on: SessionStart, SessionEnd, UserPromptSubmit, Stop, PreToolUse,
  PostToolUse, PostToolUseFailure, SubagentStart, SubagentStop, Notification, PreCompact, PostCompact.
- `hooks/install.sh` merges it into `~/.claude/settings.json` with `jq` (backup first, never overwrite).
- **DONE:** `/hooks` inside Claude Code lists the events; one real turn appends real lines.
- **Hand to CLI:** "Write hooks/claude.json + hooks/install.sh (jq merge with backup) for the events listed."

### 1.3 Pollers — one file each, tick = 2 s, anchored on `meta.json`
- `lenses/tree.sh <sid>` → descendants of `cli_pid` → `{"ts","kind":"snap","src":"tree","pids":[...]}`
- `lenses/fds.sh <sid>` → per pid: fd → target (files, `pipe:[…]`, `socket:[…]` resolved via `ss -xp`)
- `lenses/view.sh <sid>` → `zellij subscribe --pane-id <pane> --format json` passthrough → `view.ndjson`
- **DONE:** each writes ≥1 valid snap line for a live session; `kill` leaves files intact.
- **Hand to CLI:** "Implement the three pollers from study §1.1, §1.2, §2.3; each owns exactly one file."

### 1.4 `layouts/rack.kdl` — the app
- Zellij layout: session `rack`; panes: events (`tail -F … | jq -r`), tree (last snap, diffed),
  fds (last snap), view (`view.ndjson` → text).
- Launch: `zellij --layout ~/.config/ulx/rack.kdl -s rack`.
- **DONE:** four panes update live while a Claude Code session runs in another Zellij session.
- **Hand to CLI:** "Write layouts/rack.kdl per study §5.0/§5.1; readers are tail|jq pipelines only."

### 1.5 Slices
- `slices/turns.sh <sid>`, `slices/holding.sh <sid>`, `slices/stall.sh <sid>` → `slices/<name>.<sid>.md`
  per study §7.1; each < 4 KB.
- **DONE:** `claude "read <slice> and summarise"` gives a correct 5-line answer.

### 1.6 Housekeeping
- `SessionEnd` → move session dir to `archive/YYYY-MM/<sid>/`.
- README: 20 lines, what/why/run.
- **DONE:** tag `v0`.

---

## Phase 2 — v1 (Rust only where a grid or residency is needed)

### 2.1 `src/ulx-pick`
- Reads registry (`sessions/*/meta.json`) + last tree snap; keys j/k/Enter/Esc; writes
  `~/.local/state/ulx/selected` atomically (tmp+rename). Nothing else. ≤300 lines.
- **DONE:** `echo "sid tree 4201" > selected` and the picker's own writes are indistinguishable to readers.

### 2.2 Readers react to `selected`
- Detail panes wrap `tail|jq` in a loop that re-execs on inotify of `selected`.
- **DONE:** picking a session in one pane switches all detail panes.

### 2.3 `src/ulx-board` (optional)
- Single-pane grid view; spawns on-demand pollers for live drill-down (the `[OPEN]` seam, study §5.4).
- Only if `watch`+`jq` panes prove too coarse.

---

## Phase 3 — context bus (study ch. 6)

- `Stop` hook appends one-line turn summary from `last_assistant_message` → `bus/<sid>/turns.md`.
- `PreCompact` hook writes `checkpoint.<ts>.md` = `meta.json` + last N turns (facts only).
- `SessionStart` (matcher `resume|compact|clear`) prints newest checkpoints of linked sessions
  (`bus/links/<sid> -> ../<other>`), capped at N KB; logs the injection as an event.
- **DONE:** session B, started fresh, correctly answers "what was A doing?" without the human typing it.

---

## Phase 4 — other CLIs and the plugin path (later)

- Codex / Gemini: find their hook or log surface; if none, they get L1–L3 lenses only
  (viewport-unchanged + process-alive = stall). Report per CLI in `docs/reports/`.
- Zellij WASM plugin: only if `list-panes` polling is too coarse. Writes `registry.jsonl`; nothing else changes.

---

## When lost — the three-line reorientation
1. `cat docs/build-plan.md` → find the first step without a DONE.
2. Paste that step's "Hand to CLI" line plus: "Study is in docs/terminal-onion.study.*.md; flags
   [MEASURED]/[INFERRED]/[OPEN] mean what they say; do not exceed the step."
3. Every finding that changes a study flag → one file in `docs/reports/`, dated.
