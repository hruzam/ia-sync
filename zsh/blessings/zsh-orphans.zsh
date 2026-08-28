#!/usr/bin/env zsh
# zsh-orphans.zsh — deployed-vs-source drift reporter, parameterized over any
#                    deploy.sh leg (not just the zsh tree — name kept for history).
#
# WHY THIS EXISTS
#   deploy.sh rsyncs several trees WITHOUT --delete. Nothing removed from source is
#   ever removed from the machine, so a deployed tree is not a projection of its
#   source — it is an ACCRETION: the union of every state the source has ever been
#   in. First measured 2026-08-25 on home (zsh pair): 120 source files, 155
#   deployed, 37 orphans.
#
# WHY IT ONLY REPORTS
#   Plain `rsync --delete` would destroy the shell: the deployed `config.zsh` comes
#   from `config.home.zsh` and is rsync-EXCLUDED, so --delete reads it as an orphan.
#   Same for .env/ (secrets), .claude/, normalizer.py, and every log.
#   Beyond that: the classification below is a MAP, and maps in this tree have a
#   demonstrated record of being wrong in BOTH directions (2026-08-25 — AGENTS.md
#   claimed system/browser.zsh "never existed"; it was on disk. It listed five files
#   as "Maxwell must verify"; all five were live). An auto-deleter driven by a wrong
#   map deletes load-bearing files. So: this prints. A human decides.
#
# USAGE
#   zsh ~/.config/zsh/blessings/zsh-orphans.zsh                  # legacy: zsh pair
#   zsh .../zsh-orphans.zsh <preset>                              # named pair, see below
#   zsh .../zsh-orphans.zsh <source-dir> <deployed-dir>           # explicit pair
#   IA_SYNC_ZSH=/path/to/zsh zsh .../zsh-orphans.zsh              # override zsh source tree
#
# PRESETS (derived from deploy.sh's rsync legs, 2026-08-28):
#   zsh                    zsh/                    -> ~/.config/zsh            (deploy.sh:242-245) — default, no args
#   codex-agents           codex/agents/           -> ~/.codex/agents          (deploy.sh:111-115)
#   codex-skills           codex/skills/           -> ~/.agents/skills         (deploy.sh:117-121)
#   gemini                 gemini/agents/          -> ~/.gemini/agents         (deploy.sh:177-181)
#   gemini-config-projects gemini/config/projects/ -> ~/.gemini/config/projects (deploy.sh:200-203)
#
# NOTE the gemini block in deploy.sh (172-211) is FIVE legs, not one tree: the two
# rsync'd directories above plus three single-file copy_file() legs (state.json,
# GEMINI.md, mcp_config.json). The single-file legs are not comparable as trees and
# are not covered here.
#
# An explicit <source-dir> <deployed-dir> pair, or either gemini preset, runs with an
# EMPTY keep/kill policy and prints an "unaudited tree" header — see POLICY below.
#
# Report-only by contract. It has no delete path, by design, at any flag.

emulate -L zsh
setopt no_unset pipe_fail extended_glob glob_dots
# glob_dots is REQUIRED: without it zsh's **/* skips dotfiles, so .env/ and
# .claude/ vanish from the comparison silently. A drift reporter that omits part
# of the tree is worse than none. .git/ is filtered explicitly below instead.

# ---------------------------------------------------------------------------
# ARGUMENT RESOLUTION
#
#   0 args            -> preset "zsh" (exact legacy behavior, IA_SYNC_ZSH honored)
#   1 arg              -> named preset (zsh | codex-agents | codex-skills | gemini | gemini-config-projects)
#   2 args             -> explicit <source-dir> <deployed-dir>, unaudited policy
# ---------------------------------------------------------------------------
typeset PRESET="" SRC="" DEP=""
typeset -i UNAUDITED=0

case $# in
  0) PRESET="zsh" ;;
  1) PRESET="$1" ;;
  2) SRC="$1"; DEP="$2"; UNAUDITED=1 ;;
  *)
    print -u2 "usage: zsh-orphans.zsh [preset|<source-dir> <deployed-dir>]"
    print -u2 "  presets: zsh (default) · codex-agents · codex-skills · gemini · gemini-config-projects"
    exit 2
    ;;
esac

if [[ -n "$PRESET" ]]; then
  case "$PRESET" in
    zsh)
      SRC="${IA_SYNC_ZSH:-$HOME/ia-sync/zsh}"
      DEP="${HOME}/.config/zsh"
      ;;
    codex-agents)
      SRC="$HOME/ia-sync/codex/agents"
      DEP="$HOME/.codex/agents"
      ;;
    codex-skills)
      SRC="$HOME/ia-sync/codex/skills"
      DEP="$HOME/.agents/skills"
      ;;
    gemini)
      SRC="$HOME/ia-sync/gemini/agents"
      DEP="$HOME/.gemini/agents"
      UNAUDITED=1
      ;;
    gemini-config-projects)
      SRC="$HOME/ia-sync/gemini/config/projects"
      DEP="$HOME/.gemini/config/projects"
      UNAUDITED=1
      ;;
    *)
      print -u2 "zsh-orphans: unknown preset: $PRESET"
      print -u2 "  presets: zsh · codex-agents · codex-skills · gemini · gemini-config-projects"
      print -u2 "  or pass an explicit pair: zsh-orphans.zsh <source-dir> <deployed-dir>"
      exit 2
      ;;
  esac
fi

if [[ ! -d "$SRC" ]]; then
  print -u2 "zsh-orphans: source tree not found: $SRC"
  [[ "$PRESET" == "zsh" ]] && print -u2 "  (set IA_SYNC_ZSH if ia-sync lives elsewhere on this host)"
  exit 1
fi
if [[ ! -d "$DEP" ]]; then
  print -u2 "zsh-orphans: deployed tree not found: $DEP"
  exit 1
fi

# ---------------------------------------------------------------------------
# POLICY — the only part you edit.
#
# KEEP_GLOBS : machine-local by design. Deployed-only is CORRECT for these;
#              they must never be reported as removable.
# KILL_GLOBS : known-safe classes. Deployed-only is always litter here.
#
# Every entry moved from UNKNOWN into one of these lists makes the next run
# quieter. UNKNOWN is meant to shrink toward zero over time.
#
# Policy is scoped to the pair being audited — an established keep/kill map for
# the zsh tree says nothing safe about, say, ~/.codex/agents. Only the zsh preset
# carries an established policy today (below). codex-agents/codex-skills are
# policy-empty on purpose: deploy.sh's contract for those legs is "source is
# canonical", so every deployed-only file is already an orphan — nothing to KEEP,
# nothing pre-classified as safe-to-KILL either (that judgment has not been made
# yet), so they surface as UNKNOWN. gemini presets and any explicit pair are
# unaudited: empty policy + a printed header saying so (see UNAUDITED below).
# ---------------------------------------------------------------------------
typeset -a KEEP_GLOBS KILL_GLOBS

if [[ "$PRESET" == "zsh" ]]; then
  KEEP_GLOBS=(
    'config.zsh'                          # deployed from config.<machine>.zsh (rsync-excluded)
    '.zshrc'                              # deployed from zshrc.<machine>
    '.env'                                # secrets dir — never in repo (sync.deny)
    '.env/*'
    '.claude'                             # machine-local settings
    '.claude/*'
    '*.log'                               # runtime logs
    'archive'                             # machine-local parked history
    'archive/*'
    '*/journal.*.jsonl'                   # runtime journals (archx etc.)
    'temple-project-map.zsh'              # GENERATED by registries/gen-temple-map.sh at deploy
    # normalizer.py / harness.machine-project-registry.json unpinned 2026-08-28 —
    # home migrated to inline PROJECT_* exports and both deployed copies were
    # retired (moved to /tmp/normalizer-retired-2026-08-28). No longer load-bearing.
  )

  KILL_GLOBS=(
    '*.bak-*'                             # deploy.sh copy_file() exhaust — unbounded
    '*.backup'
    '*.stale-*'
    'substrate.*'                         # sync.deny'd cross-machine contamination
  )
else
  # codex-agents, codex-skills: source-is-canonical, no established keep/kill map yet.
  # gemini presets / explicit pair: unaudited (UNAUDITED=1 set above), same empty policy.
  KEEP_GLOBS=()
  KILL_GLOBS=()
fi

# Never compared at all — VCS internals would flood UNKNOWN with noise.
typeset -a SKIP_GLOBS
SKIP_GLOBS=('.git' '.git/*')

# ---------------------------------------------------------------------------

_zo_list() {
  # $1 = tree root. Emits relative paths of regular files, minus SKIP_GLOBS.
  local root="$1" f g skip
  local -a out
  for f in ${(f)"$(cd "$root" && print -rl -- **/*(.N))"}; do
    skip=""
    for g in $SKIP_GLOBS; do
      [[ "$f" == ${~g} ]] && { skip=1; break; }
    done
    [[ -z "$skip" ]] && out+=("$f")
  done
  print -rl -- ${(o)out}
}

typeset -a src_files dep_files
src_files=(${(f)"$(_zo_list "$SRC")"})
dep_files=(${(f)"$(_zo_list "$DEP")"})

typeset -a orphans missing
orphans=(${dep_files:|src_files})   # deployed but not in source
missing=(${src_files:|dep_files})   # in source but not deployed

typeset -a bucket_keep bucket_kill bucket_unknown
typeset f g matched

for f in $orphans; do
  matched=""
  for g in $KEEP_GLOBS; do
    if [[ "$f" == ${~g} ]]; then matched="keep"; break; fi
  done
  if [[ -z "$matched" ]]; then
    for g in $KILL_GLOBS; do
      if [[ "$f" == ${~g} ]]; then matched="kill"; break; fi
    done
  fi
  case "$matched" in
    keep) bucket_keep+=("$f") ;;
    kill) bucket_kill+=("$f") ;;
    *)    bucket_unknown+=("$f") ;;
  esac
done

print -- "zsh-orphans · $(date +%Y-%m-%d) · host=${MACHINE_NAME:-unknown} · pair=${PRESET:-custom}"
print -- "source   : $SRC  (${#src_files} files)"
print -- "deployed : $DEP  (${#dep_files} files)"
print -- ""

if (( UNAUDITED )); then
  print -- "unaudited tree — keep-set policy not established"
  print -- ""
fi

print -- "KEEP — deployed-only by design (${#bucket_keep})"
if (( ${#bucket_keep} )); then
  for f in $bucket_keep; do print -- "    $DEP/$f"; done
else
  print -- "    (none)"
fi
print -- ""

print -- "KILL — known-safe litter (${#bucket_kill})"
if (( ${#bucket_kill} )); then
  for f in $bucket_kill; do print -- "    $DEP/$f"; done
else
  print -- "    (none)"
fi
print -- ""

print -- "UNKNOWN — needs a human (${#bucket_unknown})"
if (( ${#bucket_unknown} )); then
  for f in $bucket_unknown; do print -- "    $DEP/$f"; done
  print -- ""
  print -- "  Each of these is either machine-local (add to KEEP_GLOBS) or dead"
  print -- "  (add to KILL_GLOBS, or quarantine it). Trace before deciding:"
  print -- "    grep -rn '<basename>' --include='*.zsh' --include='*.sh' $DEP"
else
  print -- "    (none — policy covers every orphan)"
fi
print -- ""

if (( ${#missing} )); then
  print -- "NOT DEPLOYED — in source, absent on this host (${#missing})"
  print -- "  Expected for host-specific files (config.*.zsh, zshrc.*) — anything else"
  print -- "  means a deploy has not run since that file was added."
  for f in $missing; do print -- "    $SRC/$f"; done
  print -- ""
fi

if (( ${#bucket_kill} )); then
  typeset q="/tmp/zsh-prune-$(date +%Y-%m-%d)"
  print -- "Quarantine the KILL bucket (two-phase: move now, purge after a clean shell):"
  print -- ""
  print -- "  mkdir -p $q && cd $DEP && for f in ${bucket_kill}; do"
  print -- "    mkdir -p \"$q/\$(dirname \$f)\" && mv \"\$f\" \"$q/\$f\"; done"
  print -- ""
  print -- "  # verify, then purge:"
  print -- "  zsh -n $DEP/config.zsh && zsh -n $DEP/ai/base.zsh && echo OK"
  print -- "  # rm -rf $q     <- only after a fresh shell comes up clean"
fi

exit 0
