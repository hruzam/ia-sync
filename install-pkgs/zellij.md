# zellij — install task

```
developed-on: office (hruzam-120922)
install-on:   home + office (both Arch/Manjaro)
source:       Arch extra repo (pacman -S zellij)
built:        2026-09-03
version:      1.0
hosts:        home office
automation:   auto
pinned-version: 0.44.3
```

---

## What this installs

zellij terminal multiplexer from the Arch `extra` repository (no AUR, no manual build).
Used for named session layouts (KDL layout files in `~/.config/zellij/layouts/`) and
interactive terminal workspace management on both machines.

Layouts live in `~/.config/zellij/layouts/<name>.kdl`. Load a named layout with:
```bash
zellij --layout <name>
# or attach-or-create pattern (see config.office.zsh / config.home.zsh):
zellij attach <session> 2>/dev/null || zellij --session <session> --layout <name>
```

## Verify

```bash
zellij --version   # should report pinned-version above
```

## Version tracking

When advancing to a newer zellij on one host via `sudo pacman -Syu`, bump
`pinned-version` in this file to match, bump `version` (triggers re-check on the
other host), then commit + deploy.

<!-- install:check -->
```bash
command -v pacman >/dev/null 2>&1 || { echo "pacman not found — not an Arch/Manjaro host?"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
wanted="0.44.3"
current=""
if command -v zellij >/dev/null 2>&1; then
  current="$(zellij --version 2>/dev/null | awk '{print $2}')"
fi
if [ "$current" = "$wanted" ]; then
  echo "zellij $wanted already installed — nothing to do"
else
  sudo pacman -S --noconfirm zellij || exit 1
  current="$(zellij --version 2>/dev/null | awk '{print $2}')"
  echo "installed zellij $current"
fi
zellij --version
```
<!-- /install:run -->
