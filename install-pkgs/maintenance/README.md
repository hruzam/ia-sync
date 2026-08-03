# maintenance/ — machine repair pads

Home-only folder (not mirrored to office in this batch, deliberately). Records repairs made
directly to a machine's OS/desktop-level state — the stuff `deploy.sh`/`sync.sh` never touch
because it isn't ia-sync-tracked content (kernel/DE settings, systemd/autostart state,
X11/Wayland session config...) and isn't a reproducible install recipe either — that's what
the sibling `install-pkgs/*.md` task files are for (see `../README.md`).

## Not a task file

`run.sh`'s task scanner is `find "$PKGDIR" -maxdepth 1 -name '*.md'` (see `../run.sh`) — this
folder sits one level below `maxdepth 1`, so `run.sh` never lists it, never runs it, never
tries to parse a header out of it. Pads here exist purely for reading, not execution.

## Why "pad" structure

Format borrowed from
`~/www/elements-factory/applications-in-common/.dev/session/larvaTmux/pad.*.md`: numbered
STEP blocks, each with what was run/found and a report section underneath. Good for reading
back later — scan the STEP headers for the shape of a repair without re-reading prose.

## Why this folder is safe to create home-only

It doesn't exist on office yet. `sync.sh` / `git pull` on office receives it as new content —
nothing here to conflict with, nothing pre-existing to overwrite, no merge required. It also
isn't under `claude/skills/` or `claude/commands/` (the only sync legs that run `--delete`),
so there's no risk of it wiping something office added independently. If office ever starts
its own maintenance pad, that's a separate file — this index doesn't need to predict it.

## Naming

`pad.<n>-<slug>.md` — sequential per repair line, one file per distinct maintenance episode.
Context that matters across the whole pad (mode, date, machines touched, what's still open)
goes in a short header block at the top of the file itself — these are one-shot repair logs,
not multi-sitting test protocols, so no separate `session.md` is needed the way larvaTmux uses
one.

## Index

- `pad.1-arch-repair.md` — 2026-07-30 · NumLock/Wayland shortcut regression (home + office,
  fix applied, verification pending relogin) · ssh dead-rule cleanup (diagnosed, parked
  pending go-ahead) · Sublime keymap overwrite (diagnosed, recovery parked — needs operator
  `sudo`/timeshift on office)
- `pad.2-home-deploy.md` — 2026-07-30 · `/multihost` receive on home (8 prompts, 6 superseded)
  · dead skills retired with backup · **`sync.sh` on home = NO GO** (resurrection race, 9
  files + office's `codex-run.zsh`, unresolved) · registry/normalizer superseded by
  `temple-project-map.zsh` (decision 0008) · `zshrc.home` + `.claude/` deny landed
  (`c648895` (2026-07-30)) · deploy pre-flight verified safe, **not yet run** · `deploy.sh` backup holes
  gaveled 3+1+5, queued behind the deploy
  · **charter note:** ia-sync content, not OS/desktop state — stretches this folder's scope
  (see pad header)
- `pad.3-pre-burn-exposure-audit.md` — 2026-07-30 · full-history secret enumeration taken
  **before** the planned repo burn, because a burn destroys the record of what was exposed
  along with the exposure. 10 raw hits → 8 false positives, 2 real. **REAL #1** FTP
  `defaultfan` — operator-confirmed DEAD, no rotation. **REAL #2** MariaDB `majkee`/
  `fantasyobchod` in `guides/home-setup/diagnose_opencart_404.md` — ⚠ NEW, **still in the
  working tree so the burn does not remove it**, liveness UNCLASSIFIED. Also: three
  independent gaps in `sync.sh`'s secret scan, the history bundle location, and the burn
  checklist (office's `/multihost` marker must be cleared by hand)
- `pad.4-env-vault.md` — 2026-07-30 · seal `zsh/.env/` into a single travelling ciphertext
  blob (`zsh/env.vault.age`) via the new repo-root `env-vault` tool (age, one shared key).
  **Additive** design — plaintext `.env/` never moves, so no lockout on a working machine;
  the git copy becomes ciphertext (defends a leaked clone, not a compromised live box).
  Operator test surface: STEP 0 audit → key + backup → seal → cross-machine open on home.
  Tool round-trip tested on dummy data before authoring. **Not yet walked.**
  *(Update 2026-07-31: walked compressed same day — sealed, burned into genesis, STEP 7
  closed from home with a bonus finding: the vault's first act unified a silent two-month
  secrets fork. See pad body execution record.)*
- `pad.5-shell-harmonize-verify.md` — 2026-07-31 · office login shell was `/bin/bash` (home:
  zsh) — SSH sessions from home got no zsh harness (`tsp: command not found`). `chsh` to
  `/usr/bin/zsh` run by operator, UNTESTED at authoring. Pad = Monday walk, majkee physically
  at office: account record → ssh-localhost reproduction → office→home aliases → home→office
  lands-in-zsh → eagle-rail recipe → optional reboot drill. **Not yet walked.**
- *(no pad)* **2026-08-03 · Sublime install + keymap consolidation (home)** — no OS-level
  repair; recorded here for continuity with the keymap thread from pad.1 STEP 4.
  · `editor-pin-sublime` plugin deployed to home for first time (`editor_pin.py`,
  `pin_core.py` → `Packages/User/`; `~/.wires/` created; `claim-pins.sh` +x).
  · `Default (Linux).sublime-keymap` written as merged canonical: pin bindings +
  markdown preview (`alt+m`) + freed `ctrl+r/b` (remapped to `ctrl+shift+r/b`) +
  numpad nav/selection (belt-and-suspenders against Wayland NumLock regression, pad.1 STEP 2).
  · Operator adjusted two pin chords live: `ctrl+alt+<` → `ctrl+alt+]` (drop pin),
  `ctrl+alt+r` → `ctrl+alt+'` (tmux send).
  · `ia-sync/install-pkgs/sublime-keymap.md` created (v1.0, manual, hosts: home office) —
  captures history, source path, and merge discipline for future deploys.
  · Stale Markdown packages removed from Sublime: MarkdownLivePreview, Markdown HTML
  Preview, Markmon (kept: MarkdownEditing + MarkdownPreview).
  · `Write(experiments/**)` permission rule fixed → `Edit(experiments/**)` in
  `.claude/settings.local.json`.
