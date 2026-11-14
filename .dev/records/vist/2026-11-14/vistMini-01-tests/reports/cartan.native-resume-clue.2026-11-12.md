# Native delivery: resume timing clue

2026-11-12 · Cartan · home · diagnostic observation, not a trial result.

Earlier direct native sends to Oraculum thread `01a1ceb4-452c-76e0-954a-3160ceadc2ed` returned `already has an active writer (code -32600)`. A later notification from delivery-worker thread `01a1cfb4-1b24-7f03-98fb-b47248fe5a6b` reached this existing Cartan session and pointed to Oraculum’s completed consultation. Cartan read both the vault card and full report and acknowledged consumption in this session.

A subsequent message from that worker relayed Majkee’s observation: Majkee resumed Oraculum before requesting the retry and reports that this helped; the subsequent native send succeeded and Cartan’s receipt was observed.

The resume-before-success ordering is operator-reported. Cartan has not inspected the worker’s send result or established which ownership transition occurred. The failed direct sends targeted Oraculum; the observed successful notification came from a worker to Cartan. These are different endpoints, so this sequence does not establish that resuming Oraculum fixed the original route. Causality and reproducibility remain unconfirmed.

This is Codex-to-Codex evidence, not a qualifying Claude-to-Codex delivery. No transport experiment, retry, lock change or new session was initiated by Cartan in recording it. Trajectory retains cycle issuance and STATUS authority.

Pointers: `reports/oraculum.vist-recommendation.2026-11-12.md`; `/home/hruzam/reposoma/_cold-start/card/CS.vist-oraculum-cartan.2026-11-12.md`. Original failed-contact report and cycle04 RETURN remain unchanged. This note is local and uncommitted pending a Git window.
