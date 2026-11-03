# G06 coverage matrix (Flight pen)

Opened 2026-10-20 · Flight · identity check: 45/45 SHA256 OK at open (raw/SCOPE.md). Areas = RUNBOOK 1–7.
Disposition vocabulary: INSPECTED · G05 (accounted by checked G05 evidence) · EXCLUDED (reason) · UNVERIFIED (exact limit).
State column is the **opening** state; Flight updates it in place as returns are checked. Nothing below is a finding.

| id | area | surface | path (short) | G05 touched? | assigned | state |
|---|---|---|---|---|---|---|
| R01 | 1 | Sella GUIDE | reposoma/raw.guides/sella/GUIDE.md | full (F1–F5) | FG | INSPECTED (FG full + G05) |
| R02 | 1 | Forge GUIDE | raw.guides/germline-forge/GUIDE.md | full | FG | INSPECTED (FG full + G05) |
| R03 | 1 | Forge res/checks.md | …/res/checks.md | no | FG | INSPECTED (field report; key claims Flight-checked) |
| R04 | 1 | Forge res/fold-scheme.md | …/res/fold-scheme.md | no | FG | INSPECTED (field report; key claims Flight-checked) |
| R05 | 1 | Forge res/witness.md | …/res/witness.md | no | FG | INSPECTED (field report; key claims Flight-checked) |
| R06 | 2 | germline/CHATBOT.md | ia-sync/germline/CHATBOT.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R07 | 2 | germline/README.md | ia-sync/germline/README.md | full | FS | INSPECTED (G05 + FS re-read; deployed equal) |
| R08 | 2 | houston binding.claude | germline/agents/houston/binding.claude.md | stamps only | FS | INSPECTED (field report; key claims Flight-checked) |
| R09 | 2 | houston binding.codex | …/binding.codex.md | stamps only | FS | INSPECTED (field report; key claims Flight-checked) |
| R10 | 2 | houston card audit | …/cards/audit.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R11 | 2 | houston card consult | …/cards/consult.md | stamps only | FS | INSPECTED (field report; key claims Flight-checked) |
| R12 | 2 | houston card sitting | …/cards/sitting.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R13 | 2 | houston identity | …/identity.md | stamps only | FS | INSPECTED (field report; key claims Flight-checked) |
| R14 | 2 | skill.buffering-cycle | germline/skills/skill.buffering-cycle.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R15 | 2 | tunnel.preamble | germline/tunnel/tunnel.preamble.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R16 | 2 | claude houston wrapper | ia-sync/claude/agents/houston.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R17 | 2 | codex houston agent | codex/agents/houston.toml | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R18 | 2 | codex houston profile | codex/profiles/houston.config.toml | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R19 | 2 | codex oraculum agent | codex/agents/oraculum.toml | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R20 | 2 | claude oraculum agent | claude/agents/oraculum.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R21 | 3 | journal-continuity CONTROLLER | majkee/.germline/programs/journal-continuity/CONTROLLER.md | full | FS | INSPECTED (G05 + FS re-read; deployed equal) |
| R22 | 3 | fn/audit-beds | …/fn/audit-beds.md | NOT read | FS | INSPECTED (field report; key claims Flight-checked) |
| R23 | 3 | fn/carry-unfinished | …/fn/carry-unfinished.md | NOT read | FS | INSPECTED (field report; key claims Flight-checked) |
| R24 | 3 | fn/fold-entry | …/fn/fold-entry.md | full | FS | INSPECTED (G05 + FS re-read; deployed equal) |
| R25 | 3 | fn/list-pending | …/fn/list-pending.md | NOT read | FS | INSPECTED (field report; key claims Flight-checked) |
| R26 | 3 | project-saddle CONTROLLER | …/project-saddle/CONTROLLER.md | full | FS | INSPECTED (G05 + FS re-read; deployed equal) |
| R27 | 3 | fn/saddle-project | …/project-saddle/fn/saddle-project.md | NOT read | FS | INSPECTED (field report; key claims Flight-checked) |
| R28 | 4 | nablarva convergence.md | nablarva/.germline/agents/convergence.md | no | FS | INSPECTED (field report; key claims Flight-checked) |
| R29 | 4 | nablarva houston addendum | nablarva/.germline/agents/houston/nablarva.md | stamp only | FS | INSPECTED (field report; key claims Flight-checked) |
| R30 | 5/ctx | tunnel GUIDE | raw.guides/tunnel/GUIDE.md | no | FG | INSPECTED (field report; key claims Flight-checked) |
| R31 | ctx | invariance master-brief | invariance-autonomy/raw/master-brief.2026-09-23.md | no | FG | INSPECTED-BOUNDED (grep; context only) |
| R32 | ctx | G03 RUNBOOK | germline-03-foundation-audit/RUNBOOK.md | no | Flight | INSPECTED-BOUNDED (head/gate only; history; G03 gate untouched) |
| R33 | ctx | G03 STATUS | germline-03-foundation-audit/STATUS.md | no | Flight | INSPECTED-BOUNDED (gate/checkpoint/next; G03 A2 mapping pending Majkee — dependency, not resolved) |
| R34 | G05 | G05 RUNBOOK | germline-05/RUNBOOK.md | — | Flight | G05 (preserved; read by Flight) |
| R35 | G05 | G05 STATUS | germline-05/STATUS.md | — | Flight | G05 (preserved; read by Flight) |
| R36 | G05 | POINT.01 | _bus/POINT.01…md | — | Flight | G05 (preserved; read by Flight) |
| R37 | G05/6 | RETURN.01 (Cartan C1) | _bus/RETURN.01…md | — | Flight | ATTRIBUTED EVIDENCE (read; C1 consumed) |
| R38 | G05 | janus.c2.return | _bus/janus.c2.return…md | — | Flight | G05 (preserved; read by Flight) |
| R39 | G05 | oraculum umbrella | _bus/oraculum.assessment.umbrella…md | — | Flight | G05 (preserved; read by Flight) |
| R40 | G05 | findings.q1 | findings.q1.md | — | Flight | G05 (preserved; read by Flight) |
| R41 | 6 | grammar.builder.v4 | composer-01-parse/evidence/grammar.builder.v4.md | no | Flight | INSPECTED-BOUNDED (Flight: v4 §5 five required fields, unknown_key for program/function match Cartan RETURN; no parser tested) |
| R42 | 6 | brief.sella-germline-audit | composer-01-parse/evidence/brief…md | :99,:105-107 | Flight | G05 (preserved; read by Flight) |
| R43 | 6 | VIST principle | nablarva-X4-vist/raw/vist-01…md | no | FG | INSPECTED-BOUNDED (grep; context only) |
| R44 | 6 | Sublime IDE | termbrana-X3…/termbrana-X3-sublime-ide.md | no | FG | INSPECTED-BOUNDED (grep; context only) |
| R45 | G05 | raw/INPUTS.md | germline-05/raw/INPUTS.md | — | Flight | G05 (preserved; read by Flight) |
| E1 | 5 | Operation: journals 10-16, 10-17, 10-19§2 | reposoma/.majkee/journal/ | bounded | FS | INSPECTED-BOUNDED (briefs only; outcomes UNVERIFIED; 3 functions no use found) |
| E2 | 4 | Deployed copies (~/.germline, ~/.claude, ~/.codex) of named files | read-only compare | no | FS | INSPECTED (FS: 15 files source=deployed equal; read-only) |
| E3 | 4 | Retired/experimental role material, project addenda inventory | globs under named roots | no | FS | INSPECTED (FS inventory; convergence unmarked; sitting stub) |
| E4 | 1 | Vendor/platform claims (consequential only) | official docs | no | Flight→Epoch if needed | INSPECTED (Epoch, official docs 2026-10-21; changelog window limited) |
| E5 | 7 | C2 pilot proposal (germline-planning Cartan) | locate | no | Flight | UNAVAILABLE (no germline-planning bed/proposal found; mail inboxes unopened) |
| E6 | 4 | G01 install witness (Assay) | germline-01…/raw/witness.install-test.assay.2026-10-13.md | no (prep omission) | Flight | INSPECTED (full; added 2026-10-21 — RECONCILE.G01) |
| E7 | 4 | G01 TEST-INSTALL rows + transcripts pasted | …/raw/TEST-INSTALL.houston.2026-10-10.md | no | Flight | INSPECTED (full; .jsonl transcripts NOT replayed) |
| E8 | 2/4 | G01 deploy design (majkee GO 10-12 cited) | …/raw/design.global-germline-deploy.oraculum.2026-10-12.md | no | Flight | INSPECTED (full) |
| E9 | 4 | G01 MIGRATE (per-host steps; §3 retirement proposal) | …/raw/MIGRATE.germline.2026-10-12.md | no | Flight | INSPECTED (full; home steps not run — gap) |
| E10 | 4 | G01 fold witness + fold report (10-10 gavel citations) | …/raw/witness.fold.assay…md · fold-report.houston.atlas…md | no | Flight | INSPECTED (full; agent-authored citations, no operator receipt) |
| E11 | 4 | G01 C-def FAIL evidence | …/raw/evidence.c-def.houston-note.2026-10-14.md | no | Flight | INSPECTED (full) |
| E12 | 4 | G01 hook patches (basis of feedback §3.7) | …/raw/patch.hook-{subagent-exempt,tunnel-whitelist}.atlas.2026-10-13.md | no | Flight | INSPECTED-BOUNDED (grep: status line, §6/§7 only) |
| E13 | 4 | G01 Codex-side report (Cartan) | …/raw/report.codex-side.cartan.2026-10-13.md | no | — | UNREAD (cited by feedback; not consumed) |
| E14 | 7 | Oraculum install feedback (handover) | G06 raw/feedback.houston-install.oraculum.2026-10-21.md | — | Flight | INSPECTED (full; §3.7 corrected, attributed — RECONCILE §5) |
| E15 | 7 | Operator receipts D1/D2/D4 + myShell evidence review | ~/reposoma/.majkee/journal/2026-10-21.md §§1.1–1.4 | — | Flight | INSPECTED (full; receipts integrated into DEC.01) |
| E16 | 3 | PG-r3 GAVELS G4/G5/G6 + classmap guardrail (U3 lever check) | germline-02…/raw/GAVELS.program-guide-law.md :57–58, :98–107, :115–121, :128–131 | no | Flight | INSPECTED-BOUNDED (named passages only) |
| E17 | 3 | .majkee/AGENTS.md · engine/README.md · journal 10-16 :1535–1560, :1610–1630 | reposoma/.majkee/ | no | Field (U3) | INSPECTED (Field full; Flight spot-checks; unstamped) |

| E18 | 3/5 | myShell consumer experience (fold-entry outcome) + operator reactions (1)–(4) | ~/reposoma/.majkee/journal/2026-10-21.md §1.6; to-flight 2026-10-21 | — | Flight | INSPECTED (attributed; RESULT.U3 §9) |
| E19 | 3 | CLI/tool invocation-grammar conventions (parse-safety of `&`) | web, official docs | — | Epoch | INSPECTED (3 sources live-verified 2026-10-21; rest memory; _bus/epoch.grammar.U3.return.md; RESULT.U3 §10) |

| E20 | 4 | Fork git history (`5357179` 2026-10-14 wrote `.germline/tunnel/`) · nablarva X1 `tunnel.state.json:9` · archived ISS cards (migration-tail, deploy-before-commit) | reposoma git log; nablarva X1 bed; _cold-start/archive/ | no | Flight/Oraculum (U4) | INSPECTED (read-only; home host UNREACHABLE today → home state UNVERIFIED) |
| E21 | 4 | deploy.sh germline leg + profile leg · chatbot-port SKILLs (both vendors) · fork README | ia-sync | no | Field (U4) | INSPECTED (Field full; Flight spot-checks :217, :241; port destinations) |

| E22 | 4 | Project-layer inventory (globs under unikuklatrix, ia-sync, reposoma, projects) · nablarva AGENTS.md Houston paragraph · PROJECT.yaml :1–30 · flag L16 block · nablarva/.claude + .codex agent dirs | nablarva + globs | no | Field (U5) | INSPECTED (Field full; Flight spot-checks; R28/R29 re-read in full → INSPECTED (U5)) |

| E23 | 1 | guide-writing law staleness block · /guide SKILL organ behaviour · Sella L1–L9 + kernel/userland + :444–446 · Forge GUIDE whole + res/* whole (re-read for U6) | reposoma/raw.guides | partial (G05 F1) | Field/Oraculum (U6) | INSPECTED (Field full; Flight spot-checks; Forge raw/ observations + Sella src/raw receipts NOT read) |

| E24 | 5/7 | bus GUIDE · status GUIDE · runbook GUIDE (grep) · _mail/README · HANDSHAKE · cards audit/sitting whole · G05 POINT/RETURN headers · TEST-INSTALL C-def.2 block | reposoma/raw.guides, ia-sync | no | Field (U7) | INSPECTED (Field; Flight spot-checks bus :34/:52/:56/:82, identity :119–128, carry :25–27, mail :10–25; status GUIDE body + runbook GUIDE beyond grep NOT read) |

| E25 | 2 | Oraculum claude .md + codex .toml · role TOMLs (architect/challenger/researcher) · codex/AGENTS.md · raw.card.model-effort.md · agent rosters (globs) · commit 286085d diff | ia-sync, reposoma/raw.settings | no (R19/R20 FS) | Field (U8) + Flight git | INSPECTED (Field; Flight ran git show, verified pins/hook/sandbox_mode; astrobley.toml + other Codex-only TOMLs NOT read) |

| E26 | 6 | G05 C2 material (janus.c2.return whole; umbrella C2 grep; findings.q1 F1/C2) · G04 HANDOFF (grep) · tunnel preamble + GUIDE grep · feedback §3.9 · D2 wording · compaction-card globs (none) | ia-sync beds, reposoma | yes (G05 preserved) | Field (U9) | INSPECTED-BOUNDED (no experiment; tunnel res/preamble.md NOT read) |

CLOSE-STATE 2026-10-21: every row R01–R45 and E1–E26 carries a disposition; E5 stays UNAVAILABLE / NOT INSPECTED (inboxes unread, per Majkee); E13 UNREAD (Cartan Codex-side report); home host UNVERIFIED. Unit plan U1–U9 accounted (units/RESULT.U1–U9, units/RECONCILE.G01, units/INTEGRATED.recommendations.md).

U8 update 2026-10-21: R08/R09 bindings parity-graded; R19/R20 → INSPECTED (U8: dated cross-vendor divergence after 286085d; homonym); see units/RESULT.U8.md, decisions/DEC.05.

U7 update 2026-10-21: R10/R12 (audit, sitting cards) read whole → INSPECTED (U7); see units/RESULT.U7.md, decisions/DEC.04.

U6 update 2026-10-21: R01–R05 re-dispositioned INSPECTED (U6: proof-object re-read; chapter banners absent; :72–73 anti-pattern); see units/RESULT.U6.md, decisions/DEC.03.

U5 update 2026-10-21: R28 convergence.md — no retired marker, live activation clause :9–10; R29 nablarva.md — :131 stale vs :60, :86–90 live method in History block; see units/RESULT.U5.md, decisions/DEC.02.

U4 update 2026-10-21: R06/R07/R15–R18 confirmed source==live; R04 :26/:28/:31 stale (fork as source, "no deploy leg"); see units/RESULT.U4.md.

U3 update 2026-10-21: R21–R27 re-dispositioned → INSPECTED (U3: Field full read, Flight stamp grep 5/5 match, Oraculum assessment) — see units/RESULT.U3.md.

Legend: FG = field_guidance · FS = field_system (separate fresh instances, no cross-sharing before initial returns).

Pending rows at this update: E1 → INSPECTED-BOUNDED (briefs only, outcomes UNVERIFIED), E2 → INSPECTED (FS: 15 files equal), E3 → INSPECTED, E4 → INSPECTED (Epoch, official docs 2026-10-21; changelog window 2.1.246–2.1.305 only), E5 → UNAVAILABLE (see findings.g06.md).
