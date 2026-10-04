#!/usr/bin/env zsh
# =============================================================================
# TUNNEL.ZSH — tunnel manager engine (vault on/off/use/list per session bed)
# =============================================================================
# Location: ~/.config/zsh/session/tunnel.zsh (table-authored in ~/ia-sync/zsh/;
#           `bash deploy.sh` spreads — never edit the live copy)
# Sourced by: session/base.zsh PARTITION 6 · aliases: session/keyboard.zsh tn-*
# Body: the shim ~/.config/zsh/ai/tunnel-codex.zsh (ai/ scope) — this engine only
#       resolves WHICH vault a shell points at and wraps open/close/status for it.
#       It never speaks JSON-RPC itself and spends no quota on its own.
# Born: 2026-10-04 (@Trajectory, majkee ask) as the minimal "on / off / set values"
#       device, sibling of the runbook browser; full mosaic (Atlas/Cartan) later.
# Contract of this file: definitions only on source.
#
# VAULT LAW (multi-tunnel ready)
#   one vault = one state file = one Codex thread. Keyed by BED + NAME:
#     <bed>/tunnel.state.json          default name
#     <bed>/tunnel.<name>.state.json   a named second/third tunnel in the same bed
#   All shapes match .gitignore `tunnel*.state.json` — a vault never travels.
#   A shell holds ONE current vault ($TUNNEL_CODEX_STATE); `tn-use` switches it.
#   Two vaults must never point at the same threadId (the shim's turn lock is
#   per vault, not per thread — see /guide tunnel §Limits).
#
# BED RESOLUTION (first match)
#   absolute path · path containing "/" relative to $PWD · "." = $PWD ·
#   otherwise a slug under $RB_ROOT (default ~/ia-sync/.dev/session)
# =============================================================================

_tn_shim() { zsh "$HOME/.config/zsh/ai/tunnel-codex.zsh" "$@"; }

_tn_bed() {
    local bed="${1:-.}"
    if [[ "$bed" == "." ]]; then print -r -- "$PWD"
    elif [[ "$bed" == /* ]]; then print -r -- "$bed"
    elif [[ "$bed" == */* ]]; then print -r -- "$PWD/$bed"
    else print -r -- "${RB_ROOT:-$HOME/ia-sync/.dev/session}/$bed"
    fi
}

# tn-path <bed> [name] → the vault path for that bed/name (no side effects)
_tn_path() {
    local bed name
    bed="$(_tn_bed "${1:-.}")"; name="${2:-}"
    if [[ -n "$name" ]]; then print -r -- "$bed/tunnel.$name.state.json"
    else print -r -- "$bed/tunnel.state.json"
    fi
}

# tn-use <bed> [name] → export TUNNEL_CODEX_STATE in THIS shell (the "set" act)
_tn_use() {
    local p; p="$(_tn_path "$@")"
    export TUNNEL_CODEX_STATE="$p"
    print -u2 -- "[tn] TUNNEL_CODEX_STATE=$p $([[ -f "$p" ]] && echo '(vault exists)' || echo '(no vault yet — tn-on to create)')"
}

# tn-on <bed> [name] [-- <tun open flags>] → use + `tun open --enable <flags>`
#   flags pass straight to the shim: --thread <id> --cwd <dir> --sandbox <mode> --model <id>
#   Values are set HERE, at open — Law 2.4: intent is an open-time act, never per send.
_tn_on() {
    local bed="${1:-.}" name="" ; shift || true
    if [[ $# -gt 0 && "$1" != --* && "$1" != "--" ]]; then name="$1"; shift; fi
    [[ "${1:-}" == "--" ]] && shift
    _tn_use "$bed" "$name"
    _tn_shim open --enable "$@"
}

# tn-off [bed] [name] → close that vault (prints threadId + re-bind line first)
_tn_off() {
    local p
    if [[ $# -eq 0 && -n "${TUNNEL_CODEX_STATE:-}" ]]; then p="$TUNNEL_CODEX_STATE"
    else p="$(_tn_path "$@")"; fi
    _tn_shim close --state "$p"
}

# tn-st [bed] [name] → the vault, two layers: intent (top) · runtime (server-reported)
_tn_st() {
    local p
    if [[ $# -eq 0 && -n "${TUNNEL_CODEX_STATE:-}" ]]; then p="$TUNNEL_CODEX_STATE"
    else p="$(_tn_path "$@")"; fi
    [[ -f "$p" ]] || { print -u2 -- "[tn] no vault at $p"; return 10; }
    python3 - "$p" <<'PY'
import json, sys
p = sys.argv[1]; s = json.load(open(p))
rt = s.get("runtime") or {}
sb = rt.get("sandbox"); sb = sb.get("type") if isinstance(sb, dict) else sb
print(f"vault     {p}")
print(f"thread    {s.get('threadId') or '— (born on first send)'}{'  [bound]' if s.get('bound') else ''}")
print(f"intent    sandbox={s.get('sandbox')} model={s.get('model')} cwd={s.get('cwd') or '(caller dir)'}")
if rt:
    print(f"runtime   sandbox={sb} effort={rt.get('reasoningEffort')} approval={rt.get('approvalPolicy')} model={rt.get('model')}")
    print(f"          cwd={rt.get('cwd')}  instructions={rt.get('instructionSources')}  @ {rt.get('observedAt')}")
else:
    print("runtime   (none yet — `tun resume` or the first send stamps it)")
print(f"lastTurn  {s.get('lastTurnId') or '—'}")
PY
}

# tn-ls → every vault under $RB_ROOT (and $PWD if outside it); * marks the shell's current one
_tn_ls() {
    local root="${RB_ROOT:-$HOME/ia-sync/.dev/session}"
    python3 - "$root" "${TUNNEL_CODEX_STATE:-}" "$PWD" <<'PY'
import glob, json, os, sys
root, cur, pwd = sys.argv[1], sys.argv[2], sys.argv[3]
pats = [os.path.join(root, "*", "tunnel*.state.json")]
if not pwd.startswith(root): pats.append(os.path.join(pwd, "tunnel*.state.json"))
seen, rows = set(), []
for pat in pats:
    for p in sorted(glob.glob(pat)):
        if p in seen: continue
        seen.add(p)
        try: s = json.load(open(p))
        except Exception: s = {}
        bed = os.path.basename(os.path.dirname(p))
        name = os.path.basename(p)[len("tunnel"):-len(".state.json")].strip(".") or "default"
        tid = (s.get("threadId") or "")[:8] or "—"
        rt = s.get("runtime") or {}
        sb = rt.get("sandbox"); sb = sb.get("type") if isinstance(sb, dict) else (sb or s.get("sandbox"))
        rows.append(("*" if p == cur else " ", bed, name, tid, "bound" if s.get("bound") else "born", sb, rt.get("model") or s.get("model")))
if not rows:
    print(f"[tn] no vaults under {root}"); sys.exit(0)
w = max(len(r[1]) for r in rows)
for m, bed, name, tid, kind, sb, model in rows:
    print(f"{m} {bed:<{w}}  {name:<8} {tid:<9} {kind:<5} {sb or '?':<15} {model or '?'}")
PY
}

_tn_help() {
    cat >&2 <<'EOF'
tn — tunnel manager (vault per session bed · one vault = one Codex thread)
  tn-ls                        every vault under $RB_ROOT; * = this shell's current
  tn-use <bed> [name]          point THIS shell at a vault (export TUNNEL_CODEX_STATE)
  tn-on  <bed> [name] [-- --thread <id> --cwd <dir> --sandbox <mode> --model <id>]
                               use + `tun open --enable …` (values are set here, Law 2.4)
  tn-off [bed] [name]          close (prints threadId + re-bind line first)
  tn-st  [bed] [name]          intent vs runtime layers of the vault
  bed = slug under $RB_ROOT · "." · a path.   name → tunnel.<name>.state.json
  Then drive it with the shim: tun ask / tun send / tun read / tun resume (/guide tunnel)
EOF
}
