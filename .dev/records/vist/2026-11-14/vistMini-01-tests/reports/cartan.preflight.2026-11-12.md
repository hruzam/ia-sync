# Cartan preflight — cooperation transport reuse

Date: 2026-11-12 · host: home (`hostname -s` = `hruzam`, matched to machines.json).
Author: Cartan. One bounded read-only researcher supplied candidates; Cartan inspected the cited excerpts before integration. This is a preflight report, not a completed transport trial.

## Question and method

What existing mechanism can carry vendor-neutral requests and receipts, and what Bash delta warrants a controlled test? Inspect local source and actual command outcomes; distinguish implementation existence, historical reports and current behavior. No new API behavior is inferred from memory. Baseline ia-sync HEAD was `2c2b01d`, main, clean at intake.

## Observed evidence

| Source or command | Observation | Limit |
|---|---|---|
| `HANDSHAKE.md:28–40` | persistence differs from receipt; existing consumer stamps/replies | doctrine, not a runtime test |
| `.dev/_backlog/cross-host-session-bus.md:63–104` | pointer format, loop limits, stamp table and own-host path restriction | draft under challenge |
| `zsh/ai/temple-mail.zsh:77–122` | writes receiver inbox, emits path, no sent copy | direct overwrite redirection; no collision guard/Git/tmux in inspected function |
| `zsh/ai/temple-transport-selftest.zsh:65–95` | synthetic roots and temporary map for isolated mail testing | source inspected; tests not run here |
| `zsh/session/ovitmugen.py:16–20,51` | viewer-only; explicit server and pane-ID rules; pane command/PID/dead format | do not extend it to inject input |
| `.dev/session/jev-01-codex-pilot/raw/HANDOFF.tui-bus-substrate.2026-11-10.md:24–63` | historical native notification plus persistent BUS assignment/result/verification | old handle/tool is not a current delivery guarantee |
| `.gitignore:60–61` | `_mail/*/archive` ignored | local archival does not supply a remotely inspectable archive stamp |
| `tmux has-session -t traj-home` in the ordinary sandbox, earlier exchange | socket error: Operation not permitted | access denial, not evidence session is absent |
| `tmux list-panes -a -F '#S:#I.#P #{pane_id} #{pane_current_command}'` with explicit escalation, 2026-11-12T08:03Z | exit 0: `cartan-home:0.0 %1 codex`; `traj-home:0.0 %0 claude` | snapshot only; no byte injection, input-state or busy-state guarantee |
| `git -C /home/hruzam/ia-sync pull --rebase origin main` at intake | exit 0, already up to date | no claim about a later concurrent write |

All source paths above resolve under `/home/hruzam/ia-sync/`; line ranges are inspection coordinates at the baseline revision, not stable semantic identifiers. Governing session law is in `/home/hruzam/reposoma/raw.guides/{runbook,status,bus}/GUIDE.md`; no copy of that law is proposed for deployment.

## Inference and rival explanation

Reuse receiver-owned mail and existing BUS verification. A small session-local Bash notification adapter may be enough; helper necessity is not yet established by a trial. A pane/process check can observe the wrong moment: the agent could exit or the composer could already contain operator input. An apparently successful notification could therefore corrupt a draft or land at a shell. A screenshot or exit 0 cannot exclude these rival explanations.

The researcher's useful falsification case is an isolated pane deliberately exiting between preflight and Enter. Capture the pane and attempt result; any shell execution of the pointer falsifies a safe-delivery claim. Also test an occupied composer and prove that the helper leaves it unchanged. Do not run destructive/input-interference probes on the live operator sessions.

## Coordination and reproducibility limits

Both live seats share one checkout and Git index. Separate output filenames do not isolate staging, commits, pull or rebase. The head should serialize mutation windows; neither seat should auto-stash, reset or commit the other's staged work. Record relevant commit IDs and exact artifact content for each observation. Store recipient consumption evidence separately from notification success, using the existing reply/stamp semantics rather than a new task ledger.

This preflight did not test live message submission, queue delivery, crash recovery, bounded retries, Bash allowance semantics or VIST applicability. Those remain proposed experiments in `protocol-proposal.md`. No Bash helper, runtime configuration, canon or deployment was changed. The investigator's report is not an independent VERDICT; Trajectory or a named verifier must check the actual artifacts.
