#!/usr/bin/env zsh
# =============================================================================
# PHP-SWITCH — Office PHP version management (@office only)
# =============================================================================
# Location: ~/.config/zsh/system/office.php-switch.zsh
# Sourced by: config.zsh (after PHP vars are defined)
#
# ARCHITECTURE: both FPMs run simultaneously. Valet routes per-site.
#
#   php74-fpm  →  /etc/php74/php-fpm.d/valet.conf  →  ~/.valet/valet74.sock
#   php-fpm    →  /etc/php/php-fpm.d/valet.conf    →  ~/.valet/valet.sock
#
#   PHP 7.4 sites: ~/.valet/Nginx/<site> hardcodes fastcgi_pass → valet74.sock
#                  Sites: fantasyobchod.l, imagosk.l
#   PHP 8.x sites: default Valet routing → valet.sock
#                  Sites: freya.l, psdvs.l, and all future Laravel projects
#
# NEVER call `valet use phpX`:
#   - Broken on Arch (expects php7.4-fpm, package is php74-fpm)
#   - Calls systemctl disable on the other FPM → breaks boot state
#   - Requires sudo password
#   Use the `php74` / `php8` keys from system/keyboard.zsh instead.
#
# REQUIRES:
#   - /etc/sudoers.d/valet-php (passwordless systemctl for FPM + nginx)
#   - Both services enabled on boot: sudo systemctl enable php74-fpm php-fpm
# =============================================================================

# Office-only: home uses system/home.php-composer.zsh. Inert elsewhere.
[[ "$MACHINE_NAME" != "office" ]] && return 0

# _php74 — start PHP 7.4 FPM (valet74.sock) + show status; key: php74
_php74() {
    # Start PHP 7.4 FPM → creates ~/.valet/valet74.sock
    # Sites: fantasyobchod.l, imagosk.l
    sudo systemctl start "$PHP74_FPM_SERVICE" 2>/dev/null
    _phpst
}

# _php8 — start PHP 8.x FPM (valet.sock) + show status; key: php8
_php8() {
    # Start PHP 8.x FPM → creates ~/.valet/valet.sock
    # Sites: freya.l and all other Valet-served projects
    sudo systemctl start "$PHP8_FPM_SERVICE" 2>/dev/null
    _phpst
}

_phpst() {
    local s74=$(systemctl is-active "$PHP74_FPM_SERVICE" 2>/dev/null)
    local s8=$(systemctl is-active  "$PHP8_FPM_SERVICE" 2>/dev/null)
    local sock74=$([[ -S ~/.valet/valet74.sock ]] && echo "socket ok" || echo "no socket ⚠")
    local sock8=$( [[ -S ~/.valet/valet.sock   ]] && echo "socket ok" || echo "no socket ⚠")
    printf "\n  %-26s  %-12s  %s\n" "SERVICE" "STATUS" "SOCKET"
    printf "  %-26s  %-12s  %s\n"   "--------------------------" "------------" "----------"
    printf "  %-26s  %-12s  %s\n"   "php74-fpm → valet74.sock"  "$s74"         "$sock74"
    printf "  %-26s  %-12s  %s\n"   "php-fpm   → valet.sock"    "$s8"          "$sock8"
    printf "\n  PHP 7.4 sites : fantasyobchod.l  imagosk.l\n"
    printf "  PHP 8.x sites : freya.l  psdvs.l  ltp.l  (all future Laravel; psdvs.l is Nette per ADR-001 2026-07-27)\n"
    printf "\n  CLI php   : $(${PHP8_BIN:-/usr/bin/php}  -r 'echo PHP_VERSION;' 2>/dev/null)\n"
    printf "  CLI php74 : $(${PHP74_BIN:-/usr/bin/php74} -r 'echo PHP_VERSION;' 2>/dev/null)\n\n"
}

_composer74() {
    "${PHP74_BIN:-/usr/bin/php74}" "${COMPOSER_BIN:-/usr/bin/composer}" "$@"
}

_composer8() {
    "${COMPOSER_BIN:-/usr/bin/composer}" "$@"
}

# --- Adding a new PHP 8.x project ---
# 1. cd ~/www/imago_cz/<project>   (or wherever the project lives)
# 2. valet link <sitename>
# Done — no nginx config needed, default Valet routing handles it.

# --- Adding a new PHP 7.4 project (legacy only) ---
# 1. cd <project> && valet link <sitename>
# 2. cp ~/.valet/Nginx/fantasyobchod ~/.valet/Nginx/<sitename>
# 3. Edit server_name in the new file
# 4. sudo systemctl reload nginx

#############
# test maria db connection
#############

# _test_mariadb_mcp — probe the mariadb-mcp server over stdio; key: tmcp
_test_mariadb_mcp() {

    (
        echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.0.1"}}}'
        echo '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'
        echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
        sleep 1
    ) | php -d extension=iconv /home/hruzam/www/mariadb-mcp/server.php | head -20

}
