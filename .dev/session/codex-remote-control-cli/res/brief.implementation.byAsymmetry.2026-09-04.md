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