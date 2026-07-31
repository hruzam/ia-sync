#!/usr/bin/env zsh
# temple-project-map.zsh — temple project map (P0) — shared across machines
# folder layout is 1:1 on office and home; paths are identical on both
# implements: decision 0008 Stage 1 — the single P0 map; reused by temple-doorbell + future recalibration
# companion: reposoma/registry/index.md — logical project map; THIS file holds the physical disk paths
# rule: THIS FILE is the only place physical repo-root paths live (0004 L4 — no ~/paths in canon/beacons)
# rule: source this file; do NOT hard-code these paths elsewhere
#
# Sync guide — keep TEMPLE_PROJECT_MAP in step with registry/index.md (all projects):
#   mapped:  reposoma · subai.devenv · reposoma.devenv · freya · freya.devenv · piql.dev · vacuole · fantasyobchod · psdvsSys · applications-in-common
#   omitted: nabla-lab → subdir of reposoma; resolves via [reposoma], no separate entry needed

typeset -gA TEMPLE_PROJECT_MAP
TEMPLE_PROJECT_MAP=(
  [reposoma]="/home/hruzam/reposoma"
  [subai.devenv]="/home/hruzam/www/ovum/subai.devenv"
  [reposoma.devenv]="/home/hruzam/www/ovum/reposoma.devenv"
  [freya]="/home/hruzam/www/imago_cz/freya"
  [freya.devenv]="/home/hruzam/www/imago_cz/freya.devenv"
  [piql.dev]="/home/hruzam/www/piql/piql.dev"
  [vacuole]="/home/hruzam/vacuole"
  [fantasyobchod]="/home/hruzam/www/imago_cz/fantasyobchod"
  [psdvsSys]="/home/hruzam/www/psdvs/psdvsSys"
  [applications-in-common]="/home/hruzam/www/elements-factory/applications-in-common"
)

# temple-project-root <project-name>
# Resolves a logical project name to its repo-root on this host.
# Exits non-zero and prints to stderr if unknown.
temple-project-root() {
  local name="$1"
  local root="${TEMPLE_PROJECT_MAP[$name]}"
  if [[ -z "$root" ]]; then
    print -u2 "temple-project-map: unknown project '$name' on host ${MACHINE_NAME:-unknown}"
    return 1
  fi
  if [[ ! -d "$root" ]]; then
    print -u2 "temple-project-map: project '$name' maps to '$root' but directory not found on this host"
    return 2
  fi
  print -- "$root"
}
