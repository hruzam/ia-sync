# ai/ — AI scope namespace (machine surface)

`ai/` = SCOPE, not "dedicated-to" (operator clarification 2026-07-11): the AI-interactive
machine surface generally — Gemini seats, Claude RC, temple transport, devenv transport.
Pointer-first doc. Full live map: `~/.config/zsh/AGENTS.md`.
Usage: `~/.config/zsh/guides/guide-for-user.md` · keyboard map: `guides/keyboard.md`.

---

## File map

| File | Role | Used by | Entry |
|---|---|---|---|
| `base.zsh` | Signpost (0009 L2) — wires the whole scope in partition order | `config.zsh`, git post-commit hook | sourced |
| `keyboard.zsh` | Control panel: **aliases only — no bodies** | Human shell | `base.zsh` P1 |
| `gemini-processor.sh` | Gemini scope engine (dual-sourced): subprocess core (`_gai_*`) + interactive surface (agy wrappers, hygiene, `gemini-agents-help`) | per-agent launchers + `keyboard.zsh` aliases | launchers (bash) + `base.zsh` P8 (zsh) |
| `claude.zsh` | Claude Code RC engine + help: `_rc_stop`, `_temple_help`, `_ai_help` | `keyboard.zsh` aliases | `base.zsh` P7 |
| `experimental.zsh` | Experimental-runner dispatcher: `_exp_list` / `_exp_run`; resolves runners lazily | `exp-list`, `exp-run` aliases | `base.zsh` P9 |
| `experimental/` | Portable experimental runners; [its contract](experimental/README.md) defines each `<id>/runner.zsh` | `exp-run <id>` | executed on demand |
| `devenv.zsh` | Project devenv transport engine: `_devenv_*`, `_fr_*`, `_bo_*`, `_devenv_help` (pull --rebase discipline built in) | `keyboard.zsh` P11 aliases | `base.zsh` P6 |
| `devenv-sync-core.sh` | Shared function library for devenv sync wrappers (`_devenv_resolve_app_dir`, `_devenv_sync_deny_init/cleanup`, `_devenv_secret_scan`, `_devenv_print_footer`). Sourced by each project's `sync.sh`; not executed directly. | `*.devenv/sync.sh` | sourced |
| `keys.zsh` | Global claviature engine: `_keys` → derived keys panel (UNSORTED = drift detector) | `keys` alias (keyboard P12) | `base.zsh` P9 |
| `rc.sh` | Claude Code Remote Control launcher (tmux on-demand, Approach B) | `rc-*` aliases | executed |
| `bluebottle.sh` | Bluebottle synthesizer — REST+CLI dual-path, headless | `gemini-cross-check` agent, `g-bluebottle` | executed |
| `vega.sh` | Vega architect/advisor — interactive + headless | `g-vega` | executed |
| `orby.sh` | Orby researcher — interactive + headless | `g-orby` | executed |
| `astrobley.sh` | Astrobley implementer — interactive + headless + `--patch` multi-turn coder **(RETIRED 2026-07-31 — vendor-shifted to Codex; persona quarantined 2026-09-01)** | `g-astro` | executed |
| `personas/astrobley-patch.md` | RETIRED with astrobley.sh — quarantined 2026-09-01 | `astrobley.sh --patch` | read by script |
| `harness-check.zsh` | Card freshness checker; weekly systemd + `harness-stale` | systemd `harness.service` | executed |
| `~/.wires/iterations.jsonl` | Machine-local living wires (1D flow files: append → cron-prune) — see `~/.wires/README.md` | `claude.zsh` (_ai_launch), medusa (crash check) | appended/read |
| `temple-project-map.zsh` | P0: host-scoped project map (name → repo-root) | temple family | `base.zsh` P3 |
| `temple-mail.zsh` | A: mail primitive (`temple-mail`) | temple family | `base.zsh` P3 |
| `temple-doorbell.zsh` | B: canon-doorbell (`temple-doorbell-run`) | temple family | `base.zsh` P3 |
| `temple-mail-inbox.zsh` | C: read-side inbox helper (`temple-mail-inbox`) | temple family | `base.zsh` P3 |
| `temple-mail-switch.zsh` | D: interactive mail-destination picker (`temple-mail-switch`) | temple family | `base.zsh` P3 |
| `temple-mail-manage.zsh` | E: mailbox read-state manager (TUI + `--list/--archive/--restore`) | operator + agents | executed (keyboard alias) |
| `cs-palette.zsh` / `cs-palette.py` | F: cold-start vault explorer (D1/D2/D3 curses TUI) — resolves vault via `temple-project-root reposoma`; explorer only, never mutates | operator + agents | executed (keyboard alias) |
| `temple-cs-manage.zsh` / `cs-manage-palette.py` | G: cold-start vault mover — `card/`↔`archive/`↔`routines/`, both directions (TUI + `--list/--to-card/--to-archive/--to-routines`) | operator + agents | executed (keyboard alias) |
| `cs_vault.py` | Shared read-only helpers (file discovery, frontmatter parsing) for cs-palette.py + cs-manage-palette.py — never writes | cs-palette.py, cs-manage-palette.py | imported |
| `temple-project-surface.zsh` | Project-map interactive surface: `_project_paths`, `_project_git_status`, `_project_commit_all`, `_project_pick_zle` (ZLE), `_project_help` | `keyboard.zsh` P15 aliases + bindkey | `base.zsh` P10 |
| `zenith-zsh.sh` | Zenith-ZSH launcher — ensures `blessings/` exists, routes interactive vs headless; calls `claude --agent zenith-zsh` | `zenith-zsh` alias (keyboard P16) | **executed** (not sourced) |
| `temple-tree.zsh` | tree-snapshot engine (`tree-snapshot <project>`) | temple utilities | `base.zsh` P5 |
| `tree-converter.sh` | Node.js tree formatter (zero npm deps) | `temple-tree.zsh`; direct `-c <config>` | executed |
| `temple-doorbell.post-commit.hook` | Hook template — install into `.git/hooks/post-commit` | git | — |
| `doorbell-smoke.zsh` | Real-trigger smoke probe (0009 L5 gate) | verification | executed |
| `temple-transport-selftest.zsh` | Sandboxed end-to-end selftest | verification | executed |
| `adr-guard.zsh` (+ `.fixtures/`, `.pre-commit.hook`) | Canon-integrity gate for temple/decisions commits | pre-commit hook + `adr-guard` alias | executed |

---

## Dev rules

1. **Temple family is untouched.** Never modify `temple-*.zsh` or `temple-*.hook` without a temple gate (decision 0009).
2. **Separation of concerns.** `keyboard.zsh` = aliases only (no bodies). Engines (`gemini-processor.sh`, `claude.zsh`, `devenv.zsh`) hold bodies. No aliases in engines or per-agent scripts.
3. **New Gemini agent seat.** Create `~/.gemini/agents/<name>.md` + `<name>.sh` + add shims to `keyboard.zsh` (PARTITION 3) + update `AGENTS.md`. Launcher scripts source `gemini-processor.sh`. Full checklist: `~/.config/zsh/guides/guide-for-builder.md`.
3b. **New experimental runner.** Follow [`experimental/README.md`](experimental/README.md): add `experimental/<id>/runner.zsh`; it is deployed recursively and invoked lazily through `exp-run <id>`. Do not add a deploy-script mapping. Add a file-map row here + update `AGENTS.md`.
4. **The builder guide is LAW.** Pattern-read `~/.config/zsh/guides/guide-for-builder.md` §Architecture rules BEFORE writing anything here (lesson of 2026-07-11).

---

## Guide pointers

- **Building here (LAW):** `~/.config/zsh/guides/guide-for-builder.md`
- **Invoking agents:** `~/.config/zsh/guides/guide-for-user.md`
- **Temple mail (send · read · pick · manage):** `~/.config/zsh/guides/guide-temple-mail.md`
- **Keyboard map + grammar:** `~/.config/zsh/guides/keyboard.md` · global spec: `guides/claviature.global.spec.md`
- **Guides index:** `~/.config/zsh/guides/index.md`

---

## Gemini first-awareness

First-session orientation for all Gemini CLI work — auth status · Antigravity successor ·
invocation pattern check (hang classes):

`~/.gemini/GEMINI.md`

---

## Troubleshooting (CLI hang symptoms)

**Ripgrep startup stall — "Initializing..." hangs for ~5 minutes (#20433)**
The CLI downloads `rg` to `~/.gemini/tmp/bin/rg` on first run. If network is restricted or rg
is absent and the download stalls, startup blocks for up to 300 seconds.
Fix: add `"useRipgrep": false` to `~/.gemini/settings.json`, OR symlink system rg:
`ln -s /usr/bin/rg ~/.gemini/tmp/bin/rg` (symlink is preferred — retains grep capability).

**GNOME Keyring block — CLI hangs at auth on Linux (#21622)**
`keytar.setPassword()` blocks indefinitely on some GNOME/Manjaro configurations even with
libsecret installed. Symptom: CLI hangs silently before any prompt is processed.
Fix: `export GEMINI_FORCE_FILE_STORAGE=true` in the shell (or add to launcher scripts).
This forces file-based token storage and bypasses keytar entirely.
