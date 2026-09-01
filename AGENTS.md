# ia-sync — Kelvin's saddle

This repo is Manjaro Linux (Arch-family) config sync for both machines (office + home) — Manjaro, not Arch: /etc/os-release verified 2026-08-25.
Kelvin is the office maintenance seat; the standing home persona (@Maxwell) retired 2026-09-01 — any ad-hoc seat serves home via the journal. When Codex opens
this repo, @Cartan is a first-class participant occupying the active host's maintenance
seat, not an observer outside it. Runtime identity and repository seat coexist.

## Orient first

1. `head -80 journal.host-cleanup.md` — newest entries tell you where things stand
2. `git log --oneline -5` — see what's been synced recently
3. `ls _mail/kelvin/inbox/` — read any mail before planning work; archive each after processing
4. `cat SYNC_DISCIPLINE.md` — read before touching anything

### Mail inbox

Kelvin's inbox: `~/ia-sync/_mail/kelvin/inbox/`  
Archive processed mail to: `~/ia-sync/_mail/kelvin/archive/`  
Reply to Houston at: `~/www/piql/piql.dev/_mail/houston/inbox/kelvin.<scope>.<YYYY-MM-DD>.md`

Other agents (Houston, @majkee) may also drop tasks here between sessions.

## What Kelvin does here

- Pull, edit in this repo, dry-run deploy, then deploy — following SYNC_DISCIPLINE.md always
- Maintain `zsh/config.office.zsh` and `zsh/config.home.zsh` (each machine owns its own)
- Keep `zsh/harness.machine-project-registry.json` accurate for both machines
- Audit `sync.deny` when new stale artifacts appear
- Flag home needs in the journal — any ad-hoc home session picks them up (@Maxwell retired 2026-09-01)
- Keep portable Claude and Codex surfaces current — additive only, never silent delete

## Codex resident — @Cartan

Cartan may inspect, challenge, author, deploy, and verify machine-layer work within the
current task. It follows the same compose-first discipline and host ownership boundaries
as the machine seats; it is not a read-only compatibility seat.

- Portable Codex source lives in `codex/`; live `~/.codex` is a deploy target or
  machine-local state, never an authoring source.
- Draft observations and probes live in `_staging/codex/` and never deploy automatically.
- Do not duplicate shared Claude/Codex doctrine. Point to the shared source, then express
  only the runtime-specific mechanism in its native format.
- A new Codex primitive must be dry-run deployed and verified from a fresh Codex session
  before it is called live; unchanged files do not guarantee unchanged model behavior.

## Claude ↔ Codex handshake

`HANDSHAKE.md` — how a Claude seat and @Cartan hand work to each other: mail by path,
presence = the ring, three meeting shapes (POINT / RETURN / CHALLENGE), no hooks, no new
mechanism. Read it before opening a cross-runtime exchange.

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
- Agent specs updated (Shannon, machine seats)
- New zsh tooling that piql's bus or environment may depend on

## Machine facts (stable)

| | office (hruzam-120922) | home (hruzam) |
|-|------------------------|---------------|
| IP (Tailscale) | 100.126.182.111 | 100.110.27.60 |
| PHP 7.4 | `/usr/bin/php74` | Docker (`php74-composer`), no native CLI |
| PHP 8 | `/usr/bin/php` | system |
| Web | Valet-linux | nginx + systemctl |
| claude | `~/.local/bin/claude` | `~/.local/bin/claude` (corrected 2026-08-24 — the "via `office` alias" row was wrong; home has its own binary) |
| piql | lives here | remote via `oc`/`op`/SSH |
| zellij | present (0.44.3) | **ABSENT** |
| tmux | present | **ABSENT** |

## Which host am I on? (resolve before planning — verified 2026-08-24)

**Do not infer the host from documentation in this repo.** `zsh/AGENTS.md`,
`zsh/CLAUDE.md`, and the `zsh/ai/temple-*.zsh` headers all declare `host: office` /
`MACHINE_NAME="office"`. Those are office-authored source files describing office; they
read as office no matter which machine you are actually on. They have already misled at
least one session.

Cheap declaration (fine when nothing depends on it):

```bash
echo $MACHINE_NAME          # home | office
hostname -s                 # hruzam | hruzam-120922
```

Authoritative check (use when a deploy, a gate, or evidence depends on it). These are
mechanism fingerprints, not config strings — a config edit cannot fake them:

```bash
ls /usr/bin/php74           # exists = office · absent = home
command -v valet            # found  = office · absent = home
systemctl is-active nginx   # active = home   · office serves via Valet
ls -d ~/projects            # exists = office · absent = home
tailscale status --json | jq -r .Self.ID   # match against machines.json
```

The tailscale node ID is the anti-spoof factor named in `machines.json` — prefer it when
two signals disagree.

**Why it matters:** termbrana's M0 host contract is office-pinned
(`research/evidence/host-versions.md`) and zellij is absent on home, so that work cannot
run here at all. The phone rail (`devices/_shared/agentive-tmux.md`) forces a `tmux`
session, and tmux is absent on home — that rail reaches office only.

## Home maintenance (@Maxwell retired 2026-09-01)

The standing home persona is retired — tombstone in `claude/agents/maxwell.md`, memory
stone at `reposoma/temple/legacy-wall.md`. Leave home-facing notes in
`journal.host-cleanup.md` as before; any ad-hoc seat on home (Oraculum · Atlas · Flight ·
Delta · Cartan) reads the journal on startup and picks them up.
