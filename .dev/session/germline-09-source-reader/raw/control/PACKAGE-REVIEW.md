# Independent preparation review

2026-10-26 · native `/root/g09_package_review` · read-only review; not the future tunnel auditor.
No executor, product or tunnel was launched for this review. Returned report preserved below.

VERDICT: PASS

TASK: Verify the prepared G09 session-control package—not execution—for complete schedule/roles/tunnel loops, binding consistency, safe authority, bounded retries, cold/warm handling, audit closure, and honest measurement.

RAN: `find … -type f`; full reads of RUNBOOK/STATUS/ENTRY, SCHEDULE, ACCEPTANCE, TUNNEL, briefs, packets, control, and hold-line files; `jq`/Python JSON parsing; PyYAML fenced-block parsing; SHA-256/byte verification of all manifest pins; `wc -w`; `git status --short`/`git diff`; targeted `rg` and transport-source inspection.

EVIDENCE: All 9 JSON files and both YAML blocks parsed. RUNBOOK/STATUS gates match exactly. Initial packet is 701/800 words. All 28 actual source pins match; STATUS and RELEASE are deliberately unpinned. RELEASE remains `authorized:false` and requires actual GO. Cartan is the sole STATUS owner across RUNBOOK/task/RELEASE. ROUND-MAP binds five unique cycles, operation keys, compiled packets, results, and distinct role vaults. SCHEDULE/briefs give disjoint writes and substantive C1/C2, I1/I2, R1/R2, A1/A2 assignments. A3 is required after I2 product-map change; failed audit cannot close. Usage/main-token unknowns and receipt limitations are explicit.

FAILURES: none

REPRODUCE: `cd /home/hruzam/ia-sync && wc -w .dev/session/germline-09-source-reader/{RUNBOOK.md,STATUS.md} .dev/session/germline-09-source-reader/raw/hold-line/ENTRY.md`; parse every `*.json` with `json.loads`; parse each fenced YAML block with `yaml.safe_load`; recompute every `sources.json` SHA-256 and byte count.

RESIDUAL RISK: Runtime model/effort availability, sandbox facts, preamble consumption, and product behavior remain intentionally unverified until operator GO. Optional wording correction: TUNNEL.md:80 calls preamble arming “local-only,” while existing-vault `open` also performs a zero-turn server resume; this does not spend an ask or break the schedule.

## Parent disposition after review

Cartan confirmed the observation against `zsh/ai/tunnel-codex.py:735–752` and corrected TUNNEL:
the arming operation also resumes/stamps the existing born thread, with zero target turn.
Source pins were refreshed for that instruction-file correction and final static validation
repeated. The original PASS above is a preparation judgment, not a product/runtime witness.
