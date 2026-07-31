# tmux-pin-bus — install task

```
developed-on: office (hruzam-120922)
install-on:   home (hruzam)
source:       experiments/tmux-pin-bus/
built:        2026-07-18 (H7 built · smoke tests pending operator)
version:      1.0
hosts:        home
automation:   auto
src-root:     ~/www/elements-factory/applications-in-common
```

---

## What this installs

Registers Claude Code `SessionStart` + `Stop` hooks for a project directory.
Hooks append to `~/.bus/hooks.jsonl` — the identity ledger that maps BUS_PANE tokens
to session IDs. No binary install — hook registration is a single Python command per project.

## Prerequisites

- tmux installed on home: `which tmux`
- Claude Code installed and logged in
- Project checked out at `~/www/elements-factory/applications-in-common` (or adjust below)
- Run `claude` once by hand in the project dir and quit — clears first-run trust prompts
  before hook injection will work

## Steps

1. Pull the project (get H7 files if not already there):

       cd ~/www/elements-factory/applications-in-common
       git pull

2. Run the hook installer:

       python3 experiments/tmux-pin-bus/pin_bus.py install ~/www/elements-factory/applications-in-common

   This writes `SessionStart` + `Stop` entries into `.claude/settings.local.json` for the project.

3. Restart any running claude session in that project so it picks up the new hooks.

4. `~/.bus/` is auto-created by the first hook call — no manual mkdir needed.

## Smoke tests (run once after install, in order)

    bash experiments/tmux-pin-bus/smoke/01-sid-via.sh ~/www/elements-factory/applications-in-common
    bash experiments/tmux-pin-bus/smoke/02-first-inject.sh ~/www/elements-factory/applications-in-common
    bash experiments/tmux-pin-bus/smoke/03-round-trip.sh ~/www/elements-factory/applications-in-common

Full smoke sequence with expected outputs: `.dev/session/tmux-pin-bus/handoff.json`

## Verify

    cat ~/.bus/hooks.jsonl | tail -3   # shows SessionStart entries after a claude session opens

<!-- install:check -->
```bash
command -v tmux >/dev/null 2>&1 || { echo "tmux not installed"; exit 1; }
[ -d "$SRC/experiments/tmux-pin-bus" ] || { echo "source not checked out: $SRC/experiments/tmux-pin-bus"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
cd "$SRC" || exit 1
python3 experiments/tmux-pin-bus/pin_bus.py install "$SRC"
echo "hooks written to $SRC/.claude/settings.local.json — restart claude in that project"
```
<!-- /install:run -->
