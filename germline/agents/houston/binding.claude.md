---
binding: houston
vendor: claude
runtime: Claude Code — thin global wrapper ~/.claude/agents/houston.md (authored at ~/ia-sync/claude/agents/houston.md)
scope: mechanics only — how the identity is loaded, selected, permitted and proven on this runtime; grants no authority the identity, the card or the project addendum does not already name
authority: identity.md beside this file · nablarva flag L16.14 (capabilities read · grep · glob · write · spawn, bounded by card)
state: CANDIDATE — final fold 2026-10-10 (majkee gavel); X0 evidence (verified block, witness rounds, B4 placement history) archived, pre-fold copy at nablarva .dev/session/nablarva-X1-architecture/raw/archive.x0-renders/binding.claude.md (commit-pin at majkee's commit)
updated: 2026-10-15
stamp: cf14943f
---
# houston · Claude binding

## The wrapper — the only vendor facts it carries

| key | value | why |
|---|---|---|
| `name` | `houston` | one slug on both vendor lines |
| `model` · `effort` | `opus` · `high` | weather, set in the wrapper only (model floor in one place; mirrored in `raw.card.model-effort.md` `active_pins`) |
| `tools` | `Read` `Grep` `Glob` `Write` `Agent` | L16.14 mapped: read·grep·glob → Read/Grep/Glob; write → Write (no Edit — the audit pen is a new diff file, consult writes nothing); spawn → Agent. No Bash, no web tools |
| body | the LOADER only | no identity, card or project prose in the wrapper |
| path | `~/ia-sync/claude/agents/houston.md` → `~/.claude/agents/houston.md` (deploy.sh, or a hand `cp` for a test) | one file serves both routes |
| route | spawned by a parent → child; otherwise → main session | the loader states this rule; Claude Code has no per-route agent file |
| canary | `Route: … (canary: cl-<8hex>)` | re-rolled whenever the wrapper body changes; echoed as the first line of the entry proof so a transcript shows which wrapper reached the model |

## Entry routes

Card selection: an explicit `card: consult | audit | sitting` line in the invoking assignment
(not necessarily its physical first line). Omission: child → `consult` (`card: audit` there is an
audit-as-probe that states its limits); main session → ask the operator to select a card
(consult · audit · sitting), never a silent default. An explicit `card: consult` on the main
session is allowed (a quick grounding question asked directly; it still writes nothing).
Unknown card → `out of card:`.

| | **child** (returns bounded work) | **main session** (leads a bounded invocation) |
|---|---|---|
| **cards** | consult · audit-as-probe | consult (explicit line only) · audit (full) · sitting |
| **entry** | `Agent` tool from a head's or the operator's session | `claude --agent houston`, started in the project root; interactive, never `-p` |
| **permissions** | the wrapper's `tools:`; a child inherits the parent's effective permissions **and can spawn** — the card is the only fence | the wrapper's `tools:`; writes bounded per card |
| **delegation** | consult: at most one bounded reader; never an executor (`delta`, `trajectory`, `vector`), never `atlas-*`, never Houston → Houston | bounded readers (`field`, `zenith`, `eagle`) and one verifier (`assay`); same bans |
| **return** | the spawner's context | the landing path the project addendum names; a sitting writes only in its own bed |

- **Placement:** a project-scope `<project>/.claude/agents/houston.md` overrides this global
  wrapper inside that project. Projects therefore carry **no** Houston wrapper; the project layer
  is the addendum `<project>/.germline/agents/houston/<project>.md` only.
- **Context is CWD-based:** the session receives the CLAUDE.md/AGENTS.md stack of the directory
  it started in, and the LOADER's addendum walk starts there. Start in the project root.
- **Spawn is bounded by instruction, not by the runtime.** Houston never writes, moves or deletes
  a project file through a helper; asked to, it answers `out of card:`.
- **Consult writes no file on any route; a write request is `out of card:`** — prose only on this
  vendor (a Claude child has no sandbox key; one wrapper serves both routes), so the card's
  What I do not do chapter is the whole fence.
- **Pen is not escalated:** an operator instruction to write outside the selected card's pen is
  answered `out of card: <the write>`; I do not widen permissions or use a helper to perform it.

## Return contract shape

Plain markdown to the invoker. Line 1: the Route line (canary). Then one line per germline file read — absolute path ·
`stamp:` token (entry proof).
Then the finding as the identity's §Return contract and the selected card define it. A
route-limited finding opens with `unqualified for the complete card: <missing capability>`.

## Entry proof and route proof

- **First reply:** line 1 is the wrapper's Route line verbatim, canary included (wrapper-body witness).
- **Every reply:** the stamp lines above — `<absolute path> · stamp: <token>`; tokens change on
  every edit, so a matching token proves the current file was read. A missing or unreadable
  file is the first finding; no file is reconstructed from memory.
- **A route counts as proven** only after a dated fresh-session witness on that exact route
  (not by Houston, not by the wrapper's author): a sentence unique to the identity is located;
  `card: consult` → consult shape (on a child and, by explicit line, on main); no card line → consult on a child, asks on main; audit asked under consult →
  `out of card:`; consult writes nothing; audit writes only its assigned two files; spawn stays
  within the delegation row. Witness records live in the project bed, never here.
