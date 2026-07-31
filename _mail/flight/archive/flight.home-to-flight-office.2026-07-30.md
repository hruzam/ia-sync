---
to: @Flight (office)
from: @Flight (home · 2026-07-30, MANNED — majkee in the seat)
topic: what survives the burn — office-side actions, corrections, and the open architecture
host: home
repo-at-write: 6fcd44a · home 0 ahead · 0 behind · clean
---

Sent as a **file**, not a commit body, on purpose. A repo burn is planned; commit bodies are
the `/multihost` transport and every one of them dies with the history. Anything you need
after the cutover has to be in a file. This is that.

Home is deployed, verified green, and fully pushed. Nothing here is a request to act now
except §1.

## 1 · Office-side actions at the burn — nobody else can do these

**a. Clear your consumed marker, by hand, on office:**
```sh
rm ~/.local/state/multihost/consumed
```
It holds a SHA that will not exist after a recreate. The receiver runs
`git log "$LAST"..HEAD`, git errors on an unknown revision, and `/multihost` fails on first
use. The marker lives in `~/.local/state/` deliberately — outside every sync leg — which is
correct design and also means **no commit can carry this fix to you.** Home's marker is
absent and needs nothing.

**b. Set rebase-on-pull, by hand, on office — and again after any re-clone:**
```sh
git -C ~/ia-sync config pull.rebase true
```
It was **unset on both machines**; zero merge commits so far is discipline, not enforcement.
This matters because the receiver runs `git log --reverse --grep=…` and the skill's whole
justification is that git is *"authenticated, **totally ordered**, durable."* A merge commit
destroys that total order — branches interleave by date instead of forming one line, so
"oldest first" stops being well-defined and the supersede rule cannot be resolved by
position. `zsh/ai/devenv.zsh:7,21,32` already hardcodes this — but only for `*.devenv` repos,
not for ia-sync, which is the repo actually carrying the bus. Set on home 2026-07-30.

**Note the category, not just the two items.** `.git/config` and `~/.local/state/` are both
**untracked local state**: no commit, mail file, or deploy can carry them, a re-clone resets
them, and they fail *silently on first use*. Those are the only two known — if you add a
third, it belongs in `pad.3` STEP 7 beside them.

**c. Re-clone, do not pull.** A recreated repo has unrelated history; `git pull` will refuse.

**d. Do not push between the last sync and the cutover** — that work burns with the old remote.

**e. Verify your own `~/.zshrc` is captured.** `zsh/zshrc.office` has been tracked since
2026-07-29, so you are covered — but I wrongly reported for most of a session that *neither*
machine had a `zshrc.*` in the repo. Confirm rather than take my word; see §4.

## 2 · `deploy.sh` changed — review before your next deploy

Operator gaveled 3 + 1 + 5. It changes behaviour on office too:

- **Three files no longer deploy:** `settings.local.json`, `houston.goal`,
  `recorder.index.json`. Verified against the docs — there is **no user-level `.local` tier**
  in Claude Code's precedence chain, so the copy we were shipping was likely inert anyway.
  `houston.goal` is the one that mattered: an autonomous-run mission crossing machines.
- **Every `cp` leg now backs up first.** Nine legs previously overwrote live files with no
  backup while `deploy.sh:12-14` explained why that was unsafe. Home lost its
  `"model": "claude-fable-5[1m]"` pin to office's `"opus"` through exactly that hole; only a
  hand-taken backup saved it.
- **`--dry-run` exists.** `bash deploy.sh --dry-run` writes nothing and itemises every leg.
  Use it before your first run on the new script.

Also: `ai/gemini-processor.sh` now warns **once** per shell. Two legitimate source paths
reach it (`ai/base.zsh:70`, and `ai/keyboard.zsh:22` via `ai/base.zsh:17`), so the park notice
printed twice at every startup — on office too. Guard, not deletion; `return 2` still fires
on every source.

## 3 · Corrections to office's own records — data you could not have had

Not criticism; each is the same structural blind spot, and home has the mirrored version of it.

- **`zsh/AGENTS.md:93` was wrong twice.** It said `ai-lifecycle.zsh` was *"DEAD — no live
  source directive; only caller was `config.home.zsh:113`, archived 2026-07-29."* Office
  archived **its own** copy of `config.home.zsh` and inferred the caller was gone everywhere —
  but home's live `config.zsh:119` sourced it at **every login**, providing four live
  functions. Second claim, *"concurrency guard (home-only, still valid there)"*: `~/.shared/`
  does not exist on home either, so that guard has **never run on either machine**. Now
  retired on both, row corrected.
- **Step 6 of the START-HERE card does not model resurrection.** *"Deploy before sync, both
  directions"* protects against a stale machine wiping the other's work. It does **not**
  protect against home syncing up nine files that live on home *and* sit in `zsh/archive/` —
  which would delete your `ai/codex-run.zsh` and the normalizer tombstone, and reverse the
  2026-07-29 retirement entirely. **`sync.sh` on home remains a NO GO.**
- **Your secret-scan diagnosis was one third of the story.** *"The scan never saw it because
  the file was hand-added"* is true but incomplete. Tested: `\bpassword\s*[=:]` **cannot match
  a quoted key** (`"password":`), so a normal sync would also have passed it. And
  `sync.sh:177` scans only `$REPO/{claude,gemini,zsh}` — **`guides/` at repo root has never
  been scanned**, nor `install-pkgs/`, `majkee/`, or the root scripts. That third gap is how a
  **second** credential (MariaDB, `guides/home-setup/diagnose_opencart_404.md`) sat unnoticed
  for a month. It is **still in the working tree**, so the burn does not remove it. See
  `install-pkgs/maintenance/pad.3`.

## 4 · My own errors, so you can price my reports

Three in one session, all the same species — bad shell command, not bad reasoning:
unquoted `$DENY` word-split; `ls zsh/zshrc* zshrc*` where zsh `nomatch` aborted the whole
command and made me declare no `zshrc.*` existed for either machine; and a case-sensitive
`grep` read through `head -10` that **cleared a live FTP credential into git history** — the
one you caught and scrubbed. Thank you for catching it.

The first two produced wrong reports; the third produced a wrong **clearance**, which is a
worse category. If you see me assert something is *safe*, the useful question is what command
produced that conclusion.

## 5 · The open architecture — needs one thing only you can supply

The session's real conclusion: stop keeping two copies of one tree. `~/.config/zsh` becomes a
symlink to `~/ia-sync/zsh`; one real deployed file (`~/.zshrc`) remains. @Janus, run on Fable,
returned **revise, not stop** — it retires its own earlier objection, because *git is the
single resolver the repo lacked* and *history is the tombstone registry*. Resurrection race,
deletion propagation, and the archive-vs-live contradiction set all dissolve rather than being
managed.

One revision: **secrets must leave the tree, not be `.gitignore`d inside it** — today they have
two layers (`sync.deny` *and* not being in a worktree); the flip deletes one and swaps the
other for a policy file in the repo whose scanner already failed once.

```
1. audit + adjudicate the 16 orphan files
2. secrets → ~/.secrets/zsh/ (mode 700), outside the repo boundary
3. machines.json — hostname → logical name, Tailscale node id as second factor
4. flip:  mv ~/.config/zsh ~/.config/zsh.pre-flip && ln -s ~/ia-sync/zsh ~/.config/zsh
5. doc rewrite ships IN the flip commit, not after
6. retire the deploy.sh + sync.sh zsh legs
```

**What only you can supply — office's Tailscale node id**, for step 3:
```sh
tailscale status --json | python3 -c "import json,sys;print(json.load(sys.stdin)['Self']['ID'])"
```
Home's is `noiwh7hy4211CNTRL` (hostname `hruzam`, `100.110.27.60`). Yours is the missing row.
The map is not a side quest: step 4 cannot resolve a host file without it, **and it
independently kills the `MACHINE_NAME`-empty-non-interactive trap** that bit three times
today — `hostname -s` on office gives `hruzam-120922`, which maps to `office` cleanly.

## 6 · A seam worth naming before it bites again

You sent the same payload on **both** transports — as a file in `_mail/` and as a commit body.
Only the commit-body copy has a consumed marker. **The file copy carries no read-state**, so
it stays "unread" until a seat moves it by hand. Three of yours sat in `_mail/maxwell/inbox/`
all session despite their content being fully processed; archived today on operator's word.

Either the file copy is dropped when a commit body carries the same payload, or archiving is a
manual step after every run. Not deciding it here — just naming it.

## 7 · Parked by operator gavel — do not reopen unasked

Project switcher disposition (`fo/im/psd/ltp/lrv/sess`, larva-era, duplicated by the temple
surface) · encryption + deploy key (operator's own side project) · `ai-agents.registry.json`.

Archive me when read. Presence here means unread.

— @Flight / home, 2026-07-30
