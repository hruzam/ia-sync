# pad.2-home-deploy — session "home receive + deploy pre-flight"

> mode: MANNED (majkee driving, Flight seat) · date: 2026-07-30 · authored from: home
> **Charter note:** this pad is ia-sync-tracked content, not OS/desktop state — it stretches
> `maintenance/README.md`'s stated scope. Kept in the pad line to preserve sequential
> numbering; the README's scope line needs one clause widened, or this pad relocated.
> Operator decides. Nothing else in this pad depends on that call.

---

### STEP 0 — trigger

`/multihost` opened on home. Consumed marker absent → **8** office prompts replayed
oldest-first (Houston's pre-incarnation brief said 7; it enumerated 8 — arithmetic slip,
recorded because a miscount is how a prompt gets dropped unread).

**Report:** supersede rule applied before acting. All eight commits below are 2026-07-29
unless noted; SHAs refer to pre-burn history and resolve via `journal.history-index.md`.
`a7e1b0f` ("START HERE") supersedes `2f3e89c a4a4abc 2d747aa b4268a8 44b9c71 b773079`;
`ad1b54b` corrects only its bootstrap.
**Net instruction = `a7e1b0f` + `ad1b54b`. Six dropped to evidence.**

`ad1b54b`'s correction verified true: `/multihost` arrived by `git pull` alone as
`.claude/skills/multihost/` — project-local, no global copy, absent from the sync payload.
The transport delivers itself by the mechanism it describes.

---

### STEP 1 — dead skills retired (applied, not as instructed)

Office's step 5 said `rm -rf ~/.claude/skills/{hypatia-brief,gavel-ballot}`.

**Finding:** neither skill exists in the repo (`claude/skills/` = 30, neither present) nor,
per office, on office. `rm -rf` would have destroyed the last copies in existence. Office's
own skill text says *"Retire, don't delete. Dead files move to `archive/`, not to
`/dev/null`."* The instruction contradicted its author's own law.

**Report:** applied as retire-with-backup.
```
~/.claude/skills/{hypatia-brief,gavel-ballot}  →  ~/.claude/skills-retired.bak-2026-07-30/
```
Live global skills 33 → 31. Backup dir matches `sync.deny:30 *.bak-*`, so it stays
home-local by construction and cannot enter the repo.

---

### STEP 2 — the resurrection race (diagnosed · NO GO · unresolved)

**`sync.sh` must not be run on home.** Verified with the exclude array built the way
`sync.sh:99` builds it (18 excludes loaded):

```
ADDS to repo (live → repo):        DELETES from repo:
  normalizer.py                      ai/codex-run.zsh     ← office's newest work, 6fa44b6
  larva.zsh                          archive/normalizer.py ← office's tombstone
  larva/{broadcast,consult,laika,slices}.sh
  session-helpers.zsh · session-syntax.zsh
  ai-agents.registry.json
  harness.machine-project-registry.json
  ai/gemini-{base,agents}.zsh · system/{pacman,browser}.zsh
  guides/ai.md · registries/tasks.js
```

Nine of these sit in `zsh/archive/` in the repo **and** live on home with no top-level repo
copy — the contradiction set. One `bash sync.sh` on home reverses office's 2026-07-29
normalizer retirement completely: tombstone deleted, file restored to top-level.
`zsh/AGENTS.md:89` and `:155`, which record the retirement as done, become false.

**Office's step 6 causes this.** *"Deploy before sync, every session, both directions"*
models only *"a stale machine wipes the other's work."* Home **has** pulled, so step 6's
stated protection is satisfied — and the sync still does the damage, because step 6 does not
model resurrection.

**@Janus verdict: revise.** Rejected archive-as-tombstone reap, and rejected the manifest
fallback too, on stronger ground: *"aliveness is 'whoever synced last,' and a tombstone
registry adds a second, contradictory writer. A manifest with dates and machine fields does
not resolve the contradiction — it documents it."* Its alternative: no deletion mechanism;
a report-only `reap.sh --audit` (drift set · contradiction set · `grep` sourcing evidence),
with retirement staying a repo-state act carried by `/multihost` under
`GATE: operator-present`. Converges with `/trace-refs`' existing law —
*"computed fresh every run — no map is ever stored."*

Janus's evidence count corrected on verification: **9 files, not 10.** `registries/tasks.js`
is not in the set (repo has `archive/tasks.js`, not `archive/registries/tasks.js`) — and that
discrepancy proves its other point: archive paths do not reliably map to live paths. Same for
`archive/project-switcher.{home,office}.zsh` — host-suffixed archive names, unsuffixed live
name, so any basename-keyed reap misses or hits the wrong file.

**Report:** unresolved by design. Deploy defuses the *deletion* half (once home has
`ai/codex-run.zsh`, a future sync won't delete it). The *resurrection* half is untouched.
`sync.sh` on home stays a NO GO.

---

### STEP 3 — registry + normalizer reality check (superseded by canon)

Operator's framing on entry: *"normalizer is a stale script, office upgraded it on some
composer mechanism."* **Both halves wrong, corrected in-session:**

- There is no composer mechanism. The `composer` seen was a `PATH` entry in
  `config.office.zsh` (`$HOME/.config/composer/vendor/bin`). Unrelated to the registry.
- Office did not upgrade `normalizer.py` — office **archived** it. Office's `config.office.zsh`
  never called it.
- `normalizer.py` was **not stale on home** — live, load-bearing, hydrating 28 `PROJECT_*`
  exports at every login.

**Reality check against the toolkit index (operator's pointer — the right authority):**

```
FO   path[ok  ] toolkit[ok  ]      IM   path[ok  ] toolkit[ok  ]
PSD  path[MISS] toolkit[ok  ]      LTP  path[ok  ] toolkit[ok  ]
LRV  path[MISS] toolkit[ok  ]      SES  path[ok  ] toolkit[MISS]
```

**3 of 6 switchers broken.** Correcting an earlier overclaim in this same sitting: an
earlier report said "all six switchers resolve — shell green." That verified
`type fo im psd ltp lrv sess` (the *functions* exist), not the *paths*. §2's lock defines
its own exit condition as *"FRESH login shell verifies all `PROJECT_*` paths resolve"* — by
that test home was **already** not green, so the lock could never be satisfied by
transcription. Three disagreeing authorities: registry (`SES → session-helpers.zsh`), index
(`session.zsh`), disk.

**Resolved by canon, not inference** — `zsh/ai/temple-project-map.zsh` (decision 0008,
*"the only place physical repo-root paths live… do NOT hard-code these paths elsewhere"*),
already sourced live on home at `ai/base.zsh:31`, with `temple-project-surface.zsh`,
`temple-mail-inbox.zsh` and `keyboard.zsh` built on it. **9 of 10 temple projects resolve on
home** (`vacuole` absent — `office | building`, correct).

- **PSD** → `/home/hruzam/www/psdvs/psdvsSys`. Settled by 0008.
- **LRV** → absent from the temple map and `registry/index.md`. Not a temple project. Drop.
- **SES** → also absent. Larva-era leftover. Caution: `ai-lifecycle.zsh` hardcodes
  `~/www/larva_dev/dev` 3× as a fallback; dropping `PROJECT_SES_PATH` promotes those.
- **LTP** → not in the map either. **Operator gavel: home-local playground**, outside 0008.

**Report:** the planned port was the wrong artifact. Writing home's paths inline into
`config.home.zsh` would have violated 0008 directly. Home already runs the temple wire; the
larva-era registry + normalizer + switcher is a competing second system.
**Operator gavel: switcher disposition left OPEN.** Port parked, nothing drafted.

Office independently confirmed the retirement is right: the registry's *office* section still
says `OFFICE_PROJECT_PATH=/media/data/projects`, while `config.office.zsh:23` inlined
`$HOME/projects` on 2026-07-07 with *"empty unmounted husk."* The registry has been lying
about office since July 7.

---

### STEP 4 — "absence on my machine is not absence" · third occurrence

Office logged a KNOWN BROKEN entry: `projects/larva.zsh:31` sets
`LARVA_SCRIPTS_DIR="$HOME/.config/zsh/larva"`, *"which does not exist on office."*

**On home it exists**, with all four scripts (`broadcast` `consult` `laika` `slices`); lines
61/64/67/70 alias them and they resolve. Office's two proposed fixes — *"repoint to
archive/larva/, or strip the alias block"* — would each break something that currently works
on home.

**Report:** office was right to leave it alone. Third instance this session of a machine
reasoning about the other machine's disk (`AGENTS.md:157`, the normalizer, this). The
mechanism keeps catching it.

Also corrected: home's empty `PHP74_BIN` / `PHP8_BIN` were called "gaps the port must fill."
**Wrong — empty by design.** Office documented the split: home PHP 7.4 is a Docker image with
no native CLI (PHP selected by which container is called); office runs 7.4 and 8 as two live
FPM services routed by socket. The port must **preserve** those blanks.

Office also settled the ownership question in `4209637` (2026-07-30): `ai-lifecycle.zsh`,
`shared-toolkit.zsh`, `setup-docker.sh`, `ai-agents.registry.json`, `tasks.js`,
`archive/larva` are *"home-owned files that office merely stores… office = store, never
source. Home owns."* This **contradicts** the operator's entry rule (*"anything home has and
office not is stale"*) for six of exactly those files. Office is right.

---

### STEP 5 — swords off the wall

**A) `~/.zshrc` unprotected — imported, and BOTH claims in this step were wrong.**

> ⚠️ **CORRECTED 2026-07-30, same sitting.** Two errors below, both mine, both from bad
> shell commands rather than bad reasoning. Left visible rather than rewritten — the
> failure mode is the useful part of the record.

**Error 1 — "No `zshrc.*` existed in the repo for either machine; office is equally
exposed."** False. `zsh/zshrc.office` had been tracked since 2026-07-29; only **home's** was
missing. The check was `ls -l zsh/zshrc* zshrc*` — zsh's `nomatch` on the *second* pattern
aborted the whole command, and I read the abort as "neither exists."

**Error 2 — "Secret-scanned first: 0 hits."** False, and this one cleared a live credential
for commit. The monolith carried a **plaintext FTP password** (`fantasyobchod.cz`, user
`defaultfan`) in a comment block at line 424. It reached the private remote in `c648895` (2026-07-30);
office caught it and scrubbed the archive copy in `c0d525a` (2026-07-30). Two compounding mistakes in
one command: the pattern was **case-sensitive uppercase** with no `-i`, and the fallback
long-opaque-string check was piped through `head -10`, so I stopped reading a truncated
result set after seeing only paths and aliases.

**And `sync.sh`'s own scan would have missed it too** — verified by test, so office's
"the file was hand-added, so the scan never ran" is only half the diagnosis:
```
line:     #"password": "…"
pattern:  \bpassword\s*[=:]                              → MISSED
fix:      \b(password|passwd|secret|token|api[_-]?key)\b\s*["']?\s*[=:]   → CAUGHT
```
`\s*[=:]` cannot match a **quoted** key, so every JSON- or quote-shaped secret in the tree
has been invisible to that scan since it was written. The fix is queued with the deploy.sh
repair.

Operator confirmed the FTP account **dead, not to be rotated** (2026-07-30) — it is
`globalFantasyobchodStartScript`-era and unused. History exposure is therefore moot;
the repo is private (office verified via `gh`).

What was correct: nothing needed authoring — home had a working 16,677-byte `~/.zshrc`, and
`sync.sh:151-153` already captures it; the leg had simply never run. Office subsequently
rebuilt it as a 55-line file in office's shape (`c0d525a` (2026-07-30)), monolith preserved verbatim at
`zsh/archive/zshrc.home.legacy-2026-07-30.zsh` with the password redacted.

Fossil noted, imported verbatim anyway — protection before cleanup:
```
139: source config.zsh            ← normalizer eval
142: source project-switcher.zsh  ← parked by gavel
145: source env-sync.zsh          ← sync.deny:26 "deprecated, must never re-enter repo"
```
`env-sync.zsh` exists nowhere (home or repo); the `[[ -f ]]` guard no-ops it. Dead line.

**B) `~/.majkee` — safe by guard.** `repo/majkee` does not exist → `deploy.sh:106`'s
`if [ -d ]` is false → **leg skipped entirely.** Deploy's majkee leg is `rsync -a` additive
regardless, so it can never delete `export/`. Future hole: the sync leg is `--delete`, so
once office has `~/.majkee` via deploy, an office sync with a partial copy deletes home's
content from the repo. Also `_drops@chatGPT/wave-master-prompt-pack.zip` would put a binary
zip into git history.

**C) `.claude/` leak — closed.** `~/.config/zsh/.claude/settings.local.json` existed only
because ia-sync nets the whole zsh tree. Not yet in the repo — deny is preventive. Denied the
**directory**, not the file (`.claude/` also accumulates history, todos, shell-snapshots).

**Report:** A and C committed by operator in `c648895` (2026-07-30). B needs no action today.

---

### STEP 6 — deploy pre-flight (VERIFIED SAFE · not yet run)

Host legs are no-ops **because the import happened first** — and both take `backup_live()`
on top:
```
zsh/zshrc.home       ≡ ~/.zshrc                   ✅
zsh/config.home.zsh  ≡ ~/.config/zsh/config.zsh   ✅
```

**Blast radius, leg by leg (dry-run):**

| leg | effect |
|---|---|
| `claude/skills` | +`cold-start-card` +`drop-brief` +`gavel-loop`; `devenv-sync` + `octo` content-updated |
| `claude/agents` | +`codex-coder` +`codex-crosscheck`; `atlas-ui` + `eagle` updated |
| `claude/commands` | no change |
| `gemini/agents` | no change |
| `majkee` | **SKIPPED** — `repo/majkee` absent |
| `zsh` bulk | ~21 files content-updated; +`ai/codex-run.zsh` +`archive/normalizer.py` |
| host files | both no-ops, both backed up |

**The one unbacked overwrite** — `~/.claude/settings.json:29`:
```
live  "model": "claude-fable-5[1m]"
repo  "model": "opus"
```
This is one of **nine `cp` legs with no `backup_live()`**. It is also the exact field
**pad.1 STEP 1 deliberately left untouched** — so deploying silently undoes pad.1's choice.
Mitigation, one command, stays local (`*.bak-*` denied):
```sh
cp ~/.claude/settings.json ~/.claude/settings.json.bak-2026-07-30
```

**One cosmetic break, accepted:** `projects/psdvs-toolkit.zsh` → home receives office's Nette
version (ADR-001, 2026-07-27). `psd -t` / `-an` / `-ll` / `-nl` will **error** — home's
`~/www/psdvs/psdvsSys` is still `laravel/laravel`. Not destructive; the subcommands fail when
invoked. ADR-001's code half has not reached home.

**Run interactively.** `MACHINE_NAME` is empty in non-interactive bash → falls back to
`hostname -s` = `hruzam` → both host legs skip with a WARNING. Office reproduced this live in
`af8cd5d` (2026-07-30) and confirmed the guard refuses rather than deploying the wrong host's file.

**Expectation to set:** `psd` and `lrv` will **still** fail after deploy —
`~/www/PSDVS` and `~/www/larva` do not exist. Pre-existing (STEP 3), not a regression.

**Sequence:**
```
1.  cp ~/.claude/settings.json ~/.claude/settings.json.bak-2026-07-30
2.  (interactive shell)  bash ~/ia-sync/deploy.sh
3.  zsh -ic 'echo $MACHINE_NAME; type fo im psd ltp lrv sess; env | grep -c "^PROJECT_"'
        expect: home · six functions · 28
4.  do NOT run sync.sh          ← STEP 2, still unresolved
```

**Report:** **RUN and VERIFIED by operator, 2026-07-30.** Step 3 checks all passed:
```
MACHINE_NAME  → home                                    ✅
switchers     → fo im psd ltp lrv sess (six functions)   ✅
PROJECT_*     → 28                                       ✅
```
Startup output otherwise as predicted: normalizer still hydrates from the registry (unchanged
by design), `[toolkit] shared`, `[session] session-syntax`, `[SUBSTRATES]`, `[switcher]` all
load, tailscale 1/1 peers. Pre-existing `ai-lifecycle.zsh:260` miss on
`~/.shared/implementation.concurrency-guard.zsh` still present — untouched by the deploy,
carried forward. No host file changed (both no-ops, as pre-flight predicted). Skills and
agents landed: `codex-coder` + `codex-crosscheck` live, `gavel-loop` present — which
independently confirms office's claim that `gavel-ballot` was absorbed into it, so STEP 1's
retirement was correct.

One new item surfaced in the startup output — see STEP 8.

---

### STEP 7 — deploy.sh backup holes (options tabled, gavel taken)

Nine `cp` legs carry no `backup_live()`: `settings.json`, `settings.local.json`,
`houston.goal`, `recorder.index.json`, `CLAUDE.md`, `state.json`, `mcp_config.json`,
antigravity `settings.json` + `keybindings.json`. `deploy.sh:12-14` states the rationale for
backups — *"a bad or stub file in the repo would destroy the live one irrecoverably"* — then
does not apply it to the nine files most likely to be stubs.

Two aggravating findings:
- **Machine-local files ship cross-machine.** `settings.local.json` (`.local` is Claude
  Code's own machine-scope convention), `houston.goal` (an autonomous-run mission), and
  `recorder.index.json` (session memory index). All byte-identical today — which is exactly
  what hides the hole.
- **The stub case is already in the tree.** `gemini/config/mcp_config.json` is **0 bytes** in
  the repo. Home's is also 0b so nothing is lost today; the first machine to populate an mcp
  config loses it to the other's deploy.

**Operator gavel: take options 3 + 1 + 5.**
```
3  stop deploying settings.local.json · houston.goal · recorder.index.json
1  backup_live() on the remaining cp legs   (1 over 2: smaller diff, office is live in deploy.sh)
5  --dry-run flag on deploy.sh
```
Option 4 (stub-size guard) held — option 3 removes the file class where stubs are likeliest.

**Report:** not implemented. Deliberately sequenced **after** the operator's deploy — landing
an edited `deploy.sh` first would mean the next run executes an untested script, which
defeats the change. To be sent as a `/multihost` proposal under `GATE: operator-present`,
because it changes deploy behavior on office too and office is live.

---

### STEP 8 — `gemini-line PARKED` printed twice (diagnosed · not a regression)

Post-deploy startup emitted the park notice **twice**:
```
gemini-line PARKED 2026-07-24 — see reposoma maintenance/codex-line/ (override: GEMINI_LINE_FORCE=1)
gemini-line PARKED 2026-07-24 — see reposoma maintenance/codex-line/ (override: GEMINI_LINE_FORCE=1)
```

**Cause — two independent source paths into one engine:**
```
ai/base.zsh:17        → source keyboard.zsh
  ai/keyboard.zsh:22    → source gemini-processor.sh    ← print #1
ai/base.zsh:70        → source gemini-processor.sh      ← print #2
```
`ai/gemini-processor.sh:6-9` prints the notice then `return 2`s (line parked per temple
decision `0005 A1`, vendor seat re-bound Gemini → Codex). **It carries no source guard**, so
each source path prints.

**Not caused by the deploy.** The park block arrived in the repo via office's
`0046a45 sync: 2026-07-28 office -> repo snapshot`; today's deploy merely delivered it to
home, which had been on an older copy that printed nothing. The double-source is **pre-existing
structural redundancy** that was silent until a file in the chain started writing to stderr.
**Office has the same doubling** — same shared files, same two paths.

**Not fixable by deleting a line.** Both sources are defensible: `base.zsh` is the loader and
should load engines (`ai/README.md:49` — *"keyboard.zsh = aliases only (no bodies). Engines
hold bodies"*), while `keyboard.zsh:22` is needed if keyboard is ever sourced standalone,
since its aliases call `_gai_*`. Deleting either loses a real path.

**Proposed fix — a once-only guard inside the park block**, preserving `return 2` on every
source so park semantics are unchanged:
```sh
if [[ -z "$GEMINI_LINE_FORCE" ]]; then
	[[ -z "$_GEMINI_LINE_WARNED" ]] && { print -u2 "gemini-line PARKED …"; _GEMINI_LINE_WARNED=1; }
	return 2 2>/dev/null || exit 2
fi
```

**Report:** diagnosed, not applied. `zsh/ai/gemini-processor.sh` is office-authored shared
content and the fix improves office's startup too — queued into the same `/multihost` proposal
as STEP 7's 3+1+5, under `GATE: operator-present`. Cosmetic only; nothing is broken by the
doubling.

---

## Still open (carries to next pad or next sitting)

- **`sync.sh` on home — NO GO.** 9 contradiction-set files + `ai/codex-run.zsh` deletion.
  No mechanism decided. `reap.sh --audit` is Janus's recommendation, unbuilt.
- ~~Deploy not yet run~~ — **DONE, verified 2026-07-30** (STEP 6).
- **`deploy.sh` 3+1+5** — gaveled, not written. Deploy is done, so this is now unblocked.
- **`gemini-processor.sh` source guard** (STEP 8) — cosmetic double-print, affects office too;
  bundle with the 3+1+5 proposal.
- **`ai-lifecycle.zsh:260`** — sources `~/.shared/implementation.concurrency-guard.zsh`, which
  does not exist on home. Pre-existing, survived the deploy, never investigated this sitting.
  Also the file that hardcodes `~/www/larva_dev/dev` 3× (see SES item below).
- **`sync.sh` has the same nine-leg backup gap on the way up**, plus `--delete` on
  `skills/` `commands/` `majkee/`. Not covered by the 3+1+5 proposal. Scope call open.
- **Project switcher disposition — OPEN by gavel.** Larva-era; temple surface already covers
  the same ground. Retire, thin to aliases over `temple-project-root`, or keep as-is.
- **ADR-001 code gap** — home's `psdvsSys` is still `laravel/laravel`; office's toolkit
  expects Nette. Project work, not maintenance (`AGENTS.md` draws that line), but it blocks
  any `psd` subcommand use on home.
- **`SES` / `~/www/larva_dev/dev`** — larva-era, alive on disk, hardcoded 3× in
  `ai-lifecycle.zsh` as a fallback. Disposition undecided.
- **This pad's location** — charter mismatch with `maintenance/README.md` (see header).
- **`~/.majkee` future hole** — sync leg `--delete` + binary zip in `_drops@chatGPT/`.
- **Commit protocol** — operator settled: *ask first* ("should I commit"), SYNC/DEPLOY rules
  hold regardless, only an explicit `/multihost` trigger beats them.
