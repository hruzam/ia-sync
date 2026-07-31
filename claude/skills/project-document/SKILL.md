---
name: project-document
description: Invoke as /project-document <synthetic|analytic> [target]. Thin router that writes durable project documentation into <project>/guides/. synthetic = derive an onboarding/architecture guide from session understanding + code; analytic = derive a reference from the code itself. Reads the project's own guides/README.md as the convention law — never imposes a template. Pairs with /project-read (orientation in ↔ documentation out).
---

I am a thin router. Documentation is just the project's `guides/README.md` read with an
input vector, then performed. I write into the project's own `guides/`, in the project's
own conventions — I never impose the temple's doc philosophy on a client project.

**On `/project-document <mode> [target]`** where `mode ∈ {synthetic, analytic}`:

1. **Resolve the project root** (cheapest first, same cascade as /project-read):
   `temple-project-map.zsh` grep → `registry/index.md` row → beacon `path:` → ask once.
2. **Read the convention home:** `<project-root>/guides/README.md` — the single content
   home for THIS project's doc law + guide index. Freely expandable (add a guide, add an
   index row; one README now, subfolders as it grows).
   - **If absent → bootstrap it first** (see Bootstrap), confirm, then continue.
3. Find the matching `## MODE: <mode>` block. That README + your input vector `[target]`
   is the task.
4. **Perform it, sufficiency-gated** — stop when the source gives enough; escalate one
   step only on proven need; never blast parallel reads across the whole tree.
   - **synthetic** → derive a durable guide (onboarding / architecture / how-it-works)
     from the session's accumulated understanding + targeted code reads. The seat's asset
     is its context — synthesize from it; read code only to fill proven holes.
   - **analytic** → derive a reference (API / module / route / schema map) FROM the code.
     Read entry points → follow the declared surface → stop when it is captured.
     Grep/Glob/Read only; no exhaustive tree walk.
5. **Draw discipline:** run /buffering-cycle for the release — feed → synthesize → smooth
   → draw → close. Confirm the synthesis before writing.
6. **Land it** in `<project-root>/guides/` per the README's convention, and add its index
   row to `guides/README.md`.

## Bootstrap (first run — guides/README.md absent)

The project has no doc law yet. I read its existing doc landscape and seed the home from
it — I do not invent a template:
- Grep the repo for existing docs (README.md, docs/, ARCHITECTURE, *.md) + read
  flag / PROJECT.yaml for stack + conventions.
- Draft `guides/README.md` = ROUTER NOTE + `## MODE: synthetic` + `## MODE: analytic`
  blocks stating WHERE guides land, WHAT format, WHAT is authoritative for THIS project.
- Confirm with @majkee, write it, then run the requested mode.

## Rules

- **The project's `guides/README.md` is the law, not this skill.** Client projects
  (freya = Laravel, psdvSys) do NOT inherit the temple's "wire, don't consolidate /
  point-never-copy" philosophy — that is temple canon, not client canon.
- **The session is the buffer.** I do not build a temp-file collector — that already
  exists (@recorder, /session-resume). If session context is lost, recover via those
  first, then document.
- **No `context: fork`** — documentation needs the conversation's accumulated context;
  forking would drop the very understanding synthetic mode depends on.
- I do not write files until @majkee confirms the synthesis.
