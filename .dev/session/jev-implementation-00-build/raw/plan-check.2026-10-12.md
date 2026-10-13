---
title: Jev plan — October 12 evidence and tunnel qualification limits
date: 2026-10-12
author: cartan
scope: read-only checks plus plan/protocol/STATUS authoring; no implementation
---

# Observed frame

Office: `hostname -s` → `hruzam-120922`; `/usr/bin/php74` exists. ia-sync main HEAD
`0a1bff9`; `git fetch origin` exited 0 and `git rev-list --left-right --count
HEAD...origin/main` returned `0 0` at orientation. The worktree contains unrelated active
germline/Houston/chatbot-port/deploy/journal edits; none is included in this work.

The 29 existing files in the Jev bed were hashed before authoring. The snapshot used for
this turn's comparison is `/tmp/jev-plan-before.2026-10-12.json` (temporary check aid, not a
continuity source). RUNBOOK and the original input checksums are independently covered by
the embedded verifier in `_bus/01.cartan.return.md`.

At inspection, `raw/majkee-gavels.2026-10-12.md` is an unanswered decision sheet, not a
gavel record. `_bus/01.flight.verdict.md`, `impl/`, `tests/`, the live `/home/hruzam/.jev`
store, and a Jev-bed tunnel state file are absent. Cartan's October 5 RETURN verifier
passes unchanged. No implementation or live API behavior can be inferred from that check.

# Tunnel checks

| Check | Observed result |
|---|---|
| Live/source copies of `tunnel-codex.zsh`, `tunnel-codex.py`, `tunnel-codex.selftest.zsh` and `session/tunnel.zsh` | SHA-256 pairs match; source HEAD is `0a1bff9`. |
| `zsh /home/hruzam/.config/zsh/ai/tunnel-codex.selftest.zsh` in sandbox | 138 passed; only `py_compile` failed because the live `__pycache__` directory was read-only. |
| Same command, approved outside sandbox | Exit 0: `139/139 tunnel-codex self-tests passed`. Fixture transport, no live model turns. |
| Local CLI / daemon versions from read-only preflight | CLI `0.162.0`, daemon `0.162.1`; version skew is not a demonstrated failure, but the older live receipts do not qualify this pair. |
| `_tn_check --id 01a0f5b9-b2ae-7392-af89-f434d5536d88 --cwd /home/hruzam/ia-sync`, after sourcing the local manager | Exit 0, READY; existing rollout found, writer lock file present with no reported holder. No bind/resume/turn was run. |
| Recorded usage in that probe | 228464 / 258400 = 88.4%, recorded at `2026-10-12T17:45:01.478Z`. Dated occupancy, not a promise about the next turn. |
| Recorded thread policy | `gpt-6-astra`, `xhigh`, approval `on-request`, reviewer `user`; not an effective tunnel-runtime receipt, since no resume occurred. |

Reproducing the preflight without shell aliases:

```zsh
zsh -c 'source /home/hruzam/ia-sync/zsh/session/tunnel.zsh
_tn_check --id 01a0f5b9-b2ae-7392-af89-f434d5536d88 --cwd /home/hruzam/ia-sync'
```

The READY diagnostic did not establish that this active interactive client had released
the thread. Explicit release remains necessary. No writer-lock file was removed. No
tunnel enable, live ask, compact, fork, reset or daemon restart was performed.

Source fingerprint for later comparison:

```text
ae7803d804b54fd59145550807286a030d9efc6c2f13c6a0e17584dffe768f4e  zsh/ai/tunnel-codex.zsh
8ca70c3044a9756265b42bc94d4a58b1d2c512ecd6b2e25becbd781ca2259052  zsh/ai/tunnel-codex.py
3af4e809e58d34db469265ff272fb3f58b6f5673e342c14e6912d0db8d6e8aae  zsh/ai/tunnel-codex.selftest.zsh
50408135d2d97173505c75598addd652bc1085d745b75e794f976e28e0b6e075  zsh/session/tunnel.zsh
```

# Documentation differences to carry into review

- The base tunnel guide's live receipts date from older CLI versions. Its manifest matches
  its immediate children. The local self-test is now 139 cases; it does not replace the
  guide's required one live round-trip on an upgrade.
- The installed shim/source supports `compact`, `fork` and turn overrides. The older
  user-run chapter's “no in-thread trim” statement is no longer a complete capability map.
  No live compaction/fork claim is made by this plan.
- The multi-seat seats table labels the Claude carrier as cSharp/status_owner, yet also
  says it never advances STATUS. This RUNBOOK unambiguously assigns both roles to Cartan.
  The proposed bed protocol retains that assignment and makes Flight the carrier.
- The gavel sheet says agents “can never spend,” followed by its cooperative same-user
  limitation. The design's limited guarantee must govern the implementation and wording.
- Append-only malformed-tail recovery in design D4 leaves a non-JSON forensic fragment;
  acceptance of that exception remains a Flight review item before coding.

# Provider recheck

Read the official [OpenRouter decisions reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request)
on 2026-10-12. It still documents `/api/alpha/decisions`, `typesafe/jev-1.13`, and mixed
question types. This confirms the public contract remains documented. Account entitlement,
the accepted resolved snapshot, current billed price, borrowed-key access, denomination and
revocation behavior are not observed; check the relevant items before the live phase.
No community/forum assertion is used as implementation authority here.

# Authoring boundary

This turn creates `PLAN.md`, `tunnel-using-protocole.md` and this evidence note, and replaces
Cartan's STATUS snapshot. The existing RUNBOOK, cycle-01 exchange, designs, original three
inputs, photos and Flight/Epoch-owned artifacts remain unchanged. There is no commit,
deployment, new live Jev store, credential access or paid call.

Post-authoring verification: the exact Python verifier embedded in RETURN 01 passed
(gate/STATUS, ten dispositions, six RETURN fields, original hashes, all 13 photo copies and
formatting). Comparison with the before snapshot found only STATUS changed among the 29
pre-existing files and exactly the three additions named above. New document frontmatter,
local Markdown links and whitespace passed; `git diff --check` exited 0. The final inspection
still found zero checked operator-answer boxes and no Flight VERDICT, implementation or
runtime activation. These checks verify the planning artifacts, not a Jev implementation.
