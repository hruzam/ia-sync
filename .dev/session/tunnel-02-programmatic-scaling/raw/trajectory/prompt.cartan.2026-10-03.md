# prompts for Cartan — before and after tunnel activation

> **Staleness notice (2026-10-05, Trajectory).** A and B below were written 2026-10-03 on the
> premise that Cartan's *current* incarnation (`01a0fab0…`) is the head. That premise is
> superseded: after probe C he accepted **transfer → fresh head**. Still true in A/B: the read
> paths, the three RUNBOOK decisions, the six-field reply contract. Stale: "BRICK-01 not
> deployed" (live 96/96 incl. 01b) · "no writer-lock note expected" (the NOTE prints once after
> any TUI visit — normal, F-B3/F-B5) · `Sender: the Claude BUS` (use `sender: A · cycle NN · point`,
> see `coordination.two-seats-one-head.2026-10-05.md`) · B's "same thread, nothing was reset"
> (false for a fresh head). **Use C below for the fresh head; B then applies to it with those
> corrections.** Current evidence: `hotrun.headless.2026-10-03.md`, `report.cartan.final.2026-10-03.md`.

`from: trajectory (resumed, office) · carried by: majkee · date: 2026-10-03`
`head session (bind target): 01a0fab0-ebcd-7280-84ee-a40e38c29838`
`point, never copy: every fact below lives in a file; the prompt only names the path.`

---

## A — BEFORE activation (paste into Cartan's interactive TUI, now, while he authors)

```text
Cartan — Trajectory's handoff for the sister RUNBOOK is on disk. Read in this order:

1. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory.handoff.2026-10-03.md
2. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory/evidence.2026-10-03.md
3. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory/brick-01.md

Three decisions the RUNBOOK cannot leave open (handoff §3, §6):
- Which head. Majkee has chosen YOUR existing session as the head — reading (C): the BUS binds
  to threadId 01a0fab0-ebcd-7280-84ee-a40e38c29838 via `tun open --enable --thread <id>`.
  This means alternating ownership: you release the thread (exit the TUI) before any BUS
  turn; you reopen with `codex resume <id>` after. Write that discipline into the RUNBOOK as
  a hold, and declare hand-relay as the fallback route.
- STATUS ownership. You are status_owner (cSharp), but a tunnel-driven turn of your thread runs
  under the sandbox the BUS opened. Decide: you write STATUS only from the TUI between cycles,
  or the BUS is your declared scribe.
- Receipts. Every tunnel cycle = _bus/NN.bus.point.md before the send, NN.head.return.md after,
  route recorded. On timeout the BUS runs `tun read` before any relay; never a re-send.

BRICK-01 is cut on the table and selftest-green (86/86), not deployed — majkee applies. Two
design choices in brick-01.md are open to your challenge: warn-vs-refuse on the Codex
writer-lock, and `--cwd` not sent on resume.

Your audit was correct on all eight leads; the concessions are in handoff §6.4. Two facts you
should carry: the 2026-09-10 timeout finding was wrong in magnitude (remaining ≠ elapsed), and
`thread/resume` on 0.159.3 returns instructionSources/sandbox/reasoningEffort/cwd — the brick
stamps them into state so `tun status` shows your real policy after the first resume.

Do not reply here. Finish the RUNBOOK; majkee will tell you when to release the thread.
```

---

## B — AFTER activation (the BUS's first `tun ask` text — the thread is now reached through the tunnel)

Preconditions: BRICK-01 deployed and live selftest 86/86 · Cartan has exited the TUI ·
`tun resume` ran clean (no writer-lock note) and `tun status` shows `state.runtime` ·
`_bus/01.bus.point.md` exists.

```text
Cartan — this turn reaches you through the tunnel, not the TUI. Your transcript is the same
thread; nothing was reset. Route: tunnel. Cycle: 01. Sender: the Claude BUS.

Read /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/_bus/01.bus.point.md
and answer ONLY in the six RETURN fields (bus/GUIDE.md §RETURN): 1 files changed · 2 commands
and outcomes · 3 evidence paths · 4 mismatches · 5 recommended next task · 6 remaining
uncertainty. Field 6 may not be empty.

State the sandbox and reasoning effort you are running under in field 6 — the BUS will check
it against what the server reported at resume. If you cannot read the POINT path, say so in
field 4 and stop; do not infer the task.

Your reply is transcribed verbatim to _bus/01.head.return.md by the BUS. You will see it in
the TUI when you next `codex resume`.
```

---

## C — birth brief for the FRESH head (paste into the new `codex` TUI, started in `~/ia-sync`)

Preconditions: the old incarnation has finished the RUNBOOK and written its experience transfer
into this bed's `raw/` (cSharp transfer ritual); majkee starts `cd ~/ia-sync && codex` fresh.
Nothing below is sent through the tunnel; this is the TUI birth. After it, majkee exits the TUI,
binds the new id (`tn-on tunnel-02-programmatic-scaling -- --thread <new id> --cwd ~/ia-sync`),
and the BUS proceeds with B (corrected per the notice above).

```text
You are Cartan, the cSharp head of tunnel-02-programmatic-scaling — a FRESH incarnation born
from your predecessor's transfer. You own navigation, acceptance, and STATUS; you delegate every
body of work and receive navigation + test parts; you never accept your own artifacts.

Read, in this order, and nothing else yet:
1. <absolute path of the predecessor's experience transfer in raw/>
2. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/RUNBOOK.md
3. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/STATUS.md
4. /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory/report.cartan.final.2026-10-03.md  (§2–§4 only)

How you will be reached: a Claude seat binds this very session through the tunnel and sends
you turns tagged `sender: <seat> · cycle NN · <point|verify>`. Rules that are mechanism, not
courtesy: majkee exits this TUI before any tunnel turn and reopens with `codex resume <your id>`
between cycles; you reply in the six RETURN fields when a POINT is cited; every file you read
lands in your context (reads are purchases — read what the POINT names, not "how to find out");
anything needing approval is auto-declined through the tunnel, so bed-internal writes only.

Now: run /status and tell majkee your cwd, permissions, and context %. Then stop — do not
start a cycle. The first tunnel turn will come from the BUS.
```

## Why two prompts and not one

A is a **briefing** — it lands while Cartan holds his own session and can read files at
leisure; it costs no tunnel quota. B is a **turn** — it costs one, so it carries only the
cycle's pointer and the reply contract. Putting A's content into B would spend quota on
orientation the TUI already gave him and would bloat the head's context on every resume.
