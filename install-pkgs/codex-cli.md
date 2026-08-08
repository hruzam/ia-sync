# codex-cli — install task

```
developed-on: office (hruzam-120922)
install-on:   home (hruzam)
source:       official @openai/codex npm package
built:        2026-08-08
version:      1.0
hosts:        home
automation:   auto
codex-version: 0.146.0
```

---

## What this installs

Installs the official Codex CLI into home's user-owned npm prefix, pinned to the
same release used on office: `0.146.0`. The CLI is the native Codex surface for
Linux; no system package or `sudo` is involved.

This task does **not** copy authentication, history, configuration, hooks, trust,
or other machine-local `~/.codex` state. Portable @Cartan instructions, agents,
and skills travel through `codex/` and `deploy.sh --codex-only`.

When office advances to a newer Codex version, update `codex-version` below,
update the install block's `wanted` value, and bump this task's `version`.

## Verify

```bash
codex --version
codex login status
```

The first command must report `codex-cli 0.146.0`. Authentication is deliberately
per host; run `codex login` on home if the second command reports signed out.

<!-- install:check -->
```bash
command -v node >/dev/null 2>&1 || { echo "node is not installed"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is not installed"; exit 1; }
prefix="$(npm config get prefix)"
case "$prefix/" in
  "$HOME/"*) ;;
  *) echo "npm prefix is not user-owned: $prefix"; exit 1 ;;
esac
[ -d "$prefix" ] && [ -w "$prefix" ] || { echo "npm prefix is not writable: $prefix"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
wanted="0.146.0"
prefix="$(npm config get prefix)"
bin="$prefix/bin/codex"
current=""
if command -v codex >/dev/null 2>&1; then
  current="$(codex --version 2>/dev/null | awk '{print $2}')"
fi

if [ "$current" = "$wanted" ]; then
  echo "codex-cli $wanted already available"
else
  npm install --global "@openai/codex@$wanted" || exit 1
fi

[ -x "$bin" ] || { echo "Codex executable missing after install: $bin"; exit 1; }
installed="$("$bin" --version 2>/dev/null | awk '{print $2}')"
[ "$installed" = "$wanted" ] || {
  echo "Codex version mismatch: wanted $wanted, got ${installed:-unknown}"
  exit 1
}
echo "installed $bin (codex-cli $installed)"
```
<!-- /install:run -->
