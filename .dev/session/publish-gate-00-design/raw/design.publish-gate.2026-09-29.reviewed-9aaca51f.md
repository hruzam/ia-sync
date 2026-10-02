---
title: Design — publish-gate (core buffer model + ia-sync deploy adapter)
status: "r2 — folds Cartan's RETURN 01 (REVISE); for his fold check · majkee's drop decision kept · head-reviewed (6 corrections: prefix-closure linearity, nablarva buffer fact, host-global mutex, --ref wording, check scope, beacon on drop)"
date: 2026-09-29
author: trajectory (design author, publish-gate-00-design)
folds:
  P1: "§3a Preflight (mandatory) · §4 step 2 · §7 Snapshot fidelity"
  P2: "§2 drop sequence · §2a Operation receipts and partial state · §7 Deploy target states · §7 Residual inventory"
  P3: "§1 Buffer model · §1a Project integration policy"
  P4: "§7 Boundary with muticula — enrollment states, revert-through-the-gate, pg-drop route, detached worktree, Q5 reframe, obsolete references"
  P5: "§3b Deployment mutex"
  P6: "§4 Checkbox-to-plan translation · §5 JSON CLI contract · §7 Remote movement"
inputs:
  - /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/RUNBOOK.md
  - /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/STATUS.md
  - /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/_bus/01.cartan.return.md (CHALLENGE folded by this revision)
  - /home/hruzam/ia-sync/deploy.sh
  - /home/hruzam/ia-sync/SYNC_DISCIPLINE.md
  - /home/hruzam/ia-sync/zsh/AGENTS.md (sync/ scope + control-panel convention)
  - /home/hruzam/ia-sync/zsh/sync/base.zsh, keyboard.zsh (live control-panel example)
  - /home/hruzam/ia-sync/zsh/registries/gen-temple-map.sh
  - /home/hruzam/unikuklatrix/nablarva/.dev/session/flag.md (L12 — core, plain pull, never rebase)
  - /home/hruzam/unikuklatrix/nablarva/.dev/session/muticula-01-qualify/raw/muticula.master.2026-09-26.md (r3)
  - git -C ia-sync show 9bb608b:.dev/session/runbook-upgrade-02-app/raw/cartan.publish-gate-boundary.2026-09-25.md (historical — see §7 obsolete-reference note)
  - git -C ia-sync show 9bb608b:.dev/session/runbook-upgrade-02-app/raw/draft.majkee.app-scheme.2026-09-23.md §3.5.4 (historical — see §7 obsolete-reference note)
verified-live-facts:
  - "deploy.sh — one $REPO source var, no --delete anywhere, no deployed-commit record, one repo-writing step (gen-temple-map.sh before the zsh rsync); flags only --dry-run/-n and --codex-only; legs claude, codex, gemini, majkee, nano, zsh"
  - "gen-temple-map.sh (zsh/registries/) writes zsh/ai/temple-project-map.zsh from registries/projects.json; --check exits 3 on drift, --stdout prints without writing. §3a treats ANY nonzero exit from ANY preflight check as a refusal, not only the documented 3."
  - "ia-sync's .git is a plain repo, not a worktree; git-common-dir == .git"
  - "commit trailers in use: Co-Authored-By (Claude model) and Claude-Session (url); no host trailer exists today"
  - "ia-sync: local branch main, upstream origin/main, pull.rebase=true (SYNC_DISCIPLINE.md) — the buffer model's rev-list example is this project's actual policy, not a hardcoded core default"
  - "nablarva: local branch core, upstream origin/core; flag L12 forbids pull --rebase (subtree history) — plain pull only. Checked 2026-09-29: pushed history has 3 merges in 63 commits; the current buffer range origin/core..core has 0 merges. Plain pull creates a merge whenever local and remote diverge, so §1a's linear-segment limit bites exactly then."
  - "deploy.sh's real source→destination legs (used by §7's residual-inventory rewrite): zsh/ (excl. config.*.zsh, zshrc.*) → ~/.config/zsh/; zsh/config.<host>.zsh → ~/.config/zsh/config.zsh; zsh/zshrc.<host> → ~/.zshrc; claude/{skills,agents,commands}/ → ~/.claude/{...}/; claude/{settings.json,CLAUDE.md} → ~/.claude/; codex/AGENTS.md → ~/.codex/AGENTS.md; codex/agents/ → ~/.codex/agents/; codex/skills/ → ~/.agents/skills/; gemini/agents/ → ~/.gemini/agents/; gemini/{state.json,GEMINI.md} → ~/.gemini/; gemini/config/mcp_config.json → ~/.gemini/config/; gemini/config/projects/ → ~/.gemini/config/projects/; gemini/antigravity-cli/{settings.json,keybindings.json} → ~/.gemini/antigravity-cli/; majkee/ → ~/.majkee/; nano/nanorc → ~/.nanorc"
---

# Design — publish-gate

This is a design, not an implementation. It answers RUNBOOK prompt-0's items (1)–(7), gives
the muticula boundary the depth the RUNBOOK asks for, and names what is open for majkee.
`(?)` marks a proposal to architect — never an order. **This r2 folds Cartan's RETURN 01
(CHALLENGE, disposition REVISE) in full** — six findings, P1–P6, mapped above. Cartan's
primary point stands: a confirmed list of shell commands is not sufficient to preserve the
relationship between selected Git content and live files through failure, retry and drop.
Every fold below turns a narrated partial state into something the design actually writes
down and checks. Nothing in this revision reopens majkee's 2026-09-29 drop-eligibility
decision or the committed-content gavel; no implementation GO is claimed here.

---

## (1) Buffer model

**Scope.** One buffer per `(host, checkout)` pair — the same host-local, git-common-dir-local
scoping muticula uses for its own state (`muticula.master.2026-09-26.md` §3 D2). A buffer is
never a cross-host object; there is no "office's buffer, viewed from home."

**Resolved, not assumed (P3).** The core resolves and pins, per checkout, before building any
buffer: the local branch, the configured remote/target ref, and the observed base (the
merge-base or the ref's current value at read time). It never hardcodes `main`/`origin/main`
— those are ia-sync's *policy answer*, supplied by §1a, not the core's default.

**Contents.** Given the resolved local branch and target ref:

```
git rev-list --reverse <target-ref>..<local-branch>     # oldest first
```

is the ordered candidate list — **valid as the whole buffer only when that range is a
verified linear segment** (no merge commit inside it: `git rev-list --merges <target-ref>..<local-branch>`
is empty). Publishing `c_k` publishes its whole ancestor closure `<target-ref>..c_k`, so v0 can
select only commits whose closure is linear: the segment from the observed base up to the first
merge. Every later commit is reported as **unsupported history**, never silently flattened or
reordered. See §1a for when this bites.

Each entry carries:

| Field | Source | Notes |
|---|---|---|
| `sha` | the commit | immutable identity |
| `subject`/`body` | `git log -1 --format=%B` | shown verbatim in the plan (§4) |
| `authored_by` | trailers when present, else `%an <%ae>` | **[verified]** actual trailers here: `Co-Authored-By: Claude <model> <noreply@anthropic.com>`, `Claude-Session: <url>` — no host trailer exists. Best-effort provenance, never access control. |
| `legs_touched` | `git diff --name-only <parent> <sha>` vs. the adapter's declared legs | informational, printed in the plan — never a claim or permission |
| `no_op` | true when `legs_touched` is empty | still gets deploy-then-push, same order, no special case |
| `pushed` | is `sha` an ancestor of `<target-ref>` | **(P3) a refreshed fact, not a cached one.** Read against a freshly fetched `<target-ref>` immediately before any destructive drop (§2). Stale or unreachable remote state is reported `unknown`, never coerced to "unpushed" or "pushed." |
| `deployed[host]` | §7's deployed-stamp | ia-sync-adapter-only; **absent** (no field) with no adapter, **`unknown`** (not `not_deployed`) when an adapter exists but no receipt is found — see §3a. |

**Authoring host vs. receiving host.** The buffer only ever describes the checkout it is read
from. What a host pulls was, by definition, already pushed — SYNC_DISCIPLINE's pull-before-push
invariant never lets a host pull someone else's *unpushed* commits. So the receiving host never
sees the authoring host's buffer; it runs its own local `deploy.sh` per SYNC_DISCIPLINE's
existing steps. There is no deploy-on-behalf-of-another-host operation to add.

**Live pointer per host.** `HEAD`, read fresh at plan time and re-read immediately before
execute (§7 "Remote movement") — never cached across confirm.

### (1a) Project integration policy (P3)

The core supplies mechanism; each project's policy supplies the two facts the core plugs in.
Verified 2026-09-29, not assumed:

| | ia-sync | nablarva |
|---|---|---|
| Local branch | `main` | `core` |
| Remote/target ref | `origin/main` | `origin/core` |
| Integration mode | `pull --rebase` (SYNC_DISCIPLINE.md, `pull.rebase=true` on both clones) | plain `pull`, **never** `pull --rebase` — subtree history, flag L12 |
| History shape in the buffer range | linear by discipline (`pull --rebase`) | linear today (`origin/core..core`: 0 merges, checked 2026-09-29). But plain `pull` makes a merge commit whenever local and remote diverge, so the buffer holds a merge exactly then; pushed history already has 3 |
| v0 buffer selection | the full range qualifies | qualifies while the range is linear. After a diverged `pull`, only commits before the merge are selectable, and the rest is reported as unsupported history. v0 does not fully solve nablarva's inheritance |

A merge commit inside a selected range needs an explicit mainline for `revert` (`git revert
-m <n> <sha>`) — the core never guesses parent 1. `pushed` for nablarva is checked against
`origin/core`, never `origin/main`; there is no cross-project default.

---

## (2) Actions

Three actions, all operating on buffer entries:

### publish-to-here
Deploy commit `sha`'s snapshot to *this* host, then push, in that order (fixed fact, majkee
2026-09-25). For a project without a deploy adapter, publish-to-here degrades to "push."

### revert (pushed commits only)
`git revert <sha>` — a **new** commit undoing `sha`'s tree effect, never history rewrite. If
`sha` is a merge, revert requires an explicit mainline (§1a); no default guess. The revert
commit enters the buffer as a fresh unpushed entry and goes through the same publish flow.
When the checkout is muticula-enrolled, the commit itself is made through `muticula commit`,
never raw `git commit` — the mechanics are in §7 ("Git transaction").

### drop (every unpushed commit, deployed or not — majkee 2026-09-29)
Unpushed commits may be dropped, via an interactive rebase that removes them or a reset to
the parent when they are the tip. This literally moves HEAD — a muticula human-only,
beacon-class verb when enrolled (§7). Eligibility is decided: every unpushed commit stays
droppable, deployed or not; `pg-drop` gets its own command and, later, a dashboard button.

**Every drop that can affect live state (P2) follows this sequence, recorded as an operation
(§2a) before any effect:**

1. **Show and preserve.** Print the history change, the new target's derivation, the affected
   destinations, and the residual-file inventory (§7). Preserve the old OID/tree and write a
   receipt for it — e.g. a local ref `refs/publish-gate/dropped/<op-id>`, never pushed — so
   recovery does not depend on reflog retention alone.
2. **Perform and record.** Run the authorized history operation; record whether it completed.
   If it computes a new OID (rewriting descendants), bind that resulting OID into the receipt
   before deploying — never re-read a movable HEAD as if it were the originally approved one.
3. **Deploy under §3a's checks.** A failure here means history has already changed while live
   files remain old/mixed — keep that fact visible with an offered recovery path; never report
   it as either "drop failed, nothing happened" or a clean success.
4. **Keep the residual list after redeploy.** Additive copying (no `--delete`) leaves deleted
   or renamed outputs behind by design. No auto-delete, no false clean stamp — ever.

**Foreign commits** — an unpushed commit whose trailers/author identify a different seat or
session than the one invoking drop/revert — require explicit operator confirmation:
`drop <sha> authored by <trailer/author> — confirm? [y/N]`, no silent default.

---

### (2a) Operation receipts and partial state (P2)

Every `publish-to-here`, `revert`-and-publish, and drop-with-redeploy is one **operation**.
An operation receipt is written **before** the effect it describes, not after success:

| Field | Written | Notes |
|---|---|---|
| `op_id` | at plan-confirm | see §4 — carried through every later record |
| `old_target_observation` | before any write | the pre-operation deployed-stamp read, verbatim, so a later reconciliation has something to compare against |
| `selected_oid` | before any write | the pinned commit this operation deploys/pushes |
| `host` | before any write | resolved machine identity |
| `actual_destination_set` | before deploy | from the adapter's source→destination map (§7 Residual inventory), not the source tree |
| `expected_remote_ref` | before push | the target ref this operation intends to advance |
| `status` | updated at each step | `unknown` (default, unreconciled) → `deploying` → `deployed_push_pending` → `deployed_pushed`, or `deploy_failed[:leg]` |

Rules:

- **Unfinished ⇒ unknown/partial**, never "did not happen." Killing the process after one
  rsync leg leaves files changed while the stamp still describes the prior state; the receipt
  says so until reconciled, not after guessing.
- **Deploy and push are recorded independently.** A push acknowledgement can be lost after the
  server actually received it; after any ambiguous push, the adapter checks remote state
  before retrying — it never blindly re-pushes or blindly reports failure.
- **No promised per-leg completion evidence beyond what the adapter can actually obtain.**
  `deploy.sh` emits human-readable output and can stop mid-script; unknown legs may remain
  `unknown` rather than being inferred from what ran before or after them.
- The same receipt shape (not a separate one) backs drop's four-step sequence in §2.

---

## (3) Adapter contract

**Declaring an adapter.** A project opts in by placing a manifest at
`<repo>/.dev/publish-gate/adapter.json`, tracked in git. Absence means the core buffer model
applies unmodified and publish == push — this is how nablarva "inherits the core, not the
adapter."

```json
{
  "adapter": "ia-sync-deploy-v1",
  "legs": ["claude", "codex", "gemini", "majkee", "nano", "zsh"],
  "materialize": "worktree",
  "pre_deploy_check": "zsh/registries/gen-temple-map.sh --check",
  "deploy_command": "bash deploy.sh",
  "deployed_stamp_dir": "$(git rev-parse --git-common-dir)/publish-gate/",
  "mutex": "~/.local/state/publish-gate/locks/<digest of the sorted destination set>.lock"
}
```

**ia-sync's adapter, concretely:**

- **Deploy from a HEAD snapshot, never the working tree.** Publish-gate's own `--ref <sha>`
  (default: the plan's selected commit; deploy.sh gains no flag). Materialized via `git worktree add --detach <tmp> <sha>` into a throwaway,
  exclusively allocated path (§4); `deploy.sh` runs from inside it, self-locating `$REPO` — no
  change to `deploy.sh` itself. The worktree is removed after.
- **Per-host, per-leg deployed stamp.** `$(git rev-parse --git-common-dir)/publish-gate/deployed.<host>.json`
  — host-local, untracked, never synced.
- **Residual listing.** §7. **`--worktree` escape.** Redefined — see §7.

### (3a) Preflight — mandatory, not a per-plan checkbox (P1)

`deploy.sh` runs `gen-temple-map.sh` in write mode before the zsh rsync, and performs several
earlier deploy legs before reaching it. A late or skippable check cannot protect those earlier
effects. So:

- Preflight runs **before the first live write of the operation**, no exceptions.
- It **refuses on any nonzero exit** from any declared check — not only the generator's
  documented exit 3. A check that fails in an unexpected way is still a refusal, never a pass.
- The adapter manifest, `pre_deploy_check` script, and `deploy_command` script are resolved
  **from the pinned snapshot** (the detached worktree at `<sha>`), not from whatever sits live
  on disk. Their identities — sha256 of each resolved file — are recorded in the plan (§4), so
  a confirmed plan names exactly which bytes it is about to run.
- **Removing or downgrading this check is a policy change** requiring its own gavel, never an
  ordinary per-plan opt-out.
- A green check vouches only for today's deterministic generator. A future build step added to
  `deploy.sh` needs its own check before this gate covers it.
- The receiving host's local "just run `bash deploy.sh`" shortcut (SYNC_DISCIPLINE step 5) and
  a dirty-tree hand-test are **not compliant exceptions** to this gate. They remain what they
  already are — an ungated, out-of-scope escape hatch an operator can still use by hand — but
  publish-gate's own deployment path, on either host, always goes through this preflight.
- **A missing deployment receipt means `unknown`, never `not_deployed`.** (Fixes the earlier
  §5 sample, which is corrected below.)

### (3b) Deployment mutex (P5)

A common-dir flock alone under-serializes: a second independent clone of the same repo on the
same host has its own common dir and can deploy into the same `~/.config/zsh`, `~/.claude`, or
`~/.agents` destinations concurrently. The fold:

- The mutex is **host-local, keyed to the resolved physical destination set** this operation's
  plan will write (from §7's source→destination map) — not to the git-common-dir alone. Its lock
  file lives host-global at `~/.local/state/publish-gate/locks/<digest>.lock`, never inside a git
  common dir, because a second clone has its own common dir.
- It is **shared by every path that can write those destinations through this adapter**:
  publish, plain redeploy, and drop-triggered redeploy all acquire the same mutex.
- **Cooperative limit, stated plainly:** a direct, unmediated `bash deploy.sh` call still
  bypasses it — this is not, and does not pretend to be, an enforced OS-level exclusion.
- **It is not a claim and not a beacon.** It grants no muticula authority and substitutes for
  neither (see §7, Q5 reframe).
- **Acquisition order:** if the operation must make a commit first (e.g. `revert`), the
  muticula commit gate (when enrolled) runs and completes *before* this mutex is acquired —
  the mutex only ever wraps the deploy+push sequence, never the git-authoring step. It is
  **never held across operator deliberation**: it is acquired fresh, immediately before §4's
  execute effects begin, after the plan has already been confirmed — not from confirm through
  execute.
- A future muticula deploy-resource provider can replace this responsibility through a
  deliberate handoff; r3 does not supply one today (§7).

---

## (4) Checkbox-to-plan translation

A checkbox selection never executes directly. It renders a **confirmed operation** carrying
typed inputs, not just command strings (P6):

| Field | Meaning |
|---|---|
| `op_id` | opaque identifier, minted at confirm; threads through every later record (§2a) |
| `host`, `checkout` | resolved identity of this run |
| `local_branch`, `remote_ref`, `observed_base` | §1's resolved facts, pinned at plan time |
| `adapter_digest` | sha256 of the resolved adapter manifest + its check/deploy scripts (§3a) |
| `expected_head` | the selected commit; what HEAD must still resolve to at execute time |
| `prior_deployment_state` | the last known `deployed[host]` reading, so execute can detect drift |

```
Plan <op_id> for publish-to-here <sha7> "commit subject"   (ia-sync rendering: remote, branch and host come from the typed inputs)
  1. git worktree add --detach <exclusive tmp dir>  <sha>
  2. bash <worktree>/zsh/registries/gen-temple-map.sh --check     # mandatory — any nonzero exit refuses (§3a)
  3. bash <worktree>/deploy.sh
  4. write deployed.office.json: {op_id, ref: <sha>, status: deployed_push_pending, at: <ts>}
  5. git ls-remote origin refs/heads/main     # cheap early check — must equal observed_base
  6. git push origin <sha>:refs/heads/main    # pushes exactly the selected prefix, never the whole buffer
  7. git ls-remote origin refs/heads/main     # reconciliation — must now equal <sha>
  8. write deployed.office.json: {op_id, ref: <sha>, status: deployed_pushed, at: <ts>}
  9. git worktree remove <exclusive tmp dir>

Also unpublished after this operation (unchanged, still in the buffer):
  <sha of c(k+1)> .. <sha of cN>

Confirm? [y/N]
```

Step 2 is no longer a declinable `(?)` proposal — it is mandatory (§3a). Nothing runs until
the whole plan is confirmed as one unit.

**Before effects begin (P6):** the mutex (§3b) is acquired, then the plan's typed inputs are
revalidated fresh — `HEAD` still equals `expected_head`, `observed_base` still matches a fresh
`ls-remote` — and a stale plan is refused outright rather than executed against inputs that
moved underneath it. Materialization uses an exclusively allocated `mktemp -d`, never a
predictable, collision-prone fixed path.

Human-readable command text is a **rendering** of the typed operation above, never free shell
text accepted from a dashboard. **Resuming** an interrupted operation (same `op_id`,
reconciling from its receipt) is a distinct action from **executing** a plan; re-submitting a
completed or partial `op_id` for execution must reconcile against its existing receipt, never
blindly repeat the writes.

---

## (5) JSON CLI contract (nablarva-consumable)

Core fields are top-level; adapter-specific detail nests under `adapter_state` so a
no-adapter consumer (nablarva) ignores it entirely.

```jsonc
// status --json
{ "host": "office", "checkout": "/home/hruzam/ia-sync", "upstream": "origin/main",
  "buffer": [ { "sha": "89b81cb...", "subject": "...", "pushed": false, "no_op": false,
                "authored_by": {"trailer": "Claude-Session: ...", "git_author": "hruzam <...>"},
                "legs_touched": ["zsh"],
                "adapter_state": {
                  "deployed": {"office": "deployed_pushed", "home": "unknown"} } } ],
                  // "unknown" — no receipt found — never "not_deployed" (§3a)
  "adapter": "ia-sync-deploy-v1" }                    // absent field, not null, when none

// plan --json   (input: {"action":"publish-to-here","sha":"..."})
{ "op_id": "pg-2026-09-29T...-a1b2", "action": "publish-to-here", "sha": "89b81cb...",
  "inputs": {"host": "office", "local_branch": "main", "remote_ref": "origin/main",
             "observed_base": "<sha of origin/main>", "adapter_digest": "sha256:...",
             "expected_head": "89b81cb..."},
  "steps": [ {"n": 1, "cmd": "git worktree add --detach ...", "mandatory": true},
             {"n": 2, "cmd": "bash .../gen-temple-map.sh --check", "mandatory": true} ],
  "remains_unpublished": ["<sha>", "..."], "orphans": [] }   // orphans: revert/drop only

// execute --json   (input: {"op_id": "pg-2026-09-29T...-a1b2"} — never a bare action/sha)
{ "op_id": "pg-2026-09-29T...-a1b2", "sha": "89b81cb...",
  "result": "ok" | "refused" | "partial" | "unknown",
  "receipts": [ {"n": 1, "exit": 0},
                {"n": 5, "exit": 1, "note": "remote moved since the plan — replan required"},
                {"n": 7, "exit": 0, "reconciled_remote": "89b81cb..."} ] }
```

---

## (6) Placement in `zsh/sync/`

The scope already exists (`zsh/sync/base.zsh`, `keyboard.zsh`, `guides.zsh`), following the
verified control-panel convention: `keyboard.zsh` is aliases-and-comments-only, bodies live in
engines, `base.zsh` is the idempotent signpost. Publish-gate adds one leg, unchanged in shape:

```
zsh/sync/
  base.zsh          existing — add PARTITION 3: source publish-gate.zsh
  keyboard.zsh       existing — add pg-status / pg-plan / pg-run / pg-resume / pg-drop aliases
  guides.zsh          existing, untouched
  publish-gate.zsh    NEW engine — thin zsh wrapper functions, mirrors ai/gemini-processor.sh's
                       "dual-sourced" shape: interactive surface + a standalone script so
                       nablarva can drive the JSON CLI without zsh at all.
  publish-gate.sh     NEW standalone bash script — git plumbing, JSON emission, the §3b mutex.

.dev/publish-gate/
  adapter.json        NEW, tracked — ia-sync's instance of the §3 manifest, at the project
                       root (nablarva simply has none).
```

State (`deployed.<host>.json`, operation receipts) lives **outside** the repo at
`$(git rev-parse --git-common-dir)/publish-gate/` — no `sync.deny` entry needed, same reasoning
as muticula's `.git/muticula/`. The mutex file is the exception: it lives host-global at
`~/.local/state/publish-gate/locks/` (§3b), because it must also exclude other clones.

---

## (7) Boundary with muticula — ownership, folded from Cartan's memo

| Concern | Owner |
|---|---|
| Claims, overlap, the beacon, handoff, release/recovery | Muticula (when enrolled) |
| Pending commits, selection, approved plan, publication state and recovery | Publish-gate |
| Source-file claims and unfinished edits | The current authoring actor, until release |
| Staging / commit | The authorized committer — through `muticula commit` when enrolled, plain git otherwise |
| Deployment | Publish-gate's ia-sync adapter, acting under whatever claim/beacon state applies |
| Deployment semantics and target inventory | The project adapter — ia-sync does not define other projects' policy |
| Approval and recovery decisions | Majkee |

**Obsolete RUNBOOK fact (P4):** `r3` has **no general deploy-target reservation API**. Cartan's
2026-09-25 boundary memo and the app-scheme draft §3.5.4 are historical design context, not an
API that exists in r3 today; this design does not re-grow those resources to satisfy that old
text. RUNBOOK.md's own prompt-0 citation of §3.5.4 as a live description is stale — the head
corrects RUNBOOK.md directly, outside this design file.

### Git transaction (P4)

Enrollment is **three states**, not a binary enrolled/absent — a missing `MUTICULA_ID` never
proves state 2:

| State | Condition | Effect on publish-gate |
|---|---|---|
| 1. Validated enrolled client | `MUTICULA_ID`/`MUTICULA_KEY` set and key hash matches `keys/<id>` in `.git/muticula/` | Every commit publish-gate needs (e.g. `revert`) goes through `muticula commit`; HEAD-mover verbs (`rebase`, `reset --hard`, drop's machinery) are refused for this identity and printed for the human's own terminal instead. That printed drop plan opens with `muticula beacon on` once the other teams have stopped, and closes with `muticula beacon off` (r3 Leg 3, beacon-class) |
| 2. Confirmed no muticula state | No `.git/muticula/` directory exists for this checkout at all | Publish-gate is the sole coordinator of its own git transaction; still never rewrites pushed history, still follows pull-before-push |
| 3. Refused-unknown authority | `.git/muticula/` exists, but this identity's `MUTICULA_ID` is missing/wrong/revoked, or this checkout doesn't match the registered one | Publish-gate refuses commit/HEAD-mover routes outright rather than guessing state 2; tells the operator to resolve enrollment first |

**Revert's execution gap, closed.** `git revert <sha>` alone creates a commit directly,
contradicting the commit-gate requirement. The prepared form: `git revert --no-commit <sha>`
only under (a) explicit affected-path ownership already claimed/adopted by the invoking
identity, (b) a clean-index precondition checked before starting, and (c) defined conflict
handling — on conflict, `git revert --abort`, refuse the plan, tell the operator. The staged
tree then goes through `muticula commit`, never raw `git commit`. Alternative: keep the whole
revert human-coordinated (the human runs `git revert` by hand), with the commit gate still
honoured either way.

**`pg-drop`'s own authorization gate** is independent of `MUTICULA_ID` and must not use "is
`MUTICULA_ID` set" as a human/agent classifier — an unenrolled agent session is not a human
either. `pg-drop`, like the raw HEAD-mover verbs it wraps, requires an explicit operator route
(the same interactive-confirmation surface as muticula's own human verbs) regardless of
enrollment state; `MUTICULA_ID`, when present, only decides whether the resulting commit (if
any) goes through the gate — it never decides who was allowed to run `pg-drop` in the first
place.

**The detached deployment worktree is never enrolled.** It shares the common git dir (claims
and the beacon stay visible from it — visibility, not authority) but is not itself a muticula
participant: no publish-gate step running inside it calls a muticula verb, and it inherits no
claim implicitly. All source-checkout coordination (revert preparation, the commit itself)
happens in the valid enrolled client's primary checkout, before the snapshot is materialized.

**Q5, reframed (P4).** The original framing — "register as a sharp and claim, or keep a
flock" — was a false choice: a read-only `--check`/`status`/`plan` step needs no source-edit
claim at all; a `muticula commit` step already carries one through the gate; the §3b
deployment mutex grants **neither** a claim nor beacon authority — it is a separate, narrower
resource. What remains genuinely open is narrower, and is carried into Open Questions below.

### Deploy target (P1, P2)

Muticula v0 does not model deploy targets (brief r3 §1 "Out of scope") — a clean seam, not a
contested one. States tracked per `(sha, host, leg)`:

```
unknown                          (no receipt found — the default; never read as not_deployed)
not_deployed                     (a receipt exists and positively says so)
deploying                        (in progress — the §3b mutex is held)
deployed_pushed                  (both steps landed, reconciled against remote — §"Remote movement")
deployed_push_pending            (deploy succeeded, push not yet attempted, ambiguous, or failed)
deploy_failed[:leg]              (a specific deploy.sh leg errored — additive legs can leave a mixed target)
```

A commit at `deployed_push_pending` has already changed live files on this host. majkee kept
the fixed fact (2026-09-29): it stays droppable. The drop plan for a deployed commit
re-deploys the new tip and prints the residual list (below); live files are handled
explicitly, never left silent. Per-leg receipts, not one whole-repo claim: a successful
`--codex-only` deploy is never recorded as "deployed" for the whole repository.

### Residual inventory (P2)

The earlier source-tree `comm` sketch compared the wrong trees: source and destination names
differ (`zsh/config.office.zsh` → `~/.config/zsh/config.zsh`, `codex/skills/` →
`~/.agents/skills/` — the full map is in this file's frontmatter, verified against the live
`deploy.sh`), and an incomplete deploy may not have installed every source file to begin with.

The adapter supplies a `source_to_destination()` mapping (the same legs used for deploy) and
the residual inventory is computed **on physical destinations**, comparing what a receipt says
was deployed at the *old* target against what the *new* target's mapping would produce:

- **Observed leftovers** — a destination path a prior receipt says this adapter deployed, that
  the new target's source mapping no longer produces.
- **Candidates** — a destination path that exists but carries no receipt evidence linking it to
  any publish-gate deploy (pre-existing or unrelated file); reported separately, never merged
  into "observed."
- **Forward deletions count too** — a commit that *deletes* a source file, once deployed,
  leaves its old destination behind exactly the same way a backward move does; this is not
  only a backward-move concern.
- **Filenames stay lossless.** Comparison uses NUL-framed listings (`git ls-tree -z`, `find
  -print0`), never newline-split, so a legitimately odd filename cannot corrupt the diff.

Printed as an explicit, non-actioned list — no auto-delete, ever (no-`--delete` gavel).

### Prefix publication

Unchanged from the prior draft: buffer commits form a linear chain within a verified segment
(§1), so publishing `c_k` **is** publishing the prefix `c_1..c_k` — `c_k`'s tree already bakes
in every earlier change by git's own definition. Selecting a middle commit lists `c_{k+1}..c_N`
as explicitly remaining unpublished. Wanting `c_{k+2}` but not `c_{k+1}` is not a buffer
selection — it is a replan (revert `c_{k+1}`, or an interactive rebase before re-selecting),
never a silent cherry-pick underneath a checkbox tick.

### Snapshot fidelity (P1)

`deploy.sh` runs `gen-temple-map.sh` in write mode before the zsh rsync. Run unmodified against
a pinned `--ref` snapshot, this would write bytes that were never actually committed at `<sha>`
the moment the generator's live output differs from what `<sha>` has on disk. **Resolution
(§3a, now mandatory):** the adapter runs `gen-temple-map.sh --check` inside the detached
worktree, before the rsync step; **any nonzero exit refuses the whole plan** — "commit
`1de7f27`'s `projects.json` and `temple-project-map.zsh` disagree — commit the regenerated
artifact first, then replan." `deploy.sh` still runs the generator in write mode; with the
check green beforehand, that write reproduces the committed bytes exactly, so the snapshot
stays pure. The check script's own resolved identity (sha256) is recorded in the plan (§4).

### The `--worktree` escape

Retired reading, unchanged from the prior draft: `"materialize": "worktree"` never means
"deploy whatever is sitting dirty in the working tree." It means `git worktree add --detach
<tmp> <sha>` — turning a pinned, committed `<sha>` into a real on-disk snapshot. There is no
flag anywhere in this design that deploys uncommitted content; a hand-test of a dirty local
tree remains the plain, un-gated `bash deploy.sh` (SYNC_DISCIPLINE step 5), untouched and out
of scope here (see §3a on why that shortcut is not a compliant exception to this gate).

### Remote movement (P6)

Between plan confirmation and push, the adapter re-checks `git ls-remote origin
refs/heads/main` as a **cheap early-exit optimization** against the plan's `observed_base` —
useful, but not atomic: another writer can move the ref in the gap after that read. The actual
correctness comes from two things together, not from the pre-push check alone:

- **Git's own fast-forward constraint on a normal (non-force) push.** The push either advances
  the ref to exactly `<sha>` or is rejected outright — there is no partial or ambiguous
  "moved-but-not-quite" outcome from git's side.
- **A post-push reconciliation read** (§4 step 7): `ls-remote` again, asserting the remote ref
  now equals `<sha>`. If the push exit code and the reconciliation read disagree — exit 0 but a
  mismatched ref — the operation is `unknown`/`partial`, never silently retried and never
  silently reported as success.

No force push, no unspecified lease, anywhere in this design. On rejection or reconciliation
mismatch, the operation refuses, preserves its `deployed_push_pending` (or equivalent) receipt
unchanged, and tells the operator to `git pull --rebase` (per §1a's policy) and rebuild a fresh
plan — publish-gate never rebases the buffer onto a moved target on the operator's behalf, and
never silently substitutes a new tree under an old approval.

---

## Open questions for majkee

Proposals, never decisions — each needs a gavel.

1. **DECIDED (majkee, 2026-09-29):** every unpushed commit stays droppable, even at
   `deployed_push_pending`. Drop gets its own command (`pg-drop`) and, later, a dashboard
   button. The drop plan re-deploys the new tip and lists the residuals (§2, §7).
2. **(?)** Should publish-gate reuse muticula's exit-code convention (`0`/`1`/`3`/`4`), or keep
   an independently numbered scheme? Not load-bearing either way.
3. **(?)** Rename the manifest key `materialize` back toward the RUNBOOK's original
   `--worktree` word, now that its meaning has narrowed to an implementation-strategy flag?
   Cosmetic, but the old name risks being misread as the bypass Cartan flagged.
4. **(?)** Deployed-stamp/receipt location: `$(git rev-parse --git-common-dir)/publish-gate/`
   (this design's proposal) vs. `~/.local/state/ia-sync/` alongside `install-pkgs`'s
   `installed.json`. Both are host-local/never-synced; picking one is a placement call.
5. **(?) [reframed, §7]** The original dichotomy — register as a muticula sharp and claim, or
   keep a flock — was false (a check needs no claim, a commit already carries one, the §3b
   mutex grants neither). What remains open: does publish-gate ever need its **own**
   `MUTICULA_ID`/`MUTICULA_KEY` for a write-side git step (revert preparation) it performs
   non-interactively, or does it always act inside an already-enrolled human/agent identity?
6. **(?)** Residual listing (§7) is list-only, matching the no-`--delete` gavel. Should a later
   phase ever offer a confirmed, one-file delete action, or is listing-only permanent?
7. **(?)** Placement of the *core* buffer model nablarva consumes: a standalone package
   ia-sync hosts and nablarva points at, or a copy nablarva vendors/symlinks? Really
   nablarva's placement call, named here so it isn't lost.

---

## What this design deliberately does not do

- Implement anything — no changes to `deploy.sh`, `SYNC_DISCIPLINE.md`, `zsh/`, or any live
  file. A numbered sibling session opens after GO.
- Build the dashboard/TUI view — the JSON CLI contract (§5) is the interface; a view is later.
- Decide nablarva's language, store, or its own publishing semantics beyond "no adapter ⇒
  publish == push," and beyond §1a's honest statement that its current history does not
  qualify for v0's linear-segment selection as-is.
- Own or re-specify any of muticula's named resources (claims, the beacon, the commit gate's
  internals) — §7 only draws the boundary line, including the corrected note that r3 has no
  deploy-target reservation API to defer to.
- Pin exact JSON schema versions, mutex timeout numbers, or the receipt file's on-disk format
  beyond the sketch in §2a/§5/§3 — implementation-phase detail, not architecture.
- Resolve the open questions still open (Q1 is decided) — each is majkee's call.
