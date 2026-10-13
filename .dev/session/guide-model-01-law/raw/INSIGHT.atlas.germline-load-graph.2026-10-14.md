---
title: INSIGHT — Atlas · germline controllers: one shape, two visibilities · load graph + Houston grounding
by: @Atlas (atlas-ui, consult posture) · majkee voice loop, session ff-sync.atlas.guide-model-01-law.harness
date: 2026-10-14
shape: POINT-grade note for Cartan / the germline-02 planning head — acknowledgement-free
authority: none by itself — majkee's direction (rank 1, temple/precedence.md) + Houston consult (stretches) + dated vendor facts; canon only after majkee's gavel
reads-with: POINT.atlas-to-Cartan.2026-10-13.md · RECONCILIATION.germline-02-guide-model-law.2026-10-13.md · RETURN.atlas.germline-02-reconciliation.2026-10-14.md
---

# INSIGHT — germline controllers: one shape, two visibilities

Supersedes the load graph in my chat answer of 2026-10-14 (card → program as a required edge is
withdrawn). Not read: `hypotheses.reconcile-only.md`.

## 1 · The model (majkee, 2026-10-14 — working, not gaveled)

One controller shape — invariants on top, one file per occasion below — in **two visibilities**:

| | **card** — private controller | **program** — public controller |
|---|---|---|
| belongs to | one agent's identity (inner build) | nobody — any seat, any vendor, a human |
| home | `germline/agents/<slug>/cards/` | `germline/programs/<slug>/` (working name) |
| answers | "how *I* act on this occasion" | "how *anyone* does this job" |
| authority | **grants** — invokers, reads, writes (the pen) | **requires** — capabilities the caller holds |
| example | `houston/cards/consult` | `tunnel`: run · recover · assist-user |

The GUIDE stays the book ("understand tunnel") and points at the public program.

**One edge rule survives:** private → public may point (a card may use a program, optional);
public → private never (a program names no agent, no card, no vendor).

**Promotion rule (anti-duplication):** when a card's procedure proves useful beyond its agent, it
moves into a public program and the card keeps a pointer. One home per procedure.

## 2 · Graph

```
GUIDE (book) ──points──► programs/<P>/CONTROLLER.md ──one hop──► fn/<verb-object>.md ──► MODEL
                              ▲  (invariants · requires · model refs · functions table)     (state/schema
                              │ optional, by name                                              at its owner)
agent wrapper ─► identity ─► binding.<vendor> ─► addendum ─► cards/<card> (private, holds the pen)

vendor entry for public use: ONE global `perform` (resolves, never discovers)
enforcement home: vendor-side (e.g. ia-sync claude/hooks) pointing DOWN at the program
forbidden: program → card/identity/vendor · fn → fn as prerequisite · program → guide as prerequisite
```

## 3 · Vendor facts that force the shape (@Epoch, live-fetched 2026-10-14, confidence H)

- Scope precedence is unusable for project/global choice: Claude skills personal > project;
  Claude agents project > user; Codex skills no precedence (both listed). → resolve explicitly.
- Agent Skills spec: "keep file references one level deep from SKILL.md". → controller → fn, one hop.
- Skill `allowed-tools` is a one-turn **grant**, never a restriction (Claude); unverified on Codex.
  Only Claude agent `tools`/`disallowedTools` + hooks enforce; Codex agents cannot override sandbox.
- Codex skill listing capped at ~2% of context. → one generic `perform`, not one skill per program.
- Codex skills scan `~/.agents/skills` (already the deploy target — master-brief.2026-09-23:103).
- OpenAI docs moved: developers.openai.com/codex/* → learn.chatgpt.com/docs/* (308).

## 4 · Houston consult — verdict **stretches** (neutral Houston, no addendum; stamps 6abf41fe · 9a3f17c0 · 46dcd163)

No lock or home breaks. Holds only under:

1. **Specialise, never replace.** A same-slug project package declares `specialises: <global
   CONTROLLER> @ stamp`; may add or narrow, never drop a global invariant; disagreement = finding,
   not choice (germline-forge/GUIDE.md:36-38). One global `perform`; projects ship none.
2. **The functions table is the only index.** Deploy is additive (germline/README.md:15-16) → ghost
   fns. `perform` loads only table-named fns with matching `stamp:`; takes an explicit slug + fn from
   a card row or the operator — no listing, no occasion auto-match (keeps clear of the parked
   discovery bus, master-brief:164, germline/README.md:18).
3. **Enforcement needs its own home + a placement proof.** Not agent bindings (N copies; program →
   agent forbidden). A costly controller is live only after a fresh-session witness of a run that
   survives compaction.
4. **Cards keep the pen.** Reads/Writes stay in cards (identity.md:21-22; nablarva flag L16.14);
   programs require, never grant. Rewiring Houston's cards = its own move under fresh eyes (L16.8).
5. **One home per method + a naming gavel.** `germline/skills/` already holds "vendor-neutral
   methods" (README.md:12) — write the skills/ ↔ programs/ boundary before the first program lands.
   "Program" = agent in Sella and germline-forge — keep deliberately with one distinguishing line,
   or rename.

## 5 · The foundation stone — invariance-autonomy (majkee: older, but the basic stone)

Principles that bind the programs move: measure before building/naming (identity · method · binding;
body/method/nothing — the 02 whole-tree pass is that measurement for programs) · prove placement,
not only content (master-brief:136-137) · single source, one-way stamped renderings (ptyra) ·
twin-slug. Placements since revised by later gavels: identity home (germline-01, 2026-10-12),
build-time render → runtime load (Houston fold, 2026-10-10). The candidate `Programs` H2 inside
identity was never locked; neutral programs = the "method" outcome given its own home. The identity
may still list the programs it performs — by reference.

## 6 · Naming candidates (majkee: not final)

- package: `programs/` (at rest) — or `processes/`
- entry: `CONTROLLER.md` (germline has no legacy address to protect)
- one run of `perform` = a **process**; its record = selection receipt (scope + stamps) + completion
  evidence — names Cartan's open "selection receipt" (RECONCILIATION:111-112)

## 7 · Open — tests (dated client, L8) and gavels

Tests: does `!cat` hydration survive compaction · does `!` preprocessing run for a seat without
Bash · does Codex ignore unknown frontmatter · does Claude have a `Skill(name)` permission rule.
Gavels: package/entry names · skills/ ↔ programs/ boundary · enforcement home · card/program
visibility model + promotion rule · BACKGROUND disposition (RETURN C4).

## 8 · Side findings (filed as issue cards, not this program's scope)

- `~/.germline` is a REAL dir, byte-identical to `~/ia-sync/germline` working tree (verified
  2026-10-14, office) — office migration done; journal still says OPEN.
- `germline/agents/houston/*` deployed but uncommitted — deploy ran ahead of commit (README.md:15).
- `~/reposoma/.germline/` = the old home (pre-migration stamps); holds `tunnel/tunnel.preamble.md`
  with no ia-sync copy; germline-forge GUIDE describes the pre-10-10 render model throughout.
