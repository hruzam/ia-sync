# guides/ — index & writer convention

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — the like-composer syncing both machines). Do not edit it in place: cut in
> ia-sync, deploy outward. Before trusting any machine fact here, reality-check the sync
> part: `git -C ~/ia-sync log --oneline -5 -- zsh/guides/index.md` (intent) **and** repo↔live
> `rsync -n` (reality). Commits say what *should* be deployed; only the diff says what *is*.

`~/.config/zsh/guides/index.md · audience: everyone · machine: both · verified: 2026-07-11`
`rule: guides are the operator's memory (CLAUDE.md rule 6). New or changed guide → update this index in the same session.`

---

## Process walks — "I want to…"

| I want to… | open | panel key |
|---|---|---|
| see EVERY key on this machine, live | `claviature.global.spec.md` | `keys` (`--plain` agents · `--all` internals) |
| send / read / pick temple mail | `guide-temple-mail.md` | `temple-help` |
| archive / restore mail (mark read) | `guide-temple-mail.md` §Manage | `temple-mail-manage` |
| sync / deploy a project devenv (freya · fantasyobchod) | `guide-for-builder.md` §Architecture rules · SYNC_DISCIPLINE.md (in the devenv repo) | `devenv-help` · `fr-*` · `bo-*` |
| invoke a Gemini seat (advice · research · code) | `guide-for-user.md` | `gemini-agents-help` |
| drive Gemini through a coding patch loop | `guide-for-user.md` §Patch protocol | — |
| fix/reinstall the Gemini CLI itself (npm EACCES, allow-scripts warning) | `guide-for-user.md` §ai-install :: gemini | `gemini --version` |
| add a new Gemini agent seat / new engine or scope | `guide-for-builder.md` (**LAW** — pattern-read before writing) | — |
| check / refresh stale AI settings cards | `guide-harness-check.md` | `harness-stale` |
| run Claude Code from the phone | `remote.md` | `rc-status` · `rc-*` · `/rc-launch` |
| snapshot a project tree as JSON | `toolbox.tree-converter.md` | `tree-snapshot <project>` |
| see the curated keyboard map + grammar | `keyboard.md` | `ai-help` |
| machine facts (hardware, PHP, paths) | `office.md` / `home.md` | — |
| service ops on home (nginx, fpm, db, docker) | `services.md` | — |
| memory-pressure defense on home | `resource-control.md` | — |

Panel = help functions wired by `ai/keyboard.zsh`. Lost? `ai-help` is the curated master;
`keys` is the raw derived truth.

---

## Registry

| guide | audience | machine | scope | verified | attachments |
|---|---|---|---|---|---|
| `guide-for-user.md` | operator | both | invoking Gemini seats: UI, headless, bluebottle, patch protocol, ai-install (npm) | 2026-07-27 | — |
| `guide-for-builder.md` | builder | both | adding a Gemini seat **+ Architecture rules (LAW): aliases-only keyboard · scope engines · .sh/.zsh rule · partition maps · engine inventory**; maintenance log | 2026-07-27 | — |
| `guide-temple-mail.md` | operator+agent | office | temple mail family: send · read · pick · manage · doorbell | 2026-07-11 | — |
| `guide-harness-check.md` | operator | office | card-freshness checker: `harness-stale`, systemd units, actioning alerts | 2026-07-11 | — |
| `keyboard.md` | operator+agent | office | the claviature: grammar (**LOCKED**), key map P1–12, shim class | 2026-07-11 | — |
| `claviature.global.spec.md` | builder+operator | office | global claviature: design locked + **BUILT** (`keys` panel; operator-finger gate pending) | 2026-07-11 | — |
| `remote.md` | operator | office | Claude Code Remote Control: A (systemd) · B (rc.sh/tmux) · B+ (agent-aware engine + `/rc-launch` skill, cross-host) — knowledge card, volatile | 2026-08-15 | — |
| `toolbox.tree-converter.md` | operator+agent | both | tree-snapshot usage + tcr configs | 2026-07-11 | — |
| `office.md` | operator+agent | office | machine profile: hardware, dual-FPM PHP, valet routing | 2026-07-02 | `sudoers.valet-php.conf` (deployable — install path in its own header) |
| `home.md` | operator+agent | home | machine profile: hardware, services, tools | 2026-06-28 | — |
| `services.md` | operator | home | service management + troubleshooting | 2026-06 | — |
| `resource-control.md` | operator | home | 5-layer memory-pressure defense | 2026-05-18 | — |

Retired: `ai.md` (2026-07-11) — §1 lives on as `guide-harness-check.md`; token-hygiene folded into
`guide-for-user.md` §Hygiene; the ai/ layout copy is dead by design (see convention rule 3).

---

## Writer convention (five rules, hold them)

1. **Name by kind:** `guide-<topic>.md` = how-to · `<machine>.md` = machine profile ·
   `toolbox.<tool>.md` = tool usage. Attachments keep their deploy name and are listed in the
   owning guide's registry row — never orphaned.
2. **Head block first:** location line + `audience:` (operator | agent | builder) + `machine:`
   (office | home | both) + `verified:` date. Volatile content → full knowledge-card frontmatter
   (`remote.md` is the reference shape) so `harness-check` can adopt it later.
3. **Point, never copy:** the live file map lives in `AGENTS.md`; canon lives in the temple;
   partition/engine truth lives in `guide-for-builder.md` §Architecture rules. Link — do not
   restate. (The old `ai.md` restated the map and rotted within a week. Standing cautionary tale.)
4. **Open with the process, not the inventory:** the first section answers *"when do I reach for
   this and what do I type"* — a short walk before any reference table.
5. **Same-session index update:** touched a guide → touch this index (row + verified date).
