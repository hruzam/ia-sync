---
kind: pre-runbook-return
date: 2026-10-03
from: atlas-ui
to: cartan (cSharp-tunnel head) · via majkee
answers: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/brief.atlas-ui.2026-10-03.md
package: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/atlas-ui/
host: office
verification: source review + guide law + majkee's drawings; no fresh-session proof, no tunnel enable, no deploy, no commit
---

# Atlas UI — RETURN: the provisional BUS seat `shuttle`

## 1. Primitive choice and reuse/collision check

**Choice: a provisional, project-scoped Claude agent** rendered from a `.germline` source — not a
skill, not a global role, not a modified Flight.

- *Reuse check:* the BUS is functionally Flight's **project-session mode** (reads RUNBOOK chapter →
  dispatches graded executors → Assay gate → handoff) placed **under a Codex cSharp head reached
  through the tunnel**. The delta is small and specific: head consultation over `tun`, two delivery
  routes, head-binding and unknown-completion rules, no STATUS of its own, temporary lifetime.
- *Why not Flight directly:* Flight's card is 159 lines of global wiring (pulse.flight, MCP, CEO
  proxy, hooks) and is deployed to both hosts; bending it for a pilot leaves exactly the standing
  global residue the brief forbids.
- *Why not a skill (surfaced for majkee as asked, and answered):* a skill body loads below the
  kernel boundary (Sella L1/L7). The BUS's hard limits — no self-enable, never compose the head's
  STATUS, never accept own work, bind the actual head — must survive a long, compacting session;
  a skill cannot pin model/effort either. A skill would be right for a short-lived or soft-ruled
  seat; this one is neither. majkee accepted the agent form (2026-10-03).
- *Collisions:* seat name `shuttle` (majkee's pick) — no roster hit on either line; `relay` was
  rejected because it is a fixed instrument noun (`cross-vendor-seat.md`) and a Claude agent family;
  `bus` rejected per the brief (distinct from `_bus/`). Vara / `/track-run` ("sequencer bus") walk
  pre-routed tracks and never author or dispatch — different job.

## 2. Package paths, source provenance, activation / deactivation

- Source: `raw/atlas-ui/germline/agents/shuttle/identity.md` — `gen: germline`, `scope:
  project:ia-sync`, `lifetime:` = this bed, `revision: unresolved` (uncommitted), `verified: none`.
- Rendering: `raw/atlas-ui/render/claude/shuttle.md` — `sonnet · high`, tools `Read Grep Glob Write
  Edit Bash Agent`, stamp as first body line, identity body verbatim + a Claude VENDOR DELTA section.
- Activation (majkee, after review): source → `~/ia-sync/.germline/agents/shuttle/identity.md`;
  rendering → `~/ia-sync/.claude/agents/shuttle.md`; commit; stamp the revision; commit. **No deploy
  leg** — project `.claude/` is read in place; the table and `~/.claude/` are untouched.
- Deactivation: at the tunnel-02 gate, by the cSharp head's closing sweep with majkee's hand —
  `git rm` the rendering, archive or delete the source, one journal line. Lessons may fold into
  Flight's project-session mode; the seat retires regardless.
- Full procedure + proof table: `raw/atlas-ui/README.md`.

## 3. The BUS instruction contract — operator-carried delivery and failure handling

Ten behaviour rules in the identity (§Behaviour). The ones the RUNBOOK must know:

- **Routes:** Cartan's 2026-10-03 wording adopted verbatim (rule 3). The fallback is named
  **operator-carried delivery**; "relay" is forbidden for it.
- **Bind the actual head** (rule 4, v1.2 per BRICK-01): three RUNBOOK-fixed ways — birth (reading A,
  first `send` at the handle's `--cwd`), bind (reading C, operator's `open --thread <id>` +
  explicit `resume`), continuation (stored `threadId`). Seat check = `tun status` runtime stamp
  (`threadId · cwd · sandbox · effort · model · instructionSources`) equals the RUNBOOK's; else stop.
- **Unknown completion ≠ retry** (rule 5): `tun read` returns raw thread data — last turn
  `completed` → use, never re-send; `interrupted`/absent → operator-carried delivery of the **same
  cycle id**. Exit 50 = send/ask reconcile mismatch (record); exit 61 = turn in flight on this
  handle (wait or `read`). One turn per head is now mechanical (`<state>.lock`).
- **Operator-only enable is an instruction, not a wall** (rule 6): exit 10 proves sending needs a
  table; nothing stops the seat from running `open --enable` unless majkee adds a deny rule
  (README proof #2 names the smallest one).
- **Failure form:** `BLOCKED: <reason> · evidence: <path> · asked: <head|majkee>`.
- **Initiative shape:** the BUS brings one ready question and asks the head to open the cycle;
  it never writes a VERDICT. **STATUS:** never composed by the BUS; verbatim scribing only when the
  RUNBOOK names it scribe (rule 8b) — the same conditional in identity, binding and here.
- **Second mind** = advisor spawn, never a second head (resolves drawing 1's "Claude head (second
  mind)" against one-head/one-STATUS).

## 4. Claimed permissions vs. what still needs a fresh-session behavior proof

See `raw/atlas-ui/README.md` §Proofs — six rows. Headline: direct `--agent` entry for a
**project-scoped** agent is UNVERIFIED on this install (proof #1); **operator-only enable is an
instruction** — exit 10 only proves sending needs a table; a project deny rule would make it
mechanical (proof #2, not built); write scope is prose-only — tools allow more — so the first
cycle's diff needs an Assay-grade check (proof #4); the head's effective permissions (read-only
default, approvals declined — `tunnel-codex.py:306`) are the head owner's proof, not the BUS's.
Mechanical already (BRICK-01): one turn per handle (exit 61), reconcile mismatch (exit 50), `cwd`
in the handle, binding check via `status` runtime stamp.

## 5. Conflicts with the drawings or existing guides

1. **Hand delivery vs `cross-vendor-seat.md` amendment 2** ("an instrument does not change inside a
   live RUNBOOK"). Cartan's review: acceptable for this pilot **only as majkee's explicit birth-time
   exception**, same cycle, same head, route recorded. The RUNBOOK must say so in its known
   constraints; "emergency" alone does not resolve the chapter's distinction. The chapter itself is
   DRAFT (ungaveled) — a one-line amendment there is the durable fix, not this package.
2. **Drawing 1 — "BUS creates files in bus raw/ res/ src/":** those are bed folders; `_bus/` holds
   only `NN.<seat>.<kind>.md`. The identity separates the two words explicitly.
3. **Drawing 1 — "Claude head (second mind)" spawned by BUS:** treated as an advisor spawn, not a
   head (above). If majkee meant a true second head, that is a different protocol, not Protocol 1.
4. **Drawing 2, Q1 (can A and B share one main?)** — out of this brief's scope; noted as open.
5. **Trajectory's handoff landed during authoring** (`raw/trajectory.handoff.2026-10-03.md`, 218 l)
   — folded into package v1.1 the same day: head reading A/B/C → rule 4 (birth once, continuation
   always); `tun read` completed/interrupted → rule 5; cross-host resume ban → rule 8; receipt
   fields incl. serving binary → Scripts; `cd` before every call + one-turn-in-flight → Claude
   binding; mechanism-vs-prose → README.
6. **STATUS ownership vs a read-only head** (Trajectory §3): cSharp law makes the head
   `status_owner`; a read-only headless head cannot write. The RUNBOOK must pick (i) head opened
   `workspace-write` at `cwd` = bed, or (ii) **BUS as scribe** — the identity now carries rule 8b
   for (ii): verbatim transcription on dictation, recorded in the receipt, composition never mine.
7. **Upward POINT:** the bus GUIDE models POINT as *assignment*; a BUS-authored POINT to the head
   inverts authority (and who writes its VERDICT?). Identity softened to "I bring one ready
   question and ask the head to open the cycle". Trajectory's receipt sketch (`NN.bus.point.md` →
   `NN.head.return.md`) also breaks the `<seat>` filename rule (`shuttle` · `cartan`, not
   `bus`/`head`). Cartan decides the shape; both files must carry the writer's seat name.
8. **Which head (A/B/C) is the RUNBOOK's first decision** — the package is reading-agnostic but
   only A keeps the tunnel primary; under B the fallback becomes the primary and the pilot does
   not test the tunnel.

## 6. Facts Cartan must carry into the forthcoming RUNBOOK

- Participant tuple for the BUS: `[shuttle, {brand: claude, model: sonnet, effort: high}, host:
  office, role: BUS — initiative + coordination; writes only _bus/NN.shuttle.* and raw/shuttle/**]`.
  Codex rendering, if ever wanted: `gpt-5.6-terra · high` (not built; no twin required).
- Head participant from the BUS's side: `instrument: tunnel`; handle
  `~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.state.json` (gitignored, created only
  by the operator's `open --enable`; thread born on first send).
- Known constraint lines: (a) *no seat opens the table*; (b) *operator-carried delivery is majkee's
  explicit exception to cross-vendor-seat amendment 2 — same identified cycle, same head, route
  recorded, manual completion ≠ tunnel success*; (c) *the BUS never writes a VERDICT and never composes STATUS — verbatim scribing only if the RUNBOOK names it scribe*;
  (d) *print mode `-p` never*.
- STATUS `holds:` while the table is open: one handle/host, no second open, close before the session
  closes or relinquishes the table (Cartan amendment 3).
- Acceptance evidence to list: the six proofs in the package README (#1–#5 the BUS's, #6 the head
  owner's effective-permission run), plus one complete POINT → RETURN → VERDICT cycle with the route
  line recorded.
- Lifecycle: activation is majkee's promotion (README §Activation); retirement at this gate by the
  head's closing sweep; the seat may not survive into a sibling session without re-scoping.
- `_bus/` is born at two live seats (head + shuttle) — not before.
- Shim facts as of **BRICK-01 (2026-10-03, uncommitted in `zsh/ai/`, deployed on office — commit
  before the RUNBOOK cites it):** `open --cwd <dir>` persisted in the handle and applied on every
  verb (head identity is deliberate, no `cd` discipline needed) · `open --thread <id>` binds an
  existing stored thread (reading C), resume is the operator's explicit verb · `<state>.lock` per
  handle, second caller exit 61 · runtime stamp in `status` · exit 50 belongs to send/ask
  reconciliation, `read` returns thread JSON. Trajectory's §3 gap table predates this brick.
- From Trajectory's handoff, carried not restated: every live proof records the serving Codex
  binary (0.159.3 CLI vs 0.160.0 daemon both live on office); cross-host resume of a thread another
  host's TUI may hold is forbidden; T2/T3 parametrization is NOT a Protocol 1 prerequisite.

## Remaining uncertainty

Everything in §4 (six proofs, none run). Whether an unknown frontmatter key (`gen:`) is tolerated in
a native Claude agent file — not assumed; the sign is in the source and the body stamp. Whether
`.germline/agents/<slug>/identity.md`'s H2 set survives the Atlas invariance measurement — this
package uses the candidate schema; if the schema changes, the source is re-shaped and re-rendered.
