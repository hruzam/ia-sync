#!/usr/bin/env bash
# oraculum-bash-whitelist.sh — agent-scoped PreToolUse[Bash] whitelist (token economy by mechanism)
#
# Wired from oraculum's frontmatter `hooks:`. Another seat adopting the pattern gets its own
# <seat>-bash-whitelist.sh (its own list) — do not widen this one to serve two seats. Fires only while that
# agent runs. A carrier/head seat keeps Bash for bookkeeping; everything else is denied with a
# reason the agent sees, so it routes the work to a spawn instead.
#
# Contract (Claude Code PreToolUse): JSON on stdin, command at .tool_input.command.
#   exit 0 = allow · exit 2 + stderr = deny (stderr is shown to the agent).
# Economy fence, NOT a security boundary — it stops the habit, not a determined adversary.
# Fails closed: unparseable input or missing jq = deny.
#
# Origin: CS.oraculum-bash-whitelist-hook.2026-10-07 · built by atlas-ui 2026-10-08.
# Pattern note: ~/ia-sync/claude/hooks/README.md (adopt by pointer, do not copy the list).

ROUTE="spawn @delta / @vector / @trajectory for this; carrier Bash is bookkeeping only"

deny() { echo "bash-whitelist: $1 — $ROUTE" >&2; exit 2; }

command -v jq >/dev/null 2>&1 || deny "jq missing, cannot read the command (fail closed)"
INPUT=$(cat)                                   # capture stdin ONCE — jq must not consume it twice

# ── subagent exemption ──────────────────────────────────────────────────────
# This frontmatter hook (wired only on oraculum) fires on the carrier AND on every subagent oraculum
# spawns — undocumented inheritance, observed 2026-10-13 (delta/trajectory Bash denied). Judge the
# carrier ONLY: subagents are bound by their own tools: lists, not this economy fence. agent_id is
# present in a subagent's hook input, absent on the main carrier thread → non-empty agent_id = spawn.
# See patch.hook-subagent-exempt.atlas.2026-10-13.md (risk §6: spawns gain fully unrestricted Bash).
[ -n "$(jq -r '.agent_id // empty' 2>/dev/null <<< "$INPUT")" ] && exit 0

CMD=$(jq -r '.tool_input.command // empty' 2>/dev/null <<< "$INPUT") || deny "unreadable hook input (fail closed)"
[ -z "$CMD" ] && exit 0

# ── pass 1: quote-aware mask ────────────────────────────────────────────────
# Drop quote chars; neutralise separators / redirects / whitespace INSIDE quotes to "_" so words
# stay whole and quoted text cannot fake structure. Flag live substitution: $( ` <( >( outside
# quotes, and $( ` inside double quotes.
m=""; q=""; subst=0; n=${#CMD}
for ((i = 0; i < n; i++)); do
  c=${CMD:i:1}; nx=${CMD:i+1:1}
  if [ "$q" = "'" ]; then
    if [ "$c" = "'" ]; then q=""; else case "$c" in [\;\&\|\<\>\$\`\(\)\ $'\t'$'\n']) m+="_";; *) m+="$c";; esac; fi
    continue
  fi
  if [ "$q" = '"' ]; then
    if [ "$c" = '\' ]; then m+="_"; ((i++)); continue; fi
    if [ "$c" = '"' ]; then q=""; continue; fi
    if [ "$c" = '`' ] || { [ "$c" = '$' ] && [ "$nx" = '(' ]; }; then subst=1; fi
    case "$c" in [\;\&\|\<\>\$\`\(\)\ $'\t'$'\n']) m+="_";; *) m+="$c";; esac
    continue
  fi
  case "$c" in
    "'"|'"') q=$c ;;
    '\') m+="_"; ((i++)) ;;
    '`') subst=1 ;;
    '$') [ "$nx" = '(' ] && subst=1; m+="$c" ;;
    '<'|'>') [ "$nx" = '(' ] && subst=1; m+="$c" ;;
    *) m+="$c" ;;
  esac
done
[ -n "$q" ] && deny "unbalanced quotes (fail closed)"
[ "$subst" = 1 ] && deny "command substitution \$( ) / backticks / <( ) cannot be vetted"

# Protect fd-dup redirects (2>&1, &>) from the & separator split.
m=${m//>&/>+}; m=${m//&>/+>}

# ── pass 2: split on ; & | newline — every segment must pass ───────────────
IFS=$';&|\n' read -r -d '' -a SEGS <<< "$m"

home_tunnel="$HOME/.config/zsh/ai/tunnel-codex.zsh"

for seg in "${SEGS[@]}"; do
  read -r -a W <<< "$seg"
  [ ${#W[@]} -eq 0 ] && continue

  # ── redirects: peel off, vet, keep argv ──
  argv=(); redir_md=(); k=0
  while [ $k -lt ${#W[@]} ]; do
    w=${W[k]}
    if [[ $w == '<<'* ]]; then
      deny "heredoc (<<) — append with printf '...\\n' >> file.md instead"
    elif [[ $w =~ ^[0-9]*\<(.*)$ ]]; then                       # input redirect: read-only, ok
      [ -z "${BASH_REMATCH[1]}" ] && ((k++))
    elif [[ $w =~ ^([0-9]*|\+)(\>\>?)(.*)$ ]]; then
      fd=${BASH_REMATCH[1]}; op=${BASH_REMATCH[2]}; tgt=${BASH_REMATCH[3]}
      if [ -z "$tgt" ]; then ((k++)); tgt=${W[k]}; fi
      if [ "$tgt" = /dev/null ] || [[ $tgt =~ ^\+[0-9]$ ]]; then :   # discard / fd-dup
      elif [ "$op" = '>>' ] && [[ -z $fd || $fd == 1 ]] && [[ $tgt == *.md ]]; then redir_md+=("$tgt")
      else deny "write redirect to '$tgt' (only >> *.md from echo/printf)"; fi
    elif [[ $w == *[\<\>]* ]]; then
      deny "unvettable redirect in '$w'"
    else
      argv+=("$w")
    fi
    ((k++))
  done
  [ ${#argv[@]} -eq 0 ] && continue

  # Peel a leading tunnel env prefix so `TUNNEL_CODEX_TIMEOUT=1800 zsh …tunnel… ask "…"`
  # resolves to the helper, not to the assignment word (tunnel protocol Rule 4). Only the
  # two tunnel vars, each shape-checked; any other prefix is left in place → vetted/denied
  # normally below, so this cannot widen the whitelist.
  e=0
  while [ $e -lt ${#argv[@]} ]; do
    case "${argv[e]}" in
      TUNNEL_CODEX_TIMEOUT=*) [[ ${argv[e]} =~ ^TUNNEL_CODEX_TIMEOUT=[0-9]+$ ]] || break; ((e++)) ;;
      TUNNEL_CODEX_STATE=*)   [[ ${argv[e]} == TUNNEL_CODEX_STATE=/*tunnel.state.json ]] || break; ((e++)) ;;
      *) break ;;
    esac
  done
  [ $e -gt 0 ] && argv=("${argv[@]:e}")
  [ ${#argv[@]} -eq 0 ] && continue
  cmd=${argv[0]}

  if [ ${#redir_md[@]} -gt 0 ] && [[ $cmd != echo && $cmd != printf ]]; then
    deny "'$cmd' >> file — only echo/printf may append to .md"
  fi

  case "$cmd" in
    git)
      a=1
      while :; do
        case "${argv[a]}" in
          -C) a=$((a + 2)) ;;
          --no-pager) a=$((a + 1)) ;;
          *) break ;;
        esac
      done
      case "${argv[a]}" in
        log|status|diff|show|hash-object|ls-files|ls-tree|rev-parse|add|commit|mv|rm) ;;
        *) deny "git ${argv[a]:-<none>}" ;;
      esac ;;
    sed)
      [ "${argv[1]}" = -n ] || deny "sed without -n (only 'sed -n' inspection)"
      for x in "${argv[@]:1}"; do [[ $x == -i* || $x == --in-place* ]] && deny "sed -i"; done ;;
    ls|cat|head|tail|wc|grep|cmp|diff|sha256sum|cd|pwd|date|hostname|jq|echo|printf) ;;
    zsh)
      case "${argv[1]}" in
        '~/.config/zsh/ai/tunnel-codex.zsh'|'$HOME/.config/zsh/ai/tunnel-codex.zsh'|'/home/hruzam/.config/zsh/ai/tunnel-codex.zsh'|"$home_tunnel") ;;
        *) deny "zsh ${argv[1]:-<none>} (only the tunnel helper)" ;;
      esac
      case "${argv[2]}" in
        ask|send)    [ ${#argv[@]} -eq 4 ] || deny "tunnel ${argv[2]} takes exactly one quoted argument" ;;
        read|status) [ ${#argv[@]} -eq 3 ] || deny "tunnel ${argv[2]} takes no argument" ;;
        *) deny "tunnel verb '${argv[2]:-<none>}' — only ask/send/read/status (open/close/resume/steer stay carrier/majkee)" ;;
      esac ;;
    export)
      [ ${#argv[@]} -eq 2 ] && [[ ${argv[1]} == TUNNEL_CODEX_STATE=* ]] || deny "export (only TUNNEL_CODEX_STATE=…)" ;;
    *) deny "out of whitelist ($cmd)" ;;
  esac
done

exit 0
