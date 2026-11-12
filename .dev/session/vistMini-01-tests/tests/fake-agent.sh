#!/usr/bin/env bash
# Trusted fixture only: invoked via exec -a codex|claude, never a real agent.
set -u
mode=$1 log=$2 control=$3
draft=
stty -echo -icanon min 0 time 1
draw() { printf '\033[2J\033[H❯ %s' "$draft"; }
case $mode in
    occupied) draft='operator draft: keep me'; draw;;
    whitespace) draft='   '; draw;;
    busy) printf '\033[2J\033[Hesc to interrupt';;
    unknown) printf '\033[2J\033[Hnot a composer';;
    *) draw;;
esac
while :; do
    [[ ! -e $control/exit-now ]] || exit 0
    if IFS= read -r -n 1 -t 0.025 char; then
        case $char in
            $'\r'|$'\n'|'') printf '%s\n' "$draft" >> "$log"; draft=; draw;;
            *) draft+=$char; draw;;
        esac
    fi
done
