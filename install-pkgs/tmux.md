# tmux — install task

```
developed-on: office (hruzam-120922)
install-on:   home (hruzam)
source:       Arch extra repo (pacman -S tmux)
built:        2026-09-04
version:      1.0
hosts:        home office
automation:   auto
pinned-version: 3.7b
```

---

## What this installs

tmux terminal multiplexer from the Arch `extra` repository. Required on home for:
- `tmux-pin-bus` (Claude SessionStart/Stop hooks → `~/.bus/hooks.jsonl`)
- `netOrchestrating` (symmetric SSH file-bus relay)

Office has tmux natively; home was previously absent. Installed on home 2026-09-04.

## Verify

```bash
tmux -V   # should report pinned-version above
```

## Version tracking

When advancing via `sudo pacman -Syu`, bump `pinned-version` and `version` here,
commit + deploy so the other host gets the re-check trigger.

<!-- install:check -->
```bash
command -v pacman >/dev/null 2>&1 || { echo "pacman not found — not an Arch/Manjaro host?"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
wanted="3.7b"
current=""
if command -v tmux >/dev/null 2>&1; then
  current="$(tmux -V 2>/dev/null | awk '{print $2}')"
fi
if [ "$current" = "$wanted" ]; then
  echo "tmux $wanted already installed — nothing to do"
else
  sudo pacman -S --noconfirm tmux || exit 1
  current="$(tmux -V 2>/dev/null | awk '{print $2}')"
  echo "installed tmux $current"
fi
tmux -V
```
<!-- /install:run -->
