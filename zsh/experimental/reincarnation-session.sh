#!/usr/bin/env bash
# reincarnation-session.sh — tmux bed: claude-0, claude-1, codex-0
# Adds a raw pipe-pane transcript per window, keyed by window name from
# keystroke one — ground truth independent of each agent's own session
# store (claude's UUID .jsonl / codex's session_index.jsonl).
#
# Usage: reincarnation-session.sh [logdir]
set -euo pipefail

SESSION="reincarnation"
WORKDIR="${REINCARNATION_WORKDIR:-$HOME/ia-sync}"
LOGDIR="${1:-/tmp/${SESSION}-logs-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$LOGDIR"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session '$SESSION' already exists — attach with: tmux attach -t $SESSION" >&2
  exit 1
fi

tmux new-session -d -s "$SESSION" -n claude-0 -c "$WORKDIR"
tmux new-window  -t "$SESSION"    -n claude-1 -c "$WORKDIR"
tmux new-window  -t "$SESSION"    -n codex-0  -c "$WORKDIR"

tmux pipe-pane -t "$SESSION:claude-0" -o "cat >> '$LOGDIR/claude-0.raw.log'"
tmux pipe-pane -t "$SESSION:claude-1" -o "cat >> '$LOGDIR/claude-1.raw.log'"
tmux pipe-pane -t "$SESSION:codex-0"  -o "cat >> '$LOGDIR/codex-0.raw.log'"

# fresh, interactive — no --continue/--resume, so each gets a brand-new session id
tmux send-keys -t "$SESSION:claude-0" 'claude' Enter
tmux send-keys -t "$SESSION:claude-1" 'claude' Enter
tmux send-keys -t "$SESSION:codex-0"  'codex'  Enter

echo "raw per-window logs: $LOGDIR"
echo "attach:              tmux attach -t $SESSION"
