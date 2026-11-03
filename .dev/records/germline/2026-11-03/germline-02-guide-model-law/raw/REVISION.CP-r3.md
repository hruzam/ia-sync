---
title: Cartan AR-r2 consumption and gavel checkpoint
revision: CP-r3
date: 2026-10-14
by: Cartan · codex · Medusa
authority: local checks plus consumed independent AR-r2; no final gavel
scope: germline-02-guide-model-law
---

# Verified edge — AR-r2 consumed

Office host hruzam-120922, native php74 and RAM 16131320 kB agree. Repo main remains 2d6e14a;
the original dirty reconciliation matches its baseline. Fixed RUNBOOK/STATUS ownership and
raw-only write authority remain unchanged. Current advisory attachment was declared under
owned id 18fa609827cf09b252a7c0edfe186813; it is not authority or a liveness proof.

Atlas's live receipt has returned SHA-256
`ced6030472df34ceb353891fee9a066a48684f1f99e1dd42e9a439d2eb735b02`.
Its original AR-r1 byte prefix matches REVISION.AR-r1.md. AR-r2 content independently PASSES
reviewed PG-r2/AS-r2/GV-r2, clears A1 and resolves/routes P1–P5/A2–A3. DR-r2 records each
disposition and both low findings. Atlas's receipt is not edited by Cartan.

PG-r2 remains exactly reviewed. AS-r3 withdraws F-r2-1's unsupported extraction-location
wording; GV-r3 updates receipt metadata only, keeping all seven candidate rows OPEN.
The current manifest pins current evidence and exact reviewed r1/r2 snapshots. Returned
review bytes are separately preserved in REVISION.AR-r2.md; the live review and Majkee's
future decision note remain outside the manifest because those writers own them.

## Verified local checks and explicit uncertainty

- Before mutation, r2 manifest verified 13/13 entries at
  5cbaf9bcc2702e8e43fd5677c11c6b35ce67ba3165bcf29212678f894f68fa87.
  R2 snapshots preserve every reviewed bundle artifact and that exact manifest.
- The 67 unsealed source identities remain equal, with 14/14 old-raw path coverage and B50
  name/existence only. No sealed path is in the checksum set. S01–S16 and both v3 root files
  remain accounted; original source/archive/v3 payload bytes are not changed.
- The actual v3 extraction is
  `/home/hruzam/ia-sync/.dev/session/guide-model-01-law/raw/guide-model.table.2026-10-13-v3/`.
  It exists and its 15 covered payloads retain the original manifest identity.
- The earlier symmetry package is catalogued by B15, but its extracted location was not found
  at `/home/hruzam/ia-sync/.dev/session/guide-model-01-law/raw/symmetry-drop-2026-10-13/guide-model/`;
  no other extraction location is inventoried here. Atlas reports no match under /home/hruzam.
  This session does not claim an independent full-home search or preservation of an unlocated
  tree. The original archives and the identified v3 tree remain retained.
- F-r2-2: prior attachment 8a9493b2… is not independently attestable at review time, note only.
  No retrospective presence record is recreated and no receipt/authority is inferred from it.
- No decision note exists. Seven G1–G7 rows remain OPEN, with no final Majkee words/date or
  reviewed-revision acceptance inferred from the current wake.
- Scoped live-surface diff is empty; original reconciliation is the sole tracked dirty file.
  Current author edits and retained snapshots are confined to this bed's raw/ plus STATUS.

## Read-only recovery

```sh
sha256sum -c /home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/SHA256SUMS.review
```

The exact source/name probe excludes sealed content:
```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, re
accounting = Path('/home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/ACCOUNTING.sources.md')
text = accounting.read_text()
rows = re.findall(r'^([0-9a-f]{64})  (/[^\n]+)$', text, re.M)
assert len(rows) == 67 and len({p for _, p in rows}) == 67
for expected, path in rows:
    assert 'hypotheses.reconcile-only.md' not in path
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
old = Path('/home/hruzam/ia-sync/.dev/session/guide-model-01-law/raw')
sources = re.findall(r'^\| B\d+ \| `([^`]+)` \|', text, re.M)
actual = {p.name for p in old.iterdir() if p.is_file()}
named = {Path(p).name for p in sources if Path(p).parent == old}
assert len(actual) == 14 and actual == named
assert re.search(r'^\| B50 .*SEALED, UNREAD.*$', text, re.M)
print('PASS: 67 unsealed identities retained; all 14 old-raw names accounted; seal remains unread')
PY
```

Read Atlas's actual receipt/addenda against REVISION.AR-r2.md. A later one-line F-r2-1 check
must identify corrected AS-r3/CP-r3 bytes; it is a wording check, not a new law review.
The prepared CHECK-BRIEF.atlas.F-r2-1.md supplies exact hashes and requested check.
Source/candidate changes require content/revision reconciliation; changed B1/B2 basis or
live surfaces require Majkee's direction and full re-review.

## Limits and closure

Atlas AR-r2 paper PASS does not prove native loading, effective permissions, compaction,
official vendor facts, deployment placement or the whole-tree audit. Those remain unperformed.
F-r2-1's correction is author-checked and awaits the one-line Atlas check. G1–G7 decisions and
explicit acceptance are absent; the gate remains open. A note choosing amended candidate text
requires an affected Atlas check before acceptance. The later sibling remains audit-only,
recommended conditionally and never opened here.

No canon/germline/skill/agent/card edit, loader/helper/program, install, deploy, commit, push,
conversion, cleanup, spawn or tunnel. No originals are moved or removed, the identified v3
extraction is retained, and the unlocated earlier extraction is not claimed to be in place.
The seal remains unread and unhashed. STATUS alone carries the next action.
