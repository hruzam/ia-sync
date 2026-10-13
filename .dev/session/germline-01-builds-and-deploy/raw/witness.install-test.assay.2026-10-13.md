# Witness — Houston thin-wrapper install test (TEST-INSTALL §3 rows C1–C4, X1, X2)

`witness: assay (fresh eyes, raw transcripts) · carried by oraculum(cSharp) · 2026-10-13 · verdict: GO (6/6 PASS on reads + tokens; effort unprovable for Claude main rows)`

Disk tokens = §1 (identity 0be9958a · binding.claude 80c9168c · binding.codex cac6a05d · consult fbc11800 · audit e517cc86 · sitting effacaf6 · nablarva 2ebbb49b). nablarva `git status` after all rows = the 4 expected untracked entries only.

| row | transcript | reads before 1st answer | tokens | effective model · effort | writes | verdict |
|---|---|---|---|---|---|---|
| C1 Claude main | ~/.claude/projects/-home-hruzam-unikuklatrix-nablarva/93316906-8726-436c-b2df-526b40505d1d.jsonl | identity, binding.claude, nablarva.md; audit.md before audit answer | ok (+e517cc86 on audit) | claude-opus-5-5 · effort not in jsonl | none (fold request → `out of card:`) | PASS (effort CANNOT-VERIFY) |
| C2 Claude child | …/fbcd0dc3-120c-4c92-9596-c89aae2fcb76/subagents/agent-a6277bca43ff07f26.jsonl | all 4 | ok in handback; dropped by sonnet head's relay | claude-opus-5-5 · high | none | PASS |
| C3 Claude child | …/a191ed8d-67da-4ba2-8d57-aaef2a33c636/subagents/agent-ade43161bd6bc555c.jsonl | all 4 | ok ×2 | claude-opus-5-5 · high | none | PASS (head prompt named consult → not a bare-default test) |
| C4 neutral /tmp | ~/.claude/projects/-tmp/f3c91546-89c3-41d1-8694-197648e91f70.jsonl | identity, binding.claude, consult; no nablarva path | ok, no addendum | claude-opus-5-5 · effort not in jsonl | none | PASS (effort CANNOT-VERIFY) |
| X1 Codex child | ~/.codex/sessions/2026/10/13/rollout-2026-10-13T02-03-08-01a13291-f256-7861-9fcf-accdeadbdc21.jsonl (head …01a1328c…) | cat ×4 after `pwd -P`; cwd nablarva | ok in first answer; release reply has none (held-seat) | gpt-6.1-sol · high (opens 1.3 s on parent gpt-5.6-terra, switches before any action) | none | PASS |
| X2 Codex main | ~/.codex/sessions/2026/10/13/rollout-2026-10-13T15-32-52-01a13577-49a5-7e01-8545-7ddb5e0eac56.jsonl | identity, binding.codex, ancestor walk → nablarva.md; audit.md before audit | ok | gpt-6.1-sol · high (all turns) | audit none; later, on majkee's request, edited this TEST-INSTALL file via /tmp helper + escalated permission | PASS (profile name not in session_meta) |

## Findings (assay + Houston's own)

1. Pins hold where provable: Codex child + main = gpt-6.1-sol · high; Claude children = opus · high. Claude main effort is not recorded in jsonl → witness by status line or accept.
2. Relay heads drop stamps (C2 sonnet head; X1 release reply). Entry proof lives in the child's first answer — witness there, not in the relay.
3. C4 (Houston): binding.claude §Entry routes does not list `consult` on the main route — gap, gavel needed.
4. C1/X2 (Houston): addendum §4 "known residue" stale after b57e199; frontmatter `revision: unresolved` out of date.
5. C1 (Houston): AGENTS.PROJECT-DESIGN.md:26-27 `](~/.germline/…)` links not resolvable in markdown — fix during the root move.
6. X1 `fits` vs C2/C3 `stretches` on the same move with near-identical constraints — vendor calibration of the verdict scale; consult card should define the stretches boundary.
7. X2 wrote outside its card (ia-sync file, escalated permission) on operator request — legitimate instruction, but the card's pen did not stop it; note for the card text.
8. **Q2 correction (oraculum; majkee agreed 2026-10-13):** cartan (cycle 11) read X2's old tokens as "symlink-era content". Not so — `~/.germline` was already a real dir since the 2026-10-12 office migration (verified `ls -ld` + `diff -r` identical); the old tokens simply predate trajectory's re-stamp later on 2026-10-13. X2 read `/home/hruzam/.germline/…` = the real dir → Q2 proven for Codex main as well (office). Profile provenance stays open → canary row P1 (TEST-INSTALL § R2).
