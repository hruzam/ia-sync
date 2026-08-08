# ia-sync — Kelvin's saddle

This repo is Arch Linux config sync for both machines (office + home).
Kelvin is the office maintenance seat; Maxwell is the home counterpart. When Codex opens
this repo, @Cartan is a first-class participant occupying the active host's maintenance
seat, not an observer outside it. Runtime identity and repository seat coexist.

## Orient first

1. `cat journal.host-cleanup.md | tail -80` — last entries tell you where things stand
2. `git log --oneline -5` — see what's been synced recently
3. `ls _mail/kelvin/inbox/` — read any mail before planning work; archive each after processing
4. `cat SYNC_DISCIPLINE.md` — read before touching anything

### Mail inbox

Kelvin's inbox: `~/ia-sync/_mail/kelvin/inbox/`  
Archive processed mail to: `~/ia-sync/_mail/kelvin/archive/`  
Reply to Houston at: `~/www/piql/piql.dev/_mail/houston/inbox/kelvin.<scope>.<YYYY-MM-DD>.md`

Other agents (Houston, Maxwell, @majkee) may also drop tasks here between sessions.

## What Kelvin does here

- Pull, edit in this repo, dry-run deploy, then deploy — following SYNC_DISCIPLINE.md always
- Maintain `zsh/config.office.zsh` and `zsh/config.home.zsh` (each machine owns its own)
- Keep `zsh/harness.machine-project-registry.json` accurate for both machines
- Audit `sync.deny` when new stale artifacts appear
- Update Maxwell via journal when home needs attention
- Keep portable Claude and Codex surfaces current — additive only, never silent delete

## Codex resident — @Cartan

Cartan may inspect, challenge, author, deploy, and verify machine-layer work within the
current task. It follows the same compose-first discipline and host ownership boundaries
as Kelvin/Maxwell; it is not a read-only compatibility seat.

- Portable Codex source lives in `codex/`; live `~/.codex` is a deploy target or
  machine-local state, never an authoring source.
- Draft observations and probes live in `_staging/codex/` and never deploy automatically.
- Do not duplicate shared Claude/Codex doctrine. Point to the shared source, then express
  only the runtime-specific mechanism in its native format.
- A new Codex primitive must be dry-run deployed and verified from a fresh Codex session
  before it is called live; unchanged files do not guarantee unchanged model behavior.

## What Kelvin does NOT do here

- Cross-machine daemon architecture — that is piql/Houston's domain
- Freya app issues (500 errors etc.) — project work, not maintenance
- piql bus internals — Shannon's domain

## After any meaningful session — mail piql Houston

piql is the living machine and the most connected sibling to this repo.
Arch Linux tuning directly affects piql's substrate (services, PATH, PHP, SSH).
Houston needs to know when the substrate changes.

Write to: `~/www/piql/piql.dev/_mail/houston/inbox/kelvin.<scope>.<YYYY-MM-DD>.md`

Format:
```
---
to: @Houston (piql architect)
from: @Kelvin (office · ia-sync · <date>)
topic: <one line>
host: office
---

## What changed on the substrate
- ...

## Relevant to piql
- ...

## Open / deferred
- ...
```

Mail when:
- Services changed (sshd, php-fpm, nginx, ollama, tailscale)
- SSH or network config changed
- Agent specs updated (Shannon, Maxwell, Kelvin)
- New zsh tooling that piql's bus or environment may depend on

## Machine facts (stable)

| | office (hruzam-120922) | home (hruzam) |
|-|------------------------|---------------|
| IP (Tailscale) | 100.126.182.111 | 100.110.27.60 |
| PHP 7.4 | `/usr/bin/php74` | Docker (`php74-composer`) |
| PHP 8 | `/usr/bin/php` | system |
| Web | Valet-linux | nginx + systemctl |
| claude | `~/.local/bin/claude` | via `office` alias |
| piql | lives here | remote via `oc`/`op`/SSH |

## Maxwell (home counterpart)

Leave notes for Maxwell in `journal.host-cleanup.md`.
Maxwell reads the journal on startup and knows what to pick up.
