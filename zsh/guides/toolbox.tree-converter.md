# Toolbox: tree-snapshot (tree-converter)

`~/.config/zsh/guides/toolbox.tree-converter.md · audience: operator+agent · machine: both · verified: 2026-07-11`
`lineage: born in larva (temple/legacy-wall.md — "dragged verbatim into the machine layer, still running"). The larva install paths of the old guide are dead; this is the current temple-era usage.`

---

## Usage

```bash
tree-snapshot <project>     # keyboard key; project name = TEMPLE_PROJECT_MAP key
```

Agent form (non-interactive shells):

```bash
zsh -c 'source ~/.config/zsh/ai/base.zsh && tree-snapshot <project>'
```

Output: the project's file tree as JSON on stdout (depth 4 · `.gitignore`-aware ·
`vendor/` excluded — per default config).

---

## Configs

| Path | Role |
|---|---|
| `~/.config/zsh/registries/tcr/tcr.<project>.json` | per-project config (key = TEMPLE_PROJECT_MAP key) |
| `~/.config/zsh/registries/tcr/tcr.default.json` | fallback: depth 4 · JSON · gitignore-aware · `vendor/` excluded |

---

## Engine chain

```
tree-snapshot (fn)  →  ai/temple-tree.zsh (wrapper; resolves root via P0 project map)
                    →  ai/tree-converter.sh (Node.js, zero npm deps; crawls CWD → JSON/YAML)
```

Direct engine call (bypasses the project map):

```bash
~/.config/zsh/ai/tree-converter.sh -c <config.json>
```

---

## Pointers

- Live map row: `~/.config/zsh/AGENTS.md` (temple utilities)
- Panel: `ai-help` §Temple utilities
