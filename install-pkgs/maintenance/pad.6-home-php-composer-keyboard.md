# pad.6-home-php-composer-keyboard — home verification protocol

> host: `hruzam` (`MACHINE_NAME=home`) · owner: home seat (ad-hoc)
> scope: `system/keyboard.zsh` keys backed by `system/home.php-composer.zsh`

This pad verifies the shared key names without confusing the host mechanisms. On home,
PHP 7.4 and both versioned Composer commands use Docker; PHP 8+ itself is native.

## 1. Wiring (no containers started)

```zsh
zsh -n ~/.config/zsh/system/{base,keyboard,home.php-composer}.zsh
zsh -lic 'type php74 php8 phpst composer74 composer8'
```

Expected: all five names are aliases to underscored bodies; no alias points at
`$PHP74_BIN`, `$PHP8_BIN`, or `$COMPOSER_BIN` on home.

## 2. Runtime status

```zsh
phpst
php8 -r 'echo PHP_VERSION, PHP_EOL;'
php74 -r 'echo PHP_VERSION, PHP_EOL;'
```

Expected: Docker active; `php74-composer` ready; native PHP reports 8.x; container PHP
reports 7.4.x. If Docker is stopped, run `sudo systemctl start docker` and repeat.

## 3. Composer probes (read-only)

Run from a disposable or clean project directory; these commands must not alter files.

```zsh
composer74 --version
composer8 --version
```

Expected: both run in containers as the current user, so no root-owned project files are
created. `composer74` reports Composer 2.2.24; `composer8` reports the current image's
Composer version.

## 4. Compose-first host receive key

```zsh
alias zsync
```

Expected: `git pull --rebase origin main && bash deploy.sh && git status`. Any `sync.sh`
in this alias is a hard failure; ia-sync's harvest leg is retired.
