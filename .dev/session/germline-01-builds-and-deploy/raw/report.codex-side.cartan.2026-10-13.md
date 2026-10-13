# Codex-side close-out — Houston install test

`cartan · 2026-10-13 · germline-01 · scope: installed Houston child/profile on office; no deploy, commit or home-host claim`

## 1. Q2 — real `~/.germline` under the sandbox

**said: 2026-10-13 R2.** The Codex child rollout `01a13685-62dc-7482-833a-041ef9eea180` records cwd `/home/hruzam/unikuklatrix/nablarva`, `sandbox_policy.type: workspace-write`, and a managed filesystem entry `:root: read` with Nablarva as the write root. Its tool calls read `/home/hruzam/.germline/agents/houston/{identity.md,binding.codex.md,cards/consult.md}` and the project addendum before answering. The R2 receipt reports `readlink -f /home/hruzam/.germline` resolving to itself, a real directory, with distinct inode from the old reposoma copy; its four entry stamps match the new home (`6abf41fe`, `f87f1f3c`, `a6498a47`, `46dcd163`). See `TEST-INSTALL.houston.2026-10-10.md` §R.2 and that child rollout. No read refusal appears in the cited child trace.

**said: 2026-10-13 X2.** The Codex main rollout `01a13577-49a5-7e01-8545-7ddb5e0eac56` records `gpt-6.1-sol/high`, Nablarva cwd, and reads the germline, but its earlier stamps (`0be9958a`, `cac6a05d`, `2ebbb49b`) identify the pre-migration symlink/reposoma-era content. The later R1/R2 receipts show the live home became a separate real directory after X2. See witness `witness.install-test.assay.2026-10-13.md` rows X2/R2 and `TEST-INSTALL` §§X.2, R.

**inferred: cartan.** The narrow Q2 claim is **proved for a fresh Codex child on office**, under the recorded `:root read` managed policy. It is **not yet proved for a `--profile houston` main session reading the real directory**. Extra writable roots were unnecessary for R2's reads; that does not prove every workspace-write policy grants home reads.

**unknown.** A fresh real-dir Codex main, the home host's eventual policy/filesystem, and a read-only or deny-read profile remain untested. Do not promote “both routes read the real directory” from X2 + R2 alone.

## 2. Child model-pin wobble

**said: targeted rollout inspection, 2026-10-13.** X1 child `01a13291…` first `turn_context` at `00:03:08.010Z` says parent `gpt-5.6-terra/high`; `thread_settings_applied` at `00:03:08.027Z` sets `gpt-6.1-sol/high`; next `turn_context` at `00:03:09.258Z` says Sol/high. Its first `token_usage_record` is `00:03:11.612Z`. R2 child `01a13685…` first context at `18:27:53.714Z` says Terra/high; settings apply Sol/high at `18:27:53.741Z`; next context at `18:27:55.379Z` says Sol/high; first usage is `18:27:58.257Z`. Before each Sol context, the rollout contains input `message` items and task/settings events, but no reasoning, tool call, agent output or token-usage record.

**inferred: cartan.** This is a bootstrap metadata wobble, not an observed Terra inference or pin leak. The child pin applied before the first recorded work and usage on both tested runs. The witness's effective Sol/high conclusion is supported by the trace sequence.

**unknown.** `token_usage_record` has no per-record model field; it cannot by itself prove provider billing attribution or rule out an unlogged internal request. Keep the temporal assertion exact and recheck if a future rollout shows usage before `thread_settings_applied`.

## 3. Main profile provenance

**said: X2 rollout inspection, 2026-10-13.** `session_meta` contains `source: cli`, `originator: codex-tui`, cwd and IDs, but no `profile` or launch-argument field. Its `turn_context` and `thread_settings_applied` expose effective model/effort, not the config layer that supplied them. The test receipt records majkee's `codex --profile houston -C …` invocation; the rollout alone cannot prove that flag.

**inferred: cartan.** The cheapest durable witness is a unique, route-specific canary line in the profile's `developer_instructions`, echoed verbatim in Houston's first entry proof, alongside the exact launch command and installed profile file hash in the operator receipt. That proves the main profile body reached the model; the operator receipt ties it to `--profile`. The current “Route: main session” text helps distinguish wrappers but is weaker than a versioned canary. Do not claim the rollout has a native profile-name field.

**unknown.** Whether an interactive `/debug-config` output would persist enough config-layer detail in the rollout was not tested; it is unnecessary for the canary witness.

## 4. Embedded-mode warning and tunnel coexistence

**said: `TEST-INSTALL` §X.2, 2026-10-13.** X2 displayed `Running without the shared background server: --profile requires embedded mode.` The profile session still completed on its own thread `01a13577…`. The X1 child belonged to a different head/thread; the tunnel's Cartan thread is a separate session.

**inferred: cartan.** The warning describes which server mode the profile process used; it is not evidence that the open tunnel owns or blocks this *new* Houston thread. Thread writer locks remain a concern when two clients try to write the **same thread**, not merely because both processes are open in the same repository. Keep the profile on a fresh thread; never resume/attach the tunnel thread from that process. Coordinate repository writes separately because different threads can still edit the same files.

**unknown.** No controlled simultaneous profile-plus-tunnel writer-lock trial was recorded. Do not infer general lock independence beyond the distinct thread IDs and X2's successful completion.

## 5. Held-seat release proof

**said: X1 rollout and Cartan observation, 2026-10-13.** The child's first answer carried the four stamp tokens and cwd. The held-seat release reply omitted stamps, but `followup_task` reused `/root/houston`; the parent/child SQLite edge and timestamps link its release to child rollout `01a13291…`. See `nablarva/.dev/observations/codex-houston-held-seat.cartan.2026-10-13.md` and witness X1.

**recommendation — inferred: cartan.** Binding entry proof in the first answer is sufficient for that entry. Do not require repeated tokens in every held-seat release. Require the carrier/release receipt to name the child thread or rollout and cite its first proof; if germline changed during the hold or a new card is selected, the child re-reads and supplies fresh stamps for the new move.

## 6. Rows still worth running before home migration

1. **Codex main after the real-directory move:** fresh `--profile houston` from Nablarva, explicit card, four exact reads/stamps and effective policy, plus the profile canary/launch receipt. This closes Q2 and profile provenance together.
2. **Child default and pen:** fresh child with no `card:` line should choose consult; a request to write outside consult should return `out of card:` without an approval escalation. X1 and R2 used explicit consult.
3. **Coexistence smoke:** with the tunnel thread parked, start a fresh profile thread, complete a read-only turn, then verify the carrier can resume its separate tunnel thread without a writer-lock conflict. Record both thread IDs. This tests the embedded-mode inference without touching shared files.

Office success does not substitute for home-host install verification after its own deploy and effective-policy check.
