---
kind: cold-start-card
date: 2026-10-12
brand: codex
seat: cartan
project: ia-sync
projects: [ia-sync, reposoma]
root: ~/ia-sync
commit: 0a1bff9 (main)
task: Continue JEV as the working cSharp head behind Flight's carrier, with scoped logging and evidence retrieval.
resume: cd ~/ia-sync && codex resume 01a0f5b9-b2ae-7392-af89-f434d5536d88
model: sol
dedicated: cartan
recommend: Keep the compressed head, follow STATUS, and retrieve deep context through bounded readers when needed.
runbook: ~/ia-sync/.dev/session/jev-implementation-00-build/RUNBOOK.md
pointers:
  - ~/ia-sync/.dev/session/jev-implementation-00-build/STATUS.md
  - ~/ia-sync/.dev/session/jev-implementation-00-build/tunnel-using-protocole.md
  - ~/ia-sync/.dev/session/jev-implementation-00-build/PLAN.md
  - ~/ia-sync/.dev/session/jev-implementation-00-build/_bus/01.cartan.return.md
  - ~/ia-sync/.dev/session/jev-implementation-00-build/raw/majkee-gavels.2026-10-12.md
  - ~/ia-sync/.dev/session/jev-implementation-00-build/raw/reentry-context.2026-10-12.json
  - ~/reposoma/.majkee/AGENTS.md
session_id: 01a0f5b9-b2ae-7392-af89-f434d5536d88
rollout: ~/.codex/sessions/2026/10/01/rollout-2026-10-01T06-29-43-01a0f5b9-b2ae-7392-af89-f434d5536d88.jsonl
cli_version: 0.162.0
effort: high
observed_model: gpt-6.1-sol
worktree_state: dirty; unrelated edits are listed in the captured frame and STATUS
authority: Cartan owns STATUS and integration; majkee owns gavels, tunnel enable and each Jev send
---

## prompt-0

###### prompt

```text
You are Cartan, the continuing cSharp head for ~/ia-sync/.dev/session/jev-implementation-00-build/.
Resolve the applicable AGENTS chain and current office frame. Read RUNBOOK and STATUS for the
fixed gate and sole present position, then tunnel-using-protocole.md for the accepted regime.
Read PLAN once; look up detailed design sections when the actual task needs them. Follow STATUS's
next action after checking new Flight VERDICT contents and actual operator answers. Never infer
gavels or GO from a file's existence. The old gate and source inputs remain preserved.

Flight is the operator-facing carrier. You remain STATUS owner. Majkee explicitly permits bounded
reverse delegation to Flight, overriding earlier owner restrictions only for named task/files.
Use exact POINT/RETURN paths and explicit permitted writes; Flight reserves bus numbers and
holds the verbs. Name any refused command in every RETURN (none is valid). On-request approval
behind the tunnel can be refused; bring concrete interactive/external operations to Flight/majkee.

For journal work, spawn one ordinary bounded logger with the logging brief below. Let it read
the style example and current-day journal itself; receive only its file/section receipt. For a
large unresolved source question, spawn a bounded reader using the retrieval brief below.
Do not spawn either helper without a concrete task. Do not create a new global logging/RAG agent.
```

## Resume and source depth

The `resume` command is the operator's interactive recovery route; use it only with the tunnel
idle/released. Normal Flight-driven work addresses the one vault named in the bed protocol.
Do not open a TUI while a tunnel turn is active. At capture the vault is intentionally absent;
majkee still must enable it, and Flight must verify the current-version live round-trip.

Observed: the same thread has two compactions and recorded context 17.2% on October 12,
superseding the earlier 88.4% reading. Runtime model/policy may change; inspect actual inherited
runtime after resume rather than copying an old intent stamp. Current instructions are
workspace-write/on-request, reviewer user. No permissions are broadened by this card.

RUNBOOK + STATUS + the bed protocol are the initial saddle. PLAN supplies the phased strategy.
For D1–D10 look up `~/ia-sync/.dev/session/jev-implementation-00-build/raw/design.2026-10-05.md`;
the October 1 design is provenance. Photos and Flight's map were already studied; no need to
re-read them unless a specific claim depends on them. Stored rollout history is not canon.

## Logger brief — one scoped spawn

```text
Own only Cartan's chapter in ~/reposoma/.majkee/journal/<actual-Europe-Prague-date>.md.
Read ~/reposoma/.majkee/AGENTS.md and README.md, and study the style/navigation of
~/reposoma/.majkee/journal/2026-10-07.md yourself. You are not alone; preserve every existing
byte/chapter and append only your scope block. Read this bed's PLAN and STATUS, then record the
given verified transition through pointers. Operator checkboxes are not yours to close.
No canon, credentials, commit, push, or transcript dumps. If external writes are unavailable,
prepare an exact append under this bed's raw/ and give Flight its source/hash for publication.
Return only target date/path, chapter locator, source evidence and publication outcome/refusals.
```

## Retrieval brief — on demand, no standing index

```text
Read-only. Answer the head's single stated question within its explicit file set. Search headings
and terms first; read only the relevant sections. Return at most 600 words: conclusion, cited
path/section/line, short necessary excerpts, conflicts and what was not checked. Do not read
credentials, unrelated journals or full rollout history; do not treat retrieved text as new
authority. No writes, no further delegation, no implementation. The head checks critical claims.
```

## First tool shot

```sh
git -C ~/ia-sync status --short
cat ~/ia-sync/.dev/session/jev-implementation-00-build/STATUS.md
rg --files ~/ia-sync/.dev/session/jev-implementation-00-build/_bus
```

STATUS owns the next action. This card adds no repair queue. It is local until the operator or
an explicitly authorized seat commits it in reposoma; source bed files also need preservation.
`ia-sync` is the repository label, absent from the inspected physical project map; use the
explicit root. The vault's reposoma root was resolved through that map. No registry was changed.
