---
what: walkable test pad for the @ferry agent (first crossings after deploy)
state: parked — walk when ready; each station records a verdict (L8 receipts)
verified: 2026-08-03
next:
  - "walk S0→S2 anytime (safe, report-only)"
  - "S3 after operator wants code parity; S4 after operator legs (.env, dump, intl)"
  - "record verdicts in the log at the bottom; pad stays until G3 confirmed"
---

# ferry.test-pad — stations

Law: order, not channel — issue orders from any seat (interactive `--agent ferry`,
or spawned as a subagent). Never bind the test to a CLI flag.

## S0 · preflight (office, no ferry)
- [ ] `ls ~/.claude/agents/ferry.md` — deployed
- [ ] `git -C ~/www/imago_cz/freya.devenv log --oneline -1` — mechanism commits present
GATE: both exist.

## S1 · report-only crossing
- [ ] Order: `status freya`
- [ ] Expect: `FERRY freya G<n>` + next-blocker + whose (likely: .env / php-intl → OPERATOR)
- [ ] Verify nothing changed: `git -C ~/www/imago_cz/freya status --short` identical
      before/after; same on home app repo.
GATE: grade reported, zero mutations.

## S2 · mechanism direct (home, bypasses ferry — isolates script from agent)
- [ ] `ssh hruzam@100.110.27.60 'bash ~/www/imago_cz/freya.devenv/ferry/prep-home.sh check'`
- [ ] Expect [OK] app/devenv/composer/npm/mariadb · [MISS] .env, php-intl
GATE: output matches known reality; no false [OK].

## S3 · code leg (mutating — pulls only, ff-only guarded)
- [ ] Order: `run freya to G1`
- [ ] Expect: office push confirmed with you first (never blind add); home ff-only pulls;
      devenv deploy; drag-lane inventory listed
GATE: `FERRY freya G1` + home repos current.

## S4 · after operator legs (.env drag · dump import · php-intl)
- [ ] Order: `run freya to G3`
- [ ] Expect: config+boot stages pass; serve URL reported
GATE: browser on home renders freya = G3 confirmed → this pad may die.

## Verdict log (L8 — the receipt IS the trust)
| date | station | model | verdict |
|---|---|---|---|
| 2026-08-03 | S1 report-only crossing (subagent spawn) | ferry@sonnet/high | **PASS** — G0 BLOCKED correctly (develop-first law: office on `majkee-predev`, 158 behind / 1 ahead of develop); zero mutations; all 4 repos fetched-real; drag-lane listed (.env office-only, meili parked); deploy-guard stale-stamp read as guard-working; raised exactly one operator question |
| 2026-08-03 | S3 code leg (operator-ruled merge) | ferry@sonnet/high | **PASS → G1** — origin/develop merged into majkee-predev CLEAN, no conflicts (44801f111), no push, cruft untouched; home app ff→parity (118 commits); home devenv ff→core (mechanism arrived). Found real defect: registry.json lacked hostname keys for non-interactive ssh (no MACHINE_NAME) — fixed durably d82c0a8, ferry resumed on-line to retry deploy leg. RETRY: key resolution works; deploy-guard fired on stale stamp, correctly not forced. STRUCTURAL: guard is same-host-shaped — cross-host stamp will always mismatch (office=predev, home=develop) → operator ruling queued (per-host stamp vs force-ritual); non-blocking for G2/G3 |
