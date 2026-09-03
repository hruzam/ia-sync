# RUNBOOK — upgrade-01-probe

```yaml
goal:            The bed's laws are amended from measured cold-resume failures, not from audit prose.
gate:            One cold-resume probe is run on a live session on BOTH hosts, timed, scored against the
                 six-point standard, and its scored record promoted to the project's evidence home.
participant_0:   [@Houston, {claude, opus, high}, office]
participant_1:   [@Janus, {claude, opus, high}, office]
participant_2:   [@majkee, human, office + home]
status_owner:    @Houston        # single writer for STATUS.md — see holds
schema_note:     conforms to raw.guides/runbook/GUIDE.md rev 2026-08-27
```

> **Read this once.** Nothing here changes during the session. Position lives in `STATUS.md`.
> This RUNBOOK was drafted on the bench and is live only once promoted into the session folder.

---

## Why this session exists

Two blind external audits produced twelve anchored remedies for this bed. Adopting them as a
set would reproduce the bureaucracy that killed three previous shapes. Every one of them is
justified by *prose reasoning about* the bed, and none by *observed behaviour of* the bed.

The bed's own strongest claim — a fresh agent resolves frame, risk, probe and one next action
in thirty seconds — has **never been measured**. Until it is, every amendment is speculative.

**This session measures. It does not amend.** Amendments are the *next* session, and they are
authored only against probe findings. That ordering is the point of the gate.

---

## prompt-0 — @Houston (master seat)

You own this session. You are the sole writer of `STATUS.md`.

**Read, in order, then stop and write STATUS before acting:**

1. `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md`
2. `/home/hruzam/reposoma/raw.guides/status/GUIDE.md`
3. `/home/hruzam/reposoma/raw.guides/PAD/GUIDE.md`
4. `/home/hruzam/reposoma/raw.guides/bus/GUIDE.md`
5. The synthesis: `raw.session-routines-and-file-plane.2026-09-03.md` — **Part 5 and OPEN only.**
   Do not read Parts 1–4 unless a probe finding sends you there. They are field weather and
   will bias the probe design toward the audit's conclusions.

**Your work, in order:**

**(a) Select the subject session.** A *live* session in this project with a populated
`RUNBOOK.md` and `STATUS.md`. Not this one. Not a session you have worked in. Record the
absolute path in `STATUS.md` as `checkpoint:`.

**(b) Author the probe as a PAD.** `pad.1-cold-resume.md`, per the PAD GUIDE. It is run by a
human against a genuinely fresh agent with **no session context** — a new invocation given
only the portable entry point and the subject session's folder. Each step is one instruction
with branch verdicts; the operator pastes raw output into the fence beneath.

The probe scores six things, and **time-to-answer is recorded for each**:

| # | scored | SUPPORTED when |
|---|---|---|
| 1 | frame | resolves correct repo, host, branch, HEAD, dirty paths without being told |
| 2 | probe | selects and runs the stated recovery probe, read-only, and interprets both outcomes |
| 3 | classification | distinguishes *never started* from *partially ran* on the in-flight action |
| 4 | holds | states **every** live hold. One omitted hold = REFUTED, regardless of the rest |
| 5 | next | takes exactly one action, matching `next:`, and names its `expected:` |
| 6 | total | all of the above inside thirty seconds |

**Do not help the fresh agent.** A probe the operator rescues measures nothing. Where it
stalls, record *where* — the stall location is the finding.

**(c) Hand to @Janus** via `_bus/01.houston.point.md` before scoring. See prompt-1.

**(d) Score and promote.** After Janus's verdict, write the scored record to the project's
evidence home and point `checkpoint:` at it. That promotion closes the gate.

**You may not** amend any guide in this session. Findings are recorded as findings. If a
finding is severe enough to demand immediate amendment, write it into `STATUS.md` under
`holds:` and raise it to @majkee — do not fix it.

---

## prompt-1 — @Janus (challenger seat)

You do not run the probe. You attack its design **before** it runs, and its scoring after.

**Read:** `/home/hruzam/reposoma/raw.guides/PAD/GUIDE.md`, the POINT you receive, and the
drafted `pad.1-cold-resume.md`. Nothing else.

**Before the run** — answer in `_bus/01.janus.return.md`, six fields per the BUS GUIDE:

- Which steps would pass on a **bad** bed? A probe that cannot fail is theatre.
- Where does the PAD **leak the answer** to the agent it tests?
- Is any step's success condition a *presence check* rather than a *mechanism check*? The bed's
  own law: a marker file can exist while the thing behind it is dead.
- Does the thirty-second bound measure the bed, or the operator's typing speed?

**After the run** — write the VERDICT. The RETURN is claims, not evidence: resolve every cited
path, read the raw fences yourself, and mark anything you cannot check `UNVERIFIED`. Record
curvature: where the guides' description and the observed behaviour disagree, **name the
disagreement rather than the tidier side.**

One adversarial pass. Push once per fork, clearly. If @Houston holds the line, defer and
record the disagreement in the verdict rather than re-litigating.

---

## prompt-2 — @majkee (human seat — hands required)

The probe cannot run without you. You are the one who opens a genuinely fresh agent, pastes
each step, and pastes raw output back into the PAD fence. Do not summarise the output; the
PAD is its own raw receipt.

**Run it twice: once on office, once on home.** The second run is not a repeat — it is the
only test of the mirroring law (see holds). Both runs go in the same PAD, with the host named
in the header of each sitting.

You hold the gavel on: whether a finding becomes an amendment, and whether the session closes.

---

## Known constraints and destructive holds

Fixed at authoring time. Constraints discovered mid-session go to `STATUS.md` under `holds:`.

- **`status_owner: @Houston` — single writer.** Other seats write returns, verdicts, evidence.
  They do **not** replace `STATUS.md`. Ownership transfer is itself a verified transition.
  *Cause: no revision, lock, or compare-and-swap exists under the state file. Two honest
  writers can both read revision A and lose one truth while obeying every written law. The
  serialized-operator assumption is what currently holds; this hold makes it explicit rather
  than accidental.*
- **1:1 folder placement across both hosts is a LAW of this bed, and this session is its first
  real test.** Every absolute path in every prompt depends on it silently. If any path
  resolves on one host and not the other, **stop and record it** — that is a finding about the
  bed, not an obstacle to work around. Do not patch it with a relative path mid-run.
- **No guide is amended in this session.** Not one line. The gate is measurement.
- **No tooling is built.** No validator, no revision command, no installer. Brakes stand.
- **Do not run the probe against a session you need.** Assume the fresh agent may take a wrong
  action. Choose a subject whose worst case is a discarded branch.
- **Host provenance is recorded per sitting, not in STATUS.** STATUS is a replacement snapshot
  and erases its own host on every rewrite; it cannot carry provenance by construction.

---

## references

Point, do not copy.

- `/home/hruzam/reposoma/raw.guides/{runbook,status,PAD,bus}/GUIDE.md` — the laws under test
- `raw.session-routines-and-file-plane.2026-09-03.md` — Part 5 (what is ahead) and OPEN
- `brief-r2.guides-audit.2026-09-03.md` + its reply — the twelve remedies. **Reference only.**
  Nothing here adopts them; this session decides which ones the evidence justifies.

---

## What closes this gate

The scored probe record exists in the evidence home, covering both hosts, with a time and a
verdict per criterion, and `checkpoint:` points at it.

**Not** a passing score. A *recorded* score. A failed probe closes this gate exactly as well
as a passing one — and is worth more, because the next session's amendments will be anchored
to something observed.

On closure: promote the scored record and the PAD (it *is* the evidence artifact here, so it
survives), remove the session from `pulse.md`'s router line, prune the directory.

---

## What this session deliberately does not do

Named so the next seat does not read the omissions as oversights:

- No revision field, lock, or atomic-write tool. Not until two seats actually collide.
- No portable bootstrap for a second human. No second human is imminent.
- No adoption of the audited remedies. Their premise is prose; this gate produces evidence.
- No program-level file above the numbered siblings. Parked until one program closes and its
  post-mortem says what was re-derived.
- No amendment of the gate-copy drift finding, the host-provenance gap, or the unstated
  mirroring law. All three are recorded in the synthesis; the probe may sharpen or kill them.
