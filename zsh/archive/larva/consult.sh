#!/bin/bash
# =============================================================================
# CONSULT — launch a scoped NUCLEUS/TRACHEA consultation session
# =============================================================================
# Location: ~/.config/zsh/larva/consult.sh
# Alias:    consult (in config.zsh)
#
# Usage:
#   consult <role> <scope> <ovum> <repomix_slice_file>
#
# Examples:
#   consult nucleus catalog fo /tmp/fo_catalog_slice.txt
#   consult trachea pipeline fo /tmp/fo_pipeline_slice.txt
#
# What happens:
#   1. Builds full consultation context (prompt template + repomix slice)
#   2. Saves to /tmp/consult_[role]_[scope]_[ovum].md
#   3. Opens interactive Gemini CLI session
#   4. Paste the context file path when prompted, or use manual paste
#
# Model: gemini-2.5-flash (1M context, cheap, fast)
# =============================================================================

ROLE_RAW="$1"
SCOPE="$2"
OVUM="$3"
SLICE_FILE="$4"

# --- Validate ---
if [[ -z "$ROLE_RAW" || -z "$SCOPE" || -z "$OVUM" || -z "$SLICE_FILE" ]]; then
    echo "Usage: consult <role> <scope> <ovum> <repomix_slice_file>"
    echo ""
    echo "  role:   nucleus | trachea"
    echo "  scope:  zone or flow name (e.g. catalog, pipeline, pricing)"
    echo "  ovum:   project shortcode (e.g. fo, im, psd)"
    echo "  slice:  path to repomix slice file"
    echo ""
    echo "Examples:"
    echo "  consult nucleus catalog fo /tmp/fo_catalog_slice.txt"
    echo "  consult trachea pipeline fo /tmp/fo_pipeline_slice.txt"
    exit 1
fi

ROLE=$(echo "$ROLE_RAW" | tr '[:lower:]' '[:upper:]')

if [[ "$ROLE" != "NUCLEUS" && "$ROLE" != "TRACHEA" ]]; then
    echo "[ERROR] Role must be 'nucleus' or 'trachea', got: $ROLE_RAW"
    exit 1
fi

if [[ ! -f "$SLICE_FILE" ]]; then
    echo "[ERROR] Slice file not found: $SLICE_FILE"
    exit 1
fi

# --- Resolve OVUM ---
OVUM_ROOT=""
case "$OVUM" in
    fo)
        OVUM_ROOT="${PROJECT_FO_PATH:-$HOME/www/fantasyobchod}"
        OVUM_NAME="FantasyObchod"
        PHP_VERSION="7.4 strict"
        ;;
    im)
        OVUM_ROOT="${PROJECT_IM_PATH:-$HOME/www/freya}"
        OVUM_NAME="Freya/Imago"
        PHP_VERSION="7.4 (OC) + 8.0+ (Laravel)"
        ;;
    psd)
        OVUM_ROOT="${PROJECT_PSD_PATH:-$HOME/www/psdvs}"
        OVUM_NAME="PSDVS"
        PHP_VERSION="8.0+"
        ;;
    pupa)
        OVUM_ROOT="${PROJECT_PUPA_PATH:-$HOME/www/kukla}"
        OVUM_NAME="Kukla"
        PHP_VERSION="check project config"
        ;;
    *)
        OVUM_ROOT="$HOME/www/$OVUM"
        OVUM_NAME="$OVUM"
        PHP_VERSION="check project config"
        ;;
esac

# --- Locate template ---
TEMPLATE=""
for candidate in \
    "$OVUM_ROOT/.larva/_library/_consultation_prompt.md" \
    "$HOME/www/fantasyobchod/.larva/_library/_consultation_prompt.md" \
    ; do
    [[ -f "$candidate" ]] && TEMPLATE="$candidate" && break
done

if [[ -z "$TEMPLATE" ]]; then
    echo "[ERROR] Template not found: .larva/_library/_consultation_prompt.md"
    exit 1
fi

# --- Build context file ---
SLICE_LINES=$(wc -l < "$SLICE_FILE" | tr -d ' ')
SLICE_SIZE=$(wc -c < "$SLICE_FILE" | tr -d ' ')
SLICE_NOTE="Repomix slice: $SCOPE ($SLICE_LINES lines, ${SLICE_SIZE} bytes)"

CONTEXT_FILE="/tmp/consult_${ROLE,,}_${SCOPE}_${OVUM}.md"

# Fill template variables and append slice
sed \
    -e "s/{{ROLE}}/$ROLE/g" \
    -e "s/{{SCOPE}}/$SCOPE/g" \
    -e "s/{{OVUM}}/$OVUM/g" \
    -e "s|{{OVUM_NAME}}|$OVUM_NAME|g" \
    -e "s|{{PHP_VERSION}}|$PHP_VERSION|g" \
    -e "s|{{SLICE_NOTE}}|$SLICE_NOTE|g" \
    "$TEMPLATE" > "$CONTEXT_FILE"

cat >> "$CONTEXT_FILE" <<EOF

---

## LOADED CODEBASE SLICE

$(cat "$SLICE_FILE")

---

Ready. You are ${ROLE}[${SCOPE}] for [${OVUM}]. Awaiting questions.
EOF

# --- Report ---
echo ""
echo "[$ROLE:$SCOPE] Context ready for OVUM [$OVUM] ($OVUM_NAME)"
echo "[$ROLE:$SCOPE] Slice: $SLICE_FILE ($SLICE_LINES lines)"
echo "[$ROLE:$SCOPE] Context file: $CONTEXT_FILE"
echo "[$ROLE:$SCOPE] Model: gemini-2.5-flash"
echo ""
echo "---"
echo "Launching interactive session..."
echo "Context injected as first message. Ask your questions after prompt loads."
echo ""

# --- Launch Gemini with context as initial prompt ---
# Uses one-shot prompt to inject context, then relies on Gemini's
# interactive follow-up. If this doesn't stay interactive with your
# Gemini CLI version, use the manual approach:
#   1. Run: gemini -m gemini-2.5-flash
#   2. First message: paste contents of $CONTEXT_FILE
#
# [THINK] @majkee: Gemini CLI behavior with piped stdin varies by version.
# Test and adapt. The context file at $CONTEXT_FILE is the real deliverable.

gemini -m gemini-2.5-flash "$(cat "$CONTEXT_FILE")"
