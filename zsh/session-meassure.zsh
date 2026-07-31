# Session spend logging helpers for `~/www/session`.

function _session_meassure_now_local() {
    emulate -L zsh
    local tz_name="${SESSION_MEASSURE_TZ:-Europe/Prague}"
    TZ="$tz_name" date "+%Y-%m-%d %H:%M:%S %Z (%z)"
}

function _session_meassure_now_utc() {
    emulate -L zsh
    date -u "+%Y-%m-%d %H:%M:%S UTC"
}

function _session_meassure_log_file() {
    emulate -L zsh
    local session_name="$1"
    echo "$HOME/www/session/.scrum/${session_name}_spent_$(date +%Y_%m_%d).md"
}

function session_meassure_begin() {
    emulate -L zsh

    local session_name="$1"
    local block_name="${2:-unnamed-block}"
    local note="${3:-}"

    if [[ -z "$session_name" ]]; then
        echo "Usage: session_meassure_begin <SESSION_NAME> [BLOCK_NAME] [NOTE]"
        return 1
    fi

    export SESSION_MEASSURE_NAME="$session_name"
    export SESSION_MEASSURE_BLOCK="$block_name"
    export SESSION_MEASSURE_NOTE="$note"
    export SESSION_MEASSURE_START_EPOCH="$(date +%s)"
    export SESSION_MEASSURE_START_LOCAL="$(_session_meassure_now_local)"
    export SESSION_MEASSURE_START_UTC="$(_session_meassure_now_utc)"
    export SESSION_MEASSURE_LOG="$(_session_meassure_log_file "$session_name")"

    mkdir -p "$HOME/www/session/.scrum"

    if [[ ! -f "$SESSION_MEASSURE_LOG" ]]; then
        {
            echo "# Session Spend: ${session_name}"
            echo
            echo "- time_zone: Europe/Prague (UTC+1 winter / UTC+2 summer)"
            echo "- created_at_local: $(_session_meassure_now_local)"
            echo "- created_at_utc: $(_session_meassure_now_utc)"
            echo
        } >> "$SESSION_MEASSURE_LOG"
    fi

    echo "session_meassure_begin -> ${SESSION_MEASSURE_BLOCK}"
    echo "log: ${SESSION_MEASSURE_LOG}"
    echo "start: ${SESSION_MEASSURE_START_LOCAL}"
}

function session_meassure_end() {
    emulate -L zsh

    local prompt_tokens="${1:-unknown}"
    local completion_tokens="${2:-unknown}"
    local note="${3:-$SESSION_MEASSURE_NOTE}"

    if [[ -z "$SESSION_MEASSURE_NAME" || -z "$SESSION_MEASSURE_START_EPOCH" ]]; then
        echo "No active measurement block. Run session_meassure_begin first."
        return 1
    fi

    local end_epoch="$(date +%s)"
    local end_local="$(_session_meassure_now_local)"
    local end_utc="$(_session_meassure_now_utc)"
    local duration_seconds="$(( end_epoch - SESSION_MEASSURE_START_EPOCH ))"
    local duration_minutes="$(awk "BEGIN { printf \"%.2f\", ${duration_seconds} / 60 }")"
    local total_tokens="unknown"
    local clean_note="${note//$'\n'/ }"

    if [[ "$prompt_tokens" =~ '^[0-9]+$' && "$completion_tokens" =~ '^[0-9]+$' ]]; then
        total_tokens="$(( prompt_tokens + completion_tokens ))"
    fi

    {
        echo "## ${SESSION_MEASSURE_BLOCK}"
        echo
        echo "- started_local: ${SESSION_MEASSURE_START_LOCAL}"
        echo "- ended_local: ${end_local}"
        echo "- started_utc: ${SESSION_MEASSURE_START_UTC}"
        echo "- ended_utc: ${end_utc}"
        echo "- duration_seconds: ${duration_seconds}"
        echo "- duration_minutes: ${duration_minutes}"
        echo "- prompt_tokens: ${prompt_tokens}"
        echo "- completion_tokens: ${completion_tokens}"
        echo "- total_tokens: ${total_tokens}"
        if [[ -n "$clean_note" ]]; then
            echo "- note: ${clean_note}"
        fi
        echo
    } >> "$SESSION_MEASSURE_LOG"

    echo "session_meassure_end -> ${SESSION_MEASSURE_BLOCK}"
    echo "duration_seconds: ${duration_seconds}"
    echo "total_tokens: ${total_tokens}"
    echo "log: ${SESSION_MEASSURE_LOG}"

    unset SESSION_MEASSURE_NAME
    unset SESSION_MEASSURE_BLOCK
    unset SESSION_MEASSURE_NOTE
    unset SESSION_MEASSURE_START_EPOCH
    unset SESSION_MEASSURE_START_LOCAL
    unset SESSION_MEASSURE_START_UTC
    unset SESSION_MEASSURE_LOG
}

function session_meassure_report() {
    emulate -L zsh

    local session_name="$1"
    local log_file="${2:-}"

    if [[ -z "$session_name" && -z "$log_file" ]]; then
        echo "Usage: session_meassure_report <SESSION_NAME> [LOG_FILE]"
        return 1
    fi

    if [[ -z "$log_file" ]]; then
        log_file="$(_session_meassure_log_file "$session_name")"
    fi

    if [[ ! -f "$log_file" ]]; then
        echo "Missing log file: ${log_file}"
        return 1
    fi

    awk '
        /^- duration_seconds:/ { total_duration += $3 }
        /^- total_tokens:/ {
            if ($3 ~ /^[0-9]+$/) {
                total_tokens += $3
            }
        }
        /^## / { block_count += 1 }
        END {
            printf "file=%s\n", FILENAME
            printf "blocks=%d\n", block_count
            printf "duration_seconds=%d\n", total_duration
            printf "duration_minutes=%.2f\n", total_duration / 60
            printf "total_tokens=%d\n", total_tokens
        }
    ' "$log_file"
}
