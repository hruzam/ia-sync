# adr-guard.fixtures — natural red captures

Snapshotted 2026-07-07 before any repairs. These are the two breach classes the
gate was built to catch, preserved here as test fixtures (not synthetic data).

## 0006-inplace-edit.breach.snapshot.md

The current (post-breach) state of `temple/decisions/0006-model-effort-assignment.md`.
The breach: line 53 (the L2 matrix row for the `fable · high` scientist-strategist seat)
was modified in-place AFTER the 2026-06-25 lock date. The original text read `@Hypatia`;
it was swapped to `@Oraculum`. This violates doctrine §1b (ADRs are append-only — the
index.md rule: "superseded, never edited").

Check 1 of adr-guard catches this: any removed line in a status:LOCKED ADR = FAIL.

## 0007-evidence-rot.breach.txt and 0008-evidence-rot.breach.txt

Extracts of the `_mail/*/inbox/` citations in 0007 and 0008. These paths are gitignored
and drainable (inbox items are ephemeral). Citing them as evidence in a locked ADR creates
evidence rot: the referenced evidence can disappear while the ADR stands.

Check 2 of adr-guard catches this: any new `_mail/*/inbox/` reference in decisions/ = FAIL.

## Usage as test inputs

These fixtures are documentation of the naturally-occurring breaches. The gate's
deliberate-red test (adr-guard.zsh --deliberate-red) uses synthetic data in a sandbox.
These files serve as the human-readable proof that the breach shapes were real.

Repair of the breaches is a separate commit — Houston/Delta task, not this gate build.
