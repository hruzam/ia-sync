#!/usr/bin/env bash
# remote-cli engine — sourced by zsh or executed with bash; no work on source.
# Uses the caller's tmux server and pane; explicit targets follow tmux target syntax.
_remote_cli() {
    local action="${1:-help}" target="${2:-${TMUX_PANE:-}}" window_id policy
    if (( $# > 2 )); then
        printf '%s\n' '[remote-cli] usage: remote-{fit,wide,status} [session:window | %pane]' >&2
        return 2
    fi
    case "$action" in
        help|-h|--help)
            cat <<'HELP'
remote-cli — terminal view controls
  remote-fit [target]     follow the most recently active device (tmux: latest)
  remote-wide [target]    use the largest attached device (tmux: largest)
  remote-status [target]  show window, effective policy and size in character cells
  remote-help            this panel

Target defaults to this shell's tmux pane. Outside tmux, supply session:window
or a %pane ID. Each change affects that whole window, including linked views,
for its lifetime. New windows keep the server's existing default.

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
        status) ;;
        *) printf '[remote-cli] unknown action: %s; use remote-help\n' "$action" >&2; return 2 ;;
    esac
    if [[ -z "$target" ]]; then
        printf '%s\n' '[remote-cli] outside tmux: supply a target, e.g. remote-fit agentive:0' >&2
        return 2
    fi
    # Resolve first, then pin the window ID; never fall back to another window.
    window_id=$(/usr/bin/tmux display-message -p -t "$target" '#{window_id}') || return 1
    if [[ ! "$window_id" =~ ^@[0-9]+$ ]]; then
        printf '[remote-cli] no window for target: %s\n' "$target" >&2
        return 1
    fi
    if [[ "$action" != status ]]; then
        /usr/bin/tmux set-option -w -t "$window_id" window-size "$policy" || return 1
    fi
    /usr/bin/tmux display-message -p -t "$window_id" \
        'remote-cli: #{session_name}:#{window_index} (#{window_id}) policy=#{window-size} size=#{window_width}x#{window_height} cells'
}

# Bash execution entry; sourcing from either shell only defines the function.
if [[ -n "${BASH_VERSION:-}" && "${BASH_SOURCE[0]}" == "$0" ]]; then
    _remote_cli "$@"
fi
