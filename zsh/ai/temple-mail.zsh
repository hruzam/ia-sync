#!/usr/bin/env zsh
# temple-mail.zsh — the temple mail primitive (A)
# host: office  (MACHINE_NAME=office)
# implements: decision 0008 Stage 1 — L7 mail physical-staging transport
# addressing: _mail/README.md convention (gaveled 2026-06-25)
#   filename: <receiver-repo>/_mail/<agent>/inbox/<sender>.<scope>.<YYYY-MM-DD>.md
#   receiver owns; no sent-copy; replies return to sender's inbox
#
# Interface:
#   temple-mail <origin>:<agent>  <scope>  [<body-file | ->]  [--from <sender-origin>:<sender-agent>]
#
# Examples:
#   temple-mail piql.dev:houston  doorbell-stale  body.md  --from temple:houston
#   echo "body" | temple-mail piql.dev:houston  doorbell-stale  -  --from temple:houston
#
# Depends on: temple-project-map.zsh (P0) — source it before calling temple-mail

# Ensure P0 is available (plain assignment — not local; this runs at top level, not inside a function)
if (( ${+functions[temple-project-root]} == 0 )); then
  _temple_mail_map_file="${0:h}/temple-project-map.zsh"
  if [[ -f "$_temple_mail_map_file" ]]; then
    source "$_temple_mail_map_file"
  else
    print -u2 "temple-mail: cannot find temple-project-map.zsh — source it first"
    return 1
  fi
  unset _temple_mail_map_file
fi

temple-mail() {
  local _usage="Usage: temple-mail <origin>:<agent> <scope> [<body-file|->] [--from <sender-origin>:<sender-agent>]"

  # Parse positional arguments: address scope [body_src] and optional --from
  local address="$1" scope="$2"
  local body_src="-" sender=""
  shift 2 2>/dev/null || true

  # Remaining args: [body-file|-] [--from <sender>]
  while (( $# > 0 )); do
    case "$1" in
      --from)
        sender="$2"
        shift 2
        ;;
      *)
        body_src="$1"
        shift
        ;;
    esac
  done

  if [[ -z "$address" || -z "$scope" ]]; then
    print -u2 "$_usage"
    return 1
  fi

  # Split destination address into origin:agent
  local dest_origin="${address%%:*}"
  local dest_agent="${address##*:}"
  if [[ -z "$dest_origin" || -z "$dest_agent" || "$dest_origin" == "$address" ]]; then
    print -u2 "temple-mail: address must be <origin>:<agent>, got '$address'"
    return 1
  fi

  # Parse sender
  local sender_origin sender_agent
  if [[ -n "$sender" ]]; then
    sender_origin="${sender%%:*}"
    sender_agent="${sender##*:}"
  else
    # Default sender: caller env or fallback
    sender_origin="${TEMPLE_MAIL_FROM_ORIGIN:-temple}"
    sender_agent="${TEMPLE_MAIL_FROM_AGENT:-houston}"
  fi
  local sender_short="${sender_agent}"

  # Resolve destination repo-root via P0
  local dest_root
  dest_root="$(temple-project-root "$dest_origin")" || return 1

  # Build inbox path: <repo-root>/_mail/<agent>/inbox/
  local inbox_dir="${dest_root}/_mail/${dest_agent}/inbox"
  mkdir -p "$inbox_dir" || {
    print -u2 "temple-mail: cannot create inbox '$inbox_dir'"
    return 1
  }

  # Filename: <sender>.<scope>.<YYYY-MM-DD>.md
  local date_stamp
  date_stamp="$(date +%Y-%m-%d)"
  local filename="${sender_short}.${scope}.${date_stamp}.md"
  local dest_file="${inbox_dir}/${filename}"

  # Read body
  local body
  if [[ "$body_src" == "-" ]]; then
    body="$(cat)"
  elif [[ -f "$body_src" ]]; then
    body="$(cat "$body_src")"
  else
    print -u2 "temple-mail: body source '$body_src' not found"
    return 1
  fi

  # Write frontmatter + body into receiver's inbox
  cat > "$dest_file" <<MAIL_EOF
---
from: ${sender_origin}:${sender_agent}
to: ${dest_origin}:${dest_agent}
scope: ${scope}
date: ${date_stamp}
host: ${MACHINE_NAME:-office}
---

${body}
MAIL_EOF

  print "temple-mail: delivered → ${dest_file}"
  # No sent-copy (receiver owns; filesystem is the state machine)
}
