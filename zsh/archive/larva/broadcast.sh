#!/bin/bash
# =============================================================================
# BROADCAST — group consultation across all active NUCLEUS/TRACHEA zones
# =============================================================================
# Location: ~/.config/zsh/larva/broadcast.sh
# Alias:    broadcast (in config.zsh)
#
# Usage:
#   broadcast <ovum> "<question>"
#   broadcast fo "I'm adding a new CsvExportHandler that writes to DIR_DOWNLOAD. Conflicts?"
#   broadcast fo "Changing product_price DB field from DECIMAL(10,2) to DECIMAL(15,4)"
#
# What happens:
#   1. Reads zones_[ovum].yaml for active zones
#   2. Checks that slice files exist (skips missing ones with warning)
#   3. Fires one-shot Gemini call per zone IN PARALLEL
#   4. Each zone responds or says [CLEAR]
#   5. Collects all responses into single report
#
# Prerequisites:
#   - Slices must be pre-generated (repomix per zone)
#   - python3 with pyyaml (pip install pyyaml --break-system-packages)
#   - zones_[ovum].yaml configured in .larva/_config/
#
# Model: gemini-2.0-flash (one-shot, cheapest possible)
# =============================================================================

OVUM="$1"
QUESTION="$2"

if [[ -z "$OVUM" || -z "$QUESTION" ]]; then
    echo "Usage: broadcast <ovum> \"<question>\""
    echo ""
    echo "Examples:"
    echo "  broadcast fo \"I'm adding CsvExportHandler writing to DIR_DOWNLOAD. Conflicts?\""
    echo "  broadcast fo \"Changing product_price field from DECIMAL(10,2) to DECIMAL(15,4)\""
    exit 1
fi

# --- Locate configs ---
OVUM_ROOT=""
case "$OVUM" in
    fo)  OVUM_ROOT="$HOME/www/fantasyobchod" ;;
    im)  OVUM_ROOT="$HOME/www/freya" ;;
    psd) OVUM_ROOT="${PROJECT_PSD_PATH:-$HOME/www/psdvs}" ;;
    *)   echo "[ERROR] Unknown OVUM: $OVUM"; exit 1 ;;
esac

ZONES_FILE="$OVUM_ROOT/.larva/_config/zones_${OVUM}.yaml"
BROADCAST_TEMPLATE="$OVUM_ROOT/.larva/_library/_broadcast_prompt.md"

if [[ ! -f "$ZONES_FILE" ]]; then
    echo "[ERROR] Zones manifest not found: $ZONES_FILE"
    exit 1
fi

if [[ ! -f "$BROADCAST_TEMPLATE" ]]; then
    echo "[ERROR] Broadcast template not found: $BROADCAST_TEMPLATE"
    exit 1
fi

# --- Parse zones from YAML using python ---
ZONES_JSON=$(python3 -c "
import yaml, json, sys
with open('$ZONES_FILE') as f:
    data = yaml.safe_load(f)
zones = []
for role in ['nucleus', 'trachea']:
    if role in data and data[role]:
        for scope, info in data[role].items():
            zones.append({
                'role': role.upper(),
                'scope': scope,
                'slice_output': info.get('slice_output', ''),
                'description': info.get('description', '')
            })
print(json.dumps(zones))
" 2>/dev/null)

if [[ -z "$ZONES_JSON" || "$ZONES_JSON" == "[]" ]]; then
    echo "[ERROR] No zones found in $ZONES_FILE"
    echo "[HINT] Install pyyaml: pip install pyyaml --break-system-packages"
    exit 1
fi

# --- Read OVUM metadata ---
OVUM_NAME=$(python3 -c "
import yaml
with open('$ZONES_FILE') as f:
    data = yaml.safe_load(f)
print(data.get('ovum_name', '$OVUM'))
")
PHP_VERSION=$(python3 -c "
import yaml
with open('$ZONES_FILE') as f:
    data = yaml.safe_load(f)
print(data.get('php_version', 'check config'))
")

# --- Setup output directory ---
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="/tmp/broadcast_${OVUM}_${TIMESTAMP}"
mkdir -p "$REPORT_DIR"

echo ""
echo "=== BROADCAST [$OVUM] ==="
echo "Question: $QUESTION"
echo "Zones manifest: $ZONES_FILE"
echo "Output: $REPORT_DIR/"
echo ""

# --- Fire each zone in parallel ---
PIDS=()
ZONE_NAMES=()

ZONE_COUNT=$(echo "$ZONES_JSON" | python3 -c "import json,sys; print(len(json.loads(sys.stdin.read())))")

for i in $(seq 0 $((ZONE_COUNT - 1))); do
    ROLE=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['role'])")
    SCOPE=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['scope'])")
    SLICE_FILE=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['slice_output'])")
    DESCRIPTION=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['description'])")

    ZONE_ID="${ROLE,,}_${SCOPE}"
    ZONE_NAMES+=("$ROLE[$SCOPE]")

    # Check slice exists
    if [[ ! -f "$SLICE_FILE" ]]; then
        echo "[SKIP] $ROLE[$SCOPE] — slice not found: $SLICE_FILE"
        echo "[SKIP] Slice not generated. Run repomix first." > "$REPORT_DIR/${ZONE_ID}.md"
        continue
    fi

    SLICE_LINES=$(wc -l < "$SLICE_FILE" | tr -d ' ')
    SLICE_NOTE="$DESCRIPTION ($SLICE_LINES lines)"

    echo "[FIRE] $ROLE[$SCOPE] — $DESCRIPTION ($SLICE_LINES lines)"

    # Build one-shot prompt
    PROMPT_FILE="$REPORT_DIR/${ZONE_ID}_prompt.md"
    SLICE_CONTENT=$(cat "$SLICE_FILE")

    sed \
        -e "s/{{ROLE}}/$ROLE/g" \
        -e "s/{{SCOPE}}/$SCOPE/g" \
        -e "s/{{OVUM}}/$OVUM/g" \
        -e "s|{{OVUM_NAME}}|$OVUM_NAME|g" \
        -e "s|{{PHP_VERSION}}|$PHP_VERSION|g" \
        -e "s|{{SLICE_NOTE}}|$SLICE_NOTE|g" \
        "$BROADCAST_TEMPLATE" > "$PROMPT_FILE"

    # Replace {{SLICE_CONTENT}} and {{QUESTION}} — these can be multi-line
    python3 -c "
import sys
with open('$PROMPT_FILE') as f:
    content = f.read()
with open('$SLICE_FILE') as f:
    slice_content = f.read()
content = content.replace('{{SLICE_CONTENT}}', slice_content)
content = content.replace('{{QUESTION}}', '''$QUESTION''')
with open('$PROMPT_FILE', 'w') as f:
    f.write(content)
"

    # Fire one-shot gemini in background
    OUTPUT_FILE="$REPORT_DIR/${ZONE_ID}.md"
    gemini -m gemini-2.0-flash "$(cat "$PROMPT_FILE")" > "$OUTPUT_FILE" 2>&1 &
    PIDS+=($!)

done

echo ""
echo "[WAIT] ${#PIDS[@]} zones scanning in parallel..."
echo ""

# --- Wait for all to finish ---
for pid in "${PIDS[@]}"; do
    wait "$pid"
done

# --- Collect and display report ---
echo ""
echo "================================================================"
echo "  BROADCAST REPORT — [$OVUM] — $(date +%H:%M:%S)"
echo "  Question: $QUESTION"
echo "================================================================"
echo ""

FINDINGS=0
CLEAR=0

for i in $(seq 0 $((ZONE_COUNT - 1))); do
    ROLE=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['role'])")
    SCOPE=$(echo "$ZONES_JSON" | python3 -c "import json,sys; z=json.loads(sys.stdin.read()); print(z[$i]['scope'])")
    ZONE_ID="${ROLE,,}_${SCOPE}"
    OUTPUT_FILE="$REPORT_DIR/${ZONE_ID}.md"

    if [[ -f "$OUTPUT_FILE" ]]; then
        CONTENT=$(cat "$OUTPUT_FILE")
        if echo "$CONTENT" | grep -qi "\[CLEAR\]"; then
            ((CLEAR++))
        elif echo "$CONTENT" | grep -qi "\[SKIP\]"; then
            echo "  ⊘ $ROLE[$SCOPE] — SKIPPED (slice not generated)"
        else
            ((FINDINGS++))
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "  ▸ $ROLE[$SCOPE]"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "$CONTENT"
            echo ""
        fi
    fi
done

echo "================================================================"
echo "  Summary: $FINDINGS findings, $CLEAR clear, total $ZONE_COUNT zones"
echo "  Full report: $REPORT_DIR/"
echo "================================================================"
