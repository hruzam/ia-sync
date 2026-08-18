#!/usr/bin/env zsh
# =============================================================================
# KEYS.ZSH — Global claviature engine (derived keys panel)
# =============================================================================
# Location: ~/.config/zsh/ai/keys.zsh
# Sourced by: base.zsh PARTITION 9
# Contract: sourced-only; defines ONE public body _keys; no aliases; no side
#           effects on source. Pure interactive engine (.zsh per rule).
# Spec: guides/claviature.global.spec.md (LOCKED 2026-07-11)
# =============================================================================

# ── family map: prefix → section label ───────────────────────────────────────
# Registered families only. Unknown prefixes land in UNSORTED (grammar drift).
typeset -gA _KEYS_FAMILY_MAP=(
  g              'Gemini'
  gemini         'Gemini'
  agy            'Antigravity'
  rc             'Claude RC'
  temple         'Temple transport'
  doorbell       'Temple transport (shims)'
  mail           'Temple transport (shims)'
  transport      'Temple transport (shims)'
  adr            'Temple gate'
  tree           'Temple utilities'
  harness        'Harness'
  fr             'devenv (freya)'
  bo             'devenv (fantasyobchod)'
  devenv         'devenv'
  php            'PHP switch'
  archx          'ArchX'
  ai             'Help panels'
  project        'Project map'
  zenith         'Zenith-ZSH (RAG assistant)'
  command        'Command Palette'
  palette        'Command Palette'
)

# ── singles map: exact bare name → section label ─────────────────────────────
typeset -gA _KEYS_SINGLES_MAP=(
  g              'Gemini'
  fo             'Project switchers'
  im             'Project switchers'
  psd            'Project switchers'
  ltp            'Project switchers'
  sess           'Project switchers'
  lrv            'Project switchers'
  imdev          'Project switchers'
  fodev          'Project switchers'
  php74          'PHP / Composer'
  php8           'PHP / Composer'
  phpst          'PHP / Composer'
  composer74     'PHP / Composer'
  composer8      'PHP / Composer'
  src            'System shell'
  ord            'System shell'
  hasz           'System shell'
  cod            'System shell'
  mygrep         'System shell'
  msrc           'System shell'
  smart_commit   'Git lifecycle'
  git_phases     'Git lifecycle'
  shpub          'Shared toolkit'
  shdiff         'Shared toolkit'
  shstat         'Shared toolkit'
  shsyntax       'Shared toolkit'
  keys           'Help panels'
  octo           'Octopus'
)

# ── noise exclusion: zsh machinery + shell internals ────────────────────────
typeset -a _KEYS_NOISE=(
  'gitstatus_*'
  '_p9k*'
  'p9k*'
  'p10k*'
  'prompt_*'
  'instant_prompt_*'
  'zle-*'
  'zle_*'
  'compinit'
  'compdef'
  'compdump'
  'compaudit'
  'bashcompinit'
  'add-zsh-hook*'
  'add-zle-hook-widget*'
  'is-at-least'
  'colors'
  'regexp-replace'
  'zrecompile'
  'zmv'
  'zcalc*'
  'run-help*'
  'which-command'
  'VCS_INFO_*'
  'vcs_info*'
  'zsh_*'
  'url-quote-magic'
  'bracketed-paste*'
  '*-line-or-beginning-search'
  'edit-command-line'
  'insert-*'
  'select-*'
  'spectrum_*'
  'iterm2_*'
  'precmd*'
  'preexec*'
  'chpwd*'
  'TRAP*'
  'xsource'
  'xunfunction'
  'pmodload'
  'handle-*'
  'azhw*'
  'max-history-size'
  'mkcd'
)

# =============================================================================
# _keys [--plain] [--all]
# Collect live shell surface, bucket by family prefix / singles map,
# print one section per label. UNSORTED always last.
# --plain: zero ANSI, one entry per line as "<label>\t<key>"
# --all: disable noise filter (include shell internals)
# =============================================================================
# keys — print the derived claviature panel: live functions/aliases, bucketed by family
_keys() {
  local plain=0 all=0
  [[ "${1}" == '--plain' ]] && plain=1
  [[ "${1}" == '--all' ]] && all=1
  [[ "${2}" == '--plain' ]] && plain=1
  [[ "${2}" == '--all' ]] && all=1

  # ── collect live surface ──────────────────────────────────────────────────
  # Aliases: names only
  local -a raw_aliases
  raw_aliases=( ${(k)aliases} )

  # Functions: names only (from ${(k)functions})
  local -a raw_functions
  raw_functions=( ${(k)functions} )

  # ── bucket: label → list of "name" or "name()" ───────────────────────────
  typeset -A buckets      # label → space-separated entries
  local -a unsorted_keys
  local hidden_count=0

  local name entry prefix label

  # Helper: check if name matches noise patterns
  _keys_is_noise() {
    local n="$1"
    # Always exclude names containing '::'
    [[ "${n}" == *::* ]] && return 0
    # Skip noise filter if --all flag
    (( all )) && return 1
    # Directly check against each noise pattern using [[ ]] globbing
    [[ "${n}" == gitstatus_* ]] && return 0
    [[ "${n}" == _p9k* ]] && return 0
    [[ "${n}" == p9k* ]] && return 0
    [[ "${n}" == p10k* ]] && return 0
    [[ "${n}" == prompt_* ]] && return 0
    [[ "${n}" == instant_prompt_* ]] && return 0
    [[ "${n}" == zle-* ]] && return 0
    [[ "${n}" == zle_* ]] && return 0
    [[ "${n}" == compinit ]] && return 0
    [[ "${n}" == compdef ]] && return 0
    [[ "${n}" == compdump ]] && return 0
    [[ "${n}" == compaudit ]] && return 0
    [[ "${n}" == bashcompinit ]] && return 0
    [[ "${n}" == add-zsh-hook* ]] && return 0
    [[ "${n}" == add-zle-hook-widget* ]] && return 0
    [[ "${n}" == is-at-least ]] && return 0
    [[ "${n}" == colors ]] && return 0
    [[ "${n}" == regexp-replace ]] && return 0
    [[ "${n}" == zrecompile ]] && return 0
    [[ "${n}" == zmv ]] && return 0
    [[ "${n}" == zcalc* ]] && return 0
    [[ "${n}" == run-help* ]] && return 0
    [[ "${n}" == which-command ]] && return 0
    [[ "${n}" == VCS_INFO_* ]] && return 0
    [[ "${n}" == vcs_info* ]] && return 0
    [[ "${n}" == zsh_* ]] && return 0
    [[ "${n}" == url-quote-magic ]] && return 0
    [[ "${n}" == bracketed-paste* ]] && return 0
    [[ "${n}" == *-line-or-beginning-search ]] && return 0
    [[ "${n}" == edit-command-line ]] && return 0
    [[ "${n}" == insert-* ]] && return 0
    [[ "${n}" == select-* ]] && return 0
    [[ "${n}" == spectrum_* ]] && return 0
    [[ "${n}" == iterm2_* ]] && return 0
    [[ "${n}" == precmd* ]] && return 0
    [[ "${n}" == preexec* ]] && return 0
    [[ "${n}" == chpwd* ]] && return 0
    [[ "${n}" == TRAP* ]] && return 0
    [[ "${n}" == xsource ]] && return 0
    [[ "${n}" == xunfunction ]] && return 0
    [[ "${n}" == pmodload ]] && return 0
    [[ "${n}" == handle-* ]] && return 0
    [[ "${n}" == azhw* ]] && return 0
    [[ "${n}" == max-history-size ]] && return 0
    [[ "${n}" == mkcd ]] && return 0
    return 1
  }

  # Helper: assign to bucket
  _keys_add() {
    local lbl="$1" ent="$2"
    if [[ -n "${buckets[$lbl]}" ]]; then
      buckets[$lbl]+=" ${ent}"
    else
      buckets[$lbl]="${ent}"
    fi
  }

  # Process aliases
  for name in "${raw_aliases[@]}"; do
    # Exclude private (starts with _) and noise (starts with . or no alphanumerics)
    [[ -z "${name}" ]] && continue
    [[ "${name}" == _* ]] && continue
    [[ "${name}" == .* ]] && continue
    [[ "${name}" =~ [[:alnum:]] ]] || continue
    # Exclude zle widget/hook noise (names containing ':')
    [[ "${name}" == *:* ]] && continue
    # Apply noise filter
    if _keys_is_noise "${name}"; then
      (( hidden_count++ ))
      continue
    fi

    entry="${name}"

    # (a) contains hyphen → use prefix before first hyphen
    if [[ "${name}" == *-* ]]; then
      prefix="${name%%-*}"
      label="${_KEYS_FAMILY_MAP[$prefix]}"
      if [[ -n "${label}" ]]; then
        _keys_add "${label}" "${entry}"
      else
        unsorted_keys+=( "${entry}" )
      fi
    else
      # (b) bare name → singles map
      label="${_KEYS_SINGLES_MAP[$name]}"
      if [[ -n "${label}" ]]; then
        _keys_add "${label}" "${entry}"
      else
        unsorted_keys+=( "${entry}" )
      fi
    fi
  done

  # Process functions (suffix with "()")
  for name in "${raw_functions[@]}"; do
    [[ -z "${name}" ]] && continue
    [[ "${name}" == _* ]] && continue
    [[ "${name}" == .* ]] && continue
    [[ "${name}" =~ [[:alnum:]] ]] || continue
    # Exclude zle widget/hook noise (names containing ':')
    [[ "${name}" == *:* ]] && continue
    # Apply noise filter
    if _keys_is_noise "${name}"; then
      (( hidden_count++ ))
      continue
    fi

    entry="${name}()"

    if [[ "${name}" == *-* ]]; then
      prefix="${name%%-*}"
      label="${_KEYS_FAMILY_MAP[$prefix]}"
      if [[ -n "${label}" ]]; then
        _keys_add "${label}" "${entry}"
      else
        unsorted_keys+=( "${entry}" )
      fi
    else
      label="${_KEYS_SINGLES_MAP[$name]}"
      if [[ -n "${label}" ]]; then
        _keys_add "${label}" "${entry}"
      else
        unsorted_keys+=( "${entry}" )
      fi
    fi
  done

  # ── collect and sort labels ───────────────────────────────────────────────
  local -a labels
  labels=( ${(k)buckets} )
  labels=( ${(o)labels} )   # sort alphabetically

  # ── output ────────────────────────────────────────────────────────────────
  local bold_on='' bold_off=''
  if (( plain == 0 )); then
    bold_on=$'\e[1m'
    bold_off=$'\e[0m'
  fi

  for label in "${labels[@]}"; do
    local -a entries
    entries=( ${(s: :)buckets[$label]} )
    entries=( ${(o)entries} )   # sort entries within section

    if (( plain )); then
      for entry in "${entries[@]}"; do
        print "${label}\t${entry}"
      done
    else
      print "${bold_on}${label}${bold_off}"
      for entry in "${entries[@]}"; do
        print "  ${entry}"
      done
      print ''
    fi
  done

  # ── UNSORTED last ─────────────────────────────────────────────────────────
  if (( ${#unsorted_keys[@]} > 0 )); then
    local -a sorted_unsorted
    sorted_unsorted=( ${(o)unsorted_keys} )

    if (( plain )); then
      for entry in "${sorted_unsorted[@]}"; do
        print "UNSORTED (grammar drift)\t${entry}"
      done
    else
      print "${bold_on}UNSORTED (grammar drift — register the family or fix the name)${bold_off}"
      for entry in "${sorted_unsorted[@]}"; do
        print "  ${entry}"
      done
      print ''
    fi
  fi

  # ── hidden count footer ───────────────────────────────────────────────────
  if (( hidden_count > 0 && all == 0 )); then
    print "(+ ${hidden_count} shell internals hidden — 'keys --all' to include)"
  fi

  # cleanup inner helper
  unfunction _keys_add 2>/dev/null
  unfunction _keys_is_noise 2>/dev/null
}
