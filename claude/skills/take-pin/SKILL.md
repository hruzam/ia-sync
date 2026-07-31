---
name: take-pin
description: Invoke as /take-pin [peek]. Claims pins from ~/.pins/pins.jsonl for the current project scope (git-root match). H6 transport — root-based claiming, no session binding. Matched pins consumed; unmatched (other roots) preserved. Peek mode leaves store untouched.
---

When `/take-pin` is invoked:

**1 — Locate the store.**
```
~/.pins/pins.jsonl
```
If missing or empty → report `"no pins"` and stop.

**2 — Find the current scope root.**
Walk up from cwd to the nearest `.git` directory. That directory is the root.
If no `.git` found → use cwd as root.

**3 — Filter.**
Read all lines. Matched = lines where `root` field equals the scope root.
Unmatched = everything else (other projects' pins — do not touch).

If no matched pins → report `"no pins for <root>"` and stop.

**4 — Present matched pins.**
One block per pin:
```
── pin ─────────────────────────
file:  <path>:<line>
root:  <root>
context:
  <snippet>
```
Range pins show `<line>-<line_end>`. Address-only pins show `<formatted>` with no context block.
Number them (pin 1/N … N/N).

**5 — Consume or peek.**
- **Default (consume):** rewrite `~/.pins/pins.jsonl` with unmatched lines only. Matched pins are gone; other scopes' pins are preserved exactly.
- **Peek:** `/take-pin peek` → present without rewriting.

**Hard rules:**
- Never clear the entire store — only consume matched pins.
- Never touch unmatched lines (other roots).
- No session inference, no scope attach — root field is the only binding evidence.
- If a pin has no `root` field (H5 artifact or unsaved buffer) → treat as unmatched; do not consume.

*Source: `claim-pins.sh` (H6 transport). Store: `~/.pins/pins.jsonl` (global, editor-agnostic).*
