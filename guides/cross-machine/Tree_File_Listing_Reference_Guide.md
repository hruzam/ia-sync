# Tree & File Listing Reference Guide
**For:** Majkee's multi-project dev environment  
**Updated:** 2026-04-17

---

## 1. Tree Command

### Installation (Manjaro)

```zsh
sudo pacman -S tree
```

---

### Basic Usage

```zsh
# Current directory, 2 levels deep
tree -L 2

# Specific path
tree ~/www/fantasyobchod -L 2

# Only directories (no files)
tree -d -L 3

# Show hidden files
tree -a -L 2

# Show file sizes (human-readable)
tree -sh -L 2

# Show full path prefix
tree -f -L 2
```

---

### Filtering

```zsh
# Only PHP files
tree -P "*.php" --prune

# Only specific patterns (pipe-separated)
tree -P "*.php|*.tpl|*.js" --prune

# Exclude directories
tree -I "vendor|node_modules|storage|.git"

# Combine: PHP files, skip vendor, 3 levels
tree -P "*.php" -I "vendor|node_modules" --prune -L 3
```

> **Note:** `-P` matches filenames only (not paths). `--prune` removes empty dirs from output after filtering.

---

### Output Control

```zsh
# No indentation lines (flat look)
tree -i

# Print only dirs + file count summary
tree -d --du

# No color (for piping/saving)
tree -n

# Sort by last modification time
tree -t

# Sort by size (largest first)
tree -S

# Reverse sort
tree -r
```

---

### Saving Output

```zsh
# To file (no ANSI colors)
tree -n -L 3 > project_tree.txt

# To file with metadata
tree -n -sh -D -L 3 > project_tree.txt

# Clipboard (Wayland)
tree -n -L 3 | wl-copy

# Clipboard (X11)
tree -n -L 3 | xclip -selection clipboard
```

---

### JSON Output (built-in)

```zsh
# Native JSON output
tree -J

# JSON, 3 levels, skip junk
tree -J -L 3 -I "vendor|node_modules|.git"

# JSON to file
tree -J -L 3 -I "vendor|node_modules" > tree.json

# Pretty-print with jq
tree -J -L 3 -I "vendor|node_modules" | jq '.'
```

**JSON structure** (tree -J returns):
```json
[
  {
    "type": "directory",
    "name": "admin",
    "contents": [
      { "type": "file", "name": "index.php" },
      {
        "type": "directory",
        "name": "controller",
        "contents": [...]
      }
    ]
  },
  { "type": "report", "directories": 42, "files": 318 }
]
```

---

## 2. Project-Specific Tree Commands

### FantasyObchod

```zsh
# Full structure overview
cd ~/www/fantasyobchod && \
tree -n -L 2 -I "vendor|node_modules|.git|image" > fantasyobchod_tree.txt

# Admin controllers deep view
tree admin/controller -L 2 -I "vendor"

# PMU-related files only
tree -P "pmu*" --prune -f

# System architecture
tree system/ -L 2

# Admin module structure (Pipeline/Bypass)
tree admin/module -L 3
```

### Freya / Imago

```zsh
cd ~/www/freya && \
tree -n -L 2 -I "vendor|node_modules|storage|.git|bootstrap" > freya_tree.txt

# Laravel app structure
tree app/ -L 3

# Routes + config
tree -P "*.php" --prune routes/ config/
```

### PSDVS

```zsh
cd /media/data/projects/psdvs && \
tree -n -L 2 -I "vendor|node_modules|storage|.git" > psdvs_tree.txt
```

---

## 3. File Listing to JSON / JSONL

When `tree -J` structure is too nested and you need flat lists for AI context or scripting.

### find → JSONL (one JSON object per line)

```zsh
# All PHP files as JSONL
find . -name "*.php" -not -path "*/vendor/*" -not -path "*/.git/*" \
  -printf '{"path":"%p","size":%s,"modified":"%T@"}\n'

# Readable with jq
find . -name "*.php" -not -path "*/vendor/*" \
  -printf '{"path":"%p","size":%s}\n' | jq '.'
```

### find → JSON Array

```zsh
# Wrap JSONL into a JSON array
find . -name "*.php" -not -path "*/vendor/*" -not -path "*/.git/*" \
  -printf '"%p"\n' | jq -s '.'

# With metadata as JSON array
find . -name "*.php" -not -path "*/vendor/*" -not -path "*/.git/*" \
  -printf '{"path":"%p","size":%s}\n' | jq -s '.'
```

### find → Simple List (for AI context)

```zsh
# Just paths, clean, sorted
find . -name "*.php" -not -path "*/vendor/*" -not -path "*/.git/*" \
  | sort

# Specific extensions
find . \( -name "*.php" -o -name "*.tpl" -o -name "*.js" \) \
  -not -path "*/vendor/*" -not -path "*/node_modules/*" \
  | sort
```

---

## 4. Scoped File Manifests (AI-Ready)

Quick copy-pasteable file lists for Cursor/Houston/Vega context.

### FO — PMU Module Manifest

```zsh
cd ~/www/fantasyobchod && \
find . \( -name "pmu*" -o -name "PMU*" -o -name "Pmu*" \) \
  -not -path "*/vendor/*" | sort
```

### FO — Order Module Manifest

```zsh
cd ~/www/fantasyobchod && \
find . \( -path "*/sale/order*" -o -path "*/sale/Order*" \) \
  -not -path "*/vendor/*" | sort
```

### FO — System Core Manifest

```zsh
cd ~/www/fantasyobchod && \
find system/engine system/library system/traits admin/module \
  -name "*.php" | sort
```

### Generic — Any Module by Keyword

```zsh
# Replace MODULE with what you need
cd ~/www/fantasyobchod && \
find . -iname "*MODULE*" -not -path "*/vendor/*" -not -path "*/.git/*" | sort
```

---

## 5. Combined: Tree + File List to Single Context File

For generating a quick context bundle (lighter than repomix, no file contents):

```zsh
# Project structure + file manifest in one file
{
  echo "# Project Structure"
  echo '```'
  tree -n -L 3 -I "vendor|node_modules|.git|image|storage"
  echo '```'
  echo ""
  echo "# PHP File Manifest"
  find . -name "*.php" \
    -not -path "*/vendor/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    | sort
} > project_context.md
```

### Scoped version (module-level):

```zsh
{
  echo "# PMU Module Structure"
  echo '```'
  tree -P "pmu*|PMU*|Pmu*" --prune -f
  echo '```'
  echo ""
  echo "# PMU Files (full paths)"
  find . -iname "*pmu*" -not -path "*/vendor/*" | sort
} > pmu_context.md
```

---

## 6. One-Liner Quick Reference

```
TREE BASICS
tree -L 2                             # 2 levels deep
tree -d -L 3                          # Dirs only
tree -P "*.php" --prune               # Filter by extension
tree -I "vendor|node_modules|.git"    # Exclude dirs
tree -sh                              # Show file sizes
tree -n > out.txt                     # Save (no color)
tree -J                               # JSON output
tree -J | jq '.'                      # Pretty JSON

FIND → LISTS
find . -name "*.php" | sort                           # Sorted file list
find . -name "*.php" -printf '"%p"\n' | jq -s '.'    # JSON array
find . -iname "*pmu*" | sort                          # Case-insensitive search

CLIPBOARD
tree -n -L 3 | wl-copy                # Tree → clipboard
find . -name "*.php" | sort | wl-copy # File list → clipboard
```

---

## 7. Ignore Patterns Per Project

Reusable exclude strings for each project:

```zsh
# FantasyObchod
FO_IGNORE="vendor|node_modules|.git|image|system/storage"

# Laravel (Freya, PSDVS)
LARAVEL_IGNORE="vendor|node_modules|.git|storage|bootstrap/cache|public/storage"

# Usage
tree -I "$FO_IGNORE" -L 3
find . -not -path "*/vendor/*" -not -path "*/.git/*" -not -path "*/node_modules/*"
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `tree: command not found` | Not installed | `sudo pacman -S tree` |
| Too much output | No depth limit | Add `-L 2` or `-L 3` |
| Binary/image noise | No exclusion | Add `-I "image\|uploads\|storage"` |
| `--prune` shows nothing | Pattern wrong | `-P` matches filename only, not path |
| JSON broken in pipe | Color codes | Add `-n` flag before `-J` |
| `find -printf` not working | macOS / busybox find | Use `stat` fallback or GNU find |
