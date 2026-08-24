#!/usr/bin/env zsh
# claude.zsh — Claude Code RC engine + help functions
# Sourced by: ~/.config/zsh/ai/base.zsh (PARTITION 7)
# Aliases:    ~/.config/zsh/ai/keyboard.zsh (PARTITION 8, PARTITION 10, PARTITION 13, PARTITION 14)
#
# Aggregates small Claude-line surface bodies that belong off keyboard:
#   _rc_stop       → rc-stop alias (PARTITION 8)
#   _temple_help   → temple-help alias (PARTITION 10)
#   _octo          → octo alias (PARTITION 13)
#   _pinkeys       → pinkeys alias (PARTITION 14) — live keymap for editor-pin commands
#   _ai_launch     → lifecycle frame emitter (wraps CLI launch: start → exec → end) [iterations.jsonl]

_RC_SCRIPT="${HOME}/.config/zsh/ai/rc.sh"

_rc_stop() {
  local project="${1:-}"
  if [[ -z "${project}" ]]; then
    echo "Usage: rc-stop <project>  (freya | reposoma | nabla-lab)"
    return 1
  fi
  bash "${_RC_SCRIPT}" "${project}" stop
}

_temple_help() {
  cat <<'EOF'
temple transport — operator panel (engines: ai/temple-*, gated by decision 0009)

  temple-mail <origin>:<agent> <scope> [body|-] [--from o:a]   send mail
  temple-mail-inbox <origin>:<agent>                           unread listing (presence = unread)
  temple-mail-switch [--project <origin>]   (alias: mail-pick) destination picker + preview
  temple-mail-manage    mailbox TUI — archive/restore read-state (E; --list/--archive/--restore for agents)
  doorbell-run          ring stale projects now (engine: temple-doorbell.zsh)
  doorbell-smoke        real-trigger wiring gate — green + deliberate-red (0009 L5)
  doorbell-log          tail ~/.config/zsh/temple-doorbell.log
  transport-selftest    sandboxed logic selftest (4/4 green)

  Guide: ~/.config/zsh/guides/guide-temple-mail.md
EOF
}

_ai_help() {
  cat <<'EOF'
keyboard.zsh — AI interactive surface (Gemini + Claude Code RC)

  ── General CLI (Gemini + agy) ────────────────────────────────────────────────
  g                    run gemini CLI directly
  g-ver                gemini --version
  g-help               gemini --help
  g-yolo               gemini --approval-mode yolo
  g-skip               gemini --skip-trust
  agy-ver              agy --version
  agy-help             agy --help
  agy-yolo             agy --approval-mode yolo
  agy-skip             agy --skip-trust
  gemini-bluebottle    run bluebottle.sh (Bluebottle seat — dual-mode: interactive/headless)
  g-bluebottle         alias for gemini-bluebottle
  gemini-orby          run orby.sh (Orby seat — dual-mode: interactive/headless)
  g-orby               alias for gemini-orby
  ox-alpha "prompt"   stream one reasoning-enabled stealth/ox-alpha response via OpenRouter
  ox-alpha --no-stream "prompt"
                       print the non-streaming OpenRouter response as JSON
  ox-alpha chat        multi-turn terminal chat; /exit or Ctrl-D leaves and clears history
  exp-list             list installed experimental runners
  exp-run <id> [...]   execute an experimental runner on demand

  ── Hygiene / freshness ──────────────────────────────────────────────────────
  adr-guard            run adr-guard.zsh — ADR breach/evidence-rot sandbox check
  harness-stale        run harness-check.zsh --debug — settings-card freshness report

  ── Help / panels ─────────────────────────────────────────────────────────────
  ai-help              this panel
  temple-help          temple transport operator panel (see below)
  keys                 print the derived claviature panel (live functions/aliases by family)
  octo                 octopus head launcher — drop into the session head (Medusa/Flight)
  pinkeys              live chord → command table from the installed Sublime keymap

  ── Claude Code — Remote Control ─────────────────────────────────────────────
  rc-status            Show all RC projects and their tmux session status
  rc-freya             Start or attach Remote Control session: Freya
  rc-reposoma          Start or attach Remote Control session: Reposoma
  rc-nabla             Start or attach Remote Control session: Nabla Lab
  rc-stop <project>    Stop a running RC tmux session (freya|reposoma|nabla-lab)

  ── Zenith-ZSH — zsh config RAG assistant (Haiku) ────────────────────────────
  zenith-zsh           interactive chatbot — knows keyboard wiring, engine inventory,
                       guides; answers bash/zsh questions; read-only (broken-wiring log)
  zenith-zsh "query"   headless one-shot answer with pre-built context preamble
  Agent:  ~/.claude/agents/zenith-zsh.md
  Log:    ~/.config/zsh/blessings/broken-wiring.json

  Session lifecycle (Approach B — tmux on-demand):
    First call  → creates detached tmux, starts claude remote-control, attaches
    Ctrl-b d    → detach; RC keeps running in background
    rc-<proj>   → re-attach from any terminal
    rc-stop     → kill session + RC process

  Registry: ~/.config/zsh/registries/ai.json  (key: remote-control.projects)
  Script:   ~/.config/zsh/ai/rc.sh

  For Approach A (always-on systemd): ~/.config/zsh/guides/remote.md

  ── Temple utilities ─────────────────────────────────────────────────────────
  tree-snapshot <project>  Project file tree as JSON (depth 4 · .gitignore-aware)
                           Configs: ~/.config/zsh/registries/tcr/tcr.<project>.json
                           Agents:  zsh -c "source ~/.config/zsh/ai/base.zsh && tree-snapshot <project>"

  ── Project devenv transport ─────────────────────────────────────────────────
  devenv-help    full devenv key listing (bo-sync, bo-deploy, fr-sync, fr-deploy …)
EOF
  gemini-agents-help
  temple-help
  devenv-help
  _project_help
}

# _ai_launch — lifecycle frame emitter. Wraps a CLI launch: start frame → exec → end frame.
# Telemetry only: ~/.wires/iterations.jsonl (thin cache, cron-pruned 24-48h).
_ai_launch() {
  local state_file="$HOME/.wires/iterations.jsonl"
  /usr/bin/mkdir -p "${state_file:h}"
  local id="$$-$(date +%s)"
  local label="${AI_LAUNCH_LABEL:-$1}"
  local t0=$(date +%s)
  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"evt\":\"start\",\"id\":\"${id}\",\"host\":\"${MACHINE_NAME:-unknown}\",\"label\":\"${label}\",\"cwd\":\"$PWD\"}" >> "$state_file"
  "$@"
  local code=$?
  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"evt\":\"end\",\"id\":\"${id}\",\"exit\":${code},\"dur_s\":$(( $(date +%s) - t0 ))}" >> "$state_file"
  return $code
}

# _octo — octopus head launcher. Small erasable pointer echo, then drop into the session head.
# Erase the echo line once the routine is in blood; keep the launch.
_octo() {
  print -P "octopus → head: Medusa (project seat) · cheat-sheet: /octo · buffer: stream.md (manned) · program.pulse.md (batch) · law: 0012"
  _ai_launch claude --agent flight
}

# _pinkeys — live keymap for editor-pin-sublime commands.
# Parses the INSTALLED keymap at call time (never cached — anti-staleness is the point).
# Falls back to the repo default if no installed keymap is found.
# To extend: add another topic block below the editor_pin filter — the structure is obvious.
_pinkeys() {
  local _kmap
  # Prefer the installed keymap; fall back to the repo file.
  _kmap=$(ls ~/.config/sublime-text/Packages/User/*.sublime-keymap 2>/dev/null | head -1)
  if [[ -z "${_kmap}" ]]; then
    _kmap=$(ls ~/.config/sublime-text-3/Packages/User/*.sublime-keymap 2>/dev/null | head -1)
  fi
  local _note=""
  if [[ -z "${_kmap}" ]]; then
    _kmap="/home/hruzam/www/elements-factory/applications-in-common/experiments/editor-pin-sublime/Default.sublime-keymap"
    _note=" [repo defaults — no installed keymap found]"
  fi
  echo "editor-pin keybindings (source: ${_kmap}${_note})"
  echo ""
  python3 - "${_kmap}" <<'PYEOF'
import sys, re, json

kmap_path = sys.argv[1]
with open(kmap_path, encoding="utf-8") as f:
    raw = f.read()
# Strip // line comments before JSON parse.
stripped = re.sub(r"//[^\n]*", "", raw)
entries = json.loads(stripped)

for entry in entries:
    cmd = entry.get("command", "")
    if not cmd.startswith("editor_pin"):
        continue
    keys = "+".join(entry.get("keys", []))
    args = entry.get("args", {})
    args_str = "  " + str(args) if args else ""
    print(f"  {keys:<22}  {cmd}{args_str}")
PYEOF
}

# pinprompt — copy "read from source: ~/.wires/pins.jsonl" to clipboard
# Usage: pinprompt
function pinprompt() {
    local msg="read from source: ${HOME}/.wires/pins.jsonl"
    printf '%s' "$msg" | xclip -selection clipboard 2>/dev/null \
        || printf '%s' "$msg" | xsel --clipboard --input 2>/dev/null \
        || { echo "$msg"; return 1; }
    echo "[pinprompt] copied to clipboard: $msg"
}
