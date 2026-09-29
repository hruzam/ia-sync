---
title: Design — publish-gate (core buffer model + ia-sync deploy adapter)
status: "head-reviewed 2026-09-29 — ready for Cartan's CHALLENGE (9 head corrections: beacon on drop · deploy.sh gains no --ref · status name · prefix push <sha>:main · remote check via ls-remote as its own step · manifest location · r3 vocabulary · snapshot purity · §5 receipt numbering) · OQ1 decided by majkee 2026-09-29: droppable, with its own command and button"
date: 2026-09-29
author: trajectory (design author, publish-gate-00-design)
inputs:
  - /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/RUNBOOK.md
  - /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/STATUS.md
  - /home/hruzam/ia-sync/deploy.sh
  - /home/hruzam/ia-sync/SYNC_DISCIPLINE.md
  - /home/hruzam/ia-sync/zsh/AGENTS.md (sync/ scope + control-panel convention)
  - /home/hruzam/ia-sync/zsh/sync/base.zsh, keyboard.zsh (live control-panel example)
  - /home/hruzam/ia-sync/zsh/registries/gen-temple-map.sh
  - git -C ia-sync show 9bb608b:.dev/session/runbook-upgrade-02-app/raw/cartan.publish-gate-boundary.2026-09-25.md (Cartan's boundary memo — folded point by point, §7)
  - git -C ia-sync show 9bb608b:.dev/session/runbook-upgrade-02-app/raw/draft.majkee.app-scheme.2026-09-23.md §3.5.4 (historical resource-model context)
  - git -C ia-sync show 9bb608b:.dev/session/runbook-upgrade-02-app/raw/TRAJECTORY-CARTAN-research.hardcoded-boundaries.2026-09-24.md (flock / lock-file patterns)
  - /home/hruzam/unikuklatrix/nablarva/.dev/session/muticula-01-qualify/raw/muticula.master.2026-09-26.md (r3 — current muticula design)
verified-live-facts:
  - "deploy.sh — one $REPO source var, no --delete anywhere, no deployed-commit record, one repo-writing step (gen-temple-map.sh before the zsh rsync); flags only --dry-run/-n and --codex-only; legs claude, codex, gemini, majkee, nano, zsh"
  - "gen-temple-map.sh (zsh/registries/) writes zsh/ai/temple-project-map.zsh from registries/projects.json; --check exits 3 on drift, --stdout prints without writing"
  - "ia-sync's .git is a plain repo, not a worktree; git-common-dir == .git"
  - "commit trailers in use: Co-Authored-By (Claude model) and Claude-Session (url); no host trailer exists today"
---

# Design — publish-gate

This is a design, not an implementation. It answers RUNBOOK prompt-0's items (1)–(7), then
gives the muticula boundary the depth the RUNBOOK's boundary list asks for, then names what
is still open for majkee. `(?)` marks a proposal to architect — never an order (operator
convention, carried from `zsh/AGENTS.md`).

---

## (1) Buffer model

**Scope.** One buffer per `(host, checkout)` pair — the same host-local, git-common-dir-local
scoping muticula uses for its own state (`muticula.master.2026-09-26.md` §3 D2). A buffer
is never a cross-host object; there is no "office's buffer, viewed from home."

**Contents.** The buffer is the ordered list of commits reachable from local HEAD that are
not on the configured upstream:

```
git rev-list --reverse origin/main..HEAD          # oldest first — this repo's history is linear by discipline
```

Each entry carries:

| Field | Source | Notes |
|---|---|---|
| `sha` | the commit | immutable identity |
| `subject`/`body` | `git log -1 --format=%B` | shown verbatim in the plan (§4) |
| `authored_by` | trailers when present, else `%an <%ae>` | **[verified]** actual trailers here: `Co-Authored-By: Claude <model> <noreply@anthropic.com>`, `Claude-Session: <url>` — no host trailer exists. Best-effort provenance, never access control (Cartan: "must not infer authorship from Git author/trailers"). |
| `legs_touched` | `git diff --name-only <parent> <sha>` vs. deploy.sh's leg prefixes | informational, printed in the plan — never a claim or permission |
| `no_op` | true when `legs_touched` is empty (e.g. `.dev/session/**`, journal, pulse) | still gets deploy-then-push, same order, no special case |
| `pushed` | is `sha` an ancestor of `origin/main` | the core "in scope" fact |
| `deployed[host]` | §3's deployed-stamp — not derivable from git alone | ia-sync-adapter-only; absent without an adapter (nablarva) |

**Authoring host vs. receiving host.** The buffer only ever describes the checkout it is
read from. What a host pulls via `git pull --rebase` was, by definition, already pushed —
SYNC_DISCIPLINE's pull-before-push invariant never lets a host pull someone else's *unpushed*
commits; those exist only on the machine that made them until pushed. So **the receiving
host never sees the authoring host's buffer at all**; it only runs its own local `deploy.sh`
per SYNC_DISCIPLINE's existing "deploy only" steps. There is no deploy-on-behalf-of-another-
host operation to add.

**Live pointer per host.** `HEAD` itself, read fresh at plan time and re-read immediately
before execute (§(7) "remote movement" below) — never cached across the confirm step.

---

## (2) Actions

Three actions, all operating on buffer entries:

### publish-to-here
The ia-sync-specific meaning of "publish": deploy commit `sha`'s snapshot to *this* host,
then push, in that order (fixed fact, majkee 2026-09-25). For a project without a deploy
adapter (nablarva), publish-to-here degrades to "push" — there is no deploy leg to run.

### revert (pushed commits only)
`git revert <sha>` — a **new** commit that undoes `sha`'s tree effect. Never history rewrite.
The revert commit itself immediately enters the buffer as a fresh unpushed entry and goes
through the same publish flow. This is the only backward-moving action available once a
commit is pushed — dropping/rewriting pushed history is out of scope everywhere in this
design (RUNBOOK "Known constraints": no history rewriting of pushed commits).

### drop (every unpushed commit, deployed or not — majkee 2026-09-29)
Unpushed commits may be dropped — via an interactive rebase that removes them, or a reset
to the parent when they are the tip. **This literally moves HEAD.** Under muticula r3's
deny list, `git rebase`/`git reset --hard` are HEAD-mover verbs, human-only (§4 Leg 2), and the
human's HEAD movers are beacon-class (§4 Leg 3). In an enrolled checkout, the printed plan opens
with the beacon (the human stops the other teams and lights it) and closes by clearing it. Publish-gate never executes this itself when `$MUTICULA_ID` is set
in its own environment (running as an enrolled sharp) — it prints the literal command and
hands it to the human's own terminal. Full treatment: §"Boundary with muticula"; this
action's *eligibility* is decided (majkee, 2026-09-29): every unpushed commit stays droppable, deployed
or not. Drop gets its own command (`pg-drop`), and a button once the dashboard exists. For a deployed
commit, the drop plan re-deploys the new tip and prints the orphan list (below), so the live files
are handled explicitly.

**Foreign commits** — an unpushed commit whose trailers/author identify a different seat or
session than the one invoking drop/revert — require explicit operator confirmation:
`drop <sha> authored by <trailer/author> — confirm? [y/N]`, no silent default. Generalizes
Cartan's "must not... interpret a commit as automatic release of a deploy target" to authorship.

**Orphan-file listing (backward moves only).** `deploy.sh` is additive, no `--delete` leg —
so reverting/dropping a commit that *added* a file, then re-deploying, does not remove that
file live; it becomes an orphan `deploy.sh` will never touch again. Before any backward move:

```
comm -23 <(git ls-tree -r --name-only <old_deployed_sha> -- <legs> | sort) \
         <(git ls-tree -r --name-only <new_target_sha>  -- <legs> | sort)
```

— printed as an explicit, non-actioned list. No auto-delete, ever (no-`--delete` gavel;
Open Questions #6 asks whether a confirmed delete-plan should ever exist).

---

## (3) Adapter contract

**Declaring an adapter.** A project opts into "publish means more than push" by placing a
manifest at `<repo>/.dev/publish-gate/adapter.json` (project-root-relative, tracked in git
like `install-pkgs/` task files — SYNC_DISCIPLINE: "Task files ARE tracked"). Absence of
this file means the core buffer model applies unmodified and publish == push. This is how
nablarva "inherits the core, not the adapter" — it simply never writes this file.

```json
{
  "adapter": "ia-sync-deploy-v1",
  "legs": ["claude", "codex", "gemini", "majkee", "nano", "zsh"],
  "materialize": "worktree",
  "pre_deploy_check": "zsh/registries/gen-temple-map.sh --check",
  "deploy_command": "bash deploy.sh",
  "deployed_stamp_dir": "$(git rev-parse --git-common-dir)/publish-gate/",
  "flock_path": "$(git rev-parse --git-common-dir)/publish-gate/lock"
}
```

**ia-sync's adapter, concretely:**

- **Deploy from a HEAD snapshot, never the working tree.** Publish-gate's own `--ref <sha>` (default: the
  plan's selected commit; deploy.sh gains no flag). The snapshot is materialized via `git worktree add --detach <tmp> <sha>`
  into a throwaway path; `deploy.sh` is pointed at that path as `$REPO` (it already resolves
  `$REPO` from its own script location — one variable, 35 uses per the fixed facts — so a copy
  of `deploy.sh` run from inside the detached worktree is sufficient, no change to `deploy.sh`
  itself). The worktree is removed after. This is what `"materialize": "worktree"` means —
  see §"Boundary with muticula" for why this is *not* the RUNBOOK's original `--worktree`
  escape, and why that original meaning is retired.
- **Per-host deployed stamp.** `$(git rev-parse --git-common-dir)/publish-gate/deployed.<host>.json`
  — host-local, untracked, never synced (same family as `install-pkgs`'s
  `~/.local/state/ia-sync/installed.json`, kept per-machine by SYNC_DISCIPLINE for exactly
  this reason: "recording it in the repo would let office claim installed what home never
  ran"). Never placed inside the worktree that gets deployed and discarded.
- **flock.** One lock file beside the stamp, held only across the deploy+push sequence of a
  single publish-to-here operation — narrow and short, never a general editing lock. Bounded
  wait (`flock -w <n>`, hardcoded-boundaries research pattern 3, "no verb waits forever"); on
  timeout, exit non-zero and tell the operator someone else is publishing right now.
- **Orphan listing.** §(2) above. **`--worktree` escape.** Redefined, not preserved as
  originally named — see §"Boundary with muticula".

---

## (4) Checkbox-to-plan translation

A dashboard/CLI checkbox selection (which commit, which action) never executes directly. It
first renders a **literal, ordered command plan**, shown for confirmation:

```
Plan for publish-to-here <sha7> "commit subject":
  1. git worktree add --detach /tmp/pg-<sha7> <sha>
  2. bash /tmp/pg-<sha7>/zsh/registries/gen-temple-map.sh --check     (?) — abort on exit 3, see §Snapshot fidelity
  3. bash /tmp/pg-<sha7>/deploy.sh            # self-locates $REPO to the snapshot; no deploy.sh change
  4. write deployed.office.json: {ref: <sha>, status: deployed_push_pending, at: <ts>}
  5. git ls-remote origin refs/heads/main     # must equal the base recorded at plan time, else refuse: replan
  6. git push origin <sha>:refs/heads/main     # pushes exactly the selected prefix c_1..c_k, never the whole buffer
  7. write deployed.office.json: {ref: <sha>, status: deployed_pushed, at: <ts>}
  8. git worktree remove /tmp/pg-<sha7>

Also unpublished after this operation (unchanged, still in the buffer):
  <sha of c(k+1)> .. <sha of cN>

Confirm? [y/N]
```

Each `(?)`-marked step is a proposal the operator can decline per-plan, not per-run config —
declining step 2 is itself a recorded, explicit choice, never a silent skip. Nothing runs
until the whole plan is confirmed as one unit; there is no "confirm step 3, decide step 5
later" partial-execution mode in v0 (that would reopen the exact "unpushed ≠ safely inert"
gap Cartan flagged — see §7).

---

## (5) JSON CLI contract (nablarva-consumable)

Core fields (present for every project, adapter or not) are top-level; adapter-specific
detail nests under `adapter_state` so a consumer with no adapter (nablarva) can ignore it
entirely without special-casing.

```jsonc
// status --json
{ "host": "office", "checkout": "/home/hruzam/ia-sync", "upstream": "origin/main",
  "buffer": [ { "sha": "89b81cb...", "subject": "...", "pushed": false, "no_op": false,
                "authored_by": {"trailer": "Claude-Session: ...", "git_author": "hruzam <...>"},
                "legs_touched": ["zsh"],              // null when no adapter declares legs
                "adapter_state": {                     // entirely absent, no adapter
                  "deployed": {"office": "deployed_pushed", "home": "not_deployed"} } } ],
  "adapter": "ia-sync-deploy-v1" }                    // absent field, not null, when none

// plan --json   (input: {"action":"publish-to-here","sha":"..."})
{ "action": "publish-to-here", "sha": "89b81cb...",
  "steps": [ {"n": 1, "cmd": "git worktree add --detach ...", "proposal": false},
             {"n": 2, "cmd": "bash .../gen-temple-map.sh --check", "proposal": true} ],
  "remains_unpublished": ["<sha>", "..."], "orphans": [] }   // orphans: revert/drop only

// execute --json   (input: the confirmed plan's steps, verbatim — never a bare action/sha)
{ "sha": "89b81cb...", "result": "ok" | "refused" | "partial",
  "receipts": [ {"n": 1, "exit": 0},
                {"n": 5, "exit": 1, "note": "remote moved since the plan — replan required"} ] }
```

---

## (6) Placement in `zsh/sync/`

The scope already exists (`zsh/sync/base.zsh`, `keyboard.zsh`, `guides.zsh`), already follows
the control-panel convention verified live: `keyboard.zsh` is aliases-and-comments-only,
bodies live in engines, `base.zsh` is the idempotent signpost. Publish-gate adds one leg to
this existing scope, unchanged in shape:

```
zsh/sync/
  base.zsh          existing — add PARTITION 3: source publish-gate.zsh
  keyboard.zsh       existing — add pg-status / pg-plan / pg-run / pg-drop aliases (aliases only)
  guides.zsh          existing, untouched
  publish-gate.zsh    NEW engine — thin zsh wrapper functions, mirrors ai/gemini-processor.sh's
                       "dual-sourced" shape: sourced for interactive use, logic calls into a
                       standalone script so nablarva can drive the JSON CLI without zsh at all.
  publish-gate.sh     NEW standalone bash script — the actual implementation (git plumbing,
                       JSON emission, flock); mirrors muticula's own "bash + flock(1) + git"
                       candidate (muticula §5 "Implementation").

.dev/publish-gate/
  adapter.json                        NEW, tracked — ia-sync's instance of the §3 manifest. It sits at
                                       the project root, not in zsh/registries/, because the contract
                                       is per project (nablarva simply has none).
```

State (`deployed.<host>.json`, the flock file) lives **outside** the repo entirely, at
`$(git rev-parse --git-common-dir)/publish-gate/` — needs no `sync.deny` entry since it is
never inside the repo tree, same reasoning as muticula's own `.git/muticula/` placement.

---

## (7) Boundary with muticula — ownership, folded from Cartan's memo

Cartan's boundary memo (2026-09-25) proposed "publish-gate is a client of muticula for
reservation" as separate components with distinct jobs. Folded as the design's ownership
table:

| Concern | Owner |
|---|---|
| Claims, overlap, the beacon, handoff, release/recovery | Muticula (when enrolled) |
| Pending commits, selection, approved plan, publication state and recovery | Publish-gate |
| Source-file claims and unfinished edits | The current authoring actor, until release |
| Staging / commit | The authorized committer — through `muticula commit` when enrolled, plain git otherwise |
| Deployment | Publish-gate's ia-sync adapter, acting under whatever claim/beacon state applies |
| Deployment semantics and target inventory | The project adapter — ia-sync does not define other projects' policy |
| Approval and recovery decisions | Majkee |

Publish-gate never becomes a second authority for either resource muticula names
(`RUNBOOK.md` "this design must not become a second owner of either"; the resource-resolver
contract in Cartan's memo §"Git needs more than a checkout-labelled index" and the app-scheme
draft §3.5.4 are muticula's to own, not re-specified here).

### Git transaction

- **Enrolled** (`MUTICULA_ID`/`MUTICULA_KEY` set for this checkout): every commit publish-gate
  needs to make (e.g. a `revert`) goes through `muticula commit`, never raw `git commit` —
  its Leg 2 gate is "welded to the one action nobody skips," publish-gate does not skip it.
  HEAD-mover verbs (`rebase`, `reset --hard`, the machinery behind `drop`) sit in muticula's
  deny list for every sharp; the beacon never grants them to a sharp. For the human they are
  beacon-class (brief r3, Leg 3), so the printed drop plan opens with `muticula beacon on` after the
  other teams have stopped, and closes with `muticula beacon off`.
  When publish-gate itself sees `$MUTICULA_ID` set (it is an enrolled sharp), it refuses to
  execute a drop/rebase step and prints the plan for the human's own terminal instead. An
  *absent* `MUTICULA_ID` means unenrolled (D3), not proof of a human — but human verbs are
  explicit operator commands kept off agents' routes regardless, so the human running the
  drop plan by hand is the same act as running its printed `git rebase` by hand. Publish-gate
  supplies the plan; never the authority.
- **Absent** (no `.git/muticula/` state): publish-gate is the sole coordinator of its own git
  transaction. It still never rewrites pushed history and still follows SYNC_DISCIPLINE's
  pull-before-push, but does not guard *other* sessions' edits — that job does not exist
  without muticula present. Its own flock (§3) only serializes concurrent publish-gate calls.

### Deploy target

Muticula v0 does not model deploy targets at all (brief r3, §1 "Out of scope"; deploy is not
one of its named resource types, §3.5.4/§4). This is a clean seam, not a contested one:
publish-gate owns the deploy-target state model entirely. States tracked per `(sha, host)`:

```
not_deployed
deploying                      (in progress — the flock is held)
deployed_pushed                (both steps landed)
deployed_push_pending           (deploy succeeded, push not yet attempted or failed)
deploy_failed[:leg]             (a specific deploy.sh leg errored — additive legs can leave a mixed target)
```

**Cartan's primary challenge, folded directly:** "the gaveled order is deploy then push...
deployment can succeed and push can fail, so a commit can already have external effects while
still unpushed." This means the RUNBOOK's fixed fact — "everything in the buffer is unpushed
and drop is legal inside it" — is **not safe as stated** once a commit reaches
`deployed_push_pending`. A commit in that state has already changed live files on this host;
dropping it from the buffer (rewriting it away) would leave those live files with no
corresponding commit at all, and a later re-deploy of an older commit cannot undo them
(additive, no `--delete`). majkee kept the fixed fact (2026-09-29): such a commit is still
droppable. So the drop plan for a deployed commit re-deploys the new tip and prints the orphan
list; the live files are handled explicitly, never left silently.

Per-leg receipts, not one whole-repo claim: `--codex-only` deploys only the Codex leg, so a
successful `--codex-only` deploy must never be recorded as "deployed at `<sha>`" for the
whole repository (Cartan's memo, same finding). The `deployed.<host>.json` stamp is
leg-scoped: `{"sha": "...", "legs": {"zsh": "deployed_pushed", "codex": "not_deployed"}}`.

### Prefix publication

Buffer commits form a linear chain (`git rev-list --reverse origin/main..HEAD`), not an
independent set. Publishing `c_k` **is** publishing the prefix `c_1..c_k` — there is no
mechanism by which deploying `c_k`'s tree snapshot could exclude `c_1..c_{k-1}`'s changes;
they are already baked into `c_k`'s tree by git's own definition of history. So:

- Selecting a middle commit `c_k` (k < N) means: publish through `c_k`, and the plan (§4)
  explicitly lists `c_{k+1}..c_N` as **remaining unpublished**, never silently applied and
  never silently dropped.
- If the operator later wants `c_{k+2}` but explicitly not `c_{k+1}`'s changes, that is
  **not** expressible as a buffer selection — `c_{k+2}`'s tree already contains `c_{k+1}`'s
  changes. This is a replan: revert `c_{k+1}` (a new, forward-moving commit, §2), or an
  interactive rebase to drop `c_{k+1}` before re-selecting — never a cherry-pick performed
  silently underneath a checkbox tick. Checkboxes select a prefix boundary; they do not
  reconstruct history.

### Snapshot fidelity

`deploy.sh:239-246` runs `gen-temple-map.sh` **before** the zsh rsync, writing
`zsh/ai/temple-project-map.zsh` fresh from `registries/projects.json` in the tree it is
running against. Run unmodified against a pinned `--ref` snapshot, this would write bytes
into that snapshot that were never actually committed at `<sha>` — a direct violation of
"deploy only committed content" the moment the generator's output differs even by
whitespace from what `<sha>` has on disk.

**Resolution (§3's `pre_deploy_check`):** the adapter runs `gen-temple-map.sh --check`
inside the detached worktree, **before** the rsync step, in check-only mode (exit 3 on
drift, per the script's own documented contract — verified live). On drift, the whole
publish plan is refused: "commit 1de7f27's `projects.json` and `temple-project-map.zsh`
disagree — commit the regenerated artifact first, then replan." deploy.sh still runs the
generator in write mode (deploy.sh:239-246), but with `--check` green that write reproduces the
committed bytes exactly, so the snapshot stays pure. This is the "generating and committing
beforehand, then checking during deploy" shape Cartan's memo asked for, applied literally.

### The `--worktree` escape

The RUNBOOK's item (3) names an "explicit `--worktree` escape" as part of the adapter
contract, written before this design existed to resolve what it would mean. Cartan's memo
flags the obvious reading — "an unchecked live-tree deploy" — as a direct conflict with
majkee's "deploy only committed content" gavel, and is right to. **This design retires that
reading entirely.** `"materialize": "worktree"` (§3) never means "deploy whatever is
currently sitting dirty in the working tree" — it means "use `git worktree add --detach <tmp>
<sha>`" to turn the pinned commit into a real on-disk snapshot, as opposed to a hypothetical
`git archive | tar -x` strategy. Both options always start from a resolved, committed `<sha>`
— never the live tree. There is no flag anywhere in this design that deploys uncommitted
content. An operator who wants to hand-test a dirty local tree still has the plain, un-gated
`bash deploy.sh` (SYNC_DISCIPLINE's existing step 5) — untouched, out of scope here.

### Remote movement

SYNC_DISCIPLINE's invariant ("pull before you push, always, no exceptions",
`pull.rebase=true` on both clones) is a precondition publish-gate assumes was already
satisfied *before* a plan was built — building the plan does not itself pull. Between plan
confirmation and the push, the adapter re-checks, as its own plan step (§4 step 5):

```
git ls-remote origin refs/heads/main   # must equal the base recorded when the plan was built
```

If `origin/main` moved since the plan was built, **execute refuses** (§5's receipt shape:
`{"exit": 1, "note": "push rejected — remote moved, replan required"}`) and tells the
operator to `git pull --rebase` and rebuild the plan. Publish-gate never rebases the buffer
onto the new `origin/main` on the operator's behalf — that is the HEAD-moving integration
muticula's deny list reserves for the human, and the silent "push another tree under the
previous approval" Cartan's memo rejects. No rewrite of already-pushed history is ever
performed to resolve this.

---

## Open questions for majkee

These are proposals, never decisions — each needs a gavel.

1. **DECIDED (majkee, 2026-09-29):** every unpushed commit stays droppable, even at
   `deployed_push_pending`. Drop gets its own command (`pg-drop`) and, later, a dashboard button.
   The drop plan re-deploys the new tip and lists the orphans (§2).
2. **(?)** Should publish-gate reuse muticula's exit-code convention (`0`/`1`/`3`/`4`) for
   consistency, or keep an independently numbered scheme? Not load-bearing either way.
3. **(?)** Rename the manifest key `materialize` back toward the RUNBOOK's original
   `--worktree` word, now that its meaning has narrowed to an implementation-strategy flag?
   Cosmetic, but the old name risks being misread as the bypass Cartan flagged.
4. **(?)** Deployed-stamp location: `$(git rev-parse --git-common-dir)/publish-gate/` (beside
   muticula, this design's proposal) vs. `~/.local/state/ia-sync/` alongside `install-pkgs`'s
   `installed.json`. Both are host-local/never-synced; picking one is a placement call.
5. **(?)** Should publish-gate register as a muticula sharp and claim the narrow paths it
   writes (e.g. during the `--check` step), or is its own short-lived flock enough? Decides
   whether it needs its own `MUTICULA_ID`/`MUTICULA_KEY` when run non-interactively.
6. **(?)** Orphan listing (§2) is list-only here, matching the no-`--delete` gavel. Should a
   later phase ever offer a confirmed, one-file delete action, or is listing-only permanent?
7. **(?)** Placement of the *core* buffer model nablarva consumes: a standalone package
   ia-sync hosts and nablarva points at, or a copy nablarva vendors/symlinks? Affects §6 but
   is really nablarva's placement call, not ia-sync's — named here so it isn't lost.

---

## What this design deliberately does not do

- Implement anything — no changes to `deploy.sh`, `SYNC_DISCIPLINE.md`, `zsh/`, or any live
  file. A numbered sibling session opens after GO (RUNBOOK "What this session deliberately
  does not do").
- Build the dashboard/TUI view — the JSON CLI contract (§5) is the interface; a view is later,
  over the CLI, per RUNBOOK.
- Decide nablarva's language, store, or its own publishing semantics beyond "no adapter ⇒
  publish == push."
- Own or re-specify any of muticula's named resources (claims, the beacon, the commit gate's
  internals) — §7 only draws the boundary line, never redraws muticula's side of it.
- Pin exact JSON schema versions, flock timeout numbers, or the stamp file's on-disk format
  beyond the sketch in §5/§3 — those are implementation-phase detail, not architecture.
- Resolve the six open questions still open (Q1 is decided) — each is majkee's call.
