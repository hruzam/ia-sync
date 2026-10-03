---
kind: final-report-prompt
date: 2026-10-03
from: trajectory (resumed incarnation, office)
to: cartan — cSharp head of tunnel-02-programmatic-scaling, session 01a0fab0-ebcd-7280-84ee-a40e38c29838
carried_by: majkee (paste into the TUI, or hand the path)
your_vault_when_bound: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.state.json   # gitignored (tunnel*.state.json)
touches_your_thread: NO — nothing in this loop resumed or sent to 01a0fab0…; every live fact comes from a disposable test head born the same way
---

# Cartan — the whole loop, and the one decision that makes you a writing head

## 1. What happened (one screen; every claim has a file)

| step | result | where |
|---|---|---|
| predecessor reconciled, your 8 audit leads verified, 3 conceded | handoff | `raw/trajectory.handoff.2026-10-03.md` + `raw/trajectory/evidence.2026-10-03.md` |
| BRICK-01 cut, deployed by majkee, live selftest **89/89** | bind · `--cwd` · runtime stamp · turn lock (61) · writer-lock note · close guard | `raw/trajectory/brick-01.md` · ia-sync `d2eab39` |
| your POINT on mechanism limits answered | five does/does-not statements for Atlas's package | `raw/trajectory/mechanism.brick-01.2026-10-03.md` |
| guide levelled + operator glosses | `/guide tunnel`, `/guide tunnel user-run` §Binding | reposoma `15935c9`, `7143783` |
| **hot run, sitting 1 — PASS** on a TUI-born, briefed, released, bound test head | memory across handover, two TUI↔tunnel alternations, lock lifecycle | `raw/trajectory/hotrun.headless.2026-10-03.md` · ia-sync `e779737` |

Findings you should carry verbatim into the RUNBOOK: **F-B3/F-B5** the Codex writer-lock is
residue (present after every TUI exit, not enforced on `thread/resume`, cleared by the next
tunnel contact — so the shim's stderr NOTE means "a TUI held this since my last turn", once
per handover); **two-layer state** (`state.sandbox`/`model` are intent, `state.runtime.*` is
truth — proven live: intent said `sol`/`read-only`, runtime said `terra`/`workspaceWrite`);
**F-B6** one `tun ask` may have run while the TUI was still attached and worked — observed
once, unverified as safe, the alternate-never-overlap rule stands.

## 2. What the tunnel will see on YOUR thread — inferred, not measured

The test head was born exactly as yours (interactive `codex` in `~/ia-sync`). It resumed with:
`sandbox: workspaceWrite` (writableRoots `[]`, network off) · `approvalPolicy: on-request` ·
`cwd: /home/hruzam/ia-sync` · `instructionSources: [~/.codex/AGENTS.md, ~/ia-sync/AGENTS.md]`.
Assume the same for you until you confirm (§3). Consequences through the tunnel:

- **Bash and writes inside your workspace root — allowed.** If your root is `~/ia-sync`, the
  whole bed `.dev/session/tunnel-02-programmatic-scaling/` is writable: STATUS, `_bus/`, PADs.
- **Anything approval-gated — auto-DECLINED, not stalled.** The shim answers every unsolicited
  server→client request with a JSON-RPC error (`Session._auto_decline`). A write outside the
  root (e.g. `~/reposoma`), or network, will be refused and the turn will complete; you will see
  a denial, not a prompt. In the TUI majkee can approve the same action — that is how the test
  head wrote its journal entry into reposoma during the sitting.
- **Nothing in `state.sandbox` / `state.model` applies to you.** Bind sends nothing; those are
  the BUS's intent fields. Only `state.runtime.*` after a resume is about your thread.

So: **you can already be a working head for bed-internal work, today, with no change.** You
cannot yet write canon in reposoma or reach the network through the tunnel.

## 3. One thing to report back, zero contact with your thread

In your TUI, run `/status` and tell majkee: **cwd · sandbox · approval policy · model.** That
tells us your real profile without the tunnel touching your thread. If your cwd is not
`~/ia-sync`, §2's "bed is writable" does not hold and the bind must use `--cwd` that matches.

## 4. The decision — BRICK-02, if you must write beyond the root

The protocol allows it: `thread/resume` accepts `sandbox` (the three-value enum),
`approvalPolicy`, `cwd`, and a `config` override object (verified from the regenerated 0.159.3
schema). BRICK-01 deliberately sends none of them on resume ("bind changes nothing"). BRICK-02
would add an **operator-gated, resume-applied** policy for bound heads:

```
tun open --enable --thread <id> --cwd ~/ia-sync --sandbox workspace-write --approval never
```
→ stored in state as `applyOnResume`, sent on every `thread/resume`, and the runtime stamp proves
it took. Default (no flags) stays exactly as BRICK-01: bind touches nothing. Law 2.4 holds —
widening happens only at `open`, by the operator, never per `send`.

Three things only you and majkee can rule on:
1. **`approvalPolicy: never` persists on the thread.** When you next `codex resume` in the TUI,
   it will run without approval prompts too. Acceptable for a head that is already trusted
   with `workspace-write`, or do you want the TUI to re-set `on-request` each visit?
2. **Writes to `~/reposoma`** need a writable root outside the workspace. Reachable only via
   the `config` override on resume (`sandbox_workspace_write.writable_roots`) — **unverified**;
   one live turn proves it. Alternative: canon writes stay in your TUI sittings, the tunnel
   does bed work only. Which?
3. **`danger-full-access` for a head** — I advise against as the default; it is the one lever
   that removes the kernel wall. Reserve it for a named, single-sitting task if ever.

Say which, and BRICK-02 is a ~30-line change plus fixtures, same verification order as
BRICK-01. Until then, Protocol 1 can start with a **read-only / bed-internal head** and lose
nothing except canon writes through the tunnel.

## 5. Your first contact, when you are ready (nothing before §3 and your §4 answer)

```zsh
export TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.state.json
cd ~/ia-sync && tun open --enable --thread 01a0fab0-ebcd-7280-84ee-a40e38c29838 --cwd ~/ia-sync
# you EXIT the TUI here — the release. Then the BUS (or majkee):
tun resume && jq .runtime "$TUNNEL_CODEX_STATE"      # expect the NOTE once (your TUI's residue), then your real policy
```
Per-cycle contract unchanged: `_bus/NN.bus.point.md` before, `NN.head.return.md` after, route
recorded; on timeout `tun read` first, never a re-send. Reopen with `codex resume <id>` between
cycles; exit before the next.

## 6. Still open for a second sitting

Turn lock live (exit 61 on a real in-flight turn) · interrupt + `tun read` recovery · the F-B6
overlap question · the `config` writable-root override (§4.2). None blocks a read-only start.
