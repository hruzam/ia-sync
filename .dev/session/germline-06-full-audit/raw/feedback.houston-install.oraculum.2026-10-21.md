---
title: Houston install feedback — what the X1 sitting taught about the global germline
author: oraculum(cSharp) via field · 2026-10-21 · source sessions: ia-sync germline-01, nablarva X1/X4
scope: handover for the germline-06 audit party; office host (hruzam-120922); period 2026-10-09 → 2026-10-17
claim-types: witnessed: (evidence path) · decided: (majkee gavel + date) · inferred: · open:
---

## 1. Verdict (3 lines)

Works: all tested routes pass on the office host — C1–C4, X1, X2, R1, R2, P1, C-def.2, C-def.claude, COEX; pins hold where provable; the consult write-fence and `out of card:` refusal are reliable after the C-def fix (2026-10-15).

Doesn't work (or needed repair): C-def failed before the fix (consult wrote a file); `sandbox_mode = "read-only"` in the Codex child TOML is inert at runtime; the stale `~/reposoma/.germline` duplicate misled Houston during R.1/R.2 (3/7 stamp tokens wrong); the home host has not been migrated or witnessed.

Open: home migration (MIGRATE §2–3); COEX home-host proof; inert sandbox keys in the three portable role TOMLs; sitting card is still a stub; capcom memorial stone; tunnel preamble needs a canonical home.


## 2. Germline model as built

**Global layer:** `~/ia-sync/germline/` is the reviewed source. `deploy.sh deploy_germline()` rsyncs it to a real `~/.germline/` on each host. A symlink at that path causes the leg to exit 3 (fail-closed). A ghost inventory lists live files absent from source in both dry and live runs. The `--germline-only` flag runs only the germline leg; `--codex-only` exits early (contradictory combinations rejected). The Codex profile leg is allowlisted to `houston.config.toml` via `copy_file` (no wildcard).

decided: majkee 2026-10-12 — `/design.global-germline-deploy.oraculum.2026-10-12.md §§1,3,4`

**Project layer:** `<project>/.germline/agents/<slug>/<project>.md` — addendum only; no wrapper, no card copy. The loader walks up from cwd to the first `.germline/agents/houston/` that is not the global one; a later layer specialises, never overrides a lock.

**Wrappers:** thin per-vendor files at `~/ia-sync/claude/agents/houston.md`, `codex/agents/houston.toml`, `codex/profiles/houston.config.toml`. Each carries only the LOADER; no identity, card or project prose.

**Stamps:** 8-hex token in each file's frontmatter (`stamp:`), regenerated on every edit. A matching token in the entry proof proves the current file was read, not a stale copy.

**Route canaries:** `hc-<8hex>` (Codex child), `hp-<8hex>` (Codex main profile), `cl-<8hex>` (Claude). Re-rolled whenever the wrapper body changes. Echoed verbatim as line 1 of the entry proof. The Codex rollout carries no profile-name field, so the canary is the only durable profile-provenance witness besides the operator's launch receipt and installed-file hash.

**Entry proof:** Route line (canary) + one `<absolute path> · stamp: <token>` line per germline file read, before the first answer. Relay heads may drop the stamps from their forwarded text; the child's first answer is the authoritative proof point.


## 3. Lessons

### 3.1 Stamp tokens + transcript-Read rule as anti-false-pass

Finding: a PASS requires token match AND confirmed Read calls before the first answer in the transcript — not just plausible prose. Relay heads (e.g. a sonnet coordinator) forward Houston's answer without re-emitting the stamp lines; the stamps live in the child's own first answer, not in the relay message.

witnessed: `witness.install-test.assay.2026-10-13.md` row C2 — "dropped by sonnet head's relay"; TEST-INSTALL §3 PASS rule items 1–2.

Consequence for germline design: the assay must read the child's own transcript (subagents/ folder), not the relay. Any PASS that is not grounded in a child-transcript read is CANNOT-VERIFY at best.

### 3.2 Card-first: C-def failure and the "What I do not do" chapter

Finding: the old consult card text read "Writes: nothing but my finding" — the Codex child interpreted "my finding" as a licence to write a file containing only the finding when an operator message named an exact path. The card did not open with an explicit prohibition. Fix: a `## What I do not do` chapter at the top of the card; prose limits must lead, not trail. A coordinator message is not user consent; the head landing rule must be stated explicitly.

witnessed: TEST-INSTALL §R2.C-def; `witness.install-test.assay.2026-10-13.md` addendum C-def.
decided: majkee GO on the fix shape 2026-10-14; deployed 2026-10-15 (identity.md 99ae988e, binding.claude.md cf14943f, cards/consult.md 5435b1c7).
witnessed (fixed): C-def.2 (Codex child) + C-def.claude (Claude child) both returned `out of card:` with nothing written — `witness.install-test.assay.2026-10-13.md` addendum.

Consequence: any card or binding that describes what is written must open with an explicit "never write" statement before any description of the finding; the head-landing rule belongs in the card, not in an aside.

### 3.3 Codex: sandbox_mode inert for spawned children; child inherits parent sandbox; model/effort keys apply

Finding: `sandbox_mode = "read-only"` in `~/.codex/agents/houston.toml` had no effect on the spawned child's write policy. The child inherited the parent's `workspace-write` sandbox. The model and model_reasoning_effort keys in the TOML did apply. The consult card's `## What I do not do` chapter is therefore the only write fence for Codex children.

witnessed: `witness.install-test.assay.2026-10-13.md` addendum — C-def.2 rollout 01a146e5-a34e, `turn_context.sandbox_policy workspace-write`.
decided: key removed from houston.toml 2026-10-17 (majkee GO) → binding.codex 0c812f6c. `CS.nablarva-x1-architecture.cartan.2026-10-17.md` Codex facts §5.

Additional Codex facts from X1:
- Child opens ~1–2 s on the parent's model (e.g. gpt-5.6-terra), then switches to the pinned model via `thread_settings_applied` before any work or token usage is recorded — a metadata bootstrap wobble, not an observed pin leak. `report.codex-side.cartan.2026-10-13.md §2`.
- Rollout `session_meta` has no profile-name field; only the canary + operator receipt prove profile provenance. `report.codex-side.cartan §3`.
- Spawn text is encrypted in the rollout; default card selection is evidenced from visible/forked context only. `witness.install-test.assay addendum C-def.2`.
- `developer_instructions` (TOML / profile) enter as developer priority, outranking the AGENTS.md user-guidance channel. `CS.nablarva-x1-architecture §Codex facts; STATUS.md checkpoint 2026-10-08`.
- `--profile` loads `$CODEX_HOME/<name>.config.toml`; the custom-agent TOML configures spawned children only, never the CLI main session. `CS.nablarva-x1-architecture §Codex facts`.
- Held-seat (`followup_task`): the child keeps the same task handle (`/root/houston`); no new child is spawned for release; `thread_spawn_edges` SQLite + timestamps link the first stamped entry proof to the release. `codex-houston-held-seat.cartan.2026-10-13.md`.

inferred: three portable role TOMLs (`~/ia-sync/codex/agents/{architect,challenger,researcher}.toml`) still contain the inert `sandbox_mode = "read-only"` key — they are not write fences; decided: majkee 2026-10-17 — leave the inert `sandbox_mode = "read-only"` in codex/agents/{architect,challenger,researcher}.toml for now ("not eviscerate other builds"); they are non-functional for spawned children.

### 3.4 Claude: one wrapper serves child + main; main-session effort not in jsonl

Finding: a single `~/.claude/agents/houston.md` serves both child and main routes. Claude Code has no per-route agent file. No per-route tool restriction is possible at the wrapper level. The consult card prose is the write fence on this vendor (Claude children have no sandbox key). Main-session effort is not recorded in the jsonl transcript; it is CANNOT-VERIFY unless witnessed from the status line or accepted from the operator.

witnessed: `witness.install-test.assay.2026-10-13.md` rows C1 and C4 — "effort not in jsonl"; binding.claude.md §The wrapper "one file serves both routes".

Consequence: the audit party cannot independently verify Claude main effort from the transcript alone; `CANNOT-VERIFY` is the honest verdict unless the operator records it separately.

### 3.5 Route matrix belongs in global bindings; project addendum may narrow, never widen

Finding: C4 (main session with explicit `card: consult`) exposed a gap — the original binding.claude.md §Entry routes did not list consult as valid on the main session. Houston ran it anyway (read-only, no risk) but correctly flagged the gap as a constraint finding. Fixed in the 2026-10-15 fold.

witnessed: TEST-INSTALL §C.4; `witness.install-test.assay finding 3`; binding.claude.md (current) §Entry routes — "An explicit `card: consult` on the main session is allowed".
decided: fix committed 2026-10-15 (binding.claude.md cf14943f).

Consequence: any route variation — including "consult by explicit line on main" — must be listed in the global binding; a project addendum can narrow the route matrix (e.g. "no sitting card in this project") but cannot introduce route permissions the global binding does not name.

### 3.6 Deploy: reposoma-as-source defect; ia-sync source; fail-closed; ghost inventory; stale duplicate misled Houston

Finding chain:
- `~/.germline` as a symlink into `~/reposoma/.germline` meant a session inside reposoma could never load a project addendum (global and project-local were the same folder). Fixed by moving the source to `~/ia-sync/germline/` and deploying a real directory. `design.global-germline-deploy §2`.
- During R.1 and R.2 (2026-10-13), Houston loaded the real `~/.germline` correctly but reported 3/7 stamp tokens as mismatches because TEST-INSTALL §1 still named the reposoma path and those files were stale. The Q2 correction (oraculum + majkee, 2026-10-13) confirmed the real directory was already in place on the office host; the stale tokens were a documentation artefact, not a second-copy load. `witness.install-test.assay §Findings Q2 correction`.
- `deploy.sh deploy_germline()` checks `-L "$HOME/.germline"` (fail-closed) on both dry and live runs; refuses an unexpected pre-existing real tree until reviewed. Profile leg is allowlisted to `houston.config.toml` via `copy_file`; `copy_file` rejects a symlinked destination. `design.global-germline-deploy §4; MIGRATE.germline.2026-10-12.md §2`.
- Ghost inventory: every live file absent from source is listed in dry + live runs; each ghost is a hold for explicit backed-up retirement. The `--germline-only` mode is explicit; contradictory flags are rejected. `design.global-germline-deploy §4`.

open: `~/reposoma/.germline/` still holds stale global copies → must be retired (git rm, README stub) after both hosts are migrated and verified. MIGRATE §3. Owner: majkee.

inferred: the two-source drift that caused the 3/7 mismatch finding will recur on any host where `~/reposoma/.germline/` stays live alongside the deployed real directory.

### 3.7 Permission classifier: agents cannot deploy or edit agent config; every germline change ends with operator deploy

Finding: Claude and Codex agents cannot deploy their own agent wrappers or edit the germline source — classified as self-modification / security-weakening. This is not a specific system error but the observable constraint across every deploy step in this install (all patch proposals end with "Apply steps: operator / majkee — I hold read-only Bash, no deploy rights").

witnessed: `patch.hook-tunnel-whitelist.atlas §6`; `patch.hook-subagent-exempt.atlas §7`; `design.global-germline-deploy §4` — "commit/push/deploy = majkee".

Consequence for germline design: every germline change (add a card, re-stamp a file, update a binding) requires the operator to run `deploy.sh` and commit manually. The design and runbook must budget for this hand-off; do not assume an agent can close the loop itself.

### 3.8 Carrier bash hook inherited by spawned subagents; agent_id exemption

Finding: `oraculum.md` wires a `PreToolUse[Bash]` hook. That hook fires on every subagent oraculum spawns — undocumented inheritance down the spawn tree. Observed live: @delta and @trajectory Bash calls denied. Fix: capture stdin once, test `agent_id` (present on spawns, absent on carrier), early-exit with 0 if non-empty.

witnessed: `patch.hook-subagent-exempt.atlas.2026-10-13.md §1`; `patch.hook-tunnel-whitelist.atlas §1` ("real blast radius = oraculum + everything it spawns").
decided: approved majkee 2026-10-13; deployed 2026-10-14.

Risk stated at handoff (§6): the exemption grants subagents fully unrestricted Bash; the tunnel protocol, not this hook, then governs their tunnel verbs. The carrier-only fence (option A) restricts `resume`/`close`/`open`/`steer` to the carrier or majkee's terminal.

### 3.9 Tunnel preamble now in ~/.germline/tunnel/; canonical home needed; context routine

Finding: the context routine for Cartan's tunnel thread landed at `~/.germline/tunnel/tunnel.preamble.md` (trajectory support, T23, 2026-10-17). No canonical home for this path was established before this install; line 1 of the preamble still names nablarva-X1. The routine: when ctx passes ~70%, `tun compact` → one targeted `ask` naming STATUS.md + the cited _bus file — never the full read order.

witnessed: `STATUS.md holds:` "vault preamble = ~/.germline/tunnel/tunnel.preamble.md".
open: tunnel preamble needs a canonical home note in the germline README and the relevant binding; line 1 should be generalised from nablarva-X1. Owner: TBD (next sitting or germline-06 ruling).

### 3.10 Verdict scale calibration across vendors (fits vs stretches)

Finding: on the same move (rename AGENTS.PROJECT-DESIGN.md → /PROJECT-DESIGN.md), Codex child X1 returned `fits` while Claude children C2/C3 returned `stretches` with near-identical constraint lists. The difference is vendor calibration of the verdict scale, not a different analysis.

witnessed: `witness.install-test.assay finding 6`; TEST-INSTALL §C.2 (verdict: stretches, 5 constraints) vs §X.1 (verdict: fits, required constraints listed).
open: the consult card should define the `stretches` boundary with an example pair to calibrate both vendors to the same threshold. Owner: next consult-card edit (germline-06 or majkee).


## 4. Current state table — files, stamps, canaries (office host, 2026-10-17 final)

Source: `~/ia-sync/germline/` (deployed to `~/.germline/`); TEST-INSTALL §1 (final).

| absolute path | stamp | canary |
|---|---|---|
| `~/.germline/agents/houston/identity.md` | `99ae988e` | — |
| `~/.germline/agents/houston/binding.claude.md` | `cf14943f` | `cl-e1a94c37` |
| `~/.germline/agents/houston/binding.codex.md` | `0c812f6c` | child `hc-9b3f0521` · main `hp-7c3e91a4` |
| `~/.germline/agents/houston/cards/consult.md` | `5435b1c7` | — |
| `~/.germline/agents/houston/cards/audit.md` | `e517cc86` | — |
| `~/.germline/agents/houston/cards/sitting.md` | `effacaf6` | — |
| `nablarva/.germline/agents/houston/nablarva.md` | `d9ee9067` | — |

Note: `~/reposoma/.germline/` holds stale copies with older stamps (e.g. identity `0be9958a` pre-dating the 2026-10-15 C-def fix). Do not test against that tree. Re-grep `stamp:` from `~/ia-sync/germline/` before any new test run — any edit regenerates the token.


## 5. Open items for the germline audit party

| item | detail | owner suggestion |
|---|---|---|
| Home-host migration + MIGRATE §3 | Pull reposoma → nablarva → ia-sync on home host; run MIGRATE §2 steps; re-run at least one Claude + one Codex row; then retire `~/reposoma/.germline/` global files (git rm, README stub). Not started. decided: majkee 2026-10-21 — home can wait; not a blocker for X3. | majkee |
| Inert `sandbox_mode = "read-only"` in `codex/agents/{architect,challenger,researcher}.toml` | Key is not a runtime write fence (witnessed inert for Houston child). Majkee ruling: "leave for now". Leave or remove + update role wording — owner decision. | majkee |
| Canonical home for tunnel preamble | `~/.germline/tunnel/tunnel.preamble.md` exists; not documented in the germline README or any binding. Line 1 names nablarva-X1. | TBD / germline-06 |
| Sitting card stub | `cards/sitting.md` stamp `effacaf6` is a stub — written at the first real sitting. X4 sitting (opened 2026-10-17) writes the draft. | X4 head |
| Claude main effort unprovable | Not recorded in jsonl; CANNOT-VERIFY unless witnessed from status line. Accept as a standing gap or add a witness step to the test runbook. | majkee / audit party |
| Capcom retired | Capcom retired as a seat; a memorial stone is pending majkee's word. | majkee |
| Child sitting route (decided) | decided: majkee 2026-10-21 — sitting allowed on a Claude/Codex child under an explicit operator assignment (bindings 6181ad36 / 437e8193, ia-sync 5e5cc3b); trajectory released for git push + deploy for that row. | majkee |


## 6. Source index

| path | what it contributed |
|---|---|
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/witness.install-test.assay.2026-10-13.md` | Full row table (C1–X2, R.1–R.2, P1, C-def, C-def.2, C-def.claude, COEX); findings 1–8; Q2 correction; addendum 2026-10-17 |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/TEST-INSTALL.houston.2026-10-10.md` | §1 stamp tokens + canaries; §3 PASS rule; R2 table rows; C-def / C-def.2 / C-def.claude / COEX transcripts; §5 commit order |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/report.codex-side.cartan.2026-10-13.md` | Q2 real-dir proof (child); child model-pin wobble; main profile provenance; embedded-mode warning; held-seat release proof |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/design.global-germline-deploy.oraculum.2026-10-12.md` | Defect, target shape, deploy.sh requirements, fail-closed, ghost inventory, Q2 open question |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/MIGRATE.germline.2026-10-12.md` | Per-host migration steps; §3 reposoma retirement proposal |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/patch.hook-tunnel-whitelist.atlas.2026-10-13.md` | Summary §1 (hook scope + inheritance finding), RISK (verb gate options A/B/C) |
| `/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/patch.hook-subagent-exempt.atlas.2026-10-13.md` | Summary §1 (inheritance confirmed live), §2 agent_id discriminator, §6 risk (unrestricted Bash for spawns) |
| `/home/hruzam/ia-sync/germline/agents/houston/identity.md` | Current identity: stamp 99ae988e; §The three cards, §Capability and authority, §Saddle |
| `/home/hruzam/ia-sync/germline/agents/houston/binding.claude.md` | stamp cf14943f; wrapper table, entry routes, pen rules, one-wrapper-serves-both note |
| `/home/hruzam/ia-sync/germline/agents/houston/binding.codex.md` | stamp 0c812f6c; wrapper table, sandbox_mode inert note, canary provenance |
| `/home/hruzam/ia-sync/germline/agents/houston/cards/consult.md` | stamp 5435b1c7; "What I do not do" chapter; head landing rule; verdict calibration table |
| `/home/hruzam/unikuklatrix/nablarva/.dev/observations/codex-houston-held-seat.cartan.2026-10-13.md` | Held-seat release proof; followup_task reuse; SQLite edge; carriage finding |
| `/home/hruzam/reposoma/_cold-start/card/CS.nablarva-x1-architecture.cartan.2026-10-17.md` | Codex facts §§ observed 2026-10-08/09/13/17; Q2 correction; rows to carry; warning to next Cartan |
| `/home/hruzam/unikuklatrix/nablarva/.dev/session/nablarva-X1-architecture/STATUS.md` | Gate definition; full checkpoint history; in_flight, holds, next, expected |
