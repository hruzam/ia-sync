#!/usr/bin/env zsh
# =============================================================================
# SYNC/GUIDES.ZSH — Guide-publish synchronizer
# One-way publish: project guides -> reposoma raw.guides mirror.
# Source of truth = project. Run `sync-guides` after editing a source guide.
# Do NOT hand-edit the reposoma copies.
# Aliases: sync/keyboard.zsh (control panel — aliases + comments only, WP4 retrofit)
# =============================================================================

sync-guides() {
    local REGISTRY="$HOME/.config/zsh/registries/config.sync.json"

    # --- dependency check ---
    if ! command -v jq &>/dev/null; then
        echo "[sync] ERROR: jq is required but not found in PATH" >&2
        return 1
    fi

    if [[ ! -f "$REGISTRY" ]]; then
        echo "[sync] ERROR: registry not found: $REGISTRY" >&2
        return 1
    fi

    local REPOSOMA_ROOT
    REPOSOMA_ROOT="$(jq -r '.reposoma_root' "$REGISTRY")"

    local synced=0
    local skipped=0
    local failed=0
    local project_count i j
    local project_name guides_dir item_count
    local src_file dst_rel SRC DST

    project_count="$(jq '.projects | length' "$REGISTRY")"

    for (( i=0; i<project_count; i++ )); do
        project_name="$(jq -r ".projects[$i].name" "$REGISTRY")"
        guides_dir="$(jq -r ".projects[$i].guides_dir" "$REGISTRY")"

        item_count="$(jq ".projects[$i].publish | length" "$REGISTRY")"

        for (( j=0; j<item_count; j++ )); do
            src_file="$(jq -r ".projects[$i].publish[$j].src" "$REGISTRY")"
            dst_rel="$(jq -r ".projects[$i].publish[$j].dst" "$REGISTRY")"

            SRC="${guides_dir}/${src_file}"
            DST="${REPOSOMA_ROOT}/${dst_rel}"

            if [[ ! -f "$SRC" ]]; then
                echo "[sync] WARN: source missing: $SRC (skipped)"
                (( skipped++ ))
                (( failed++ ))
                continue
            fi

            mkdir -p "$(dirname "$DST")"

            # Write banner + blank line + verbatim source content
            {
                echo "<!-- PUBLISHED MIRROR · do not edit here · source: ${project_name}/guides/${src_file} · regenerate with: sync-guides -->"
                echo ""
                cat "$SRC"
            } > "$DST"

            echo "[sync] ${project_name}: ${src_file} -> ${DST} (OK)"
            (( synced++ ))
        done
    done

    echo "[sync] done: synced ${synced} · skipped ${skipped}"

    [[ $failed -eq 0 ]]
}

# =============================================================================
# HELP
# =============================================================================
_sync_help() {
    cat << 'EOF'
sync — guide-publish synchronizer (engine: sync/guides.zsh; keys: sync/keyboard.zsh)

  sync-guides   one-way publish: project guides -> reposoma raw.guides mirror
                (registry: registries/config.sync.json; source of truth = project)
EOF
}
