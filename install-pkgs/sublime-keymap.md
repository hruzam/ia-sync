# sublime-keymap — install task

```
version:    1.1
hosts:      home office
automation: manual
src-root:   ~/www/elements-factory/applications-in-common
```

---

## What this installs

The merged `Default (Linux).sublime-keymap` in Sublime Text's `Packages/User/`.
This file is the single canonical keymap for both machines — it merges:

- **editor-pin-sublime bindings** (`ctrl+alt+*`) — pins to `~/.wires/pins.jsonl`
- **Markdown preview** (`alt+m`, `alt+shift+m`) — opens current file as HTML in browser (both local parser)
- **Freed navigation keys** — `ctrl+r/b/f` nooped; Sublime commands moved to `ctrl+shift+r/b`
- **Numpad navigation** (belt-and-suspenders Arch/Wayland fix — see History below)

> **Note:** `editor-pin-sublime.md` step 2 (`cp Default.sublime-keymap`) now overlaps with
> this task. On a fresh machine: run THIS task first, skip step 2 of editor-pin-sublime.
> On an existing machine: merge by hand (see Steps below).

---

## History / why this task exists

### Numpad regression — 2026-07-30 (pad.1-arch-repair.md)

NumPad-based selection shortcuts (Shift+End, Ctrl+Shift+End-style) stopped working on both
machines. Suspected cause at the time: pacman/Sublime update. **Actual cause:** KDE Plasma
Wayland does not read `numlockx.desktop` (X11-only tool); `~/.config/kcminputrc` was not
set, so NumLock state was undefined at session start.

Fix applied 2026-07-30: `[Keyboard] NumLock=1` written to `~/.config/kcminputrc` on both
machines (takes effect on next Plasma session start).

The Sublime numpad bindings added in v1.0 of THIS keymap are belt-and-suspenders — they
map `keypad1`–`keypad9` directly in Sublime so selections work regardless of system NumLock
state, protecting against future Wayland regressions.

### Keymap overwrite gap — flagged in pad.1-arch-repair.md

`editor-pin-sublime.md` deploy (step 2) does a plain `cp` with no backup guard. Office
keymap was overwritten 2026-07-18 with pin-only bindings, losing whatever was there before.
Recovery via timeshift was possible but not yet confirmed (needs `sudo` on office).

This task is `automation: manual` specifically to prevent blind overwrites.

---

## Source

```
experiments/editor-pin-sublime/Default.sublime-keymap
```

This file is the merged canonical source — updated 2026-08-05 to include all binding
groups listed above. Keep it in sync when keymap changes.

---

## Steps (manual)

### Fresh machine (no keymap in Packages/User yet)

```bash
cp "$SRC/experiments/editor-pin-sublime/Default.sublime-keymap" \
   ~/.config/sublime-text/Packages/User/"Default (Linux).sublime-keymap"
```

### Existing machine (keymap already present — merge by hand)

1. Open both files side by side:
   - Source: `$SRC/experiments/editor-pin-sublime/Default.sublime-keymap`
   - Target: `~/.config/sublime-text/Packages/User/Default (Linux).sublime-keymap`
2. Copy any missing binding groups into the target.
3. Never overwrite without diffing — the live file may have local additions.

### After install / merge

```bash
# confirm keymap loaded (Sublime must be running)
# Ctrl+` → console → check for syntax errors
# Test: alt+m (markdown preview), ctrl+alt+< (pin), ctrl+shift+keypad1 (select to EOF)
```

Record as done:

```bash
bash ~/ia-sync/install-pkgs/run.sh mark sublime-keymap
```

---

<!-- install:check -->
```bash
[ -d "$HOME/.config/sublime-text/Packages/User" ] || { echo "Sublime Text not installed or never launched"; exit 1; }
[ -f "$SRC/experiments/editor-pin-sublime/Default.sublime-keymap" ] || { echo "source keymap not found at $SRC/experiments/editor-pin-sublime/"; exit 1; }
```
<!-- /install:check -->
