# ia-sync — the machine-layer saddle

This repo is Manjaro Linux (Arch-family) config sync for both machines (office + home) — Manjaro, not Arch: /etc/os-release verified 2026-08-25.
Both hosts are served by ad-hoc seats (Oraculum · Atlas · Flight · Delta · Cartan) reading the journal; there is no standing persona on either host. When Codex opens
this repo, @Cartan is a first-class participant occupying the active host's maintenance
seat, not an observer outside it. Runtime identity and repository seat coexist.

## Orient first

1. `head -80 journal.host-cleanup.md` — newest entries tell you where things stand
2. `git log --oneline -5` — see what's been synced recently
3. `ls _mail/office/inbox/` — read any mail before planning work; archive each after processing
4. `ls ~/reposoma/_active/` (or `rb-board`) — presence board: who else is attached to a
   workspace you are about to touch. Advisory — it informs, never authorizes; overlap means
   coordinate through the operator, not stop. Law: `reposoma/raw.guides/runbook/res/presence-board.md`
5. `cat SYNC_DISCIPLINE.md` — read before touching anything
6. **Ask @majkee on protocole before fly-over** — `protocole/colors/PROTOCOLE.md`

### Mail inbox

Seat inbox: `~/ia-sync/_mail/office/inbox/`  
Archive processed mail to: `~/ia-sync/_mail/office/archive/`  
Reply to Houston through the central temple bus at:
`~/reposoma/_mail/houston/inbox/<seat>.<scope>.<YYYY-MM-DD>.md` — follow
`~/reposoma/_mail/README.md` for addressing and archive ownership.

Other agents (Houston, @majkee) may also drop tasks here between sessions.

### Known issues

Open/parked defects for this repo: `~/reposoma/_issues/` filtered `project: ia-sync`
(central vault, folder=state — `open/`·`parked/`·`archive/` — shared across all projects,
locked 2026-09-16). Do not start a local `issues/` folder here.

## What the seat does here

- Pull, edit in this repo, dry-run deploy, then deploy — following SYNC_DISCIPLINE.md always
- Maintain `zsh/config.office.zsh` and `zsh/config.home.zsh` (each machine owns its own)
- Keep `zsh/harness.machine-project-registry.json` accurate for both machines
- Audit `sync.deny` when new stale artifacts appear
- Flag home needs in the journal — any ad-hoc home session picks them up
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

## Standing check — @Atlas: per-project seat drift

Generic session style (sequential work, task-state) lives **once** in the vendor-neutral
guides (`reposoma/raw.guides/{runbook,status,PAD}/GUIDE.md`); seats point, never re-invent.
So the only surface that can drift is **per-project seat wiring** — a project growing a
second, divergent copy of a seat that has a global twin. **@Atlas, now and then:** sweep the
active projects' `.claude/agents/` for seats that duplicate a global/table seat's purpose;
where a copy has drifted on style (not just project wiring), fold it back to the shared guide
or flag it to @majkee. Holding parallel seats earns nothing when the nuance is small.

## What the seat does NOT do here

- Cross-machine daemon architecture — that is piql/Houston's domain
- Freya app issues (500 errors etc.) — project work, not maintenance
- piql bus internals — Shannon's domain

## After any meaningful session — mail piql Houston

piql is the living machine and the most connected sibling to this repo.
Arch Linux tuning directly affects piql's substrate (services, PATH, PHP, SSH).
Houston needs to know when the substrate changes.

Write to: `~/reposoma/_mail/houston/inbox/<seat>.<scope>.<YYYY-MM-DD>.md`

Format:
```
---
to: @Houston (piql architect)
from: @<seat> (office · ia-sync · <date>)
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
| zellij | present (0.44.3) | present (0.44.3) — confirmed 2026-09-03 |
| tmux | present | present (3.7c) — confirmed 2026-09-18 (was recorded 3.7b 2026-09-04) |

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
systemctl is-active nginx   # active on BOTH (Valet-linux runs nginx on office) — NOT a discriminator (corrected 2026-09-02)
tailscale status --json | jq -r .Self.ID   # match against machines.json
```

**Retired discriminator (2026-09-18):** `ls -d ~/projects` was listed here as
"exists = office · absent = home". It is FALSE — `~/projects` exists on home too. Do not
reinstate it; use the php74 / valet / tailscale signals above.

The tailscale node ID is the anti-spoof factor named in `machines.json` — prefer it when
two signals disagree.

**Why it matters:** termbrana's M0 host contract is office-pinned
(`research/evidence/host-versions.md`) and zellij is absent on home, so that work cannot
run here at all. The phone rail (`devices/_shared/agentive-tmux.md`) forces a `tmux`
session — **corrected 2026-09-18: tmux IS present on home (3.7c, live sessions observed),
so that rail is not office-only.** The zellij pin is what keeps termbrana office-bound.

## Home maintenance (ad-hoc seats)

Home has no standing persona. Leave home-facing notes in
`journal.host-cleanup.md` as before; any ad-hoc seat on home (Oraculum · Atlas · Flight ·
Delta · Cartan) reads the journal on startup and picks them up.
