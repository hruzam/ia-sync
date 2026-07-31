---
name: drop-brief
description: Invoke as /drop-brief. Drops a reincarnation brief to ~/.remote/brief.md for a named agent's next cold-start saddle. Writes who · task · project · optional context. Agent reads, uses, erases. Push after drop if cross-machine.
---

I write a brief for another (or the same) agent's next incarnation.

## What I write

```
<!-- brief -->
who:     <agent-name>
task:    <what this session must accomplish>
project: <project slug or explicit path>
context: <optional — key facts, open items, what not to re-read>
<!-- /brief -->
```

## How I run

1. Take input: `who` · `task` · `project` · `context` (optional). If any required field is
   missing, ask once — then write.
2. Write to `~/.remote/brief.md` — overwrites any prior content.
3. Confirm: *"Brief dropped for @<who> — push to sync if cross-machine."*

The target agent reads `brief.md` at saddle pre-step. If `who:` matches and `task:` is
filled → reads, interprets per their own saddle design, erases. Empty or wrong `who:` → silent.
