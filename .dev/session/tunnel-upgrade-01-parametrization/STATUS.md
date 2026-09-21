---
updated: 2026-09-21 CEST
writer: trajectory · Claude Code (opus-5)
host: home (hruzam) — verified by mechanism fingerprint, not config string: /usr/bin/php74 ABSENT, valet ABSENT, MACHINE_NAME=home
worktree: /home/hruzam/ia-sync · branch main · HEAD 9f6ff85 ("2026-09-18. protocole + tunnel") · near-clean — only `.gitignore` modified, owned by this session. Operator synced both repos host-to-host and committed: the session spine, `protocole/`, `AGENTS.md`, and the previously-foreign work all landed in 9f6ff85. Companion repo /home/hruzam/reposoma clean at d909151 (settings.md chapter + both observations + journal entries committed). **A clean rollback point now exists for T2.**
gate: a preset named in `zsh/registries/tunnel.json` opens a tunnel thread whose sandbox AND reasoning effort demonstrably match that preset, proven by one live turn (`tun status` + one `tun ask`)
checkpoint: session spine authored and COMMITTED (9f6ff85). All backing findings durable and committed in reposoma (d909151). No T-task started yet. Zero quota spent this session to date — every probe so far was `codex sandbox` or an app-server `initialize` handshake. **Law 2.4 hole found and CLOSED (2026-09-21).** Tracked vault state files (`.dev/session/tunnel-home.state.json`, `.dev/session/cs-card-sys-update/tunnel.state.json`) both carried `enabled: true` — one bound to a live threadId, one pre-armed `workspace-write` — and synced host-to-host, handing office a pre-opened table it never opened. Fix landed by @majkee: `git rm --cached` + commit, plus a scoped `.gitignore` rule. Verified post-commit: untracked ✓, both files still on disk so live vaults are intact ✓, ignored going forward via `.gitignore:48 tunnel*.state.json` ✓. Office's copies disappear on its next pull — intended; each host must open its own table. Ignore rule was deliberately narrowed from `*.state.json` to `tunnel*.state.json` to avoid swallowing unrelated future files; audit any widening with `git ls-files | git check-ignore --stdin --no-index -v` (note: without `--no-index` that check silently skips tracked files and fails OPEN).
in_flight: none
recovery_probe: |
  Three read-only checks, in order, to learn where a dead session stopped:
  (1) `zsh /home/hruzam/ia-sync/zsh/ai/tunnel-codex.selftest.zsh` → "64/64 ... passed" means shim logic is intact (T2 either untouched or landed cleanly); a failure count means T2 was mid-edit and the compose copy is broken.
  (2) `diff -q /home/hruzam/ia-sync/zsh/ai/tunnel-codex.py /home/hruzam/.config/zsh/ai/tunnel-codex.py` (repeat for .zsh) → identical means compose==live, no half-deploy; differing means an edit was cut but `deploy.sh` never ran, so the LIVE tunnel is still the old behaviour and any `tun` result observed was pre-change.
  (3) `TUNNEL_CODEX_STATE=/home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization/tunnel.state.json zsh /home/hruzam/.config/zsh/ai/tunnel-codex.zsh status` → exit 13 means no vault was ever bound (no quota spent, nothing in flight); exit 0 with `threadId: null` means the table was opened but no thread born; exit 0 with a threadId means a thread exists and MAY hold an interrupted turn — resolve with `tun read`, which re-fetches without spending a turn.
holds: |
  - commits/pushes HELD by @majkee (explicit: "we commit later, requires gentle approach") — this session commits nothing
  - office host declared quiet by operator; no inbound sync expected while this runs
  - `deploy.sh`'s foreign `~/.nanorc` leg is now COMMITTED (9f6ff85), so T2's deploy no longer ships uncommitted foreign work. Side effect stands and is now legitimate: running `deploy.sh` also deploys `nano/nanorc` → `~/.nanorc`. Expect it in the dry-run output; it is not this session's change
  - do not stage, revert, or clean any dirty path outside this session's own files
  - compose-first: `/home/hruzam/.config/zsh/**` is a deploy target, never an authoring surface
  - Law 2.4: operator opens the table; every send/ask spends shared ChatGPT quota
  - never touch `~/.codex/thread-writer-locks/`
  - no self-gavel of canon; T3's chapter lands `[DRAFT]` pending @majkee
next: open T2 with its VERIFICATION leg only — confirm whether a born thread honours spawn-level `-c` sandbox config, before writing any shim code. Concretely: cut a throwaway branchless probe that spawns `codex app-server --stdio -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=["<tmp dir>"]'`, drives `thread/start` + one minimal `turn/start`, and asks the thread to attempt one write inside that root and one outside it. This SPENDS ONE REAL TURN — @majkee must open the table (Law 2.4) before it runs.
expected: the thread writes successfully inside the named `writable_roots` path and is refused (EROFS) outside it → `-c` is honoured at thread level, T3's registry can carry the full Card-2 knob set. If instead both writes are refused, or the sandbox reported by `tun status` ignores the `-c` values, then `-c` governs only the app-server process and NOT the thread — in which case T3's registry shrinks to `sandbox_mode` + `model_reasoning_effort`, and the chapter's claims must shrink with it.
---

# STATUS — tunnel-upgrade-01-parametrization

Task ledger (state lives in the front-matter above; this is the map).

| task | scope | colour | state |
|---|---|---|---|
| T1 | correct four false canon/AGENTS statements — audited edit, not gavel-gated | 🔴 canon | **DONE** 2026-09-18 — `res/user-run.md`, `res/settings.md`, `AGENTS.md` (×3 facts). Uncommitted. |
| T2 | shim: `-c` passthrough · occupancy % in usage tail · `close` orphan-guard · **central vault relocation** | 🔴 deployed + quota | **next** — verification leg first, needs @majkee to open the table |
| T3 | `zsh/registries/tunnel.json` + `res/registry.md` chapter, `[DRAFT]` | 🔴 canon + deployed | not started — scope depends on T2's verification outcome |

### T1 — what was NOT done, deliberately

- `dev-journal.tunnel.md` left untouched. Its own header declares it an **append-only
  ladder**; rewriting the 2026-09-04 entry would violate that law. The drift is already
  carried by the newer 2026-09-17 / 2026-09-18 entries, which is how a ladder corrects.
- Wording kept minimal per @majkee: stale formulation during development is acceptable and
  reconciled later by an audit pass (@assay, or @Cartan for cross-vendor eyes) rather than
  by agonising now.

### T2 — scope grew by operator decision (2026-09-18)

Vault state files move OUT of every repo into a central per-host directory —
**`~/.local/state/tunnel/`** (XDG `STATE_HOME`; *not* `~/.config/zsh/`, which is a
`deploy.sh` rsync target and would entangle state with deploy). Rationale: gitignore is a
policy guard that must be remembered — and its absence is exactly how the Law 2.4 hole
opened. Relocation makes the bad state structurally unrepresentable instead.

Must preserve the shim's existing safety property: **no global default, exit 13 when
neither `--state` nor `$TUNNEL_CODEX_STATE` is given.** Shape: add `--vault <name>` →
`~/.local/state/tunnel/<name>.json`, keep `--state <path>` working, default nothing.

Carries a follow-on canon correction, which must land only AFTER the code does: `res/user-run.md`
currently says "put it where the work lives", which is TRUE today and becomes false only
once this ships. Migration: two existing vaults move.

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
