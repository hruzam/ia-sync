---
title: JEV bed — proposed Flight carrier / Cartan head tunnel
date: 2026-10-12
author: cartan
status: operator accepted the head/carrier regime on 2026-10-12; transport not enabled
law: /home/hruzam/reposoma/raw.guides/tunnel/res/multi-seat.md
---

# Flight carries; Cartan remains the head

Yes: Flight can be majkee's visible conversation, carry bounded tasks through `_bus/` into
a stored Cartan/Codex thread, and bring back questions, gavels and hands-on steps. Cartan
works when called; it is not an always-running listener. Flight's wake/read cadence is a
separate, explicit arrangement. Jev does not need to exist for this transport to work.

```text
majkee ↔ Flight conversation
            ↕ authored _bus files + one-line tunnel calls
         Cartan stored Codex thread
            ↕ bounded implementation assignment after review
         Astrobley
```

## Fixed values and ownership

| Item | Proposed value |
|---|---|
| Host / working root | office / `/home/hruzam/ia-sync` |
| Bed | `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build` |
| One vault | `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/tunnel.head.state.json` |
| Head / STATUS owner | Cartan, as already fixed in RUNBOOK |
| Carrier | Flight, the existing operator-woken Claude session |
| Numbering after activation | Flight reserves the next unused bus cycle before dispatch; Cartan requests numbers for builder work |
| Builder | Astrobley, bounded spawn after the implementation hold is cleared; `impl/` and `tests/` only |
| Independent witness | Flight for implementation it did not author |
| Human | Majkee enables the table, resolves choices, handles interactive operations and approves each Jev send |

The shared multi-seat chapter's seats table calls the carrier “cSharp / status_owner” but
also says the carrier never advances STATUS. This bed's existing RUNBOOK explicitly gives
Cartan that role. Preserve that contract: **transport moves to Flight; STATUS ownership does
not move**. This proposed instance makes the mismatch visible for Flight's review rather
than silently changing roles. Cycle 01 keeps its current writers and outstanding VERDICT.

## A human decision travels as evidence

1. Cartan's RETURN identifies one needed human decision or hands-on step, its reason, the
   recommended choice, alternatives and what work depends on it. No question means `none`.
2. Flight shows that block verbatim or points to its file, then discusses it with majkee.
   Flight may explain or disagree, clearly labelled as Flight's assessment.
3. Flight carries majkee's actual words and date in its next POINT, distinguishing dictated
   answers from Flight's recommendation. No reply, a timeout or a checked artifact is not
   consent. The existing eight-question sheet retains its declared answer ownership.
4. Cartan checks the source, records the accepted disposition and updates STATUS. A gavel
   resolves the named choice; it does not silently authorize credentials, a paid call or GO.

For this bed the first decision source remains `raw/majkee-gavels.2026-10-12.md`. Flight can
take its questions one at a time; do not create a competing checklist. Human PAD operations
are returned as exact commands, expected observations and stop conditions. Flight returns
actual output as evidence, not “probably passed.”

## Before activation

Read RUNBOOK, STATUS, PLAN, cycle 01, the October 5 design, the October 12 gavel sheet and
Flight's VERDICT once available. Shared mechanics are in
`/home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md` and `res/multi-seat.md`.

The guide's gate is explicit: “Any Bash-capable seat may drive verbs AFTER the operator's
`open --enable`; no seat enables itself.” This document prepares that act; it does not perform it.
At authoring there is no vault here. Fixture tests pass 139/139; current-version live behavior
still needs one verified round-trip. See `raw/plan-check.2026-10-12.md` for the dated checks.

The current thread candidate is `01a0f5b9-b2ae-7392-af89-f434d5536d88`. Its recorded usage was
88.4% at the earlier October 12 probe. The later probe, after compaction/model change,
records 130608/760000 (17.2%) at `2026-10-12T21:52:49.199Z`, model `gpt-6.1-sol`, effort
`high`, approval `on-request`, reviewer `user`. Cartan accepts majkee's requested regime and
chooses this compressed continuation as the candidate. Recheck at handoff; no reset is
required by the earlier, now-superseded occupancy snapshot. A fork inherits history; it is
not a fresh context. The installed shim has `compact`; this preparation invokes neither
compaction nor fork and does not rely on the older “no in-thread trim” statement.

For an actual reset/transfer, prepare the head and carrier cold-start cards required by the
multi-seat re-entry chapter, pointing back to this bed; do not copy its doing-state. No reset
or transfer has occurred merely because this optional protocol has been written.

## Majkee's 2026-10-12 delegation instruction

Majkee explicitly allows Cartan, as tunnel head, to delegate bounded work back to Flight
even where an earlier RUNBOOK ownership restriction would otherwise prevent it. Apply this
instruction to this bed: Cartan names the task, exact permitted files, acceptance and return
path; Flight carries or executes it and may spawn its bounded helper. Ownership transfers
only for the named assignment, never by inference. Cartan remains cSharp and sole STATUS
owner; implementation witnessing still requires a seat that did not author that body.

The transport still points inward to Codex. Reverse delegation is a Cartan-authored POINT
or a requested follow-up in its RETURN, carried by Flight through files. It does not add
an outbound Claude API, unattended wakeup, or permission to spend a Jev request.

### Logging and context

Keep one ordinary Cartan logging spawn per active sitting. It reads the journal exemplar
and `.majkee` instructions itself, authors only Cartan's chapter for the actual local day,
and returns a small receipt. It logs this PLAN and later verified transitions by pointers.
Existing chapter bytes stay intact; operator checklist answers stay with majkee.

When the head's sandbox cannot write the external journal, the logger prepares an exact
append in this bed's `raw/`; Flight publishes that append after arranging the required
filesystem permission. A tunnel approval refusal is reported, not bypassed. Logging is a
task for an ordinary spawn, not a new global agent/binding.

An on-demand Codex reader can retrieve a specific question from an explicit source set and
return file/section/line citations, bounded excerpts and unresolved conflicts. Start with
STATUS/RUNBOOK/PLAN and targeted design sections; do not dump journals or whole rollout
histories into the head. No vector store, embedding service or standing RAG process is needed.
Verify that the resumed runtime exposes native spawn capability before depending on these
helpers; if absent, report the limitation and arrange a bounded carrier-side helper.

### Tunnel support on Flight's side

My choice is a bounded Flight child for routine transport diagnosis, using Flight's existing
Trajectory-like support capability. It receives one fault and owns only its assigned
`raw/flight-tunnel-support/` evidence file; Flight owns its bus RETURN. Its default work is
read-only: versions, explicit vault address, turn ID/status, lock-holder and effective-policy
checks. It may not call turn/enable/close/compact/fork/rebind, remove locks, change policy or
repair source without a new explicit assignment. Flight keeps ownership of tunnel verbs.

Heavy protocol/runtime defects return to Cartan as cited evidence for a separate bounded
engineering task. No support child is spawned before an actual support need. The carrier
cold-start card carries this brief; majkee relays it to Flight when opening this regime.

For the existing thread, **after this turn finishes and the interactive client releases it**,
the operator can use this command if choosing that candidate:

```zsh
TUNNEL_CODEX_STATE=/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/tunnel.head.state.json \
  zsh /home/hruzam/.config/zsh/ai/tunnel-codex.zsh open --enable \
  --thread 01a0f5b9-b2ae-7392-af89-f434d5536d88 --cwd /home/hruzam/ia-sync
```

That command binds an existing thread. Its model/sandbox/policy are inherited, not reset by
the command's defaults. Flight then resumes once, inspects `state.runtime`, and records the
effective policy. Keep the intended workspace-write/on-request policy; do not silently
choose never/full-access to bypass an unavailable approval conversation.

```zsh
TUNNEL_CODEX_STATE=/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/tunnel.head.state.json \
  zsh /home/hruzam/.config/zsh/ai/tunnel-codex.zsh resume
```

`tn-check` is a useful read-only diagnostic. A READY result alone is insufficient: the probe
reported no held writer lock even while this interactive conversation was active. Require
the operator's explicit release of that client. Never remove Codex writer-lock files.

## First call and ordinary cycle

Flight first reserves the next unused cycle and writes its POINT with exact read/write paths.
For the current-version live check, assign only: read the bed, report effective cwd/policy and
open holds, and write the named Cartan RETURN. Explicitly exclude implementation, credentials,
Jev HTTP and deployment. Writing that RETURN and obtaining matching streamed/read-back text
is the bounded live proof; fixture success alone is insufficient.

The wire message is one line, for example `Flight · cycle NN: read <absolute POINT path>.`
Replace NN/path with the actual file already written. Every agent shell invocation supplies
the same explicit state path. Flight preserves stdout/stderr and checks the exit code before
claiming delivery; Cartan's six-field RETURN stays the work record. Flight verifies the
claimed files and writes its own VERDICT. Never rewrite a handed-off cycle to add new work.

The required POINT question is “Name any refused command”; RETURN field 2 answers it, with
`none` valid. Behind this tunnel, an on-request escalation has no interactive approver and
may be declined. Report the exact refusal and leave the dependent step pending. Flight brings
the concrete operation to majkee or arranges an interactive sitting; it does not broaden
policy or claim success on Cartan's behalf.

## Serialization and recovery

- One vault, one carrier, one turn at a time. No TUI and tunnel work on the same thread at
  once; no second vault for that thread. Other seats use files unless explicitly given a
  settled carrier slot. Nothing here permits cross-host access to this thread.
- Unknown completion: `read` first. Match the requested turn ID and inspect status. Completed
  means recover the existing result; interrupted means decide a bounded continuation; unknown
  means hold. Never blindly resend after a timeout or kill a still-running driver.
- Exit 50: preserve both texts and inspect the read-back; do not silently pick/retry. Exit 61:
  wait for the existing turn. Exit 13: fix the missing state address, not the thread. Other
  errors follow the guide's read-before-retry rule.
- Observe the usage tail. Above about 80%, tell majkee; compact/reset is an operator choice.
  Preserve unfinished work and receipt paths before a handoff.
- A need for another Claude seat goes through Flight/operator and files. The tunnel reaches
  Codex; it does not wake Claude, inject keystrokes into a pane, or enable `claude -p`.

Closing/rebinding follows the guide and preserves the old thread ID. `close` removes the
local vault, not the Codex conversation. No lifecycle command is run by this planning step.
