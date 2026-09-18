---
updated: 2026-09-18 01:05 CEST
writer: trajectory · Claude Code (opus-5)
host: home (hruzam) — verified by mechanism fingerprint, not config string: /usr/bin/php74 ABSENT, valet ABSENT, MACHINE_NAME=home
worktree: /home/hruzam/ia-sync · branch main · HEAD 6683ee5 · DIRTY — this session owns only `AGENTS.md`(+1 line), `protocole/`, `.dev/session/tunnel-upgrade-01-parametrization/`; all other dirty paths are foreign work (deploy.sh, journal.host-cleanup.md, zsh/session/runbook.py, zsh/system/dashboard.md, zsh/session/help/**, nano/, terminal/). Companion repo /home/hruzam/reposoma also dirty: raw.guides/tunnel/{GUIDE.md, dev-journal.tunnel.md, res/settings.md, src/observation.parametrization-and-session-hygiene.2026-09-18.md}
gate: a preset named in `zsh/registries/tunnel.json` opens a tunnel thread whose sandbox AND reasoning effort demonstrably match that preset, proven by one live turn (`tun status` + one `tun ask`)
checkpoint: session spine authored (RUNBOOK.md + STATUS.md). No task started. Findings backing all three tasks are durable in reposoma at `raw.guides/tunnel/src/observation.parametrization-and-session-hygiene.2026-09-18.md` + the 2026-09-18 dev-journal entry — both written, both uncommitted. Zero quota spent this session to date; every probe so far was `codex sandbox` or an app-server `initialize` handshake.
in_flight: none
recovery_probe: |
  Three read-only checks, in order, to learn where a dead session stopped:
  (1) `zsh /home/hruzam/ia-sync/zsh/ai/tunnel-codex.selftest.zsh` → "64/64 ... passed" means shim logic is intact (T2 either untouched or landed cleanly); a failure count means T2 was mid-edit and the compose copy is broken.
  (2) `diff -q /home/hruzam/ia-sync/zsh/ai/tunnel-codex.py /home/hruzam/.config/zsh/ai/tunnel-codex.py` (repeat for .zsh) → identical means compose==live, no half-deploy; differing means an edit was cut but `deploy.sh` never ran, so the LIVE tunnel is still the old behaviour and any `tun` result observed was pre-change.
  (3) `TUNNEL_CODEX_STATE=/home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization/tunnel.state.json zsh /home/hruzam/.config/zsh/ai/tunnel-codex.zsh status` → exit 13 means no vault was ever bound (no quota spent, nothing in flight); exit 0 with `threadId: null` means the table was opened but no thread born; exit 0 with a threadId means a thread exists and MAY hold an interrupted turn — resolve with `tun read`, which re-fetches without spending a turn.
holds: |
  - commits/pushes HELD by @majkee (explicit: "we commit later, requires gentle approach") — this session commits nothing
  - office host declared quiet by operator; no inbound sync expected while this runs
  - `deploy.sh` is modified+uncommitted by a FOREIGN session (adds an additive `~/.nanorc` leg). Running it for T2 will also deploy `nano/nanorc`, work this session does not own — surface to @majkee BEFORE the deploy leg
  - do not stage, revert, or clean any dirty path outside this session's own files
  - compose-first: `/home/hruzam/.config/zsh/**` is a deploy target, never an authoring surface
  - Law 2.4: operator opens the table; every send/ask spends shared ChatGPT quota
  - never touch `~/.codex/thread-writer-locks/`
  - no self-gavel of canon; T3's chapter lands `[DRAFT]` pending @majkee
next: open T1 — apply the four canon corrections listed in RUNBOOK.md §T1 (three files in /home/hruzam/reposoma/raw.guides/tunnel/, one in /home/hruzam/ia-sync/AGENTS.md). No code, no deploy, no quota. Awaiting @majkee's go on the `user-run.md` policy question: correct the mechanism while preserving the multi-repo restriction as an explicit house choice (recommended), or drop the restriction entirely.
expected: the four statements read true against observed 0.154.0 behaviour; `res/user-run.md` still carries the multi-repo restriction but framed as a house choice rather than a mechanical necessity; `AGENTS.md` host-resolution section names tmux 3.7c present on home and drops `~/projects` as an office discriminator; no file outside those four is modified; still zero quota spent.
---

# STATUS — tunnel-upgrade-01-parametrization

Task ledger (state lives in the front-matter above; this is the map).

| task | scope | colour | state |
|---|---|---|---|
| T1 | correct four false canon/AGENTS statements — audited edit, not gavel-gated | 🔴 canon | **next** — awaiting policy answer on `user-run.md` |
| T2 | shim: `-c` passthrough · occupancy % in usage tail · `close` orphan-guard | 🔴 deployed + quota | not started — opens with one live verification turn |
| T3 | `zsh/registries/tunnel.json` + `res/registry.md` chapter, `[DRAFT]` | 🔴 canon + deployed | not started — depends on T2's verification outcome |

## Open question blocking T1

`res/user-run.md` fuses a mechanism claim (wrong — `writable_roots` disproves "multi-repo
forces `danger-full-access`") with a policy claim (keep multi-repo fan-out gated behind
verify→execute), which may still be wanted for its own reasons. Correcting the mechanism
while silently dropping the policy would be a decision this seat has no authority to make.

## Known unverified premise under T2

App-server *accepts* `-c sandbox_workspace_write.writable_roots=[…]` at handshake — proven.
A *born thread honouring it* — NOT proven, and not provable without spending a turn. T2
therefore opens with that verification rather than assuming it. If the answer is no, T3's
registry can only carry `sandbox_mode` + `model_reasoning_effort`, and the chapter's claims
must shrink accordingly.
