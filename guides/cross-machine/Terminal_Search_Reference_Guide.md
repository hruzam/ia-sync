# Terminal Search Reference Guide
**For:** Majkee's multi-project dev environment  
**Updated:** 2026-04-17

---

## Tool Overview

| Tool | Install (Manjaro) | Speed | Best For |
|------|-------------------|-------|----------|
| `grep` | Built-in | Baseline | Universal, pipes, simple searches |
| `ripgrep` (`rg`) | `sudo pacman -S ripgrep` | ~10x grep | Large codebases, respects .gitignore |
| `ag` (Silver Searcher) | `sudo pacman -S the_silver_searcher` | ~5x grep | Similar to rg, lighter feature set |

> **Recommendation:** Install `ripgrep` — it auto-skips `.git/`, `vendor/`, `node_modules/`, binary files, and respects `.gitignore` out of the box. All examples below show both `grep` and `rg` variants.

---

## 1. Grep Essentials

### Flags Worth Memorizing

```
-r    Recursive (search subdirectories)
-n    Show line numbers
-i    Case-insensitive
-l    Show filenames only (not matching lines)
-L    Show files that do NOT match
-c    Count matches per file
-w    Match whole words only
-P    Perl-compatible regex (lookahead, lookbehind, \d, \w)
-E    Extended regex (equivalent to egrep — +, ?, |, () without escaping)
-o    Print only the matched part
-v    Invert match (lines NOT matching)
-H    Show filename (default in recursive)
-h    Hide filename
-A N  Show N lines After match
-B N  Show N lines Before match
-C N  Show N lines Context (before + after)
--include="GLOB"   Only search these files
--exclude="GLOB"   Skip these files
--exclude-dir=DIR  Skip these directories
```

### The Base Command

```zsh
# Your existing alias (from .zshrc)
alias mygrep='grep -Hrn'

# Equivalent to: grep -H (filename) -r (recursive) -n (line numbers)
```

---

## 2. Searching by Phrase

### Exact Phrase

```zsh
# Grep — quote the phrase
grep -rn "function getProducts" ~/www/fantasyobchod/
grep -rn "class ModelSaleOrder" ~/www/fantasyobchod/admin/

# Ripgrep
rg "function getProducts" ~/www/fantasyobchod/
rg "class ModelSaleOrder" ~/www/fantasyobchod/admin/
```

### Case-Insensitive Phrase

```zsh
grep -rni "pmu_profiles" ~/www/fantasyobchod/
rg -i "pmu_profiles" ~/www/fantasyobchod/
```

### Whole Word Only

Prevents `getOrder` matching `getOrderProducts`:

```zsh
grep -rnw "getOrder" ~/www/fantasyobchod/
rg -w "getOrder" ~/www/fantasyobchod/
```

### Multi-Word with Regex

```zsh
# Either word
grep -rnE "PmuJobRunner|PmuProfile" ~/www/fantasyobchod/
rg "PmuJobRunner|PmuProfile" ~/www/fantasyobchod/

# Word followed by something
grep -rnP "function\s+get\w+" ~/www/fantasyobchod/admin/model/
rg "function\s+get\w+" ~/www/fantasyobchod/admin/model/
```

---

## 3. Scoped Searching (by file type / directory)

### By Extension

```zsh
# Grep — only PHP files
grep -rn --include="*.php" "executeBypass" ~/www/fantasyobchod/

# Grep — PHP + TPL
grep -rn --include="*.php" --include="*.tpl" "order_tag" ~/www/fantasyobchod/

# Ripgrep — file type filter
rg -t php "executeBypass" ~/www/fantasyobchod/
rg -t php -t js "order_tag" ~/www/fantasyobchod/

# Ripgrep — list known types
rg --type-list | grep php
```

### Excluding Junk

```zsh
# Grep — skip vendor, node_modules, .git
grep -rn \
  --exclude-dir=vendor \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  --exclude-dir=image \
  "getProducts" ~/www/fantasyobchod/

# Ripgrep — automatic! But manual override:
rg --glob '!vendor' --glob '!storage' "getProducts" ~/www/fantasyobchod/
```

### Specific Directory Scope

```zsh
# Only admin controllers
grep -rn "function index" ~/www/fantasyobchod/admin/controller/sale/

# Only system engine
grep -rn "class Action" ~/www/fantasyobchod/system/engine/
```

---

## 4. Context Lines (See Surrounding Code)

```zsh
# 3 lines before and after match
grep -rn -C 3 "function apply" ~/www/fantasyobchod/admin/controller/sale/pmu*

# 5 lines after (see function body)
grep -rn -A 5 "function preview" ~/www/fantasyobchod/admin/controller/sale/pmu*

# 2 lines before (see docblock/comment)
grep -rn -B 2 "function saveAjax" ~/www/fantasyobchod/admin/controller/sale/pmu*

# Ripgrep — same flags
rg -C 3 "function apply" ~/www/fantasyobchod/admin/controller/sale/
rg -A 10 "class PmuJobRunner" ~/www/fantasyobchod/
```

---

## 5. Finding Definitions & Patterns

### PHP Functions

```zsh
# Find function definition
grep -rn "function getOrder(" ~/www/fantasyobchod/admin/
rg "function getOrder\(" ~/www/fantasyobchod/admin/

# Find all public methods in a file
grep -n "public function" ~/www/fantasyobchod/admin/model/sale/order.php

# Find class definitions
grep -rn "^class " ~/www/fantasyobchod/system/engine/
rg "^class \w+" ~/www/fantasyobchod/system/engine/
```

### SQL / Database

```zsh
# Find table references
grep -rn "pmu_profiles" ~/www/fantasyobchod/admin/ --include="*.php"

# Find JOINs in model
grep -rn "JOIN" ~/www/fantasyobchod/admin/model/sale/order.php

# Find queries modifying a table
grep -rnE "(INSERT|UPDATE|DELETE).*oc_order" ~/www/fantasyobchod/ --include="*.php"
```

### JavaScript / jQuery

```zsh
# Find event bindings
grep -rn "\.on(" ~/www/fantasyobchod/admin/view/ --include="*.js"
rg "\.on\(" ~/www/fantasyobchod/admin/view/ -t js

# Find AJAX calls
grep -rn "ajax(" ~/www/fantasyobchod/admin/view/ --include="*.js" --include="*.tpl"
rg "ajax\(" ~/www/fantasyobchod/admin/view/
```

### Config / Language Keys

```zsh
# Find where a language key is defined
grep -rn "text_pmu_profile" ~/www/fantasyobchod/admin/language/

# Find where it's used
grep -rn "text_pmu_profile" ~/www/fantasyobchod/admin/controller/ ~/www/fantasyobchod/admin/view/
```

---

## 6. Advanced Patterns (Regex)

### Perl-Compatible Regex (-P flag)

```zsh
# Match variable assignment: $this->model_sale_order
grep -rnP '\$this->model_\w+' ~/www/fantasyobchod/admin/controller/sale/

# Find TODO/FIXME/HACK comments
grep -rnP '(TODO|FIXME|HACK|XXX):?\s' ~/www/fantasyobchod/ --include="*.php"

# Find numbers in function names (version-smell)
grep -rnP 'function \w+\d+' ~/www/fantasyobchod/ --include="*.php"

# Match PHP array syntax (old-style)
grep -rnP "array\s*\(" ~/www/fantasyobchod/admin/controller/sale/pmu*
```

### Lookahead / Lookbehind

```zsh
# Function calls (not definitions) — "getOrder(" NOT preceded by "function "
grep -rnP '(?<!function )getOrder\(' ~/www/fantasyobchod/admin/ --include="*.php"

# Find $data['key'] assignments
grep -rnP "\\\$data\['" ~/www/fantasyobchod/admin/controller/sale/order.php
```

### Multi-Line (ripgrep only)

```zsh
# Match across lines (e.g., function + its first line)
rg -U "function apply\(.*\)\s*\{[^}]{0,200}" ~/www/fantasyobchod/admin/controller/sale/pmu*
```

---

## 7. Counting & Statistics

```zsh
# Count matches per file
grep -rc "TODO" ~/www/fantasyobchod/ --include="*.php" | grep -v ":0$"

# Total match count
grep -rc "TODO" ~/www/fantasyobchod/ --include="*.php" | awk -F: '{s+=$2} END{print s}'

# Count files containing pattern
grep -rl "order_tag" ~/www/fantasyobchod/ --include="*.php" | wc -l

# Ripgrep stats
rg --stats "order_tag" ~/www/fantasyobchod/ -t php
```

---

## 8. Find Files by Name (not content)

```zsh
# Find files by name pattern
find ~/www/fantasyobchod -name "pmu*" -type f
find ~/www/fantasyobchod -iname "*order*" -name "*.php" -type f

# Find recently modified (last 24h)
find ~/www/fantasyobchod -name "*.php" -mtime 0

# Find recently modified (last 7 days)
find ~/www/fantasyobchod -name "*.php" -mtime -7

# Find large files
find ~/www/fantasyobchod -name "*.php" -size +100k

# fd (faster alternative, respects .gitignore)
# Install: sudo pacman -S fd
fd "pmu" ~/www/fantasyobchod --extension php
fd --changed-within 1d --extension php ~/www/fantasyobchod
```

---

## 9. Piping & Combining

### Search Results → Further Filtering

```zsh
# Find function, then filter to specific keyword
grep -rn "function " ~/www/fantasyobchod/admin/model/sale/order.php | grep -i "total"

# Find files, then search inside them
find ~/www/fantasyobchod -name "pmu*" -name "*.php" -exec grep -ln "preview" {} \;

# Ripgrep → filter filenames
rg -l "executeBypass" ~/www/fantasyobchod/ | grep "controller"
```

### Search → Open in Editor

```zsh
# Open all files containing pattern in VS Code
grep -rl "PmuJobRunner" ~/www/fantasyobchod/ --include="*.php" | xargs code

# Open all files in Sublime
grep -rl "PmuJobRunner" ~/www/fantasyobchod/ --include="*.php" | xargs subl

# Ripgrep → editor
rg -l "PmuJobRunner" ~/www/fantasyobchod/ -t php | xargs code
```

### Search → Clipboard

```zsh
# Copy matching lines to clipboard
grep -rn "order_tag" ~/www/fantasyobchod/ --include="*.php" | wl-copy

# Copy filenames only
grep -rl "order_tag" ~/www/fantasyobchod/ --include="*.php" | wl-copy
```

---

## 10. Project-Specific Search Functions

Drop these in a toolkit or `.zshrc` for daily use:

```zsh
# FantasyObchod — search PHP + TPL + JS
fos() {
    grep -Hrn \
      --include="*.php" --include="*.tpl" --include="*.js" \
      --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git \
      "$1" "${PROJECT_FO_PATH:-$HOME/www/fantasyobchod}"
}

# FantasyObchod — filenames only
fof() {
    grep -Hrl \
      --include="*.php" --include="*.tpl" --include="*.js" \
      --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git \
      "$1" "${PROJECT_FO_PATH:-$HOME/www/fantasyobchod}"
}

# Laravel projects — search app + routes + config
las() {
    local project_path="${2:-$(pwd)}"
    grep -Hrn \
      --include="*.php" --include="*.blade.php" --include="*.js" \
      --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=storage --exclude-dir=.git \
      "$1" "$project_path"
}

# SQL hunting — find queries touching a table
sqlh() {
    grep -HrnP \
      --include="*.php" \
      --exclude-dir=vendor \
      "(SELECT|INSERT|UPDATE|DELETE|JOIN|FROM).*$1" \
      "${2:-$(pwd)}"
}
```

**Usage:**
```zsh
fos "getOrder"           # Search FO codebase
fof "PmuJobRunner"       # Find files containing pattern
las "Route::" ~/www/freya  # Search Laravel project
sqlh "oc_order" ~/www/fantasyobchod  # Find SQL touching oc_order
```

---

## 11. Replacing (Search & Replace)

### sed — In-Place

```zsh
# Preview first (no -i)
grep -rn "old_function_name" ~/www/fantasyobchod/admin/ --include="*.php"

# Replace in single file
sed -i 's/old_function_name/new_function_name/g' file.php

# Replace across files (careful!)
grep -rl "old_text" ~/www/fantasyobchod/admin/ --include="*.php" \
  | xargs sed -i 's/old_text/new_text/g'

# Dry run with diff
grep -rl "old_text" ~/www/fantasyobchod/admin/ --include="*.php" \
  | xargs sed 's/old_text/new_text/g' | diff - file.php
```

### Backup Before Replace

```zsh
# Create .bak files
grep -rl "old_text" ~/www/fantasyobchod/admin/ --include="*.php" \
  | xargs sed -i.bak 's/old_text/new_text/g'

# Clean up backups after verification
find ~/www/fantasyobchod/admin/ -name "*.bak" -delete
```

---

## Quick Reference Card

```
BASIC SEARCH
grep -rn "phrase" path/              # Recursive + line numbers
grep -rni "phrase" path/             # + case-insensitive
grep -rnw "word" path/               # Whole word only
grep -rnE "a|b|c" path/              # OR patterns
grep -rnP "regex" path/              # Perl regex

SCOPE
--include="*.php"                    # Only these files
--exclude-dir=vendor                 # Skip directory
-l                                   # Filenames only
-c                                   # Count per file

CONTEXT
-A 5                                 # 5 lines after
-B 3                                 # 3 lines before
-C 3                                 # 3 lines both sides

RIPGREP (rg)
rg "phrase" path/                    # Auto-skips .git, vendor, binaries
rg -t php "phrase"                   # By file type
rg -i "phrase"                       # Case-insensitive
rg -w "word"                         # Whole word
rg -l "phrase"                       # Filenames only
rg --stats "phrase"                  # Match statistics
rg -C 3 "phrase"                     # Context lines

FIND FILES
find . -name "*.php" -type f         # By name
find . -name "*.php" -mtime 0        # Modified today
fd "pattern" --extension php         # fd (fast alternative)

CUSTOM HELPERS
fos "pattern"                        # Search FO codebase
fof "pattern"                        # FO filenames only
las "pattern" path/                  # Search Laravel project
sqlh "table_name" path/              # Find SQL queries
```
