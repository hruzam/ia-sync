---
to: @Maxwell (home · ia-sync)
from: @Flight (office · ia-sync · 2026-07-28)
topic: zshrc.{host} mechanism is live — home has no zshrc.home yet, and you must NOT fake one
host: office
priority: read before your next deploy
---

## TL;DR

Pull first. Then run `sync.sh` on home once, to fold home's `~/.zshrc` into
`zsh/zshrc.home`. Until you do, `deploy.sh` will print a WARNING and skip your
`~/.zshrc` — **that is correct behaviour, not a bug. Do not "fix" it.**

## What changed on the substrate (office, pushed as 0046a45)

- `zshrc.{host}` mechanism is now active. `sync.sh` folds `~/.zshrc` →
  `zsh/zshrc.${MACHINE}`; `deploy.sh` restores it back.
- `zsh/zshrc.office` now exists (54 lines). **`zsh/zshrc.home` does not exist yet** —
  only home can create it, by running `sync.sh` on home.
- `sync.sh` gained two hardcoded rsync excludes: `config.*.zsh` and `zshrc.*`.
- `SYNC_DISCIPLINE.md` documents the guard and the host-file-pair table.

## Why the sync.sh guard exists — this nearly reverted your work

`sync.sh` mirrors `~/.config/zsh/` → `zsh/` with `rsync --delete` and had no guard for
host-specific files. Office was carrying a stale `~/.config/zsh/config.home.zsh` dated
07-20 — **missing your `ai/base.zsh` fix** (21b2eb6).

A dry run showed it overwriting the repo copy. Had it run, the next home
`pull` + `deploy.sh` would have silently reverted the ai/ scope wiring — the exact
regression your commit exists to prevent, reintroduced by the sync tool itself.

Guard is hardcoded in `sync.sh`, deliberately **not** in `sync.deny`: that registry means
"must never exist in the repo", and its `find -delete` pass would have erased
`config.home.zsh` outright — a worse bug than the one being fixed.

Your `zsh/config.home.zsh` in the repo is canonical and intact. Verified on the remote.

## ⚠️ Do NOT create an empty or placeholder zshrc.home

@majkee floated hand-creating a stub `zshrc.home` so the file "exists". **Don't.**
`deploy.sh` does:

```sh
if [ -f "$REPO/zsh/zshrc.${MACHINE}" ]; then
  cp "$REPO/zsh/zshrc.${MACHINE}" "$HOME/.zshrc"     # no backup, straight overwrite
```

A stub file passes `-f`, so deploy would copy the stub over home's **real** `~/.zshrc`.
There is no backup step, and home's `~/.zshrc` has never been committed — the loss would
be unrecoverable.

The file being **absent** is the safe state: deploy warns and skips. Absence protects you;
a stub destroys you.

## What home should do — ORDER MATTERS, deploy before sync

```
1. git pull origin main     → repo up to date
2. bash deploy.sh           → LIVE home up to date   ← DO NOT SKIP
3. bash sync.sh             → now safe; creates zsh/zshrc.home
4. sanity-check zsh/zshrc.home is home's real file, not a stray
5. git add -A && git commit && git push
```

**Step 2 is not optional and `git pull` is not a substitute for it.** Pull updates the
*repo*; `sync.sh` reads the *live* machine (`~/.claude/skills/`, `~/.claude/commands/`),
which a pull never touches. Only `deploy.sh` refreshes those.

`sync.sh` runs `rsync --delete` on `claude/skills/`, `claude/commands/`, `gemini/agents/`
and `gemini/config/projects/`. If home's live set is stale and you sync before deploying,
every file home lacks is deleted from the repo — **30 skills and 3 commands as of today**,
including `gavel-loop`, `cold-start-card`, `drop-brief` (all added on office 2026-07-28).
Git records it as a deliberate removal, so it will not look like an accident in review.

`claude/agents/` is the only leg protected (additive, no `--delete`). Skills, commands and
the gemini legs are not. @majkee reviewed this 2026-07-28 and chose to rely on the order
discipline rather than add a code guard — so the discipline is the only control. Honour it.

Note: @majkee may hand-create `zsh/zshrc.home` from office (copy `zshrc.office`, rename,
paste home's real content). If it is already in the repo when you pull, step 3 will simply
overwrite it with home's genuine `~/.zshrc` — no conflict, no action needed.

## Open / deferred

- ~~No backup-before-overwrite in `deploy.sh`.~~ **Implemented same session** (@majkee's call).
  `deploy.sh` now backs up `~/.zshrc` and `~/.config/zsh/config.zsh` to
  `<file>.bak-YYYY-MM-DD` before replacing them. One backup per file per day — a second
  deploy the same day keeps the first, so the original pre-deploy state survives repeated
  bad deploys. `*.bak`/`*.bak-*` are already in `sync.deny`, so they never travel back into
  the repo. Undo a bad deploy on home with `cp ~/.zshrc.bak-<date> ~/.zshrc`.
  Note this means your first deploy on home will leave `.bak-` files in `~` and
  `~/.config/zsh/` — expected, not clutter to clean blindly.
- Office's live `~/.config/zsh/config.home.zsh` (stale 07-20) is still on disk. Harmless now
  that sync excludes it, but it is cross-machine contamination and could confuse a future
  reader. Left in place — deleting live files on office is your call, not mine.
- Rescue tag `rescue/pre-rebase-tip` is on the remote (pre-rebase originals from a
  2026-07-28 stuck-rebase recovery). Safe to ignore; @majkee will retire it.

— @Flight, office, 2026-07-28
