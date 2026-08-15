---
name: rc-launch
description: >
  Invoke as /rc-launch. Spins up a Claude Code remote-control session on a named host
  from anywhere (phone-friendly). Gathers {host, project, agent, model, effort}: host +
  agent + project are required (I ask if missing); model + effort default from the
  registry. Resolves the project path, checks the host is reachable, then dispatches the
  tmux-backed engine (ai/rc.sh) locally or over tailscale ssh. Use when the operator says
  "launch <agent> on <project> at <host>" or wants a catchable RC session started.
---

When /rc-launch is active I turn a launch request into a running, catchable remote-control
session. I am the resolution + dispatch front over the engine `~/.config/zsh/ai/rc.sh`;
the engine holds the session in tmux and prints the reach lines. I never hold the session
myself.

## Registries I read (deployed paths)

- `~/.config/zsh/registries/hosts.json`    — host-label → tailscale identity + locality
- `~/.config/zsh/registries/projects.json` — project → physical path (authoritative)
- `~/.config/zsh/registries/ai.json`       — `.remote-control.launch-defaults` (model, effort, per-project agent)

## The five parameters

`{ host, project, agent, model, effort }`

- **host** — REQUIRED. If the operator did not name one, I ASK (offering the labels from `hosts.json`).
- **project** — REQUIRED. If missing, I ASK (offering `projects.json` keys).
- **agent** — REQUIRED. If missing, I check the per-project default in `ai.json`; if there is none, I ASK "which agent?".
- **model** — optional. Omit and the engine defaults it (`launch-defaults.model`, currently `opus`).
- **effort** — optional. Omit and the engine defaults it (`launch-defaults.effort`, currently `high`).

## Procedure

1. **Parse** the operator's request into the five params. Do not invent a host or agent — those are required; ask.

2. **Validate project**:
   ```bash
   jq -e --arg p "$PROJECT" '.projects[$p]' ~/.config/zsh/registries/projects.json >/dev/null \
     || jq -e --arg p "$PROJECT" '."remote-control".projects[$p]' ~/.config/zsh/registries/ai.json >/dev/null
   ```
   If neither matches: show `jq -r '.projects|keys|join(", ")' projects.json` and ask the operator to pick.

3. **Resolve host** from `hosts.json`:
   ```bash
   HJSON=~/.config/zsh/registries/hosts.json
   MACHINE_NAME_OF_HOST=$(jq -r --arg h "$HOST" '.hosts[$h].machine_name // empty' "$HJSON")
   TS_DNS=$(jq -r --arg h "$HOST" '.hosts[$h].tailscale_dns // empty' "$HJSON")
   SSH_USER=$(jq -r --arg h "$HOST" '.hosts[$h].ssh_user // "'"$USER"'"' "$HJSON")
   HOST_HN=$(jq -r --arg h "$HOST" '.hosts[$h].hostname // empty' "$HJSON")
   ```
   If `$HOST` is not a key: show `jq -r '.hosts|keys' "$HJSON"` and ask.

4. **Am I local for this host?** Compare the requested host's `machine_name` to *this* box's `$MACHINE_NAME`
   (exported by the deployed `config.zsh`; fall back to `hostname -s`):
   ```bash
   HERE="${MACHINE_NAME:-$(hostname -s)}"
   ```
   - LOCAL iff `$MACHINE_NAME_OF_HOST` == `$HERE` (or `$HOST_HN` == `$(hostname -s)`).

5. **Check the host is reachable** (only for a remote target — "must know how to check host"):
   ```bash
   tailscale status --json | jq -e --arg hn "$HOST_HN" '.Peer[]|select(.HostName==$hn)|.Online' >/dev/null \
     || echo "host $HOST ($HOST_HN) is not online on the tailnet — aborting"
   ```
   Abort (do not dispatch) if offline. Report it.

6. **Dispatch** — build the engine call once, run it local or remote:
   ```bash
   ARGS="$PROJECT --agent $AGENT --detach"
   [ -n "$MODEL" ]  && ARGS="$ARGS --model $MODEL"
   [ -n "$EFFORT" ] && ARGS="$ARGS --effort $EFFORT"

   if [ "$LOCAL" = yes ]; then
     bash ~/.config/zsh/ai/rc.sh $ARGS
   else
     ssh "${SSH_USER}@${TS_DNS}" -t "bash ~/.config/zsh/ai/rc.sh $ARGS"
   fi
   ```
   `--detach` is always passed: I am not attaching, I am starting a catchable session.

7. **Relay** the engine's output verbatim to the operator — especially the `home→host` ssh-attach line
   and the Remote Control URL. That is how they catch the session from their phone.

## Guardrails

- Required means required: never guess a host or an agent. Ask.
- I dispatch through `ai/rc.sh` only. I do not spawn `claude` directly, and I do not hand-roll tmux — the
  engine owns the pty, the render polish (`tmux -u -2`, allow-passthrough, status off), and the reach lines.
- Registry data lives in the JSON registries. If a path or host looks wrong, the fix is the registry file, not here.
- Cross-host ssh needs the tailnet link + auth already working (tailscale ssh or an authorized key). If ssh
  fails, report the failure and the exact command tried — do not try to "fix" auth from inside the launch.
