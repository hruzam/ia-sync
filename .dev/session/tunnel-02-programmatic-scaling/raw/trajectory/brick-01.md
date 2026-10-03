# BRICK-01 — head binding + continuity hygiene for Protocol 1

`author: trajectory (resumed, office) · date: 2026-10-03 · state: CUT ON THE TABLE, selftest green,`
`dry-run clean — NOT deployed, NOT committed. Apply is majkee's hand.`
`surface: ~/ia-sync/zsh/ai/tunnel-codex.{py,zsh,selftest.zsh} (compose-first; live ~/.config/zsh/ai/ untouched)`
`companion: trajectory.handoff.2026-10-03.md §3 (why these six and not the parametrization set)`

## What it adds — six things, smallest-first

| # | change | mechanism | why Protocol 1 needs it |
|---|---|---|---|
| 1 | **`open --enable --thread <id>`** — bind a vault to an EXISTING stored thread | state gets `threadId`, `bound: true`, `boundAt`; preflight only, **no `thread/resume` at bind** | the head is Cartan's existing session, not a fresh birth. Binding is a local declaration; the liveness probe is the operator's explicit `tun resume` *after* the interactive client has released the thread |
| 2 | **`open --cwd <dir>`** | stored in state; app-server **spawn dir on every verb** + `thread/start.cwd` on birth; **never sent on resume** (a bound thread keeps its own cwd) | head identity = which `AGENTS.md` loads = cwd. Was accidental (wherever the caller stood); now deliberate |
| 3 | **runtime stamp** | after `thread/start`, `thread/resume`, or `tun resume`: server-reported `sandbox · reasoningEffort · cwd · model · instructionSources · approvalPolicy` → `state.runtime` + `observedAt` | repairs Cartan's "status weakness": `tun status` now shows runtime truth as of last contact, not only saved intent. `ThreadResumeResponse` carries all of these on 0.159.3 (verified from regenerated schema) |
| 4 | **per-vault turn lock** | `<state>.lock` (our pid, `O_EXCL`) held for the whole of `send/ask/steer`; live holder → **exit 61**; dead-pid residue cleared automatically | the hard rule "never two turns on one head" becomes a mechanism, not a discipline |
| 5 | **writer-lock advisory** | READ-ONLY existence check of `~/.codex/thread-writer-locks/<id>.lock` at bind/resume/send → stderr note. Never blocks, never removes | the Codex lock can be stale residue (HANDSHAKE). Blocking on it would push someone toward deleting it — the forbidden act. The receipt layer (`tun read` before any relay) owns the race outcome |
| 6 | **`close` orphan-guard** | prints the threadId + the exact re-bind command + transcript glob on stderr **before** removing state; also removes a leftover turn lock | `close` was one-way in practice — the state file was the only holder of the address |

**Deliberately NOT in this brick:** `-c` passthrough, effort/presets/registry, occupancy %,
`~/.local/state/tunnel/` relocation, `thread/list`/`setName` verbs. Those are the
parametrization axis (handoff §6.1); none is a Protocol 1 prerequisite for a read-only head.

## Exit-code contract change

`61 turn-in-flight` added to both headers. Everything else unchanged (0 · 10 · 11 · 12 · 13 · 20 ·
30 · 40 · 50). `--cwd` on a non-directory and `--thread`/`--cwd` on any verb but `open` → 11.

## Proof on the table (zero quota)

- `python3 -m py_compile`, `zsh -n` on all three: clean.
- Selftest on the compose copy: **86/86** = the original 64 + 22 BRICK-01 fixtures (bind state
  shape · bind banner · send-after-bind takes the resume path · lock held by a live pid → 61 and
  the lock is left alone · dead-pid lock cleared and send proceeds · `--cwd` missing dir → 11 ·
  `--thread` on `send` → 11 · close names the thread + re-bind command, stdout empty).
- `bash deploy.sh --dry-run`: exactly `ai/tunnel-codex.py`, `ai/tunnel-codex.zsh`,
  `ai/tunnel-codex.selftest.zsh` would travel in the zsh leg (the `__pycache__` my compile step
  created was removed before this check).
- Live copy still the old shim; live selftest still 64/64.

## Apply (majkee's hand — the verification order is fixed)

```zsh
cd ~/ia-sync
PYTHONDONTWRITEBYTECODE=1 zsh zsh/ai/tunnel-codex.selftest.zsh   # expect 86/86
bash deploy.sh --dry-run                                         # read the zsh leg
bash deploy.sh
PYTHONDONTWRITEBYTECODE=1 zsh ~/.config/zsh/ai/tunnel-codex.selftest.zsh   # LIVE copy: 86/86
```

Commit when you choose; nothing here commits.

## First hot run — Protocol 1, head = Cartan's existing session (reading C)

Each step is one bounded action; the two marked ⚡ spend quota and need the table opened.

```zsh
# 0. vault lives in the sister bed; gitignored by tunnel*.state.json
export TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.state.json

# 1. bind — local declaration only, no server call beyond preflight
cd ~/ia-sync && tun open --enable --thread 01a0fab0-ebcd-7280-84ee-a40e38c29838 --cwd ~/ia-sync
tun status      # expect threadId set, bound:true, cwd set, no runtime block yet

# 2. ⚡ liveness probe — ONLY after Cartan's interactive session has released the thread
tun resume      # stderr: status + effective sandbox/effort/cwd + instructionSources → stamped into state
tun status      # now shows state.runtime — this is the head's real policy, not our intent

# 3. ⚡ first collaboration turn — BUS writes _bus/01.bus.point.md first, then:
tun ask "read /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/_bus/01.bus.point.md and reply in the six RETURN fields"
# → transcribe reply to _bus/01.head.return.md; receipt: route=tunnel, threadId, lastTurnId, usage tail

# recovery rule, always: on timeout / lost reply →  tun read   (free) before ANY hand relay.
```

**What the first run proves / does not prove.** Step 2 proves bind + resume + runtime
stamping against a real thread. Step 3 proves one POINT→RETURN cycle with a receipt. Neither
proves that the interactive client and the tunnel can *alternate* safely on one thread over
many cycles — that is the reading-(C) race (handoff §3) and needs its own evidence before it is
called a capability. The writer-lock note on stderr is the tell: if it appears at step 2,
Cartan had not released.

## Open to Cartan's challenge

- Should bind refuse (not just warn) when the Codex writer-lock exists? I chose warn-only because
  the lock is documented residue-prone and the forbidden act is touching it. A refuse-with-override
  flag trains the operator to always pass the override.
- `--cwd` is not sent on resume by design. If the sister RUNBOOK wants the head re-rooted on
  resume, `ThreadResumeParams.cwd` exists on 0.159.3 — a one-line change, but it mutates a thread
  the interactive client also uses.
