#!/usr/bin/env zsh
# system/keyboard.zsh — system scope control panel
# Rule: aliases and comments ONLY — no function bodies.
# Bodies live in scope engines (tailscale.zsh, shell.zsh).
# Law: ~/.config/zsh/guides/guide-for-builder.md §Architecture rules

# ── Tailscale ──────────────────────────────────────────────────────────────────
# Bodies in: system/tailscale.zsh
alias tss='tailscale status'           # raw status table
alias tsip='tailscale ip -4'           # my tailscale IP
alias ts-ls='_ts_ls'                   # formatted peer list (online / offline)
alias ts-header='_ts_header'          # compact startup line (called on shell open)
alias tsping='_ts_ping'                # ping peer  · arg or $TAILSCALE_PEER
alias tsp='_ts_ssh'                    # ssh to peer (fast, no header)
alias tso='_ts_session'               # ssh with pre-connect status line
alias ts-dash='_ts_dash'              # start HTTP status dashboard
alias ts-dash-stop='_ts_dash_stop'   # stop dashboard
alias ts-web='_ts_web'                 # open login.tailscale.com/admin/machines
alias ts-help='_ts_help'              # command panel for this scope


# ── General shell utilities ────────────────────────────────────────────────────
# Bodies in: system/shell.zsh
alias src='source ~/.zshrc'            # reload shell config
alias ord='ls -lthr'                   # list newest last
alias hasz='openssl rand -hex 12 | cut -c 1-21'  # random 21-char hex token
alias cod="php -r 'echo uniqid(). PHP_EOL;'"     # PHP uniqid
alias mygrep='grep -Hrn'               # recursive grep with line numbers
alias msrc='_msrc'                     # search www tree · arg = pattern
