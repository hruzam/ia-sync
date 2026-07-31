# ia-sync — AI config sync guide

Backup and restore for `~/.claude`, `~/.gemini`, `~/.config/zsh/`.
Private repo. Two scripts, no magic.

---

## Repo layout

```
ia-sync/
├── claude/                  # ~/.claude keep-set (skills, agents, commands, settings)
├── gemini/                  # ~/.gemini keep-set (agents, config, antigravity-cli settings)
├── zsh/                     # ~/.config/zsh keep-set
│   └── config.<host>.zsh    # machine-specific config (one file per host)
├── sync.sh                  # backup: source → repo
├── deploy.sh                # restore: repo → destination
└── SYNC_GUIDE.md            # this file
```

---

## Backup (sync to repo)

```bash
cd ~/ia-sync
bash sync.sh
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push
```

`sync.sh` reads `$MACHINE_NAME` (falls back to `hostname -s`) and saves
`~/.config/zsh/config.zsh` as `zsh/config.<machine>.zsh`.
A built-in secret scan runs before exit — if it hits, the script exits 1 and you must review before pushing.

**What is synced:**

| Source | What |
|--------|------|
| `~/.claude/` | `skills/`, `agents/`, `commands/`, `settings.json`, `settings.local.json`, `houston.goal`, `recorder.index.json` |
| `~/.gemini/` | `agents/`, `config/`, `antigravity-cli/{settings,keybindings}.json`, `state.json`, `projects.json` |
| `~/.config/zsh/` | everything except `.env/`, `*.bak`, `*.log` — `config.zsh` saved as `config.<host>.zsh` |

**What is excluded (never committed):**

- `.env/` — secrets, API keys
- `.credentials.json` — Claude auth token
- `projects/`, `file-history/`, `paste-cache/`, `tmp/` — session/runtime data
- `*.jsonl`, `*.db`, `*.log` — conversation logs and runtime artefacts
- binaries, caches, updater state

---

## Restore (deploy to new machine)

```bash
git clone git@github.com:hruzam/ia-sync.git ~/ia-sync
cd ~/ia-sync
bash deploy.sh
```

`deploy.sh` detects `$MACHINE_NAME` and maps `zsh/config.<machine>.zsh` → `~/.config/zsh/config.zsh`.
If no matching host file exists, it lists available host configs and skips `config.zsh`.

**deploy.sh is non-destructive** — it copies/overwrites but never deletes existing local files.

---

## Multi-host config.zsh

Each machine has its own `~/.config/zsh/config.zsh` with host-specific paths.
The repo stores them by name:

```
zsh/config.home.zsh      # home workstation
zsh/config.office.zsh    # office workstation
```

When you sync from a new host for the first time, a new `config.<host>.zsh` is created automatically.

---

## Adding a new machine

```bash
git clone git@github.com:hruzam/ia-sync.git ~/ia-sync
# ensure MACHINE_NAME is set in your shell env
bash ~/ia-sync/deploy.sh      # pull existing config down
# ... work, tweak config.zsh for this host ...
bash ~/ia-sync/sync.sh        # push this host's config into the repo
git add -A && git commit -m "sync: new host $(hostname -s)" && git push
```
