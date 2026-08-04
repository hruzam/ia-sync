# dev-journal.sella — the Sella line's drop-place + log

## RULES (inner law — this file governs itself)

1. **Two zones:** `HANDOFF` (top) + `LOG` (below). Nothing else.
2. **HANDOFF** holds the *last* handoff only. When the next session consumes it, that
   session overwrites it at its end. Never append handoffs — overwrite.
3. **LOG** is append-only, newest on top. Entries are never edited — superseded by a
   newer entry that names what it supersedes.
4. **Every entry stamps its writer:** `[YYYY-MM-DD · brand/agent · model · host · ref: <source>]`.
5. **Format is markdown** (picked over jsonl 2026-08-03: entries are prose read by humans
   + agents, no machine consumer parses this stream; md when explanation dominates,
   JSON only when a machine validates — Wave's own rule, applied to Wave's own line).
6. This file lives in `_staging/` — git-tracked, deploy-inert. Point, never copy.
   Live files and newer receipts outrank anything logged here.

---

## HANDOFF — last (overwrite when consumed)

`[2026-08-03 · claude/atlas-ui · opus · office · session: atlas.office.paralele-sella-builder]`

**State:** Wave's radio answered. Full chain complete on paper: radio synthesized →
aperture recorded → Epoch receipt landed (`sella.receipt.codex.2026-08-03.md`) →
**ARCHITECTURE CANDIDATE WRITTEN** → `sella.cross-vendor.architecture.candidate.2026-08-04.md`
(A3 provisional winner · all laws classified · L4 flipped to CORE on evidence · ontology
rewritten to five primitive classes · 11-field envelope · gavel block G1–G5).

**Next:** majkee gavels G1–G5 (end of candidate doc) → probes A–E on a Bash seat
(Jacquard pad = Probe B instrument, ready) → only after probes: coder-guide v2 /
CODEX profile v1. NOT written yet, per Wave's own gate: no v2 without probe evidence.

---

## LOG (newest on top · append-only · stamped)

### [2026-08-04 · claude/atlas-ui · opus · office · ref: sella.cross-vendor.architecture.candidate.2026-08-04.md] — architecture candidate delivered

Wave's required output #2 written (point, never copy — read the file). Headlines:
**A3 (thin core + vendor profiles + exchange envelope) provisional winner** — A2 monolith
rejected ON EVIDENCE (Wave's own links went stale in 24h = L8 demonstrated), A1 rejected
because the cross-vendor line is already live and uncontracted. **⚡One flip of Wave's
table:** L4's exit-0/2 pair promoted PROFILE→CORE (Codex documents the identical
convention — convergent micro-ABI, receipt-backed). Ontology (`agents=programs,
skills=methods`) → REWRITE at core into five neutral primitive classes; Unix cognates
retained in the Claude profile only. Envelope: 11 fields + 2 verbs (delegate/consult),
each deletion-tested; 1 field probe-pending. Q6 (Codex self-characterization) NOT
adopted — both of Wave's characterizations ride single-author evidence; Probe A decides.
Dissent preserved: the flip-condition that would return Sella to Claude-only stands live
(probes D/E failing to beat clean baselines). Gavel block G1–G5 at doc end.

### [2026-08-03 · claude/epoch (via atlas-ui) · sonnet · office · ref: sella.receipt.codex.2026-08-03.md] — Codex primary-source receipt landed

Full receipt in the named file — point, never copy. Headlines: (1) AGENTS.md = Codex-native
walk-and-merge chain (~32KiB cap, override file, closest-wins); Claude has NO native
equivalent — `@AGENTS.md` import is the bridge. (2) Custom-agent TOML ≈ closest structural
match to `.claude/agents/*.md`. (3) **Convergent micro-convention confirmed:** hook exit
0/2 semantics IDENTICAL across vendors — Sella L4's "Claude-specific exit semantics"
partly WRONG in the good direction. (4) `codex exec --json` typed JSONL contract has no
Claude-documented equivalent at that fidelity — real asymmetry, keep it. (5) Codex splits
sandbox × approval into two independent axes; Claude bundles one `permissionMode` enum —
do not collapse into one `tools:` metaphor (Wave's point, now evidenced). Surprises: docs
migrated to `developers.openai.com` (Wave's `learn.chatgpt.com` links partly stale) ·
OpenAI's own `/import` page = vendor-authored Claude→Codex mapping table, must be diffed
against Sella, not ignored · Codex does NOT document cross-scope agent precedence (gap —
Sella's L6 precedence axis has no Codex receipt). **Vocabulary verdict (Part C): NO
evidence for ≥30-op fixed vocabulary; survivors are tiny (one filename, exit-code pair,
stdio/JSON shape). Thin-core hypothesis corroborated; atlas position (entry below) holds.**
Note: a harness false-positive fired on `raw.settings` reads (permission-syntax vocabulary
mistaken for injected instructions) — verified benign, nothing acted on.

### [2026-08-03 · claude/atlas-ui · opus · office · ref: majkee Q, voice] — vocabulary question: ≥30-command Sella syntax?

majkee asks: is a specific Sella vocabulary (≥30 commands/functions/operations, in the
spirit of CodeIgniter's `$this->load->model('')`) worth building — or a blind shot, with
the "magic" living elsewhere?

**Position (atlas, pre-Epoch-evidence): blind shot — the magic lives at the boundary, not
in an operation vocabulary.** Reasons: (1) Sella governs the ABI *between* seats; a
30-operation vocabulary is a framework API — exactly Wave's cage territory ("native harness
feature rebuilt as metadata convention," "neutral layer must change whenever a vendor adds
a key"). (2) The stochastic compiler executes *native* primitives (slash commands, tools,
CLI flags) reliably; invented syntax needs enforcement machinery (hooks/parsers) or it is
decoration. (3) What historically survives cross-vendor is *tiny* vocabularies: exit codes,
stdin/stdout, HTTP verbs, the filename `AGENTS.md` itself. Big-vocabulary frameworks bind
you to the framework — vendor-fragile, CodeIgniter included. **Where a small vocabulary
DOES earn its cost:** the Q5 neutral-exchange envelope (~10–15 boundary nouns/verbs: task,
scope, ownership, evidence, delegate vs consult…) — each term must pass the deletion test.
Grow vocabulary like bricks: promoted from repeated use, never born ≥30 at once.
**Status:** position, not verdict — Epoch pass carries the evidence question; final answer
lands in the architecture candidate doc.

### [2026-08-03 · claude/atlas-ui · opus · office · ref: majkee-provided repomix tree, home box] — Wave's aperture: what the Codex architect actually saw

The `repomix.openai-context.md` (home: `~/.majkee/exports/repomix/`) packed this tree —
i.e. Wave's entire *file* view of the Claude/temple side when authoring the radio:

```
.claude/agents/{astrobley,vega}.md · .claude/CLAUDE.md
.config/zsh/ai/{base.zsh,codex-run.zsh}
.config/zsh/guides/{ai.md,codex-relay.contract.md,
  codex-relay.metadata-scripting.2026-07-31.md,guide-for-builder.md,guide-regime-session.md}
reposoma/maintenance/codex-line/runcard.codex-onboarding.2026-07-24.md
reposoma/raw.guides/codex-line.{builder,user}.md
reposoma/temple/decisions/{0001,0002,0005,0006,0012,index}.md
reposoma/temple/{README,roster,system-map}.md
reposoma/AGENTS.md
```

Plus his separate named inputs: sella.coder-guide.md · sella.receipt.epoch-2026-08-02.md ·
sella.observation.atlas-office (below) · ferry.md · _staging/README.md · WAVE.md · the
Jacquard pad.

**Blind spots (weigh his generalizations accordingly):**
- His "Claude side" agent sample = **2 relay seats** (astrobley, vega) whose whole job is
  Bash-dispatch to his own CLI. The other ~28 agents, the entire skills tree,
  settings.json/hooks, ia-sync composer, pulses, `_mail/`, registry — unseen. His
  "file-consuming sensor" characterization of Claude agents rides a biased sample; may
  still be right, but the evidence base is thin.
- His temple picture = the governance slice (0001/0002/0005/0006/0012 + roster/system-map),
  not the operational texture. His CORE/PROFILE/HOUSE classifications need re-checking
  against what he didn't see.
- **No `.codex/` tree in the pack** — his Codex self-knowledge is harness-native, not
  file-evidenced. Both his radio and his Jacquard pad share one author: neither confirms
  the other. Decorrelation must come from my independent receipt (Epoch pass + probes).

Provenance: snapshot stays on home as dated evidence (`captured: 2026-08-03 · authority:
observation · volatile: true`). Live office files outrank it.

### [2026-08-03 · claude/atlas-office (atlas-ui) · opus · office · ref: sella.coder-guide.md + receipt + ferry.md] — conformance observation (migrated verbatim from `sella.observation.atlas-office-2026-08-03.md`, original burned to tombstone)

---
what: atlas-office conformance observation on Sella (the discipline-language) and its
     first program (@ferry) — does the real build meet the philosophy it was bred from
state: OBSERVATION — advisory, not canon; feeds majkee's gavel on sella.coder-guide.md
verified: 2026-08-03 (read: sella.coder-guide.md · sella.receipt.epoch-2026-08-02.md ·
     claude/agents/ferry.md — all on the surgical table this date)
by: atlas-office (primitive creator, office shore)
next:
  - majkee gavel on sella.coder-guide.md (canon is operator-gaveled)
  - resolve FLAG-1 (schema:1) before ferry deploys as the reference program
  - codex-line instructions block (majkee, parallel build) — cross-reference when it lands
  - close the OPEN item (agent-description budget) with one targeted Epoch pass → M→H
---

# Observation — do Sella and @ferry meet the philosophy?

**Verdict: YES — and stronger than expected. Sella is the 2026-08-01 philosophy matured
into a language; @ferry is its first clean conforming program. The rare part: the
adversarial corrections propagated, not just the original claims.**

## 1 · Fidelity — the doctrines survived their own stress test

The load-bearing check is not "did D1/D2 make it in" but "did the *corrected* forms make
it in." They did:

- **L2 (Terse header) = D1′, corrected.** Sella §2 frames `description` as the exported
  symbol and the body as never entering the parent's routing view. It did NOT repeat my
  original category error ("separate router-hints from human-docs into different file
  locations") — it absorbed the Janus finding that `<example>` blocks live *inside* the
  routing field, so the rule became "examples only if they demonstrably earn routing
  lift," not "relocate them." The broken version died in transit; the true version lived.
- **L8 (Moving compiler) = D2′, corrected.** Verbatim "unchanged `.md` ≠ unchanged
  behavior," and it **dropped** the per-run model-pin mechanism (Janus's "reproducibility
  theater" REVISE), replacing it with receipts/pilots/gavels. The ceremony Janus flagged
  is absent; the epistemic guardrail that survived is present.

Receipt trail: Sella cites the two 08-01 research files ([S2] arch study, [S1]/[S-EPOCH]
mechanics) plus [S5] the nablarva conforming-application precedent. Grounded, dated,
`state: DRAFT — pending majkee gavel` — it has not jumped the canon gate.

## 2 · @ferry — the doctrine made flesh (a good exemplar)

Point, don't re-list: ferry embodies terse no-example description (L2), name-teaches-job
(L3 — Sella's own L3 example), minimal explicit `tools` with no Write, a graded G0–G4
**exit ladder** as exit-code legibility (L4), judgment-here/mechanism-there
(`ferry/prep-home.sh`), vendor-invariance (contract = the ORDER, not a print-flag), and
— the sharp part — L8 as *behavior not ceremony*: "my route holds because each leg
re-verifies reality, never because last crossing worked." The moving-compiler honesty is
baked into `fetch-real-first`, not bolted on. This is what conformance should look like.

## 3 · FLAG-1 — `schema: 1` contradicts Sella itself (resolve before deploy)

ferry.md carries `schema: 1`. But: Sella §2's key surface does not list `schema`; the
Epoch receipt states plainly *"No `schema` key exists — house `schema: 1` is
forward-marker only"*; and Walk A step-3 gate says *"every key exists in the [S1] table —
no invented keys."* So the reference program trips its own gate. This is STUDY-2
tension #5 (the `schema: N` idea) half-surviving: present in ferry, unblessed in Sella.
**Resolve one way:** either Sella explicitly names `schema` a sanctioned house
forward-marker and exempts it from the no-invented-keys gate, or ferry drops the key.
Not cosmetic — a language's first program must not violate the language.

## 4 · FLAG-2 — recursive-minimalism risk (watch, don't fix yet)

Sella is a 380-line, nine-law language with a machine model, three walks, and a glossary.
Its *own* [S2] arch study says this audience reads every new layer as "prove you're not
bloat" and treats heaviness as a red flag. A coder-guide is a legitimate human full-read
(L9 grants humans full reads). The risk is only if *conformance* starts meaning "an agent
loads all nine laws." Philosophy-true form: **Sella stays the human guide; primitives
conform via a terse anchor (a provenance stone + the gates that apply), not by ingesting
380 lines.** Keep it a guide, not a liturgy. This is the language passing — or failing —
its own L9 and L2 at the meta level.

## 5 · OPEN — the mechanism gap is real and honestly marked

The Epoch receipt (claim 2) confirms *"Agent-description budget: UNRESOLVED — no analogous
cap found."* So L2's agent side rests partly on the skill-side 1,536-char cap; the
agent-side is not proven. Sella marks this honestly rather than papering it — correct.
But it means L2 is CONFIDENCE-M for agents until one targeted Epoch pass closes how the
`Agent`-tool `subagent_type` schema serializes descriptions into the parent request. Close
M→H before L2 is codified as hard canon; if the router reads only the `description` field,
nothing changes, but the budget claim needs its receipt.

---

*atlas-office observation · staged, deploy-inert · 2026-08-03 · advisory to majkee's gavel.*
