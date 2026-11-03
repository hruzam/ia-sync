---
point: Flight → myShell / open distribution
date: 2026-10-20
session: germline-05-sella-germline-audit
pen: flight · integration of oraculum umbrella assessment (prompt-3 dispatch)
oraculum_return: verbatim below, sections 1–6
flight_notes: integrated corrections and flags appended after §6
audience: Majkee · myShell (machine seat)
status: POINT — no verdict yet; investigation sequence proposed; awaits Majkee direction
---

# Umbrella assessment — Nablarva · Composer · germline programs · Sella

*Oraculum return, verbatim and attributed. Flight corrections appended at end.*

---

## 1. Component map

**Nablarva** — the agent-communication project (`~/unikuklatrix/nablarva/`). Owns session beds (composer-01-parse, X1), the project flag locks (L8′ routes composer publication to/through ia-sync; L16 said/inferred/locked), its own `.germline/` project addendum, Ovitmugen/Termbrana. Supplies Sella with its [S5] conforming-application precedent and supplies the audit with the Composer reference case and the Sella-v.0.1 *personal proposals* (brief §Source map: "design proposal, not the Sella GUIDE"). Runtime consumer of global germline: Houston loads identity → binding → Nablarva addendum → card at entry (Q1 F1, journal 2026-10-17).

**Composer** — Phase 0 grammar only (v3), Cartan holds the STATUS pen. Owns the delimiter-body contract, flat string header, deterministic diagnostics. Supplies a wire shape `request/0.1` whose header *declares* `program`/`function` names; v3 §5 "resolution deferred", §2 "Do not open references, resolve bindings or execute". Authoring surface is zsh/CLI; nothing is runtime — no parser, loader or writer exists. Publication target proposed at `~/ia-sync/zsh/composer/` (v3 preamble).

**Germline programs** — three distinct surfaces (brief :68–73; README :14):
- (a) global source `~/ia-sync/germline/` → deployed `~/.germline/` — agent identities, bindings, cards, skills, stamped and runtime-loaded;
- (b) personal `.majkee/.germline/programs/<p>/CONTROLLER.md + fn/<f>.md` — manual procedure, stamp table, "uncanonical; no deploy";
- (c) `<project>/.germline/` addendum.

Only (b) is a *program* in the CONTROLLER/function sense. CONTEXT §2A: stamp is "a checked marker in this manual procedure, not runtime enforcement." Mechanism, not doctrine.

**Sella** — doctrine for building Claude Code primitives (agent/skill/hook): the authority stack (§1), source model (§2), nine laws, three walks, conforming application (§5). DRAFT, G3-HELD, verified 2026-09-01, half-life 42 days. Owns "is this primitive well-made"; disclaims session shape (§Boundary). Points to germline-forge as its promotion procedure (§5.4).

---

## 2. Established mechanisms

- Runtime-load with per-file stamps regenerated on edit — README :8–11; observed in journal 2026-10-17 (Q1 F1).
- CONTROLLER table binds name/path/stamp; mismatch halts, no guessed replacement — CONTEXT §2A; CONTROLLER :54–55.
- `ctrl <program>&<function> : <task>` is prompt syntax, one pair per prompt; `&` is not shell — CONTEXT §2A.
- Composer declares, never resolves; `&&` has no Phase 0 action — v3 §2, §5, §10.4.
- Composer resolution route is "existing controller tables" — CONTEXT §9; FOR-NABLA.oraculum :10–11. Proposed, not built.
- Sella/session-shape seam: built under Sella, run under the canon — Sella §Boundary.
- Sella → germline-forge → README doctrine chain — Sella §5.4; germline-forge :13 (via Q1).

---

## 3. Actual conflicts

**C1 — v3 mandatory single `program`/`function` vs body composition.**
v3 §5 lists both as required scalars; §8 step 4 emits `required_absent`; §7 examples and §9 header negatives assume one pair. Majkee's clarification (RUNBOOK fixed constraint) composes several in the body. Lineage: v3 inherited the one-pair model from the `ctrl a&b` convention. Affected clauses: §5 table + absent-order sentence, §7 examples, §8.4, §9 "header" row. **Owner: Cartan.**

**C2 — Sella L1/L7 vs germline runtime-load (Q1 misclassified).**
Sella L1: identity declarations → kernel; L7: only the kernel survives inattention; §2: an agent body "loads ONLY as the spawned agent's own system prompt". Germline wrappers "carry only a loader" and identity arrives via file reads — i.e. userland. Q1 F1 calls this SUPPORTS by mapping it to Sella's *skill* two-phase model; but germline applies the skill mechanism to agent *identity*, which Sella places above the boundary. Sella's paging row (§1) covers skill bodies and CLAUDE.md re-injection, not tool-read files — compaction survival of a runtime-loaded identity is unspecified. **This is a real tension, not an extension.**

**C3 — Stale doctrine hop.**
Sella §5.4 points to germline-forge (2026-10-07) whose §0–§3 are superseded by the 2026-10-10 fold (:13). Sella's half-life expired 2026-10-13; its §2 key tables (`context: fork`, which Q1 F2 leans on) are weather by its own L8.

**C4 — Vocabulary.**
Sella §6: program = subagent, method = skill. Germline: program = CONTROLLER + functions. Composer `program:` uses the germline sense. Q1 uses "program" in both senses without flagging; a germline *function* is closest to a Sella *method body*, and a CONTROLLER is a userland re-implementation of Sella's kernel router.

*(C5 — Q1 D1 internal inconsistency: resolved by Flight before this file was written. D1 withdrawn.)*

---

## 4. Unresolved questions

Brief's preserved opens (from Q1):
- Q-A (brief Q1/Q2): stamp proves addressing, not correct interpretation — preserved
- Q-B (brief Q3): `from` as declared string, no scope grant — preserved

**Brief Q4 and Q5 were dropped from Q1's open list — restored here:**
- Q4: editor body-tags vs declared block grammar — mismatch between Sublime §Changed and v3 opaque body rule (brief :113-117)
- Q5: publication home/duties — exact code home, stack, verifier, distinct duty separation (brief :118-122)

New (Oraculum):
- N1: which germline surface is the actual audit object (three surfaces; Q1 mostly reads (b))
- N2: compaction behaviour of runtime-loaded identity (blocks C2 resolution)
- N3: if a germline function is outside Sella's primitive set, Sella has no law for it — reconcile or extend?
- N4: under body composition, does the CONTROLLER table become the registry the brief forbids?
- N5: Composer `&&` vs program `&` notation lineage

---

## 5. Investigation sequence

1. **Pin the object** — reader (zenith-tier): list the three germline surfaces from README :14, brief :68–73 and the two program directories; return a table of what each holds. Blocks everything else.
2. **Re-test C2** — field_sella: Sella §1 stack + paging row, L1, L7, §2 body sentence, plus [S3] §2/§6 in both July and September versions; question: where does a tool-read identity sit and what survives compaction.
3. **Program pilot evidence** — field_germline: find one recorded `ctrl journal-continuity&…` invocation with stamp check in the journals. Q1's only practice evidence is an *agent-identity* load, not a program load.
4. **Package C1** — field: extract affected v3 clauses and draft acceptance cases; Flight POINTs to Cartan (RUNBOOK prompt-2).
5. **Janus** before reversing Q1 F1's SUPPORTS verdict (consequential gate).
6. Only then: Majkee decisions on Q4/Q5 scope and N3.

---

## 6. Missing prerequisites

- Sella source identity never frozen (brief :36–37 required it; Q1 records "full" with no hash/revision).
- Sella past half-life (expired 2026-10-13); §2 tables unverified against the current claude version (germline-forge cites 2.1.292).
- No read of the actual Houston wrapper to confirm what sits in the kernel; README text stands in for mechanism.
- No observed program-layer pilot (Sella L8: trust is a dated pilot, not a clean diff).
- Q4/Q5 dropped from Q1's open list (now restored in this file and in findings.q1.md).

---

## Flight integration notes

**What Q1 got right:** mechanisms confirmed — runtime-load sequence, stamp-gate, CONTROLLER table, BUS return shape, per-function authority declarations, recovery hold. These findings are supported by multiple source passages and practice evidence. The [S3] supplement adds §5d staleness table (authoring trap: `allowed-tools` vs `tools` key split) and §7 `omitClaudeMd` exception.

**What Q1 needs correction or flags:**
- F1 SUPPORTS verdict: flagged as potentially wrong by C2. Must be re-tested before settled. The classification holds provisionally; it is not available as a basis for implementation guidance until C2 is resolved.
- Vocabulary (C4): Q1 uses "program" in both Sella (= subagent) and germline (= CONTROLLER+functions) senses. Any statement in Q1 about "programs" should be read against this ambiguity.
- C3 (stale doctrine hop): Sella's own half-life expired before this audit ran. The RUNBOOK's read bounds ("check the present source rather than treating dated vendor facts as current") apply here. Q1 read Sella carefully against its own caveats; this is noted rather than acted on without Majkee direction.

**Decisions this assessment surfaces for Majkee:**
- D2 (from Q1) — brief Q1/Q2/Q3 open questions: investigate further or note-and-park?
- D3 (from Q1) — three remaining journal-continuity functions: in scope?
- D4 (from Q1) — invariance-autonomy master brief: in scope?
- D5 (new) — which germline surface is the audit's primary object? N1 must be pinned before investigation sequence runs.
- D6 (new) — authorize step 1 of investigation sequence (pin the object), or revise the sequence?
- D7 (new) — C1 package to Cartan: authorize Flight to prepare the POINT?

**myShell / Cartan:** C1 is addressed to Cartan. The affected v3 clauses are §5 (required scalars table + absent-order sentence), §7 (examples), §8.4 (required_absent emit), §9 ("header" row). When authorized, Flight will prepare a POINT to Cartan under this bed's `_bus/` with the affected clauses and proposed acceptance cases. No v3 edit from Flight.
