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

## The card (four fields, loose — bend freely)
    CS · <YYYY-MM-DD> · <task name>

    commit : <short-hash> (<branch>)      # git rev-parse --short HEAD
    task   : <task name>
    context: <one sip — the least that rebuilds intent>
    resume : <command + flags>            # e.g. claude --agent atlas-ui → /cold-start-card

Keep it tiny. Skip any empty field. No template rigor — this is a note.

## Run
1. Pull the four from THIS session (I hold the context — no subagent).
   commit via seat Bash if present, else leave the field for majkee.
2. Draft, show majkee, confirm — then Write the file.
3. Confirm: "CS card dropped — `temple-mail-inbox temple:monkey` to see it."
