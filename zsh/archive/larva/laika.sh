# ~/.config/zsh/larva/laika.sh
#!/bin/bash
# @Laika — one-shot scanner
# Usage: laika.sh [ovum] [repomix_output_file]
# Example: laika.sh fo ~/repomix-output.txt

OVUM="$1"
INPUT_FILE="$2"
OVUM_ROOT=""
case "$OVUM" in
    fo)  OVUM_ROOT="${PROJECT_FO_PATH:-$HOME/www/fantasyobchod}" ;;
    im)  OVUM_ROOT="${PROJECT_IM_PATH:-$HOME/www/freya}" ;;
    psd) OVUM_ROOT="${PROJECT_PSD_PATH:-$HOME/www/psdvs}" ;;
    pupa) OVUM_ROOT="${PROJECT_PUPA_PATH:-$HOME/www/kukla}" ;;
    *)
        echo "[ERROR] Unknown OVUM: $OVUM"
        exit 1
        ;;
esac

if [[ -z "$INPUT_FILE" || ! -f "$INPUT_FILE" ]]; then
    echo "Usage: laika.sh <ovum> <repomix_output_file>"
    echo "Example: laika.sh fo ~/repomix-output.txt"
    exit 1
fi

OUTPUT_DIR="$OVUM_ROOT/.larva/_knowledge"
TIMESTAMP=$(date +%Y%m%d_%H%M)
OUTPUT_FILE="$OUTPUT_DIR/laika_${TIMESTAMP}.md"
PROMPT_FILE="$HOME/.config/gemini/agents/laika.md"

mkdir -p "$OUTPUT_DIR"

if [[ -f "$PROMPT_FILE" ]]; then
    BASE_PROMPT=$(cat "$PROMPT_FILE")
else
    BASE_PROMPT="You are @Laika, one-shot codebase scanner for OVUM [$OVUM].
Your job: map structure, patterns, key dependencies, risks.
Output ONLY structured Markdown. No conversation.
Footer every output with: ---\n*Mapped by @Laika. Output persists.*"
fi

PROMPT="$BASE_PROMPT

OVUM: [$OVUM]

CODEBASE SNAPSHOT:
$(cat "$INPUT_FILE")"

gemini -m gemini-2.5-flash "$PROMPT" > "$OUTPUT_FILE"

echo "Output saved: $OUTPUT_FILE"