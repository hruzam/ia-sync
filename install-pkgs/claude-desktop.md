# claude-desktop — install task

```
developed-on: home (hruzam)
install-on:   office (hruzam-120922)
source:       AUR — https://aur.archlinux.org/packages/claude-desktop
built:        2026-08-27
version:      1.0
hosts:        home office
automation:   manual
```

> **manual** — AUR builds can prompt (PKGBUILD review, GPG, makepkg confirmation) and
> take a while; not safe to run unattended. The runner only gates on `check` below,
> then points here. Do the one-liner by hand, then record it:
> `bash run.sh mark claude-desktop`.

---

## What this installs

Official Anthropic desktop app (Chat, Cowork, Claude Code) packaged for Arch/Manjaro
via AUR. Confirmed on AUR 2026-08-27: `claude-desktop` v1.37937.1-1, maintainer
kevindiaz314, 17 votes — the higher-popularity of two AUR options (the other is
`claude-desktop-extra`, a fork adding Computer Use / multi-profile / custom themes;
not installed, not tracked here — swap package name below if you want that one instead).

This is a plain AUR package — no repo-authored config, no `~/.claude` state, nothing
`deploy.sh` can carry. Login/auth stays per-machine, same as the CLI.

## Steps

```bash
pamac build claude-desktop
# or: yay -S claude-desktop
```

## Verify

```bash
pacman -Qi claude-desktop | head -3
command -v claude-desktop
```

<!-- install:check -->
```bash
command -v pamac >/dev/null 2>&1 || command -v yay >/dev/null 2>&1 || command -v paru >/dev/null 2>&1 \
  || { echo "no AUR helper (pamac/yay/paru) found — install one first"; exit 1; }
echo "prereqs ok — run: pamac build claude-desktop"
```
<!-- /install:check -->
