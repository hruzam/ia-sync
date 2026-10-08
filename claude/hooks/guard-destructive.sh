#!/usr/bin/env bash
# guard-destructive.sh — global deny-list for provably destructive Bash patterns.
# Wired from an agent's frontmatter hooks: PreToolUse[Bash] (currently houston.md).
# Contract: JSON on stdin, command at .tool_input.command · exit 2 + stderr = block · exit 0 = allow.
#
# Folded onto the table 2026-10-08 (atlas-ui). The live-only original read $TOOL_INPUT, which
# Claude Code never sets, so it passed everything — ISS.guard-destructive-reads-dead-env-var.2026-10-08.
# Patterns unchanged from the original; only the input read is fixed.

command -v jq >/dev/null 2>&1 || { echo "BLOCKED: guard-destructive needs jq to read the command (fail closed)" >&2; exit 2; }
INPUT=$(jq -r '.tool_input.command // empty' 2>/dev/null) || { echo "BLOCKED: unreadable hook input (fail closed)" >&2; exit 2; }
[ -z "$INPUT" ] && exit 0

# Universal destructive patterns
if printf '%s\n' "$INPUT" | grep -qE 'rm -rf /|DROP TABLE|mkfs|dd if=.*of=/dev|format [A-Z]:'; then
  echo "BLOCKED: destructive pattern detected" >&2
  exit 2
fi

# Never force-migrate production from agent context
if printf '%s\n' "$INPUT" | grep -qE 'artisan migrate:fresh|artisan migrate:reset|artisan migrate --force'; then
  echo "BLOCKED: destructive migration — run manually with full awareness" >&2
  exit 2
fi

exit 0
