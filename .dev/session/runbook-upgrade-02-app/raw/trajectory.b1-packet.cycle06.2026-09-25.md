---
what: "B1 packet, cycle 06 revision — muticula cooperative occupation core"
from: "trajectory-dashboard (session ff-sync.trajectory.cSharp-muticula)"
for: "cartan-muticula verification · majkee build gavel"
supersedes: "raw/trajectory.b1-packet.2026-09-25.md (frozen; kept as cycle-05 evidence)"
date: "2026-09-25"
status: "PROPOSAL — no source, no build, no store created by this file"
---

# B1 — cooperative occupation core (revised)

B1 is **resource arbitration only**: a transactional core with a JSON CLI, proven by black-box
tests in disposable fixtures. It does not enforce anything, bind identities, install hooks,
resolve Git or deploy targets to physical resources, or release claims automatically. Every
rule below has a matching acceptance case in §9. Findings F1–F6 refer to VERDICT 05.

## 1. Claims B1 makes, and does not

B1 claims: correct, durable, deterministic arbitration among clients that ask it.
B1 does not claim: that clients ask (B2), that an `actor_id` is who it says (B2), that a
completion check authorizes release (B3), physical-collision coverage for opaque named keys (§3).

## 2. Resource types (F4)

| Type | Key | Overlap rule |
|---|---|---|
| `file` | `(checkout_root, path)` | equal key; or a `subtree` of the same checkout containing it |
| `subtree` | `(checkout_root, path)` | path-component prefix either way (`src/a` ⊇ `src/a/x`, never `src/abc`) |
| `named` | `(namespace, key)` opaque strings | equal `(namespace, key)` only |

Normalization at request time: `checkout_root` = realpath of `git rev-parse --show-toplevel`;
`path` = repo-relative, `.`/`..` resolved against realpath of the existing parent, no trailing
slash. Rejected as `unsupported` (never partially granted): a path whose realpath leaves
`checkout_root`; an existing regular file with `st_nlink > 1`; a `checkout_root` that is not a
git toplevel. Not handled in B1, stated: symlink targets changing after grant; case-folding
filesystems. A path not yet existing is legal (creates). Rename is not observed by the core — a
client wanting one acquires source **and** destination in one bundle (§4).

## 3. Git and external resources — explicit resolver deferral (F6)

B1 treats Git and deploy resources as **typed opaque `named` keys** — e.g.
`git-index:<resolved index id>`, `git-refs:<common dir>`, `deploy:<host>:<destination set id>` —
and arbitrates them by equality only. It makes **no** claim that two keys denote distinct
physical things. The resolver (index path via `git rev-parse --git-path index`, shared refs via
the common dir, deploy destination sets) is a **client contract** shared by later bricks and by
publish-gate; B1 neither implements nor tests it. Worktrees therefore get no automatic
ref-collision guarantee from B1: separate worktrees share branch refs, and only a client that
claims `git-refs:<common dir>` is arbitrated.

## 4. Requests, tickets and replay (F1)

- **Two identities.** `request_id` = one attempt, scoped to `(actor_id, operation, request_id)`.
  `ticket_id` = a stable queue position, created at the first `occupied` answer and carried
  across later attempts. A later attempt (new `request_id`) presenting the ticket can be granted.
- **Replay.** Same scoped `request_id` + byte-identical canonical payload → the originally
  recorded response, marked `"replayed": true`, **plus** the claim/ticket's current state. A
  replayed `granted` is history, never authorization: authority is always the pair
  `(claim_id, generation)` validated against current state by every later call.
- **Payload mismatch.** Same scoped `request_id`, different payload → `request_conflict`,
  no state change.
- **Per operation:** `register` (idempotent → same `actor_id`), `acquire`, `cancel` (cancelling
  an already-cancelled ticket → `already_cancelled`, success class), `release`, `handoff`,
  `recover` (all idempotent on `request_id`). `inspect`, `check-completion`, `verify-baseline`
  are read-only and take no `request_id`.

## 5. Queue and the hold-and-wait rule (F2)

- **No queued expansion while holding.** An actor holding any claim may acquire more only if the
  whole new bundle is free *now*. If any part conflicts it gets `refused` with reason
  `hold_and_wait` — **no ticket**. Only actors holding nothing can queue. A waiting actor
  therefore never holds anything, so the wait-for graph has no cycle: no deadlock. To need more
  under contention, an actor releases (or hands off) and requeues for the full bundle.
- **One enqueue order.** Every ticket gets a monotonic global sequence number at creation.
- **Eligibility.** A ticket may be granted when all its resources are free **and** no live ticket
  with a lower sequence overlaps any of them. Later tickets on disjoint resources proceed —
  unrelated work is never blocked by an earlier ticket.
- **Newcomer without ticket:** granted only if eligible by the same rule; otherwise `occupied` with
  a new ticket at the end of the sequence.
- **Dead tickets** block overlapping successors until cancelled — by their actor, or by
  `--operator`, which in B1 is a cooperative assertion recorded as such, not proof of a human.
  No timeout, no pass-over. Claims never expire.

## 6. Operations and data returned

| Operation | Effect / result |
|---|---|
| `register(meta)` | `actor_id`; `meta` (host, runtime, native ids) stored as unverified labels |
| `acquire(actor, bundle, request_id[, ticket_id])` | `granted {claim_id, generation, base_oid per checkout, baseline}` · `occupied {holder, conflict, ticket_id, sequence, ahead}` · `refused {hold_and_wait}` · `unsupported {reason}` |
| `release(claim_id, generation, request_id)` | `released`, or `stale` if generation not current |
| `handoff(claim_id, generation, to_actor, request_id)` | atomic transfer; generation +1; old generation becomes `stale` |
| `recover(claim_id, --operator, reason, request_id)` | audited release or transfer; generation +1 |
| `cancel(ticket_id, request_id)` | `cancelled` / `already_cancelled` |
| `inspect(resource \| actor \| all)` | claims, tickets with sequence, generations |
| `verify-baseline(claim_id, generation, paths)` | per path: grant-time hash vs current hash → `fresh` / `stale_base` |
| `check-completion(...)` | §7; read-only |

`baseline` = content hash of each granted existing file at grant time. The client must re-read
and call `verify-baseline` before writing; the core only makes a stale base detectable.

## 7. Completion check — inputs, predicate, snapshot (F3)

**Inputs:** `claim_id`, `generation`, `candidate_oid`, `completion_scope` (subset of the claim's
`file`/`subtree` resources; default all). **Read-only**: records nothing, releases nothing.

**Snapshot boundary:** the check pins `base_oid` (from the grant), `candidate_oid` and
`head_oid` (checkout HEAD when the check starts), reads index and worktree once, and returns all
three OIDs plus `observed_at`. The result is valid only for that snapshot; B3 must re-run it
inside the claim transaction after draining admitted writers.

**PASS iff every predicate holds** (FAIL returns each failing reason):

1. `held` — claim held, generation current.
2. `lineage` — `base_oid` is an ancestor of `candidate_oid`, and `candidate_oid` is an ancestor
   of (or equal to) `head_oid` in this checkout. A commit merely existing in the repo fails.
3. `attributed` — every commit in `base_oid..candidate_oid` that changes any claimed path carries
   exactly one `Muticula-Claim: <claim_id>@<generation>` trailer for **this** claim. Another
   claim's trailer, several trailers, or none → FAIL `unattributed_or_ambiguous`.
4. `in_scope` — every commit carrying this claim's trailer changes only paths inside the claim.
   Extra unclaimed content → FAIL `outside_claim`.
5. `no_merges` — a merge commit in the range that changes claimed paths → FAIL `merge_unsupported`.
6. `committed_clean` — for every path in `completion_scope` (a subtree expands to the union of
   paths under it in `base_oid`, `candidate_oid` and the worktree): index entry and worktree
   content equal the `candidate_oid` blob, or the path is absent in all three (a delete).
   Renames are delete + add, and both sides must be inside the claim. A newly created, committed
   file completes. A file present in the worktree but untracked → FAIL `untracked_in_scope`.
7. `git_resource` — a `named` resource in `completion_scope` → FAIL `not_git_completable`
   (explicit release only).

Commits in the range that carry no trailer and touch no claimed path are ignored — concurrent
unrelated work on a shared branch doesn't fail the check. The trailer is caller-written and
forgeable in B1; PASS means "consistent", never "attributed" (identity is B2).

## 8. JSON, exit codes and state (F5)

Every command writes exactly one JSON object to stdout; diagnostics go to stderr only.
Common fields: `ok`, `result`, `op`, `state_path`, plus the result-specific fields above.

| Exit | `result` values |
|---|---|
| 0 | `granted`, `released`, `handed_off`, `recovered`, `cancelled`, `already_cancelled`, `registered`, `inspected`, `fresh`, `pass` |
| 3 | `occupied` |
| 4 | `refused`, `unsupported` |
| 5 | `stale`, `stale_base` |
| 6 | `fail` (completion) |
| 2 | `usage`, `request_conflict` |
| 1 | `error`, `store_unavailable` |

**State path:** `--state <path>`, else `MUTICULA_STATE`, else
`${XDG_STATE_HOME:-~/.local/state}/muticula/muticula.db`. Every test sets `--state` inside its
fixture, and the harness asserts the default path is untouched (absent before and after, or
unchanged digest). An absent or damaged store is `store_unavailable` — never "all free".

## 9. Acceptance cases (deterministic, zero model calls)

| ID | Case | Pass condition |
|---|---|---|
| A1 | 20 processes race one `file` | exactly one `granted`, 19 `occupied`, sequences 1–19 |
| A2 | 20 processes, 20 disjoint files | 20 `granted` |
| A3 | subtree held → file inside requested, and reverse | `occupied` both ways |
| A4 | `src/a` held → `src/abc` | `granted` |
| A5 | bundle of 3, one conflicting, actor holds nothing | no new grant; store delta = one ticket + request record |
| A6 | rename bundle (src + dst), dst held elsewhere | `occupied`, nothing granted |
| A7 | same `request_id` + same payload | identical response with `replayed: true` |
| A8 | same `request_id`, different payload | `request_conflict`, exit 2, no state change |
| A9 | replay of a `granted` after `release` | historical response + current state `released`; `release` with that generation → `stale` |
| A10 | later attempt with the ticket, once first-eligible | `granted` |
| A11 | FIFO: T1 < T2 overlapping; holder releases | only T1 eligible; T2 `occupied`, `ahead: 1` |
| A12 | T1 (A+B) < T2 (B) < T3 (C); A, B, C free except A held | T3 granted; T2 waits behind T1; T1 granted when A frees |
| A13 | hold-and-wait: X holds A, requests B held by Y | `refused hold_and_wait`, no ticket |
| A14 | expansion while holding, new bundle free | `granted` |
| A15 | cancel T1 (twice) | `cancelled`, then `already_cancelled`; T2 becomes first |
| A16 | dead ticket, `--operator` cancel | cancelled; audit record marks the operator flag as asserted |
| A17 | `handoff` then old generation `release` | `stale`; new holder `release` works |
| A18 | `recover` without / with `--operator` | refused / audited transfer, generation +1 |
| A19 | `kill -9` mid-`acquire` (injected pause point) | store holds a full grant or none |
| A20 | restart, then `inspect` | claims, tickets, sequences unchanged |
| A21 | clock advanced 30 days | claims still held |
| A22 | escaping symlink; hardlinked file; non-git root | `unsupported` |
| A23 | same relative path in two worktrees | both `granted` (distinct `file` keys) |
| A24 | `named` contention (`deploy:office:x`) | second `occupied` |
| A25 | two unrelated fixture repos, no bed, no dashboard | independent grants; one store |
| A26 | `verify-baseline` after a foreign write | `stale_base` for that path |
| A27 | completion PASS: own trailer, in scope, committed clean, lineage ok | `pass` |
| A28 | completion FAIL per predicate 1–7 (one fixture each: stale gen, not ancestor, foreign/untrailered change, trailer commit outside claim, merge, dirty/untracked, named in scope) | `fail` with that exact reason |
| A29 | concurrent unrelated commit in range (no trailer, unclaimed path) | still `pass` |
| A30 | default state path | untouched by the whole suite |

## 10. Placement, stack, writer, witness

- **Source (proposed, created only at dispatch):**
  `~/unikuklatrix/nablarva/toolbox/muticula/`, built in an **isolated worktree** on a new branch
  from a committed base named in the build POINT (current `core` HEAD `4e76b64`). The main
  nablarva checkout currently carries uncommitted germline changes, so it must not be the build
  checkout. Provenance header per nablarva `PROJECT.yaml`. Promotion = reviewed merge (L6).
- **Evidence:** `~/ia-sync/.dev/session/runbook-upgrade-02-app/raw/b1-core/` — suite transcript,
  JSON outputs, digests. No JSONL session data.
- **State:** default path as in §8; tests use fixture state only.
- **Stack — majkee's decision:** python-stdlib + `sqlite3`, run as an experiment explicitly
  *not* counted as a docket-2 vote; or wait for docket 2. The suite is black-box against §8, so
  the core can be reimplemented later without changing a test.
- **Sole core writer:** `muticula-builder`. **Independent witness:** `muticula-verifier`.

## 11. Separation from publish-gate

muticula grants, queues and releases resources. publish-gate (its own session) is a **client**:
its executor acquires a bundle of `named` Git/deploy keys through the shared resolver contract
(§3), and publish-gate owns selection, plan, publication state and recovery. There is no second
mutable ownership table and no independent lock service issuing grants for the same resource.
Cartan's boundary note (deployed-but-unpushed state, prefix publication, snapshot fidelity,
remote movement) is input to publish-gate's design, handled in that bed — not B1 scope.

## 12. Exclusions

No hooks or runtime adapters; no `claude -p`/`codex exec` in core or tests; no dashboard or
`zsh/session` wiring; no worktree automation; no automatic release; no Git or deploy resolver;
no deploy.sh; no cross-host; no model calls.

## 13. B0 evidence retention (corrected)

Correction: RETURN-05 said the matrix and verdicts were "already tracked" — they are **not**
(both matrices, both B0 verdicts and all B0 packages are untracked). A reviewed digest
inventory records what existed and allows a later integrity comparison; it neither stores the
evidence nor guarantees it survives cleanup. The 35 JSONL files fall under `.gitignore:14`'s
"conversation/session data" intent. Raw retention, any commit of the untracked artifacts, and a
non-git evidence home are separate operator decisions — not B1 work.

## 14. Operator decisions remaining

1. Stack: python-stdlib+sqlite3 experiment, or wait for docket 2.
2. Queue policy as specified (§5: strict sequence eligibility, no queued expansion while holding,
   operator-cancelled dead tickets).
3. Build placement and base (§10), including the isolated worktree.
4. Worktree-first as the operating default for independent tasks.
5. B0 retention plan (§13).
