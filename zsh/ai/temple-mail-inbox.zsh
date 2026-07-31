#!/usr/bin/env zsh
# temple-mail-inbox.zsh — read-side helper (Task 1 / 0008 Stage-1 completion)
# host: office  (MACHINE_NAME=office)
# implements: decision 0008 Stage 1 — mail round-trip, read side
# rule: LIST ONLY — never auto-reads content. Surface count+metadata, then ask-first (boot-order note below).
# rule: zero side effects — does NOT create directories; temple-mail creates them on send.
# rule: exits quietly (0) when inbox is absent or empty — boot never errors on a silent inbox.
#
# Interface:
#   temple-mail-inbox <origin>:<agent>
#
# Output (stdout):
#   Quiet when nothing unread. When items exist:
#     "INBOX <origin>:<agent> — N unread item(s) [+ M toAll broadcast(s)]:"
#     "  <sender>.<scope>.<date>  [toAll: <sender>.<scope>.<date>]"
#   No content is printed — just the identifiers. Caller decides whether to read.
#
# Boot-order note:
#   Source after temple-project-map.zsh. Call once per saddle-boot or project-switch.
#   Convention: if output is non-empty, ask the operator: "I see inbox items — read them now?"
#   Do NOT auto-cat contents (ask-first rule; _mail/README.md).
#
# Depends on: temple-project-map.zsh (P0) — sources automatically if not already loaded.

# --- Load P0 if needed ---
if (( ${+functions[temple-project-root]} == 0 )); then
  _temple_inbox_map="${0:h}/temple-project-map.zsh"
  if [[ -f "$_temple_inbox_map" ]]; then
    source "$_temple_inbox_map"
  else
    print -u2 "temple-mail-inbox: cannot find temple-project-map.zsh — source it first"
    return 1
  fi
  unset _temple_inbox_map
fi

temple-mail-inbox() {
  local _usage="Usage: temple-mail-inbox <origin>:<agent>"

  local address="$1"
  if [[ -z "$address" ]]; then
    print -u2 "$_usage"
    return 1
  fi

  # Split <origin>:<agent>
  local origin="${address%%:*}"
  local agent="${address##*:}"
  if [[ -z "$origin" || -z "$agent" || "$origin" == "$address" ]]; then
    print -u2 "temple-mail-inbox: address must be <origin>:<agent>, got '$address'"
    return 1
  fi

  # Resolve repo-root via P0
  local root
  root="$(temple-project-root "$origin")" || return 1

  # --- Agent-specific inbox ---
  local inbox_dir="${root}/_mail/${agent}/inbox"
  local agent_items=()
  if [[ -d "$inbox_dir" ]]; then
    # Collect files (filenames only, no path, no cat)
    for f in "${inbox_dir}"/*.md(N); do
      [[ -f "$f" ]] && agent_items+=("$(basename "$f")")
    done
  fi

  # --- toAll/inbox (global broadcasts — always live in reposoma, not the project being checked) ---
  # Recalibration reminders and other global broadcasts land in reposoma/_mail/toAll/inbox/.
  # Always resolve from reposoma so any project boot surfaces them.
  local reposoma_root
  reposoma_root="$(temple-project-root reposoma 2>/dev/null)" || reposoma_root=""
  local toall_dir="${reposoma_root}/_mail/toAll/inbox"
  local toall_items=()
  if [[ -d "$toall_dir" ]]; then
    for f in "${toall_dir}"/*.md(N); do
      [[ -f "$f" ]] && toall_items+=("$(basename "$f")")
    done
  fi

  # --- Quiet when nothing unread ---
  local agent_count="${#agent_items[@]}"
  local toall_count="${#toall_items[@]}"
  if (( agent_count == 0 && toall_count == 0 )); then
    return 0
  fi

  # --- Build summary line ---
  local summary="INBOX ${address} —"
  if (( agent_count > 0 && toall_count > 0 )); then
    summary+=" ${agent_count} unread item(s) + ${toall_count} toAll broadcast(s)"
  elif (( agent_count > 0 )); then
    summary+=" ${agent_count} unread item(s)"
  else
    summary+=" ${toall_count} toAll broadcast(s)"
  fi
  summary+=":"
  print -- "$summary"

  # List agent inbox items
  for item in "${agent_items[@]}"; do
    print "  ${item}"
  done

  # List toAll items (labelled)
  for item in "${toall_items[@]}"; do
    print "  [toAll] ${item}"
  done

  return 0
}
