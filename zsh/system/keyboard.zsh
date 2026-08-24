#!/usr/bin/env zsh
# system/keyboard.zsh — system scope control panel
# Rule: aliases and comments ONLY — no function bodies.
# Bodies live in scope engines (tailscale.zsh, shell.zsh, host PHP engines).
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
alias ts-pull='_ts_pull'              # pull same-path file from peer (mirror copy)
alias ts-push='_ts_push'              # push same-path file to peer (mirror copy)
alias ts-beam='_ts_beam'              # beam file(s) to peer transporter pad
alias ts-help='_ts_help'              # command panel for this scope

# ── Database (cross-host tunnel) ───────────────────────────────────────────────
# Bodies in: system/tailscale.zsh · guide: reposoma/raw.guides/reach/mariadb-cross-host.md
alias db-reach='_db_reach'             # tunnel peer's MariaDB → 127.0.0.1:3307
alias db-reach-down='_db_reach_down'   # close the db-reach tunnel

# ── Browser egress (cross-host SOCKS tunnel) ──────────────────────────────────
# Bodies in: system/tailscale.zsh
alias web-reach='_web_reach'           # browser traffic exits through peer at SOCKS 127.0.0.1:1080
alias web-reach-firefox='_web_reach_firefox' # open isolated Firefox through peer egress
alias web-reach-down='_web_reach_down' # close the web-reach SOCKS tunnel


# ── General shell utilities ────────────────────────────────────────────────────
# Bodies in: system/shell.zsh
alias src='source ~/.zshrc'            # reload shell config
alias ord='ls -lthr'                   # list newest last
alias hasz='openssl rand -hex 12 | cut -c 1-21'  # random 21-char hex token
alias cod="php -r 'echo uniqid(). PHP_EOL;'"     # PHP uniqid
alias mygrep='grep -Hrn'               # recursive grep with line numbers
alias msrc='_msrc'                     # search www tree · arg = pattern

# ── PHP + Composer (same keys; host-specific engines) ─────────────────────────
# Bodies in: system/home.php-composer.zsh or system/office.php-switch.zsh
alias php74='_php74'                   # PHP 7.4 · home Docker / office FPM
alias php8='_php8'                     # PHP 8+ · home native / office FPM
alias phpst='_phpst'                   # host runtime status
alias composer74='_composer74'         # Composer on PHP 7.4
alias composer8='_composer8'           # Composer on PHP 8+
alias tmcp='_test_mariadb_mcp'          # office MariaDB MCP stdio probe
