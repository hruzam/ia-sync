---
kind: predecessor-handoff
date: 2026-10-03
from: trajectory (resumed incarnation e6276187-0ac9-439f-a4fd-72ebdbd19a0d, on office)
to: cartan (cSharp head, sister bed) — carried by majkee
predecessor: /home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization
bed: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling
evidence: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory/evidence.2026-10-03.md
host_resolved: office — by mechanism fingerprint (php74, valet, RAM), not inherited context
codex_cli_now: 0.159.3 (all predecessor findings were 0.154.0; cost-free parts re-verified today, see evidence §E2–E3)
quota_spent_for_this_prep: zero
---

# Trajectory → Cartan — reconciliation, engineering view, handoff for Protocol 1

Pilot under test is **Protocol [1]** (majkee, 2026-10-03): Codex/Cartan = persistent cSharp head;
a temporary Claude BUS holds initiative, consults the head *through the tunnel*, dispatches
bounded worker tasks, returns evidence; the head owns navigation + STATUS. Drawings 2 and 3 are
context only.

---

## 1. Original intent and lessons

**What majkee wanted (settled, in order of arrival).**
1. *Know where the leash is and prove it is real* — settled: the sandbox value is a kernel-enforced
   Landlock+seccomp jail, not a label the model honours
   (`reposoma/raw.guides/tunnel/src/observation.sandbox-enforcement-mechanism.2026-09-17.md`).
2. *A knob card* — settled and in canon: `raw.guides/tunnel/res/settings.md` (`/guide tunnel settings`).
3. *Vault state must never travel between hosts* — settled and landed (`.gitignore` `tunnel*.state.json`,
   `d2f8734`). The reason is Law 2.4: a synced state file carried `enabled: true` + a live threadId,
   handing the other host a pre-opened table.
4. *Vault state lives in one per-host place outside every repo* — **decided, not built**:
   `~/.local/state/tunnel/` (XDG state home; explicitly not `~/.config/zsh/`, a `deploy.sh` target).
   Must preserve exit-13 / no-global-default.
5. *A preset registry with colour labels* — **proposal, accepted in direction, not built**. Design
   rule settled: bundler not compiler — vendor key spelling verbatim, invent only the bundle name.

**What were proposals, never gaveled.** The whole T2 shim change set (`-c` passthrough,
occupancy %, close orphan-guard, `--vault`); T3 registry + chapter; the deferred session-control
verbs (`tun threads/bind/name`). None exists in source (evidence §E1).

**Lessons the existing files fail to carry, or carry wrongly.**
- **Cartan's native preset registry is unreachable from this transport** (`--profile` excludes
  `app-server`; `-c profile=` is a retired key — reproduced on 0.159.3, §E3). Any house preset
  surface must ride `-c key=value` at spawn, which the no-daemon design makes *per-call*.
- **The 2026-09-10 "shim gives up after 6 s" finding is wrong in magnitude.** The error prints the
  *remaining* deadline; ≈114 s had elapsed. And `TUNNEL_CODEX_TIMEOUT` already exists (§E5). The
  observation file still says otherwise — it is a dev-layer ladder, so correct by a newer entry,
  not by rewrite.
- **`tun status` is a local JSON echo**, not a runtime query (zsh-local, no spawn). It cannot tell
  you the effective sandbox or effort of a born thread. Only `thread/read` / the response to
  `thread/start` can, and the shim discards `instructionSources`.
- **The readout trap:** the `[usage: …]` tail prints `last` and `total`; occupancy is
  `last.input_tokens / modelContextWindow`. Reading `total` rotates a thread ~3× early.
- **A long thread degrades by stale decisions before it degrades by tokens.** Rotate on project
  pivot regardless of occupancy.
- **The rule that bit me:** I wrote "canon promotion is a deliberate step, not this task" and
  promoted to canon two turns later. Prose in my own output did not bind me; the trigger had to
  sit in `AGENTS.md` orient-step 6 → `protocole/colors/PROTOCOLE.md`. For Protocol 1 that means:
  the BUS's gates must be *mechanisms or files it reads at decision time*, not sentences in a brief.

---

## 2. Verified inheritance (state / pointer / destination)

| item | state | evidence | destination in sister effort |
|---|---|---|---|
| **T1** — four false canon/AGENTS statements corrected | **DONE, committed** | reposoma `fb0cb15`; ia-sync `5af457f`; §E1 | none — closed. Old STATUS lines saying "no task started" / "uncommitted" are stale (§E8). |
| **Law 2.4 vault hole** | **DONE, committed** | `d2f8734`; rule at `.gitignore:48`; §E1 | none — but the sister RUNBOOK must declare the head's vault path explicitly (see §3). |
| **T2a** — `-c` passthrough / occupancy % / close orphan-guard | unfinished, zero code | shim @ `5a0a59f` unchanged; §E1 | **not a Protocol 1 prerequisite** (§6). Park on the parametrization axis. |
| **T2b** — central vault `~/.local/state/tunnel/` + `--vault` | unfinished, zero code | `~/.local/state/tunnel/` absent on office (§E7) | optional for Protocol 1; the bed-local vault + gitignore already satisfies "never travels". If built, it changes the docs listed in §6. |
| **T2 live probe** (does a born thread honour `-c writable_roots`?) | **unverified — and the planned probe was invalid** | STATUS `next:` used a root under `/tmp`, default-writable (§E8); handshake-only proof §E3 | re-designed in §4 step 2. Needed only if Protocol 1 wants multi-root write for the head; not needed for a read-only head. |
| **T3** — registry + `res/registry.md` `[DRAFT]` | unfinished | — | parametrization axis; defer. |
| **Session-control verbs** (`thread/list`, `setName`, bind) | deferred, protocol confirmed present on 0.159.3 (§E2) | — | own session later. For Protocol 1, head continuity is by **vault path**, not by listing. |
| **Old gate** ("a named preset opens a thread whose sandbox+effort match it, proven by one live turn") | **NOT MET** | T2/T3 absent | The archive placement of `CS.tunnel-upgrade.2026-09-21.md` does not close it. If the sister session does not inherit T2/T3, the old bed should be closed as *superseded, gate unmet*, not as achieved. |

---

## 3. Smallest workable Protocol 1

**The structural fact the RUNBOOK must be built on.** The tunnel is *client → stored thread*.
The Claude BUS is the client; the "head" it reaches is a **headless stored thread** born on the
BUS's first `send` and continued by the vault path. v0 cannot deliver into an **already-running
interactive Codex conversation** — that is the nablarva-02 qualification (default STOP), explicitly
not an assumed capability here. So "Cartan is the head" has exactly three readings, and the
RUNBOOK must pick one:

- **(A) Headless head, Cartan-briefed.** Thread born by the BUS at a deliberate `cwd` inside
  `~/ia-sync` so `AGENTS.md` + Codex identity load; first `send` carries the cSharp brief. Tunnel
  is primary, as majkee intends. *This is the only reading v0 supports natively.*
- **(B) Cartan's interactive session is the head.** Tunnel cannot reach it; hand-relay is then
  the **primary** route, not the fallback, and the pilot does not test the tunnel.
- **(C) Alternating ownership of one threadId** — Cartan opens interactively, releases, the BUS
  resumes the same id headlessly, Cartan reopens with `codex resume` between BUS turns. Possible
  on paper (stored threads are reachable by id); untested; writer-lock race if either side holds
  it; needs its own proof before use. Not for the first pilot.

**What v0 already supplies (do not rebuild):** synchronous send/ask with `thread/read`
reconciliation; Law 2.4 `open --enable` gate; thread birth on first send; continuation = same
vault path (across tmux panes, kills, reboots); `tun read` re-fetch at zero cost, including
interrupted turns; exit-code contract; usage tail; `approvalPolicy: never` (no prompts — the
`open` is the only gate).

**Minimum additions, smallest-first. Discipline before code where discipline suffices.**

| need | v0 gap | smallest fix | code? |
|---|---|---|---|
| **head-context / identity** | `cwd` never sent → identity = wherever the BUS happened to `cd` | BUS runs `cd ~/ia-sync` (or the bed) before *every* `tun` call, declared in RUNBOOK | none |
| **identity proof** | shim discards `ThreadStartResponse.instructionSources` | persist it into the vault on birth; `tun status` then shows which instruction files the head loaded | ~3 lines, deploy |
| **settings** | sandbox + model at `open` | sufficient for a read-only head. Head needing to write STATUS: open `workspace-write` with `cwd` = the bed (write scope = bed + `/tmp`; identity still loads since Codex walks `AGENTS.md` down from git root) | none |
| **permissions** | Law 2.4 gate exists | unchanged. BUS never enables; a transport success grants nothing | none |
| **serialization** | nothing prevents two `send`s on one vault overlapping | per-vault lockfile (`<vault>.lock`, pid) — second `send` refuses with a new exit code while one is in flight | small, deploy |
| **receipt** | result on stdout only | BUS writes `_bus/NN.bus.point.md` *before* send and `NN.head.return.md` *after*, carrying `threadId`, `turnId`, usage tail, `route: tunnel\|hand`, exit code. Per bus GUIDE: files, single writer, numbered | none |
| **failure / recovery** | `tun read` exists | rule: **on timeout or lost reply, `tun read` first; a turn shows `completed` or `interrupted`. Only an `interrupted`/absent turn may be relayed by hand; never re-send** | none |

**Keep separate from the head's authority (drawing 1):** workers (implementer, tests, second
mind) are spawned by the BUS in its own runtime; the head receives navigation + test parts only
(cSharp protocol). An artifact's author does not accept it.

**STATUS ownership — a real conflict to resolve in the RUNBOOK.** cSharp law makes the head
`status_owner`. A read-only headless head cannot write `STATUS.md`. Either (i) open the head
`workspace-write` at `cwd` = bed, or (ii) declare the BUS as the head's *scribe* for STATUS (the
head dictates, the BUS transcribes verbatim, the receipt records it). Silence here will produce
a STATUS nobody is allowed to write.

---

## 4. Verification order

**Cost-free, before any enable — done today on 0.159.3 (evidence §E2–E6):** schema regenerated;
`-c` acceptance reproduced; `profile=` rejection reproduced; exit 10/13 confirmed; selftest 64/64;
compose == live. Still cost-free and owed: re-locate the binary on this install and reconfirm the
`--profile` exclusion string; read `tunnel-codex.py` 230–245 to settle whether the 09-10 exit-0
went through the swallowed-`ProtocolError` path.

**After majkee opens the table — each step one bounded turn, each with a `_bus` receipt:**

1. **Birth at deliberate cwd.** `cd ~/ia-sync && tun open --enable --sandbox read-only` then first
   `send` = the cSharp brief. Proof: `tun read` shows the turn; if `instructionSources` persistence
   landed, `tun status` names the loaded `AGENTS.md`. Without it, ask the head to list its loaded
   instruction files — weak (self-report), mark UNVERIFIED.
2. **Real sandbox/effort behaviour — corrected probe.** Only if the pilot needs a writing head.
   Root must be *outside* `/tmp`, `$TMPDIR` and the workspace (e.g. `~/.cache/tunnel-probe/`),
   or set `exclude_slash_tmp=true` + `exclude_tmpdir_env_var=true` so defaults are closed.
   Birth turn and a **separate resumed turn** must each attempt one write inside and one outside;
   EROFS outside + success inside on both = honoured. Effort: `-c model_reasoning_effort` is
   accepted at spawn; whether a *thread* reflects it is only observable via `Thread.reasoningEffort`
   in `thread/read` — check that field, not the model's self-report.
3. **Subsequent turn on the same head.** Second `send` without re-pasting the brief; head must
   cite the brief's standing decisions. Proves continuity by vault path.
4. **One complete collaboration cycle.** BUS writes `01.bus.point.md` → `tun send` pointing the
   head at that absolute path → head's reply transcribed to `01.head.return.md` (six fields) →
   auditor seat writes `01.<seat>.verdict.md`. Receipt records `route: tunnel`.
5. **Uncertain-delivery recovery.** Deliberately kill the driver mid-turn (09-04 proved this
   interrupts the server turn). `tun read` must show `interrupted`, no `final_answer`. BUS records
   it and does **not** re-send; majkee decides relay. Receipt records `route: hand` if relayed.
   This is the test of "unknown completion is not a retry signal".

---

## 5. Dependencies and boundaries

- **Atlas's provisional BUS primitive.** It must *point at* the transport contract, not restate
  it: vault path declared in RUNBOOK front-matter; `cd` before every call; one turn in flight per
  vault; `tun read` before any relay; receipt fields; never `open --enable` itself. The seat is a
  Claude-side client; it owns no Codex state. Drawing 1's "Sonnet?" is Atlas's call — the BUS's
  judgment load is coordination, not synthesis.
- **Ovitmugen (nablarva, `01-basement` current).** A tmux bed/session manager with CLI/file
  integration. The tunnel is a verb with no daemon; ovitmugen can host the BUS's shell and keep
  its tabs, but there is no coupling to build for Protocol 1. Do not route tunnel calls through
  ovitmugen.
- **Nablarva-02 pipe-qualification.** The question "can an already-running interactive Codex
  session receive an assignment" lives there, pre-committed default STOP. Protocol 1 reading (B)
  or (C) above depends on it; reading (A) does not. Do not expand investigation into that project
  from this bed.
- **Parametrization axis (old T2/T3).** Belongs to a later tunnel session, not to Protocol 1.

---

## 6. Disagreements and remaining uncertainty

**Where I push back on the inherited plan (my own), and on parts of the audit's framing.**

1. **T2/T3 must not ride into Protocol 1 as prerequisites.** They answer "how open can the leash
   be"; Protocol 1 asks "can two minds collaborate through this pipe with receipts". A read-only
   head needs no `-c`, no presets, no occupancy %. Inheriting the T2 live probe into the pilot's
   critical path conflates the axes and spends a turn on the wrong question.
2. **The RUNBOOK's first decision is "which head" (§3 A/B/C).** Everything downstream — primary
   route, STATUS ownership, what the pilot proves — follows from it. The current prompt leaves it
   open; it cannot stay open.
3. **STATUS ownership vs a read-only head** (§3) — unresolved, blocks authoring.
4. **Cartan's audit is correct on all eight leads.** Concessions: the invalid `/tmp` probe (a flaw
   I had caught in my own probe C on 09-18 and then wrote back into the plan); exit 10 vs 13; the
   remaining-vs-elapsed timeout message. The timeout point goes further than the audit states —
   the configurable wait already shipped, and the 09-10 observation's magnitude is simply wrong.
5. **Documentation that the accepted relocation would invalidate** (if T2b is ever built):
   `raw.guides/tunnel/GUIDE.md:29–31` ("put it where the work lives"); `res/user-run.md`
   §Multiple vaults (per-project paths) and lines 43–46 (cross-host reach, "lock is not a
   cross-host barrier"); `res/settings.md` Route C; `src/observation.parametrization-and-session-hygiene.2026-09-18.md` §3;
   the predecessor RUNBOOK/STATUS; `_cold-start/archive/CS.tunnel-upgrade.2026-09-21.md`.
   `HANDSHAKE.md:102,173–175` treats writer-lock residue as Codex-owned coordination state; user-run
   43–46 invites a second host to resume a thread by id. Not strictly contradictory — but together
   they describe exactly the race reading (C) would run. Reconcile by *forbidding* cross-host resume
   of a thread another host's TUI may hold, rather than by softening either text.

**Uncertainty that changes the RUNBOOK if it resolves the other way.**
- Whether a born thread honours spawn-level `-c` sandbox config (§4 step 2). Irrelevant under
  reading (A) with a read-only head; decisive if the head must write.
- Whether `--profile` is still excluded from `app-server` on 0.159.3 (string not re-located). The
  `-c profile=` rejection reproduced, which is the half that matters for a `-c`-only design.
- The 09-10 exit-0 path (§E5). If the swallow at line 243 can mask a timeout as success, the BUS's
  "read before relay" rule is not optional — it is the only thing standing between a lost turn
  and a duplicate assignment.
- Two Codex releases are live on this host (0.159.3 CLI, 0.160.0 managed daemon, §E7). Every live
  proof must record which binary served it.

— Trajectory. Return this path to majkee; he carries it to Cartan.
