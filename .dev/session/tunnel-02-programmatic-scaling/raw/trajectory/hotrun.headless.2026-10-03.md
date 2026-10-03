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

## Variant B — TUI-born, briefed, released, then bound (majkee's proposal, adopted 2026-10-03)

Replaces Steps 1–2 above. The head is born in the interactive TUI with a little history —
Protocol 1's real condition — then released and bound through the tunnel. Disposable thread;
Cartan's session is never touched. This variant ALSO tests what the headless ladder cannot:
whether a just-released TUI thread resumes clean or shows writer-lock residue.

```zsh
# B1 (TUI, free of tunnel quota) — birth + brief, then RELEASE
cd ~/ia-sync && codex                       # interactive; cwd = repo root so AGENTS.md loads
#   give it 2–3 short turns: "you are a disposable test head for the tunnel; remember the word
#   KESTREL; reply OK"  … then one more turn of anything … then EXIT the TUI (this is the release)

# B2 — find the thread you just made (newest rollout today; the trailing UUID is the id)
ls -t ~/.codex/sessions/$(date +%Y/%m/%d)/rollout-*.jsonl | head -1
ls ~/.codex/thread-writer-locks/ | grep -c "<id>"      # 0 = released clean · 1 = residue (report it; do NOT remove)

# B3 — bind through the tunnel (free)
export TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/tunnel-02-programmatic-scaling/tunnel.test.state.json
cd ~/ia-sync && tun open --enable --thread <id> --cwd ~/ia-sync; echo "exit=$?"
tun status            # expect threadId, bound:true, cwd; NO runtime block yet

# B4 ⚡ — resume = the liveness probe on a thread born elsewhere
tun resume; echo "exit=$?"
#   expect: banner with sandbox=… effort=… cwd=/home/hruzam/ia-sync instructionSources=[…AGENTS.md…]
#   if "NOTE — Codex writer-lock present" appears: report it — that is the finding, not a failure
tun status | jq .runtime

# B5 ⚡ — memory born in the TUI survives the tunnel
tun ask "What word did I ask you to remember? Reply with that word only."; echo "exit=$?"
#   expect: KESTREL  + [usage: …]

# then continue with Steps 4 (read/resume), 5 (turn lock), 6 (recovery) above on this thread,
# and finally B6: reopen the TUI —  codex resume <id>  — and confirm the tunnel's turns are
# visible there. That is the alternating-ownership proof, on a thread nobody needs.
```

### Variant B — sitting 1 results (majkee, office, 2026-10-03 ~12:55 CEST)

- B1: TUI born at `cd ~/ia-sync && codex --model gpt-5.6-terra`, briefed, exited. Thread
  `01a10144-a173-7020-b1f3-d33f5fff7606` (rollout 12:17:17).
- B2: lock grep returned 0 — **invalid** (searched the literal `<id>`; placeholder not
  substituted). Superseded by B3's shim note.
- B3: `open --enable --thread … --cwd ~/ia-sync` → **writer-lock NOTE fired** (lock present after
  a clean TUI exit), then bound, exit 0. Re-target → exit 11 ✓. `status`: threadId · bound ·
  cwd · `model: gpt-6.1-sol` (account default, intent only) · no `runtime` block ✓.

**FINDING F-B3 — the Codex writer-lock persists after a TUI exit.** A TUI-born head carries
residue on every bind, so the stderr note is NOT a held-vs-released discriminator. Warn-only
was the right call: a refusing shim could never bind a TUI-born head. Whether Codex *enforces*
the lock on `thread/resume` is B4's question.

**Live demonstration of the two-layer rule:** state.model says sol (preflight default),
the thread is terra. B4's `runtime.model` must say terra.

### B4 result (~13:13 CEST) — outcome A

`tun resume` → exit 0. `runtime`: model **gpt-5.6-terra** (truth ≠ sol intent ✓) ·
sandbox **workspaceWrite** writableRoots [] network false (≠ read-only intent ✓) · effort max ·
approvalPolicy **on-request** · cwd /home/hruzam/ia-sync · instructionSources
[`~/.codex/AGENTS.md`, `~/ia-sync/AGENTS.md`] (identity proof ✓).

- **F-B4a** — resume succeeded despite the writer-lock: Codex does not enforce it on
  `thread/resume` once the TUI has exited. F-B3 = residue, confirmed.
- **F-B4b** — in a second terminal `tun resume` → exit 13: `TUNNEL_CODEX_STATE` is per shell;
  no-global-default refused rather than guessed. Correct, and worth seeing once.
- **F-B4c** — ladder bug: `tun status | jq .runtime` is wrong (status → stderr). Use
  `jq .runtime "$TUNNEL_CODEX_STATE"`. Fixed in guide + here.
- **F-B4d** — a TUI-born head carries `approvalPolicy: on-request`. Through the tunnel a
  write-requesting turn will stall on an approval nobody answers. Questions are fine; write
  tasks on a bound TUI head are a limit until the RUNBOOK decides who answers.
- Open: whether the resume cleared the residue lock (the NOTE did not reprint in the paste).
  Check with the real id: `ls ~/.codex/thread-writer-locks/ | grep -c 01a10144`.

### B5 result — PASS

`tun ask "What word did I ask you to remember? …"` → stdout **`KESTREL`**. Memory born in
the TUI survived release → bind → resume → tunnel turn: the Protocol 1 mechanic, proven on a
real thread. (usage line / exit not pasted; thread state confirmed by the answer.)

- **F-B5** — writer-lock count after resume+ask: **0**. Codex clears the previous holder's
  residue when a new client resumes; the tunnel's per-verb app-server leaves no lock behind.
  Lifecycle: TUI exit → residue → first tunnel contact clears it → clean. The NOTE fires once
  per handover, not forever — so it IS a usable tell for "a TUI held this since my last turn".
- Operator note: bare `tun read` floods the terminal (raw JSON by contract, stdout). Guide
  gloss now carries the two jq filters. Not a defect.

### B6 result — PASS, and one cycle beyond the ladder

`codex resume 01a10144-…` in the TUI showed the tunnel's KESTREL Q/A. Majkee then **briefed
further in the TUI, asked about that new material through `tun ask`, got a correct answer
against the full thread history, and saw those tunnel questions in the TUI afterwards** —
a second TUI→tunnel→TUI alternation. After exiting the TUI: lock count **1** (F-B3
reproduced; lifecycle symmetric: each TUI visit leaves residue, the next tunnel contact
clears it).

- **F-B6 (needs one clarification):** whether the TUI was still *open* during the second
  `tun ask`. Majkee's wording ("living TUI") suggests yes. If so: one observed instance of a
  tunnel turn succeeding while a TUI was attached, with the TUI subsequently displaying it.
  Recorded as **observed once, unverified as safe** — it does NOT lift the alternate-never-
  overlap rule; it is evidence for a deliberate later sitting on overlap tolerance for
  read-only turns. If the TUI was closed: plain second alternation, rule untouched.

### Sitting 1 — verdict (operator-run, Trajectory-navigated, office, 2026-10-03)

PROVEN on a real TUI-born thread: bind without server contact · deliberate identity via
`--cwd` (both AGENTS.md loaded) · runtime stamping that exposes model/sandbox/effort/
approval truth over bound intent · memory across release→bind→resume→turn · TUI↔tunnel
alternation (two cycles) · writer-lock lifecycle (residue per TUI visit, cleared by next
tunnel contact; not enforced on resume) · per-shell state path refusal (exit 13) · re-target
refusal (exit 11).
NOT run (second sitting): step 5 turn-lock live (exit 61 on a real in-flight turn) · step 6
interrupt + `tun read` recovery · F-B6 overlap clarification.
Quota spent: 2 turns (B5 + the extra ask).

## What this ladder proves / does not

Proves: deliberate identity via `--cwd`; runtime stamping on birth and resume; vault
continuity; per-handle turn lock; interrupted-turn recovery; close→bind→resume on a real
thread. Does NOT prove: alternating ownership with an interactive client (the reading-C race)
— that needs Cartan's session and its own, later sitting.
