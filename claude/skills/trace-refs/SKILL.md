---
name: trace-refs
description: >
  Invoke as /trace-refs <target> [scope]. Pointer-trace runner — the judgment layer
  before erasures, renames, relocations, and absorption checks. Horizontal pass:
  sweep configured roots for every reference to the target, classify each hit
  (live · historical · frozen · design-time). Vertical pass: walk the target's
  mechanism chain hop by hop, disk-verifying each hop. Output: edge list + per-hit
  verdict (repair / leave / flag). Computed fresh every run — no map is ever stored.
  Scope config: reposoma/raw.research/trace-refs/draft/README.md (default: temple).
  Not /track-back (zsh history forensics) — different tool.
---

I trace every reference to a target before anyone erases, renames, moves, or absorbs it.
I am judgment-dense: if I am running in an executor-tier seat, I stop and route up.
I never write repairs myself — I produce verdicts; repairs are dispatched to an executor
with exact instructions AFTER the verdicts are approved.

## Steps

1. **Parse arguments.** `<target>` = name, path, or identifier to trace (mandatory —
   if missing, ask and stop). `[scope]` defaults to `temple`.

2. **Read scope config** from `~/reposoma/raw.research/trace-refs/draft/README.md`,
   section `## scope: <scope>`. Extract: roots, classify taxonomy, special handling,
   chains. If the scope section is missing, list available scopes and stop.

3. **Horizontal pass.** Grep the target across every root — name plus known variants
   (old names, hyphen/dot forms, `name:` field vs filename). Classify every hit
   against the taxonomy in order: frozen → historical → design-time → live.
   First match wins; anything unmatched = live.

4. **Vertical pass.** Match the target to a chain from the scope config. Walk the
   chain hop by hop and verify each hop ON DISK (Read/Glob — never from memory,
   never from my own prior report). Record per hop: OK / MISSING / DRIFTED.
   If no chain fits, say so — an unchained target is a finding, not a failure.

5. **Emit the trace** — chat only, never a file:

   ```
   ## Trace: <target> (scope: <scope>)
   ### Vertical — chain: <name>
   hop → hop → hop   [each: OK / MISSING / DRIFTED]
   ### Horizontal — N hits
   | path:line | class | verdict | note |
   ### Verdict summary
   repair: [...] · leave: [...] · flag: [...]
   ```

6. **Stop.** No writes. On operator approval: live-pointer fixes go to an executor
   as exact edits · design-time flags route to the refresh cycle · canon-touching
   items route to @majkee's gavel.

## Hard rules

- Computed, never stored — I write no map files, sidecars, or caches.
- historical and frozen hits are NEVER repair candidates — leave, always.
- design-time hits (settings cards) are NEVER hand-edited — flag for re-synthesis.
- Machine-layer hits (`~/.config/zsh/`): fresh-read-first before any repair verdict —
  the standing stale-memory warning applies.
- Trust disk over model: every claim in my output cites a path I read this run.

---

_Born 2026-07-15 from the skills-audit session (claude-creator + 4-tombstone erasures).
Prior improvised occurrences: tools.md:16 dangling pointer · relocation rewires ×8 ·
gemini-line repair map (6 breaks). Complement to adr-guard / aihs-stale (deterministic
scanners) — this is the judgment layer._
