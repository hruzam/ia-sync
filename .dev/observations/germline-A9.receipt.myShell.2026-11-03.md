<!-- Origin: .dev/session/germline-A9-reader-economy/RESULT.md; preserved: .dev/records/germline/2026-11-03/germline-A9-reader-economy/RESULT.md; sha256: 2274e6e83af2d0e81e24a37038dfbc438b0752b73da3eac822394da6161683b8; preservation commit: pending (local-only); promoter: myShell. Original body follows verbatim. Relative links in that body use its original directory; use the preserved source/legacy alias for navigation. -->

> **2026-11-03 adjudication:** The [scoring addendum](raw/SCORING-ADDENDUM.md) revises reader-01 from 6/8 to 7/8 and reader-03 from 7/8 to 8/8 under the RUNBOOK's meaning-based interpretation. Reader-03 was not supplied the summary's contrary claim; an explicit-comparison interpretation conflicts with the declared four-source minimum. Identity therefore has a qualified 8/8 versus 8/8 semantic comparison and 48.8% lower stored D, but 23.9% higher E; outside reads and manually transcribed payload carriage remain unverified. No clean unqualified economy result is established. The figures and wording below are the original report and are retained for provenance; `SCORES.json`, `METRICS.json` and `analyze.py` still reproduce that original scoring. The original 103-protected-hash statement below describes the earlier final check; the addendum records the later A3 checklist index change. Operator acceptance remains pending.

# A9 reader economy — mixed results, no clean maintained-correctness pair

2026-11-03 · Cartan / Codex · experiment work complete; Majkee's acceptance remains pending.

In this bounded message-mediated pilot, none of the three pairs establishes reduced delivered material at maintained correctness. Selective readers were sent fewer UTF-8 bytes in all cases, but each selective answer missed at least one frozen criterion. Two selective paths also accumulated more visible-history exposure than full reading. The third stopped before receiving any documents and gave an incomplete answer, so its lower byte counts do not demonstrate successful economy.

| Case | Full score | Selective score | Full / selective D bytes | D reduction | Full / selective E proxy bytes | E reduction |
|---|---:|---:|---:|---:|---:|---:|
| Readiness | 6/8 | 0/8 | 8,102 / 4,113 | 49.2% | 8,102 / 9,628 | −18.8% |
| Review identity | 8/8 | 7/8 | 7,938 / 4,061 | 48.8% | 7,938 / 9,836 | −23.9% |
| Interrupted operation | 8/8 | 0/8 | 7,942 / 2,144 | 73.0% | 7,942 / 2,144 | 73.0% |

The negative E reductions indicate increased exposure under the retained-visible-history assumption. D includes the stored task, index, instructions and each document delivery; E sums visible input and prior output available before each admitted response, assuming the native conversation retains that history. Neither measure is backend token usage, billing or monetary cost. Payloads were manually transcribed into native calls; frozen stored payload and serving hashes were checked, but the actual tool-call bytes were not independently extracted for byte-for-byte verification. Consequently these numbers are reproducible from the preserved records, with that carriage qualification. Actual usage, cost and invisible state are unknown.

Reader-01 omitted the proposal-only limit and explicit comparison with the inherited summary. Reader-02 selected three necessary documents and one distractor, then answered early without reading the inventory and without citations; the frozen rubric requires citations for each factual item, hence 0/8 rather than a claim that every statement was substantively wrong. Reader-03 retrieved all four necessary sources and cited them but did not compare the inherited summary, giving 7/8. Reader-04 supplied the comparison and scored 8/8. Reader-05 supplied the recovery evidence and scored 8/8. Reader-06 returned an early `ANSWER` asking for documents and supplied no evidence-based decision; the fixed protocol ends a run on ANSWER, so no corrective delivery followed.

Reader-03 disclosed reading the host journal, sync discipline and protocole file outside the task source set. Required runtime initialization was allowed, but the status and effects of these reads are not independently established; the pair is qualified. Other readers self-reported no outside reads, which is not an independent trace. Readers 01, 04 and 05 gave terminal answers without a literal `ANSWER` marker; whether that violates the formatting convention is qualified. No hidden harness instructions, effective model/effort, or complete tool traces are independently visible. The roster requested six fresh Luna/low default-role subjects with no parent history; requested settings are not proof of effective backend settings. Message boundaries were enforced by instruction, not filesystem isolation.

Six spawns and ten admitted response turns were spent; the limits were six and fifteen. There were no replacements, feedback turns, or reruns. Scoring is Cartan's judgment against the frozen rubric, not an independent scoring study. Preparation and manual dispatch/scoring are real overhead, but their token usage is not exposed. This small sample does not establish general noninferiority, model ranking, production readiness, end-to-end savings, or the benefit of a crawler.

## Bounded return to A3

- **S02:** require explicit source selection, authority and citations, and make early termination and incomplete-evidence behavior unambiguous. A correct direction without grounded claims did not meet this pilot's frozen scoring standard.
- **S07:** retain A5's qualified navigation baseline alongside this mixed A9 comparison. This experiment adds no clean maintained-correctness economy result.
- **S08:** repeated conversation history can reverse the delivered-input advantage. Any design choice should distinguish D from E and from measured backend usage; do not infer a parser, cache or central architecture from these observations.

## Evidence and custody

- [Scores](raw/SCORES.json), [metrics](raw/METRICS.json) and [checks](raw/CHECKS.json); the reproducible calculation is [analyze.py](raw/analyze.py).
- [Dispatch ledger](raw/DISPATCH.json), `raw/runs/reader-01` through `reader-06`, and `_bus/` preserve admissions, visible returns and head-landed exchange records.
- [Freeze](raw/FREEZE.json), [preflight](raw/PREFLIGHT.md), [protected hashes](raw/PROTECTED.json), and [continuity receipt](raw/CONTINUITY-RECEIPT.md) preserve scope and limitations.

All 57 frozen hashes and 103 protected hashes matched at final check. A3/A4/A5, runtime, pulse and journal were preserved. No deployment, publication, commit, push, canon change or A3 state advance was performed. This bed remains local pending the operator's disposition and custody decision.
