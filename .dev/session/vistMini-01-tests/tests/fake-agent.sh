#!/usr/bin/env bash
# Trusted fixture only: invoked via exec -a codex|claude, never a real agent.
set -u
mode=$1 log=$2 control=$3
draft= ghost= style=legacy cursor_start=0 multiline=0
case $mode in
    claude-*) style=claude;; codex-*) style=codex;;
esac
stty -echo -icanon min 0 time 1
draw() {
    local row=5 glyph='❯' ansi= footer='⏵⏵ auto mode on (shift+tab to cycle)'
    printf '\033[2J\033[H'
    if [[ $style == legacy ]]; then printf '❯ %s' "$draft"; return; fi
    [[ $style != codex ]] || glyph='›'
    if [[ $mode == *historical ]]; then
        row=12
        printf '%s old prompt-looking transcript\n• Working (historical • esc to interrupt)' "$glyph"
    fi
    if [[ $mode == codex-busy || -e $control/busy-now ]]; then
        if [[ $style == codex ]]; then printf '\033[%d;1H• Working (49s • esc to interrupt)' "$((row-1))"; else footer+=' · esc to interrupt'; fi
    fi
    printf '\033[%d;1H\033[39m%s' "$((row+1))" "$glyph"
    if [[ $style == claude ]]; then printf '\302\240'; else printf '\033[0m\033[48;2;57;60;66m '; fi
    case $mode in
        *-bg-rgb) ansi=$'\033[48;2;10;20;30m';;
        *-rgb) ansi=$'\033[38;2;10;20;30m';;
        *-bg-indexed) ansi=$'\033[48;5;2m';;
        *-indexed) ansi=$'\033[38;5;2m';;
    esac
    printf '%s' "$ansi"
    if [[ -n $ghost ]]; then
        if [[ $mode == *reset-dim ]]; then printf '\033[0;2m%s\033[0m' "$ghost"; else printf '\033[2m%s\033[0m' "$ghost"; fi
    fi
    printf '%s\033[0m' "$draft"
    if ((multiline)); then
        printf '\033[%d;1H' "$((row+2))"
        [[ $mode != *dim-continuation-start ]] || printf '\033[2m'
        printf 'synthetic continuation\033[0m'
    fi
    if [[ $mode != *missing-footer ]]; then
        if [[ $style == claude ]]; then
            printf '\033[%d;1H────────────────────────────────────────────────────\033[%d;1H  %s' "$((row+3))" "$((row+4))" "$footer"
        else
            printf '\033[%d;1H  GPT-6.1-Sol high · ~/reposoma · cartan|astrobley · synthetic · Context 50%% left · Main…' "$((row+3))"
            printf '\033[%d;1H  ← for agents · ? for shortcuts' "$((row+4))"
        fi
    fi
    if ((cursor_start)); then printf '\033[%d;3H' "$((row+1))"
    elif ((multiline)); then printf '\033[%d;12H' "$((row+2))"
    elif [[ -n $ghost ]]; then printf '\033[%d;3H' "$((row+1))"
    else printf '\033[%d;%dH' "$((row+1))" "$((${#draft}+3))"; fi
}
case $mode in
    *-continuation-start) ghost='synthetic suggestion'; multiline=1; cursor_start=1; draw;;
    *-suggestion|*-reset-dim) ghost='synthetic suggestion'; draw;;
    codex-placeholder|codex-busy|codex-historical) ghost='Ask Codex to do anything'; draw;;
    codex-alternative) ghost='unknown suggestion'; draw;;
    *-typed-start) draft='synthetic operator draft'; cursor_start=1; draw;;
    *-typed|*-rgb|*-indexed) draft='synthetic operator draft'; draw;;
    *-mixed) ghost='dim hint'; draft='non-dim draft'; draw;;
    *-whitespace) draft='   '; draw;;
    *-multiline) draft='synthetic first line'; multiline=1; draw;;
    claude-busy) ghost='synthetic suggestion'; : > "$control/busy-now"; draw;;
    occupied) draft='operator draft: keep me'; draw;;
    whitespace) draft='   '; draw;;
    busy) printf '\033[2J\033[Hesc to interrupt';;
    unknown) printf '\033[2J\033[Hnot a composer';;
    *) draw;;
esac
: > "$control/ready"
busy_drawn=0
while :; do
    [[ ! -e $control/exit-now ]] || exit 0
    if [[ -e $control/busy-now && $busy_drawn == 0 ]]; then busy_drawn=1; draw; fi
    if IFS= read -r -n 1 -t 0.025 char; then
        case $char in
            $'\r'|$'\n'|'') printf '%s\n' "$draft" >> "$log"; draft=; draw;;
            *) ghost=; draft+=$char; draw;;
        esac
    fi
done
