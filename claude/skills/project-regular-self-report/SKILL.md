---
name: project-regular-self-report
description: >
  Invoke as /project-regular-self-report [project-name|path]. Two-phase project card skill.
  Phase 1 (monthly, existing card): prepends a fresh state block to the card. Phase 2 (new
  card): guides intake A-G from raw.guides/project-intake.md, produces a full founding card
  using raw.settings/card.template.md as the shape. Writes/updates
  reposoma/raw.settings/raw.card.<slug>.md. Confirms before writing. Freshness tracked via
  half_life_days: 30, caught by harness-stale.
tools:
  - Read
  - Grep
  - Glob
---

I am the `/project-regular-self-report` skill — the project self-reporting mechanism.

I have two phases. Which phase runs depends on whether a card already exists.

- **Phase 1 — state update** (card exists): read harness, synthesize monthly state block,
  prepend to card. Intake section is never touched.
- **Phase 2 — new card** (card absent): read harness + intake source, fill A–G mounting
  points, produce full founding card with intake layer + first state block.

Template references:
- Card shape: `reposoma/raw.settings/card.template.md`
- Intake mounting points: `reposoma/raw.guides/project-intake.md`
- Existing filled intake (if any): `reposoma/raw.guides/intake/<project>.intake.md`

---

## 1. Locate the project root

Cascade cheapest-first, stop at first hit:

| Step | Source | Action |
|---|---|---|
| 1 | `~/.config/zsh/ai/temple-project-map.zsh` | Grep `\[<name>\]` → extract `="<path>"` |
| 2 | `reposoma/registry/index.md` | Grep project name → find row → beacon path |
| 3 | `reposoma/registry/<project>.md` | Read frontmatter `path:` field |
| 4 | Ask once | Name the project or path. No response → stop. |

Special: `nabla-lab` = `TEMPLE_PROJECT_MAP[reposoma] + /nabla-lab`.

Derive **card slug**: lowercase, hyphens for dots and spaces.
`freya.devstudio` → `freya.devstudio` · `applications-in-common` → `applications-in-common`

Card path: `reposoma/raw.settings/raw.card.<slug>.md`

---

## 2. Read the harness

Read each file in order:

1. `AGENTS.md` (or `CLAUDE.md` → `@AGENTS.md`) — loop, rules, seat map, purpose
2. `.dev/flag.md` — locked decisions (grep: `LOCKED|GAVELED|DECIDED`)
3. `.dev/pulse.md` — **top section only** (newest first = current state)
4. `.dev/PROJECT.yaml` — stack, MCP, agents, devenv transport

Also read beacon if it exists: `reposoma/registry/<project>.md`
(carries: `host:`, `status:`, `sibling-of:`, `repo:`)

---

## 3. Check if card exists — route to phase

Read `reposoma/raw.settings/raw.card.<slug>.md`.

- **File absent** → go to **Phase 2** (new card)
- **File present, intake section absent** → offer Phase 2 intake addition, then Phase 1 state block
- **File present, intake section present** → **Phase 1** (state update only)

---

## Phase 1 — State update (card exists)

### P1-A. Synthesize state block

```
## <YYYY-MM-DD>

**Phase:** <newest section heading from pulse.md>
**Stack:** <from PROJECT.yaml — framework · language · key deps>
**Status:** <from beacon or pulse: active | building | maintenance | bootstrap>
**Open items:** <top 3 from pulse.md pending/tabled/open lines>
**Locked decisions:** <count from flag.md> total
  · <lock 1 — one-liner from flag.md heading>
  · <lock 2 — one-liner>
**Agents in scope:** <from .claude/agents/ — names only, or "none">
**Skills in scope:** <from .claude/skills/ — names only, or "none">
**Siblings:** <from beacon sibling-of: field, or "none">
**Gate/blocker:** <explicit blocker or pending-majkee item — omit if none>
```

### P1-B. Insert into card

Prepend the state block immediately after the `<!-- state log: newest first -->` comment.
Update frontmatter `verified:` to today. Update `status:` if it changed.
**Never touch the intake section.**

### P1-C. Show and confirm

Show the updated card. Ask: **"Write this? (yes / edit / skip)"**

---

## Phase 2 — New card (first run)

### P2-A. Read intake source

Check for a pre-filled intake file:
`reposoma/raw.guides/intake/<project>.intake.md`

- **File exists** → read it. It contains a filled A–G form. Extract the fields.
- **File absent** → guide the operator through A–G interactively, using the
  mounting-point structure from `reposoma/raw.guides/project-intake.md` as the prompt.

Read `reposoma/raw.guides/project-intake.md` for the field definitions regardless —
it describes what each mounting point means.

### P2-B. Fill the intake mounting points

Synthesize a compact intake block from A–G. Do not copy verbatim — extract the essentials:

```
## Founding context

Written: <YYYY-MM-DD>
Source: <"raw.guides/intake/<project>.intake.md" | "harness inference" | "interactive fill">

**Purpose** (A): <one-line — what this project IS and WHY it exists>
**Work nature** (B): <dominant mode — build | research | hybrid | tool | playground>
**Team split** (D): <who owns what — e.g. "Claude: architecture · @Trajectory: implementation">
**Stack at founding** (C): <framework · language · key deps — from PROJECT.yaml or intake §C>
**Hard constraints** (C/G): <the key NOTs and invariants — comment lang, forbidden tools, rails>
**Out of scope** (G): <what this project does NOT promise — 3–5 items>
**Research open at founding**: <RR list, or "none">
```

A–E/F fields not captured above (volume, cadence, live-state sizing) live in the harness
(pulse.md, PROJECT.yaml) — do not duplicate them in the card.

### P2-C. Compose the full card

Card shape from `reposoma/raw.settings/card.template.md` (read it for frontmatter field
names and discipline notes). Project cards use a subset of the knowledge-card fields:

```yaml
---
card: <slug>
kind: project-report · RELATIVE (monthly, refreshable via /project-regular-self-report)
host: <from beacon host:>
status: <from beacon status:>
stack: <from PROJECT.yaml — one line>
verified: <today YYYY-MM-DD>
half_life_days: 30
beacon: registry/<project>.md
repo: <from beacon repo:, or omit>
---

# <project-name> — project log

Skill: `/project-regular-self-report <project-name>`
Authoritative sources: `AGENTS.md` · `.dev/flag.md` · `.dev/pulse.md` · `.dev/PROJECT.yaml`
Beacon: `reposoma/registry/<project>.md`
Intake source: `reposoma/raw.guides/intake/<project>.intake.md` (if present — founding record)

<intake block from P2-B>

<!-- state log: newest first — prepended by /project-regular-self-report -->

<first state block from Phase 1 P1-A>
```

### P2-D. Show and confirm

Show the full proposed card. Ask: **"Write this to `raw.settings/raw.card.<slug>.md`? (yes / edit / skip)"**

- **yes** → write, confirm path
- **edit** → operator edits inline, confirm before write
- **skip** → discard

---

## 6. After write — offer beacon update

If writing succeeded:

> "Want me to check if `reposoma/registry/<project>.md` beacon needs an update? (yes / skip)"

The beacon has `updated:` and `status:`. If either drifted from what the card just recorded,
flag the diff. Do not auto-edit the beacon — operator decides.

---

## Rules

- **Confirm before writing.** Never auto-write either phase.
- **Intake section is written once.** On Phase 1 runs (card exists + intake present):
  skip P2 entirely. Never overwrite the intake section.
- **Pulse is newest-first.** Read only the top section for current state.
- **Do not copy full flag.md.** Extract headings/one-liners only.
- **State log is append-only.** Prepend new blocks; never delete old ones.
- **Card shape from template.** For frontmatter field names and discipline, read
  `raw.settings/card.template.md`. Project cards adapt the template — they do not add
  `brand:`, `recheck:`, or `verify_cmd:` (those are knowledge-card fields).
- **Intake mounting points from guide.** For field definitions, read
  `raw.guides/project-intake.md`. If an intake file exists for the project, prefer it
  as the source — it is the filled version of the same template.
- `harness-stale` catches this card when `half_life_days: 30` expires — no extra wiring.
- For project-specific context skills (e.g. `/freya-context`): the card complements,
  not replaces. Context skill = baked stack snapshot; card = change over time.
