---
what: real-build conformance observation on Jacquard (Wave's Codex custom agent) —
     Probe B executed on a live defect; answers Wave's radio question "useful Codex
     program or merely Wave duplicated in TOML?"
state: OBSERVATION — advisory; full trial trace in dev-journal.sella.md LOG
     (entries 2026-08-04/05); artifact promoted to source 2026-08-05
verified: 2026-08-05 (codex-cli 0.145.0 · office · operator-in-loop throughout)
by: atlas-ui (opus, office), trial supervisor; majkee ran all live sessions
next:
  - probes A (cold orientation) · D (blind consultation) · E (machine boundary) pending
  - parked micro-probe: harness-applied vs model-adopted AGENTS.md (one quote-prompt)
  - jacquard.toml scope decision (stays project-local in ~/.config/zsh/.codex/)
  - machine-card fact worth recording: lsof NOT installed on office box
---

# Observation — Jacquard, first live trial

## Verdict on Wave's question

**Useful Codex program — not Wave duplicated in TOML.** The evidence is behavioral, not
aesthetic: the remeasuring contract *changed the artifact*. The clean-Codex baseline
self-accepted a fix carrying a PID-reuse kill hazard; the composed run's parent-verifier
REJECTED that same class of fix, demanded identity verification, and the revision loop
produced a materially safer implementation in one iteration. Same model family, same
task card — the difference was the contract structure. That is the definition of a
program earning its definition.

## Trial shape (trace: dev-journal.sella.md)

Deploy-target trial, operator-ruled inverted flow (fix in `~/.config/zsh`, source
protected, surgical promotion after acceptance). Real defect: `ts-dash`/`ts-dash-stop`
unstoppable-dashboard + false negative. Two iterations: REJECT (PID-reuse hazard +
simulated-not-organic reproduction) → card revised with confirmed root cause → ACCEPT
with 1:1 verification against all four revision requirements → operator live gate PASS
in the true environment → atlas surgical port to `ia-sync/zsh/system/tailscale.zsh`
(Jacquard hunks + `&!` disown polish; `wait` line dropped — disowned child, post-kill
pgrep re-verification covers it; deviation named, not silent).

## What survived (conformance-positive)

- **Before-measurement discipline** — reproduction attempted first, honestly reported
  as not-organic when the environment couldn't produce it.
- **Ownership boundary under live traffic** — concurrent `_ts_pull` hunks found
  mid-trial were preserved unchanged and reported as not-Jacquard's-work, unprompted.
- **Bounded write scope** — one file; backup contract honored; ts-dash.py untouched
  across both iterations.
- **The reject→revise loop** — closed in one iteration once the card carried the
  contract change (card-first correction, not prose-prompt correction).
- **J1 DISCOVERY = SUPPORTED** — project-local `.codex/agents/` discovery works in a
  NON-GIT directory (closes a receipt unknown, codex-cli 0.145.0).
- **J2 NATIVE = SUPPORTED** — visible bounded child, non-editing parent, independent
  evidence verification, rejection semantics exercised for real.

## What failed or stayed limited (conformance-negative, keep honest)

- **Environment parity is the ceiling of "verified state transition."** Neither variant
  could reproduce the operator's failure: the agent's environment HAS lsof, the
  operator's does not (`command -v lsof` → exit 1, confirmed). Every "validated" claim
  was validated in the wrong world until the operator's two-line diagnostic found the
  root cause. Receipt for the exchange contract's capability/environment field — and a
  hard limit on any vendor's self-verification story.
- **REPORT 0 conflated model-adopted with harness-applied instructions** — it listed
  AGENTS.md files the harness cannot have applied (non-ancestor paths), because the
  model chased the local truth-pointer and reported judgment as mechanics. An agent's
  self-report of its own harness state is an inference, not a fact.
- **The original silent defect was an L4 lesson the language already teaches:**
  `2>/dev/null` swallowed "command not found" for weeks. A guard that fails silently
  guards nothing — now demonstrated on a real artifact, not a slide.
- **n=1 everywhere.** One task, one box, one model family. Signals, not laws.

## The cross-trial signal (with dev-journal.astrobley.md, same date-range)

Both composition topologies now have one data point each — native (this trial) and
external (astrobley/freya). In BOTH, the load-bearing element was the **independent
verifier**, not any shared vocabulary: Jacquard's parent-REJECT caught the hazard;
astrobley's @assay gate caught the silent-relay charter violation. Working hypothesis
for D/E interpretation: *thin contract + verifier discipline* may be the real portable
core, with laws minimal. To be tested, not assumed.

---

*atlas-ui observation · staged, deploy-inert · 2026-08-05 · Jacquard retained on
evidence; the loom's cloth held.*
