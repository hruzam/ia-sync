# A9 scoring addendum — semantic adjudication, 2026-11-03

Cartan · record review requested by Majkee through Oraculum's approved handoff. This is a correction to Cartan's interpretation of two existing responses, not independent scoring or operator acceptance. Original [SCORES.json](SCORES.json), [METRICS.json](METRICS.json), frozen rubric, prompts, fixtures and transcripts remain unchanged. The original scores remain the historical output of the initial scorer; the adjudicated scores below govern this addendum's interpretation. `analyze.py` still reproduces the original scores and original paired flags, not this addendum.

## Reader-01 — readiness

Original **6/8**; adjudicated **7/8**. Item 5 in the frozen rubric reads “Current rule supersedes inherited summary.” The [full prompt](messages/reader-01.txt) supplied both `readiness/acceptance-rule.md` and the inherited summary. The rule explicitly makes designated-owner acceptance necessary, rejects author assent as sufficient, and supersedes the contrary summary. The [answer](runs/reader-01/transcript.jsonl) says “The current rule requires that owner’s acceptance; the author’s assent does not suffice” and cites `readiness/acceptance-rule.md` among the supporting paths. That applies the operative position in direct opposition to the summary's claim. It does not explicitly name the summary or affirm awareness of its supersession, but the RUNBOOK says to score meaning rather than preferred wording. I restore the point for correctly applying and citing the current rule; the prior deduction demanded an explicit comparison not specified to the reader.

This is a scoring-interpretation error, not evidence that reader-01 recognized the summary conflict. The separate proposal-only criterion remains failed: the response does not say the output is only a proposal. Thus this full-reading baseline remains below 8/8. Reader-02 remains **0/8** under the unchanged citation-grounded scoring, with some substantively correct statements but no cited paths and no inventory read.

## Reader-03 — review identity

Original **7/8**; adjudicated **8/8** under the meaning-based reading of item 6, “Gate unsatisfied despite inherited summary.” The [initial task and index](messages/reader-03.txt) asked whether the current review gate passes and listed an inherited-summary path but did not disclose its assertion. The [two delivered messages](runs/reader-03/delivery-1.txt) and [second delivery](runs/reader-03/delivery-2.txt) supplied the four frozen necessary sources: registry, R4 policy, ledger and binding. The binding selects R4 and refers generally to older summaries, but does not state the summary's actual claim. The fifth document, `identity/summary.md`, which states that two ledger entries suffice, was not delivered to reader-03. Full reader-04 did receive it.

The [reader-03 answer](runs/reader-03/transcript.jsonl) cites all four delivered sources, identifies two handles as one person, applies the two-distinct-people rule, concludes the gate is unsatisfied, and calls for another distinct approval. That is the correct grounded gate decision. I restore the point when the criterion is interpreted as applying the current gate correctly despite the existence of a contrary summary. The response does **not** demonstrate awareness of, or rebut, the undisclosed summary claim.

The frozen criterion is ambiguous: if it requires an explicit comparison with the summary's *specific* contrary claim, that fact requires a fifth source absent from the declared four-source minimum and was not in the task or the four delivered bodies. In that stricter interpretation, the score remains 7/8, but the failure to perform that comparison cannot fairly be attributed to reader-03's reasoning from its supplied minimum. This is a fixture/minimum-evidence and rubric-interpretation inconsistency, not a post-hoc change to the frozen fixture or a new scored criterion. No correction or additional call is warranted.

## Effect on paired conclusions

| Case | Original full / selective | Adjudicated full / selective | Effect |
|---|---:|---:|---|
| Readiness | 6/8 / 0/8 | 7/8 / 0/8 | Full baseline and selective answer still fail the frozen full-success standard. |
| Review identity | 8/8 / 7/8 | 8/8 / 8/8 | Under the meaning-based interpretation, both answers satisfy all items; lower delivered input is a **qualified semantic** observation, not a clean protocol-qualified pair. |
| Interrupted operation | 8/8 / 0/8 | 8/8 / 0/8 | Unchanged; selective reader stopped without documents. |

For identity, stored D is 7,938 full versus 4,061 selective bytes, a 48.8% reduction; the E proxy is 7,938 versus 9,836 bytes, an increase of 23.9%. Reader-03 disclosed outside reads whose required-initialization status and effect are unverified. Native payload bytes were manually transcribed and not independently captured. Consequently the fixed rule requiring valid, unqualified protocol conditions does not support a clean maintained-correctness economy claim; even under the revised semantic score, the lower D is accompanied by a higher E proxy. The stricter summary-aware interpretation remains a documented alternative rather than evidence of a substantive reader failure. No token, billing, general noninferiority, monetary-saving or production-readiness conclusion follows.

## Integrity and custody

At this review, all 57 hashes in [FREEZE.json](FREEZE.json) matched. Before this edit, the original SCORES SHA-256 was `b976823d792649576fa8ecb900e1b589065f61d3b1911bb5182041e4ebec37a5`, METRICS was `d346d1096b774c5779cead105347f09ec8d81b09b00178b33bdd2097363bde31`, and RESULT was `c67952b1cf08982a397aef62504d4ef7a264940ad7fef050ea4d10298b4e0fda`, matching Oraculum's intake. Of the 103 pre-experiment protected hashes, the A3 CHECKLIST now differs: its visible diff includes the later combined-evaluation index entry, as the handoff records. The other 102 still match. The original RESULT's preservation statement describes its earlier final check, not the present state. This review does not change A3 or claim current equality of all 103.

Acceptance of A4/A5/A9 and evidence preservation remain with Majkee and the respective owners. No new subjects, reruns, external publication, A3 state change or canon decision occurred.
