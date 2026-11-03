# BRIEF U4 → field (Flight, 2026-10-21) — deploy, source of truth, drift, consumers
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch, no deploy/dry-run execution.

## Read in full (absolute paths)
1. /home/hruzam/ia-sync/deploy.sh (whole; focus: header comments :1–60, `copy_file` :100–115, `deploy_germline` :140–225, Codex legs :230–250, main sequence :265–290)
2. /home/hruzam/ia-sync/germline/README.md
3. /home/hruzam/ia-sync/germline/CHATBOT.md
4. /home/hruzam/reposoma/.germline/README.md (the fork's README — compare with 2)
5. /home/hruzam/ia-sync/claude/skills/chatbot-port/SKILL.md and /home/hruzam/ia-sync/codex/skills/chatbot-port/SKILL.md (where the "port home" points)
6. /home/hruzam/ia-sync/SYNC_DISCIPLINE.md — only the germline-bearing passages (grep `germline`; read ±10 lines around :20 and :92) and its dead-edit rule
7. /home/hruzam/ia-sync/AGENTS.md — the `~/.germline — a deploy target` section only
8. /home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/MIGRATE.germline.2026-10-12.md (whole) and …/raw/design.global-germline-deploy.oraculum.2026-10-12.md §§3–5 only
9. /home/hruzam/ia-sync/journal.host-cleanup.md — the `OFFICE — 2026-10-12` entry (≈ :38–70) and any later line mentioning germline/home migration
10. Cold-start cards: locate `ISS.germline-migration-tail.2026-10-14.md` and `ISS.germline-deploy-before-commit.2026-10-14.md` under /home/hruzam/reposoma/_cold-start/{issues,routines,archive}/ — report WHICH folder each sits in (folder = state) and read both.
11. /home/hruzam/reposoma/raw.guides/germline-forge/res/fold-scheme.md :20–32 only (the stale location/symlink claims — already a known finding; needed as a consumer pointer).
Facts you may rely on (Flight-checked today, do not re-run): `diff -rq ia-sync/germline ~/.germline` = no differences; the three Houston wrappers are byte-equal source↔live; fork `~/reposoma/.germline/` differs from source in exactly 6 files (README, identity, binding.claude, binding.codex, cards/consult, tunnel/tunnel.preamble) and CHATBOT.md + skills/ are equal; `~/.germline/programs` does not exist; office migration done 2026-10-14 (journal :53), home pending.

## One question
What is the complete deploy/source-of-truth model as the files state it — source, targets, legs, holds (fail-closed, adopt, ghosts), what is additive vs deleting, what is hand-installed vs deployed — and who are ALL the consumers of each copy (deployed `~/.germline`, the reposoma fork, GitHub `hruzam/reposoma` for chatbots, Forge pointers, chatbot-port skills)? Then: which written claims about deploy/source are stale or contradictory today, and which prerequisites MIGRATE §3's retirement needs that are not yet met.

## Hypotheses to TEST (evidence for/against; no conclusion)
H1 Every consumer pointer resolves to ia-sync source or deployed `~/.germline` — except CHATBOT.md (fork) and Forge R04 (fork). List any other pointer still naming `~/reposoma/.germline`.
H2 The stamp rule scope: README says every loaded germline file carries `stamp:`; skill.buffering-cycle.md and tunnel.preamble.md carry none. Quote the README sentence exactly and say which files it literally covers.
H3 `deploy.sh` germline leg never deletes (ghost inventory only) — so a file removed at source lingers live; is a retirement procedure written anywhere (SYNC_DISCIPLINE, README, MIGRATE)?
H4 Home-host readiness: MIGRATE §2 steps + the "Known window" + TEST-INSTALL §5 pull order — what must be true on home before `deploy.sh` runs there, as written; what the ISS cards record as done/pending.
H5 Chatbot route: CHATBOT.md tells a chatbot to read `hruzam/reposoma` `.germline/` via GitHub connector or hand-drop. Does any file state how that copy is refreshed, who owns it, or that ia-sync is private/accessible to a connector? Quote or report absence.
H6 MIGRATE §3 retirement prerequisites as written vs the live consumers found in H1/H5: list each prerequisite and whether a document says it is met.

## Return shape (write yourself, verbatim, to the path below; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U4.return.md — header `from: field · unit U4 · date`, then:
A. Deploy model table (per copy/target: source · mechanism · additive/deleting · holds · hand vs script · documented in).
B. Consumer map (consumer → which copy it reads → pointer location + quoted text → current/stale).
C. H1–H6 evidence tables.
D. Stale/contradictory claims (file:line, quote, what is true today per the facts above).
E. MIGRATE §3 prerequisite checklist (prerequisite · source · met? · evidence).
F. Friction for an agent/operator consumer (ranked, cited).
G. Uncertainty / not-read.
Bounds: ≤ 3,500 words; quote text with each line ref (line numbers from files as read today); separate authored / deployed / historical / proposed. Stop when A–G are filled.
