---
what: errata r1 to sella.cross-vendor.architecture.candidate.2026-08-04.md — the five
     bounded corrections Wave's formal check required (CONDITIONAL PASS ruling,
     dev-journal.sella.md, 2026-08-04). Supersedes the named sections of the candidate;
     the candidate itself is preserved unmodified as history
state: CANDIDATE-r1 — staged, deploy-inert; advisory to majkee's gavel. NOT a v2 guide,
     NOT a redesign — errata only, per Wave's scope
verified: 2026-08-04 (inputs: Wave's gavel-phase check + voice · the original candidate ·
     sella.receipt.codex.2026-08-03.md · dev-journal.sella.md)
by: atlas-ui (opus, office). Concurrence map: all five findings accepted (F3's factual
     sub-claim flagged, see E3)
next:
  - majkee: revised gavel block G1–G5 (end of file)
  - one live fetch closes the E3 URL-fact discrepancy (any web seat, one claim)
  - probes A(clean-first) → B → D/E, on majkee's release
---

# Errata r1 — five corrections to the architecture candidate

## E1 — architecture comparison decoupled (replaces candidate §1)

The candidate coupled two independent decisions: language scope and boundary governance.
The strongest alternative — **Claude-only Sella + a separate neutral exchange contract**
— was Wave's own supplied rejection path and was missing. Restored, two axes:

| Language scope | Boundary governance | Assessment |
|---|---|---|
| **B1** Claude-only Sella | separate neutral exchange contract | **the real rival.** Governs live cross-vendor traffic WITHOUT making Sella cross-vendor. Cheap, reversible, no shared-core maintenance |
| **B2** thin Sella core + vendor profiles | the same exchange contract | Wave's A3. Adds shared LAWS above the contract. Must prove the laws add measured value BEYOND the contract itself |
| **B3** monolithic cross-vendor Sella | embedded vendor mechanics | still rejected — inherits both vendors' churn; no guard survives L8 |

**Corrected question for probes D/E:** not "is a boundary contract useful" (both B1 and
B2 have one) but **"do shared core laws add measured value beyond the exchange contract
alone?"** A3/B2 status: **authorized as an experiment branch only — NOT adopted.** If
D/E show no law-level lift over B1, Sella stays Claude-only and the exchange contract
stands alone.

## E2 — L4 flip reversed (replaces candidate §2, L4 row)

The 0/2 exit-pair promotion to CORE was wrong: integer convergence ≠ semantic
convergence. Exit-2 effects differ BY EVENT within each vendor (deny before-tool ·
non-undoable after-tool · "continue" on stop-class events) — there is no stable shared
ABI, only a shared surface. Corrected classification:

- **CORE keeps only:** *every boundary operation returns an explicit typed result state
  and a reason; native event/exit mappings live in the named machine profile.*
- **PROFILES keep:** each vendor's full event × exit-code × effect table.
- **Retained observation (both profiles, marked):** the 0/2 surface convergence is real
  and worth recording — as a note, not a law. If Sella ever defines a process-level
  transport ABI, that is a NEW adapter contract with tested mappings, not a discovered
  universal.

## E3 — evidence rule repaired (replaces candidate §1 A2-evidence + receipt discipline)

Two corrections, one flag:

1. **Claim corrected:** "Wave's links went stale inside 24h" is withdrawn. Host movement
   demonstrates VOLATILITY (routing churn), not breakage; it does not by itself prove
   the monolith multiplies failure. B3's rejection now rests on the churn-inheritance
   argument alone, which stands without the overreach.
2. **Rule adopted (this is the durable fix):** *point-never-copy is safe only for
   stable, git-tracked LOCAL artifacts. Volatile EXTERNAL receipts must preserve the
   exact carried claim + retrieval date + observed version where available + confidence
   + enough excerpt/fingerprint to identify what was actually read.* Not whole manuals —
   enough to falsify yesterday's claim tomorrow.
3. **Flag (unresolved fact, one fetch closes it):** Epoch (2026-08-03) reported
   migration TO `developers.openai.com`; Wave's live check (2026-08-04) reports the
   Learn URLs resolving and the developers URL redirecting TO them. Wave's is the newer
   dated receipt and is adopted at confidence M; the discrepancy is itself the best
   specimen of why rule 2 exists — Epoch's receipt did not carry a fingerprint, so it
   cannot be audited now. One direct fetch closes this; flagged, not blocking.

## E4 — contract, not protocol (replaces candidate §4 title + one field rule)

- **Renamed:** the 11-field checklist is the **SELLA exchange contract candidate**. It
  becomes a *protocol* only when wire encoding (or negotiated mappings), versioning/
  compatibility rules, transport assumptions, and failure behavior exist and are proven
  at a machine boundary (Probe E territory).
- **Source-scope field corrected:** "paths, not pasted bodies" → **resolvable source
  references.** Bare paths suffice only when both seats share filesystem + revision.
  Across home/office hosts, worktrees, or vendors, a reference may need repository
  identity, revision/snapshot, content hash, access assumption, or a bounded inline
  excerpt. The law is "no undifferentiated context dumps," not "paths are universal."

## E5 — blind critique demoted (replaces candidate §6)

Blind critique leaves CORE. A Sella-conforming single-vendor build must not pay a
blind-review tax. The envelope keeps only the `consult` verb semantics; the full
procedure (frozen position-free brief · no position leak · independent outputs before
synthesis · synthesis owner rechecks sources · named write owner · no recursive loop)
moves to an **optional COMPOSITE pattern**, promoted into anything binding only if
Probe D shows it changes decisions or catches defects. (This is the candidate's own
FLAG-2 anchor-conformance discipline, applied to itself.)

## Revised gavel block — G1–G5 (Wave's formal advice · Atlas concurs on all five)

| # | Decision | Ruling proposed |
|---|---|---|
| G1 | A3/B2 status | **authorize for probes as experiment branch; do NOT adopt.** Must beat B1 (Claude-only + exchange contract), not an ungoverned strawman |
| G2 | ferry `schema: 1` | **strip** — unless a house-schema contract is separately defined AND enforced |
| G3 | sella.coder-guide.md gavel | **HOLD** — a retitle is not a profile. An actual CLAUDE PROFILE candidate (ontology scoped, CORE laws lifted out, open facts marked) must exist first |
| G4 | probes | **authorize with ordering law: clean Probe A BEFORE installing Jacquard for B** (installing first contaminates the baseline). D/E mandatory before any architectural promotion; C follows profile survival |
| G5 | name | **Sella confirmed; no second language name** |

---

*atlas-ui errata r1 · staged, deploy-inert · 2026-08-04 · candidate preserved unmodified
as history · no v2 written · no deploy implied · majkee retains the gavel.*
