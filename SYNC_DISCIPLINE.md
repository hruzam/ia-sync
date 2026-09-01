# ia-sync — Sync Discipline

Applies to: **all operators** — human (@majkee) and autonomous agents (any seat, standing or ad-hoc).

---

## Doctrine — compose-first (operator gavel, 2026-07-31)

**This repo is the authoring surface — the surgical table ("compose").
All deployable edits are cut HERE, then deployed outward. Nothing flows
machine → repo by bulk copy.**

```
edit in ~/ia-sync  →  commit  →  push
                                   ↓ (other machine)
                       pull  →  deploy.sh  →  live machine
```

Consequence: **`sync.sh` (the harvest leg) is RETIRED** — see its section below.
The live trees (`~/.claude/`, `~/.config/zsh/`, `~/.gemini/`) are deployed copies.
`zsh/AGENTS.md` has said it since before the burn: *"Truth is living THERE: `~/ia-sync`
(the surgical table). Cut in ia-sync, deploy outward."* This file now agrees.

---

## The invariant

**Pull before you push. Always. No exceptions.**

Both machines commit to this repo. If you push without pulling first, you overwrite
what the other machine committed. This is how traps happen.
`pull.rebase=true` is set on both clones — keep it that way.

---

## Steps — every working session

```
1. cd ~/ia-sync
2. git pull --rebase origin main     ← receive other machine's work first
3. edit repo files                   ← the authoring surface is HERE
4. bash deploy.sh --dry-run          ← preview what would change on this machine
5. bash deploy.sh                    ← apply to THIS machine
6. git add … && git commit -m "<scope>: <one line>"
7. git push origin main
```

Machine identity auto-resolves via `machines.json` (`hostname -s` → logical name);
`MACHINE_NAME=<name>` remains available as an explicit override.

**A live-machine edit that never lands in the repo is a dead edit** — the next
`deploy.sh` overwrites it (with a dated `.bak` for the covered files, silently for the
rest). If you experimented live, fold the change back into the repo in the same session.

---

## Steps — deploy only (receiving the other machine's work)

```
1. cd ~/ia-sync
2. git pull --rebase origin main
3. bash ~/ia-sync/deploy.sh              ← repo → ~/.config/zsh, ~/.claude/agents, etc.
4. bash ~/ia-sync/install-pkgs/run.sh update   ← apply out-of-repo installs deploy.sh can't
```

Step 4 is safe to run any time — it only installs what's new or stale on THIS machine.

---

## RETIRED: sync.sh — do not run, on either machine (2026-07-31)

Under compose-first the harvest direction has no job: there is nothing legitimate on a
live machine that the repo should learn about by bulk copy. What retiring it kills:

- the **`rsync --delete` trap** — syncing from a machine with a stale live set deleted
  from the repo every file that machine lacked, recorded as deliberate removals
  (the 30-skills/3-commands near-miss, 2026-07-28);
- the **resurrection race** (pad.2) — a stale live tree re-injecting content the repo
  had deliberately dropped;
- the **"deploy before sync" ordering rule** that existed only to soften the two above.

The script stays in the tree as reference/history. Running it is a red flag, not a
workflow. If you believe a live file diverged from the repo in a way worth keeping,
copy that one file into the repo **by hand, reviewed, in a normal commit** — never by
bulk harvest.

---

## Authoring surface rule (inverted 2026-07-31 — this replaces the old rule verbatim)

**`claude/`, `zsh/`, `gemini/` inside this repo ARE the authoring surfaces.**
The live machine trees are deploy targets, not sources.

- **Author here.** Edit `ia-sync/claude/agents/<agent>.md`, `ia-sync/zsh/<file>.zsh`,
  then deploy. The old rule ("author in live files, sync.sh carries it in") is dead.
- **Machine-local content never enters the repo**: secrets plaintext (`.env/`,
  `secrets.zsh`), backups (`*.bak*`), per-machine state. `sync.deny` +
  `.gitignore` are the registries — see below.
- **`install-pkgs/` is unchanged** — it was always ia-sync's own authored content
  (task files, README, `run.sh`). Author there directly; guide: `install-pkgs/README.md`.

---

## install-pkgs — the second deploy leg

`deploy.sh` only does what a plain rsync can: repo files → machine config locations.
Some things it **can't** do — install a Sublime plugin into `Packages/User/`, register
Claude hooks, `chmod` a script, edit a per-machine config outside the repo. Those live
in `install-pkgs/` as task files, and `install-pkgs/run.sh` applies them — a tiny local
package manager (AUR `-Syu`, home-made).

- **Task files ARE tracked** and travel by git like any repo content.
- **Install state is NOT synced.** It lives per-machine at
  `~/.local/state/ia-sync/installed.json`. Recording it in the repo would let office claim
  installed what home never ran — the same overwrite trap the invariant guards against.
- `run.sh list` shows what this machine needs; `run.sh update` applies auto tasks; manual
  tasks it gates and hands to you (`run.sh mark <slug>` when done).

---

## Conflict avoidance rules

**Machine config files are owned by their machine's seat.**
- `config.home.zsh` — only home edits this file (home seats)
- `config.office.zsh` — only office edits this file (Kelvin / office seats)
- `zshrc.home` / `zshrc.office` — same ownership rule
- Never cross-edit the other machine's config file. Ownership is about **who edits**,
  not where the file lives — both files sit in this repo, authored here (compose-first).

**Host-specific file pairs (repo → deploy):**

| Repo (zsh/) | Deploy target |
|---|---|
| `config.{host}.zsh` | `~/.config/zsh/config.zsh` |
| `zshrc.{host}` | `~/.zshrc` |

**A missing `zshrc.{host}` is the safe state — never stub it.**
`deploy.sh` overwrites `~/.zshrc` wholesale from `zshrc.{host}`. When that file is absent
it warns and skips, leaving the live file alone. Hand-creating an empty placeholder passes
the `-f` test and makes deploy copy the stub over the machine's real `~/.zshrc`. The
correct way to create it: the owning machine's seat authors it **in the repo**,
deliberately, from its real live file — one reviewed commit. Same rule for
`config.{host}.zsh`.

**deploy.sh backs up before it overwrites.**
`~/.zshrc` and `~/.config/zsh/config.zsh` are copied to `<file>.bak-YYYY-MM-DD` before
being replaced. One backup per file per day — a second deploy the same day keeps the
first. `*.bak` / `*.bak-*` are deny'd, so backups never enter the repo. Undo a bad
deploy with `cp ~/.zshrc.bak-<date> ~/.zshrc`.

**New wiring must be mirrored by hand, not assumed to propagate.**
- The two machine config files are NOT derived from each other — each is hand-maintained
  by its own seat.
- When you add a `source`/signpost line to one machine's config, the OTHER machine's
  config needs the equivalent line added deliberately, in the same session or flagged in
  the journal — it will NOT appear there on its own.
- Concrete example (2026-07-20): `config.office.zsh` sourced `ai/base.zsh`;
  `config.home.zsh` never did. Silent gap — the whole ai/ scope just never loaded on home.
- Before calling a wiring change "done": diff the two configs' `source`/signpost lines
  (ignore machine-specific blocks, e.g. Docker-vs-native PHP) and confirm parity, or note
  in the journal why one machine intentionally lacks it.

**Agents are additive on deploy; removals are explicit.**
- `deploy.sh` never deletes live agents.
- To remove an agent: `git rm claude/agents/<name>.md`, commit — then each machine deletes
  its live copy deliberately (deploy being additive means removal does not propagate).
- Never delete an agent file you didn't create.

**sync.deny + .gitignore are the "never in the repo" registries.**
- `sync.deny` means "must never exist in the repo" (secrets, backups, machine-local
  state). It outlives sync.sh as a declaration and audit list.
- Do not work around it by renaming files.
- If you find a file in the repo that belongs there: add the pattern and `git rm` the
  file in the same commit.
- **Do not put `config.*.zsh` / `zshrc.*` patterns in `sync.deny`** — those MUST exist in
  the repo (they are the authored host files); deny means "never in repo".

---

## For autonomous agents

Before touching ia-sync:

1. Run `git status` and `git log --oneline -3` — understand current state
2. If `git status` shows uncommitted changes: read them before adding more
3. If behind origin (`git fetch` shows new commits): pull first, always
4. **Never run `sync.sh`** — retired 2026-07-31; single-file hand-copies into the repo
   only, reviewed, in a normal commit
5. Write journal entries (`journal.host-cleanup.md`) to communicate cross-machine; do not
   edit the other machine's config file
6. If in doubt whether an action is safe: stop, write the journal entry, flag for the
   other seat

---

## Red flags — stop and flag before continuing

- `git status` shows files you did not touch
- `git pull` results in a merge conflict
- An agent file appears deleted that you did not delete
- A deny'd file appears in `git diff --staged`
- You are about to `git rm` more than 2 files at once
- **Anyone — human or agent — runs or proposes running `sync.sh`**

When a red flag appears: commit nothing, write a journal entry describing what you found,
and leave the decision to the operator or the other machine's seat.
