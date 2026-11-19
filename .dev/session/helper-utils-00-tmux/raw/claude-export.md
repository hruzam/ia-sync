# Independent Claude status pane in tmux — findings + build instructions

Source: Trajectory seat, 2026-11-13, host verified by probing live files (Claude Code 2.1.323, tmux 3.7c).
Status: **findings are probed; the script in §4 is a sketch, not yet run in a pane.**

## 1. Why a pane

The vendor `statusLine` is a single line that Claude Code truncates with `…` at terminal width.
No wrap, no multi-row control. A tmux pane is ours: any width/height, any refresh rate, many rows.
Cost: it is a *sidecar* reading files, not fed the vendor JSON — so a few fields are derived, not exact.

## 2. What a sidecar can read (probed)

| Field wanted | Source | Exact? |
|---|---|---|
| session ID | `~/.claude/sessions/<pid>.json` → `.sessionId` | exact |
| session name (live, follows rename) | same file → `.name`, `.nameSource` (`user`/`derived`), `.formerNames[]` | exact, updates on rename |
| cwd | same file → `.cwd` | exact |
| agent seat (e.g. `trajectory`) | same file → `.agent` | exact |
| busy/idle | same file → `.status`, `.statusUpdatedAt` | exact (bonus) |
| tmux pane that hosts the session | same file → `.tmux` (e.g. `traj-home:@3.%3`) — **absent if session not started in tmux** | exact when present |
| CC version, started time | `.version`, `.startedAt` (ms epoch) | exact |
| jsonl path | `~/.claude/projects/<cwd with / → ->/<sessionId>.jsonl` (slug: `/home/hruzam/ia-sync` → `-home-hruzam-ia-sync`) | exact, deterministic |
| model | last `type=="assistant"` line in jsonl → `.message.model` (raw id, e.g. `claude-sonnet-5-5`; no pretty name) | exact id |
| context used | last assistant `.message.usage`: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` | **derived** |
| context left % | `1 - used / window` — window size is **not** in files; must be configured per model (200k / 1M) | **derived, approximate** |
| effort | `~/.claude/settings.json` → `.effortLevel` (configured, not live) | **config only**; live `/effort` change not visible |

Not available to a sidecar: vendor-computed `remaining_percentage`, pretty `display_name`, live effort. If those matter, keep the vendor `statusLine` for them and use the pane for the rest.

## 3. Pairing a pane with a session

1. In the pane, pick the target: `*.json` in `~/.claude/sessions/` whose `.tmux` starts with the same tmux session (`tmux display -p '#S'`), or let the user pass a pid/sessionId as `$1`.
2. Sessions without a `.tmux` field (like a session launched outside tmux) can only be chosen by pid/sessionId or newest `updatedAt` for `cwd`.
3. Multiple sessions share a tmux group (`traj-home`, `traj-home-majkee`) — match on window/pane (`@3.%3`) when precise, not on session name.
4. Stale files: a `<pid>.json` whose pid is dead is leftover — check `kill -0 <pid>`.

## 4. Sketch (bash + jq, poll 1–2 s)

```bash
#!/usr/bin/env bash
# claude-pane.sh [pid]  — run in a tmux pane:  watch-style loop, no vendor input
pid=${1:-$(ls -t ~/.claude/sessions/*.json | head -1 | xargs -n1 basename | cut -d. -f1)}
S=~/.claude/sessions/$pid.json
WINDOW=${WINDOW:-1000000}                      # per-model, configure
while sleep 1; do
  [ -f "$S" ] || { printf '\rno session %s' "$pid"; continue; }
  sid=$(jq -r .sessionId "$S"); cwd=$(jq -r .cwd "$S")
  name=$(jq -r .name "$S"); st=$(jq -r .status "$S")
  jl=~/.claude/projects/$(printf %s "$cwd" | tr / -)/$sid.jsonl
  last=$(tac "$jl" 2>/dev/null | jq -c 'select(.type=="assistant")|{m:.message.model,u:.message.usage}' 2>/dev/null | head -1)
  model=$(jq -r .m <<<"$last"); used=$(jq -r '.u|(.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens)' <<<"$last")
  left=$(( 100 - used*100/WINDOW ))
  eff=$(jq -r '.effortLevel // "?"' ~/.claude/settings.json)
  clear
  printf '%s  %s . %s . ctx %s%% left\n%s  [%s]\n%s\n%s\n' \
    "$model" "$eff" "${cwd/#$HOME/\~}" "$left" "$name" "$st" "$sid" "${jl/#$HOME/\~}"
done
```

Layout is free: one row per field (no truncation), or a single row sized to the pane.
`tac | jq … | head -1` is a perf wart on large jsonl — if it lags, switch to `tail -n 200`.

## 5. Wiring

- Author under `~/ia-sync/claude/` or `~/ia-sync/zsh/` (deployed surface), never live-only; dry-run `deploy.sh` first (SYNC_DISCIPLINE).
- Launch: `tmux split-window -v -l 6 'bash ~/.claude/hooks/claude-pane.sh'` or a keybind in tmux conf.
- Needs `jq` (already used by the vendor statusline script).

## 6. Open risks / checks

- `~/.claude/sessions/*.json` and the jsonl line shape are **undocumented internals** — may change between CC versions (seen: 2.1.322/2.1.323). Guard every `jq` with `// empty` and show `?`.
- Context-left is an estimate; label it `~`.
- Do not print `messagingSocketPath` or the `.key` files in `~/.claude/sessions/` (mode 600 secrets).
- Not verified: behaviour in a pane from a fresh session; a rename showing within 1 s (the `nameSince` field suggests yes).
- Vendor line is still deployed in `claude/settings.json`; the truncation is its width limit, not the script.
