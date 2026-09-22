# RUNBOOK: voice-meetings-01-threshold

```yaml
goal: >
  Know, with evidence on disk, how well each vendor's chatbot voice regime (Claude voice ·
  ChatGPT voice) holds situated reasoning at threshold — the entry bar a voice must clear
  before it is seated in a two-voice meeting. This is loop 1 of a long-run watch; the watch
  continues in numbered siblings, never by widening this gate.
gate: >
  Each test in the fixed battery (paprika · blackout) has been run once as its SINGLE-agent
  version against each vendor voice (claude-voice · gpt-voice) with a run record on disk, and a
  VERDICT per test×vendor scores its three checkpoints clear / assisted / miss — four VERDICT
  files exist in loops/.
participant_1: [majkee, {brand: human, model: n/a, effort: n/a}, host: office + home + phone, role: chair — runs each loop by voice; relays verbatim; drops the RETURN; gavels]
participant_2: [claude-voice, {brand: anthropic, model: claude-opus-5 (operator's choice — record the exact version per loop), effort: n/a}, host: chatbot app, instrument: relay, role: voice under test — NABLA or SYMMETRY persona + participants.md]
participant_3: [gpt-voice, {brand: openai, model: gpt-6-astra (operator's choice — record the exact version per loop), effort: n/a}, host: chatbot app, instrument: relay, role: voice under test — WAVE or ASYMMETRY persona + participants.md]
participant_4: [scribe, {brand: openai (host app), model: as gpt-voice, effort: n/a}, host: chatbot app with the longest voice session, instrument: relay, role: OPTIONAL silent recorder — Ptyra REGIME B + scribe.md; not required for single-voice loops]
participant_5: [atlas-ui, {brand: anthropic, model: sonnet, effort: medium}, host: office, role: evaluator — scores each RETURN into a VERDICT; rewrites STATUS; folds toward the meeting GUIDE]
status_owner: atlas-ui
```

## Why this session exists

Meetings ran once (v1) and the protocol reached v3 on *external* evidence (Epoch, mirror) — but zero
of our own results exist, and the v1 debriefs were self-report. Before any two-voice scenario we
need a cheap, checkable entry bar per voice, or every meeting result carries the confound "could
this voice even reason at threshold?" This session produces that bar's first four data points. It
is deliberately loose in pace (a long-run watch) and strict in record (one file group per loop).

## Fixed facts

- **Living home — NOT this bed, never pruned:** `/home/hruzam/ia-sync/.dev/session/voice-meetings/`
  — briefings `res/participants.md` · `res/scribe.md`, addendum `raw/meeting-addendum.template.md`,
  tests `test/logic-test-paprika.md` · `test/logic-test-blackout.md`, `meeting-themes/`, v1 debriefs.
- **Test loops replace `_bus/`** (operator's call: "tests instead bus" — bus wording kept as notation
  only). Per loop, one file group in
  `/home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/`:
  - the POINT is the test design itself (pointed, never copied) + the loop header (test × vendor);
  - `NN.<test>.<vendor>.return.md` — the run record, single writer: **majkee**;
  - `NN.<test>.<vendor>.verdict.md` — the evaluation, single writer: **atlas-ui**.
  Four loops: `01 paprika×claude` · `02 paprika×gpt` · `03 blackout×claude` · `04 blackout×gpt`.
  Order is free.
- **RETURN (run record) fields:** test · vendor · persona · exact model/version · date · chair ·
  context pack given (must be: `participants.md` + the live narrative, nothing else) · transcript
  (paste or absolute path) · scribe log (if seated) · examiner leaks (any prompt from the test's
  forbidden list that was spoken — verbatim, or `none`) · chair notes · uncertainty (`none` is
  valid; silence is not).
- **VERDICT fields:** loop · test · vendor · verified_by (seat · date · host) · checkpoints a/b/c
  each `clear | assisted | miss` + the transcript line that proves it · disposition
  `CLEAR | BELOW | ASSISTED` · curvature (map vs observed; `none` valid) · gate_effect
  (`n/4 verdicts`) · status_rewritten.
- **Checkpoints — fixed for this gate; graduate into the test files afterwards:**
  - **paprika** — (a) normalizes €/package vs €/kg unprompted; (b) discovers *weighing* unprompted
    once the scale exists; (c) names the remaining unresolved condition (promotion eligibility)
    unprompted.
  - **blackout** — (a) asks a *discriminating* question before proposing any fix; (b) localizes to
    the study circuit from hallway-lit + floor-lamp-dark; (c) asks *why* it tripped after the reset
    works, unprompted.
  - **Scoring:** `clear` = all three unprompted · `assisted` = a hint was given (that checkpoint does
    not count) · `miss`. Disposition `CLEAR` only when all three are clear.
- **`relay` here** = the human chair carries verbatim in/out between chatbot voice apps; no tunnel,
  no stored thread in this bed. The instrument is fixed for the session
  (`raw.guides/runbook/res/cross-vendor-seat.md`).
- **Threshold runs are the tests' SINGLE-agent version.** Two-agent meetings are a later sibling.

## prompt-0 — atlas-ui (evaluator · status_owner)

```text
You are the evaluator and status_owner of session voice-meetings-01-threshold.
Read /home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/RUNBOOK.md, then STATUS.md.
For every /home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/NN.<test>.<vendor>.return.md
that has no matching NN.<test>.<vendor>.verdict.md:
  1. read the RETURN and its transcript; read the test design it points to
     (/home/hruzam/ia-sync/.dev/session/voice-meetings/test/logic-test-<test>.md);
  2. score checkpoints a/b/c per RUNBOOK "Fixed facts" — quote the transcript line that proves each;
     any examiner leak listed in the RETURN downgrades the affected checkpoint to assisted;
  3. write NN.<test>.<vendor>.verdict.md with every VERDICT field; name curvature, never smooth it;
  4. rewrite STATUS.md as a bounded snapshot (/home/hruzam/reposoma/raw.guides/status/GUIDE.md):
     checkpoint = the newest verdict, gate_effect n/4, next = the single next loop (or the close)
     naming the seat to wake.
Do not edit the test files, the briefings, or the meeting GUIDE from this session — results
graduate later under majkee's gavel. Do not commit or push; report the paths written.
Done-when: STATUS reflects every RETURN on disk. Return path: STATUS.md + a one-line note to majkee.
```

## prompt-1 — majkee (chair · the sitting)

```text
Run ONE loop (test × vendor), single-agent version — one voice, not a meeting.
1. Load /home/hruzam/ia-sync/.dev/session/voice-meetings/res/participants.md into the voice's
   Project (additive to its persona). Give it NO other context. Scribe optional: if seated, load
   /home/hruzam/ia-sync/.dev/session/voice-meetings/res/scribe.md.
2. Deliver the narrative exactly per the test's "Voice cadence" and "Preserve the narrative space"
   (/home/hruzam/ia-sync/.dev/session/voice-meetings/test/logic-test-<paprika|blackout>.md).
   Volunteer nothing; answer only what is asked. Note any forbidden prompt you let slip — it is
   not a failure of the run, it is data (scores → assisted).
3. Drop the run record:
   /home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/NN.<test>.<vendor>.return.md
   with every RETURN field from RUNBOOK "Fixed facts" (transcript paste or path; exact model version).
4. Wake atlas-ui (prompt-0) on the office carriage of your choice. No commit is needed to proceed;
   commit the bed via @Delta when you want it cross-machine.
```

## Known constraints + destructive holds

- `/home/hruzam/ia-sync/.dev/session/voice-meetings/` is the program's living home, not this
  session's bed — it is **never pruned** on closure; only `voice-meetings-01-threshold/` is prunable.
- The battery is fixed for this gate: paprika + blackout. A new test = a numbered sibling, never a
  widened gate.
- Single-voice runs only; no two-agent scenario in this bed.
- Context parity: both vendors get the identical briefing + narrative; nothing from
  `meeting-themes/` enters a threshold run.
- Never re-run a leaked run silently: a leak is recorded and scored `assisted`; a clean re-run is a
  new numbered loop.
- No edit to the meeting GUIDE (reposoma), the test designs, or the briefings from inside this
  session — graduation is a separate reposoma gavel.
- No `deploy.sh`, no `~/.claude` / `~/.codex` writes — session files are not deploy targets
  (`/home/hruzam/ia-sync/SYNC_DISCIPLINE.md`). Commits to ia-sync: operator or @Delta only.
- Model versions are weather: record the exact version in every RETURN; never assume the RUNBOOK's
  declared model is what actually ran.

## Acceptance evidence

- Four files `/home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/0N.<test>.<vendor>.verdict.md`,
  each with checkpoints a/b/c scored and a disposition, each citing a transcript line per checkpoint.
- `STATUS.md` checkpoint names the fourth verdict and `next:` is the close.

## References

- `/home/hruzam/reposoma/raw.guides/meeting/GUIDE.md` — protocol v3 + the hypotheses this bar protects
- `/home/hruzam/ia-sync/.dev/session/voice-meetings/test/logic-test-paprika.md` · `logic-test-blackout.md` — the two test designs (cadence, forbidden prompts, observables)
- `/home/hruzam/ia-sync/.dev/session/voice-meetings/res/participants.md` · `res/scribe.md` — seat briefings (v3 renderings)
- `/home/hruzam/ia-sync/.dev/session/voice-meetings/raw/meeting-addendum.template.md` — per-instance addendum (for later meeting siblings)
- `/home/hruzam/reposoma/raw.guides/meeting/raw/epoch.brand-strengths-for-performance.2026-09-16.md` — why a threshold exists (hypothesis source)
- **Decision trail** — *what was wrong in v1 · what arrived from Epoch/@mirror · what we do better* — lives durably in `/home/hruzam/reposoma/raw.guides/meeting/GUIDE.md` §Version history + §The primary risk (pushed); the operator-learning layer (the *why*) belongs in `/home/hruzam/ia-sync/.dev/session/GLOSS.voice-meetings.md` per `/home/hruzam/reposoma/raw.guides/gloss/GUIDE.md` — born on need, session ROOT, never this bed
- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` · `status/GUIDE.md` · `bus/GUIDE.md` — the law; bus wording borrowed as notation only
- `/home/hruzam/reposoma/raw.guides/runbook/res/cross-vendor-seat.md` — the instrument tuple (`relay`)
- `/home/hruzam/ia-sync/SYNC_DISCIPLINE.md` — what may and may not deploy from this repo

## What this session deliberately does not do

- Run any two-voice meeting scenario (01–07) — that is sibling `voice-meetings-02-<phase>`, after this gate.
- Reshape the meeting GUIDE into the thin-wrapper / results-built form — a reposoma gavel, informed by these verdicts.
- Rank vendors or pick a "champion" — this is a bar, not a scale; the long-run watch continues in siblings as voice regimes change.
- Add tests, seats, or a scribe requirement mid-flight.
