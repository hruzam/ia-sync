#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — nablarva/ control panel (aliases + comments ONLY)
# =============================================================================
# Location: ~/.config/zsh/nablarva/keyboard.zsh (table-authored; deploy.sh spreads)
# Sourced by: nablarva/base.zsh P1
# LAW (guide-for-builder.md §Architecture rules): aliases and comments only —
# every function body lives in an engine (nablarva.zsh), never here.
# First project-scoped keyboard-exp (founding 2026-08-02, majkee-directed).
# =============================================================================

# --- P1: harness surfaces (flag L9) ------------------------------------------
alias nab-flag='nab -f'        # locks + pending-gavel docket
alias nab-pulse='nab -p'       # the ONLY canonical doing-state
alias nab-dock='nab -d'        # uncanonical scratch — side quests, no blessing

# --- P2: devenv transport ----------------------------------------------------
alias nab-sync='nab -sync'     # stage harness app -> devenv (git-home)
alias nab-deploy='nab -dep'    # devenv -> app, guarded prompt; sync first!

# --- P3: orientation ---------------------------------------------------------
alias nab-st='nab -s'          # project status (path, git, newest pulse entry)
alias nab-help='nab -h'        # engine help panel

# --- P4: keys panel ----------------------------------------------------------
alias nab-keys='grep -E "^alias nab-" ~/.config/zsh/nablarva/keyboard.zsh | sed "s/alias //"'

# --- P5+ (reserved): stridularium / broker bindings — post-gavel -------------
