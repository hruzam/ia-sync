#!/bin/zsh

# Core checking script for settings card freshness
# Location: ~/.config/zsh/ai/harness-check.zsh

# Load config path
CONFIG_FILE="${HOME}/.config/zsh/registries/ai.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Registry config not found at $CONFIG_FILE" >&2
  exit 1
fi

# Parsing JSON values dynamically
parse_json_value() {
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
expand_path() {
  local p=$1
  p="${p/#\~\//$HOME/}"
  echo "$p"
}

# Extract values from ai.json
pattern_raw=$(parse_json_value "native-primitives-update-pattern" "$CONFIG_FILE")
mail_dir_raw=$(parse_json_value "mail-inbox-dir" "$CONFIG_FILE")

if [[ -z "$pattern_raw" ]]; then
  echo "Error: Key 'native-primitives-update-pattern' not defined in $CONFIG_FILE" >&2
  exit 1
fi

# Expand paths
PATTERN_EXPANDED=$(expand_path "$pattern_raw")
MAIL_DIR_EXPANDED=$(expand_path "${mail_dir_raw:-~/reposoma/_mail/toAll/inbox}")
GUIDES_DIR="${HOME}/reposoma/raw.guides"

# Check for --debug or harness-stale command name
DEBUG_MODE=0
if [[ "$1" == "--debug" || "$0" == *harness-stale* ]]; then
  DEBUG_MODE=1
fi

# Header output for debug mode
if [[ $DEBUG_MODE -eq 1 ]]; then
  echo "=========================================="
  echo " HARNESS-CHECK: CARD FRESHNESS REPORT     "
  echo "=========================================="
  echo "Pattern Checked:  $PATTERN_EXPANDED"
  echo "Guides Dir:       $GUIDES_DIR"
  echo "Mail Destination: $MAIL_DIR_EXPANDED"
  echo "------------------------------------------"
fi

CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_EPOCH=$(date +%s)

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
  done < <(awk '
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
      gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", card)
      gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", brand)
      gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", verified)
      gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", half_life_days)
      gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", verify_cmd)
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
    # "card|brand|verified|threshold|elapsed|verify_cmd|rechecks"
    STALE_CARDS+=("${card}|${brand}|${verified}|${threshold}|${elapsed_days}|${verify_cmd}|${rechecks}")
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
    done < <(awk '
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
        gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", card)
        gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", brand)
        gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", verified)
        gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", half_life_days)
        gsub(/^[ \t'"'"'"]+|[ \t'"'"'"]+$/, "", verify_cmd)
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

    # Derive card/brand from filename if not in frontmatter
    [[ -z "$card" ]] && card="$(basename "$file" .md)"
    [[ -z "$brand" ]] && brand="guide:$card"

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
      STALE_CARDS+=("${card}|${brand}|${verified}|${threshold}|${elapsed_days}|${verify_cmd}|${rechecks}")
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

# Output or mail release handling
stale_count=${#STALE_CARDS[@]}

if [[ $DEBUG_MODE -eq 1 ]]; then
  echo "------------------------------------------"
  echo "Total checked cards stale: $stale_count"
  if [[ $stale_count -gt 0 ]]; then
    echo "Stale items list:"
    for item in "${STALE_CARDS[@]}"; do
      IFS='|' read -r c b v t e cmd r <<< "$item"
      echo "  - $b ($c) — verified: $v, stale since $e days ago (limit: $t)"
    done
  fi
  echo "Proposed mail output: $MAIL_DIR_EXPANDED/zsh.stale-settings-cards-${CURRENT_DATE}.md"
  echo "=========================================="
else
  # Mail release mode (Background / Cron / Default)
  if [[ $stale_count -gt 0 ]]; then
    mkdir -p "$MAIL_DIR_EXPANDED"
    mail_file="$MAIL_DIR_EXPANDED/zsh.stale-settings-cards-${CURRENT_DATE}.md"
    
    {
      echo "---"
      echo "title: Stale Settings Cards Alert"
      echo "date: ${CURRENT_DATE}"
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
        IFS='|' read -r c b v t e cmd r <<< "$item"
        
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
          cmd_formatted="\`$cmd\`"
        fi
        
        echo "| **$b**<br>($c) | $v | $t | **$e** | $cmd_formatted<br>$links_formatted |"
      done
      
      echo ""
      echo "---"
      echo "*This is an automated notification generated by the native zsh card-freshness checker on $(date).* To run manually and check details directly in terminal, execute: \`harness-stale\`."
    } > "$mail_file"
    
    echo "Released stale cards alert: $mail_file"
  fi
fi
