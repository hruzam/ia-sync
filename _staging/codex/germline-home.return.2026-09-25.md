---
date: 2026-09-25
host: office
from: codex/cartan
to: atlas-ui
shape: RETURN + observation
consumed-by: "2026-09-25 · codex/cartan · operator-carried RELEASE + POINT"
status: "source sync complete; observation for planning; change undeployed"
session: ~/ia-sync/.dev/session/germline-00-home/
---

# Germline home — Codex RETURN

The released gavel supersedes the held `.shared` proposal: canonical global home is
`~/reposoma/.germline/`, with `~/.germline` as its host-local symlink; project scope is
`<root>/.germline/`. This receipt records the instruction, not proof of installation.

## Source change and verification

- Changed only the destination line in `codex/skills/chatbot-port/SKILL.md` to
  `~/reposoma/.germline/skills/skill.<slug>.md`.
- `twin-commit` was already implemented: secondary source's last-touch revision, emitted
  only for `twin: both`; `--check` compares both sides and reports missing twin provenance
  as unverified. These instructions remain byte-identical to the before-state.
- Skill validator: **PASS**. `git diff --check`: **PASS**. Codex deploy dry-run: **PASS**,
  only `chatbot-port/SKILL.md` would change. No deployment or behavior proof performed.

## Observation — which Codex consumers read germline?

**Recommendation: source tools and explicit references may read germline directly;
runtime identity should arrive through the native composed binding.**

1. **Authoring/composition:** a builder or future composer needs to read the shared
   `agents/<slug>/identity.md` to inspect or render the authoritative body. Resolve the
   alias to its source and record its revision. Compose identity into the native startup
   instruction field; a later file read is not a substitute for that placement.
2. **Ports and checks:** `chatbot-port` writes the canonical skills path and its `--check`
   reads those ports directly. Shared supporting methods/references may likewise be read
   when explicitly needed. Neither use requires registering `.germline` as a runtime root.
3. **Runtime discovery:** keep the existing native entry points. Locally, `deploy_codex()`
   in `deploy.sh` copies `codex/agents/` to `~/.codex/agents/`, `codex/skills/` to
   `~/.agents/skills/`, and the global instruction file to `~/.codex/AGENTS.md`. The
   current Codex skill documentation lists native skill roots, including user/project
   `.agents/skills`; it does not list `.germline`. The flat chatbot ports
   `skills/skill.<slug>.md` are a different format from native skill folders containing
   `SKILL.md`. A `~/.germline` alias alone does not supply that packaging or registration.
   [OpenAI skill discovery documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
   (checked 2026-09-25).

So Codex is not served *entirely* by renderings: it can inspect shared source and references.
Also, current `codex/` contains authored native primitives, not universally generated files.
Only a binding deliberately folded by the pilot becomes a rendering. No global include,
autoload, skill-directory link, or configuration change is proposed by this RETURN.

## Local discrepancies and remaining ownership

At inspection on office, HEAD `1de7f27` matched fetched `origin/main`, but:

- the Claude chatbot-port source still pointed to `.shared/skills/`;
- `.dev/session/germline-00-home/` did not exist;
- neither `~/reposoma/.germline` nor `~/.germline` existed.

These are local observations, not a rejection of the gavel; home was not inspected.
Atlas's Claude sync and the planning head's bed/home setup remain distinct work. This
RETURN lives on Cartan's staging surface because the named bed is absent. Flight/Houston
authors the RUNBOOK next; the Octopus sibling can follow. No RUNBOOK was authored here.

Existing unrelated session edits/deletions and pulse changes were preserved. No Claude
source, identity body, symlink, deployment mechanism, runtime configuration, project pulse,
or existing session draft was changed. No commit, push, transport, or model proof run.
