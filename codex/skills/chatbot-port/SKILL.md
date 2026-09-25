---
name: chatbot-port
description: Port a named Claude or Codex CLI skill into a self-contained chatbot method in reposoma. Invoke explicitly as $chatbot-port with a slug; no slug lists candidates, and --check reports ports behind their source.
---

# Chatbot port

I port one CLI skill to a self-contained method for ChatGPT or Claude.ai, preserving its
method and first-person voice while removing its harness. One slug produces one file.
My twin contract is `~/ia-sync/claude/skills/chatbot-port/SKILL.md`, **Provenance** and **--check**;
the twin-slug discipline lives in `~/ia-sync/claude/agents/atlas-ui.md`, **Guardrails**.

## Homes and provenance

- Claude source: `~/.claude/skills/<slug>/SKILL.md`.
- Codex source: `~/.agents/skills/<slug>/SKILL.md`.
- Only write destination: `~/reposoma/.germline/skills/skill.<slug>.md`.
- Naming precedent: `~/reposoma/raw.vendor-neutral-agents/ptyra/skill.*.md`.

I read the deployed homes for lookup and folding. Revision provenance comes from the
corresponding authored source in `~/ia-sync`: `claude/skills/<slug>/SKILL.md` or
`codex/skills/<slug>/SKILL.md`. The primary source is Claude when present, otherwise Codex.
Its revision is the last commit touching that file, never repository HEAD:

```text
git -C ~/ia-sync log -1 --format=%h -- <primary-source-relative-path>
```

When `twin: both`, the other source is secondary. I obtain its last-touch revision with
the same command on its own authored path and record it as `twin-commit`. I write this
key only for `twin: both`; `--check` compares both source revisions independently.

I check that each consumed source's bytes match its committed source. Missing history,
uncommitted changes, or deployed/source drift leave provenance unresolved; I report the
reason and stop before writing. I do not invent a revision or silently substitute a source.

## Invocation and decisions

I take the slug and optional `--check` from the user's message. A slug is one skill-folder
name, never a path. `--check` selects the read-only check below and takes precedence over
the no-slug advisory. Otherwise:

1. **Advise — no slug.** List the slugs with a `SKILL.md` in either home. Mark `[ported]`
   when the port exists, `[twin]` for both homes, otherwise `[claude-only]` or `[codex-only]`.
   Stop for majkee to choose.
2. **Refuse — unknown slug.** If neither home contains it, say “no CLI skill `<slug>`”,
   provide the advisory list, and stop. Do not create a source or guess another slug.
3. **Lookup and near-miss-wait.** One source means `twin: claude` or `twin: codex` and
   `orphan: true`; both mean `twin: both` and `orphan: false`. For each matched home, scan
   the other home for a different slug that contains the requested slug or is contained by
   it, such as `buffering` and `buffering-cycle`. Report every pair and wait for majkee's
   direction before folding, even if an exact twin also exists. A near-miss never licenses
   a second port. Record the resolved relationship in `near-miss`.
4. **Update-ask — existing port.** Ask “`skill.<slug>.md` exists — update only?” unless
   the user has already explicitly authorized that update. No means stop; yes means
   re-fold the current sources and replace only that port. No answer is no permission.

With both sources, I fold from the Claude body and cite both source paths. If their methods
disagree, I expose the disagreement in `## Twin note`; I do not silently choose or merge it.

## Fold and write

- **Keep:** the job, steps, rules, output shape, and first-person voice.
- **Rewrite:** the description as a chatbot trigger, such as “when majkee says …”, without
  slash-command or dollar-skill invocation syntax.
- **Strip from the method:** tool names, home-directory paths, hydration directives, spawn
  verbs, deployment/commit steps, and CLI-only frontmatter or policy that a chatbot cannot
  honor. This includes `disable-model-invocation`, `allowed-tools`, `context`, `agent`,
  `argument-hint`, and Codex invocation metadata.
- **Translate dependencies:** ask majkee for what a harness tool would have fetched.
- **Add no new method, rule, or capability.** Source paths remain in provenance only.

I write these frontmatter keys, then the provenance note and folded body. Values below
are placeholders; I serialize real values as valid YAML, quoting paths and free text.

```yaml
---
name: <slug>
description: <chatbot trigger phrasing>
source: <Claude path, Codex path, or both joined with ·>
twin: <claude | codex | both>
orphan: <true | false>
near-miss: <none | other-side slug and one-line explanation>
source-commit: <primary source's last-touch revision>
twin-commit: <secondary source's last-touch revision> # only when twin: both; omit otherwise
ported: <YYYY-MM-DD>
---
```

Provenance note: _Ported from the CLI skill — do not edit here; re-run `$chatbot-port <slug>`._
That note is maintenance framing, not part of the chatbot method.

I confirm in one line: path written · twin / orphan / near-miss status.

## --check

For every `skill.*.md` in the port home, compare `source-commit` with the current last-touch
revision of its matching primary authored source. For `twin: both`, also compare
`twin-commit` with the secondary authored source's last-touch revision on its own path.
Different revisions report `<slug>: port @<a> · source @<b>` per side, identifying the side,
and suggest `$chatbot-port <slug>`. Equal revisions are silent. Missing or unverifiable
provenance, including a missing `twin-commit` for `twin: both`, is reported as unverified,
never as current.
This mode only reads; it neither folds nor requests an overwrite nor changes a port.

## Boundary

I write no README or index, edit no CLI source, and do not deploy, commit, or push. The
shared-skills discovery bus remains separate work. I use available file tools; this
procedure requires no model subprocess, print mode, subagent, or transport. If the port
destination is outside the active writable roots, I prepare the result and request the
runtime's required filesystem approval before writing there.
