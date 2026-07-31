# editor-pin-sublime — install task

```
developed-on: home
install-on:   home (Packages/User/ deploy; office deploy pending)
source:       experiments/editor-pin-sublime/
built:        2026-07-17 (H5 closed reshaped) · v1.1 deployed 2026-07-18
```

---

## What this installs

Sublime Text plugin that pins editor lines to `~/.wires/pins.jsonl` for agent consumption.
No build step — two Python files + keymap copied to Sublime's user packages dir.

## Prerequisites

- Sublime Text installed on home
- Project checked out (pull first — `git pull` in the project dir)

## Steps

1. Copy plugin files to Sublime user packages:

       cp experiments/editor-pin-sublime/editor_pin.py ~/.config/sublime-text/Packages/User/
       cp experiments/editor-pin-sublime/pin_core.py   ~/.config/sublime-text/Packages/User/

2. Copy or merge the keymap:

       cp experiments/editor-pin-sublime/Default.sublime-keymap ~/.config/sublime-text/Packages/User/

   If a `Default.sublime-keymap` already exists in Packages/User/ — merge by hand.
   Operator may remap freely; command names are stable, chord-to-key is personal.

3. Create the global pin store directory:

       mkdir -p ~/.wires

4. Make the claim script executable:

       chmod +x experiments/editor-pin-sublime/skill/claim-pins.sh

5. Reload Sublime: Command Palette → `Package Control: Reload Package`, or restart.

## zsh wiring (if not already on home via ia-sync)

`pinkeys` is defined as `_pinkeys` in `~/.config/zsh/ai/claude.zsh` — deployed by ia-sync.
If `pinkeys` is not found after `source ~/.config/zsh/ai/base.zsh`:
→ run ia-sync deploy first (`bash ~/ia-sync/deploy.sh`), then re-verify.

## Verify

    pinkeys                           # prints chord-to-command table for installed keymap
    ls ~/.wires/                       # dir exists (empty is fine)
    # Drop a test pin in Sublime, then:
    cat ~/.wires/pins.jsonl | tail -1  # should show a JSON record
