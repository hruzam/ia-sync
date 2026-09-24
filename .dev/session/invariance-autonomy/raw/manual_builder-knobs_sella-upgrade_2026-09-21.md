---
manual: builder-knobs (the vendor-shaped plumbing under a shared body)
scope: seller-upgrade
date: 2026-09-21
status: OPERATIONAL · expected to churn every vendor release · re-verify before relying
canon: canon_shared-body_seller-upgrade_2026-09-21.md (the invariant this serves)
verification: published docs only (asymmetry 2026-09-21; symmetry doc search 2026-09-21). Home/office installs UNVERIFIED.
---

# MANUAL — the knobs

Each wrapper declares all five. "Declared" means written in the wrapper file, not held in the operator's head. Where a knob has no mirror on the other side, the wrapper says so.

---

## Knob 1 — Load timing
**What:** when the body enters the child's window.

| | Claude Code | Codex |
|---|---|---|
| Native | markdown body = system prompt of the subagent, present before first token | `developer_instructions` in the agent TOML, injected into the session at start |
| Mirror | equivalent — both compose at startup | |
| Anti-pattern | "read `identity.md` first" as a task instruction → arrives as a tool result, mid-window, can silently not happen | same |

**Cost:** one composition step per wrapper (include/import or build-time concatenation). Near zero once the pattern exists.
**Required:** a mechanism that puts the shared markdown INTO the vendor file's instruction field — import on Claude, factor-out + include on Codex.
**Example:** Astrobley — body currently inline in `astrobley.toml`; factoring it into `bodies/astrobley.md` and composing it is the first concrete move. The Claude wrapper then points at the same file.
**Watch:** Claude project instructions (CLAUDE.md) and preloaded skills ALSO enter the child's window. Know what else is arriving beside the body.

---

## Knob 2 — History copying
**What:** whether the parent's conversation crosses into the child.

| | Claude Code | Codex |
|---|---|---|
| Fresh (default subagent) | starts empty: body + task only | native delegation: separate thread |
| Inherit | conversation fork — inherits parent history | history-copying fork: all / some / none of parent conversation (Work interface; CLI policy not inferred) |
| Note | skill `context: fork` is FRESH despite the name — it does NOT copy history | |

**Cost:** zero to build; the cost is in choosing wrong. Inherited history drowns the body (see knob 4 pain case) and leaks parent context into a specialist.
**Required:** the wrapper states `history: fresh | inherit`. Dispatch skill respects it.
**Example:** researcher / architect — fresh, always. Buffering (RAG Sonnet) — fresh at spawn, then held (knob 4); it builds its own history, doesn't inherit yours.

---

## Knob 3 — Permissions
**What:** whose sandbox actually applies to the child.

| | Claude Code | Codex |
|---|---|---|
| Declared | `tools:` / `disallowedTools:` in wrapper | sandbox + model + reasoning in agent TOML |
| Override risk | preloaded-skill and tool inheritance rules — check per version | **documented: live parent permission overrides can supersede child profile defaults** |

**Cost:** one test run per child profile per install. Cheap, but never skipped.
**Required:** an actual attempt to write from a read-only child, on the real machine. TOML is a claim, not proof.
**Example:** researcher.toml / architect.toml — declared read-only. Proof obligation open.

---

## Knob 4 — Lifetime
**What:** one-shot or held on the line.

| | Claude Code | Codex |
|---|---|---|
| One-shot | Agent tool: spawn → final message → gone | delegate → thread ends on completion |
| Held | `SendMessage` resumes the child; transcript persists, survives parent compaction | follow-up steering on the agent thread |

**Cost:** held = operator now owns the child's coherence. One-shot = re-priming cost per spawn, clean identity each time.
**Required:** wrapper states `lifetime: oneshot | held`. Held wrappers get a re-ground line the operator sends every few turns — one sentence pointing at the body, not a reload. (= anchor: licenses drift, catches at the radius.)
**Pain case:** reviewer held for three passes. Body at the top, quieter each turn; pass three reviews like a generic assistant. No error. Output still looks competent. That is the failure you can't see from outside.
**Example:** ~80% of the roster — one-shot, unchanged. Buffering (RAG Sonnet) — held; it is the one agent that was already resumable in spirit. Trajectory / Delta on a long implementation — candidate held, only when the task provably won't fit one spawn.
**Telemetry:** re-grounding keeps firing → task exceeds one context → decompose.

---

## Knob 5 — Entry point
**What:** where the operator can start.

| | Claude Code | Codex |
|---|---|---|
| Direct child | yes — operator can invoke a subagent wrapper without a parent | no — parent required; child only via delegation |
| Mirror | none on Codex side. DECLARE the gap. | |

**Cost:** a Codex session always carries a parent's window on top of the child's. Budget it.
**Required:** dispatch skill exists on both sides even though Claude doesn't strictly need it — parity of operator habit, not of mechanism.
**Example:** Cartan (Codex maintenance seat) is the mandatory parent; on the Claude side the same body can be entered cold.

---

## Wrapper declaration block (both sides, same keys)
```
body:       bodies/<agent>.md
load:       compose        # never "read-later"
history:    fresh | inherit
perms:      <declared>     # proof-run date: ____
lifetime:   oneshot | held
entry:      child | parent-only
mirror-gap: <none | text>
```

## Not-to-forget
- Factor Astrobley's body out of the TOML first; everything else follows the pattern it sets.
- One proof run per read-only profile per machine, dated in the wrapper.
- Don't collapse wrappers into one shell. Families, per-agent wrappers, shared bodies.
- This file is weather. Re-verify each row against current docs before building on it.
