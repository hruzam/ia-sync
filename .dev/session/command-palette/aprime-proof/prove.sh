#!/usr/bin/env bash
# aprime-proof/prove.sh — proves the A' (palette v2) "frontmatter projection"
# mechanism on an isolated scratch scope. Does NOT touch any real config file.
set -e

PROOF_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZSH_ROOT="$(cd "$PROOF_ROOT/../../../zsh" && pwd)"

echo "=================================================================="
echo "[a] palette-map-gen.py --root aprime-proof  (writes palette.map)"
echo "=================================================================="
python3 "$ZSH_ROOT/ai/palette-map-gen.py" --root "$PROOF_ROOT"
echo
echo "--- aprime-proof/palette.map ---"
cat "$PROOF_ROOT/palette.map"

echo
echo "=================================================================="
echo "[b] palette-map-gen.py --root aprime-proof --check  (discipline audit)"
echo "=================================================================="
python3 "$ZSH_ROOT/ai/palette-map-gen.py" --root "$PROOF_ROOT" --check || true

echo
echo "=================================================================="
echo "[c] palette-help.py  (rendered panel — scratch scope)"
echo "=================================================================="
python3 "$ZSH_ROOT/ai/palette-help.py" "$PROOF_ROOT/scratch/keyboard.zsh"

echo
echo "=================================================================="
echo "[d] palette-help.py  (READ-ONLY render of the real system/keyboard.zsh)"
echo "=================================================================="
python3 "$ZSH_ROOT/ai/palette-help.py" "$ZSH_ROOT/system/keyboard.zsh"
