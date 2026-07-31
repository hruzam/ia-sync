# Guide: Regime Session Protocol

`~/.config/zsh/guides/guide-regime-session.md`

_Extracted from session 2026-07-20 (Flight · Medusa · system/tailscale build). This is a
developing standard — it will sharpen with each regime session that runs through it._

---

## What is a regime session?

A regime session is a build that happens **outside a project's normal flow** — typically
a shell config scope, a tool, a protocol, or infrastructure that serves the whole crew.
It is run interactively with majkee in the seat. It is not a project sprint; it is
operator + Flight building together, with krakens for execution.

---

## Protocol: Medusa (default for structured builds)

```
Flight (main seat, Sonnet / Opus as needed)
  ├── Oraculum (on hold — spawn when design complexity rises)
  └── Krakens: Delta / Vector / Trajectory (coding execution via _drop)
```

**When to use Medusa:** structured, sequential build. One seat driving. Krakens for code.
**When to use Octopus:** project sessions — Medusa head, persistent tentacles (Eagle · coders) held on line via SendMessage; buffer: stream.md manned · program.pulse.md batch (law 0012).
**When to use Sea-Pen:** research-first — Oraculum/Houston plans, Vara/Flight executes.

---

## The loop

```
1. Receive task
2. Orient (read scope harness — AGENTS.md · README · relevant guides)
3. Drop task in _drop/ if implementation is needed → delegate to krakens
4. For design questions → spawn Oraculum or Houston, hold line
5. Build together with majkee in seat
6. Close with sequential test (blessing card)
7. Compress session → pulse.flight.md entry + this guide updated if new pattern emerges
8. ia-sync when blessing is green
```

---

## _drop convention

Location: `applications-in-common/.dev/session/_drop/<date>-<scope>-<task>.json`

**Drop before executing.** Eagle/Flight working alone on coding = protocol violation.
Drop the task, let Delta/Vector/Trajectory execute, report back.

Minimum shape:
```json
{
  "dropped": "YYYY-MM-DD",
  "dropped_by": "<seat>",
  "for": "flight",
  "scope": "<what scope is affected>",
  "summary": "<what needs doing>",
  "context": "<links to harness, guides, relevant files>"
}
```

Post-hoc drops (work already done, logging for record) must mark:
```json
"type": "post-hoc — work executed by <seat> directly (violation noted)"
```

---

## Blessing card pattern

Every feature close requires a blessing card before ia-sync.

**Two files, one scope name:**

| File | Purpose |
|---|---|
| `~/.config/zsh/blessings/<scope>.json` | Machine-readable: commands, expect values, status |
| `~/.config/zsh/blessings/<scope>.md` | Human checklist: operator runs top to bottom |

**JSON shape:**
```json
{
  "scope": "<scope-name>",
  "session": "YYYY-MM-DD",
  "authored_by": "<seat>",
  "description": "...",
  "checks": [
    {
      "id": "01",
      "label": "short label",
      "command": "the bash command",
      "expect": "what to see",
      "status": "pending",
      "note": "optional — extra context"
    }
  ]
}
```

**Status values:** `pending` → `pass` / `fail` (operator fills in during run).

**MD shape:** plain checklist, mirrors JSON checks, ends with:
_"All checked → scope blessed. Uncheck = flag to Eagle or Flight before syncing."_

**Gate:** do not run ia-sync until all checks are `pass` or explicitly waived by operator.

---

## Scope build conventions (zsh config)

Applies to: `~/.config/zsh/system/` · `~/.config/zsh/ai/` · any scoped subfolder.

**Law:** `~/.config/zsh/guides/guide-for-builder.md §Architecture rules`

Quick rules:
- One `keyboard.zsh` per scope — **aliases and comments only**
- Function bodies in scope-named engine (`<scope>.zsh`)
- Help function `_<scope>_help` mandatory — `<scope>-help` alias in keyboard
- Scope `README.md` mandatory — file map + command surface + 3-step "how to add" + pending audit items
- `zsh -n <engine>.zsh && zsh -n keyboard.zsh` before commit

---

## Session compression format

At session close, Flight prepends to `pulse.flight.md`:

```markdown
## [YYYY-MM-DD · <session title>]

**MANNED/UNMANNED session.** Model · effort.

**Trigger:** <what started this>

**What was built:** <table of artifacts>

**Protocols/standards established:** <bullet list>

**Violations logged:** <any protocol breaks>

**Standards extracted to:** <guide file if pattern was new>

**Open items:** <what's pending>
```

---

## Memory

The delegation + build regime pattern is recorded in Eagle's agent memory:
`~/.claude/agent-memory/eagle/feedback-delegation-and-build-regime.md`

This is the persistent cross-session reminder. The guide (this file) is the
reference for builders entering the work.
