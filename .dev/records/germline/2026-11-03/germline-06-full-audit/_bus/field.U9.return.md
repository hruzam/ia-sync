---
from: field · unit U9 · date: 2026-10-21
session: germline-06-full-audit
question: retention vs rehydration vs recovery — evidence for a question sheet
sources-read:
  - findings.g06.md (E4 vendor facts + E5/C2)
  - janus.c2.return.2026-10-20.md (whole)
  - oraculum.assessment.umbrella.2026-10-20.md (C2/compaction/pilot grep ±10)
  - findings.q1.md (F1 and C2 passages — full file read)
  - HANDOFF.g06-make-program.md (whole; grep: no pilot/P1/compaction hits)
  - sella/GUIDE.md :180–190 (paging row) and :290–300 (L7)
  - tunnel/GUIDE.md (compact/ctx grep ±10)
  - germline/tunnel/tunnel.preamble.md (whole)
  - feedback.houston-install.oraculum.2026-10-21.md (§3.9)
  - reposoma/.majkee/journal/2026-10-21.md :39–54 (D2)
  - germline/agents/houston/binding.claude.md (whole)
  - claude/agents/houston.md (wrapper loader section :38–48)
  - RUNBOOK.md (compaction/authorization grep)
globs-run:
  - /home/hruzam/ia-sync/.dev/session/*/raw/*compaction* → no files found
  - /home/hruzam/reposoma/_cold-start/**/*compaction* → no files found
---

# A. Three-column knowledge table

Rows: RETENTION · REHYDRATION · RECOVERY.
Columns: documented mechanism · design intent · agent assumption · untested.
Vendors: Claude · Codex · chatbot — kept separate within each row.

---

## RETENTION

### Claude
| | |
|---|---|
| documented mechanism | E4 (findings.g06.md:27): "Tool-read content: up to 5 recently read/edited files are re-read after compaction; a file >5,000 tokens returns only as a path reference; other tool results are summarized." CLAUDE.md re-injected from disk. Skill bodies: 5,000 tok each / 25,000 combined, newest first (Sella GUIDE.md:185). Kernel/system-prompt = always resident. |
| design intent | Agent .md body (system prompt layer): docs say "system prompt … still applies" after compaction (findings.g06.md:27) — so the wrapper loader is intended resident, but no germline source makes this explicit for Houston. |
| agent assumption | Subagent .md body survival = inferred, not documented (findings.g06.md:27 "conf M"). No germline file claims identity/binding/card content as kernel-resident. |
| untested | Whether tool-read identity, binding, card survive compaction in practice; whether the 5-file slot is occupied by the load-order files or later reads (findings.g06.md:28; findings.q1.md:51). |

### Codex
| | |
|---|---|
| documented mechanism | E4 is silent on Codex internal compaction (findings.g06.md:27: "Codex: does any read source state Codex's compaction behaviour? (feedback §3.9 `tun compact`; E4 silent?)"). |
| design intent | Not stated in any source read. |
| agent assumption | Context degrades after ~70% usage (feedback.houston-install.oraculum.2026-10-21.md §3.9; tunnel/GUIDE.md:79 usage line). |
| untested | Codex internal compaction model; what survives a `tun compact` call. |

### Chatbot
Nothing found in any source.

---

## REHYDRATION

### Claude
| | |
|---|---|
| documented mechanism | CLAUDE.md from disk after compaction (Sella GUIDE.md:185, :295; findings.g06.md:27). Up to 5 most-recently-read tool-result files re-read (E4). No instruction for re-reading germline load-order files found in any Claude wrapper, binding, or identity. |
| design intent | No "re-read after compaction" instruction in houston.md wrapper, binding.claude.md, or identity.md — confirmed by reading those files. Wrapper carries only a loader (germline/README.md:8-12 quoted at findings.q1.md:39). |
| agent assumption | The stamp-every-reply rule (binding.claude.md:65–67) may function as a compaction-loss detector — this is an inference, not stated in the binding text; attributed to RESULT.U6 §3 in findings.g06.md UPDATE U6. |
| untested | Whether any Claude-side rehydration path exists for runtime-loaded identity/binding/card after compaction. No analogue to the Codex tunnel preamble found. |

### Codex
| | |
|---|---|
| documented mechanism | `tun compact` → one targeted `ask` naming STATUS.md + the cited _bus file — never the full read order (feedback §3.9; tunnel.preamble.md:4: "If your context was compacted or you lack orientation, read only STATUS.md and the files this message names; never the full read order"). |
| design intent | Operator-driven: operator watches ctx% from usage line; at ~70% issues `tun compact` (feedback §3.9). The preamble is set at open and prepended by the shim to every turn (tunnel/GUIDE.md:50–52). |
| agent assumption | The preamble instruction reaches the head as part of every message — so the head receives it even after compaction. |
| untested | Whether germline identity/binding survive in the Codex thread after `tun compact`; the preamble instructs reading STATUS.md and named files, not the full germline load order. |

### Chatbot
Nothing found in any source.

---

## RECOVERY

### Claude
| | |
|---|---|
| documented mechanism | houston.md wrapper:44: "A file missing or unreadable is my first finding; I never reconstruct its content from memory." Covers on-disk file state only — does not cover content lost from context through compaction (file remains readable on disk). |
| design intent | No design text for content-lost-from-context recovery found. |
| agent assumption | Gap: findings.q1.md:51 — "Tool-read content has no named survival path in either source; compaction behaviour is untested." The "missing or unreadable" rule does not extend to compaction loss. |
| untested | What Houston does when identity/binding/card stamps are absent from context after compaction (file still on disk, readable, but not in window). |

### Codex
| | |
|---|---|
| documented mechanism | tunnel.preamble.md:4 provides an explicit compaction recovery instruction: "If your context was compacted or you lack orientation, read only STATUS.md and the files this message names; never the full read order." This is the one existing recovery routine in the house. |
| design intent | Operator-designed, shim-delivered, Codex-only (feedback §3.9; tunnel/GUIDE.md:120–122 "preamble — a standing turn rule the shim prepends to every send/ask/steer"). |
| agent assumption | N/A — preamble is operator-inserted, not agent-initiated. |
| untested | Whether this routine restores germline identity authority (vs. STATUS.md only). |

### Chatbot
Nothing found in any source.

---

# B. H1–H7 evidence tables

## H1 Retention — file-slot arithmetic

**E4 quote** (findings.g06.md:27): "Tool-read content: up to 5 recently read/edited files are re-read after compaction; a file >5,000 tokens returns only as a path reference; other tool results are summarized." "Agent definition body: docs say only 'system prompt … still applies'; survival of a subagent .md body is *inferred, not documented* (conf M)."

**Slot arithmetic** (from brief-stated sizes; no test):

| file | bytes | approx tokens | under 5k cap? |
|---|---|---|---|
| identity.md | 10,179 | ~2,545 | yes |
| binding.claude.md | 5,688 | ~1,422 | yes |
| binding.codex.md | 7,054 | ~1,764 | yes |
| nablarva addendum | 11,261 | ~2,815 | yes |
| consult card | 2,983 | ~746 | yes |
| audit card | 2,311 | ~578 | yes |
| sitting card | 1,291 | ~323 | yes |

All seven are under the 5k-token per-file cap. The primary load order (identity → binding → addendum → card) = 4 files. These 4 fit the 5-file count **if they are the 5 most recent reads**. Any reads after the load order (CLAUDE.md auto-read, skill files, project context, further tool reads) compete for the 5 slots and could displace earlier load-order files. The wrapper body = inferred resident (system prompt survives), confirmed only by "still applies" inference (findings.g06.md:27).

**Codex:** E4 silent (findings.g06.md:27 "E4 silent?"). Feedback §3.9 gives `tun compact` as an operator action, not a retention mechanism.

**Chatbot:** nothing found.

---

## H2 Rehydration intent

Grep for "compact" in houston.md wrapper and binding.claude.md: neither file uses the word or says "re-read after compaction." Confirmed by full reading of both files.

**Stamp-every-reply** (binding.claude.md:65–67): "Every reply: the stamp lines above — `<absolute path> · stamp: <token>`; tokens change on every edit, so a matching token proves the current file was read. A missing or unreadable file is the first finding; no file is reconstructed from memory." — The text makes the stamp a load-time proof. It does not say "stamp absence = compaction loss" or "re-read if stamp missing." A compaction-loss detector interpretation is an inference, not stated design (attributed to RESULT.U6 §3 in findings.g06.md UPDATE U6:70).

No Claude-side rehydration instruction found in any germline source.

---

## H3 Recovery rule — scope gap

**Full quote** (houston.md wrapper:44): "A file missing or unreadable is my first finding; I never reconstruct its content from memory."

The phrase "missing or unreadable" describes on-disk file state. After compaction, the file is still on disk and readable — only its content is absent from context. The rule does not address this case. **Gap confirmed:** no rule covers content-lost-from-context. findings.q1.md:51 states: "Tool-read content has no named survival path in either source; compaction behaviour is untested."

---

## H4 Existing routine

**Full tunnel preamble** (germline/tunnel/tunnel.preamble.md:4): "If your context was compacted or you lack orientation, read only STATUS.md and the files this message names; never the full read order."

**Operator routine** (feedback §3.9): "The routine: when ctx passes ~70%, `tun compact` → one targeted `ask` naming STATUS.md + the cited _bus file — never the full read order."

**Delivery mechanism** (tunnel/GUIDE.md:50–52): "a standing turn rule prepended to EVERY send/ask/steer: tun open [--enable] --preamble <file> ... missing file at turn time → exit 11, no turn sent"

**Codex-only, operator-driven.** The shim prepends the preamble text to every turn; the Codex head receives it as part of every message. No Claude-side analogue found in any source read.

---

## H5 G05 C2 state and drift

| source | what it says | line |
|---|---|---|
| janus.c2.return.2026-10-20.md | "Majkee direction (2026-10-20): C2 recorded as later-work handoff to germline-planning Cartan. Janus's proposed experiment is not automatically a universal production gate." | :27 |
| findings.q1.md | "C2 recorded as later-work handoff to germline-planning Cartan; Janus's proposed compaction pilot is not automatically a universal production gate (Majkee direction 2026-10-20)." | :305–306 |
| oraculum.assessment.umbrella.2026-10-20.md | N2 open: "compaction behaviour of runtime-loaded identity (blocks C2 resolution)" | :77 |
| HANDOFF.g06-make-program.md | grep for pilot/P1/compaction: no matches | — |
| journal/2026-10-21.md :46 (D2) | "Runtime loading remains the current working design. Its behaviour through compaction—including retention and the intended rereading/recovery path—remains unverified. Carry validation to the germline-planning owner as later work. The October 10 gavel is cited; its original receipt remains unlocated. No universal production gate follows from this finding." | :46 |

**No contradiction** across these four. The drift: G05 Janus named a specific pilot shape (load, force-compact, check stamp and limits without re-reading); G04 HANDOFF carries no compaction mention at all; D2 restates "later work" with broader scope ("retention and the intended rereading/recovery path"). Oraculum N2 is the only source calling it a blocker. All agree: not a universal gate.

---

## H6 Measurables — candidate question-sheet rows

| statement | source · line | what would falsify it | vendor |
|---|---|---|---|
| Up to 5 recently read/edited files re-read after compaction | findings.g06.md:27 (E4) | more or fewer than 5 re-read in practice | Claude |
| File >5,000 tokens returns as path reference only | findings.g06.md:27 (E4) | large file content survives intact | Claude |
| Skill bodies: 5,000 tok each / 25,000 combined, newest first | Sella GUIDE.md:185; findings.g06.md:27 | different count in a live test | Claude |
| CLAUDE.md re-injected from disk after compaction | Sella GUIDE.md:185, :295; findings.g06.md:27 | CLAUDE.md absent from post-compact context | Claude |
| identity.md ≈ 2.5k tok — under 5k cap | findings.g06.md:27–28 | token count measured differently | Claude |
| addendum ≈ 2.8k tok — under 5k cap | findings.g06.md:28 | token count measured differently | Claude |
| bindings ≈ 1.4–1.8k tok — under 5k cap | findings.g06.md:28 | token count measured differently | Claude |
| Subagent .md body survival = inferred, not documented | findings.g06.md:27 | platform docs explicitly address subagent .md survival | Claude |
| CLAUDE.md = user-message layer — not enforced, only guided | Sella GUIDE.md:295–296 (L7) | kernel enforcement of CLAUDE.md found | Claude |
| Nested CLAUDE.md NOT re-read after compaction | findings.g06.md:27 | nested CLAUDE.md found in post-compact context | Claude |
| Houston load order: identity → binding → addendum → card = 4 tool reads | findings.q1.md:39–48 (F1) | different order or count observed in transcript | Claude |
| Ask for the Hard limits after forced compaction; compare against kernel-resident | findings.g06.md:44 (P1) | limits quoted correctly without re-read | Claude |
| ctx ~70% → `tun compact` → one targeted ask naming STATUS.md + _bus file | feedback §3.9 | different threshold or read set in operator practice | Codex |
| Preamble prepended to every `tun send/ask/steer` | tunnel/GUIDE.md:50–52 | preamble missing from any turn | Codex |
| Stamp = load-time proof, not compaction-loss detector (by stated design) | binding.claude.md:65–67 | text found saying "if stamp missing in later reply, re-read" | Claude |

---

## H7 Ownership and authorization

**Owner** (findings.g06.md:44): "P1 Pilot design (germline-planning Cartan, C2): test the documented mechanism — identity/binding/card as ≤5 tool-read files, <5k tok each, then force compaction and ask for the Hard limits; compare against kernel-resident. Needs Majkee authorization (live test)."

**Authorization gate** (RUNBOOK.md:60–61): "Force-compaction/live model tests are not authorized by this preparation. Janus's earlier experiment is not a universal production gate."

**D2 stamp** (journal/2026-10-21.md:46): "Carry validation to the germline-planning owner as later work. … No universal production gate follows from this finding."

**Finding from E5/C2** (findings.g06.md:23): "owner = germline-planning Cartan; absence of a file here ≠ proof none was sent."

No germline-planning bed found; no pilot proposal file found (findings.g06.md:23; globs returned no compaction files).

---

# C. Measurables list

(Candidate question-sheet rows; see B/H6 for the full table with falsification conditions.)

1. ≤5 recently-read files re-read post-compaction — Claude — E4 / findings.g06.md:27
2. ≤5,000 tokens per file; >5k → path reference — Claude — E4 / findings.g06.md:27
3. 25,000 tokens combined for skill bodies — Claude/Sella — Sella:185
4. CLAUDE.md from disk; nested CLAUDE.md not — Claude — Sella:185/:295; E4
5. Identity ≈ 2.5k, addendum ≈ 2.8k, bindings ≈ 1.4–1.8k, cards <1k — Claude — findings.g06.md:27–28
6. All four load-order files fit 5-slot count (arithmetic only) — Claude — findings.g06.md:28
7. Subagent .md body survival inferred, not documented — Claude — findings.g06.md:27
8. Stamp = load-time proof; no compaction-loss-detector text found in binding — Claude — binding.claude.md:65–67
9. wrapper:44 covers only on-disk missing files, not context loss — Claude — houston.md:44
10. Codex: E4 silent on compaction; no germline retention model found — Codex — findings.g06.md:27
11. Codex recovery routine: ctx ~70% → `tun compact` → STATUS.md + _bus file — Codex — feedback §3.9; tunnel.preamble.md:4
12. Preamble = only existing recovery routine in the house — Codex — feedback §3.9

---

# D. Contradictions / drift

**No outright contradiction** across G05 C2 material, G04 HANDOFF, D2, and feedback §3.9.

**Drift (specificity):**
- G05/Janus named a concrete pilot shape: load → force-compact → check stamps + forbidden limits without re-reading (findings.q1.md:57).
- G04 HANDOFF carries no compaction mention (grep returned no matches).
- D2 (journal 2026-10-21:46) restates it more broadly: "retention and the intended rereading/recovery path — remains unverified."
- Result: the pilot shape is in G05 evidence only; D2 does not re-specify it; G04 does not carry it. If a germline-planning Cartan reads only G04 and D2, it would not find the Janus pilot shape.

**Structural gap:**
- Sella L7 (GUIDE.md:293–294): "identity, hard limits, the one safety rule — must live in the kernel; the rest can live below the boundary." The germline runtime-load places these in tool-read slots (findings.q1.md:52 — Janus confirmed as L7 tension, not just a gap). This tension persists unresolved through G05, G04, D2 — all mark it for later work, none resolve it.

---

# E. Friction for an agent just compacted (ranked, cited)

1. **No re-read instruction exists (Claude).** The wrapper, binding, and identity carry no "re-read after compaction" rule. An agent that has been compacted has no authored path back to its identity/binding. (binding.claude.md: entire file; houston.md:44)

2. **Recovery rule gap.** The "missing or unreadable" rule (houston.md:44) does not fire on compaction loss — the file is still on disk. The agent has no trigger to detect loss of its own authority fence. (findings.q1.md:51)

3. **5-file slot competition.** The four load-order files fit the slot budget, but only if they are the most recent reads at compaction time. Any later reads (CLAUDE.md auto-read, skill bodies, project queries) displace them from the re-read set. No ordering rule is prescribed. (findings.g06.md:28)

4. **Stamp-every-reply is load-time proof only.** Stamps prove a file was read at entry. After compaction the stamp lines remain in the transcript history but do not prove current context residence. An agent cannot distinguish "I read this at load time" from "this content is in my window now." (binding.claude.md:65–67)

5. **Codex routine is operator-dependent.** The one existing recovery routine (tunnel preamble + `tun compact`) requires the operator to watch ctx%, issue `tun compact`, and follow with a targeted `ask`. If the operator does not do this, no recovery happens. (feedback §3.9; tunnel.preamble.md:4)

---

# F. Uncertainty / not-read

- **Not read:** germline/agents/houston/identity.md (full text); codex/agents/houston.toml; RESULT.U6 (referenced in findings.g06.md UPDATE U6 as source for "stamp-as-detector = inference" claim — not available as a listed source; treated as attributed). Any "compact" grep in the full germline directory was not run; only the files explicitly in the load order were read.
- **Not read:** reposoma/raw.guides/tunnel/res/preamble.md (full chapter); only the GUIDE.md grep and tunnel.preamble.md were read.
- **Not confirmed independently:** Sella's [S3] confidence-L downgrade for the 5k/25k token figures (findings.q1.md:246 "downgraded to CONFIDENCE L by the refresh — live docs now surface a line-count guideline instead"). The E4 quote still uses 5k/25k figures; treat as CONFIDENCE L.
- **Chatbot channel:** the brief asks whether any source says anything about chatbot retention/rehydration/recovery; nothing was found.
- **RESULT.U6 §3:** explicitly named in findings.g06.md as the source for the "stamp-as-detector = inference" classification, but the file was not in the brief's source list and was not read.
- **The germline-planning bed:** no file found; no pilot proposal received; cannot verify whether a proposal was sent and is awaiting reading (findings.g06.md:23 "absence of a file here ≠ proof none was sent").
