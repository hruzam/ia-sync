# codex-remote-control-cli-01-wrapper

goal: The Codex prosthetic remote control — Codex has no vendor app-door, so a Termux
wrapper v0 gives any tailnet device terminal-reach into living claude|codex sessions in
prepared tmux beds on a selected host (office first; home + incoming arch-mac as registry
slots), with the FULL Codex TUI (approvals ON), multi-seat sub-tabs, a shared prompt
buffer as PTYRA's paste landing pad, and the Claude both-doors variant verified alongside.

gate: From the Redmi, wrapper v0 over the existing `agentive` rail drives a full Codex TUI
on office — one live bash-approval confirmed from the phone keyboard, session surviving
phone lock + reattach — with ZERO `authorized_keys` changes.

participant_0: [majkee, {human}, redmi+home+office] — hands: C1 comfort drive + friction
  notes, phone cable / one-time adb authorization (optional lane), tunnel table open,
  linger enable if =no, gavels. Nothing else — autonomy is the point (gavel 2026-09-10).
participant_1: [trajectory, {claude, fable, high}, office] — head; authored this redraft
  and stays; delegates bodies of work to @Delta in-window; navigation + test parts only
  head_note: oStar — cSharp posture, un-canonical: head spawns subagents in-window and
  reaches Codex through the tunnel's stored thread; authors and stays as navigator and
  status_owner; closes the session if it can.
participant_2: [cartan, {codex, terra, high}, office, tunnel] — crossed witness + Codex-side
  probe over ONE stored tunnel thread (continuity across days per tunnel GUIDE); counter-signs
  C2 artifacts by path; never rewrites STATUS
participant_3: [delta, {claude, haiku, high}, office] — surgical file authoring under the
  head, spawned in-window (token-economy law)

status_owner: trajectory
schema_note: raw.guides/runbook/GUIDE.md verified 2026-09-05 · res/csharp-head-protocol.md
  GAVELED 09-04 (oStar = un-canonical variant, majkee gavel 2026-09-10 in session
  fc-sync.trajectory-cSharp.cli-remotes) · tunnel: raw.guides/tunnel/GUIDE.md (LIVE, stored
  thread — supersedes the v1 "flat request→response" note). v3 redraft by the seated head
  2026-09-10; gate unchanged since v1 → same session, no sibling.

## why-this-session

Claude has Remote Control; **Codex has no vendor app-door** — the wrapper is its
prosthesis. App-reach exists (rc.sh, tmux-free gavel 08-15); terminal-reach of a living
session from a pocket device did not. The wrapper keeps Codex sandbox+approvals ON and
makes them comfortable from a phone instead of bypassed (v2 finding 9, inverted).
Multivendor multisessions (shape: .dev/session/runbook-upgrade) become drivable from
Redmi + Galaxy-tablet-as-monitor + any future device. PTYRA (voice→clean prompt,
clipboard-only by its own doctrine) lands through the shared prompt buffer — the wrapper
is the missing half of the voice loop, not a new bridge.

Verified mechanism this redraft stands on (probes 2026-09-10): rc-launch skill exists
(cross-host RC dispatch is native) · home has tmux 3.7c (live tailnet probe — AGENTS.md
prose is wrong, table right; owed edit tracked in STATUS) · `claude` is NOT on home's
non-interactive SSH PATH → absolute binaries everywhere · tunnel = stored thread with
memory. Two standing gavels coexist: rc.sh tmux-free (app door) · this bed tmux-first
(terminal door). Both doors, same room.

## prompts

prompt-0 · head navigation · executor: @Trajectory (this seat)
  Seated by this redraft. Hold the arc: STATUS claims as testable paths; Cartan tunnel
  thread opened once by majkee and kept for the whole session; the four scars of
  res/csharp-head-protocol.md are counter-signed — do not re-derive.

prompt-1 · C0 preflight · executor: head (autonomous, read-only first)
  - office: `loginctl show-user hruzam | grep -i linger` → `Linger=no` ⇒ majkee runs
    `loginctl enable-linger hruzam` (mutation = his hands). `tmux has-session -t agentive`.
  - phone reachability for push flow: Termux sshd on :8022 per
    /home/hruzam/ia-sync/devices/_shared/termux-bootstrap.md (devices never pull).
  - optional adb lane (phone cabled to HOME host): head drives it as
    `ssh hruzam@100.110.27.60 'adb ...'` — activation requires majkee's one-time USB-debug
    authorization; used only for keyboard install / comfort, never for the C1 confirmation.
  - Redmi keyboard: extra-keys row is the v0 baseline; Hacker's Keyboard = optional comfort
    (majkee hands or adb lane).

prompt-2 · C1 full-UI driving test · executor: majkee hands (the friction data IS the point)
  From Redmi Termux: `ssh hruzam@100.126.182.111` → forced-command lands in `agentive`.
  cd to any project, run `codex`; trigger a bash-approval; confirm FROM THE PHONE. Lock
  phone ≥2 min, reopen, reconnect, reattach — same TUI state. Report PASS/FAIL + friction
  notes (which keys hurt) to the head; friction feeds prompt-3 scope.

prompt-3 · C2 wrapper v0 · executor: @Delta under the head · counter-sign: @Cartan (tunnel,
  by path — the head receives only navigation + test parts)
  Author under `/home/hruzam/ia-sync/devices/_shared/termux/` (absolute binaries everywhere):
  - `termux.properties` extra-keys fragment (Esc/Tab/Ctrl/arrows/pipe — from C1 friction list)
  - `bin/bed` — the tso-shaped HOST-BED command: `bed <host>` → `ssh -t <ip> 'tmux
    new-session -A -s agentive'` — slots read from
    /home/hruzam/ia-sync/zsh/harness.machine-project-registry.json + machines.json
    (office · home · future arch-mac = a registry row, zero code change); session bonded
    to the TARGET host, invariant to the access window; same script usable PC→PC
  - 4-seat sub-tabs: preconfigured tmux windows 1–4 inside the bed + extra-keys bindings
    to switch (one termux → four claude|codex seats; tmux native, zero build)
  - shared prompt holder: `bin/agentive-send` grows `termux-clipboard-get | tmux
    load-buffer -` + paste verb — ONE buffer global across all windows = PTYRA landing pad
  - `shortcuts/` — Termux:Widget one-taps: `office-attach`, `home-attach`, `paste-to-bed`
  - `README.md` help card: which command → which host · spawn claude|codex · reach living
    codex (claude is app-reachable) · install via PUSH flow only (termux-bootstrap law)
  Deploy by push from a PC with keys; verify one live tap-to-attach (majkee hands).
  No new listener, no web layer, no protocol, no daemon — v2 DO-NOT-BUILD list is law.

prompt-4 · C3 Claude both-doors + rebind checklist · executor: majkee or @Delta (haiku/high)
  Inside `agentive` on office: `~/.local/bin/claude` in a project dir → verify the SAME
  session reachable (a) in tmux from phone/terminal and (b) via `/remote-control` rebind
  in the mobile app. Law to record: ONE cloud seat, last claimer wins — a living session
  and a released sibling cannot both hold the app door. Evidence → STATUS.

prompt-5 · C4 sister-audit cold-start frame · executor: the head, FRAME ONLY
  Write `/home/hruzam/ia-sync/.dev/session/codex-remote-control-cli-01-wrapper/res/reaudit.cold-start-frame.md`:
  scope (full-process audit of `runbook-upgrade`) · auditor: FRESH Oraculum — no seat of
  this session · probe: Cartan(tunnel-spawn) · input: final head report (path recorded when
  it lands) · read-order · verdict shape · what NOT to read. No findings, no conclusions.

## backlog siblings — named now, opened by PROMOTION only (never pre-created)

- `codex-remote-control-cli-02-rc-anyhost` — from Redmi, spawn a host-bonded RC claude
  session on office AND home (rc-launch skill + rc.sh Mode B), appearing in the mobile
  app, surviving spawner death. Mostly verification of native harness.
- `codex-remote-control-cli-03-home-relay` — the home multisession scenario (trajectory +
  cartan relayed from the phone); unblocked by the 09-10 tmux-3.7c probe.

## known constraints + destructive holds

- HOLD: no `authorized_keys` edits — v0 rides the verified agentive rail; named-bed
  dispatcher stays v1, pain-gated.
- HOLD: other sessions' files (runbook-upgrade · codex-identity-resolution · rellays-* ·
  therapy · the dirty AGENTS.md) — no stage/commit/stash/edit from this session; the
  AGENTS.md tmux-prose correction is an OWED EDIT tracked in STATUS, not performed here.
- HOLD: full `deploy.sh` under palette.map hold — targeted flows only.
- Tunnel law: `--state` explicit (exit-13 rule); state file NEVER committed; NEVER unlink
  `~/.codex/thread-writer-locks/*`; each send spends real ChatGPT turns — one thread,
  opened once.
- Devices never pull; tablet read-only (`attach -rt`); Codex approvals stay ON; all trust
  flows PC → device (adb lane is doctrine-aligned, activation = majkee's hands).
- Absolute paths / absolute binaries in every wrapper command (home PATH scar, 09-10).
- Single RC cloud seat — last claimer wins; never `--continue` for remote.

## references (point, never copy)

- Briefs: `/home/hruzam/ia-sync/.dev/session/codex-remote-control-cli/raw/brief.implementation.byAsymmetry.2026-09-04.md`
  · `…/raw/brief.implementation.session-bed.v2.bySymmetry.2026-09-04.md`
- Head protocol: `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md`
- Tunnel: `/home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md` · shim
  `/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh` (header = law)
- RC: `/home/hruzam/reposoma/raw.guides/remote-control/GUIDE.md` (engine truth = rc.sh) ·
  `~/.claude/skills/rc-launch/SKILL.md`
- Rail + device law: `/home/hruzam/ia-sync/devices/_shared/agentive-tmux.md` ·
  `…/termux-bootstrap.md` · `/home/hruzam/ia-sync/devices/README.md` ·
  `…/devices/redmi-15c-5g/device.md`
- Voice: `/home/hruzam/reposoma/raw.chatGPT-agents/ptyra/PTYRA.knowledge.md` (clipboard-only
  by doctrine — the wrapper is the paste target, never a bridge)
- Cross-runtime: `/home/hruzam/ia-sync/HANDSHAKE.md`

## what closes the gate

STATUS records the gate verbatim as PASSED with C1 evidence (approval confirmed from the
phone, survived lock+reattach) AND C2 wrapper files live on the Redmi via push flow,
counter-signed by Cartan over the tunnel. Before prune, the head's ritual: C3 both-doors
evidence · C4 frame on disk · experience-transfer letter in this bed's `raw/` · explicit
promotion manifest listing EVERY `raw/` keeper (scar 4) · journal entry · piql-Houston
substrate mail if any service/ssh surface moved · owed AGENTS.md edit either landed by its
owner or re-flagged.

## what this session deliberately does not do

The runbook-upgrade audit itself · the named-bed dispatcher · mosh/ttyd/web terminal/any
new daemon or listener · the 02/03 sibling work (named above, promotion only) · arch-mac
onboarding beyond its registry slot · cross-machine daemon architecture (piql/Houston
domain) · any `authorized_keys` change · any edit to files owned by other sessions.
