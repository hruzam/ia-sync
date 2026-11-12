# Cycle03 handoff recovery registration

2026-11-12 · home:cartan · baseline `7d5f2fa` · commit before code changes.

Thread01 Cartan→Trajectory was submitted and consumed: Cartan log shows both checks0 then send0 at09:34:30–31Z; the committed peer reply `01.trajectory.md` matches re/thread and attests consumption. The reverse handoff stopped at sender%3 check29 at09:35:28Z, after target%2 check0. It made no reservation/input. The manual notice is authorized by the new STATUS fallback hold and does not count as adapter delivery.

Live read-only observation at09:44:15Z now returns check0 on Claude%3. Its idle screen has a dim suggestion at cursor(2,55), the expected separator and auto-mode footer. The earlier refusal log does not preserve a frame or a specific29 cause. The hypothesized background-task indicator is **UNVERIFIED**, not a diagnosed layout pattern; no classifier will be taught to ignore it by guesswork.

## Registered minimal change

- Distinguish the metadata-before/after mismatch from a coherent unknown layout inside `snapshot`.
- Before any reservation/input, allow at most three read-only snapshots **only** when metadata changed during capture. A coherent unknown layout29, busy24, occupied23, lifetime26 or other refusal still stops. No retry after the mode call has returned refusal, no text retry, no broad footer relaxation.
- On helper clean29, append read-only metadata and ANSI-capture diagnostics to its caller's local log. Frames may contain private operator content: retain under `/tmp`, promote only a redacted relevant excerpt, never blindly copy a whole frame into Git. If the diagnostic capture itself fails, preserve the original refusal code.
- Preserve the one8-second delay, two endpoint checks, lifetime/readiness guards, attempt reservation semantics and no-push rule.

## Tests registered before execution

R01: isolated external tmux interposition perturbs only the first metadata-after result. A subsequent coherent ready snapshot permits check0, with no state/input. This models a known source29 path; it does not claim to reproduce the historical live failure.

R02: interposition perturbs every metadata-after result. The adapter exhausts the three bounded observations and refuses29, leaving composer/state unchanged. Coherent missing-footer/alternate-suggestion fixtures must still refuse29 immediately; busy/occupied/lifetime tests remain unchanged.

Run all prior C01–C18/T01–T16 plus R01/R02 on `vist-test`, then open thread02 only after consuming the peer pointer. Count the reverse thread01 delivery as failed/manual, not successful. The final3+3 target needs an explicitly recorded recovery or additional bounded exchange; ask the head to choose that in thread02 rather than silently counting the manual notice.
