# freya/ — zsh scope

Thin shell aggregation for the **freya** project's cross-machine operations.
Follows the `system/` partition pattern: `base.zsh` (signpost) → `keyboard.zsh`
(aliases only) → `engine.zsh` (function bodies).

**No logic lives here.** Every function is a thin wrapper that calls the
**canonical** scripts in the `freya.devenv` companion repo
(`$FREYA_DEVENV_DIR`, default `~/www/imago_cz/freya.devenv`):

| Bus | Wraps | Aliases |
|-----|-------|---------|
| **buffer** (git app-code, office↔home over Tailscale) | `scripts/freya-buffer.sh` | `fb`, `fb-status`, `fb-update`, `fb-push`, `fb-pull`, `fb-doctor`, `fb-meili`, `fb-meili-ack` |
| **devenv** (config/harness, office↔home) | `deploy.sh`, `sync.sh` | `freya-deploy`, `freya-sync`, `freya-ferry` |

`freya-help` prints the panel.

## Wiring
- Registered in `config.office.zsh` / `config.home.zsh` via:
  `[[ -f ~/.config/zsh/freya/base.zsh ]] && source ~/.config/zsh/freya/base.zsh`
- Deployed to both machines by `zsync` (ia-sync `deploy.sh` rsyncs `zsh/` → `~/.config/zsh/`).
- The two buses are deliberately distinct — see the `freya-buffer` skill for the full model.

## Design note
The buffer/deploy/sync logic is owned by the project (freya.devenv), version-controlled
there, and used by both agents (via the `/freya-buffer` skill) and the human (via these
aliases). This scope is pure ergonomics — a keyboard over the same one script set.
