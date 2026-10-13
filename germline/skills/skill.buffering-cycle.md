---
name: buffering-cycle
description: When majkee says "buffer this", "hold — more is coming", "feed", or drops noisy / voice-transcribed input in pieces, I run the buffering cycle — collect, synthesize, question, and release the artifact only on his approval.
source: ~/.claude/skills/buffering-cycle/SKILL.md
twin: claude
orphan: true
near-miss: codex/buffering — the Codex skill merges buffering-cycle + buffering-creative-triad under one slug; ported from the Claude source on majkee's call (2026-09-23), the near-miss stands recorded for the twin-slug ruling
source-commit: 8da748a
ported: 2026-09-23
---
_Ported from the CLI skill — do not edit here; re-run `/chatbot-port buffering-cycle`._

I am running the buffering cycle. I do not execute until the buffer is ready and approved.

## Phases

| # | Phase | Trigger | I do |
|---|-------|---------|------|
| 1 | **feed** | input arriving | Buffer, handle fragments/noise, mark _underline_ incomplete threads, confirm understanding |
| 2 | **synthesize** | feed end signal | Process buffer, connect to existing context, draft internal structure |
| 3 | **smooth** | synthesis ready | Clarifying questions, honest pushback, surface ambiguities |
| 4 | **draw** | smoothing approved | Release final artifact — md, json, yaml as appropriate, in the chat or as the file majkee asks for |
| 5 | **close** | artifact released | Flush buffer, preserve _underline_ items, ask if regime change needed |

## Underline rule

Items marked _underline_ persist across all phases. On close I surface them:
> "These threads are still open — continue now or park?"

They get their own loop when the main cycle closes.

## Hard rules

- I do not execute on incomplete input
- I do not skip the smooth phase to save time
- I do not release artifacts before majkee approves the synthesis
- If majkee signals "feed end" explicitly, I move to synthesize immediately
