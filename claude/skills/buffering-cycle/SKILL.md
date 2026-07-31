---
name: buffering-cycle
description: >
  Invoke as /buffering-cycle. Phased input buffering before artifact release.
  Prevents premature execution on noisy, incremental, or voice-style input.
  Five phases: feed → synthesize → smooth → draw → close.
  Compatible with /honest and /regime-karpathy.
---

I am running the buffering cycle. I do not execute until the buffer is ready and approved.

## Phases

| # | Phase | Trigger | I do |
|---|-------|---------|------|
| 1 | **feed** | input arriving | Buffer, handle fragments/noise, mark _underline_ incomplete threads, confirm understanding |
| 2 | **synthesize** | feed end signal | Process buffer, connect to existing context, draft internal structure |
| 3 | **smooth** | synthesis ready | Clarifying questions, honest pushback, surface ambiguities |
| 4 | **draw** | smoothing approved | Release final artifact — md, json, yaml as appropriate |
| 5 | **close** | artifact released | Flush buffer, preserve _underline_ items, ask if regime change needed |

## Underline rule

Items marked _underline_ persist across all phases. On close I surface them:
> "These threads are still open — continue now or park?"

They get their own loop when the main cycle closes.

## Hard rules

- I do not execute on incomplete input
- I do not skip the smooth phase to save time
- I do not release artifacts before @majkee approves the synthesis
- If @majkee signals "feed end" explicitly, I move to synthesize immediately
