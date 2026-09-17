---
name: cold-start-card
description: Create a compact, evidence-backed session-glue card in the central vault ~/reposoma/_cold-start/ for a later session of any brand. Use when pausing, repairing, resuming, transferring, or closing work that needs exact project, commit, resume, authority, first-action, and verification context; use issue-card for known defects in the same vault. Schema of record raw.guides/cold-start-card/GUIDE.md.
---

# Cold Start Card

Leave the next session a precise re-entry point. The card points to durable sources; it
does not copy their full contents or the session transcript.

Read the current shared law at `~/reposoma/raw.guides/cold-start-card/GUIDE.md` and the
CS/routine schema at `~/reposoma/raw.guides/cold-start-card/res/cold-start-card.md` before
composing a card. These sources outrank this execution copy.

## Destination — the central vault

- Resolve the vault through `temple-project-map.zsh` → reposoma root → `_cold-start/`.
- Process card: `<reposoma>/_cold-start/card/CS.<slug>.<YYYY-MM-DD>.md`.
- Born routine (recurring task glue, dateless):
  `<reposoma>/_cold-start/routines/RT.<slug>.md`.
- The sibling `issue-card` skill writes caught issues into the flat top-level `issues/`
  category, or directly into `routines/` when recurrence is known from the start.
  Graduated recurring issues keep their dated `ISS.*` name in `routines/`; solved
  one-shots move to the shared `archive/`.
- Expand `~` to the user home before use; both hosts resolve to `/home/hruzam`.
- The vault is git-tracked in the reposoma repository. Do not stage or commit
  implicitly; report that the card is invisible on the other machine until committed.
- Folder is state: `card/` live, `archive/` read, `routines/` standing. Never edit or
  move another seat's card.
- A project-local card (for example `.dev/session/…`) is an explicit exception only
  when the user requests it; the vault is the default.

The cold-start vault and flat issue category are coupled: any future relocation moves
`_cold-start/` and `issues/` together in the same commit, never independently.

## Family-wide filename sorting

Dated `CS.*` and `ISS.*` cards sort by the `YYYY-MM-DD` substring in the filename, not
filesystem mtime. Extracting that date for ordering is distinct from inferring category:
frontmatter `kind:` remains the category truth. Surface a dated card without the filename
date in an `UNSORTED` bucket rather than guessing. Born `RT.*` routines are intentionally
dateless and exempt; a graduated `ISS.*` routine retains its date as “first seen.”

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
kind: cold-start-card
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
runbook: ~/<project>/<session-root>/<program>-<NN>-<phase>/RUNBOOK.md   # optional live bed
pointers:
  - ~/<durable source path>
---
```

Codex-specific evidence keys (session_id, rollout path, cli version, effort, worktree
tracked/ignored state, authority may_write/gated) go AFTER the shared block, still flat
where possible. Tooling parses only the shared contract. Skip empty keys; never invent
values.

Include `runbook:` only when that exact live session bed exists in the owning project. Omit it
when work has no live bed. Never use reposoma as a project session owner or fallback RUNBOOK
location; it holds the shared canon and card vault.

For a routine born as a routine, use a dateless `RT.<slug>.md`, omit `date:`, set
`kind: routine`, and add `origin: intended`. An issue that graduates into `routines/` is
folded by the `issue-card` lifecycle: keep its `ISS.<slug>.<YYYY-MM-DD>.md` name and catch
date, add `origin: issue`, and use optional `from_issue:` only when a fresh routine card
splits from the issue instead of moving it wholesale. Never rename a graduated issue to
`RT.*`.

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
