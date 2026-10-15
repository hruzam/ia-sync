---
title: Cartan verified Atlas-reconciliation checkpoint
revision: CP-r2
date: 2026-10-14
by: Cartan · codex · Medusa
authority: local verification and consumed AR-r1; no independent r2 PASS or final gavel
scope: germline-02-guide-model-law
---

# Verified reconciliation edge — CP-r2

Office frame remains hruzam-120922, native php74/valet and RAM 16131320 kB; repo main at
2d6e14a. The original tracked dirty reconciliation is retained exactly against its AS baseline.
Only this proposal bed's evidence/STATUS are authored. RUNBOOK, live surfaces and other work
remain unchanged. Advisory presence for this reconciliation used owned id
`8a9493b2271b7c0d0467bbeddfee696c`; no presence claim grants task authority.

AR-r1 has been received through Majkee and read by Cartan. Its exact receipt remains unchanged
at Atlas's owned path, digest 797614f708ad5a125a6b1b693ad83573d072464f6bb4076c3d11e91b00532c5b.
Its verdict is narrow FAIL, and DR-r1 records every P1–P5/A1–A3 disposition and retained limit.
No Atlas r2 addendum or final G1–G7 ruling exists yet.

Current candidates are PG-r2/AS-r2/GV-r2/AB-r2/CP-r2 plus DR-r1. SHA256SUMS.review identifies
these six and seven retained r1 evidence files: five candidate snapshots, original Atlas
snapshot and original manifest. It is a 13-file identity receipt, not an independent review.
Atlas's live receipt and STATUS remain outside that manifest because their next authorized
writers will advance them. The immutable r1 receipt snapshot stays covered.

## Observed verification

- The original 61 input/control hashes match the first wake's baseline; six additional
  unsealed A1 input hashes match before/after reconciliation. AS-r2 has 67 unique identities.
  The sealed old-raw file is accounted as B50 by name/existence only and is never opened/hashed.
- All 14 regular files directly in the old bed's raw/ are represented: 13 unsealed inputs plus
  the sealed name-only row. S01–S16 remain the exact 16 staged files. Both root files are named;
  v3 contains 18 files total, with 15 root-covered payloads verifying OK.
- Nested/root manifests and PACKAGE equality remain valid. B46–B48 equal their three v3 review
  copies by direct byte comparison. B49's pre-ruling conditional countersign differs from
  S02's post-ruling SIGN; only S02 carries the adopted whole-tree-first R2 provenance.
- Name-only ZIP inspection counts 18 v3 archive files versus 14 earlier-table archive files;
  neither archive has a sealed member. Whole-container hashes identify bytes, not payload
  equivalence or ZIP integrity. No archive member was opened or extracted.
- Six REVISION.*-r1.md snapshots match r1 candidate/receipt identities; SHA256SUMS.review.r1
  equals the original manifest digest. Atlas's actual receipt is unchanged.
- PG-r2 explicitly holds all-scope table/file stamp mismatch without caller pin; T1–T12 exist.
  Seven final gavel rows remain OPEN. Candidate YAML/revisions/fences and source path coverage
  checks pass. DR-r1/AB-r2 declare changed-section re-review and unchanged-text carry-over limits.
- Scoped tracked live-surface diff is empty and git diff --check passes. The pre-existing
  reconciliation remains the only tracked changed path; new evidence stays in this bed.
- No proposal recommendation is final law. Foundation seams and tunnel candidates remain audit
  subjects; the next separately authorized numbered session is still audit-only.

## Read-only recovery probes

Candidate/snapshot identities:
```sh
sha256sum -c /home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/SHA256SUMS.review
```

Exact unsealed source retention and sealed-name coverage, without reading the sealed file:
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

Read the contents and actual revision coverage of Atlas's receipt, not just its presence.
AR-r1's FAIL remains until Atlas appends an AR-r2 finding on the new candidate identities.
Its original hash may then change legitimately at its sole-owned path; inspect the dated
addendum and compare its preserved original section to REVISION.AR-r1.md. A changed candidate
identity needs content/review reconciliation; a changed planning basis or live surface requires
Majkee's direction and full re-review. No receipt or gavel is inferred from silence.

## Limits

All r2 corrections are author-verified proposals, not an independent PASS. Runtime loading,
effective permissions, compaction, official vendor facts, whole-tree measurement and destination
placement remain unperformed. AR-r1's source-read and interest limitations are preserved.
No spawn, tunnel, executable/helper, loader, source/canon/native/card edit, deploy, commit, push,
conversion, cleanup or new session was performed. Originals and extracted trees remain in place.
The planning gate stays open pending r2 review, disposition and Majkee's final explicit gavels.
STATUS alone carries the next action.
