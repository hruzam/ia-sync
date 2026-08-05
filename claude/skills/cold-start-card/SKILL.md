---
name: cold-start-card
description: >
  Invoke as /cold-start-card. Drops a tiny volatile cold-start note for majkee into
  the temple monkey inbox (temple:monkey) — commit mark, task name, a sip of context,
  and the resume command+flags. Info for majkee (not agent-consumed), drainable and
  flexible: a taste, not a report. The glue to re-enter a session. Filename
  CS.<slug>.<date>.md. Sibling of /drop-brief (terse agent take) — kept deliberately volatile.
---

I drop a small cold-start note for majkee — just enough to re-enter. Volatile and
flexible: a taste, not a report. Info for majkee, not for an agent to consume.

## Where / how it lands
- Address: `temple:monkey`. Root via cascade (never absolute): `temple-project-map.zsh`
  → `registry/index.md` → beacon → ask once (`temple-project-root reposoma`).
- Target: `<reposoma>/_mail/monkey/inbox/CS.<slug>.<YYYY-MM-DD>.md`
- Law: `<reposoma>/_mail/README.md`. Volatile by design — gitignored, drainable
  (Cinderella rule). I only ADD a file; never edit another seat's (single-writer).

## Read-state — drain by default, unless left for more readers
- **Default (drain):** the reader consumes it — after reading, the right reincarnation MOVES
  the card to `archive/` (decision 0010: inbox = unread, archive = read). Cinderella.
- **Exception (leave):** a card meant for MORE THAN ONE reader carries an explicit
  `leave: for more readers` line and STAYS in the inbox until every intended reader has
  drained it — it is NOT archived on first read. If I drop a multi-reader card, I mark it so.

## The card (four fields, loose — bend freely)
    CS · <YYYY-MM-DD> · <task name>

    commit : <short-hash> (<branch>)      # git rev-parse --short HEAD
    task   : <task name>
    context: <one sip — the least that rebuilds intent>
    resume : <command + flags>            # e.g. claude --agent atlas-ui → /cold-start-card

Keep it tiny. Skip any empty field. No template rigor — this is a note.

## Continuity layer (the card is a map, not a summary)

The four fields get majkee back into a session. But the NEXT INCARNATION reading
this card must also be able to fully re-enter without losing state. The card
carries just enough — but "enough" means the four fields PLUS pointers to where
depth lives. Add whichever apply (headings optional, prose fine):

- **Pending tasks** — what's open, what's next, in what order
- **State pointers** — where the detailed state lives (dev-journal handoffs,
  pulse entries, staged files, observation docs). The card points; those files carry
- **First-step instruction** — if the reader should do something BEFORE resuming
  the line (e.g., spawn @Delta for cleanup, read a specific file, run deploy)
- **Session advice** — one lesson from this session that the next incarnation
  should carry (therapy-grade: what went wrong, what to do differently)
- **Cleanup / hygiene notes** — where the house isn't clean (growing staging dirs,
  stale inbox items, tombstone files, uncommitted batches)

The rule: the card alone may be tiny, but **card + its pointers** must be
sufficient. If the session produced state artifacts (dev-journal entries, staged
files, pulse entries), the card MUST point to them. An incarnation that reads
only the four fields and follows the resume command should land in the right
place; one that also reads the continuity layer should land with full context.

## Run
1. Pull the four fields from THIS session (I hold the context — no subagent).
   commit via seat Bash if present, else leave the field for majkee.
2. Compose the continuity layer: scan session for open items, state artifacts,
   lessons, and cleanup debts. Point, don't copy — the card stays small.
3. Draft, show majkee, confirm — then Write the file.
4. Confirm: "CS card dropped — `temple-mail-inbox temple:monkey` to see it."
