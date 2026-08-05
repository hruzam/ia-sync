# install-pkgs — SOURCE OF TRUTH

From different projects come innovations. Not every one is a clean git sync —
some must be *installed* on the second machine (home ↔ office): application
packages, hook registrations, per-machine configs, chmod requirements — things
`deploy.sh` cannot do as a plain rsync.

Each task file here is the exact install prescription for one such thing.
`run.sh` is the local package manager over them — AUR `-Syu`, home-made.

---

## Using it — step by step (run one, read output, next)

### STEP 0 — see what this machine needs

```bash
cd ~/ia-sync/install-pkgs
bash run.sh list
```

Read the **STATE** column:
- `not-installed (auto)`   → STEP 1 installs it for you
- `not-installed (manual)` → STEP 2, you run it by hand
- `STALE (have X)`         → recipe got a new version → STEP 1 re-installs
- `current`                → done, nothing to do
- `n/a (other host)`       → not for this machine, ignore

---

### STEP 1 — install everything automatic

```bash
bash run.sh update
```

Watch each line:
- `installing... ok`            → done and recorded ✅
- `already current, skip`       → nothing to do ✅
- `check failed: <reason>`      → fix the reason, run STEP 1 again
- `manual — run steps in X.md`  → go to STEP 2

---

### STEP 2 — a manual task (runner won't auto-run it)

Some tasks are too interactive to automate (SSH host-key accept, `nano` a config,
launch a live tmux pane). The runner only checks the prerequisites, then hands it
to you. Open the file it named, do the steps, then **record it**:

```bash
# example — after doing netOrchestrating.md by hand:
bash run.sh mark netOrchestrating
```

---

### STEP 3 — confirm

```bash
bash run.sh list
```

Everything for this host should now read `current`. Done.

> Reinstall / retest a task: `bash run.sh unmark <slug>` then STEP 1 again.
> State is per-machine at `~/.local/state/ia-sync/installed.json` — **never synced**
> (or office would claim installed what home never ran — the SYNC_DISCIPLINE trap).

---

## Adding a new task — step by step

### STEP A — when does a thing belong here?

Create `install-pkgs/<slug>.md` at **build time** when ALL hold:
1. **Out-of-repo target** — lands outside any git path: Sublime `Packages/User/`,
   `~/.wires/`, `~/.bus/`, `~/.remote/`, per-machine configs, hook registrations, `chmod`
2. **Must be reproduced** on the other machine
3. **`deploy.sh` cannot do it** — not a plain rsync from ia-sync

### STEP B — put these 4 lines in the header (the runner reads only these)

```
version:     1.0          # bump this when the recipe changes → triggers re-install
hosts:       home         # which machines install this: home, office, or "home office"
automation:  auto         # auto = runner runs it · manual = runner gates, you run it
src-root:    ~/www/...     # optional: project root the recipe copies FROM (~ expands)
```

Free-form docs above/below (`developed-on:`, `source:`, prose, smoke tests) are for
humans — the runner ignores them.

### STEP C — for `automation: auto`, add the two bash blocks

The HTML comments are sentinels (invisible on GitHub; the ```bash still renders):

```
<!-- install:check -->
​```bash
# preconditions. echo a reason and `exit 1` to REFUSE.
# $SRC (src-root expanded), $FRIENDLY, $MACHINE are in the env.
command -v tmux >/dev/null 2>&1 || { echo "tmux not installed"; exit 1; }
​```
<!-- /install:check -->

<!-- install:run -->
​```bash
# idempotent + NON-DESTRUCTIVE. Never blind-overwrite a hand-edited file —
# guard it: if [ -e "$f" ]; then echo "exists, merge by hand"; else cp ...; fi
python3 "$SRC/experiments/tmux-pin-bus/pin_bus.py" install "$SRC"
​```
<!-- /install:run -->
```

For `automation: manual` — omit the `run` block. Keep only `check`. The runner gates
on it, then waits for `run.sh mark`.  Copy `tmux-pin-bus.md` (auto) or
`netOrchestrating.md` (manual) as your template.

### STEP D — test it

```bash
bash run.sh list        # your task should show its version + hosts, not "?"
bash run.sh update      # (on the target host) installs it
```

---

## Current tasks

### editor-pin-sublime · v1.1 · hosts: home · auto
Sublime plugin — pins editor lines to `~/.wires/pins.jsonl` for agents.
Source: `experiments/editor-pin-sublime/`
```bash
bash run.sh update      # copies plugin .py + keymap, makes ~/.wires
```

### tmux-pin-bus · v1.0 · hosts: home · auto
Registers Claude `SessionStart`+`Stop` hooks for a project → `~/.bus/hooks.jsonl`.
Source: `experiments/tmux-pin-bus/`
```bash
bash run.sh update      # runs pin_bus.py install on the project
```

### sublime-keymap · v1.1 · hosts: home office · MANUAL
Merged canonical Sublime keymap — markdown preview (`alt+m`, `alt+shift+m`), freed
nav keys, numpad navigation, editor-pin bindings.
Source: `experiments/editor-pin-sublime/Default.sublime-keymap`
```bash
bash run.sh update              # checks prereqs, points to sublime-keymap.md steps
# ...diff + merge the new binding groups by hand into Packages/User/...
bash run.sh mark sublime-keymap
```

### netOrchestrating · v1.0 · hosts: home office · MANUAL
Symmetric SSH file-bus relay between home ↔ office panes. Too interactive to auto-run.
Source: `experiments/netOrchestrating/`  ·  needs tmux-pin-bus first.
```bash
bash run.sh update              # runner only checks prereqs, points to the file
# ...do the steps in netOrchestrating.md by hand...
bash run.sh mark netOrchestrating
```
