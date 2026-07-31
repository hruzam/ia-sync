---
name: project-read
description: >
  Invoke as /project-read [project-name|path]. Standard project orientation pass — reads
  the harness in canonical order (AGENTS.md → flag → pulse → PROJECT.yaml), maps structure,
  and surfaces active phase, key locks, agent/skill set, and navigation patterns. Use before
  any work session on an unfamiliar project, or to brief a subagent. Optional argument: project
  name (key in temple-project-map) or explicit path. Defaults to CWD.
---

I orient any agent in a temple project. I read the harness in canonical order, map the structure,
and produce a compact orientation report — phase, locks, agent set, key paths, and ready-to-use
grep patterns.

## 1. Locate the project root

**If Bash is available** (via @Delta) — cheapest single call:
```bash
zsh -c "source ~/.config/zsh/ai/base.zsh && temple-project-root <project-name>"
```
Returns the physical path or exits non-zero if unknown.
**Special case — `nabla-lab`**: omitted from the map (subdir of reposoma).
Use: `temple-project-root reposoma` result + `/nabla-lab`.

**If Bash is unavailable** — cascade cheapest-first, stop at first hit:

| Step | Source | Action |
|---|---|---|
| 1 | `~/.config/zsh/ai/temple-project-map.zsh` (42 lines) | Read · Grep `\[<name>\]` · extract path from `="<path>"` |
| 2 | `reposoma/registry/index.md` | Grep project name · find table row · extract beacon path |
| 3 | `reposoma/registry/<project>.md` (beacon) | Read frontmatter `path:` field |
| 4 | Ask once | Name the project or path. If no response, stop. |

**Explicit path** (`/home/...` or `~/...`): skip cascade, use as-is.

**No argument**: use CWD. If CWD ends in `.devenv`, strip suffix and look for the app root
as a sibling directory.

---

## 2. Read the harness — in this order, always

Read each file if it exists. Note what you find before moving to the next.

| File | What it carries |
|------|----------------|
| `AGENTS.md` (or `CLAUDE.md` → `@AGENTS.md`) | The loop, hard rules, delegation table, seat map, routing |
| `.dev/flag.md` | Locked decisions — invariants no seat crosses without a gavel |
| `.dev/pulse.md` | Current state — **newest section is at the top** — active phase, open items, tabled work |
| `.dev/PROJECT.yaml` | Machine contract: stack, MCP wiring, agent list, devenv transport spec |

**If `.dev/` does not exist**: look for `flag.md` and `pulse.md` at the project root.
**For reposoma itself**: read `pulse.claude.md` (Houston/Flight state) and `pulse.atlas.md`
(Atlas state) — the seat-specific pulses replace a single `pulse.md`.

**Reading order is load-bearing.** AGENTS.md gives the rules. Flag gives the locks.
Pulse gives where we are. PROJECT.yaml gives the machine layer. Never invert this.

---

## 3. Structure overview

After reading the harness, get a structural picture.

**If the project is registered in temple-project-map** (has a key in that file):
```
/tree-snapshot <project-name>
```
Produces compact JSON, depth 4 by default, respects `.gitignore`. Use this before grepping —
knowing the tree shape prevents wasted searches.

**If not registered, or Bash unavailable**:
Infer layout from AGENTS.md or flag.md. Key signatures:
- `app/`, `resources/`, `routes/` + `composer.json` → Laravel project
- `.dev/`, `.claude/`, `experiments/` → temple harness present
- `src/` or `lib/` + `package.json` / `pyproject.toml` → generic project
- `_mail/`, `registry/`, `temple/` → temple meta-repo (reposoma pattern)

---

## 4. Sibling navigation

When the task requires crossing into a sibling project, follow the sibling graph — do not
cold-search.

**Find siblings for the current project:**
```bash
# From the beacon (read reposoma/registry/<project>.md)
grep "sibling-of:" reposoma/registry/<project>.md
# Also read ## Shared anchors section — it names exact entry points inside the sibling
```

**Resolve the sibling root:** run the same cascade from section 1 with the sibling name.
Most siblings are in temple-project-map.zsh — step 1 (Bash shortcut or file grep) is
usually sufficient.

**Scope the sibling read:** the `## Shared anchors` section in the origin beacon tells you
exactly which paths inside the sibling are the relevant entry points. Read those — not the
full harness — unless the task requires broader orientation.

**If delegating to @Eagle:** spawn Eagle with the sibling name directly:
> "Read sibling project `<name>` — focus on `<entry-point from Shared anchors>`"

---

## 5. Navigation patterns

Standard grep and list patterns — use these for all subsequent exploration.

**Harness lookups:**
```bash
# What is locked / decided
grep -n "LOCKED\|GAVELED\|DECIDED\|🔒\|decision:" .dev/flag.md | head -20

# Active phase and open items
grep -n "Phase\|TODO\|OPEN\|tabled\|pending\|next\|blocked" .dev/pulse.md | head -30

# Agents in scope for this project
ls .claude/agents/*.md 2>/dev/null

# Skills in scope
ls .claude/skills/*/SKILL.md 2>/dev/null
```

**Code lookups — Laravel / PHP:**
```bash
# Find a class
grep -rn "class <ClassName>" app/ --include="*.php"

# Find a route
grep -rn "'<route-name>'\|\"<route-name>\"" routes/ --include="*.php"

# Find where a method is called
grep -rn "-><methodName>(" app/ --include="*.php" -l

# Find a blade component
find resources/views/ -name "*.blade.php" | grep <name>
```

**Code lookups — generic:**
```bash
# Find a symbol across the codebase
grep -rn "def <name>\|function <name>\|const <name>\|<Name> =" src/ --include="*.py" --include="*.ts" --include="*.js"

# Find references to a concept in docs
grep -rn "<term>" . --include="*.md" -l
```

**Temple / reposoma pattern:**
```bash
# Find a decision
grep -rn "<keyword>" temple/decisions/ --include="*.md"

# Find a registry entry
grep -n "<project>" registry/index.md

# Check mail presence (lists filenames only — never reads content without asking)
ls _mail/<seat>/inbox/ 2>/dev/null
```

---

## 6. Key paths by project type

| Project type | Read-first paths beyond the harness |
|---|---|
| Laravel (freya / psdvsSys) | `routes/web.php` · `app/Models/` · `app/Http/Controllers/` · `.dev/flag.md` stack section |
| Playground (applications-in-common) | `.dev/hypotheses.md` (the H-ledger) · `experiments/` · `bricks/` |
| Temple meta (reposoma) | `temple/decisions/index.md` · `registry/index.md` · `pulse.claude.md` · `pulse.atlas.md` |
| Devenv repo (`*.devenv`) | `SYNC_DISCIPLINE.md` · `registry.json` (use `/devenv-sync` instead of this skill) |
| Research / lab (nabla-lab) | `flag.md` · `session/` · `_mail/` presence scan |

---

## 7. Orientation report

Surface this compact summary after completing steps 1–4:

```
── project-read: <project-name> ──────────────────────
Root:          <resolved path>
Stack:         <from PROJECT.yaml, or "not declared" if absent>
Active phase:  <newest section heading in pulse.md>
Open items:    <top 3 from pulse.md pending/tabled/open lines>
Locked decisions (count): <N from flag.md>
  Top locks:   <2–3 one-liners from flag.md headings>
Agents in scope: <list from .claude/agents/, or "none">
Skills in scope: <list from .claude/skills/, or "none">
Recommended next read: <whatever AGENTS.md names as the read-first path, if any>
──────────────────────────────────────────────────────
```

Then ask: **"What do you need — read a specific area, grep for something, or start work?"**

---

## Rules

- Read the harness in the stated order. Never skip flag.md or pulse.md.
- pulse.md is **newest-first** — the top section IS the current state. Read the whole file
  only if you need history.
- Flag.md locks are invariants — surface them, never cross them without a gavel.
- If PROJECT.yaml is absent, note it: the project may be pre-bootstrap.
- This skill is **read-only**. If Bash is needed for grep/ls/tree-snapshot, spawn @Delta.
- Do **not** carry project state from one project into another — always re-read fresh.
- If a project has a project-specific context skill (e.g. `/freya-context`), prefer it —
  it carries the baked stack snapshot. Use `/project-read` when no such skill exists.
