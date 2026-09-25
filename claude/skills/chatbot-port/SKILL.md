---
name: chatbot-port
description: Invoke as /chatbot-port <slug> [--check]. Ports one CLI skill (Claude and/or Codex) into a chatbot-readable file ~/reposoma/.germline/skills/skill.<slug>.md — method kept, harness stripped, provenance stamped. No slug → advisory list of portable skills. Unknown slug → refuses. Existing port → asks "update only?". --check → lists ports that fell behind their source.
argument-hint: <slug> [--check]
disable-model-invocation: true
---
I port a CLI skill to the chatbots (ChatGPT · Claude.ai) majkee carries in the field. They read
the port from project memory or the GitHub connector, so it must be self-contained: the method
without the harness. One CLI slug → one file. I never write anywhere else.

Codex twin: `~/ia-sync/codex/skills/chatbot-port/SKILL.md` — same slug, same contract (below),
native expression. Contract changes land in both twins together or in neither.

## Constants

- Claude home  `~/.claude/skills/<slug>/SKILL.md`
- Codex home   `~/.agents/skills/<slug>/SKILL.md` (deploy target of `~/ia-sync/codex/skills/`)
- Port home    `~/reposoma/.germline/skills/skill.<slug>.md`
- Naming precedent: `~/reposoma/raw.vendor-neutral-agents/ptyra/skill.*.md` — the `skill.`
  prefix tells a chatbot "this is a method" when the file lands in its memory.

## Provenance — authored source, primary rule, unresolved = stop

I read the deployed homes for lookup and folding; revisions come from the **authored source**
in `~/ia-sync`: `claude/skills/<slug>/SKILL.md` or `codex/skills/<slug>/SKILL.md`.

- **Primary source** = Claude when present, otherwise Codex. Its revision is the last commit
  that touched that file — never repo HEAD:
  `git -C ~/ia-sync log -1 --format=%h -- <primary-source-relative-path>`
- **`twin: both`** → the other side is the secondary; its last-touch revision is stamped as
  `twin-commit:` by the same command on its own path. One key per side; `--check` compares both.
- **Unresolved provenance = stop before writing.** No history, uncommitted changes, or
  deployed≠authored bytes on any consumed source → report the reason, write nothing. I never
  invent a revision or silently substitute a source.

## How I run

`--check` takes precedence over the no-slug advisory. Otherwise:

0. **Advise — no slug.** List every slug with a `SKILL.md` in either home; mark `[ported]`
   where a port exists, `[twin]` for both homes, else `[claude-only]` / `[codex-only]`. Stop —
   majkee picks.
1. **Refuse — unknown slug.** Neither home → *"no CLI skill `<slug>`"* + the advisory list. Stop.
   No guessing another slug.
2. **Lookup + near-miss-wait.** One home → `twin: claude|codex` · `orphan: true`. Both →
   `twin: both` · `orphan: false`. Then scan the other home for a *different* slug that contains
   `<slug>` or is contained by it (`buffering` ↔ `buffering-cycle`): print every pair and WAIT
   for majkee's word before folding — even when an exact twin also exists. This is the twin-slug
   discipline firing (single source: `atlas-ui` Guardrails); a near-miss is a defect to record,
   never a second port. The resolved relationship goes into `near-miss:`.
3. **Update-ask — existing port.** *"`skill.<slug>.md` exists — update only?"* No, or no answer
   → stop. Yes → re-fold from the current source(s), replace only that port.
4. **Fold** — the method survives, the harness goes:
   - KEEP: the job, the steps, the rules, the output shape, first-person voice.
   - REWRITE: `description` → chatbot trigger phrasing ("when majkee says …"); no `/slug`, no `$slug`.
   - STRIP: tool names, `~/` paths, `!`-hydration lines, spawn verbs, deploy/commit steps, and
     frontmatter or policy a chatbot cannot honor (`disable-model-invocation`, `allowed-tools`,
     `context`, `agent`, `argument-hint`, Codex invocation metadata).
   - TRANSLATE: a harness dependency becomes an ask — *"ask majkee for <what the tool would
     have fetched>"*.
   - ADD nothing the source does not say. With `twin: both` I fold from the Claude body and cite
     both paths; where the two bodies disagree on the method, a `## Twin note` says so — never a
     silent pick or merge.
5. **Write** — this frontmatter, then the provenance note, then the folded body:
   ```
   ---
   name: <slug>
   description: <chatbot trigger phrasing>
   source: <claude path> [· <codex path>]
   twin: claude | codex | both
   orphan: true | false
   near-miss: none | <other-side slug — one line why>
   source-commit: <primary source last-touch revision>
   twin-commit: <secondary source last-touch revision>     # only when twin: both
   ported: <YYYY-MM-DD>
   ---
   ```
   Provenance note (maintenance framing, not part of the method):
   `_Ported from the CLI skill — do not edit here; re-run /chatbot-port <slug>._`
6. **Confirm** in one line: path written · twin / orphan / near-miss status.

## --check

For every `skill.*.md` in the port home: compare `source-commit:` (and `twin-commit:` when
present) with the current last-touch revision of the matching authored source. Differ →
`<slug>: port @<a> · source @<b>` (per side) and suggest `/chatbot-port <slug>`. Equal →
silent. Missing or unverifiable provenance → reported as `unverified`, never as current.
Read-only: no fold, no overwrite prompt, no change to any port.

## What I do not do

No README or index in the port home — ".germline/skills as a bus" is parked for its own
session. No edits to the CLI source. No deploy, commit, or push.
