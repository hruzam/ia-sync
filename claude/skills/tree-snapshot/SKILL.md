---
name: tree-snapshot
description: Invoke as /tree-snapshot. Dumps a project's file tree as compact JSON for orientation. Use before building context skills, exploring unknown project structure, or scoping a search. Invoke when you need to see a project layout without browsing directories.
---

I produce a JSON file-tree snapshot of any registered temple project.

## Invocation

From Bash (agents with shell access):

```bash
zsh -c "source ~/.config/zsh/ai/base.zsh && tree-snapshot <project-name>"
```

Project names match the keys in `TEMPLE_PROJECT_MAP` (see `~/.config/zsh/ai/temple-project-map.zsh`):
`reposoma` · `freya.devstudio` · `fantasyobchod` · `psdvsSys` · `piql.dev` · `vacuole` · `subai.devenv` · `reposoma.devenv`

## What it does

- Resolves the project's physical root via `temple-project-root`
- Picks `~/.config/zsh/registries/tcr/tcr.<project>.json` if it exists
- Falls back to `tcr.default.json` (depth 4 · JSON · respects `.gitignore` · ignores `node_modules/`, `vendor/`)
- Outputs JSON to stdout — pipe or capture as needed

## When to use

- Before building a project context skill (freya-context, etc.) — get the folder shape first
- When asked "what files does this project have" — cheaper than directory browsing
- Scoping a search: know the tree before running Grep

## Per-project configs

To override defaults for a specific project, add:
`~/.config/zsh/registries/tcr/tcr.<project>.json`

Config schema (all fields optional — merges over defaults):
```json
{
  "output": { "style": "json" },
  "tree": { "level": 3 },
  "include": ["app/**", "resources/**"],
  "ignore": {
    "customPatterns": ["storage/**", "bootstrap/cache/**"]
  }
}
```

## Operator shortcut (interactive shell)

```zsh
tree-snapshot freya.devstudio
```

## Guide

Full usage, config schema, and file-output mode: `~/.config/zsh/guides/toolbox.tree-converter.md`
