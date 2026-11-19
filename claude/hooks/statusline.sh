#!/usr/bin/env bash
# statusline.sh — Claude Code status line (scheme saved 2026-11-13)
# Order: model effort . CWD . context left . session name . session ID . transcript jsonl
# Reads the statusLine JSON on stdin; session name is re-read every render, so /rename shows live.
input=$(cat)
j() { printf '%s' "$input" | jq -r "$1 // empty" 2>/dev/null; }

model=$(j '.model.display_name')
effort=$(j '.effort.level // .effort // .reasoning_effort')
[ -z "$effort" ] && effort=$(jq -r '.effortLevel // empty' ~/.claude/settings.json 2>/dev/null)
cwd=$(j '.workspace.current_dir // .cwd')
ctx=$(j '.context_window.remaining_percentage')
name=$(j '.session_name // .session.name')
sid=$(j '.session_id')
tp=$(j '.transcript_path')

dim='\e[2m'; grn='\e[01;32m'; wht='\e[01;37m'; cyn='\e[36m'; rst='\e[00m'
sep=" ${dim}.${rst} "
out="${grn}${model:-?}${rst}"
[ -n "$effort" ] && out+=" ${cyn}${effort}${rst}"
out+="${sep}${wht}${cwd/#$HOME/\~}${rst}"
[ -n "$ctx" ] && ctxs="${ctx%.*}%" || ctxs="?"
out+="${sep}ctx ${ctxs} left"
out+="${sep}${name:--}"
out+="${sep}${dim}${sid:-?}${rst}"
out+="${sep}${dim}${tp/#$HOME/\~}${rst}"
printf '%b' "$out"
