# Cartan → Trajectory: publish-gate / muticula boundary

2026-09-25 · office · early design input requested by majkee through
`ff-sync.trajectory.cSharp-muticula` (same seat as `trajectory-dashboard`).

This is the muticula head's boundary recommendation, not publish-gate's formal CHALLENGE
RETURN. Its RUNBOOK and STATUS exist; its design and addressed POINT do not yet exist at
this review. Trajectory remains that session's author and STATUS owner. Nothing here changes
its fixed gate, authorizes implementation, or locks canon.

**Recommendation: publish-gate is a client of muticula for reservation.** They are separate
components with distinct jobs. Muticula arbitrates who may hold a resource; a named publisher
actor holds it; publish-gate decides what to publish and records the operation's progress.

## Ownership without a second authority

| Concern | Authority / responsible participant |
|---|---|
| Claim grants, overlap, queue, generation, release/recovery | Muticula, through one active reservation provider |
| Pending commits, selection, approved plan, publication state and recovery | Publish-gate |
| Source-file claims and unfinished edits | The current authoring actors, until explicit release or delegated handoff |
| Staging / commit | The explicitly authorized committer actor, holding the required Git and file resources; it may be a publish-gate operation or an ordinary author |
| Deployment | The publisher actor holds the target claim; the project adapter acts on its behalf under the same operation/binding |
| Deployment semantics and actual target inventory | The project adapter; ia-sync does not define other projects' publication policy |
| Approval and meaningful recovery decisions | Majkee; a resource grant is never Git/deploy permission |

The gate does not acquire permanent ownership merely because a commit appears in its buffer.
It must not steal an author's active claims, infer authorship from Git author/trailers, or
interpret a commit as automatic release of a deploy target. Release is scoped to the resource
and lifecycle actually completed. A dashboard is a view/client of these contracts.

## Git needs more than a checkout-labelled index

Use the existing draft's §3.5.4 distinction between checkout/index operations and shared
repository/ref operations. Separate worktrees have separate indexes and HEADs, but normally
share branch refs. That is documented Git behavior, not an architectural preference.
[Git worktree: details and refs](https://git-scm.com/docs/git-worktree#_refs)

Proposed resource resolver contract:

- Staging uses the **actual resolved index identity**, plus the affected file claims where
  worktree content is read or changed. `git rev-parse --git-path index` accounts for index-path
  relocation; reject unsupported overrides instead of silently keying only by checkout root.
  [Git rev-parse: --git-path](https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---git-pathltpathgt)
- Committing, rebasing, dropping and publishing identify the **common repository and affected
  refs**, in addition to any worktree/index they mutate. A deliberately coarse common-repo
  transaction claim is an acceptable first implementation if documented; claiming an index
  alone is not equivalent. Two isolated checkouts must still conflict when updating the same ref.
- Deploy claims identify the **physical destination set on the target host**. Different projects,
  worktrees and full/partial adapters that touch the same destination must resolve to overlapping
  claims. Free-form labels are not proof that physical targets are distinct.

Keep this mapping in one shared contract/helper. Publish-gate declares its intended operation;
its adapter resolves the required resource set using that contract. Neither side creates a
parallel mutable ownership board. Git's own internal locks still apply; muticula coordinates
the longer application operation around those commands.

## Minimal lifecycle to design against

1. **Prepare and review.** Identify the exact candidate commit OID, base/ref expectations,
   adapter version, host, deploy legs and destinations. A branch name or changing HEAD is a
   selector, not an immutable plan. Do not hold a deployment claim while waiting on a human.
2. **Acquire and revalidate.** The authorized executor requests its complete resource bundle
   promptly. Conflict produces a ticket/return, not a waiting hook. Recheck the approved plan
   after grant; changed inputs invalidate it. Specify a no-hold-and-wait policy for actors that
   already own other claims, rather than assuming a batch API eliminates every deadlock.
3. **Execute the exact plan.** The adapter uses the pinned committed snapshot. Staging is needed
   only if this authorized operation creates commits; selecting existing commits need not touch
   the authors' indexes. No unrelated staged content may enter the candidate.
4. **Record per-phase outcomes.** Keep an operation ID, actor/claim generations, approved OIDs,
   target manifest and observed results. This is publication state, not another claims table.
5. **Finish or recover.** Release only after no admitted writer remains and the result is known.
   On a crash/unknown result, retain the uncertain operation and reconcile its effects before
   retry/recovery. Identity binding is necessary for later automatic release; it does not by
   itself authenticate a trailer, drain a writer, or make check-then-release atomic.

An unavailable reservation provider means the integrated publisher refuses to start its
mutations. B1's cooperative core does not protect against arbitrary clients that skip it.
If publish-gate ships before muticula, a temporary standalone locking provider needs an explicit
scope and replacement plan. Do not let independent `flock` and muticula tables both issue grants
for one resource; migration must drain/reconcile the old provider before switching. An internal
mutex below one provider is fine; an independently authoritative second lock service is not.

## Primary challenge to the opening publish-gate brief

**REVISE the assumption “unpushed therefore safely droppable.”** The gaveled order is deploy,
then push. Deployment can succeed and push can fail, so a commit can already have external
effects while still unpushed. Even Git's atomic push covers remote ref updates, not local
deployment. [Git push: --atomic](https://git-scm.com/docs/git-push#Documentation/git-push.txt---atomic)

Concrete failure: deploy commit C; network/push fails; UI still classifies C as unpublished;
operator drops C; live files still contain C. An additive deploy also cannot undo deleted or
renamed outputs merely by redeploying an older commit. Existing `deploy.sh` is additive and its
legs run sequentially, so interrupted deploys can leave a mixed target too.

The smallest alternative is a persistent **publication operation with separate deploy and
remote-ref outcomes**, including partial/unknown and `deployed, push pending`. “Drop” eligibility
must account for those effects, descendant commits and active users of the history, not just
absence from one remote branch. Treat completed external effects as a recovery/revert decision.
Record host-local deployed receipts per scope/leg; one successful Codex-only deploy must not
make a whole-repository “deployed at C” assertion.

The design should also settle these before a formal GO:

- **Selection:** commits form a dependency graph. Define prefix publication or an explicit
  reconstruction/integration plan; checkboxes cannot imply independent commit deletion.
- **Snapshot fidelity:** current `deploy.sh:239` runs `gen-temple-map.sh` before copying the zsh
  tree. Generating different bytes after selecting C would violate deploy-only-committed.
  Prefer generating and committing beforehand, then checking during deploy. Any artifact-build
  alternative must bind its inputs and output digest explicitly rather than claim C's exact tree.
- **No raw-worktree bypass:** the RUNBOOK's proposed `--worktree` escape conflicts with the
  operator's committed-content rule unless it only identifies a checkout from which a pinned
  commit is materialized. An unchecked live-tree deploy would require an explicit policy change.
- **Remote movement:** ia-sync still requires pull before push. Resolve required integration
  before pinning/reviewing the candidate; movement after deploy creates a recovery/replan edge,
  not permission to push another tree under the previous approval. A local claim cannot lock a
  remote writer. Preserve the no-rewrite-of-published-history rule.

## Evidence and handoff

Read locally: publish-gate RUNBOOK/STATUS; muticula draft §3.5.4–3.5.5 and B1 packet;
`deploy.sh` source/flags/ordered legs/generator; SYNC_DISCIPLINE's compose-first and pull-before-push
rules. External references above are official Git documentation. Findings about failure ordering
are design counterexamples, not claims that a deployment was run. No deployment, commit, push,
runtime change or publish-gate artifact edit was performed for this review.

Trajectory can fold this input into its design. The formal challenger receipt still belongs to
the exact POINT/RETURN path in publish-gate's own bed when that design is ready.
