# pad.3-pre-burn-exposure-audit — what is in git history, before the history is burned

> mode: MANNED (majkee driving, Flight seat) · date: 2026-07-30 · authored from: home
> **Purpose:** the operator intends to delete and recreate the GitHub repo, burning history.
> That removes the exposure — it also removes the ability to ever answer *"what did I
> expose?"* This pad is that answer, captured while it is still answerable.
> **No secret values appear in this file.** Every finding is location + kind + liveness.

---

### STEP 0 — why this pad exists at all

The repo is private (office verified via `gh`), so exposure is contained and a history burn
closes it. But a burn is irreversible in both directions: it destroys the leak **and** the
record of the leak. Ten minutes of enumeration now answers a question that is unanswerable
afterwards — chiefly *"is any exposed credential still live and therefore still needing
rotation, independent of the burn?"*

A history burn fixes **exposure**. It does not fix a **live credential**.

---

### STEP 1 — method

Scanned every commit on every ref with the **corrected** pattern — the one that catches
quoted keys, which the repo's own scanner cannot:

```
(password|passwd|secret|token|api[_-]?key|credential)[^a-z0-9]*["']?\s*[=:]
```

Raw hits: **10**, across 8 commits. Each was then inspected for *shape* — literal value vs
variable reference vs pattern definition — because a hit is not a finding.

**Result: 8 false positives, 2 real.**

---

### STEP 2 — the 8 false positives (recorded so nobody re-audits them)

| commit | file | why not a secret |
|---|---|---|
| `f6683cc` (2026-06-27) | `sync.sh` | the scanner's **own** pattern list |
| `511de2f` (2026-07-30) | `pad.2-home-deploy.md` | this session's write-up **of** the pattern |
| `60839b0` (2026-06-29) | `zsh/guides/sudoers.valet-php.conf` | `NOPASSWD:` sudoers directive |
| `f6683cc` (2026-06-27) | `zsh/ai-lifecycle.zsh:290,304` | `local token="${args[$i]}"` — a CLI arg-parser variable |
| `8a2201b` (2026-07-20) | `zsh/ai/gemini-processor.sh` | `${GOOGLE_API_KEY:-}` · `$(_gai_api_key)` · `${api_key}` — all **references**, no literal |
| `bc337d4` (2026-07-03) | `zsh/ai/processor.sh` | same family, same shape |
| `8a2201b` (2026-07-20) | `zsh/ai/devenv-sync-core.sh` | no literal on inspection |
| `c0d525a` (2026-07-30) | `zsh/archive/zshrc.home.legacy-*.zsh` | office's **redacted** copy — the scrub worked |

Worth stating plainly: the Gemini engines read their key from the environment and never
store one. That design is correct and held.

---

### STEP 3 — REAL #1 · FTP · `fantasyobchod.cz` · user `defaultfan`

- **Where:** `c648895` (2026-07-30) → `zsh/zshrc.home`, line 424, in a comment block
- **How it got in:** hand-imported from home's live `~/.zshrc` by @Flight, after a secret
  scan that reported "0 hits". The scan was case-sensitive uppercase with no `-i`, and its
  fallback check was read through `head -10`. **A wrong clearance, not a wrong report.**
- **Caught by:** office, same day, `c0d525a` (2026-07-30) — archive copy redacted
- **Still in:** git history on the remote; home's live `~/.zshrc` until office's 55-line
  rebuild is deployed
- **Liveness:** ✅ **CONFIRMED DEAD by operator, 2026-07-30.** `globalFantasyobchodStartScript`-era,
  unused. **No rotation required.** Burn closes it completely.

---

### STEP 4 — REAL #2 · MariaDB · `fantasyobchod` DB · user `majkee` ⚠ NEW

- **Where:** `d653ccf` (2026-06-29) → `guides/home-setup/diagnose_opencart_404.md`
- **Shape:** an OpenCart `config.php` example carrying a literal `DB_PASSWORD`, plus the same
  value repeated in a `mariadb -u majkee -p` walkthrough
- **⚠ Still in the CURRENT working tree** — 4728 b, dated 2026-06-29. This is **not** a
  history-only finding, so **the burn does not remove it.** It must be scrubbed from the
  working tree or the new repo inherits it on day one.
- **Liveness:** ⚠ **UNCLASSIFIED — needs operator call.** The username and database name are
  both real and match the live registry (`DB_USER=majkee`, `DB_NAME_FO=fantasyobchod`). The
  password value is weak and *looks* like a placeholder, which is exactly why it should be
  confirmed rather than assumed. Scope is a local MariaDB instance, so blast radius is small
  — but it is the credential `fo -db` uses.

**The structural point.** The correct home for this credential already exists and works:
`zsh/AGENTS.md:67` documents `.env/fo-db.cnf`, mode 600, with `.env` in `sync.deny`. The
secret-management design was right. **A documentation file bypassed it entirely** — the
credential leaked through prose, not through config.

---

### STEP 5 — three independent gaps in `sync.sh`'s secret scan

REAL #2 was invisible to the repo's own scanner for a **third** reason, on top of the two
already found today. All three are separate defects:

1. **Quote-blind pattern.** `\bpassword\s*[=:]` cannot match `"password":` or
   `DB_PASSWORD', '…'` — a quote sits between the word and the separator. Tested.
2. **Never runs on hand-added files.** It fires inside `sync.sh` only; anything committed
   by hand bypasses it. (Office's diagnosis — correct, but only one third of the story.)
3. **Does not cover the repo.** `sync.sh:177` scans exactly `$REPO/claude`, `$REPO/gemini`,
   `$REPO/zsh`. **`guides/` at repo root is outside all three** — as are `install-pkgs/`,
   `majkee/`, and the root scripts. REAL #2 has been sitting in an unscanned directory for
   a month.

A fix for any one of these alone would still have missed it.

---

### STEP 6 — history backup (taken before any burn)

```
~/ia-sync-history-backup/ia-sync.full-history.2026-07-30.bundle    638K, dir mode 700
```

Complete `git bundle --all`. Restorable with `git clone <bundle>`.

🔴 **This bundle contains both credentials.** It must never enter the new repo, never be
synced, and never be committed. It is a local forensic artifact only. If the FTP account is
dead and the MariaDB one is rotated, the bundle can simply be deleted.

---

### STEP 7 — burn checklist

1. **Scrub REAL #2 from the working tree first** — the burn does not touch it.
2. **Classify REAL #2** — rotate, or confirm dead like #1.
3. **Office must re-clone, not pull** — unrelated histories. And office must not push
   between the last sync and the cutover, or that work burns with the old remote.
4. **Commit bodies are the `/multihost` transport.** A burn deletes every prompt ever
   exchanged. Anything that must survive has to be in a **file** before the cutover — see
   `journal.history-index.md` (the exported log), and the two `_mail/flight/` handoffs.
5. Convert dangling SHA citations in the pads and `zsh/AGENTS.md` to date + subject.
   *(Done 2026-07-30 — 22 citations annotated. Note this must be redone for any commit
   referenced after a rebase: **rebase rewrites SHAs**, dates survive. That is the second
   reason the annotation exists.)*

### ⚠ UNTRACKED LOCAL STATE — the class that no commit can carry

The items below live outside the repo, survive nothing, and fail **silently on first use**.
A re-clone resets them all. None can be delivered by a commit, a mail file, or a deploy —
they must be re-established on each machine by hand, after the cutover.

| what | where | why it cannot travel |
|---|---|---|
| `/multihost` consumed marker | `~/.local/state/multihost/consumed` | deliberately outside every sync leg, so a marker can never travel and mark the other machine's mail read. Correct design; same property blocks the fix. |
| `pull.rebase = true` | `.git/config` | git config is never tracked. A fresh clone defaults to **merge**. |
| `env-vault` shared key | `~/.secrets/zsh/id.age` (mode 600) | outside the repo boundary by design. The seal is *additive*, so a working machine is safe on its own plaintext — but a **fresh clone has no plaintext to fall back on**, so without this key hand-copied in, `zsh/env.vault.age` cannot be opened. This is the third member home predicted. Added 2026-07-30 (pad.4). |

```sh
# BOTH machines, after re-cloning:
rm -f ~/.local/state/multihost/consumed        # office's is set; home's is absent
git -C ~/ia-sync config pull.rebase true       # set on home 2026-07-30; lost at re-clone
# copy the env-vault key back from your durable backup (NOT a typed command — a file):
#   install -m600 -D <backup>/id.age ~/.secrets/zsh/id.age
```

**Why `pull.rebase` is not cosmetic.** The `/multihost` receiver runs
`git log --reverse --grep='MACHINE<>MACHINE' "$LAST"..HEAD`, and the skill's own
justification is that git is *"authenticated, **totally ordered**, durable."* A merge commit
destroys that total order — two branches interleave by date instead of forming one line, so
"oldest first" stops being well-defined and the supersede rule (`a7e1b0f` supersedes six
others) can no longer be resolved by position. History currently has **zero** merge commits;
that has been held by discipline alone, un-enforced. `zsh/ai/devenv.zsh:7,21,32` already
hardcodes `pull --rebase` — but for `*.devenv` repos, not for ia-sync, which is the one repo
actually carrying the prompt bus.

---

### STEP 8 — this pad could not be committed under its own name

Filed after the fact, because it is a hazard and not merely a slip.

This pad was first written as `pad.3-pre-burn-secret-audit.md` and **silently refused entry
to the repo**: `.gitignore:5` carries `*secret*`, so the secrets guard swallowed the secrets
audit. `*credential*` on line 6 blocks the obvious second choice. Renamed to
`…-exposure-audit.md`, which trips neither.

Tested — of the natural vocabulary for this subject, only two words are unusable:
```
secret     IGNORED        password   ok
credential IGNORED        exposure   ok · audit ok · leak ok
```

**Why it went unnoticed for a full commit cycle:** `git add -A <dir>` skips ignored paths
*without an error*. `git status` then reports clean, because an ignored file is not untracked.
`git log` shows the commit. Every signal reads as success. The hint only appears when the
ignored path is named **explicitly** on the `git add` line.

Consequences at the time: commit `409ff6d` (2026-07-30) announced this pad in its message
and did not contain it; `install-pkgs/maintenance/README.md` advertised a file that was not
in the repo; the office handoff pointed at it. All corrected in the same commit as this note.

**Rule for anything under the ignore patterns:** never `git add -f` past a secrets guard to
land a document — rename the document. Forcing works once and teaches the next person that
the guard is advisory. And after any `git add` of a batch, verify with
`git diff --cached --name-only` that what you meant to commit is actually staged.

---

## Still open

- **REAL #2 liveness** — operator leans accept-as-local-dev (dev training data, never
  production); formal gavel pending. Only remaining blocker for bundle deletion.
- ~~REAL #2 scrub~~ — **DONE 2026-07-31** pre-burn: all THREE literals (this pad's summary
  listed two; a third sat at line 93 — found by full-file sweep with the corrected pattern).
- **`sync.sh` scan: all three gaps** — quote-blind pattern, hand-add bypass, and incomplete
  path coverage. None fixed. A pre-commit hook would close gaps 2 and 3 together.
  Mitigation since: secrets travel only as ciphertext (pad.4), so the scanner is no longer
  the last line for `.env` content.
- **The bundle** at `~/ia-sync-history-backup/` — delete once REAL #2 is gaveled.

## BURN EXECUTED — 2026-07-31 (office, majkee in the seat)

Checklist ran to completion: scrub ✓ · re-clone directive to home via reposoma mail ✓ ·
no-push window respected ✓ · survival-as-files held ✓. GitHub repo deleted (operator, web),
recreated private same-name; fresh history = single genesis commit `8da748a`. Local purge:
stash (verified duplicate) dropped, two `rescue/*` tags released (bundle covers them),
reflog expired, objects pruned — 1 reachable commit, credential sweep silent.
**Independent fresh-clone verification (Delta): PASS ×6** — history shape, credential
sweep, vault opens to live secrets, plaintext guards. Untracked-local-state rows
re-established on office (marker cleared, pull.rebase survived via kept .git/config,
key untouched). This pad is now a historical record of a closed episode.
