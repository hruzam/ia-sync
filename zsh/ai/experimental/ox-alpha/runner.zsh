#!/usr/bin/env zsh
# Ox Alpha experimental runner — executed by ai/experimental.zsh.
# Usage: exp-run ox-alpha [--stream|--no-stream] <prompt> | chat

_openrouter_load_key() {
  local secrets_path="$HOME/.config/zsh/.env/secrets.zsh"
  [[ -f "$secrets_path" ]] && source "$secrets_path"

  if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
    print -u2 'ox-alpha: OPENROUTER_API_KEY is not set in ~/.config/zsh/.env/secrets.zsh'
    return 1
  fi
}

_ox_alpha_help() {
  cat <<'EOF'
Usage:
  ox-alpha [--stream|--no-stream] <prompt>
  ox-alpha chat

Runs the OpenRouter stealth/ox-alpha experimental reasoning model.
Default: --stream (raw server-sent events). Use --no-stream for formatted JSON.
chat keeps multi-turn history only for the active terminal process; exit with /exit or Ctrl-D.
The API key is loaded only at runtime from ~/.config/zsh/.env/secrets.zsh.
EOF
}

_ox_alpha_chat() {
  local messages='[]'
  local prompt payload response assistant answer

  _openrouter_load_key || return 1
  print 'ox-alpha chat — /exit or Ctrl-D to leave; history stays in this process only.'

  while true; do
    print -n 'ox-alpha> '
    if ! IFS= read -r prompt; then
      print ''
      break
    fi

    case "$prompt" in
      '') continue ;;
      /exit|/quit) break ;;
    esac

    messages="$(jq -c --arg prompt "$prompt" '. + [{role: "user", content: $prompt}]' <<< "$messages")" || return 1
    payload="$(jq -n --argjson messages "$messages" '{
      model: "stealth/ox-alpha",
      stream: false,
      reasoning: {enabled: true},
      messages: $messages
    }')" || return 1

    if ! response="$(curl --fail-with-body --silent --show-error \
      https://openrouter.ai/api/v1/chat/completions \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $OPENROUTER_API_KEY" \
      -d "$payload")"; then
      print -u2 -- "$response"
      messages="$(jq -c '.[0:-1]' <<< "$messages")"
      continue
    fi

    if ! assistant="$(jq -ec '.choices[0].message' <<< "$response")"; then
      print -u2 -- "$response"
      messages="$(jq -c '.[0:-1]' <<< "$messages")"
      continue
    fi

    answer="$(jq -r '.content // ""' <<< "$assistant")"
    print -- "assistant> $answer"
    messages="$(jq -c --argjson assistant "$assistant" '. + [{
      role: "assistant",
      content: $assistant.content,
      reasoning_details: $assistant.reasoning_details
    }]' <<< "$messages")" || return 1
  done
}

_ox_alpha() {
  local stream=true

  case "${1:-}" in
    chat)
      shift
      if [[ $# -ne 0 ]]; then
        _ox_alpha_help
        return 2
      fi
      _ox_alpha_chat
      return
      ;;
    --stream) stream=true; shift ;;
    --no-stream) stream=false; shift ;;
    --help|-h) _ox_alpha_help; return 0 ;;
  esac

  if [[ $# -eq 0 ]]; then
    _ox_alpha_help
    return 2
  fi

  local prompt="$*"
  local payload
  payload="$(jq -n --arg prompt "$prompt" --argjson stream "$stream" '{
    model: "stealth/ox-alpha",
    stream: $stream,
    reasoning: {enabled: true},
    messages: [{role: "user", content: $prompt}]
  }')" || return 1

  _openrouter_load_key || return 1

  if [[ "$stream" == true ]]; then
    curl --fail-with-body --no-buffer --silent --show-error \
      https://openrouter.ai/api/v1/chat/completions \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $OPENROUTER_API_KEY" \
      -d "$payload"
  else
    curl --fail-with-body --silent --show-error \
      https://openrouter.ai/api/v1/chat/completions \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $OPENROUTER_API_KEY" \
      -d "$payload" | jq .
  fi
}

_ox_alpha "$@"
