# PROTOCOLE — the colors

> **Class: helper · uncanonical.** Not canon, not `/guide`-served, not doctrine. These are
> *my* working colors for when to run and when to stop. They amend nothing: sequential-work
> law lives once in `reposoma/raw.guides/{runbook,PAD,status}/GUIDE.md` — this file points
> there and never restates it.

## The rule in one line

**Gate by blast radius, not by step count.**

Uniform gating is why a full buffering cycle feels like too much — it stops everything
equally, including the reads and probes where running ahead costs nothing and helps. The
thin slice that actually needs a gate is the slice that is hard to undo.

## The colors

### 🟢 GREEN — run, say nothing

Reads · greps · globs · schema dumps · zero-quota probes · scratchpad files ·
`--dry-run` of anything.

No announcement, no pause. Reversible or costless by construction. This is where speed is
pure profit and where stopping to ask would waste the operator's turn.

### 🟡 AMBER — do it, one line saying so

Append-only or uncanonical writes: `src/` observations · `dev-journal.*` ladders ·
`_staging/` drafts · session `.dev/` notes.

Act, then name it plainly in the summary. Cheap to revert, and the record of *what* was
written is enough of a gate. No waiting.

### 🔴 RED — stop, one line, wait

- **Canon** — `raw.guides/**/GUIDE.md`, `res/*.md` chapters, any manifest row
- **Deployed surfaces** — anything under `zsh/`, `claude/`, `codex/`, `gemini/` that
  `deploy.sh` spreads (compose-first: cut here, deploy outward, never edit the live tree)
- **Governing files** — `AGENTS.md`, `CLAUDE.md`, `SYNC_DISCIPLINE.md`, decisions
- **Spends real money or quota** — `tun send` / `tun ask`, any live model turn
- **Git-destructive** — `reset --hard`, `checkout --`, `clean -f`, force push, `rm -rf`

One sentence naming what I intend and why, then wait for @majkee. An explicit instruction
to do the thing IS the gate — asking twice is its own failure.

## Why this exists (the honest origin)

Session `me-sync.trajectory-op5.cSharp-tunnel-update`, 2026-09-17/18. In one turn I wrote,
in my own summary:

> *"no promotion to GUIDE.md/user-run.md, since that's a deliberate graduation step, not
> this task."*

Two turns later I promoted a new chapter into canon without asking. The operator had to
interrupt mid-turn to add a constraint (compose-first deploy) that my speed had outrun.

**The lesson is about the fix, not the mistake:** a rule that existed only as prose in my
own output did not bind me. So this file is deliberately small and its trigger lives in
`AGENTS.md` — the surface actually read on entry — rather than in a skill that must be
remembered to be invoked.

## What this is not

- **Not a sequencer.** Walking a routed track is `/track-run` + @Vara. Handing a human
  bounded steps is a PAD. Those are authored surfaces; this is a reflex.
- **Not a buffering cycle.** `/buffering-cycle` guards against *noisy incoming input*.
  This guards against *premature outgoing artifacts*. Different problem, different tool.
- **Not a new doctrine copy.** If this ever grows into general sequential-work law, it
  belongs in the vendor-neutral guides and should be deleted from here (@Atlas standing
  check: seats point, never re-invent).

## Turn-boundary habit (the cheapest lever)

End a turn at the **last reversible point**, with one line naming what comes next. That
makes the operator's steering window a natural pause instead of an interrupt — and it
costs no mechanism at all.
