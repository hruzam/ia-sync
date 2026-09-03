#!/usr/bin/env zsh
# tunnel-codex.zsh — termbrana 03-tunnel v0: Codex app-server stored-thread supervisor
#
# SPEC (verbatim call sequence + curvature findings this shim implements):
#   ~/ia-sync/session/rellays-calude-codex/CARTAN-ORACULUM-tunnel-verdict.2026-09-02.md
# PROTOCOL PIN: codex-cli 0.152.1-observed, protocol experimental — upgrade = a TESTED
#   migration, never a drop-in swap (curvature 3, verdict file: `codex app-server --help`
#   still labels the command [experimental] on this release). Method/param names live in
#   the sibling tunnel-codex.py and were cross-checked 2026-09-02 against a local,
#   zero-quota `codex app-server generate-json-schema --experimental` run on this exact
#   binary — not copied from the docs page, which curvature 1 shows is stale for the
#   sandbox enum.
#
# STATUS: v0 build. NOT deployed to ~/.config/zsh — behavior proof (session t3, one live
#   round-trip) is required before promotion (Sella L8: unchanged files != unchanged
#   behavior on an experimental protocol). Law 2.4 (termbrana): the default is read-only;
#   this file is the deliberately-enabled write capability, never a silent default.
#
# MECHANICS: JSON-RPC 2.0, newline-delimited, one message per line, over the stdio of a
#   freshly spawned `codex app-server --stdio` — one subprocess per shim invocation, no
#   daemon (RUNBOOK constraint; `codex app-server daemon` exists but is out of v0 scope).
#   The actual JSON-RPC framing/parsing lives in tunnel-codex.py (python3 stdlib only,
#   same directory); this file owns the operator surface, the Law 2.4 gate, arg/enum
#   validation, and the exit-code contract below. Text arguments are always passed to
#   python as a literal argv element (never interpolated into a shell/eval string), so
#   there is no quoting-injection hazard to harden against here.
#
# THREAD BIRTH (fix, 2026-09-03 — t3 FAIL evidence, session toolbox-termbrana-03-tunnel):
#   on codex-cli 0.152.1 a zero-turn `thread/start` allocates a thread id + writer-lock
#   but writes NO rollout file — the rollout is written on the first *turn*. Since each
#   shim verb is its own `codex app-server --stdio` subprocess, a threadId stored from a
#   zero-turn thread/start fails EVERY later thread/resume with -32600 "no rollout
#   found". Fix: `open --enable` no longer calls thread/start at all — it only
#   preflights and persists `threadId: null`. The thread is born inside `send`'s own
#   connection (thread/start immediately followed by turn/start, same process — Cartan's
#   proven continuous sequence), so a rollout always exists before any other verb can
#   try to resume it. `read` / `resume` / `steer` refuse cleanly (exit 12) if no thread
#   has been born yet.
#
# VERBS
#   open   [--enable] [--sandbox read-only|workspace-write|danger-full-access] [--model M]
#          First call MUST pass --enable (Law 2.4) — creates tunnel.state.json via a
#          zero-turn preflight (initialize -> account/read -> model/list). Does NOT call
#          thread/start (see THREAD BIRTH above) — state is persisted with
#          `threadId: null`; the thread is born on the first `send`. A later call with
#          an existing state file and a threadId already born resumes it
#          (thread/resume) as a liveness probe; if no thread has been born yet it just
#          reports that fact and exits 0.
#   send <text>     if state has no threadId yet: thread/start then turn/start in the
#                   SAME connection (thread birth), persisting the new threadId. If a
#                   threadId is already stored: thread/resume then turn/start. Either
#                   way: blocks for turn/completed; reconciles via
#                   thread/read(includeTurns=true); prints the final agent-message text
#                   + a trailing `[usage: {...}]` line; records the turn id as the new
#                   steer target.
#   ask <text>      send + reconcile in one call, VERIFIED: performs the full send
#                   (thread birth or resume, same as 'send'), then
#                   thread/read(includeTurns=true) reconciliation, then compares the
#                   streamed agent text against the read-back text for that turn. On
#                   match: prints the verified text + `[usage: {...}]` tail to stdout,
#                   exit 0. On mismatch: exit 50, both texts named on stderr — never
#                   silently picks one. Same Law 2.4 gates as every other verb: does
#                   NOT auto-enable (exit 10 without a state file; exit 13 without a
#                   state path).
#   steer <text>    turn/steer(expectedTurnId = last recorded turn id) — steers the turn
#                   THIS shim itself most recently drove. Requires a threadId already
#                   born (exit 12 "no thread yet" otherwise — run send first). KNOWN v0
#                   LIMIT: each verb is its own process (no daemon), so `steer` can only
#                   target a turn id recorded in this shim's own state file, via a
#                   freshly resumed connection — it cannot inject into a turn that is
#                   concurrently streaming inside a still-running separate `send`
#                   invocation in another terminal. True mid-stream steering from a
#                   second process needs a resident process (v1/daemon), not promised
#                   by v0.
#   read            thread/read(includeTurns=true); prints the raw JSON result.
#                   Requires a threadId already born (exit 12 otherwise).
#   resume          thread/resume only (liveness probe); prints thread id + status.
#                   Requires a threadId already born (exit 12 otherwise).
#   close           LOCAL ONLY — removes tunnel.state.json; re-arms the Law 2.4 gate.
#                   RESIDUE (v0, honest): send's thread birth leaves ~/.codex/thread-writer-locks/<threadId>.lock;
#                   local-only close does not clean codex-side state.
#                   Lock cleanup verdict (@Cartan 2026-09-03): NEVER unlink
#                   ~/.codex/thread-writer-locks/* — Codex-owned state, unlink can race
#                   another client; Codex has coordinated stale-lock cleanup. To retire a
#                   stored thread deliberately: supported 'codex archive' / 'codex delete'
#                   as an explicit operator lifecycle action — never hidden cleanup, never
#                   manual rm.
#                   Also: resumed-steer only (no mid-stream steer across processes) — v1
#                   resident-process candidate.
#   status          LOCAL ONLY — prints tunnel.state.json (refused per the gate below
#                   if the shim was never enabled — Law 2.4 applies to every verb).
#
# STDOUT PURITY (Sella L4 / one-return-channel law, added 2026-09-03): all
#   narrative/banner/progress output (open:/close:/status:/resume: messages) goes to
#   STDERR. STDOUT carries ONLY the driven agent-message text (send/ask/steer), read's
#   raw JSON, and the trailing `[usage: {...}]` line send/ask/steer append after it.
#   close and status print nothing to stdout at all (their content is diagnostic, not a
#   result) — human UX is unaffected since a terminal shows stderr inline anyway. Exit
#   codes are unchanged by this; only the fd each message lands on moved.
#
# FLAGS
#   --enable              required on the very first `open` (Law 2.4)
#   --state <path>        state file path — see STATE PATH SELECTION below
#   --sandbox <value>     open only; one of the three CLI-form values above (curvature 1)
#   --model <id>          open only; omit to have `open` resolve+stamp the account's
#                         `isDefault` model from model/list (fix, 2026-09-03 — this used
#                         to stamp state/banner with a literal `model=None`)
#
# STATE PATH SELECTION (hardened 2026-09-03 — Cartan safe-order fix, resurrection trap
#   removed): there is NO hardcoded default state path anymore. Precedence, explicit
#   only:
#     1. --state <path>          (flag wins)
#     2. $TUNNEL_CODEX_STATE     (env var, if flag absent)
#     3. neither given -> exit 13 (state-not-specified) — CREATES NOTHING: no directory,
#        no file, not even the parent tree. The error names both mechanisms above.
#   Rationale: the old baked-in default path
#   (~/unikuklatrix/nablarva/.dev/session/toolbox-termbrana-03-tunnel/tunnel.state.json)
#   let any stray invocation silently resurrect/recreate session-bed state nobody asked
#   for. State selection is now always an explicit operator/agent decision.
#
# ENV
#   TUNNEL_CODEX_STATE     state file path (see STATE PATH SELECTION above) — no default
#   TUNNEL_CODEX_BIN       codex binary name/path (default: "codex", resolved via PATH —
#                          this is how the fixture selftest substitutes a fake binary)
#   TUNNEL_CODEX_TIMEOUT   seconds to wait per JSON-RPC response / turn/completed
#                          (default: 120, read by tunnel-codex.py)
#
# EXIT CODES (man-page style; tunnel-codex.py mirrors these exactly)
#   0   ok
#   10  no-enable          — Law 2.4 refusal: verb needs the state file, it is absent,
#                            and (for `open`) --enable was not given
#   11  usage              — bad/missing args, unknown verb, invalid --sandbox value
#   13  state-not-specified — neither --state nor $TUNNEL_CODEX_STATE was given; see
#                            STATE PATH SELECTION above. Nothing is created.
#   20  spawn-fail         — the codex binary would not start, or python3 is missing
#   30  protocol-error     — JSON-RPC transport broke: bad JSON, EOF, timeout, error reply
#   40  turn-error         — a turn ended non-"completed", or steer had no turn to target
#   50  reconcile-mismatch — thread/read(includeTurns=true) disagrees with what
#                            turn/completed just reported; also `ask`'s own verify step
#                            (streamed agent text != thread/read read-back text for the
#                            same turn) — both texts named on stderr, never silently
#                            picks one
#   12  no-thread          — read/resume/steer called before any thread has been born
#                            (state threadId is null); run 'send' first — thread birth
#                            happens on first send, not on open (see THREAD BIRTH above)
#
# DIAGNOSTICS go to stderr; RESULT TEXT goes to stdout (man-page convention, Sella L4).
# deploy target (post-t3 only): ~/.config/zsh/ai/ — see STATUS above.

set -euo pipefail

SCRIPT_DIR="${0:A:h}"
PY="$SCRIPT_DIR/tunnel-codex.py"

SANDBOX_VALUES=(read-only workspace-write danger-full-access)

_usage() {
  print -u2 -- "tunnel-codex: $1"
  exit 11
}

if (( $# == 0 )); then
  _usage "usage: tunnel-codex.zsh <open|send|ask|steer|read|resume|close|status> [...] (exit 11)"
fi

verb="$1"
shift

case "$verb" in
  open|send|ask|steer|read|resume|close|status) ;;
  *) _usage "unknown verb '$verb' — see this file's header for the verb list (exit 11)" ;;
esac

# --- arg parsing: pull known flags, collect the rest as positional ---
enable_flag=0
sandbox_val="read-only"
model_val=""
state_flag=""
state_flag_given=0
positional=()

while (( $# )); do
  case "$1" in
    --enable) enable_flag=1; shift ;;
    --state) (( $# >= 2 )) || _usage "--state requires a path (exit 11)"; state_flag="$2"; state_flag_given=1; shift 2 ;;
    --sandbox) (( $# >= 2 )) || _usage "--sandbox requires a value (exit 11)"; sandbox_val="$2"; shift 2 ;;
    --model) (( $# >= 2 )) || _usage "--model requires a value (exit 11)"; model_val="$2"; shift 2 ;;
    --) shift; positional+=("$@"); break ;;
    -*) _usage "unknown flag '$1' (exit 11)" ;;
    *) positional+=("$1"); shift ;;
  esac
done

# --- state path resolution (hardened 2026-09-03 — no default, see STATE PATH
# SELECTION in the header): --state flag wins over $TUNNEL_CODEX_STATE; if neither is
# given, refuse cleanly (exit 13) and create nothing — no directory, no file. ---
if (( state_flag_given )); then
  state_file="$state_flag"
elif [[ -n "${TUNNEL_CODEX_STATE:-}" ]]; then
  state_file="$TUNNEL_CODEX_STATE"
else
  print -u2 -- "tunnel-codex: refused — no state path given; pass --state <path> or set \$TUNNEL_CODEX_STATE (exit 13, state-not-specified)"
  exit 13
fi

case "$verb" in
  send|ask|steer)
    (( ${#positional[@]} >= 1 )) || _usage "verb '$verb' requires <text> (exit 11)"
    text_arg="${positional[1]}"
    ;;
esac

if [[ "$verb" == open ]]; then
  if (( ! ${SANDBOX_VALUES[(Ie)$sandbox_val]} )); then
    _usage "--sandbox must be one of: ${(j:, :)SANDBOX_VALUES} — got '$sandbox_val' (exit 11)"
  fi
fi

# --- Law 2.4 explicit-enable gate: every verb refuses without the state file, except
# 'open --enable' which is the sole path allowed to create it. ---
if [[ ! -f "$state_file" ]]; then
  if [[ "$verb" == open && $enable_flag -eq 1 ]]; then
    : # allowed: first enable
  else
    print -u2 -- "tunnel-codex: refused — no state file at $state_file; run 'open --enable' first (Law 2.4, exit 10)"
    exit 10
  fi
fi

# --- close / status are local-only: no app-server spawn, no python needed. Both are
# narrative/diagnostic, not a result — stdout purity (see header): nothing on stdout. ---
if [[ "$verb" == close ]]; then
  rm -f -- "$state_file"
  print -u2 -- "close: tunnel.state.json removed — Law 2.4 re-arms; next 'open' requires --enable again"
  exit 0
fi

if [[ "$verb" == status ]]; then
  if (( $+commands[jq] )); then
    jq . "$state_file" >&2
  else
    cat -- "$state_file" >&2
  fi
  exit 0
fi

# --- dispatch mechanics to python (open/send/steer/read/resume only) ---
if ! (( $+commands[python3] )); then
  print -u2 -- "tunnel-codex: python3 not found on PATH — cannot run app-server mechanics (exit 20)"
  exit 20
fi

py_args=("$verb" "--state" "$state_file")
case "$verb" in
  open)
    py_args+=(--sandbox "$sandbox_val")
    [[ -n "$model_val" ]] && py_args+=(--model "$model_val")
    ;;
  send|ask|steer)
    py_args+=("$text_arg")
    ;;
esac

exec python3 "$PY" "${py_args[@]}"
