#!/bin/zsh

# Core checking script for settings card freshness
# Location: ~/.config/zsh/scheduled/harness-check.zsh

# Load config path
CONFIG_FILE="${HOME}/.config/zsh/registries/ai.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Registry config not found at $CONFIG_FILE" >&2
  exit 1
fi

# Parsing JSON values dynamically
_parse_json_value() {
  local key=$1
  local file=$2
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import json; print(json.load(open('$file')).get('$key', ''))" 2>/dev/null && return
  fi
  if command -v jq >/dev/null 2>&1; then
    jq -r ".[\"$key\"]" "$file" 2>/dev/null && return
  fi
  awk -v k="$key" -F'"' '{
    for(i=1; i<=NF; i++) {
      if($i==k) {
        for(j=i+1; j<=NF; j++) {
          if($j ~ /[^:, \t\r\n]/) {
            print $j
            exit
          }
        }
      }
    }
  }' "$file"
}

# Expand ~ and environment variables
_expand_path() {
  local p=$1
  p="${p/#\~\//$HOME/}"
  echo "$p"
}

# Extract values from ai.json
pattern_raw=$(_parse_json_value "native-primitives-update-pattern" "$CONFIG_FILE")
mail_dir_raw=$(_parse_json_value "mail-inbox-dir" "$CONFIG_FILE")

if [[ -z "$pattern_raw" ]]; then
  echo "Error: Key 'native-primitives-update-pattern' not defined in $CONFIG_FILE" >&2
  exit 1
fi

# Expand paths
PATTERN_EXPANDED=$(_expand_path "$pattern_raw")
MAIL_DIR_EXPANDED=$(_expand_path "${mail_dir_raw:-~/reposoma/_mail/toAll/inbox}")
# Normalise: strip all trailing slashes (registry value may end in '/'); a bare '/' stays '/'
while [[ "$MAIL_DIR_EXPANDED" == ?*/ ]]; do
  MAIL_DIR_EXPANDED="${MAIL_DIR_EXPANDED%/}"
done

# Check for --debug or harness-stale command name
DEBUG_MODE=0
if [[ "$1" == "--debug" || "$0" == *harness-stale* ]]; then
  DEBUG_MODE=1
fi

# Two trees (option C, gaveled 2026-11-25):
#   --debug / harness-stale  scans the LIVE tree ~/reposoma and writes nothing.
#   mail mode (the timer)    scans, writes, commits and pushes ONLY inside its own clone
#                            MAIL_REPO. It never touches ~/reposoma (no pull, no write).
LIVE_REPO="${HOME}/reposoma"
MAIL_REPO="${HARNESS_MAIL_REPO:-$HOME/.local/share/harness/reposoma-mail}"
MAIL_BRANCH="core"
MAIL_ATTEMPTS=3                                   # publish attempts (fetch→reset→write→push)
FETCH_TRIES=3
FETCH_DELAY="${HARNESS_FETCH_RETRY_DELAY:-60}"    # seconds between fetch tries
MAIL_NAME_PREFIX="zsh.stale-settings-cards-"

# Rewrite a "$HOME/reposoma/..." path onto another root. Prints nothing (status 1) if the
# path is not under the live tree — mail mode must then refuse rather than write elsewhere.
_rebase_live_path() {
  local p=$1 root=$2
  [[ "$p" == "$LIVE_REPO" ]] && { echo "$root"; return 0; }
  [[ "$p" == "$LIVE_REPO/"* ]] || return 1
  echo "$root/${p#"$LIVE_REPO/"}"
}

_die() { echo "harness-check: ERROR: $*" >&2; exit 1; }
_log() { echo "harness-check: $*"; }

if [[ $DEBUG_MODE -eq 1 ]]; then
  SCAN_ROOT="$LIVE_REPO"
else
  # ── SAFETY GUARDS — all read-only; any failure aborts before anything is touched ──
  [[ -d "$MAIL_REPO" ]] || _die "mail clone missing: $MAIL_REPO — run ia-sync deploy.sh on the scheduled host (it creates the clone), or set HARNESS_MAIL_REPO"
  MAIL_REPO_REAL=$(realpath -e -- "$MAIL_REPO" 2>/dev/null) || _die "cannot resolve $MAIL_REPO"
  LIVE_REPO_REAL=$(realpath -m -- "$LIVE_REPO" 2>/dev/null)
  [[ "$MAIL_REPO_REAL" != "$LIVE_REPO_REAL" ]] || _die "MAIL_REPO resolves to the live tree $LIVE_REPO_REAL — refusing"
  mail_top=$(git -C "$MAIL_REPO_REAL" rev-parse --show-toplevel 2>/dev/null) || _die "$MAIL_REPO_REAL is not a git work tree"
  [[ "$(realpath -m -- "$mail_top")" == "$MAIL_REPO_REAL" ]] || _die "$MAIL_REPO_REAL is not the top of its repo (toplevel: $mail_top) — refusing"
  want_origin=$(git -C "$LIVE_REPO" remote get-url origin 2>/dev/null) || _die "cannot read origin of $LIVE_REPO (needed to verify the clone)"
  have_origin=$(git -C "$MAIL_REPO_REAL" remote get-url origin 2>/dev/null) || _die "$MAIL_REPO_REAL has no origin remote"
  [[ -n "$want_origin" && "$have_origin" == "$want_origin" ]] || _die "clone origin '$have_origin' != live origin '$want_origin' — refusing"
  MAIL_REPO="$MAIL_REPO_REAL"
  SCAN_ROOT="$MAIL_REPO"

  # One run at a time (timer, Restart=, and a manual start must not interleave).
  exec 9>"${MAIL_REPO}.lock" || _die "cannot open lock ${MAIL_REPO}.lock"
  if ! flock -n 9; then
    _log "another harness-check run holds ${MAIL_REPO}.lock — skipping this run"
    exit 0
  fi

  # Non-interactive git: never prompt (systemd has no tty and no SSH agent).
  export GIT_TERMINAL_PROMPT=0
  if [[ -z "${GIT_SSH_COMMAND:-}" && -z "$(git -C "$MAIL_REPO" config core.sshCommand)" ]]; then
    export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=20"
  fi
fi

# Map the registry paths onto the tree being scanned.
if [[ "$SCAN_ROOT" != "$LIVE_REPO" ]]; then
  PATTERN_EXPANDED=$(_rebase_live_path "$PATTERN_EXPANDED" "$SCAN_ROOT") \
    || _die "native-primitives-update-pattern is not under ~/reposoma/ — cannot map it into $SCAN_ROOT"
  MAIL_DIR_EXPANDED=$(_rebase_live_path "$MAIL_DIR_EXPANDED" "$SCAN_ROOT") \
    || _die "mail-inbox-dir is not under ~/reposoma/ — cannot map it into $SCAN_ROOT"
  MAIL_ARCHIVE_DIR="${MAIL_DIR_EXPANDED%/inbox}/archive"
  [[ "$MAIL_ARCHIVE_DIR" != "$MAIL_DIR_EXPANDED" ]] || _die "mail-inbox-dir must end in /inbox (archive is its sibling)"
fi
GUIDES_DIR="${SCAN_ROOT}/raw.guides"

# Header output for debug mode
if [[ $DEBUG_MODE -eq 1 ]]; then
  echo "=========================================="
  echo " HARNESS-CHECK: CARD FRESHNESS REPORT     "
  echo "=========================================="
  echo "Pattern Checked:  $PATTERN_EXPANDED"
  echo "Guides Dir:       $GUIDES_DIR"
  echo "Mail Destination: $(_rebase_live_path "$MAIL_DIR_EXPANDED" "$MAIL_REPO" || echo "$MAIL_DIR_EXPANDED") (written by the timer, in its own clone)"
  echo "------------------------------------------"
fi

CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_EPOCH=$(date +%s)
FS=$'\x1f'  # unit separator — cannot occur in card frontmatter
# awk trim(): strip surrounding whitespace, then exactly ONE matching outer quote pair ('…' or "…"),
# then whitespace again — inner/closing quotes of the value itself survive. q is passed via -v q="'".
AWK_TRIM='
  function trim(s,   c) {
    gsub(/^[ \t]+|[ \t]+$/, "", s)
    c = substr(s, 1, 1)
    if (length(s) >= 2 && (c == q || c == "\"") && substr(s, length(s), 1) == c) {
      s = substr(s, 2, length(s) - 2)
      gsub(/^[ \t]+|[ \t]+$/, "", s)
    }
    return s
  }
'
CURRENT_WEEK=$(date +%G-W%V)

# Scan both sets (settings cards + guides) under SCAN_ROOT into STALE_CARDS.
# The loop bodies are unchanged from the single-tree version; only the roots moved.
scan_cards() {
STALE_CARDS=()

# Process each matching card file
# We use Zsh's globbing ${~PATTERN_EXPANDED}
for file in ${~PATTERN_EXPANDED}; do
  if [[ ! -f "$file" ]]; then
    continue
  fi

  # Initialize values
  card=""
  brand=""
  verified=""
  half_life_days=""
  verify_cmd=""
  rechecks=""

  # Parsing frontmatter cleanly
  while IFS= read -r line; do
    case "$line" in
      CARD=*) card="${line#CARD=}" ;;
      BRAND=*) brand="${line#BRAND=}" ;;
      VERIFIED=*) verified="${line#VERIFIED=}" ;;
      DAYS=*) half_life_days="${line#DAYS=}" ;;
      CMD=*) verify_cmd="${line#CMD=}" ;;
      RECHECKS=*) rechecks="${line#RECHECKS=}" ;;
    esac
  done < <(awk -v q="'" "$AWK_TRIM"'
    /^---$/ { count++; next }
    count == 1 {
      if ($1 ~ /^card:/) { sub(/^card:[ \t]*/, ""); card=$0 }
      if ($1 ~ /^brand:/) { sub(/^brand:[ \t]*/, ""); brand=$0 }
      if ($1 ~ /^verified:/) { sub(/^verified:[ \t]*/, ""); verified=$0 }
      if ($1 ~ /^half_life_days:/) { sub(/^half_life_days:[ \t]*/, ""); half_life_days=$0 }
      if ($1 ~ /^verify_cmd:/) { sub(/^verify_cmd:[ \t]*/, ""); verify_cmd=$0 }
      if (in_recheck && $1 ~ /^-/) {
        link=$0; sub(/^[ \t]*- /, "", link); sub(/[ \t]*#.*$/, "", link); gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", link)
        if (link != "") rechecks = (rechecks == "" ? link : rechecks "," link)
      }
      if ($1 ~ /^recheck:/) { in_recheck=1 }
      else if ($1 ~ /^[a-zA-Z0-9_]+:/) { in_recheck=0 }
    }
    count == 2 { exit }
    END {
      card = trim(card)
      brand = trim(brand)
      verified = trim(verified)
      half_life_days = trim(half_life_days)
      verify_cmd = trim(verify_cmd)
      print "CARD=" card
      print "BRAND=" brand
      print "VERIFIED=" verified
      print "DAYS=" half_life_days
      print "CMD=" verify_cmd
      print "RECHECKS=" rechecks
    }
  ' "$file")

  # Skip if basic info is missing
  if [[ -z "$card" || -z "$verified" ]]; then
    if [[ $DEBUG_MODE -eq 1 ]]; then
      echo "[-] Skipping $(basename "$file"): missing 'card' or 'verified' metadata."
    fi
    continue
  fi
  [[ -z "$brand" ]] && brand="$card"

  # Default threshold is 30 days
  threshold=${half_life_days:-30}

  # Parse verified date to epoch
  verified_epoch=$(date -d "$verified" +%s 2>/dev/null || date -f "$verified" +%s 2>/dev/null)
  if [[ -z "$verified_epoch" ]]; then
    if [[ $DEBUG_MODE -eq 1 ]]; then
      echo "[-] Skipping $card: invalid verified date format ($verified)."
    fi
    continue
  fi

  # Calculate elapsed days
  diff_seconds=$((CURRENT_EPOCH - verified_epoch))
  elapsed_days=$((diff_seconds / 86400))

  # Check staleness
  is_stale=0
  if [[ $elapsed_days -ge $threshold ]]; then
    is_stale=1
    # Store card data in array format:
    # card FS brand FS verified FS threshold FS elapsed FS verify_cmd FS rechecks
    STALE_CARDS+=("${card}${FS}${brand}${FS}${verified}${FS}${threshold}${FS}${elapsed_days}${FS}${verify_cmd}${FS}${rechecks}")
  fi

  if [[ $DEBUG_MODE -eq 1 ]]; then
    if [[ $is_stale -eq 1 ]]; then
      echo "[!] $brand ($card): STALE"
      echo "    Verified: $verified | Elapsed: $elapsed_days days | Limit: $threshold days"
    else
      echo "[✓] $brand ($card): FRESH"
      echo "    Verified: $verified | Elapsed: $elapsed_days days | Limit: $threshold days"
    fi
  fi
done

# Scan raw.guides/ — selection by frontmatter presence (verified: + half_life_days:), not filename pattern
if [[ $DEBUG_MODE -eq 1 ]]; then
  echo ""
  echo "--- Guides scan: $GUIDES_DIR ---"
fi

if [[ -d "$GUIDES_DIR" ]]; then
  while IFS= read -r file; do
    [[ ! -f "$file" ]] && continue

    card=""
    brand=""
    verified=""
    half_life_days=""
    verify_cmd=""
    rechecks=""

    while IFS= read -r line; do
      case "$line" in
        CARD=*) card="${line#CARD=}" ;;
        BRAND=*) brand="${line#BRAND=}" ;;
        VERIFIED=*) verified="${line#VERIFIED=}" ;;
        DAYS=*) half_life_days="${line#DAYS=}" ;;
        CMD=*) verify_cmd="${line#CMD=}" ;;
        RECHECKS=*) rechecks="${line#RECHECKS=}" ;;
      esac
    done < <(awk -v q="'" "$AWK_TRIM"'
      /^---$/ { count++; next }
      count == 1 {
        if ($1 ~ /^card:/) { sub(/^card:[ \t]*/, ""); card=$0 }
        if ($1 ~ /^brand:/) { sub(/^brand:[ \t]*/, ""); brand=$0 }
        if ($1 ~ /^verified:/) { sub(/^verified:[ \t]*/, ""); verified=$0 }
        if ($1 ~ /^half_life_days:/) { sub(/^half_life_days:[ \t]*/, ""); half_life_days=$0 }
        if ($1 ~ /^verify_cmd:/) { sub(/^verify_cmd:[ \t]*/, ""); verify_cmd=$0 }
      }
      count == 2 { exit }
      END {
        card = trim(card)
        brand = trim(brand)
        verified = trim(verified)
        half_life_days = trim(half_life_days)
        verify_cmd = trim(verify_cmd)
        print "CARD=" card
        print "BRAND=" brand
        print "VERIFIED=" verified
        print "DAYS=" half_life_days
        print "CMD=" verify_cmd
        print "RECHECKS=" rechecks
      }
    ' "$file")

    # Guide selection: must have both verified: and half_life_days: in frontmatter
    if [[ -z "$verified" || -z "$half_life_days" ]]; then
      if [[ $DEBUG_MODE -eq 1 ]]; then
        echo "[-] Skipping $(basename "$file"): not a freshness-tracked guide (missing verified: or half_life_days:)."
      fi
      continue
    fi

    # Derive card/brand from the path if not in frontmatter: <dir>/GUIDE.md → <dir>,
    # <dir>/<name>.md → <dir>/<name>, top-level <name>.md → <name>. (Was basename only, so
    # every <dir>/GUIDE.md row read "GUIDE" and the alert rows were indistinguishable.)
    if [[ -z "$card" ]]; then
      guide_rel="${file#"$GUIDES_DIR"/}"
      guide_dir="${guide_rel:h}"
      guide_base="${guide_rel:t:r}"
      if [[ "$guide_dir" == "." || "$guide_dir" == "$guide_rel" ]]; then
        card="$guide_base"
      elif [[ "$guide_base" == "GUIDE" ]]; then
        card="$guide_dir"
      else
        card="$guide_dir/$guide_base"
      fi
    fi
    [[ -z "$brand" ]] && brand="guide:$card"
    [[ -z "$brand" ]] && brand="$card"

    # Default threshold (guides default to half_life_days from frontmatter; no prose fallback needed)
    threshold=$half_life_days

    # Parse verified date to epoch
    verified_epoch=$(date -d "$verified" +%s 2>/dev/null || date -f "$verified" +%s 2>/dev/null)
    if [[ -z "$verified_epoch" ]]; then
      if [[ $DEBUG_MODE -eq 1 ]]; then
        echo "[-] Skipping $card: invalid verified date format ($verified)."
      fi
      continue
    fi

    # Calculate elapsed days
    diff_seconds=$((CURRENT_EPOCH - verified_epoch))
    elapsed_days=$((diff_seconds / 86400))

    # Check staleness
    is_stale=0
    if [[ $elapsed_days -ge $threshold ]]; then
      is_stale=1
      STALE_CARDS+=("${card}${FS}${brand}${FS}${verified}${FS}${threshold}${FS}${elapsed_days}${FS}${verify_cmd}${FS}${rechecks}")
    fi

    if [[ $DEBUG_MODE -eq 1 ]]; then
      if [[ $is_stale -eq 1 ]]; then
        echo "[!] $brand ($card): STALE"
        echo "    Verified: $verified | Elapsed: $elapsed_days days | Limit: $threshold days"
      else
        echo "[✓] $brand ($card): FRESH"
        echo "    Verified: $verified | Elapsed: $elapsed_days days | Limit: $threshold days"
      fi
    fi
  done < <(find "$GUIDES_DIR" -maxdepth 2 -name "*.md" -type f | sort)
fi
}

# Render the alert for the current STALE_CARDS to stdout. Deterministic: same stale set and
# week → same bytes (no timestamp, no host in the body).
render_mail() {
  local stale_count=${#STALE_CARDS[@]}
  echo "---"
  echo "title: Stale Settings Cards Alert"
  echo "week: ${CURRENT_WEEK}"
  echo "stale_count: ${stale_count}"
  echo "---"
  echo ""
  echo "# Stale Settings Cards Alert"
  echo ""
  echo "The following settings/knowledge cards are past their freshness threshold (half-life) and require manual re-verification."
  echo ""
  echo "| Brand / Card | Last Verified | Threshold (Days) | Elapsed (Days) | Verification Command & Recheck Links |"
  echo "| :--- | :---: | :---: | :---: | :--- |"

  for item in "${STALE_CARDS[@]}"; do
    IFS="$FS" read -r c b v t e cmd r <<< "$item"

    # Format links if any
    links_formatted=""
    if [[ -n "$r" ]]; then
      IFS=',' read -r -A links_arr <<< "$r"
      for link in "${links_arr[@]}"; do
        # Truncate link display
        display_link="${link#https://}"
        display_link="${display_link#www.}"
        if [[ ${#display_link} -gt 35 ]]; then
          display_link="${display_link:0:32}..."
        fi
        links_formatted+="[[link]($link)] "
      done
    fi

    cmd_formatted=""
    if [[ -n "$cmd" ]]; then
      cmd_md="${cmd//|/\\|}"
      cmd_formatted="\`$cmd_md\`"
    fi

    echo "| **$b**<br>($c) | $v | $t | **$e** | $cmd_formatted<br>$links_formatted |"
  done

  echo ""
  echo "---"
  echo "*Automated notification from the zsh card-freshness checker (week ${CURRENT_WEEK}), published once per ISO week by the scheduled host from its own clone. Do not edit. To dismiss, \`git mv\` it to \`_mail/toAll/archive/\` and commit. To run manually: \`harness-stale\`.*"
}

# Bring the clone to exactly origin/core: fetch (FETCH_TRIES tries, FETCH_DELAY apart), then
# reset --hard + clean. Runs ONLY inside MAIL_REPO (guarded above).
sync_clone() {
  local try branch
  branch=$(git -C "$MAIL_REPO" symbolic-ref --short -q HEAD) || branch=""
  [[ "$branch" == "$MAIL_BRANCH" ]] || _die "clone $MAIL_REPO is on '${branch:-detached}', expected '$MAIL_BRANCH' — refusing"
  for (( try = 1; try <= FETCH_TRIES; try++ )); do
    if timeout 120 git -C "$MAIL_REPO" fetch --quiet --prune origin; then
      break
    fi
    if (( try == FETCH_TRIES )); then
      echo "harness-check: ERROR: fetch from origin failed $FETCH_TRIES times — nothing published" >&2
      return 1
    fi
    _log "fetch failed (try $try/$FETCH_TRIES); retrying in ${FETCH_DELAY}s"
    sleep "$FETCH_DELAY"
  done
  git -C "$MAIL_REPO" rev-parse -q --verify "refs/remotes/origin/$MAIL_BRANCH" >/dev/null \
    || _die "origin/$MAIL_BRANCH missing in $MAIL_REPO after fetch"
  git -C "$MAIL_REPO" reset --hard --quiet "origin/$MAIL_BRANCH" || _die "reset --hard failed in $MAIL_REPO"
  git -C "$MAIL_REPO" clean -fdq || _die "clean failed in $MAIL_REPO"
}

# The clone commits with a LOCAL identity only (deploy.sh sets it; this is the fallback).
ensure_identity() {
  local host="${MACHINE_NAME:-$(hostname -s)}" email
  if [[ -z "$(git -C "$MAIL_REPO" config --local user.name)" ]]; then
    git -C "$MAIL_REPO" config --local user.name "harness-check ($host)"
  fi
  if [[ -z "$(git -C "$MAIL_REPO" config --local user.email)" ]]; then
    email=$(git -C "$MAIL_REPO" config --global user.email)
    git -C "$MAIL_REPO" config --local user.email "${email:-harness-check@$(hostname -s).localdomain}"
  fi
}

# ── Debug / interactive: scan the live tree, print, write nothing ─────────────────
if [[ $DEBUG_MODE -eq 1 ]]; then
  scan_cards
  stale_count=${#STALE_CARDS[@]}
  echo "------------------------------------------"
  echo "Total checked cards stale: $stale_count"
  if [[ $stale_count -gt 0 ]]; then
    echo "Stale items list:"
    for item in "${STALE_CARDS[@]}"; do
      IFS="$FS" read -r c b v t e cmd r <<< "$item"
      echo "  - $b ($c) — verified: $v, stale since $e days ago (limit: $t)"
    done
  fi
  echo "Proposed mail output: $(_rebase_live_path "$MAIL_DIR_EXPANDED" "$MAIL_REPO" || echo "$MAIL_DIR_EXPANDED")/${MAIL_NAME_PREFIX}${CURRENT_WEEK}.md"
  echo "=========================================="
  exit 0
fi

# ── Mail mode (timer / default): publish once per ISO week, from the clone only ───
mail_name="${MAIL_NAME_PREFIX}${CURRENT_WEEK}.md"
mail_file="$MAIL_DIR_EXPANDED/$mail_name"
mail_rel="${mail_file#"$MAIL_REPO"/}"
host_label="${MACHINE_NAME:-$(hostname -s)}"

for (( attempt = 1; attempt <= MAIL_ATTEMPTS; attempt++ )); do
  sync_clone || exit 1

  if [[ -e "$MAIL_DIR_EXPANDED/$mail_name" || -e "$MAIL_ARCHIVE_DIR/$mail_name" ]]; then
    _log "already published: $mail_name exists on origin/$MAIL_BRANCH (inbox or archive) — nothing to do"
    exit 0
  fi

  scan_cards
  if [[ ${#STALE_CARDS[@]} -eq 0 ]]; then
    _log "no stale cards for $CURRENT_WEEK — nothing published"
    exit 0
  fi

  mkdir -p "$MAIL_DIR_EXPANDED"
  render_mail > "$mail_file" || _die "cannot write $mail_file"
  ensure_identity
  git -C "$MAIL_REPO" add -- "$mail_rel" || _die "git add failed for $mail_rel"
  git -C "$MAIL_REPO" commit --quiet -m "_mail: stale-settings-cards ${CURRENT_WEEK} (harness, ${host_label})" -- "$mail_rel" \
    || _die "git commit failed for $mail_rel"

  if timeout 120 git -C "$MAIL_REPO" push --quiet origin "HEAD:$MAIL_BRANCH"; then
    _log "published $mail_rel (${#STALE_CARDS[@]} stale) → origin/$MAIL_BRANCH at $(git -C "$MAIL_REPO" rev-parse --short HEAD)"
    exit 0
  fi
  _log "push rejected or failed (attempt $attempt/$MAIL_ATTEMPTS); re-syncing and retrying"
done

echo "harness-check: ERROR: could not publish $mail_rel after $MAIL_ATTEMPTS attempts" >&2
exit 1
