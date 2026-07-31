# Repomix Reference Guide
**For:** Majkee's multi-project dev environment  
**Updated:** 2026-04-16

---

## What Is Repomix

Repomix bundles selected source files into a single XML (or plain text) output — designed for feeding codebase context to AI collaborators (Houston, Vega, Cursor).

---

## Installation

```zsh
npm install -g repomix
```

Verify:
```zsh
repomix --version
```

---

## Basic Usage

```zsh
# Run in project root (uses repomix.config.json if present)
repomix

# Explicit output path
repomix --output ./repomix-output.xml

# Plain text instead of XML
repomix --style plain

# Markdown instead of XML
repomix --style markdown

# JSON output
repomix --style json

# Verbose — shows token count + included files
repomix --verbose
```

---

## Include / Exclude Strategy

> **Key learning:** Using both `include` whitelist and `ignore.customPatterns` blacklist simultaneously causes conflicts. Rely solely on the `include` array. Negation patterns in `customPatterns` are unreliable when `include` is active.

### CLI — Ad-hoc Include

```zsh
# Specific dirs/globs only
repomix --include "admin/controller/sale/**,admin/model/sale/**"

# All PHP files, skip vendor
repomix --include "**/*.php" --ignore "vendor/**,node_modules/**,storage/**"
```

### Config File — Persistent Include (recommended)

Drop `repomix.config.json` in the project root:

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml"
  },
  "include": [
    "admin/controller/sale/pmu*",
    "admin/model/sale/pmu*",
    "admin/view/template/sale/pmu*",
    "admin/language/en-gb/sale/pmu*"
  ]
}
```

> **Rule:** Use `include`-only. Do NOT add `ignore.customPatterns` alongside `include`.

---

## Project-Specific Commands

### FantasyObchod (OpenCart, PHP 7.4)

```zsh
# Full core system snapshot
cd ~/www/fantasyobchod && \
repomix --output repomix-fantasyobchod-core.xml

# PMU module only
cd ~/www/fantasyobchod && \
repomix \
  --include "admin/controller/sale/pmu*,admin/model/sale/pmu*,admin/view/template/sale/pmu*,admin/language/en-gb/sale/pmu*" \
  --output repomix-pmu.xml

# Order module
cd ~/www/fantasyobchod && \
repomix \
  --include "admin/controller/sale/order*,admin/model/sale/order*,admin/view/template/sale/order*" \
  --output repomix-order.xml

# System engine + library (architecture context)
cd ~/www/fantasyobchod && \
repomix \
  --include "system/engine/**,system/library/**,system/traits/**" \
  --output repomix-system.xml

# Admin modules (Pipeline/Bypass/ExecutionAdvisor)
cd ~/www/fantasyobchod && \
repomix \
  --include "admin/module/**" \
  --output repomix-modules.xml
```

### Freya / Imago (Laravel, PHP 8+)

```zsh
cd ~/www/freya && \
repomix --output repomix-freya.xml

# Specific domain
cd ~/www/freya && \
repomix \
  --include "app/Models/**,app/Http/Controllers/**,routes/**" \
  --output repomix-freya-core.xml
```

### PSDVS (Laravel, PHP 8+)

Already wired in psd-toolkit:

```zsh
psd -rep          # Generate repomix-output.xml
psd -repcp        # Generate + timestamped copy + clipboard
```

Manual equivalent:

```zsh
cd /media/data/projects/psdvs && \
repomix --output repomix-output.xml
```

---

## Clipboard Shortcuts

```zsh
# Wayland (Manjaro default)
repomix --output /dev/stdout | wl-copy

# X11 fallback
repomix --output /dev/stdout | xclip -selection clipboard
```

---

## Useful Patterns

### Dry Run — See What Would Be Included

```zsh
repomix --include "admin/controller/sale/**" --verbose 2>&1 | head -20
```

### Combine Multiple Domains in One Bundle

```zsh
repomix \
  --include "admin/controller/sale/pmu*,admin/model/sale/pmu*,system/engine/**,admin/module/core/**" \
  --output repomix-pmu-with-context.xml
```

### Timestamped Outputs (for version tracking)

```zsh
repomix --output "repomix-fo-$(date +%Y%m%d_%H%M%S).xml"
```

### Larva-wide Manual Snapshot

For a one-off full Larva terrain snapshot intended for `@Laika` or similar mapping work:

```zsh
cd ~/www/larva && \
repomix --output ~/www/session/larva/scratch/larva_global_repomix_$(date +%Y_%m_%d).xml
```

Markdown variant:

```zsh
cd ~/www/larva && \
repomix --style markdown \
  --output ~/www/session/larva/scratch/larva_global_repomix_$(date +%Y_%m_%d).md
```

Rule of thumb:

- keep one-off heavy repomix snapshots in `~/www/session/larva/scratch/`
- keep only useful follow-up reports in `~/www/session/larva/reports/`
- do not store generated full-repo repomix output inside `~/www/larva`

### Size Check

```zsh
repomix --output repomix-output.xml && \
du -h repomix-output.xml && \
wc -l repomix-output.xml
```

---

## Config File Templates

### Minimal — Single Module

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml"
  },
  "include": [
    "admin/controller/sale/pmu*",
    "admin/model/sale/pmu*"
  ]
}
```

### Full — Multi-Layer Context

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml"
  },
  "include": [
    "system/engine/**",
    "system/library/**",
    "system/traits/**",
    "admin/module/core/**",
    "admin/module/library/**",
    "admin/controller/sale/pmu*",
    "admin/model/sale/pmu*",
    "admin/view/template/sale/pmu*",
    "admin/language/en-gb/sale/pmu*"
  ]
}
```

### Laravel Project

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml"
  },
  "include": [
    "app/**",
    "routes/**",
    "config/**",
    "database/migrations/**",
    "resources/views/**"
  ]
}
```

---

## Multi-Config Setup (Custom `--config` Path)

By default repomix looks for `repomix.config.json` in the project root. With `--config` you can point to any JSON file — enabling **multiple named configs** per project, each with its own scope and output target.

### Directory Convention

```
project-root/
├── .repomix/
│   ├── config/
│   │   ├── hard_focus_pmu.json      # PMU controller + model + view only
│   │   ├── system_core.json         # engine + library + traits
│   │   ├── full_admin.json          # broad admin context
│   │   └── order_module.json        # order-related files
│   └── xml/
│       ├── hard-focused.xml         # output from hard_focus_pmu
│       ├── system-core.xml          # output from system_core
│       └── full-admin.xml           # output from full_admin
└── ...
```

> Add `.repomix/xml/` to `.gitignore` — configs are worth tracking, outputs are not.

```gitignore
# .gitignore
.repomix/xml/
```

### Usage

```zsh
# Explicit config + explicit output
npx repomix --config .repomix/config/hard_focus_pmu.json -o .repomix/xml/hard-focused.xml

# Config defines its own output path (no -o needed)
npx repomix --config .repomix/config/system_core.json

# Verbose — see what gets bundled
npx repomix --config .repomix/config/hard_focus_pmu.json -o .repomix/xml/hard-focused.xml --verbose
```

> **`-o` overrides `output.filePath` in config.** If you pass `-o`, the config's `filePath` is ignored. If you omit `-o`, the config's `filePath` is used. You can embed the output path in the config itself to keep commands short.

### Example Config: Hard-Focused PMU

`.repomix/config/hard_focus_pmu.json`:
```json
{
  "output": {
    "filePath": ".repomix/xml/hard-focused.xml",
    "style": "xml"
  },
  "include": [
    "admin/controller/sale/pmu*",
    "admin/model/sale/pmu*",
    "admin/view/template/sale/pmu*",
    "admin/view/javascript/sale/pmu*",
    "admin/language/en-gb/sale/pmu*"
  ]
}
```

With `filePath` embedded, the command shortens to:
```zsh
npx repomix --config .repomix/config/hard_focus_pmu.json
```

### Example Config: System Core

`.repomix/config/system_core.json`:
```json
{
  "output": {
    "filePath": ".repomix/xml/system-core.xml",
    "style": "xml"
  },
  "include": [
    "system/engine/**",
    "system/library/**",
    "system/traits/**",
    "admin/module/core/**",
    "admin/module/library/**"
  ]
}
```

### Example Config: Order Module + Dependencies

`.repomix/config/order_module.json`:
```json
{
  "output": {
    "filePath": ".repomix/xml/order-module.xml",
    "style": "xml"
  },
  "include": [
    "admin/controller/sale/order*",
    "admin/model/sale/order*",
    "admin/view/template/sale/order*",
    "admin/view/javascript/sale/order*",
    "admin/language/en-gb/sale/order*",
    "admin/controller/sale/order_tag*",
    "admin/model/sale/order_tag*"
  ]
}
```

### npx vs Global

```zsh
# npx — uses project-local or fetches latest, no global install needed
npx repomix --config .repomix/config/hard_focus_pmu.json

# Global — if installed via npm install -g repomix
repomix --config .repomix/config/hard_focus_pmu.json
```

Both work identically. `npx` is useful when you want to avoid version mismatches between projects.

### Quick Aliases (optional, add to toolkit)

```zsh
# Drop in fo-toolkit.zsh or .zshrc
alias fo-rep-pmu='cd $PROJECT_FO_PATH && npx repomix --config .repomix/config/hard_focus_pmu.json'
alias fo-rep-sys='cd $PROJECT_FO_PATH && npx repomix --config .repomix/config/system_core.json'
alias fo-rep-ord='cd $PROJECT_FO_PATH && npx repomix --config .repomix/config/order_module.json'
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Empty output | `include` + `customPatterns` conflict | Remove `customPatterns`, use `include` only |
| Huge output (10MB+) | Too broad include, vendor captured | Narrow `include` globs, verify with `--verbose` |
| Missing files | Glob doesn't match | Test glob: `ls admin/controller/sale/pmu*` |
| `command not found` | npm global not in PATH | Check `~/.npm-global/bin` is in PATH (see config.zsh) |

---

## Quick Reference Card

```
repomix                              # Default (config.json)
repomix --output file.xml            # Custom output
repomix --include "glob1,glob2"      # Whitelist files
repomix --ignore "dir/**"            # Exclude (without --include only!)
repomix --style plain                # Text instead of XML
repomix --style markdown             # Markdown output
repomix --style json                 # JSON output
repomix --verbose                    # Show details + token count
repomix --config path/to/config.json # Use named config file
repomix --config cfg.json -o out.xml # Named config + override output
npx repomix --config .repomix/config/hard_focus_pmu.json  # npx variant
psd -rep                             # PSDVS shortcut
psd -repcp                           # PSDVS + copy + clipboard
```
