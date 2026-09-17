# fork handover — from the withdrawing Oraculum window to the resumed head

`class: handover note, thin. Two live instances of one name existed 2026-09-14 (this original window`
`+ the resumed sitting in majkee's second terminal column). G-43: identity rides the work, not the`
`process; both are real; withdraw the empty hand from an already-held task. The resumed sitting holds`
`the work (row 0 recorded, STATUS rewritten) → it is the head. This window wrote this note and stopped.`
`It did NOT touch STATUS.md or res/trial.md — one writer. Nothing in flight from this window.`
`majkee wording for the boot session: "ff-sync.trajectory-incarnation-copartner" (read as his fc-sync.*`
`session naming; the string is present in the transcript below — verified by grep, content not read).`

## 1 · What this window did after the fork point (2026-09-13 → 14) that the head may not have

- **reposoma:** committed the CS card only — `58ba151` on `core`
  (`_cold-start/card/CS.incarnations-00-head.2026-09-11.md`, 86 lines). Untouched remainder there was
  other seats' state (presence churn, a CS card mid-drain, `_mail/cartan/inbox/`).
- **ia-sync — a race, priced:** the bed and the router line had already been committed by majkee on
  09-12 (`e69837f`). My Delta brief, designed against the 09-11 snapshot, took `HEAD:pulse.md` (which
  already held the router block) and appended it again → spurious commit `69d8e23` = a duplicate
  6-line block, nothing else. Two guarded fix runs halted correctly: the first on my own count error
  (the slug appears TWICE per block — 2/4/2 was one/two/one blocks), the second because majkee's live
  commit `442e6c9` ("2026-09-13 .dev/session/remote-cli") had already overwritten the duplicate with
  the single-block working tree. Net: HEAD clean, one block, tree clean. History keeps the harmless
  pair; not rewritten (would rebase majkee's commit). Nothing pushed by this seat.
  Receipt majkee can run: `git -C /home/hruzam/ia-sync show HEAD:pulse.md | grep -c incarnations-00-mechanism` → `2`.
- **Scar (mine, for the transfer letter):** *a delegated write designed against a stale snapshot; two
  days passed and I did not re-read state before acting; then I raced a live operator session twice.*
  Price: one spurious commit, three Delta runs, one afternoon of majkee's attention. Rule: every
  delegated write brief opens with a read of the CURRENT state and a stop condition on it — never a
  memory of the last state; and no writes into a repo where a live session is committing.

## 2 · Four doctrine leans given in chat 2026-09-13 (majkee's questions) — not locks

1. **Per persona or per gavels for all?** Both, by layer: the gavel bed is for all (`gavels.md`,
   de-specified, any seat reads); inheritance is per persona (a seed points only at what bends THIS
   seat's hand; birth keyed on a NATIVE scar per L1, content may point at any gavel); scope-seeds
   (`scope:`, L6) inherit per posture. Bed for all · seat-seed per persona · scope-seed per posture.
2. **All therapies per persona?** Never loaded whole, never a seed. Therapy feeds forward through two
   organs only — `/gavel-interpreter` at arc close and the seed's curated pointers. Across all
   therapies: only L7 tier 2 (attended Agol composing OVER them, never rewriting — Class I). Drift per
   persona = the anchor test (card §5). Under A0, nothing more.
3. **Shadow vs real.** Law is in `raw.therapy/README.md`: a shadow is described as a candidate, never
   appended; majkee decides. Only a REAL gavel has a G-ID → only real gavels can be inherited. Lean:
   recurrence across two arcs is the natural trigger to present a shadow for lock (the bed already
   shows "shadow confirmed by recurrence → lock").
4. **A vault for gavel loops — per project or temple?** No. Two beds already hold decisions (project
   `flag.md` · temple `gavels.md`); a third store is a third authority. What this session exposed is
   ia-sync lacking a `flag.md` — fixed by a convention, not a vault: *session-record ledger, promoted
   at gate close*; one GUIDE line when a third project hits it. The vault that IS right for loops is
   the existing `_cold-start/routines/` — the weekly Agol pass (L7) is an RT card.

## 3 · Owed folds for the head (its cells, its writes)

- **Row-0 transcript pointer (majkee's ask 2026-09-14):** track file, point never copy —
  `/home/hruzam/.claude/projects/-home-hruzam-reposoma/655e7a78-2673-485a-ad93-f3cef7c360e0.jsonl`
  (374007 bytes; last write 2026-09-14 14:21; contains both the report path string and majkee's
  session name). First `"timestamp"` in the file reads `2026-09-14T12:10:09Z` while STATUS records the
  boot on 09-13 — consistent with a resume-continuation under the copartner name, but VERIFY before
  citing (Delta read-only: first user-turn timestamp, not the first field). Fold into `res/trial.md`
  row 0 (`loaded-by` cell or a `transcript:` line under the row-0 record note) and, if the head wants
  it durable, `_bus/00.trajectory.return.md` header. `_bus/` held only `00.trajectory.return.md` at
  14:2x — cartan's verdict not yet on disk; STATUS `next:` stands.
- **Bed-worthy candidates for `/gavel-interpreter`** (from the loop close): L2 "inheritance requires a
  second pair of eyes on the price paid" · L6 "a file is read because a prompt points at it — never
  because a mind decided to" · from this note: "two instances of one name — withdraw the empty hand"
  is already G-43; no new gavel, but the row-0 finding (recall supplied the justification for the
  crossing) is a candidate the head should surface, not this window.
- **Transfer letter at gate close** (`scope: csharp`, seed shape): take the scar in §1 verbatim.

`oraculum (withdrawing window) → oraculum (resumed head) · 2026-09-14 · carried by majkee, never by assumed memory`
