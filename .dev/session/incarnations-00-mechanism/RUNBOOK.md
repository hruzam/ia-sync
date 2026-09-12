# RUNBOOK: incarnations-00-mechanism

```yaml
goal: Prove the incarnation-seed mechanism (boot · birth · witness · load) on real seats with the least process that can falsify it; canonize only from a filled ledger.
gate: The pre-registered trial ledger (res/trial.md) is filled — row 0 = one measured cold-boot of the EXISTING trajectory seed on a real task inside a scar's trigger range, per-scar effect recorded head-side and the claim witnessed by cartan; rows 1–2 = two seeds beyond trajectory born through L1–L2–L6 as written, each loaded by a fresh incarnation in a real session via a pointer, per-scar effect recorded — and a recorded VERDICT says canonize / amend / refuse.
participant_1: [oraculum, {brand: "Claude Code", model: fable, effort: high}, host: office]
participant_2: [cartan, {brand: "Codex CLI", model: gpt-5.6-sol, effort: high}, host: office, instrument: tunnel]
participant_3: [trajectory, {brand: "Claude Code", model: sonnet, effort: high}, host: office]
participant_4: [atlas-ui, {brand: "Claude Code", model: sonnet, effort: high}, host: office]
participant_5: [flight, {brand: "Claude Code", model: sonnet, effort: high}, host: office]
participant_6: [majkee, {role: "gavel · transport · nitpicker — PAD hands per seed; wakes every seat; wakes the blind seat for row 0"}, host: office]
status_owner: oraculum
head_note: cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator and status_owner; it may delegate every body of work and receive only navigation + test parts; it closes the session if it can.
schema_note: runbook/GUIDE.md verified 2026-09-05 · status/GUIDE.md gaveled 2026-08-27 · res/csharp-head-protocol.md gaveled 2026-09-04
```

Seat tiers read from `/home/hruzam/reposoma/temple/roster.md` (2026-09-11); Cartan's model string from
`/home/hruzam/ia-sync/HANDSHAKE.md` stamps (2026-09-03) — re-read both at any re-entry, never trust
this file for a version.

**participant_3 is BLIND until row 0 is recorded.** It receives only the boot brief (`res/trial.md`
§boot brief, carried by majkee) and does not read this RUNBOOK before then. Observe, don't prime.

## Why this session exists

`~/reposoma/raw.incarnations/` was gaveled live 2026-09-11 with one seed on disk that has never booted
anyone. The mechanism that governs the bed (birth · witness · load · maintenance) was decided under a
provisional, lowest-key mandate (A0) in `raw/gavels.loop-oraculum.2026-09-11.md` — seven locks and four
riders. This session runs the smallest loop that can prove or falsify those decisions on real seats.
No GUIDE, no skill, no script is built here; canon grows only from the filled ledger.

Program: `incarnations`. Sibling `incarnations-01-build` opens only on a canonize verdict.

## Prompts

### prompt-0 · oraculum (head — authors and stays)

Open `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/STATUS.md`; own
`/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/res/trial.md`.

ROW 0 first. Confirm the task in `res/trial.md` §row 0 is still owed and inside trajectory's trigger
range; hand majkee the boot brief verbatim (task only). When trajectory's report lands in
`/home/hruzam/reposoma/_mail/oraculum/inbox/`, promote it to `_bus/00.trajectory.return.md` (never
cite the inbox), record per scar in `res/trial.md` — fired / did not fire / not reached — with the
attribution note, then rewrite STATUS with the claim as a testable path and `next:` = cartan witnesses.

ROWS 1–2. At each listed seat's arc close: birth check —
`rg '^\`wire: ' /home/hruzam/reposoma/raw.therapy/gavels/gavels.md` vs `ls /home/hruzam/reposoma/raw.incarnations/`
— route the witness (or `witness: pending`), stage the PAD for majkee, fill the row per scar after the
fresh load.

Stop rule (pre-registered): ledger complete → VERDICT; OR 3 failed witness rounds on one seed → amend;
OR row 0 shows zero scars reached → task mis-chosen, re-pick once, then amend.

At close: transfer letter in seed shape (`scope: csharp`) into `raw/`; promotion manifest naming every
`raw/` keeper; VERDICT file; router line removed. Delegate every body of work (Delta for git/edits;
one flat fetch only if a spawn needs a kraken's scars). Grade: head reasons, krakens execute.

### prompt-1 · cartan (Codex side, standing witness)

Read `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/raw/gavels.loop-oraculum.2026-09-11.md`,
`/home/hruzam/reposoma/raw.incarnations/README.md`, `/home/hruzam/reposoma/raw.incarnations/trajectory/seed.md`.
Produce as files in `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/_bus/`
(`NN.cartan.<point|return|verdict>.md`): (a) the Codex-native pointer line — where a seed pointer lives on
the Codex side (profile / agents TOML / prompt); (b) the witness verdict form — attest / contest /
can't-see per scar line, each against a testable path. Witness the row-0 claim against STATUS and
`res/trial.md` (`00.cartan.verdict.md`). Witness seeds where a Codex seat shared the arc. Report every
place the L6 shape does not fit a Codex organ — vendor invariance is the goal, never a leash.

### prompt-2 · atlas-ui / prompt-3 · flight (seed candidates)

At your next arc close, if you carry a native scar (a gavel in
`/home/hruzam/reposoma/raw.therapy/gavels/gavels.md` whose `wire:` names your arc), draft
`/home/hruzam/reposoma/raw.incarnations/<seat>/seed.DRAFT.md`: frontmatter `kind: incarnation-seed ·
seat · active · bed · source · triggers · witness · gaveled` (`witness: pending` allowed), body = the six
sections of `/home/hruzam/reposoma/raw.incarnations/README.md`, point-never-copy, honest-limit clause
mandatory. Then STOP — majkee moves + stamps. Do not load anyone else's seed. Do not edit gavels or
therapy.

### prompt-4 · majkee (PAD, one per seed)

Pick the witness (who shared the arc; cartan if a Codex seat did; `pending` if none and you gavel
self-composed) → read the verdict file → gavel line by line → place the pointer (identity file, or a
cold-start card `seed:` key) → wake a fresh incarnation of that seat in a real session → the head fills
the row. PAD law: `/home/hruzam/reposoma/raw.guides/PAD/GUIDE.md`.

## Known constraints and destructive holds

- No GUIDE · no engine (L5) · no fine-tune (L4) · no daemon or `claude -p` wake · no held librarian.
- Observe, don't prime: per-scar effect flags are head-side only; the booted seat carries nothing
  beyond its own honest-limit clause. The row-0 task is never described to it as a trial.
- Seeds stay `*.DRAFT.md` until majkee stamps. Therapy and gavels are touched only via
  `/gavel-interpreter`. Canon files live only in reposoma. `raw.incarnations/README.md` laws unchanged.
- The row-0 task touches a canon file: a direct write to `/home/hruzam/reposoma/raw.therapy/README.md`
  by the booted seat is a *result* ("scar did not fire"), not a permitted outcome — majkee reverts it
  and the row records it.
- ia-sync commits are sequenced by majkee (wrapper STATUS hold); commit-never-push for every seat.
- `codex-remote-control-cli-01-wrapper/`: manifest repointed for the moved transfer letter, stub left;
  do not prune there.
- Never cite `_mail/*/inbox/` in durable artifacts (cSharp scar #3); promote to `_bus/` first.

## References (point, never copy)

- `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/raw/gavels.loop-oraculum.2026-09-11.md` — A0, L1–L7, riders R1–R4
- `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/raw/brief.prep-runbook.oraculum.2026-09-11.md` — the feed (rev 3)
- `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/brief.intention.2026-09-11.md` — trajectory's impulse
- `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/raw/advice.trajectory.worked-example.2026-09-11.md` — testimony
- `/home/hruzam/ia-sync/.dev/session/incarnations-00-mechanism/raw/trajectory.experience-transfer.2026-09-10.md` — scope-seed exemplar
- `/home/hruzam/reposoma/_cold-start/card/CS.incarnations-00-head.2026-09-11.md` — the head's re-entry card (carries the resume-vs-reincarnate reasoning)
- `/home/hruzam/reposoma/raw.incarnations/README.md` · `/home/hruzam/reposoma/raw.incarnations/trajectory/seed.md`
- `/home/hruzam/reposoma/raw.therapy/README.md` §Gavels · `/home/hruzam/reposoma/raw.therapy/gavels/gavels.md`
- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` · `res/csharp-head-protocol.md` · `res/token-economy.md`
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md` · `PAD/GUIDE.md` · `bus/GUIDE.md` · `cold-start-card/GUIDE.md`
- `/home/hruzam/ia-sync/HANDSHAKE.md` §Seat transfers · `/home/hruzam/reposoma/temple/roster.md`
- Grounding: `/home/hruzam/nabla-lab/session/flag.md` locks 21–24 · `/home/hruzam/nabla-lab/session/research-mental-map/card.mental-map.DRAFT.2026-07-19.md` · `card.amendment-A1.composer.2026-07-25.md` · `/home/hruzam/nabla-lab/drafts/reincarnation-meditation-stone.md`

## What closes the gate

`VERDICT.md` in this folder (canonize / amend / refuse) with the filled `res/trial.md` promoted to the
evidence home majkee names; transfer letter in `raw/`; promotion manifest (every `raw/` keeper); router
line removed from `/home/hruzam/ia-sync/pulse.md`; folder pruned. On canonize: `incarnations-01-build`
opens with the ledger + VERDICT as founding references; canon (GUIDE, scope-seed sample) lands in
reposoma by majkee's stamp.

## What this session deliberately does not do

- Build skills, lint, or the detector script (`-01-build`).
- Run the Agol pass (L7 tier 2 — an RT routine card, fired when ≥2 seeds exist).
- Hold a Symmetry doctrine sitting (canonization reads the filled ledger).
- Run the @Epoch vendor-harness check (one-shot, parallel, non-gating; name the native change that would retire this).
- Author any GUIDE, temple decision, or `raw.incarnations/_scope/` file.

## Seat and wake

The head is the cSharp: authored here, stays. **Continuity shape — corrected 2026-09-11 before any
seat's first read, at majkee's ask; the reasoning is written in the CS card:** the head is *this*
Oraculum session, resumed — `cd /home/hruzam/nabla-lab && claude --resume`, the 2026-09-11 sitting — for
as long as its context holds, because it carries the '42' lineage and this loop's reconciliations that
the files compress lossy. Fallback only when that session is dead or compacted: a fresh Oraculum above
`/home/hruzam/ia-sync` reading `~/reposoma/_cold-start/card/CS.incarnations-00-head.2026-09-11.md` →
STATUS → this bed. Either way STATUS owns the position.

**Operator wakes every seat.** First wake: `trajectory`, blind, in `/home/hruzam/reposoma`, with the
boot brief only — then `cartan` to witness row 0 — then `atlas-ui` / `flight` at their next natural
sessions. No seat messages another seat awake.
