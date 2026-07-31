#!/bin/bash
# =============================================================================
# SLICES — regenerate all repomix slices for an OVUM
# =============================================================================
# Location: ~/.config/zsh/larva/slices.sh
# Alias:    slices (in config.zsh)
#
# Usage:
#   slices <ovum>
#   slices fo          # regenerate all fo zone slices
#
# Reads zones_[ovum].yaml, runs repomix for each zone.
# Must be run from OVUM root or it finds it from config.
# =============================================================================

OVUM="$1"

if [[ -z "$OVUM" ]]; then
    echo "Usage: slices <ovum>"
    echo "Example: slices fo"
    exit 1
fi

# --- Locate OVUM root ---
case "$OVUM" in
    fo)  OVUM_ROOT="$HOME/www/fantasyobchod" ;;
    im)  OVUM_ROOT="$HOME/www/freya" ;;
    psd) OVUM_ROOT="${PROJECT_PSD_PATH:-$HOME/www/psdvs}" ;;
    *)   echo "[ERROR] Unknown OVUM: $OVUM"; exit 1 ;;
esac

ZONES_FILE="$OVUM_ROOT/.larva/_config/zones_${OVUM}.yaml"

if [[ ! -f "$ZONES_FILE" ]]; then
    echo "[ERROR] Zones manifest not found: $ZONES_FILE"
    exit 1
fi

cd "$OVUM_ROOT" || exit 1

echo "[SLICES] Regenerating slices for OVUM [$OVUM]..."
echo "[SLICES] Root: $OVUM_ROOT"
echo ""

# --- Parse and generate each slice ---
python3 -c "
import yaml, subprocess, os

with open('$ZONES_FILE') as f:
    data = yaml.safe_load(f)

count = 0
errors = 0

for role in ['nucleus', 'trachea']:
    if role not in data or not data[role]:
        continue
    for scope, info in data[role].items():
        config = info.get('slice_config', '')
        output = info.get('slice_output', '')
        desc = info.get('description', '')

        if not config or not output:
            print(f'  [SKIP] {role.upper()}[{scope}] — missing config or output path')
            continue

        if not os.path.exists(config):
            print(f'  [SKIP] {role.upper()}[{scope}] — config not found: {config}')
            errors += 1
            continue

        print(f'  [GEN]  {role.upper()}[{scope}] — {desc}')
        print(f'         config: {config}')
        print(f'         output: {output}')

        result = subprocess.run(
            ['repomix', '--config', config, '--output', output],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            lines = sum(1 for _ in open(output))
            print(f'         done ({lines} lines)')
            count += 1
        else:
            print(f'         [ERROR] {result.stderr.strip()}')
            errors += 1
        print()

print(f'[SLICES] Complete: {count} generated, {errors} errors')
"
