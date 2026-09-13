#!/usr/bin/env bash
# remote-cli engine — sourced by zsh or executed with bash; no work on source.
# Uses the caller's tmux server and pane; explicit targets follow tmux target syntax.
_remote_cli() {
    local action="${1:-help}" target="${2:-${TMUX_PANE:-}}" window_id policy
    local resolved session_id history_limit output
    if (( $# > 2 )); then
        printf '%s\n' '[remote-cli] usage: remote-{fit,wide,scroll,status} [session:window | %pane]' >&2
        return 2
    fi
    case "$action" in
        help|-h|--help)
            cat <<'HELP'
remote-cli — terminal view controls
  remote-fit [target]     follow the most recently active device (tmux: latest)
  remote-wide [target]    use the largest attached device (tmux: largest)
  remote-scroll [target]  enable session mouse scrolling and at least 50,000 history lines
  remote-status [target]  show window sizing, mouse and scrollback state
  remote-help            this panel

Target defaults to this shell's tmux pane. Outside tmux, supply a session,
session:window or %pane ID. Fit/wide affect the whole window, including linked
views. Scroll sets session options; linked panes still share their history.
No server defaults change. Repeat scroll after recreating a session.

Keyboard fallback (default prefix): Ctrl+B, [; PgUp/PgDn; q to leave copy mode.
Old discarded lines cannot be recovered. Application mouse/alternate-screen
handling is not changed; use copy mode if a TUI consumes the wheel.

One shared pane still has one size. Fit is for alternating PC/phone use.
Connections: phone = bed office; other PC = tso -t office (or home).
No pocket-specific session is required. Select existing sessions with Ctrl+B, s.

Standalone (host shell, including bash):
  bash ~/.config/zsh/remote-cli/remote-cli.sh fit 'agentive:0'
Guide: ~/reposoma/raw.guides/remote-cli/GUIDE.md
HELP
            return 0 ;;
        fit) policy=latest ;;
        wide) policy=largest ;;
        scroll|status) ;;
        *) printf '[remote-cli] unknown action: %s; use remote-help\n' "$action" >&2; return 2 ;;
    esac
    if [[ -z "$target" ]]; then
        printf '%s\n' '[remote-cli] outside tmux: supply a target, e.g. remote-fit agentive:0' >&2
        return 2
    fi
    # Pin the session too: a linked window ID alone loses the selected session.
    resolved=$(/usr/bin/tmux display-message -p -t "$target" '#{session_id}:#{window_id}.#{pane_id}') || return 1
    if [[ ! "$resolved" =~ ^[$][0-9]+:@[0-9]+[.]%[0-9]+$ ]]; then
        printf '[remote-cli] no pane for target: %s\n' "$target" >&2
        return 1
    fi
    session_id="${resolved%%:*}"
    window_id="${resolved#*:}"
    window_id="${window_id%.*}"
    if [[ "$action" == scroll ]]; then
        history_limit=$(/usr/bin/tmux display-message -p -t "$resolved" '#{history-limit}') || return 1
        if [[ ! "$history_limit" =~ ^[0-9]+$ ]]; then
            printf '[remote-cli] invalid history-limit for %s\n' "$session_id" >&2
            return 1
        fi
        if (( history_limit < 50000 )); then
            /usr/bin/tmux set-option -t "$session_id" history-limit 50000 || return 1
        fi
        /usr/bin/tmux set-option -t "$session_id" mouse on || return 1
    elif [[ "$action" != status ]]; then
        /usr/bin/tmux set-option -w -t "$window_id" window-size "$policy" || return 1
    fi
    output='remote-cli: #{session_name}:#{window_index} (#{window_id}) policy=#{window-size} size=#{window_width}x#{window_height} cells'
    if [[ "$action" == scroll || "$action" == status ]]; then
        output+=$'\n''scroll: mouse=#{mouse} history=#{history_size}/#{history_limit} lines session-limit=#{history-limit} alternate=#{alternate_on}'
    fi
    /usr/bin/tmux display-message -p -t "$resolved" "$output"
}

# Bash execution entry; sourcing from either shell only defines the function.
if [[ -n "${BASH_VERSION:-}" && "${BASH_SOURCE[0]}" == "$0" ]]; then
    _remote_cli "$@"
fi
