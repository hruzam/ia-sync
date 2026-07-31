# ia-sync — Sync Discipline

Applies to: **all operators** — human (@majkee) and autonomous agents (Maxwell, Kelvin, Haiku, any future seat).

---

## The invariant

**Pull before you push. Always. No exceptions.**

If you sync local state into the repo without pulling first, you overwrite what the other machine committed. This is how traps happen.

---

## Steps — every sync session

```
1. cd ~/ia-sync
2. git pull --rebase origin main     ← receive other machine's work first
3. bash ~/ia-sync/sync.sh            ← push local state into repo
4. git add -A
5. git commit -m "sync: YYYY-MM-DD <machine> — <one line>"
6. git push origin main
```

Never skip step 2. Never reorder steps 2 and 3.

**If this machine may be behind, run `deploy.sh` BEFORE `sync.sh`.**
`git pull` updates the *repo* only. `sync.sh` reads the *live* machine
(`~/.claude/skills/`, `~/.claude/commands/`, `~/.config/zsh/`), which a pull never touches —
only `deploy.sh` refreshes those. So pulling first does **not** protect you.

This matters because `sync.sh` uses `rsync --delete` on `claude/skills/`,
`claude/commands/`, `gemini/agents/` and `gemini/config/projects/`. Syncing from a machine
whose live set is stale deletes from the repo every file that machine happens to lack, and
git records it as a deliberate removal. As of 2026-07-28 that is 30 skills and 3 commands.
`claude/agents/` is the only leg protected (additive, no `--delete`) — the rest are not.

Safe order on a machine that has been idle, or after a long gap:

```
git pull origin main     → repo up to date
bash deploy.sh           → LIVE machine up to date   ← the step that actually protects you
bash sync.sh             → now safe to push local state back
```

---

## Steps — deploy only (no local changes to push)

```
1. cd ~/ia-sync
2. git pull origin main
3. bash ~/ia-sync/deploy.sh              ← repo → ~/.config/zsh, ~/.claude/agents, etc.
4. bash ~/ia-sync/install-pkgs/run.sh update   ← apply out-of-repo installs deploy.sh can't
```

Step 4 is safe to run any time — it only installs what's new or stale on THIS machine.
Do not run sync.sh after a deploy-only session unless you actually changed local files.

---

## Authoring surface rule

**`claude/` and `zsh/` inside this repo are sync containers, not authoring surfaces.**

Files in `ia-sync/claude/agents/` and `ia-sync/zsh/` are copies synced FROM the live
machine files (`~/.claude/agents/`, `~/.config/zsh/`). They travel:

```
office ~/.claude/agents/<agent>.md
    → sync.sh  → ia-sync/claude/agents/<agent>.md
    → deploy.sh → home ~/.claude/agents/<agent>.md
```

- **Author in the live machine files.** Edit `~/.claude/agents/<agent>.md` or
  `~/.config/zsh/<file>.zsh` on the source machine. `sync.sh` carries the change in.
- **Never edit `ia-sync/claude/` or `ia-sync/zsh/` directly.** There is no
  composer-style install routine yet to make that safe — a direct edit here would
  be overwritten on the next sync from the machine, or silently diverge.
- **`install-pkgs/` is different** — it is ia-sync's own content (task files, README,
  `run.sh`), not a machine-config sync copy. Author there directly. See below.

---

## install-pkgs — the second deploy leg

`deploy.sh` only does what a plain rsync can: repo files → machine config locations.
Some things it **can't** do — install a Sublime plugin into `Packages/User/`, register
Claude hooks, `chmod` a script, edit a per-machine config outside the repo. Those live
in `install-pkgs/` as task files, and `install-pkgs/run.sh` applies them — a tiny local
package manager (AUR `-Syu`, home-made).

```
git pull        → repo up to date (task files travel as normal tracked content)
deploy.sh       → the plain-rsync leg  (configs, agents, zsh)
run.sh update   → the out-of-repo leg  (installs deploy.sh cannot do)
```

- **Task files ARE tracked** and travel by git like any repo content — no sync.sh copy step.
- **Install state is NOT synced.** It lives per-machine at
  `~/.local/state/ia-sync/installed.json`. Recording it in the repo would let office claim
  installed what home never ran — the same overwrite trap the invariant guards against.
- `run.sh list` shows what this machine needs; `run.sh update` applies auto tasks; manual
  tasks it gates and hands to you (`run.sh mark <slug>` when done). Full guide: `install-pkgs/README.md`.

---

## Conflict avoidance rules

**Machine config files are owned by their machine.**
- `config.home.zsh` — only home edits this file
- `config.office.zsh` — only office edits this file
- `zshrc.home` / `zshrc.office` — same ownership rule; folded from `~/.zshrc` on each machine
- Never cross-edit the other machine's config file

**Host-specific file pairs (sync → deploy symmetry):**

| Live location | Repo (zsh/) | Deploy target |
|---|---|---|
| `~/.config/zsh/config.zsh` | `config.{host}.zsh` | `~/.config/zsh/config.zsh` |
| `~/.zshrc` | `zshrc.{host}` | `~/.zshrc` |

Both legs must exclude these patterns from their bulk rsync — `sync.sh` excludes
`config.*.zsh` and `zshrc.*`, `deploy.sh` excludes `zshrc.*`. Without it, `sync.sh`'s
`rsync --delete` overwrites the *other* machine's config with whatever stale copy happens
to sit in this machine's `~/.config/zsh/`, and deletes the host files this machine lacks.
Caught 2026-07-28: office held a 07-20 `config.home.zsh` that would have silently reverted
home's `ai/base.zsh` fix. **Do not put these patterns in `sync.deny`** — that registry means
"must never exist in the repo", and its `find -delete` pass would erase them outright.

**A missing `zshrc.{host}` is the safe state — never stub it.**
`deploy.sh` overwrites `~/.zshrc` wholesale from `zshrc.{host}`. When that file is absent it
warns and skips, leaving the live file alone. Hand-creating an empty or placeholder
`zshrc.{host}` to "make it exist" passes the `-f` test and makes deploy copy the stub over
the machine's real `~/.zshrc`. Nothing requires the file to exist — not git, not the scripts.
The correct way to create it is to run `sync.sh` on that machine, which folds its real
`~/.zshrc` in. Same rule for `config.{host}.zsh`.

**deploy.sh backs up before it overwrites.**
`~/.zshrc` and `~/.config/zsh/config.zsh` are copied to `<file>.bak-YYYY-MM-DD` before being
replaced. One backup per file per day — a second deploy the same day keeps the first, so the
original pre-deploy state survives repeated bad deploys. `*.bak` / `*.bak-*` are in
`sync.deny`, so backups never travel back into the repo. Undo a bad deploy with
`cp ~/.zshrc.bak-<date> ~/.zshrc`.

**New wiring must be mirrored by hand, not assumed to propagate.**
- These files are NOT derived from each other and NOT auto-synced — each is hand-maintained by
  its own machine's seat (Kelvin @office, Maxwell @home).
- When you add a new `source`/signpost line to one machine's config (a new engine, a new scope
  wired in), the OTHER machine's config needs the equivalent line added deliberately, in the
  same session or flagged in the journal — it will NOT appear there on its own.
- Concrete example (2026-07-20): `config.office.zsh` sourced `ai/base.zsh` (the whole ai/ scope
  signpost); `config.home.zsh` never did. Silent gap — no error, no warning, the ai/ scope just
  never loaded on home. Caught only because commands from it were missing in a live shell.
- Before calling a wiring change "done": diff the two config files' `source`/signpost lines
  (ignore the machine-specific blocks, e.g. Docker-vs-native PHP) and confirm parity, or
  explicitly note in the journal why one machine intentionally lacks it.

**Agents are additive.**
- sync.sh never deletes agents from the repo via rsync
- To remove an agent: `git rm claude/agents/<name>.md` explicitly, then commit
- Never delete an agent file you didn't create

**sync.deny is the exclusion list.**
- If a local file must not enter the repo, add it to `sync.deny`
- Do not work around sync.deny by renaming files
- If you find a file in the repo that belongs in sync.deny, add it and `git rm` the file in the same commit

---

## For autonomous agents

Before touching ia-sync:

1. Run `git status` and `git log --oneline -3` — understand current state
2. If `git status` shows uncommitted changes: read them before adding more
3. If behind origin (`git fetch` shows new commits): pull first, always
4. Do not run sync.sh on behalf of the user without the user's explicit instruction in the current session
5. Write journal entries (`journal.host-cleanup.md`) to communicate cross-machine; do not commit config changes to the other machine's config file
6. If in doubt whether an action is safe: stop, write the journal entry, flag for the other seat

---

## Red flags — stop and flag before continuing

- `git status` shows files you did not touch
- `git pull` results in a merge conflict
- An agent file appears deleted that you did not delete
- A file in sync.deny appears in `git diff --staged`
- You are about to `git rm` more than 2 files at once

When a red flag appears: commit nothing, write a journal entry describing what you found, and leave the decision to the operator or the other machine's seat.
