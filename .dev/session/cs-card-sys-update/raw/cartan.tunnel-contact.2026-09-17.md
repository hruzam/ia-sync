# raw/cartan.tunnel-contact.2026-09-17.md — first tunnel contact, Phase 2 pre-check

Sent via `tun ask` over `~/ia-sync/.dev/session/tunnel-home.state.json`
(threadId `01a0ac77-4fb2-7053-8a7f-fd224389cd1e`, created 2026-09-16T23:04:17Z, sandbox
declared `readOnly` in state file). Purpose: contact/readiness check before the real
phase-2 build send, explicitly NOT the build task (told Cartan not to write files this
turn). `tun read` on this same state reproduces the exchange — this note is the distilled
findings, not a transcript copy.

## Cartan's reply, condensed

Confirmed reading: RUNBOOK's Phase 2 section, STATUS.md, the GUIDE diff (cites commit-ish
`2f59340` — NOT a real git commit, nothing is committed in this arc; likely Cartan's own
internal diff/version marker for the working-tree state it read, not a repo ref. Flagging,
not resolving — curvature between what it said and actual repo state, evidence: `git log`
in reposoma has no `2f59340`; `git diff` hash-of-working-tree is plausible but unverified).

Confirmed the Codex-native shape is clear: new `issue-card` skill + lockstep `cold-start-card`
update, preserving shared vault / reactions / >=7 associations / sort rules.

### Two real GUIDE gaps named (not yet verified against the actual GUIDE.md diff by a
### Claude-side read — do that before amending)

1. **"Never parse filenames" vs. date-sorting, apparent contradiction.** The cold-start-card
   GUIDE's own filename law says machines never parse filenames — `kind:` frontmatter is the
   truth, prefixes are for human/glob ergonomics only. This session's sort-key decision
   (filename date as primary sort) requires parsing the filename to extract the date. Cartan
   read this as a live contradiction in the amended GUIDE, not just a style tension.
2. **Reaction-card frontmatter (`kind: issue-reaction`, no `date:`, etc.) is specified only
   in the Claude skill** (`~/ia-sync/claude/skills/issue-card/SKILL.md`), not written into
   the GUIDE itself. The GUIDE is supposed to be the shared cross-brand contract — per
   `cold-start-card/GUIDE.md`'s own law: "on conflict between this guide and any skill copy
   of the schema, THIS GUIDE WINS." A schema that exists only in one brand's skill file
   isn't actually canon yet.

### Sandbox clarification (curvature, named not resolved)

State file says `sandbox.type: "readOnly"`. Cartan's own report: "Effective sandbox permits
session-directory writes but excludes `~/ia-sync/codex/`; the build table must include that
path." This disagrees with the state file's literal `readOnly` value — could mean Codex's
runtime sandbox differs from what the tunnel state JSON reports, or "session-directory"
refers to Codex's own scratch dir, unrelated to this repo. Not resolved here — needs
majkee's read or a second tunnel round-trip to pin down exactly what IS and ISN'T writable
before sending the real build task.

## What this means for next steps

- Before phase 2's real build send: reconcile gap 1 (filename-parsing law vs. sort-key rule)
  and gap 2 (reaction frontmatter missing from GUIDE) — likely another small @Delta pass on
  the GUIDE draft, cross-witnessed by @assay same as the reactions/ delta.
- Sandbox: majkee's call whether the existing table's actual write permissions are already
  sufficient (per Cartan's "session-directory writes" claim) or whether a fresh
  `--sandbox workspace-write` table is still needed. Don't assume either way from chat alone
  — verify with a second small tunnel round-trip once majkee decides.
