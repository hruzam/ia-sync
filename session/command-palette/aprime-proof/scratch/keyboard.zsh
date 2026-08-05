#!/usr/bin/env zsh
# scratch/keyboard.zsh — A' mechanism proof fixture (isolated scratch scope)
# Rule: aliases and comments ONLY — no function bodies.
# Not a real config file; consumed only by aprime-proof/prove.sh.

# ── Alpha ──────────────────────────────────────────────────────────────────
alias av='_alpha_view'                 # show alpha status
alias ar='_alpha_run'                  # run alpha job · arg = job name
alias ax='_alpha_reset'

# ── Beta ───────────────────────────────────────────────────────────────────
alias bv='_beta_view'                  # show beta status
alias bp='_beta_ping'                  # ping beta peer · arg or $BETA_PEER
