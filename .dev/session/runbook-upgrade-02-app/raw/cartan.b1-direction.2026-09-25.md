# B1 navigation draft — occupation protocol and worktree complement

Status: operator direction captured; B0 independently disposed on 2026-09-25. Proposed
boundary conditions below feed cycle 05's concrete B1 packet. No implementation or shared-canon
change is authorized by this note. Sources: majkee's operator-carried Trajectory message,
cycle-03/04 RETURNs, their raw evidence and the two muticula-verifier VERDICTs.

## Verified B0 boundary

- [Cycle 03](../_bus/03.muticula-verifier.verdict.md): **ACCEPT**, limited to the observed Claude
  seam. Healthy main/child denial has print and interactive evidence; fault cases were measured
  in print mode. Authenticated `--bare` remains untested. The operator-reported fixture trust
  exception is explicit; current entry absence is verified, whole-file restoration is not.
- [Cycle 04](../_bus/04.muticula-verifier.verdict.md): **STOP**. Native Codex observations remain
  useful, but the run violated the no-global-trust-edit gate. Its exact fixture block was removed;
  no pre-test configuration hash proves whole-file restoration. Interactive tool denial/control
  and child identity are evidenced, but the required before/after file hashes are absent.
- Both tested runtimes allowed covered writes when the tested guard failed to return a valid
  blocking decision, and exposed disable/uncovered-tool bypasses. These observations constrain
  the architecture; they do not qualify reservations or strict protection of interactive work.
- The two terminal branch dispositions permit the head's turn-01 join. They do not close the
  RUNBOOK's muticula v0 gate or authorize a build, rerun, deployment or another commit.
- Retention remains unresolved: 25 Claude and 10 Codex decisive JSONL files are ignored, and
  both evidence packages remain untracked. Preserve them and their fixtures in place. A later
  retention decision must respect SYNC_DISCIPLINE's machine-state exclusions; no force-add,
  renaming, packaging or ignore-rule exception is implied. The Claude logs count is 107, not
  the RETURN's 106; the witness found the copied logs byte-identical to the fixture.

## Direction and proposal ownership

Majkee's direction: an **occupation protocol** for files controlled by another session;
newcomers queue, get a landmine autoresponse, and can unblock after commit. Trajectory's
proposed constraint: **deny + ticket + retry**, never a hook that waits for the holder.
Release belongs to the holder's own commit of held paths.

Trajectory's separate recommendation: use worktrees for independent tasks and reserve
occupation claims for a small set of shared surfaces such as journal, pulse and AGENTS.
This hybrid is a candidate operating default, not a gaveled implementation rule. These are
shared files, not all literally `_bus/` files; existing numbered BUS records have distinct
writer ownership which should remain intact.

## Head's boundary conditions for the next packet

1. **Grant is atomic; a queue ticket is not permission.** An occupied resource returns its
   holder, conflicting scope, stable ticket and retry action immediately. A later successful
   claim acquisition changes ownership. Hooks never wait on another participant. Define queue
   ordering and cancellation in the core before promising fairness or automatic scheduling.
2. **Revalidate after waiting.** The newcomer reads the latest file after grant and checks the
   baseline before writing. A ticket wake-up does not make an old edit fresh.
3. **Commit completion and release are different facts.** Make release-on-commit an explicit
   holder-selected completion policy, then automate only the verified transition. The receipt
   must bind actor incarnation, claim ID/generation, checkout, commit and exact claimed path
   set. Git author name, HEAD movement or a generic post-commit notification is insufficient
   evidence that this holder completed those claims.
4. **Release only completed scope.** Require no admitted operation still writing, and verify
   that the held paths have the expected committed content with no outstanding changes. A
   partial commit cannot release an entire subtree. A failed commit, foreign commit, stale
   generation, dirty held path or missing receipt leaves the claim occupied for explicit
   completion/recovery. Untracked resources and non-Git resources need an explicit release
   rule; a Git commit cannot complete them by implication.
5. **A shared index is another resource.** Claims on files do not by themselves make a shared
   staging/commit operation belong to one session. The B1 packet must either reserve that
   operation explicitly or defer automatic commit release until its attribution is proved.
6. **Worktrees complement claims.** Independent checkout/index state can reduce contention;
   shared source workspaces and external targets still need named ownership. Reusing the same
   filename across isolated checkouts is not necessarily a physical-file conflict. Define
   resource identity before enforcing folder-wide claims.

## B0 limits the next contract must preserve

- Separate successful tested denial, observed bypass/failure, uncovered tools, and untested
  modes. Neither a successful fixture nor model compliance establishes all-writer protection.
- Internal error-to-deny handling is useful, but cannot fix a missing executable, disabled
  hooks, or a timeout before the runtime gets a decision. Do not rename this hard fail-closed
  enforcement merely because the guard catches exceptions when it runs.
- A SessionStart registration marker is enrollment evidence. It cannot attest continued hook
  health or stop a later unguarded mutation. A truthful dashboard needs unknown/uncovered
  states; claiming a strict lane requires an independently enforced admission boundary.
- Keep the interactive/headless distinction. Fault results measured only in print/exec do
  not become interactive measurements. `claude -p` remains B0 instrumentation only.
- The witness confirmed child identity fields at actual hooks in both runtimes. This refines
  the earlier conservative capability map for the measured cases only; a runtime session ID
  alone still does not bind every independent writer or establish a trustworthy claim holder.

## Smallest candidate B1 boundary

A local transactional occupation core plus deterministic fixture clients: acquire/deny-ticket,
inspect, cancel/retry, explicit release and generation-safe completion receipts. Test racing
claimants, overlap, cancellation, stale retries and release attribution. The live dashboard,
automatic worktree creation, runtime adapter rollout and automatic commit release stay outside
that first implementation unless their exact proof and authority are added to the packet.

This is a sequencing proposal: it preserves majkee's desired experience without pretending
that B0 has already supplied a reliable commit-to-release or fail-closed runtime boundary.
The head issues a build POINT only after B1's actual scope is gaveled. Cycle 05 asks Trajectory
to challenge these boundaries and supply one concrete packet for that decision. Nablarva's
PROJECT.yaml still leaves the animal's language unresolved; an experimental B1 language/store
proposal cannot silently settle it.
