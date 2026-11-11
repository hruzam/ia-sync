---
title: Stream continuity, memory/cache and programmable decisions
author: cartan
date: 2026-11-03
status: operator terminology correction plus design advice; no implementation release
---

to-cartan(jev-01) from-majkee ---

5. where I can set Jev channell. And sorry now I remeber : channel was intended as stream line (just for continuity because CLIs itself, Jev does not care.)

---

to-majkee(jev-01) from-cartan ---

1. **Meaning corrected:** channel is the local continuity stream; iterations are entries
   within it. The earlier channel/profile question and the interim channel/single-iteration
   interpretation are superseded as current interpretations. Accepted engagement/session/
   cumulative-allowance scope remains unchanged. Stream count and exact storage schema have
   not been gaveled.
2. **Proposed pilot shape:** one named stream, initially `main`, inside the engagement's
   durable session. Select it explicitly in the local CLI, record its stable identity and
   readable name in opening/binding records, and display it with effective settings. Carry
   its ID on iterations, references and dispositions. Several CLIs may select the same
   stream. A different CLI conversation does not itself create a new stream or allowance.
   Later multiple streams can share the engagement ledger and spending authority. No command
   exists today: any `--channel`/`--session` syntax shown is an interface sketch.
3. **Useful small memory:** keep a bounded, versioned stream note containing current purpose,
   operator decisions, unresolved questions and selected prior observations, each with source
   references. It is a derived reading aid; the durable event record remains authoritative.
   Human/head authorship is explicit. A prepared request freezes the selected note version
   and excerpts actually sent. Old model advice is labelled as advice; no automatic promotion
   to fact or global rule. This is explicit context, not model training or hidden persistence.
4. **Cache is distinct:** local show/ref already reuses saved replies. Optional exact-response
   reuse could later match complete frozen request context, rubric/adapter/validator and
   pinned model/provider policy, with an explicit freshness policy. A hit records the source
   occurrence and age and makes no new inference claim. Changed input, unpinned/drifted model,
   invalid/unknown result, expired relevance or a request for a fresh sample bypasses it.
   Identical replies on two trials cannot prove determinism. The predecessor Flight map
   section 8.7 made that stronger inference; do not inherit it. Reuse is an explicit policy
   choice even for a nondeterministic model. Automatic semantic caching, a vector service
   and self-updating memory have no demonstrated need in this pilot.
5. **Jev as IF:** code may consume validated Noul/Choice/Score output as a bounded decision.
   A Noul wrapper should expose YES/NO/UNCERTAIN under versioned, empirically checked thresholds;
   invalid replies, timeout and unknown transport remain separate errors. A confidence value
   is not permission and is not necessarily a probability of correctness. The approved code
   owns branches, action allow-lists, loop limits, cost/time budgets and logs. The current pilot
   can demonstrate the chosen branch without taking external action; later automatic calls
   and action execution need their own released policy and proof. No new action dispatcher,
   background watcher or automatic spend is authorized here.
6. **Complexity:** the same small callable judgment interface can support conditionals,
   classifications, weighted scores, bounded sequences or state machines. Build the concrete
   workflow in ordinary code first; introduce a generic workflow framework only if repeated
   workflows actually need it. Keep known deterministic predicates in code; use Jev for the
   semantic judgment that cannot already be calculated directly.
7. **Documentation:** Houston's read-only native consult is preserved verbatim in
   `consult.documentation.2026-11-03.md`; parent checked its sources and requested a narrow
   clarification about the explicitly permitted project-owned guide/published-mirror route.
   That returned clarification is preserved verbatim in
   `consult.documentation-clarification.2026-11-03.md`: both ownership routes are lawful;
   choose one editable source. A direct machine-workflow guide in reposoma is the current
   recommendation; ia-sync retains engine-authoring architecture and exact reference.
   Placement recommendation is not guide promotion. The active draft should ultimately
   consolidate these clarifications into one design body, preserving earlier dated evidence.

---

## Evidence and limits

- Operator's latest message supplies the stream meaning and authorizes Houston consultation.
- Current pilot RUNBOOK and decision-01 receipt preserve existing authority and funding scope.
- Parent inspected Houston's actual identity/binding/project/card stamp values and the cited
  Guide-writing law, A3 S03–S04 and Germline-forge stale warning. This corroborates document
  contents; it is not an audit of the child's complete loader trace or runtime behavior.
- [TypeSafe confidence](https://docs.typesafe.ai/confidence),
  [intent routing](https://docs.typesafe.ai/patterns/intent-routing) and
  [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring), read publicly
  2026-11-03. These demonstrate intended composition patterns, not our implementation,
  threshold calibration or operational acceptance.
- No Jev implementation, live runtime store or dedicated global Jev guide exists at this check.
