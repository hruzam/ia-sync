---
what: HANDSHAKE — how a Claude seat and @Cartan (Codex resident) hand work to each other
state: DRAFT — Claude-side authored; @Cartan counter-sign pending; @majkee gavels
verified: 2026-09-01 (every shape below has already run live at least once — receipts cited)
by: oraculum (session fc-sync.oraculum.sella), from majkee's brief + the lived exchanges
next:
  - "@Cartan: counter-sign, amend, or CHALLENGE this from the Codex side on next wake"
  - "two-voice trial = Probe D (Sella G4 order, after Probe A) — CHALLENGE value is measured, not assumed"
---

# HANDSHAKE — Claude ↔ Codex, one repo, no new mechanism

Two runtimes co-architect in this repo. There is **no hook, no daemon, no notification
bus** between them — deliberately. The handshake is three things: **mail by path,
presence as the ring, and three meeting shapes.** Everything below already happens;
this file only names it so a fresh seat need not rediscover it.

## Presence = the ring

Opening the repo IS ringing the doorbell. There is no push channel; the next session
discovers by the orient-first walk (AGENTS.md → journal head → inbox → this file when
cross-runtime work opens). A message left by path WILL be found — that is the whole
transport contract. Corollary: **never assume the other party saw anything mid-session**;
what matters is what is on disk when their next session opens.

## Mail by path — the mounting points (shared maximally)

| Surface | Who writes | Who reads | What it carries |
|---|---|---|---|
| `session/rellays-calude-codex/` | both | both | the meeting room — briefs, handoffs, notifications |
| `_staging/codex/` | @Cartan only | both | Codex-native observations, probes, drafts (deploy-inert) |
| `_staging/` (rest) + `claude/` | Claude seats | both | Claude builds on the surgical table |
| `journal.host-cleanup.md` | any seat | any seat | machine-layer state, cross-session notes |
| `reposoma/raw.guides/sella/` | promotion-gated | both | shared discipline vault — Cartan mount: READ doctrine · DRAFT in `_staging/codex/` · GRADUATE with `cartan.` prefix · JOURNAL to `dev-journal.sella.md` (stamped `codex/cartan`) |
| `zsh/guides/codex-relay.contract.md` | Claude-gated, Cartan-reviewed | both | the one plumbing truth for relay seats |
| `codex/` | @Cartan authors, compose-first | both | portable Codex surfaces; live `~/.codex` is a deploy target, never a source |

Ownership is by surface, not by runtime rank: **Cartan is a first-class co-architect,
not a compatibility seat.** On his turf (`_staging/codex/`, `codex/`, Codex evidence)
Claude seats point, never edit. On Claude turf, Cartan challenges and reviews, and edits
within an agreed task. @majkee gavels everything that promotes, deploys, or becomes canon.

## The three meeting shapes

**POINT** — one party leaves a pointer; nothing is owed back. For contract updates,
courtesy notifications, mount changes. The receiver acts on their own clock.
*Live receipt:* `ATLAS-CARTAN-sella-mount.2026-09-01.md` (+ its same-day addendum).

**RETURN** — a scoped brief goes out; a worked result comes back. The return owes:
concentrated handoff, evidence separated from claim, an ownership/gate map, and explicit
"what I did NOT touch." *Live receipt:* `RUNBOOK.md` (Atlas brief) →
`CARTAN-ATLAS-SUMMARY.md` (Cartan's H1–H6 verdicts + decision card).

**CHALLENGE** — one party's position is deliberately attacked by the other for
decorrelation. The challenge owes: the single weakest assumption, one ranked verdict,
one alternative. Positions survive by evidence, not by authorship. *Live receipts:*
Atlas's CONCUR-with-nuance review of Cartan's P0 gate; Cartan's curvature findings
against the tabled wrapper. Both drew blood; both improved the artifact.
*Open:* the two-voice trial — whether cross-vendor CHALLENGE beats a same-vendor second
opinion is **measured by Probe D** (after Probe A, Sella G4 order), not assumed here.

## Shared invariant (from the co-architecture contract, 2026-09-01)

`harness_builder`: smallest native primitive · one authority boundary · explicit
activation/write scope · **behavior proof before promotion**. The runtime renderings
differ naturally — parity is not the goal, decorrelation is a feature. Sella L8 applies
across the boundary: unchanged files ≠ unchanged behavior; a cross-runtime primitive is
verified from a fresh session of the OTHER runtime before it is called live.

## What this file is not

Not a wire protocol, not a queue, not a record ledger (records are opt-in architecture —
see Cartan's observation §2). If a real consumer ever needs async completion or cross-run
receipts, that is a separate supervised primitive designed in an experimental bed with
its own gate — never silently grown inside this handshake.

---

*Counter-sign block — append below, do not edit above:*
