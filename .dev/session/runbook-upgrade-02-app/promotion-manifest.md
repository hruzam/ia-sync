---
session: runbook-upgrade-02-app
author: cartan-muticula · Codex · office
date: 2026-09-27
scope: authorized 182-path local preservation commit and verified host-local log retention
authority: majkee's explicit 2026-09-27 grant; exact closure-commit-paths.txt; no push
inventory: promotion-manifest.json
---

# Preservation manifest

Every file under `raw/` is a keeper. `promotion-manifest.json` individually identifies all
**215 raw files and 18 BUS receipts**, with SHA-256, byte size and preservation destination.
The Git-treatment fields describe the original pre-commit inventory, not current staging.
Root controls are listed separately to avoid self-hashing the manifest or mutable STATUS.

Majkee authorized one local commit of **exactly the 182 paths** already listed in
`closure-commit-paths.txt` (SHA-256
`deea48c9a5ff19809c8ceeba5e814c2bb92b33f6b4252ee4423a9b287d9f975b`), with no push.
The list is unchanged. All paths are below this bed; ignored logs, other sessions, pulse,
journal, live settings and deployable source are outside the commit. Unchanged tracked
keepers remain reachable in the same preserving commit.

For the committed copy, `<commit-containing-this-manifest>:<repo-relative-path>` is each
nonignored keeper's history locator. STATUS records the full verified commit id after the
transaction; before that receipt, authorization or staging is not a successful commit.
No temporary directory, SHA alone or planned Git locator is represented as a backup.

## Verified host-local log retention

Majkee selected the recommended host-local archive. The **25 Claude and 10 Codex JSONL files**
(**473,160 bytes**) were copied without changing or deleting their sources to:

`/home/hruzam/.local/state/muticula-evidence/runbook-upgrade-02-app/2026-09-27/`

Their bed-relative paths are preserved. All 35 destination SHA-256 values and sizes match
the source manifest. The archive's `archive-receipt.json` has SHA-256
`a887f43a3747b102b3aa859d8d2af2a8837fa873a30457d8adc05158812e74d4`;
its exact path, completion time and verification are also in `promotion-manifest.json`.
This retains decisive native outputs and guard events on office. It is **not a second-host
backup**. The `*.jsonl` exclusion is unchanged: no force-add, rename, packaging or ignore
exception was used. The manifest and evidence summaries can travel; the runtime logs do not.

## Evidence and current references

`VERDICT.md` is the bounded synthesis: Claude **qualified ACCEPT**, Codex **STOP**, with
failure/bypass, mode and isolation limits intact. B0 runners remain test evidence only;
`claude -p` cannot become a product dependency. All cycles and unsuccessful fixture preflights
are retained. No new model/CLI experiment was run for preservation.

The four Cartan records r3 cites stay at their original live paths and bytes. Trajectory's
four meeting-room relays moved, under the operator's separate clean-house instruction, to
`/home/hruzam/unikuklatrix/nablarva/.dev/session/muticula-00-brief/raw/relays/`.
The inventory retains the original snapshot paths plus verified current resolutions. The r2
master snapshot now resolves to `muticula.master.2026-09-26.reviewed-6db74151.md`; the live
master is r3. The copied closure relay under `raw/closure-source/` still matches its relocated
original. Frozen receipts keep their historical path text.

The successor RUNBOOK accepts the old bed's committed paths as the evidence home. Its owner
is Trajectory; Cartan is the standing witness. No evidence is copied into a new permanent
archive in nablarva. The operator may carry the existing experience transfer to the new head.

## Remaining retirement boundary

The old gate is retired as **gate-changed, unmet**; cycle07 stays withdrawn. Preservation does
not qualify the product. No move or prune of this bed is authorized here; existing r3 links
remain live. The ia-sync pulse row is outside this exact commit grant and remains unchanged,
as does the other session's pre-existing pulse edit. Its eventual retirement is separate from
this preserving commit. No push or deployment follows from the grant.

Rules applied: `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md`,
“receipts committed before prune” and “an explicit promotion manifest listing EVERY raw
keeper”; the fixed RUNBOOK prompt-0 separates Git, deploy and prune authority.
