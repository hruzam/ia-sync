---
what: "B1 packet proposal — muticula occupation core (cooperative, deterministic)"
from: "trajectory-dashboard (session ff-sync.trajectory.cSharp-muticula, renamed from ...cSharp-dashboard and worktrees)"
for: "cartan-muticula verification · majkee gavel"
date: "2026-09-25"
status: "PROPOSAL — no source created, no build authorized by this file"
---

# B1 — occupation core packet

**One sentence:** a local, transactional, *cooperative* occupation core with a JSON CLI, proven
by deterministic black-box tests in disposable fixtures — arbitration logic only; no runtime
enforcement, identity binding, hooks, dashboard, worktree automation or automatic release.

## 1. What B1 proves and what it does not

| B1 proves | B1 does not prove (later brick) |
|---|---|
| Atomic all-or-nothing grants, overlap rules, FIFO queue, cancel, idempotent retry | That any runtime asks the core before writing (B2 adapters) |
| Generation-safe release; stale holders rejected | That an actor id belongs to the process presenting it (B2 binding) |
| A pure **completion check** (commit ↔ claim) with pass/fail reasons | Automatic release on commit (B3 integration, after B2) |
| Crash/restart consistency of the store; no time-based expiry | Hook health, fail-closed enforcement, arbitrary-writer coverage |

**Cooperative means:** the core's answers are correct and durable; honoring them is the client's
job until B2 binds real runtimes. B1 must never be described as "protection".

## 2. Resource identity (the model the tests pin)

- **File / subtree:** `(host, checkout_root, repo-relative canonical path)`. `checkout_root` =
  `git rev-parse --show-toplevel` realpath. Different checkout roots (separate worktrees) are
  **different resources** even for the same logical file — isolation is the point of worktrees.
- **Overlap** by path components: `src/a` covers `src/a/x`, never `src/abc`. Subtree vs file
  inside it conflicts both ways.
- **Creates:** canonical existing parent + suffix; claiming a not-yet-existing path is legal.
- **Renames:** require holding **both** source and destination; the core exposes this as a
  single two-resource acquire (all-or-nothing).
- **Symlinks:** resolved at request time; a path whose realpath leaves `checkout_root` is
  **rejected `unsupported`** in B1. A symlink changing after grant is out of scope (stated).
- **Hardlinks** (`st_nlink > 1` on an existing regular file): **rejected `unsupported`** in B1.
- **Named resources:** `git-index:<checkout_root>` and `external:<label>` (e.g.
  `external:deploy-target:office`). The index is claimable like any resource so a committer can
  hold staging+commit explicitly; B1 does not infer it from file claims.
- Case-folding filesystems: not supported (office/home are ext4); stated, not tested.

## 3. Operations (design vocabulary; CLI names are the builder's)

All mutations take a caller-chosen `request_id`; repeating it returns the original outcome.

| Op | Result |
|---|---|
| `register` → `actor_id` | random id + caller-supplied metadata (host, runtime, native session/agent ids as *unverified labels*) |
| `acquire(actor, resources[], request_id[, ticket])` | `granted {claim_id, generation, baseline}` **or** `occupied {holder, conflicting scope, ticket, position}` **or** `unsupported {reason}` |
| `inspect(resource \| actor \| all)` | current claims, queue, generations — read-only, never reserves |
| `cancel(ticket)` | removes the ticket; queue re-orders |
| `release(claim_id, generation, request_id)` | only the current generation succeeds; else `stale` |
| `check-completion(claim_id, generation, commit)` | pure check, returns PASS/FAIL + reasons (§5); mutates nothing |
| `recover(claim_id, --operator, reason)` | explicit, audited transfer/release; never automatic |

`baseline` = content hash per granted existing file at grant time. The client compares its edit
base against it (**re-read before write**); a stale base is the client's refusal, the core only
makes it detectable.

## 4. Queue semantics (no waiting hook, ever)

- **Deny + ticket + retry.** `acquire` never blocks. An occupied answer carries a ticket and a
  FIFO position per resource set.
- **All-or-nothing, no hold-and-wait:** a ticket reserves nothing, so no deadlock is possible.
- **Strict FIFO** among ticket holders: when resources free, only the first eligible ticket can
  acquire them; a newcomer without a ticket queues behind. A retry with a ticket that is not yet
  first returns `occupied` with the current position.
- **A dead ticket blocks the line until cancelled** — visible in `inspect`, cancellable by its
  actor or `--operator`. No time-based pass-over in B1 (that would be expiry in disguise); any
  pass-over policy is a separate, tested decision later.
- Claims **never expire**. Idle time changes nothing (tested with an advanced clock).

## 5. Completion check (the honest core of "unblock after commit")

`check-completion` returns **PASS** only if all hold, each reported separately on FAIL:

1. claim exists, is held, generation current;
2. the commit exists in `checkout_root` and **carries the trailer**
   `Muticula-Claim: <claim_id>@<generation>` (cooperative binding: the holder writes it);
3. every path the commit touches under the claim ⊆ claimed resources, and every claimed file the
   holder declared as "done" is in the commit;
4. the held paths are **clean** after the commit (no worktree or index difference);
5. no other actor's claimed path appears in the commit (foreign-content guard — the shared-index
   collision we actually had).

Required FAIL fixtures: foreign commit (no/other trailer), partial commit, dirty held path after
commit, stale generation, non-existent/failed commit, commit carrying another holder's path,
untracked resource (a commit cannot complete it — explicit release only).

**Auto-release belongs to B3, not B1.** The trailer is self-asserted until B2 binds actor ↔
runtime; automating release on an unbound assertion would let any commit free any claim. B1
ships the check; B3 wires `post-commit → check-completion → release` after B2 identity proof.

## 6. Placement, writer, witness

- **Source (proposed, not created):** `~/unikuklatrix/nablarva/toolbox/muticula/` — sibling of
  `toolbox/termbrana/`, per nablarva L6 (experimental organs build here; promotion = reviewed
  merge) and L12 (one repo on `core`, plain pull/push, **parallel work via `git worktree`** —
  the builder works in its own worktree). Carries the PROJECT.yaml provenance header
  (name · status · schema · source · trust note).
- **Language/store:** **not decided here.** PROJECT.yaml docket 2 is open (python-stdlib vs C++).
  To keep B1 from voting on it, the acceptance suite is **black-box against the CLI's JSON
  contract**, so the core's implementation language is swappable. Decision for majkee: implement
  B1 in python-stdlib+sqlite3 *as an experiment explicitly not counted as a docket-2 vote*, or
  wait for docket 2. The store file lives outside all repos (XDG state dir) — ia-sync's
  `.gitignore` already excludes `*.db`, consistent with that.
- **Evidence:** `~/ia-sync/.dev/session/runbook-upgrade-02-app/raw/b1-core/` (test transcript,
  JSON outputs, hashes — no JSONL session data).
- **Sole core writer:** `muticula-builder`. **Witness:** `muticula-verifier`. No amendment.
  Trajectory stays available for the B2 Claude adapter (the B0 Claude seam is its evidence).

## 7. Deterministic acceptance cases (black-box, disposable fixture repos)

| ID | Case | Pass condition |
|---|---|---|
| A1 | 20 processes race `acquire` on one file | exactly one `granted`; 19 `occupied` with distinct tickets, positions 1–19 |
| A2 | subtree held, file inside requested (and reverse) | `occupied` both ways |
| A3 | `src/a` held, `src/abc` requested | `granted` (no false overlap) |
| A4 | batch of 3, one conflicting | nothing granted; store unchanged |
| A5 | same `request_id` repeated | identical response; one claim |
| A6 | FIFO: tickets 1,2 queued; holder releases | only ticket 1 can acquire; ticket 2 `occupied`, position 1 |
| A7 | cancel ticket 1 | ticket 2 becomes first |
| A8 | release with old generation after recover | `stale`; claim untouched |
| A9 | `kill -9` of a client mid-`acquire` (injected pause) | store consistent: either full grant or none |
| A10 | restart core/process, then `inspect` | claims and queue unchanged |
| A11 | clock advanced 30 days | claims still held (no expiry) |
| A12 | symlink escaping checkout; hardlinked file | `unsupported` |
| A13 | rename without destination held | `occupied`/`unsupported`, never partial |
| A14 | same relative path in two worktrees | both `granted` (distinct resources) |
| A15 | `git-index:<root>` held by X; Y requests it | `occupied` |
| A16 | completion: own full clean commit with trailer | PASS |
| A17 | completion: foreign / partial / dirty / stale gen / failed / carries other holder's path / untracked | FAIL with the specific reason each |
| A18 | `recover` without `--operator` | refused; with it: audited record written |

## 8. Explicit exclusions

No hooks installed or modified; no runtime adapters; no `claude -p` or `codex exec` anywhere in
the core or its tests; no dashboard/zsh/session wiring (clients stay outside core lifetime); no
automatic worktree creation; no automatic release; no deploy.sh; no cross-host; no model calls
(the suite is pure process/fixture tests — zero paid probes).

## 9. Retention boundary for the B0 evidence (recommendation, separate from B1)

`.gitignore:14 *.jsonl` exists to keep conversation/session data out of the repo — and the B0
`*.stream.jsonl` files *are* session transcripts, so the rule's intent genuinely applies; it is
not an accident to route around. Recommend: (1) keep the 35 raw JSONL files machine-local in the
bed until closure; (2) track a reviewed **manifest** (path · size · sha256) of them plus the
already-tracked matrix/verdicts, so their existence and integrity are provable without their
contents entering git; (3) if majkee wants the raw files durable, move them at closure to an
operator-chosen **non-git evidence home**, credential-scanned — never a renamed extension, never
an ignore negation slipped into B1. This is a closure/promotion decision, not B1 build work.
