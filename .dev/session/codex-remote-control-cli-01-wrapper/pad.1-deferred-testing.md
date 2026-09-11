# pad.1-deferred-testing — the remote-cli surface, walked by hand

> Operator test surface. Sequential — one step, report back, next step.
> Driver: @Vara (sequential walker, live session — this sitting doubles as Vara's own
> field test). Protocol: driver reveals ONE step, waits for the report fence to fill,
> branches on the verdict; REFUTED/BLOCKED → flag the head (@Trajectory), never
> re-classify or improvise a fix mid-pad.

## Driver rules (read before step 0, every sitting)

1. One step, then wait. Never run ahead, never dump the rest.
2. Every command is copy-pasteable — absolute paths, no assumed cd, say WHERE it runs
   (home terminal / office terminal / phone Termux / phone app).
3. Errors are evidence — paste them whole into the report fence, read bottom-up.
4. Off-pad questions: answer in one breath, park big ones under `## parked`.
5. This PAD is its own raw log — reports live HERE, distilled verdicts graduate once,
   to the session evidence (head's job, not mid-run).

## Shared constants

```
session folder : /home/hruzam/ia-sync/.dev/session/codex-remote-control-cli-01-wrapper
office         : hruzam-120922 · 100.126.182.111
home           : hruzam · 100.110.27.60
guide          : /guide remote-cli   (the idiot-proof command map)
```

## Precondition

Home has pulled ia-sync ≥ `561e324` and copied the two zsh files live (the finishing
block from 2026-09-10). If unsure, STEP 0 catches it.

### STEP 0 — state check (read-only, run in HOME terminal)

```bash
tailscale status | grep -E "hruzam-120922|redmi" ; ssh hruzam@100.126.182.111 '/usr/bin/tmux list-windows -t agentive' ; grep -c -- '--bed' ~/.config/zsh/system/tailscale.zsh
```

Expected: office + (maybe) redmi rows · a window list · final line `1`.

- all three present → `SUPPORTED`, proceed
- `grep` prints `0` → home not deployed: run the finishing block from the 2026-09-10
  chat (pull + cp + source), rerun STEP 0
- ssh fails → `BLOCKED`, flag the head

>MAJKEE report 0
```zsh

```

### STEP 1 — C3 both-doors (office claude, two doors, one session)

In HOME terminal: `tso -t office` → you land on a shell seat. `Ctrl+b 1` → a claude TUI
should be running (if seat 1 is empty: run `~/.local/bin/claude` there, wait for the
prompt). Then open the **Claude mobile app** on the Redmi → the office session should be
listed/reachable.

- TUI visible in terminal AND session visible in app → `SUPPORTED` (C3 closes — tell
  the head, STATUS gets the evidence pointer)
- app does not show it → inside the TUI type `/remote-control` (rebinds the ONE cloud
  seat), recheck app; still nothing → `REFUTED`, paste what the app shows
- `Ctrl+b d` to leave; claude keeps running

>MAJKEE report 1
```zsh

```

### STEP 2 — pc→pc maiden voyage, home → office door

HOME terminal, fresh shell:

```bash
tso -t office
```

Expected: `connecting → office (bed)` · ping line · you land on a PLAIN SHELL seat
(never inside a TUI), glyphs and colors correct.

- shell seat + clean glyphs → `SUPPORTED`; type `exit`? NO — `Ctrl+b d` to detach
- landed inside a TUI → `REFUTED` (door defect), note which window
- bricks/flat colors → `REFUTED` (locale), paste the prompt line

>MAJKEE report 2
```zsh

```

### STEP 3 — reverse lane, office → home door

In the OFFICE shell you reached in step 2 (or any office terminal):

```bash
tso -t home
```

Expected: bed door on home, shell seat, correct glyphs (home bed was UTF-8-reseeded
2026-09-10).

- same as step 2 branches. `Ctrl+b d` twice unwinds both hops.

>MAJKEE report 3
```zsh

```

### STEP 4 — phone: reattach + seat-hop + the voice-loop rehearsal

On the Redmi: copy any short text in the notes app (stand-in for a PTYRA output) →
Termux → `bed office` (no passphrase expected — agent holds it since last boot) →
tap `S2` (shell seat) → tap `PASTE` → the copied text appears on the prompt → `S1`
hops to claude → `DETACH` leaves.

- all four gestures land → `SUPPORTED` (voice loop = proven end-to-end minus PTYRA voice)
- passphrase asked again → note it (phone rebooted since? once-per-boot is the law);
  asked WITHOUT reboot → `REFUTED`
- PASTE empty → check Termux clipboard permission, retry once, else `REFUTED`

>MAJKEE report 4
```zsh

```

### STEP 5 — Termux:Widget (one-tap from home screen)

On the Redmi: install **Termux:Widget** from F-Droid (MUST be same install source as
Termux itself). Add the Termux widget to the home screen → it lists `office-attach` /
`home-attach` → tap `office-attach`.

- lands in the office bed → `SUPPORTED` (the pocket door is now one tap)
- scripts not listed → `ls ~/.shortcuts/` in Termux, paste output, `REFUTED`
- skipped for now → write `DEFERRED`, proceed (not a blocker)

>MAJKEE report 5
```zsh

```

### STEP 6 — decision gate: phone enters through the door?

No command — a choice. Current: phone lands on last-active seat (good for
reattach-to-work). Swap = phone lands on a shell seat like `tso -t` (good for
arrive-and-choose; `Ctrl+b l` returns to work). Swap is YOUR paste on BOTH PCs —
in the redmi line of `~/.ssh/authorized_keys`, replace only the command= part with:
`command="sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door"`.

- record: `SWAPPED (both PCs)` / `SWAPPED (office only)` / `DEFERRED AGAIN`

>MAJKEE report 6
```zsh

```

### STEP 7 — cleanup gate (DESTRUCTIVE — only when 0–4 all SUPPORTED)

The rotation is trusted once steps 0–4 pass. Then, and only then:

```bash
ssh -p 8022 hruzam@100.105.201.3 'rm ~/.ssh/id_ed25519.old ~/.ssh/id_ed25519.pub.old'
rm ~/.ssh/authorized_keys.pre-rotation-2026-09-10
ssh hruzam@100.126.182.111 'rm ~/.ssh/authorized_keys.pre-rotation-2026-09-10'
```

(run from HOME terminal; middle line cleans home, last cleans office)

- three clean removals → `SUPPORTED` — rotation debt is zero
- any step 0–4 not SUPPORTED → DO NOT RUN, write `HELD`

>MAJKEE report 7
```zsh

```

## Verdict map

| step | proves | SUPPORTED when | REFUTED when |
|---|---|---|---|
| 0 | deploy parity | flag live on home | grep 0 / ssh dead |
| 1 | C3 both doors | TUI + app see one session | app blind after rebind |
| 2 | door, home→office | shell seat, clean glyphs | TUI ambush / bricks |
| 3 | door, office→home | same, reverse | same |
| 4 | phone loop + agent | 4 gestures, no passphrase | re-prompt, empty paste |
| 5 | one-tap widget | tap → bed | scripts missing |
| 6 | phone-door choice | recorded either way | — (decision, not test) |
| 7 | rotation closure | 3 removals | — (gated, not refutable) |

## Muscle-memory drills (repeat freely — NO verdict, build the reflex)

Not tests — reps. Run each a few times until the keys are in your hands. Duplication
with the steps above is intentional. Model behind it: /guide remote-cli §"one session,
many seats, many views" — more agents = more WINDOWS, never more sessions.

### Drill 0 — SEE what's alive (do this first, tmux is new)
```
tso office             # plain shell on office (no bed take-over)
tmux ls                # which beds exist + seat count   → proof line
tmux list-windows -t agentive   # each seat + what runs in it (claude? codex? shell?)
exit                   # leave the plain shell
```
Then attach and look from inside:
```
tso -t office
#   Ctrl+b w           # VISUAL list of every seat + what's running — arrow, Enter
#   read the green bar bottom: [agentive] 1:claude*  = bed·seat·current(*)
#   Ctrl+b d           # leave
```
Reflex to build: **`Ctrl+b w` = "show me everything running, let me pick."** That one
key answers "what do I have and where is it." (This is the exact command that proved
two claudes were alive — /guide remote-cli §"what's alive?".)

### Drill A — computer host ⇄ host (the tso -t reflex)
```
tso -t office          # home terminal → office bed, shell seat
#   Ctrl+b c           #   new seat (window)
#   claude   …or codex #   run an agent there — it will OUTLIVE this connection
#   Ctrl+b 1 / 2 / …   #   hop between seats (each its own live agent)
#   Ctrl+b w           #   pick a seat from a list
#   Ctrl+b d           #   detach — everything keeps running
tso -t home            # same, other host; a future PC = tso -t <its-name>
```
Reflex to build: **Ctrl+b c to make a seat · Ctrl+b <n> to hop · Ctrl+b d to leave.**

### Drill B — mobile: make the session on the computer, reach it two ways
Two doors to ONE bed. Start the agent from a computer (or the phone), then reach it:
```
# --- Claude, via the APP door (no Termux needed) ---
#   on any computer, inside the office bed:  ~/.local/bin/claude
#   inside it once:  /remote-control          # binds the ONE cloud seat
#   phone: open the Claude mobile app → the session is there. (last claimer wins)

# --- Codex (or Claude), via the TERMUX door ---
#   phone Termux:  bed office                  # into the bed
#   Ctrl+b <n> to the seat, or Ctrl+b c for a new one
#   codex        …or ~/.local/bin/claude       # runs on office, you drive from the phone
#   S1–S4 buttons hop seats · PASTE = clipboard/voice · DETACH leaves
```
Reflex to build: **Claude has an app door (`/remote-control`); Codex does not — reach it
through the Termux bed.** Same bed either way; the agent lives on the computer.

## parked

- (driver appends off-pad questions here; head sweeps at close)
