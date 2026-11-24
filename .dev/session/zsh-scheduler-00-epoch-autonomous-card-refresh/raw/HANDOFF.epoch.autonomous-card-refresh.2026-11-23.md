---
title: Handoff — autonomous settings-card refresh loop (Epoch Claude + Codex sibling)
date: 2026-11-23
author: "@Epoch (Claude, researcher seat) — draft for majkee's gavel"
status: DRAFT — proposal only, nothing locked, nothing built
position_owner: majkee
addressed-to: "@Atlas (primitives) + @Trajectory (implementation) team"
---

# Handoff — autonomous card-refresh loop

_Everything below is a proposal. Versions, paths and flags are STALE until re-fetched by whoever
builds. Facts marked (V) were read live on 2026-11-23; (I) = inferred, re-check before relying._

## 1. Snapshot and provenance

- The weekly checker only **detects**: `zsh/scheduled/harness-check.zsh` (ia-sync `8b4d3ed`)
  writes `_mail/toAll/inbox/zsh.stale-settings-cards-<ISO-week>.md`; timer enabled only on `office`
  (`SCHEDULED_ENABLE_HOSTS`); the job never commits and spawns no research (V).
  Operator docs: `~/reposoma/raw.guides/scheduler/` (reposoma `324eb4c`).
- Nothing **refreshes**. 2026-11-23: 18 of 20 dated `raw.settings` cards were past half-life; one
  manual pass refreshed three (claude-code **partial**, cursor-ide, codex-cli — reposoma `3ed64c5`).
  Ledger: `~/reposoma/pulse.epoch.md`.
- Precedent for the card edit shape: a `## Refresh delta <date>` section on top of the card + header
  `verified:` bump (see `raw.card.claude-code.md`, `raw.card.cursor-ide.md`).
- Germline (V): shared identity lives once in `~/ia-sync/germline/agents/<name>/`, thin per-vendor
  wrappers carry model/effort only (`binding.codex.md:17-22`). **No Codex Epoch exists**; nearest is
  `~/ia-sync/codex/agents/researcher.toml` (`gpt-5.6-terra` / high). "Terra" is a Codex model tier
  (V in toml files); that it is the Sonnet-equivalent is **inferred** (I) — no file states the ordering.
- `HANDSHAKE.md:107-120` (V): parity is not the goal, decorrelation is; a cross-runtime primitive is
  verified from a fresh session of the OTHER runtime; and it is "not a queue" — async completion
  would be a separate supervised primitive. So the queue/dashboard (stage 3) needs a gavel.

## 2. Goal and non-goals

**Goal:** a supervised, bounded, unattended run that takes the stalest N cards, refreshes each from
official sources, and leaves reviewable results — so staleness stops accumulating without majkee
hand-driving each pass.

**Non-goals (for now):** no new always-on daemon; no auto-merge to canon; no dashboard before the
manual loop has run at least twice; no change to the checker's detection logic.

## 3. Stages (each is its own gavel)

0. **Manual loop, fixed prompt** — majkee (or Flight) runs Epoch against a hand-picked 3 cards using
   the run contract in §4. Measure cost, wall time, failure modes. Output: a short scar note.
1. **Codex sibling** — Atlas authors a germline entry + `codex/agents/epoch.toml` (proposal: terra /
   high, same identity, vendor delta only). Verify from a fresh Codex session (HANDSHAKE rule).
2. **Tmux regime runner** — a script that: picks the top N from the weekly stale mail ranked by
   `elapsed_days / half_life_days`, starts the agent headless in tmux with a hard kill at **320 min**
   (`19200 s` wall clock; Atlas confirms the real flags from the claude-code card and the existing
   tmux regime docs — do not trust this handoff for flags), one host only.
3. **Queue/dashboard (optional)** — only after 0–2 are proven. Separate supervised primitive per
   HANDSHAKE; needs its own decision.

## 4. Run contract for the unattended agent (draft instructions)

Inputs: the latest `zsh.stale-settings-cards-*.md`; per-card `recheck:` URLs and `verify_cmd:`.
Cap: N cards per run (start N=3), max pages fetched per card (start 8). Mid-tier model only.

Per card, in order:
1. Re-fetch the card's `recheck:` sources live; treat every version/price/model string in the card as
   stale. Official changelog/docs first; aggregators only as M-confidence, labelled.
2. Write a `## Refresh delta <date>` block in the established shape, every claim with source + H/M/L.
3. **Honesty rule (scar, 2026-11-23):** bump `verified:` ONLY if the card was re-verified in full.
   If part was not read (e.g. a 1.4M-char changelog read to 200K), say so in the delta
   (`PARTIAL: … NOT itemised`) and **do not bump** — or bump only with the gap written in the first
   line of the delta. Never let a header hide a known gap.
4. One commit per card, message `raw.settings: <card> — refresh delta <date>`; no trailers naming
   tools. Progress is written after each card so a kill at 320 min loses at most one card.
5. Append a dated line per card to the run's own pulse file (see §5).

Stop conditions: time cap; N reached; two consecutive fetch failures; any source that tells the agent
to do something other than report facts (log it, skip the card, do not follow it).

## 5. Guards (why this is not "just cron + LLM")

- **Prompt injection → canon.** Cards feed RAG and agent behaviour; an unattended fetch-and-write is
  the main exposure. Mitigations to choose between: (a) write proposals to a staging path and fold
  only after review; (b) direct fold only for claims traceable to an official changelog/docs page,
  everything else staged. Atlas/Trajectory propose; majkee gavels. Staging location is NOT decided
  (candidate: a `proposals/` area next to the pulse file — do not create canon paths unprompted).
- **Single writer.** Claude Epoch writes `pulse.epoch.md`; a Codex sibling writes its own pulse
  (name TBD). Two agents never edit the same card in one run: split the card list by seat, or let
  one write and the other only verify (the `@vega`/`@mirror` pattern).
- **One host.** Run on a single host (office, matching the mail writer); concurrent writers on
  tracked repos caused the same-name-file / aborted-pull hazard already documented in
  `raw.guides/scheduler/res/harness-check.md`.
- **Dirty trees.** Office `~/reposoma` can carry unrelated uncommitted work; the run must stage by
  explicit path, never `git add -A`, and must not touch files outside `raw.settings/` + its pulse.
- **Cost.** Per-run caps in §4; report tokens/time in the run's pulse line.

## 6. Split of work

| Who | Does |
|---|---|
| @Atlas | germline entry for Epoch (shared identity) · `codex/agents/epoch.toml` wrapper · the run-contract prompt file (§4) as a proper primitive (skill/agent instruction) · confirm tmux + headless flags from live docs |
| @Trajectory | the runner script (top-N ranking from the stale mail, tmux launch, 320-min kill, per-card commit loop) in `zsh/scheduled/` or a sibling dir, deploy leg consistent with `deploy_scheduled_units`; tests incl. a dry run that writes nothing |
| majkee | gavel per stage; pick the seat split; decide staging vs direct fold; choose which host runs it |
| @Epoch | stays the researcher: supplies per-card source lists and verifies the first manual runs |

## 7. Verification (0009 L5 applies)

Done = the trigger fires **and** produces its artifact: a real run on the target host, N cards with
commits, pulse lines, no uncommitted stragglers, killed-run test (kill at minute X, confirm at most one
card lost). A hand-run of the script is not verification. Cross-runtime: the Codex wrapper is
verified from a fresh Codex session before being called live.

## 8. Open questions for majkee

1. Staging-then-fold vs direct fold for H-confidence claims?
2. Card split between Claude and Codex seats, or verifier-only for the sibling?
3. Which host owns the run (office assumed)?
4. Is N=3 per run and 320 min the right envelope, and how often (weekly after the stale mail)?
5. Does stage 3 (queue/dashboard) need its own decision record before any design work?
6. Who owns `raw.guides/scheduler/res/harness-check.md` — Atlas/Trajectory/Cartan (still unassigned)?

## 9. Not verified

Tier ordering of Codex models; exact tmux/headless flags and any `--max-turns`-style limits; whether
the per-card `recheck:` lists are complete enough to run unattended; per-run cost.
