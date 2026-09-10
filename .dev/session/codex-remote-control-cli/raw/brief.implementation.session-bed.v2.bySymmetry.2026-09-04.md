---
brief: mobile-cli-session-bed
version: v2
date: 2026-09-04
lineage: brief.implementation.byAsymmetry.2026-09-04 (v1, kept verbatim below) → review by Symmetry (claude.ai) same day
status: reviewed · NOT built · phase 1 scope unchanged, hardening added
sovereignty: HIGH — tmux + SSH + Tailscale are vendor-neutral; one bed serves Codex and Claude Code
grep: #bed #session-bed #ptyra #remote-control #linger #forced-command
---

# PART A — original brief (Asymmetry, verbatim)

MOBILE CLI SESSION BED — implementation brief

GOAL

Provide a durable interactive Codex CLI session running on a workstation,
accessible from Android phone/tablet through Termux.

Architecture:

    voice
      ↓
 ChatGPT prompt-forge
 (Luna / Terra / disposable flat thread)
      ↓
 cleaned prompt
      ↓ clipboard
    Termux
      ↓
 Tailscale SSH
      ↓
 session-bed
      ↓
 tmux
      ↓
 Codex CLI
      ↓
 project filesystem / BUS / cold-start artifacts


PRINCIPLE

The mobile device is a lens, not the execution host.

The workstation owns:
- Codex process
- repository
- credentials
- filesystem state
- tmux session

Android owns only:
- SSH credentials
- terminal UI
- temporary clipboard text


IMPLEMENT

Create one small command:

    bed <name> [project]

Example:

    bed imago ~/www/imago

Behavior:

1. connect to target workstation over Tailscale SSH
2. find tmux session:
       agent-<name>
3. if session does not exist:
       create it
       cd to project
       launch Codex
4. if session exists:
       attach to the existing session
5. SSH disconnect MUST NOT terminate Codex
6. reconnecting from another device MUST reach the same session


OPTIONAL COMMANDS

    bed imago
        normal interactive attachment

    bed-list
        list living agent sessions

    bed-new imago ~/www/imago
        explicitly create session

    bed-kill imago
        deliberately terminate session

    bed-view imago
        observer mode / read-only where practical


HOST IMPLEMENTATION

Prefer Bash initially.

Dependencies:

    tmux
    openssh
    tailscale
    codex

Session naming convention:

    agent-<scope>

Examples:

    agent-imago
    agent-agentive
    agent-network

Do NOT tie identity to PID or terminal device.


ANDROID / TERMUX

Provide tiny wrappers.

Example conceptual use:

    imago

which resolves to:

    ssh <tailscale-host> 'session-bed attach imago'

Phone and Samsung tablet therefore expose the same living process.

Both may attach simultaneously if wanted.

tmux should remain the multiplexing authority.


SECURITY

SSH:
- key authentication only
- no password authentication
- host reachable through Tailnet
- do not expose SSH publicly merely for this feature

Do not copy:
- OpenAI credentials
- repository credentials
- project secrets

to Android unless independently required.

Codex authenticates and executes on workstation.


PROMPT-FORGE BOUNDARY

ChatGPT/Luna/Terra has NO authority over the CLI.

Its contract is only:

    noisy human intent
          ↓
    cleaned executable prompt

Output should preferably be:

- plain text
- no conversational prefix
- no Markdown decoration unless useful to Codex
- explicit objective
- relevant constraints
- requested stopping condition

Then operator deliberately copies the result into Termux.

Clipboard transfer is an intentional capability boundary.


DO NOT BUILD YET

Do not build:
- custom web terminal
- websocket proxy
- Android Codex runtime
- session database
- proprietary remote-control protocol
- synchronization daemon

tmux + SSH already solve process persistence and terminal transport.


PHASE 2, ONLY IF PAIN APPEARS

Possible additions:

- fuzzy bed selector
- session metadata
- project auto-detection
- BUS/cold-start card injection
- push notification when Codex needs operator input
- QR/deep-link for opening a named session
- Android shortcut/widget
- observer-only secondary tablet layout


SUCCESS TEST

Start Codex from workstation.

Attach from phone.

Send prompt.

Lock phone / lose network.

Codex continues running.

Attach from Samsung tablet.

See exactly the same CLI state.

Send another prompt.

Detach tablet.

Reconnect from phone.

Nothing has been restarted or reconstructed.

PASS.


# PART B — review (Symmetry, 2026-09-04)

Verdict: brief is sound. tmux + SSH is the correct floor; the DO NOT BUILD
list is the strongest part. Nothing below changes phase 1 scope; it hardens it.

## B1. Reframe — what the bed is FOR (#remote-control)

Since v1 was written, both vendors ship native remote control:

- Codex: `codex remote-control` (CLI/app-server on Linux works) pairs the
  workstation to the ChatGPT mobile app; sessions can be opened and driven
  from the phone. Enrollment goes through chatgpt.com backend and is
  account-policy gated (fails without MFA enabled).
- Claude Code: `/rc` pairs a session to the Claude mobile app.

So the bed is NOT a capability gap anymore. It is a sovereignty choice:

- own transport (Tailnet), no relay through a vendor backend
- one bed for both vendors — `agent-<scope>` does not care what runs inside
- no account-policy dependency on the control path
- observer mode, multi-device, and kill are ours, not the vendor's roadmap

Consequence for PHASE 2: "pain" now means pain the native remote control
does NOT already solve. If a phase-2 item is just re-implementing vendor
remote control over our transport, the honest move is to use the vendor
feature for that case and keep the bed as the neutral floor.

## B2. Findings, by risk

1. #linger — tmux does NOT guarantee persistence alone. On systemd distros
   with `KillUserProcesses=yes` in logind.conf, the tmux server dies on SSH
   logout. Step 0 of host setup: `loginctl enable-linger <user>`. Add to
   SUCCESS TEST as a precondition, otherwise the test passes on one distro
   and fails silently on another.

2. "Tailscale SSH" is ambiguous: Tailscale's own SSH server (identity-based,
   no keys) vs OpenSSH over the Tailnet (keys). v1 says "key auth only",
   which implies OpenSSH. State it explicitly; hardening differs.

3. #forced-command — the phone key is the weakest link (lost phone).
   Restrict it in `authorized_keys`:

       command="session-bed $SSH_ORIGINAL_COMMAND",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty-if-not-needed ssh-ed25519 AAAA...

   (drop the pty restriction; attach needs a pty — keep the rest). The
   phone key can then only reach bed operations, never a shell. Cheap;
   belongs in phase 1.

4. Create-or-attach atomically:

       tmux new-session -A -s "agent-$name" -c "$project" -- codex

   resolves steps 3+4 of IMPLEMENT and the two-devices-racing case.
   Validate `$name` against `^[a-z0-9-]+$` and quote everything — it flows
   through `ssh host 'session-bed attach ...'`, so it is an injection
   surface.

5. `[project]` is only meaningful on create. If the session exists and a
   different path is passed, v1 silently attaches to the wrong project.
   Warn (or refuse) on mismatch.

6. `bed-kill` as `tmux kill-session` kills Codex mid-write. Graceful first:
   send `/quit` (or C-c), wait, then kill. Related: tmux server death
   (reboot) loses the running conversation but NOT the transcript —
   Codex saves sessions as JSONL under `~/.codex/sessions/` and offers
   `codex resume --last` / `codex resume <id>`. Decide whether cold-create
   should offer resume; cheap win for the "nothing reconstructed" test.

7. Multi-line clipboard paste: test early — Termux paste → tmux → Codex TUI.
   Bracketed paste usually works; a stray Enter submits a half-prompt.
   Fallback: `tmux load-buffer` / `paste-buffer` from a file.

8. Simultaneous attach: tmux resizes to the smallest client by default;
   set `window-size latest` or the tablet gets a phone-sized view.
   Observer mode is free: `tmux attach -r -t agent-<name>`.

9. Codex approval mode on a phone screen: small screens tempt
   `--dangerously-bypass-approvals-and-sandbox`. Keep sandbox + approvals
   on. That is the real safety gate; SSH hardening only protects transport.

10. Network flakiness: mosh over Tailscale reconnects far better than SSH.
    Correctly phase 2.

## B3. Ptyra deltas (prompt-forge side)

- Release check item 7: "Did I carry a stopping condition?" — the brief
  requires one; Ptyra's contract never mentions it.
- Secrets rule: voice may carry tokens/passwords read aloud. Ptyra strips
  them and says so. The clipboard boundary is a capability boundary, not a
  secret boundary.
- Authority tag: optionally prefix released prompts with the gradient
  level (`[inspect]`, `[implement]`) so the operator sees the ceiling
  before pasting. Costs three tokens, removes one class of silent escalation.

## B4. Research notes (life hacks found, not adopted)

- tmux + ttyd + Tailscale HTTPS: existing open-source wrappers give a
  browser terminal on the Tailnet with systemd autostart. Equivalent to
  the bed with a web lens instead of Termux. Phase-2 candidate only;
  adds a listening web service.
- happy-cli / Agents-Anywhere: self-hosted control planes for Codex and
  Claude Code with mobile UI and resume-by-id. Richer than needed;
  exactly the "custom web terminal / proxy" the DO NOT BUILD list rejects.
- Codex session storage: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
  plus sqlite metadata. Useful for a future `bed-list` that shows the last
  thread title per bed. Not phase 1.

## B5. Amended SUCCESS TEST

Precondition: `loginctl show-user <user> | grep Linger=yes`.
Then v1 test unchanged, plus:

- reboot workstation → `bed imago` → offered resume of last thread → PASS
- attempt `ssh host` with the phone key alone → shell denied → PASS
- `bed-view imago` from tablet while phone drives → tablet cannot type → PASS

## Brake

No build before the linger check and the forced-command line are in the
host setup. One mountain: phase 1 only.
