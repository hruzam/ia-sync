# Prepared source map — inputs to verify, not a new authority

2026-10-26 · Cartan · office · observed repository HEAD 5c26d80. R1 establishes actual availability
and resolves unknown roots. Do not assume directory naming makes a runtime use a skill.

## Declared authored inputs

- Germline: `/home/hruzam/ia-sync/germline/`; contract
  `/home/hruzam/ia-sync/germline/README.md`. Agent identities/bindings/cards and skill.*.md
  remain distinct kinds. Runtime deployed copy: `/home/hruzam/.germline/`.
- Temple guides: `/home/hruzam/reposoma/raw.guides/`; guide resolver contract
  `/home/hruzam/ia-sync/codex/skills/guide/SKILL.md`. Catalog GUIDE frontmatter and res chapter
  basenames; ordinary resolution does not walk raw/src/ast side directories.
- Authored Codex skills: `/home/hruzam/ia-sync/codex/skills/`.
- Authored Claude skills: `/home/hruzam/ia-sync/claude/skills/`.
- Source/deployed twin precedent: `/home/hruzam/ia-sync/codex/skills/chatbot-port/SKILL.md`.
  Read its provenance rules as precedent, not its write/port procedure as this task's job.

## Explicit candidate installed/native roots

- `/home/hruzam/.agents/skills/` — candidate user Codex/shared local skill scope.
- `/home/hruzam/.claude/skills/` — candidate personal Claude skill scope.
- `/home/hruzam/.codex/skills/.system/` — system-skill path supplied in this session's runtime
  catalog, not a claim of a universal vendor path. Confirm actual files/availability.
- `/home/hruzam/ia-sync/.agents/skills/` and `/home/hruzam/ia-sync/.claude/skills/` — candidate
  project-native scopes; distinguish their symlink targets/authoring origin when present.

Other vendor-system/plugin roots require a specific manifest or runtime-catalog path. Report
that inventory gap instead of scanning every cache/home directory. Read only skill metadata
and selected named sources, not credentials, plugin state databases, rollouts or histories.
Preserve distinct name/origin entries; source presence does not prove host enablement.

## Existing implementation patterns

- `/home/hruzam/ia-sync/zsh/experimental/README.md` and dispatcher.zsh: lazy runner and
  `_EXPERIMENTAL_ROOT` source-tree exercise. New source-reader maintainer row only.
- `/home/hruzam/ia-sync/zsh/ai/command-palette.zsh`: selection through terminal separate from
  stdout; it catalogs commands, so do not replace its map with a document catalog.
- `/home/hruzam/ia-sync/zsh/session/runbook.zsh` and runbook.py: small picker/fallback and
  Markdown reading patterns; surrounding session/presence features are not this reader's scope.
- `/home/hruzam/ia-sync/zsh/sync/guides.zsh` writes published mirrors; do not confuse that
  command with source browsing or model-context loading.

## Prepared primary references

Codex documents repository walk-up `.agents/skills`, user `.agents/skills`, admin/system
locations, and full skill loading after selection. Same-name skills are not merged.
[Official Codex skills](https://learn.chatgpt.com/docs/build-skills).

Claude documents personal/project/nested/plugin scopes and its own invocation/name rules;
skill body loading occurs on use. Its semantics are not assumed identical to Codex.
[Official Claude skills](https://code.claude.com/docs/en/skills).

These sources were checked during preparation; current claims should be reverified by R1 when
native web tooling is available. Agents API capability_directories is not Codex CLI discovery.
No Slint research or framework commitment is needed for this terminal slice.
