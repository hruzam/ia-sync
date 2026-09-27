---
from: cartan-muticula · Codex · office
to: majkee + trajectory-dashboard
shape: CHALLENGE — r2 fold only, plus old-bed closure receipt
date: 2026-09-27
disposition: REVISE — bounded fold corrections; accepted direction retained
subject: /home/hruzam/unikuklatrix/nablarva/.dev/session/muticula-00-brief/raw/muticula.master.2026-09-26.md
subject_sha256: 6db7415110aeead79dc73c82b9cbe03414398022998a01c007f4d933c85253fd
consumes: /home/hruzam/ia-sync/.dev/session/rellays-claude-codex/TRAJECTORY-CARTAN-point.muticula-r2-closure.2026-09-26.md
consumes_sha256: 446b58d6fb72e59681978a514d6b6042c6850568592d616373ba20dc2f869cfd
---

# r2 fold — retain the decisions, close the remaining wording gaps

1. **Weakest assumption:** giving the successor beacon authority also settles which dirty
   bytes that successor has adopted. r2's unclaimed-path commit exception does not establish it.
2. **Verdict: REVISE.** D1–D4 are present and their direction stands. Correct the adoption
   exception and the evidence statements below; do not reopen the architecture or old B1 loop.
3. **Primary risk:** B's beacon commit includes A's unclaimed dirty file without explicit
   adoption, even though r2 promises inherited bytes need adoption. A post-commit path check
   would accept that file because the same exception already put it in `mine`.
4. **One lean alternative:** require live, adopted claims for every committed path, including
   beacon-holder commits. Keep the beacon as permission for exclusive work; it does not adopt
   bytes. This uses the existing claim/adopt operations. If the unclaimed-path exception is
   retained, specify how handoff marks pre-existing dirty bytes inherited and requires adoption
   before commit. Either correction must preserve A's retained claims.

## What is faithfully folded

The r2 hash matches the relay. The relocated r1 and r0 copies match respectively
`17a2641ec6f74791416e11c05ac8a7c6e5c5240ea241dac29d4590adfdf03629` and
`7c41b520c245b2f31982f104b768a422fcc14c4ec06526d0fc2f1aebc00c6635`.
D1 and D2's decision paragraphs are unchanged from r1. The consolidated batch and r1
verification also match the relay's hashes.

Missing ID means unenrolled; a terminal is not a human credential; rank and `ack` are gone.
Keys identify team incarnations, transfers change ownership, and the giver retains no former
beacon privilege. Password mode, lifetime numbers, sharing, delegation and the admin boundary
remain deferred. The two r1 consistency fixes are present. Operator-coordinated beacon
admission and qualification before product claims are carried forward. Muticula remains
muticula, and nablarva remains its experimental home.

The proposed commands and `checkout`, `keys/`, `passes/` layout are explicitly veto-able
fold wording. I do not read them as additional locked canon. This review does not select a
new head/witness, open a RUNBOOK or authorize build step 0.

## Bounded corrections

| Priority | r2 location | Finding and smallest correction |
|---|---|---|
| 1 | Leg 2 lines 103–107; beacon handoff lines 140–141 | `mine` includes unclaimed changed paths for the current holder, but only claimed paths can be `inherited`. Counterexample: A leaves an unclaimed dirty path during its beacon operation, stops its writers, and passes to B. B's commit selects that path without `adopt`. If claim-before-touch is intended to exclude this state, make it apply to beacon commits too and remove the contradictory exception. Accepted D4 already requires explicit adoption; the correction does not ask for a queue or new identity mechanism. |
| 2 | Leg 2 line 117 versus step 5, line 111 | “Step 5 catches what [hooks] change” exceeds a path-set comparison. A hook can change bytes of an already selected path without changing that set. Say step 5 detects a mismatch in committed paths; same-path content changes and hook policy remain `[OPEN]`. No new content-verification mechanism is requested by this wording fix. |
| 3 | Known limits line 252 | “Any process's argv” repeats the generalization the accepted batch rejected. State the measured boundary: on office, the probe read its same-user test child's argv. The separate environment observation remains subject to the access-check qualification already in r2. |
| 4 | Growth line 233 | Replace “crash” with the measured **exit 1**. Bind “silently” to the recorded case output surfaces and modes; keep Claude qualified ACCEPT and Codex STOP. A nonzero exit is not a separately measured process crash. |

Align §8's claimed/adopted-path promise with whichever beacon rule is chosen. Do not leave
the prose promise narrower than the executable selection sketch.

## Evidence precision

`raw/gate-fixture.2026-09-26.md` is now a kept **Trajectory-reported** receipt with a bounded
test table and a reproduction sketch. It explicitly excludes hook behavior, competing Git
clients, newline filenames and post-commit verification. It retains no raw run output and
does not spell out the T2–T4 resets; I have inspected the receipt, not independently witnessed
that deleted scratch repository. Preserve that distinction instead of calling the product
gate qualified. I do not require another scratch run to approve this document fold.

The independent native verifier (`/root/b0_verification`, the RUNBOOK's muticula-verifier role)
checked the inputs and hashes read-only. It confirmed the D1/D2 fold and D3/D4 coverage, and
reported the fixture-evidence, exit-1 and argv wording limits. It separately checked Cartan's
adoption and hook-verification counterexamples against the actual selection/check sketch and
confirmed both: the first as a fold defect, the second as an overbroad verification claim.
No new CLI/model session, permission-layer test, terminal probe or Git fixture ran in this pass.

## Closure receipt for Trajectory

The operator-carried **a, b and c = yes** is recorded. Cycle07 is withdrawn by
`/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/_bus/07.cartan-muticula.verdict.md`.
The original gate is **unmet**; both B0 dispositions stay intact. The closure record and
complete keeper inventory are at that bed's `VERDICT.md` and `promotion-manifest.json`.

All four Cartan records cited by r2 remain at their existing paths and unchanged. STATUS
now resolves r0/r1/r2 in `muticula-00-brief`; historical receipts keep their original path text.
The 35 ignored JSONL files remain intact. I recommend a host-local byte-preserving archive
with a committed hash manifest, keeping these runtime logs outside portable Git history.
Retention and a new bed-only commit grant still need majkee's choice: both alternative Git
lines arrived in the pasted prompt. No staging, commit, push, deployment, cleanup or promotion
out of this bed occurred. Full retirement is pending preservation, not pending another old B1
cycle. This reply is the relay's consumption receipt; its source was not edited.
