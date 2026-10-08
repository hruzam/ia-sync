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

# tn-check [bed] [name] | tn-check --id <thread> [--cwd <dir>] → read-only health verdict.
#   Vault mode: is the bound thread usable for the next tunnel verb right now?
#   --id mode:  is a candidate thread fit to BE bound (successor check, before tn-on)?
#   Reads the vault, <vault>.lock, ~/.codex/thread-writer-locks/<id>.lock (HOLDER via fuser —
#   a lock file can outlive its holder), the thread's rollout and the running codex versions.
#   Never writes, never spawns codex, spends no quota.
#   exit 0 READY · 2 BUSY (shim turn in flight) · 3 HELD (writer-lock held: TUI or daemon) ·
#        4 BROKEN (unusable: no rollout / zero turns / subagent / cwd / preamble) · 10 no vault
_tn_check() {
    local p="" id="" cwd=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id)  id="$2"; shift 2 ;;
            --cwd) cwd="$2"; shift 2 ;;
            *) break ;;
        esac
    done
    if [[ -z "$id" ]]; then
        if [[ $# -eq 0 && -n "${TUNNEL_CODEX_STATE:-}" ]]; then p="$TUNNEL_CODEX_STATE"
        else p="$(_tn_path "$@")"; fi
    fi
    python3 - "$p" "$id" "$cwd" <<'PY'
import glob, json, os, subprocess, sys
p, cand, cand_cwd = sys.argv[1], sys.argv[2], sys.argv[3]
home = os.path.expanduser("~")
bad, busy, held, warn = [], [], [], []

def sh(*cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception: return ""

def alive(pid):
    try: os.kill(int(pid), 0); return True
    except Exception: return False

# 1 · vault (or candidate)
s = {}
if p:
    print(f"vault     {p}")
    if not os.path.isfile(p):
        print("          (no vault — closed, or wrong bed/name)"); sys.exit(10)
    s = json.load(open(p))
    tid = s.get("threadId")
    print(f"thread    {tid or '—'}  enabled={s.get('enabled')} bound={s.get('bound')}")
    want_cwd = s.get("cwd") or ""
    pre = s.get("preamble")
    if pre:
        ok = os.path.isfile(pre)
        print(f"preamble  {pre}  {'ok' if ok else 'MISSING'}")
        if not ok: bad.append("preamble file missing (turn would exit 11)")
    if not s.get("enabled"): bad.append("vault disabled")
    if not tid: bad.append("vault has no threadId (born on first send — nothing to check)")
    lk = p + ".lock"
    if os.path.exists(lk):
        try: pid = open(lk).read().strip() or "0"
        except Exception: pid = "0"
        if alive(pid): busy.append(f"shim turn in flight (pid {pid})")
        else: warn.append(f"stale shim lock {lk} (pid {pid} dead)")
else:
    tid, want_cwd = cand, cand_cwd
    print(f"candidate {tid}" + (f"  (expect cwd {want_cwd})" if want_cwd else ""))

if tid:
    # 2 · writer-lock holder
    wl = f"{home}/.codex/thread-writer-locks/{tid}.lock"
    holders = sh("fuser", wl).split() if os.path.exists(wl) else []
    if holders:
        for h in holders:
            cmd = sh("ps", "-o", "args=", "-p", h)[:90]
            kind = "daemon" if "app-server" in cmd else "TUI/other"
            print(f"writer    HELD by {h} [{kind}] {cmd}")
            held.append(f"writer-lock held by {kind} pid {h}")
    else:
        print("writer    free" + (" (lock file present, no holder)" if os.path.exists(wl) else ""))

    # 3 · rollout
    rs = glob.glob(f"{home}/.codex/sessions/*/*/*/rollout-*{tid}.jsonl")
    if not rs:
        print("rollout   NONE")
        bad.append("no rollout — zero-turn thread (/clear or /new never used) — resume gives -32600")
    else:
        r = rs[0]; turns = compacts = 0; meta = {}; last_ctx = None; settings = None; last_compact = None
        with open(r) as fh:
            for line in fh:
                try: e = json.loads(line)
                except Exception: continue
                t, pl = e.get("type"), e.get("payload") or {}
                if t == "session_meta": meta = pl
                elif t == "turn_context":
                    turns += 1
                    settings = {k: pl.get(k) for k in ("model", "effort", "approval_policy", "approvals_reviewer")}
                elif t == "compacted": compacts += 1; last_compact = e.get("timestamp")
                elif t == "event_msg" and pl.get("type") == "thread_settings_applied":
                    ts = pl.get("thread_settings") or {}
                    settings = {"model": ts.get("model"), "effort": ts.get("reasoning_effort"),
                                "approval_policy": ts.get("approval_policy"),
                                "approvals_reviewer": ts.get("approvals_reviewer")}
                elif t == "event_msg" and pl.get("type") == "token_count":
                    info = pl.get("info") or {}
                    last_ctx = ((info.get("last_token_usage") or {}).get("input_tokens"),
                                info.get("model_context_window"), e.get("timestamp"))
        src = meta.get("source")
        print(f"rollout   {r}")
        print(f"          turns={turns} compacted={compacts}{' last '+last_compact if last_compact else ''}"
              f"  cli={meta.get('cli_version')} source={json.dumps(src)}")
        if settings: print(f"policy    " + " ".join(f"{k}={v}" for k, v in settings.items()))
        if last_ctx and last_ctx[0] is not None and last_ctx[1]:
            print(f"ctx       {last_ctx[0]}/{last_ctx[1]} ({100*last_ctx[0]/last_ctx[1]:.1f} %) @ {last_ctx[2]}"
                  + ("  ← reset by compaction, next turn re-measures" if last_ctx[0] == 0 else ""))
        if turns == 0: bad.append("rollout has zero turns — give it a first turn before binding")
        if isinstance(src, dict) and "subagent" in src: bad.append(f"subagent thread ({json.dumps(src)}) — not a head")
        if want_cwd and meta.get("cwd") and os.path.realpath(meta["cwd"]) != os.path.realpath(want_cwd):
            bad.append(f"cwd mismatch: thread {meta['cwd']} vs expected {want_cwd}")

# 4 · version skew (CLI the shim spawns vs running daemon)
cli = sh("codex", "--version").split()[-1:] or ["?"]
daemons = sorted(set(x.split("/releases/")[1].split("-")[0] for x in sh("pgrep", "-af", "app-server").splitlines()
                     if "/releases/" in x and "app-server" in x))
print(f"codex     cli={cli[0]} daemon={','.join(daemons) or 'none'}")
if daemons and any(d != cli[0] for d in daemons): warn.append(f"version skew cli {cli[0]} ≠ daemon {','.join(daemons)} (L8: selftest + one live ask)")

for w in warn: print(f"note      {w}")
if bad:  print("VERDICT   BROKEN — " + " · ".join(bad)); sys.exit(4)
if busy: print("VERDICT   BUSY — " + " · ".join(busy) + " — wait, never retry in a loop"); sys.exit(2)
if held: print("VERDICT   HELD — " + " · ".join(held) + " — exit the TUI / wait, then tun resume"); sys.exit(3)
print("VERDICT   READY" + (" (as a successor: bind it with tn-on … --thread)" if not p else "")); sys.exit(0)
PY
}

# tn-back [bed] [name] [--timeout S] → "tunnel back" after a TUI visit (compact, /permissions…):
#   waits until NO process holds ~/.codex/thread-writer-locks/<thread>.lock (the 0.160+/0.162
#   daemon keeps the writer for a while after TUI /exit — support log T10/T18), then `tun resume`,
#   then tn-check. Never touches the lock. Refuses while a shim turn is in flight.
#   exit = resume's exit · 2 BUSY · 3 still HELD at timeout (nothing sent) · 10 no vault
_tn_back() {
    local timeout=300 args=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --timeout) timeout="$2"; shift 2 ;;
            *) args+=("$1"); shift ;;
        esac
    done
    local p tid lk wl pid t0 rc
    if [[ ${#args} -eq 0 && -n "${TUNNEL_CODEX_STATE:-}" ]]; then p="$TUNNEL_CODEX_STATE"
    else p="$(_tn_path "${args[@]}")"; fi
    [[ -f "$p" ]] || { print -u2 -- "[tn-back] no vault at $p"; return 10; }
    tid="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("threadId") or "")' "$p")"
    [[ -n "$tid" ]] || { print -u2 -- "[tn-back] vault has no threadId — nothing to resume"; return 10; }
    lk="$p.lock"
    if [[ -f "$lk" ]]; then
        pid="$(<"$lk")"
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            print -u2 -- "[tn-back] BUSY — shim turn in flight (pid $pid); wait, never retry in a loop"; return 2
        fi
    fi
    wl="$HOME/.codex/thread-writer-locks/$tid.lock"
    t0=$SECONDS
    while [[ -e "$wl" ]] && fuser "$wl" >/dev/null 2>&1; do
        if (( SECONDS - t0 >= timeout )); then
            print -u2 -- "[tn-back] still HELD after ${timeout}s by pid(s)$(fuser "$wl" 2>/dev/null) — nothing sent. TUI still open? pgrep -af 'codex resume'"
            return 3
        fi
        (( (SECONDS - t0) % 15 == 0 )) && print -u2 -- "[tn-back] writer-lock held ($(( SECONDS - t0 ))s) — waiting for release…"
        sleep 1
    done
    print -u2 -- "[tn-back] writer free after $(( SECONDS - t0 ))s — resuming $tid"
    _tn_shim resume --state "$p"; rc=$?
    _tn_check "${args[@]}" >/dev/null 2>&1; print -u2 -- "[tn-back] resume exit=$rc · tn-check exit=$? (0 READY)"
    return $rc
}

# tn-rebind <bed> [name] --thread <NEW> [--reason TEXT] → successor without the hand-copied line.
#   Carries the vault's intent (cwd, sandbox, model, preamble) to NEW, appends
#   {old,new,at,reason} to the vault's `lineage` array, keeps the old lineage.
#   Gate: `tn-check --id NEW --cwd <vault cwd>` must not be BROKEN (zero-turn / no rollout /
#   subagent / cwd mismatch are refused); refuses NEW == old and a shim turn in flight.
#   Local only: no resume. HELD is allowed (binding is local) — follow with `tn-back`.
#   If the re-open fails, the old vault is restored byte-for-byte.
#   exit 0 rebound · 2 BUSY · 4 NEW refused · 10 no vault · 11 usage · other = shim open failed (restored)
_tn_rebind() {
    local new="" reason="" args=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --thread) new="$2"; shift 2 ;;
            --reason) reason="$2"; shift 2 ;;
            *) args+=("$1"); shift ;;
        esac
    done
    [[ -n "$new" ]] || { print -u2 -- "usage: tn-rebind <bed> [name] --thread NEW_ID [--reason TEXT]"; return 11; }
    local p
    if [[ ${#args} -eq 0 && -n "${TUNNEL_CODEX_STATE:-}" ]]; then p="$TUNNEL_CODEX_STATE"
    else p="$(_tn_path "${args[@]}")"; fi
    [[ -f "$p" ]] || { print -u2 -- "[tn-rebind] no vault at $p (closed? use tn-on … --thread)"; return 10; }
    local saved; saved="$(<"$p")"
    local -a f; f=("${(@f)$(python3 -c '
import json,sys; s=json.load(open(sys.argv[1]))
for k in ("threadId","cwd","sandbox","model","preamble"): print(s.get(k) or "")' "$p")}")
    local old="${f[1]}" cwd="${f[2]}" sandbox="${f[3]:-read-only}" model="${f[4]}" pre="${f[5]}"
    [[ "$new" != "$old" ]] || { print -u2 -- "[tn-rebind] NEW == current thread $old — nothing to do"; return 11; }
    if [[ -f "$p.lock" ]] && kill -0 "$(<"$p.lock")" 2>/dev/null; then
        print -u2 -- "[tn-rebind] BUSY — shim turn in flight; wait"; return 2
    fi
    _tn_check --id "$new" ${cwd:+--cwd "$cwd"}
    local crc=$?
    if (( crc == 4 )); then print -u2 -- "[tn-rebind] refused — $new is not bindable (see VERDICT above); vault unchanged"; return 4; fi
    local -a open_args; open_args=(--enable --state "$p" --thread "$new" --sandbox "$sandbox")
    [[ -n "$cwd" ]] && open_args+=(--cwd "$cwd")
    [[ -n "$model" ]] && open_args+=(--model "$model")
    [[ -n "$pre" ]] && open_args+=(--preamble "$pre")
    _tn_shim close --state "$p" 2>/dev/null
    _tn_shim open "${open_args[@]}"
    local orc=$?
    if (( orc != 0 )); then
        print -r -- "$saved" > "$p"
        print -u2 -- "[tn-rebind] open on $new FAILED (exit $orc) — old vault restored ($old)"; return $orc
    fi
    python3 - "$p" "$old" "$new" "$reason" "$saved" <<'PY'
import json, os, sys, datetime
p, old, new, reason, saved = sys.argv[1:6]
s = json.load(open(p)); prev = json.loads(saved)
lin = list(prev.get("lineage") or [])
lin.append({"old": old, "new": new, "reason": reason or None,
            "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
s["lineage"] = lin
tmp = p + ".tmp"; json.dump(s, open(tmp, "w"), indent=2, sort_keys=True); os.replace(tmp, p)
PY
    print -u2 -- "[tn-rebind] $old → $new (carried: cwd=${cwd:-—} sandbox=$sandbox model=${model:-—} preamble=${pre:-—}); lineage recorded"
    (( crc == 3 )) && print -u2 -- "[tn-rebind] NEW is HELD right now — run tn-back (waits for release, then resumes)" \
                   || print -u2 -- "[tn-rebind] next: tn-back   (resume + tn-check)"
    return 0
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
  tn-check [bed] [name]        read-only verdict READY/BUSY/HELD/BROKEN (locks, rollout, ctx, versions)
  tn-check --id <thread> [--cwd <dir>]   is this id fit to bind? (successor check, before tn-on)
  tn-back  [bed] [name] [--timeout S]    after a TUI visit: wait for the writer-lock holder to go, resume, check
  tn-rebind <bed> [name] --thread NEW [--reason TEXT]   successor: carry cwd/sandbox/model/preamble, log lineage
  bed = slug under $RB_ROOT · "." · a path.   name → tunnel.<name>.state.json
  Then drive it with the shim: tun ask / tun send / tun read / tun resume (/guide tunnel)
EOF
}
