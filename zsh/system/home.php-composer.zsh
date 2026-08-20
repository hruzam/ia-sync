#!/usr/bin/env zsh
# home.php-composer.zsh — home PHP/Composer engine
# Sourced by: system/base.zsh on MACHINE_NAME=home
# Aliases live in: system/keyboard.zsh
#
# Home has no native PHP 7.4 CLI. PHP 7.4 and composer74 use the local
# php74-composer image; PHP 8+ is native, while composer8 remains containerized.

[[ "$MACHINE_NAME" != "home" ]] && return 0

_home_check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        echo "[php] Docker is not installed"
        echo "      sudo pacman -S docker"
        return 1
    fi

    if ! systemctl is-active --quiet docker 2>/dev/null; then
        echo "[php] Docker service is not running"
        echo "      sudo systemctl start docker"
        return 1
    fi

    if ! groups | grep -qw docker; then
        echo "[php] Current user is not in the docker group"
        echo "      sudo usermod -aG docker $USER && logout/login"
        return 1
    fi
}

_home_ensure_php74_image() {
    _home_check_docker || return 1

    if ! docker image inspect php74-composer >/dev/null 2>&1; then
        echo "[php] Building php74-composer image (one time)"
        docker build -t php74-composer "$HOME/.docker/php74-composer/" || return 1
    fi
}

_home_docker_tty_args() {
    reply=(-i)
    [[ -t 0 && -t 1 ]] && reply+=(-t)
}

_php74() {
    _home_ensure_php74_image || return 1
    local -a tty_args
    _home_docker_tty_args
    tty_args=("${reply[@]}")
    (( $# == 0 )) && set -- -v

    docker run --rm "${tty_args[@]}" \
      --user "$(id -u):$(id -g)" \
      --volume "$(pwd):/app" \
      --entrypoint php \
      php74-composer \
      "$@"
}

_php8() {
    if (( $# > 0 )); then
        /usr/bin/php "$@"
        return $?
    fi

    if ! systemctl is-active --quiet php-fpm 2>/dev/null; then
        sudo systemctl start php-fpm || return 1
    fi

    _phpst
}

_phpst() {
    local docker_status="inactive"
    local php74_image="missing"
    local php8_version="missing"
    local php8_fpm="inactive"
    local php8_socket="missing"

    systemctl is-active --quiet docker 2>/dev/null && docker_status="active"
    if [[ "$docker_status" == "active" ]] && docker image inspect php74-composer >/dev/null 2>&1; then
        php74_image="ready"
    fi
    [[ -x /usr/bin/php ]] && php8_version="$(/usr/bin/php -r 'echo PHP_VERSION;' 2>/dev/null)"
    systemctl is-active --quiet php-fpm 2>/dev/null && php8_fpm="active"
    [[ -S /run/php-fpm/php-fpm.sock ]] && php8_socket="ready"

    printf "\n  %-20s  %s\n" "HOME RUNTIME" "STATUS"
    printf "  %-20s  %s\n" "--------------------" "----------------"
    printf "  %-20s  %s\n" "Docker" "$docker_status"
    printf "  %-20s  %s\n" "PHP 7.4 image" "$php74_image"
    printf "  %-20s  %s\n" "PHP 8+ native" "$php8_version"
    printf "  %-20s  %s\n" "PHP 8 FPM" "$php8_fpm · socket $php8_socket"
    printf "\n  php74/composer74 : php74-composer image\n"
    printf "  php8              : /usr/bin/php · no args starts php-fpm\n"
    printf "  composer8         : composer:latest image\n\n"
}

_composer74() {
    _home_ensure_php74_image || return 1
    local -a tty_args
    _home_docker_tty_args
    tty_args=("${reply[@]}")

    mkdir -p "$HOME/.composer/cache"
    docker run --rm "${tty_args[@]}" \
      --user "$(id -u):$(id -g)" \
      --volume "$(pwd):/app" \
      --volume "$HOME/.composer:/composer" \
      --env COMPOSER_HOME=/composer \
      --env COMPOSER_CACHE_DIR=/composer/cache \
      php74-composer \
      --ignore-platform-req=ext-posix \
      --ignore-platform-req=ext-pcntl \
      "$@"
}

_composer8() {
    _home_check_docker || return 1
    local -a tty_args
    _home_docker_tty_args
    tty_args=("${reply[@]}")

    mkdir -p "$HOME/.composer/cache"
    docker run --rm "${tty_args[@]}" \
      --user "$(id -u):$(id -g)" \
      --volume "$(pwd):/app" \
      --volume "$HOME/.composer:/tmp/composer" \
      --env COMPOSER_HOME=/tmp/composer \
      composer:latest \
      --ignore-platform-req=ext-posix \
      --ignore-platform-req=ext-pcntl \
      "$@"
}

_test_mariadb_mcp() {
    echo "[tmcp] MariaDB MCP probe is office-only"
    return 1
}
