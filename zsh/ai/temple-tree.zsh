#!/usr/bin/env zsh
# temple-tree.zsh — tree-snapshot engine (temple utility)
# Sourced by: ~/.config/zsh/ai/base.zsh (PARTITION 5)
# Depends on: temple-project-map.zsh — must be sourced first (base.zsh handles order)
# Engine:     ~/.config/zsh/ai/tree-converter.sh (Node.js; no npm deps)
# Configs:    ~/.config/zsh/registries/tcr/tcr.<project>.json
#             fallback: ~/.config/zsh/registries/tcr/tcr.default.json
#
# Agents: zsh -c "source ~/.config/zsh/ai/base.zsh && tree-snapshot <project>"

_TREE_SCRIPT="${HOME}/.config/zsh/ai/tree-converter.sh"
_TREE_REGISTRY="${HOME}/.config/zsh/registries/tcr"

tree-snapshot() {
  local project="${1:-}"
  if [[ -z "$project" ]]; then
    echo "Usage: tree-snapshot <project-name>"
    echo "Known: ${(k)TEMPLE_PROJECT_MAP}"
    return 1
  fi

  local root
  root=$(temple-project-root "$project") || return 1

  local config="${_TREE_REGISTRY}/tcr.${project}.json"
  local default_config="${_TREE_REGISTRY}/tcr.default.json"

  if [[ -f "$config" ]]; then
    (cd "$root" && bash "$_TREE_SCRIPT" -c "$config")
  elif [[ -f "$default_config" ]]; then
    (cd "$root" && bash "$_TREE_SCRIPT" -c "$default_config")
  else
    (cd "$root" && bash "$_TREE_SCRIPT")
  fi
}
