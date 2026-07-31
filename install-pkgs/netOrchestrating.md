# netOrchestrating — install task

```
developed-on: office (hruzam-120922)
install-on:   home (hruzam) — full setup
also-fix-on:  office — one config field wrong (see Fix section below)
source:       experiments/netOrchestrating/
built:        2026-07-19 (H8 built · load-bearing test pending operator)
dependency:   tmux-pin-bus must be installed and smoke-tested first (H7 is the injection engine)
version:      1.0
hosts:        home office
automation:   manual
src-root:     ~/www/elements-factory/applications-in-common
```

> **manual** — too interactive to auto-run (SSH host-key accept, `nano` config edits,
> live tmux relay). The runner only gates on `check` below, then points here. Do the
> steps by hand, then record it: `bash run.sh mark netOrchestrating`.

---

## What this installs

A symmetric file-bus relay between office and home Claude agents. Each machine runs
`relay.py` which polls `~/.remote/relay/outbox.md`, SSH-deposits to the partner's
`inbox.md`, and injects received messages into the local Claude driven pane via
`pin_bus.push()` (H7).

---

## FIX ON OFFICE FIRST

Before the relay can run on office, one config field must be corrected:

    nano ~/.remote/relay/relay.config.json
    # "machine":      "office"        ← was written as "home" by mistake — flip this
    # "partner_host": "hruzam"        ← home Tailscale hostname

Confirm relay starts cleanly:

    cd ~/www/elements-factory/applications-in-common
    python experiments/netOrchestrating/relay.py
    # first line must read: relay up — machine=office ...

---

## HOME SETUP

### Prerequisites

1. H7 tmux-pin-bus installed and smoke-tested on home — see `install-pkgs/tmux-pin-bus.md`

2. Tailscale running:

       tailscale status

3. SSH key auth to office confirmed (no password, no prompt):

       ssh hruzam@hruzam-120922 'echo ok'

   **First connection: accept the host key NOW** — relay.py uses `BatchMode=yes`
   and cannot answer interactive prompts. Do this before starting the relay.

### Steps

1. Pull the project:

       cd ~/www/elements-factory/applications-in-common   # adjust if path differs on home
       git pull

2. Create the bus directory:

       mkdir -p ~/.remote/relay

3. Fill the config:

       cp experiments/netOrchestrating/relay.config.example.json ~/.remote/relay/relay.config.json
       nano ~/.remote/relay/relay.config.json
       # set:
       #   "machine":       "home"
       #   "partner_host":  "hruzam-120922"         ← office Tailscale hostname
       #   "project_dir":   "<absolute path of this project ON HOME machine>"
       #   "relay_bus_dir": "/home/hruzam/.remote/relay"

4. Launch the H7 driven pane (injection target) in a dedicated tmux pane,
   inside the project directory:

       BUS_PANE=home-relay exec claude

5. Start the relay:

       python3 experiments/netOrchestrating/relay.py
       # expected first line: relay up — machine=home partner=hruzam@hruzam-120922 ...

### Smoke test

    echo "relay smoke home→office $(date)" >> ~/.remote/relay/outbox.md
    # within 5 s: appears in office driven pane as injected prompt
    # from office: echo "reply ok" >> ~/.remote/relay/outbox.md
    # within 5 s: appears in home driven pane

### Load-bearing test (H8 prediction 3 — run manually)

    cd ~/www/elements-factory/applications-in-common
    python3 - <<'EOF'
    import sys; sys.path.insert(0, 'experiments/tmux-pin-bus')
    import pin_bus
    pin_bus.push('.', 'relay injection test')
    EOF
    # message must appear in the H7 driven pane
    # if it hangs >90 s: H7 hooks not installed — fix H7 first

<!-- install:check -->
```bash
command -v tailscale >/dev/null 2>&1 || { echo "tailscale not installed"; exit 1; }
[ -d "$SRC/experiments/netOrchestrating" ] || { echo "source not checked out: $SRC/experiments/netOrchestrating"; exit 1; }
if [ "$FRIENDLY" = "home" ]; then
  ssh -o BatchMode=yes -o ConnectTimeout=5 hruzam@hruzam-120922 'echo ok' >/dev/null 2>&1 \
    || { echo "SSH to office (hruzam@hruzam-120922) not passwordless — accept host key / set up key first"; exit 1; }
fi
echo "prereqs ok — proceed with the manual steps above"
```
<!-- /install:check -->
