---
name: cold-start-card
description: Create a compact, evidence-backed session-glue card in the central vault ~/reposoma/_cold-start/ for a later session of any brand. Use when pausing, repairing, resuming, transferring, or closing work that needs exact project, commit, resume, authority, first-action, and verification context; use issue-card for known defects in the same vault. Schema of record raw.guides/cold-start-card/GUIDE.md.
---

# Cold Start Card

Leave the next session a precise re-entry point. The card points to durable sources; it
does not copy their full contents or the session transcript.

Schema and lifecycle of record: `~/reposoma/raw.guides/cold-start-card/GUIDE.md`. On
conflict between this skill and that guide, the guide wins.

## Destination — the central vault

- Process card: `~/reposoma/_cold-start/card/CS.<slug>.<YYYY-MM-DD>.md`
- Routine card (recurring task glue, dateless): `~/reposoma/_cold-start/routines/RT.<slug>.md`
- Issue category: `~/reposoma/_cold-start/issues/{open,parked,archive,reactions}/`,
  written by the sibling `issue-card` skill. Dated instances are `ISS.*`; dateless
  recurring reaction playbooks are `IR.*`.
- Expand `~` to the user home before use; both hosts resolve to `/home/hruzam`.
- The vault is git-tracked in the reposoma repository. Do not stage or commit
  implicitly; report that the card is invisible on the other machine until committed.
- Folder is state: `card/` live, `archive/` read, `routines/` standing. Never edit or
  move another seat's card.
- A project-local card (for example `.dev/session/…`) is an explicit exception only
  when the user requests it; the vault is the default.

The cold-start and issue locations are coupled: any future vault relocation moves
`_cold-start/` and its `issues/` subtree together in the same commit, never independently.

## Family-wide filename sorting

Dated `CS.*` and `ISS.*` cards sort by the `YYYY-MM-DD` substring in the filename, not
filesystem mtime. Extracting that date for ordering is distinct from inferring category:
frontmatter `kind:` remains the category truth. Surface a dated card without the filename
date in an `UNSORTED` bucket rather than guessing. Dateless `RT.*` routines and `IR.*`
reaction cards are intentionally exempt.

## Capture the frame

1. Resolve the current repository, applicable `AGENTS.md` chain, host, branch, HEAD,
   upstream, tracked and ignored project state, recent relevant commits, sandbox/write
   boundary, and any repository-defined state or transport files.
2. Run the bonded entry point `bash scripts/capture-context.sh --cwd "$PWD"` from this
   skill directory. Treat its JSON as candidate evidence and verify surprising or
   task-critical fields directly.
3. If the runtime exposes an active goal or plan, record its status. A Codex rollout
   JSONL is a track file, not project canon: point to it, session ID, model, and
   effort, but never copy transcript content.

Do not inspect or include `.env`, credentials, authentication state, prompt history,
full environment dumps, database contents, or remote URLs containing credentials.

## Compose the card

Write the shared cross-brand frontmatter block FIRST, flat, exactly these keys. Every
path is whole and `~`-anchored (`~/path/to/target`); never bare-relative, never a
literal `/home/<user>` prefix.

```yaml
---
kind: cold-start-card            # cold-start-card | routine
date: <YYYY-MM-DD>
brand: codex
seat: <seat or agent name>
project: <origin project registry key per temple-project-map>
projects: [<a>, <b>]             # optional — cross-project span
root: ~/<whole path to project root>
commit: <short SHA> (<branch>)
task: <one sentence objective>
resume: <command + flags for the next session>
model: <sol | terra | ...>       # thinking level the continuation deserves
dedicated: <recommended seat/agent>
recommend: <author's one-line steer>
runbook: ~/reposoma/_runbook/<project>/<slug>/RUNBOOK.md   # optional
pointers:
  - ~/<durable source path>
---
```

Codex-specific evidence keys (session_id, rollout path, cli version, effort, worktree
tracked/ignored state, authority may_write/gated) go AFTER the shared block, still flat
where possible. Tooling parses only the shared contract. Skip empty keys; never invent
values.

**Master prompt (optional)** — use the runbook grammar exactly, so blocks lift verbatim
into `RUNBOOK.md` files and the palette reveals them without opening the card:

```markdown
## prompt-0

###### prompt

​```text
<master prompt for the next session>
​```
```

**One-authority law:** the card is a transfer pointer, never a second doing-state. If a
live session bed exists (a `STATUS.md` for an open gate), point to it in `pointers:` and
carry no competing next-action — STATUS owns the position (`raw.guides/runbook/GUIDE.md`:
two files are allowed, two authorities are not). Include a `Repair queue` only when no
live bed exists.

**Body** — add only the sections that carry continuity:

- `Read first`: ordered sources and why each matters.
- `Observed state`: expected versus observed facts, including unexplained curvature.
- `Repair queue`: bounded items with acceptance evidence; mark completed work so it is
  not repeated.
- `First tool shot`: one safe, copyable read-only command block. Prefer `rg`,
  `rg --files`, targeted `git`, and the included context script over recursive dumps.
- `Gates`: decisions or mutations requiring the user.
- `Done when`: concrete checks, including any fresh-session smoke test.

Keep claims distinguishable as `observed`, `reported`, or `inferred`. Include exact
commits and whole `~`-anchored paths. Do not claim authorship for state that appeared
externally during the session.

## Write and validate

Show the destination and scope before writing. Then:

1. Parse the YAML frontmatter.
2. Confirm every local pointer exists or label it intentionally absent/external.
3. Re-run critical read-only commands and compare expected with observed output.
4. Report the created path, that a commit is needed for cross-machine visibility, and
   any gated action not performed.

## Lifecycle

The reader who consumed a CS card moves it `card/` → `archive/`. A card intended for
more than one reader carries `leave: for more readers` and stays until all have drained
it. RT cards never move.
