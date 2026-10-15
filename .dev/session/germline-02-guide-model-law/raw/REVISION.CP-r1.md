---
title: Cartan proposal-preparation checkpoint and verification boundary
revision: CP-r1
date: 2026-10-14
by: Cartan · codex · Medusa
authority: observed local checks; no independent review or final acceptance
scope: germline-02-guide-model-law
---

# Verified proposal-preparation edge

Office frame: hostname hruzam-120922, native /usr/bin/php74, valet path and MemTotal
16131320 kB agree. Worktree /home/hruzam/ia-sync, main at 2d6e14a. Office inbox is empty.
Advisory presence was attached as cartan at this bed using owned id
`a409df1ff08e859e9afdeaba7b5c4532`; existing attachments were not altered or interpreted as
authority. Presence lifecycle is independent of planning-gate closure.

RUNBOOK's gate and Cartan STATUS ownership agree with the existing snapshot. This deliberate
wake supersedes the parked hold that authorized only the two control files. Candidate evidence
is limited to this bed's raw/ plus the assigned STATUS replacement. RUNBOOK stays fixed.
The observed pre-existing dirty reconciliation retains accepted planning direction and exactly
its starting bytes. pulse has no germline-02 row; router maintenance remains outside authority.

Candidate set: PG-r1 proposal; AS-r1 accounting; GV-r1 gavel register; AB-r1 read-only Atlas
brief; CP-r1 this receipt. `SHA256SUMS.review` pins the exact five files. The manifest is an
identity receipt, not acceptance. STATUS is excluded because it is the live position.

Observed checks before final STATUS replacement:

- All 61 explicitly named input/control hashes in AS-r1 compare equal before/after drafting.
  This includes all 18 v3-tree files, both original bed-root ZIP containers, named planning
  inputs/current-law/native-door sources, fixed RUNBOOK and extra Sella/tunnel comparison inputs.
- Root v3 SHA256SUMS verifies 15/15 unique payloads at manifest digest
  `640e3069342c50165373bbe0730f8e15d53b378d36eb50b67498c714c687ff0d`.
  The accounting's 16 staged paths equal both disk inventory and the prior 16-row matrix.
  The extra path is the nested checksum file; it equals the root receipt. Root PACKAGE equals
  covered nested PACKAGE. Total v3 tree is 18 files, not 18 covered payloads.
- Candidate YAML headers, fenced blocks, revision identities and source paths pass inspection;
  AS-r1 has 43 distinct non-v3 source rows and 61 full identity rows. T1–T10 are present;
  all seven final gavel decision rows explicitly remain OPEN. P8 and audit-only next-sibling
  recommendation incorporate Majkee's extra steering.
- `git diff --check` passes. Scoped tracked live-surface diff is empty for germline, claude,
  codex, zsh, deploy.sh, pulse, AGENTS, SYNC_DISCIPLINE and host journal. The sole tracked
  changed path is the pre-existing reconciliation. New task artifacts are only inside this bed.
- No Atlas receipt exists. The brief is prepared, not delivered or consumed. No independent
  review result or final Majkee choice is inferred.

One preliminary verification expression counted a G1–G7 summary row as an eighth decision
and failed its assertion. The expression was narrowed to actual OPEN decision rows and the
full structural check passed. No candidate/source edit was required by that probe correction.

## Read-only source-retention recovery check

This command reads only AS-r1's exact named sources, never a sealed file or ZIP member.
It is a local verification probe, not an authored loader/program/census tool.

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, re
accounting = Path('/home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/ACCOUNTING.sources.md')
rows = re.findall(r'^([0-9a-f]{64})  (/[^\n]+)$', accounting.read_text(), re.M)
assert len(rows) == 61 and len({p for _, p in rows}) == 61
for expected, path in rows:
    assert 'hypotheses.reconcile-only.md' not in path
    observed = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert observed == expected, path
print('PASS: all 61 named input/control bytes retained')
PY
```

Separately check candidate identities with:

```sh
sha256sum -c /home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/SHA256SUMS.review
```

Changed candidate hashes require content/revision reconciliation and an affected review;
changed planning basis or live surfaces returns to Majkee before dependent work. A later Atlas
receipt must name these reviewed identities and actual cases/read limits; mere file presence
or an unqualified PASS is insufficient.

## Limits and retained holds

These are author's content/structure/retention checks, not an Atlas fresh-reader receipt.
T1–T10 are prepared paper predictions, not live behavior trials. Runtime loading, permission
enforcement, official vendor verification, compaction, whole-tree measurement and destination
placement are unperformed. No v3 install, subtree copy, executable/helper, loader, native skill,
agent/card/canon rewrite, deploy, git transport, conversion, new session, spawn or tunnel occurred.
The sealed hypotheses remain unread. Historical sources/extracted trees stay in place.

Majkee's next-session requirement is audit-only. P8 foundation and candidate programs are
review subjects; they neither canonize Sella nor select a tunnel-user skill for implementation.
The planning gate remains unmet pending independent Atlas review, Cartan's dispositions and
Majkee's explicit final decisions on the reviewed candidate. STATUS alone carries the next action.
