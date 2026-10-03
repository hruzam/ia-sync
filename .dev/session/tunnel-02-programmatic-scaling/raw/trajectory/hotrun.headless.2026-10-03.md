# hot run — headless head, step ladder (operator runs, Trajectory navigates)

`driver: trajectory (office) · operator: majkee · date: 2026-10-03 · shim: BRICK-01 live, 89/89`
`shape: PAD-style — one step, report back, next step. Steps marked ⚡ spend ChatGPT quota.`
`head: a FRESH headless thread born by the tunnel (reading A). Cartan's interactive session is`
`NOT touched by this ladder — it exists to prove the mechanics without the writer-lock race.`

Report back after each ⚡ step: the stderr banner, the stdout tail, the exit code, and
`tun status` — verbatim, no paraphrase. If a step shows something other than "expect", STOP
and report; do not run the next step.

## Step 0 — vault + shell (free)

```zsh
cd ~/ia-sync
export TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.headless.state.json
tun status; echo "exit=$?"
```
expect: `refused — no state file … (Law 2.4, exit 10)`, exit=10. (The gate is armed.)

## Step 1 — open the table, deliberate identity (free)

```zsh
tun open --enable --cwd ~/ia-sync --sandbox read-only; echo "exit=$?"
tun status
```
expect: stderr `open: enabled (model=…, sandbox=read-only, cwd=/home/hruzam/ia-sync); no thread yet`,
exit=0. status: `"threadId": null`, `"cwd": "/home/hruzam/ia-sync"`, NO `runtime` block.
report: the model id the preflight stamped.

## Step 2 ⚡ — birth + first turn + runtime stamp

```zsh
tun ask "Reply with exactly the single word PONG and nothing else."; echo "exit=$?"
tun status
```
expect: stdout `PONG` then one line `[usage: {…}]`, exit=0. status now has `"threadId": "<id>"`
and a `runtime` block: `sandbox` (readOnly), `cwd` (/home/hruzam/ia-sync), `instructionSources`
(should name `/home/hruzam/ia-sync/AGENTS.md` — THIS is the identity proof), `observedAt`.
report: the threadId, the whole `runtime` block, the `[usage: …]` line.
if exit=50: streamed ≠ read-back — report both texts from stderr; do not retry.

## Step 3 ⚡ — continuity by vault (same thread remembers)

```zsh
tun send "What single word did I ask you to reply with in your previous turn? Answer with that word only."; echo "exit=$?"
```
expect: `PONG`, `[usage: …]` with `last.input_tokens` larger than step 2's. exit=0.
report: the usage line (we read occupancy from `last`, never `total`).

## Step 4 — inspection + re-stamp (free)

```zsh
tun read | jq '{turns: (.thread.turns|length), status: .thread.status}'
tun resume; echo "exit=$?"
tun status | jq .runtime
```
expect: turns ≥ 2; resume banner with `sandbox=… effort=… cwd=… instructionSources=[…]`;
`runtime.observedAt` newer than step 2's. NO "writer-lock present" note (nobody else holds it).

## Step 5 ⚡ — turn lock, live (two shells, or `&`)

```zsh
tun ask "Count from 1 to 15, one number per line, slowly." &   # shell A
sleep 2; tun send "x"; echo "exit=$?"                          # shell B, while A runs
wait
```
expect: shell B → `turn already in flight on this vault (pid …)`, **exit=61**, no second turn.
Shell A completes normally. report: both exits.

## Step 6 ⚡ — recovery drill (unknown completion ≠ retry)

```zsh
tun ask "Write 25 lines, each a different proverb." &
sleep 3; kill %1; wait 2>/dev/null       # kill the DRIVER mid-turn
ls ~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/*.lock 2>/dev/null   # expect: nothing
tun read | jq '.thread.turns[-1] | {status, completedAt}'
```
expect: last turn `status: "interrupted"`, `completedAt: null`; the turn lock is gone (released
in `finally`). report both. Do NOT re-send — this is the rule the BUS lives by.

## Step 7 ⚡ — close, then BIND to the thread we birthed (the Protocol 1 mechanic, race-free)

```zsh
tun status | jq -r .threadId        # copy it
tun close                            # expect: "releasing thread <id> … tun open --enable --thread <id>"
tun open --enable --thread <id> --cwd ~/ia-sync; echo "exit=$?"
tun resume; echo "exit=$?"           # expect runtime stamped, no writer-lock note
tun ask "Which word did I first ask you to say in this conversation?"; echo "exit=$?"
```
expect: close prints the re-bind command; bind banner `BOUND to existing thread <id>`; resume
clean; the answer is `PONG` — the thread's memory survived close → bind → resume.
report: exits + the answer. This step is what proves bind/resume/stamp on a real thread.

## Step 8 — leave it tidy (free)

```zsh
tun close
```
The thread stays server-side (`codex archive <id>` later if wanted). Ladder complete.

## What this ladder proves / does not

Proves: deliberate identity via `--cwd`; runtime stamping on birth and resume; vault
continuity; per-handle turn lock; interrupted-turn recovery; close→bind→resume on a real
thread. Does NOT prove: alternating ownership with an interactive client (the reading-C race)
— that needs Cartan's session and its own, later sitting.
