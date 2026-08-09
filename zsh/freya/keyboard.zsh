#!/usr/bin/env zsh
# freya/keyboard.zsh — freya scope control panel
# Rule: aliases and comments ONLY — no function bodies.
# Bodies live in freya/engine.zsh, which wraps the canonical scripts in freya.devenv.

# ── Buffer bus (git app-code office↔home over Tailscale; vendor develop = read) ──
# Bodies: freya/engine.zsh → freya.devenv/scripts/freya-buffer.sh
alias fb='_freya_buffer'                             # bare → status (script default)
alias fb-status='_freya_buffer status'               # ahead/behind vs develop + transports
alias fb-update='_freya_buffer update'               # fetch vendor develop + merge (journal-safe)
alias fb-push='_freya_buffer push'                   # mirror branch to reachable transports
alias fb-pull='_freya_buffer pull'                   # receive other machine's work (ff-only)
alias fb-doctor='_freya_buffer doctor'               # remotes + reachability
alias fb-meili='_freya_buffer meili-watch'           # tripwire: meili app-code churn on develop
alias fb-meili-ack='_freya_buffer meili-watch ack'   # move the tripwire baseline

# ── Devenv bus (config/harness office↔home; NOT the git buffer) ─────────────────
# Bodies: freya/engine.zsh → freya.devenv/{deploy,sync}.sh
alias freya-deploy='_freya_deploy'                   # stage-IN : devenv → freya working dir
alias freya-sync='_freya_sync'                       # stage-OUT: freya .dev/ → devenv
alias freya-ferry='_freya_ferry'                     # office→home cascade (agent) — prints how

# ── Help ──────────────────────────────────────────────────────────────────────────
alias freya-help='_freya_help'
