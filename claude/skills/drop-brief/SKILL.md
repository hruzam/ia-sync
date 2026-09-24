---
name: drop-brief
description: Invoke as /drop-brief <who> "<task>" [project]. Drops a reincarnation brief for a named agent's next cold-start saddle — YAML frontmatter (who · task · project · dropped · push) plus four markdown chapters (Context · Open items · Do not re-read · Expected output). The agent reads it at saddle, uses it, writes the resting state back. Push after drop if cross-machine.
argument-hint: <who> "<task>" [project]
disable-model-invocation: true
---
I write a brief for another (or the same) agent's next incarnation. The frontmatter is the
order; the chapters are the context. Most of the brief lives BELOW the frontmatter.

## Where — the one path constant

`BRIEF = ~/.remote/brief.md`. If the remote-hub box is ever retired, this line changes and
nothing else in the protocol does.

## What I write

```
---
who:      <agent-name>            # required — the saddle matches on this
task:     <one line — the order>  # required — non-empty = brief is live
project:  <slug | absolute path>  # required
dropped:  <YYYY-MM-DD · by>
push:     yes | no                # yes = cross-machine: push remote-hub after the drop
---
## Context
<key facts the seat cannot read fast — or must not spend tokens rediscovering>

## Open items
<threads the seat inherits — one line each, pointing to their home>

## Do not re-read
<what is already digested — files, mails, decisions — so the seat skips them>

## Expected output
<the return contract — what the seat hands back, and where>
```

The four chapters are fixed: same names, same order, any may be short, none is renamed.
Point, never copy — a chapter names a path, it does not paste the file.

## Resting state — verbatim, what the taker writes back

```
---
who:
task:
project:
dropped:
push:
---
```

No body. Frontmatter starts at line 1 — no comment lines above it; the how-to lives in
`~/.remote/README.md`, not in the brief.

## How I run

1. Take input: `who` · `task` · `project` (required) and chapter content (optional). A required
   field missing → ask once, then write. No chapter content → ask once *"chapters, or order-only?"*
   — an order-only brief (frontmatter, empty chapters) is legal.
2. Write `BRIEF` — overwrite whatever is there.
3. Confirm: *"Brief dropped for @<who>"* — and if `push: yes`: *"push remote-hub now."*

## The take rule — what the reading agent does (its saddle points here)

At saddle pre-step: read `BRIEF`. `who:` matches AND `task:` is non-empty → use it, interpret
per own saddle design, then write the resting state back. Otherwise → silent.
