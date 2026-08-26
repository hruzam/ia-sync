# chatgpt-desktop — install task

```
developed-on: home (hruzam)
install-on:   office (hruzam-120922)
source:       AUR — https://aur.archlinux.org/packages/chatgpt-desktop
built:        2026-08-26
version:      1.0
hosts:        home office
automation:   manual
```

> **manual** — AUR builds can prompt (PKGBUILD review, GPG, makepkg confirmation) and
> take a while; not safe to run unattended. The runner only gates on `check` below,
> then points here. Do the one-liner by hand, then record it:
> `bash run.sh mark chatgpt-desktop`.

---

## What this installs

OpenAI's official ChatGPT desktop app for Linux, repackaged from the official binary
(AUR package `chatgpt-desktop`, provides `chatgpt`). Installed on home 2026-08-26 via
`pamac build chatgpt-desktop`. This is the app referred to loosely as "codex" in
conversation — there is no separate `codex-desktop`/`codex-app-*` AUR package installed
here; the Codex agent surface lives inside this ChatGPT app. The standalone Codex CLI
is unrelated and already tracked in `codex-cli.md` (npm-based, no change needed there).

Plain AUR package — no repo-authored config, no state `deploy.sh` can carry. Login/auth
stays per-machine.

## Steps

```bash
pamac build chatgpt-desktop
```

## Verify

```bash
pacman -Qi chatgpt-desktop | head -3
command -v chatgpt
```

<!-- install:check -->
```bash
command -v pamac >/dev/null 2>&1 || command -v yay >/dev/null 2>&1 || command -v paru >/dev/null 2>&1 \
  || { echo "no AUR helper (pamac/yay/paru) found — install one first"; exit 1; }
echo "prereqs ok — run: pamac build chatgpt-desktop"
```
<!-- /install:check -->
