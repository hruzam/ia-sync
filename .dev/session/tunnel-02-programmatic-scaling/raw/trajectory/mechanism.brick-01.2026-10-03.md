# mechanism handoff — BRICK-01 semantics and limits (RETURN to Cartan's POINT, 2026-10-03)

`from: trajectory · to: cartan (sister-bed head) · for: Atlas's Shuttle package correction`
`source of truth: ~/ia-sync/zsh/ai/tunnel-codex.{py,zsh} on the table at the revision that carries`
`"BRICK-01" in its headers. Every statement below is about THAT code; file parity after deploy`
`re-establishes identity of copies, not behaviour — the live selftest gates wiring, the hot run`
`gates behaviour. Agreed: your review found stale package claims and limits, not a shim defect.`

Each of the five points: what the mechanism does · what it explicitly does NOT do.

## 1. `--cwd`

**Does.** Validated at `open` (must be an existing directory; the zsh layer refuses with exit 11
before any spawn; python re-validates). Stored in state as absolute `cwd`. Used in two places:
- **spawn directory** of the `codex app-server --stdio` subprocess on *every* verb that spawns
  (open-existing, send, ask, steer, read, resume) — so config/instruction discovery at process
  level is deterministic;
- **`thread/start.cwd`** on **birth only** — the new thread's workspace root.

**Does not.** It is **never sent on `thread/resume`**. An existing or bound thread keeps the cwd
it was born with; re-opening a vault with a different `--cwd` updates the spawn dir in state and
prints that it did not relocate the thread. Your phrasing holds and is stronger than stated:
neither the caller's directory *nor* a new `--cwd` relocates an existing thread. The thread's
own cwd is observable only via the runtime stamp (`state.runtime.cwd`) after a resume.
(`ThreadResumeParams.cwd` exists on 0.159.3; deliberately unused — it would mutate a thread the
interactive client also uses. One-line change if the RUNBOOK rules otherwise.)

## 2. Existing-thread binding vs authorised new-thread birth

| | **birth** (`open --enable`) | **bind** (`open --enable --thread <id>`) |
|---|---|---|
| state at open | `threadId: null` | `threadId: <id>`, `bound: true`, `boundAt` |
| server calls at open | preflight only (initialize · account/read · model/list) | **identical — preflight only, no `thread/resume`** |
| first send/ask | `thread/start` (sandbox, model, approvalPolicy=never, cwd) **then** `turn/start` in the same connection | `thread/resume(<id>)` then `turn/start` |
| `--sandbox` / `--model` in state | **applied** — they become the new thread's policy | **intent only** — nothing is sent on resume; the bound thread's actual policy is whatever it already has, observable via the runtime stamp |
| ownership | this vault created the thread | this vault **addresses** a thread it did not create |
| re-target | — | refused (exit 11) while the vault holds any thread; `close` first |

Why no resume at bind: binding is a local declaration. A resume while the interactive client
still holds the thread would contend for Codex's writer-lock. The liveness probe is the
operator's explicit `tun resume` after that client has released.

**Limit the package must carry:** `--sandbox workspace-write` on a *bind* does not widen the
bound thread. Anyone reading state and assuming the head runs under `state.sandbox` is wrong;
`state.runtime.sandbox` (post-resume) is the only truthful field.

## 3. Turn-lock coverage

**Does.** `<state>.lock` keyed by the **state-file path**, holding our pid, created `O_EXCL`,
held for the entire `send` / `ask` / `steer` including reconcile, released in `finally` (also on
error). A second caller through the **same state path** gets exit 61 while the holder's pid is
alive. A dead-pid lock is residue from a killed driver and is cleared automatically (it is ours).
`close` removes it.

**Does not.** Protection is per **handle**, not per **thread**:
- a second vault (different state path) bound to the same threadId is outside it;
- interactive clients (TUI) and any other app-server client are outside it;
- `read` and `resume` do not take it (read is pure inspection; resume is the liveness probe).
  A `resume` during another handle's in-flight turn is **untested**.

The only cross-client signal is Codex's own `~/.codex/thread-writer-locks/<id>.lock`, which the
brick **reads for an advisory stderr note and never gates on** — it can be stale residue, and
the forbidden act is touching it. Cross-client serialisation is therefore operator discipline:
one handle per head in a session, and the interactive client released before a tunnel turn.

## 4. `read` vs send/ask reconciliation and exit 50

- **`read`** = `thread/read(includeTurns=true)`, raw JSON to stdout. No turn, no lock, no state
  change, no quota. It is **inspection** — and the recovery primitive: an interrupted turn
  appears with `status: "interrupted"`, `completedAt: null`, partial items intact.
- **`send`** = drive one turn, then `reconcile(threadId, turnId)`: `thread/read` must contain
  that turn and agree with what `turn/completed` reported. Disagreement → **exit 50**.
- **`ask`** = `send` plus a second lane: the **streamed** agent text must equal the **read-back**
  text for that turn. Disagreement → exit 50, both texts named on stderr, never silently picks
  one.
- **`steer`** = like send but `turn/steer` with `expectedTurnId = state.lastTurnId`.

Order that matters for recovery: state (`lastTurnId`) is saved **before** the 50 is raised. A 50
never loses the turn; `read` recovers it at zero cost. For the BUS this is the mechanism behind
"unknown completion is not a retry signal": timeout or 50 → `read` → decide; never re-send.

## 5. Explicit-enable gating vs enforcement of who may enable

**Does.** Every verb refuses (exit 10) when the state file is absent; `open --enable` is the sole
verb permitted to create it; without any state path at all every verb refuses (exit 13) and
creates nothing. Law 2.4 is a **presence** mechanism: no state file, no table.

**Does not.** It does not check **who** runs `open --enable`. There is no identity, token, or
operator proof; any process that can execute the shim with a state path can enable. "The
operator opens the table" is discipline plus the explicit-path rule. The one *mechanical* bypass
found — a pre-enabled vault travelling between hosts via git — is closed by `tunnel*.state.json`
in `.gitignore` and the untracking commit (`d2f8734`).

**Consequence for the Shuttle package:** the BUS primitive must be **instructed** never to run
`open --enable`, because the shim cannot distinguish BUS from operator. A transport success,
a preset, or a model reply grants no permission — but the shim will not stop a BUS that enables
itself; only its instruction contract will.

## What the package may claim after deploy, and what it may not

May claim: the six mechanisms above, with their stated limits; exit code 61; runtime stamping
after start/resume; close orphan-guard; selftest coverage of bind shape, lock, refusals.

May not claim until the hot run: that a bound thread honours anything in `state.sandbox`; that
`tun resume` against a thread an interactive client just released is clean (the writer-lock
note is the tell); that alternating TUI/tunnel ownership is safe over many cycles.
