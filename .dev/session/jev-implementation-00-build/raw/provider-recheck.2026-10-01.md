---
title: Jev provider recheck and offline source assessment
date: 2026-10-01
author: cartan
host: office / hruzam-120922
status: public contract checked; offline tests only; no authenticated request
---

# Provider and reusable source evidence

The operator identified `session-draft-memory.md` as the lead on provider intent. Both prose
inputs carry 2026-09-24 dates; their import mtimes do not establish provider correctness.
Current first-party documentation independently supports its OpenRouter choice.

## Current documented contract

| item | checked value / source |
|---|---|
| Raw HTTP endpoint | `POST https://openrouter.ai/api/alpha/decisions` — [API reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request) |
| Request | `model`, `state`, `questions`; named Choice/Noul/Score entries — same reference |
| Model requested | `typesafe/jev-1.13` |
| Public provider metadata | TypeSafe; endpoint name `TypeSafe \| typesafe/jev-1.13-20260917`; context 32000; prompt price `0.000000042` USD/token, completion `0` — [public endpoint metadata](https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints) |
| Response | `answers`, resolved `model`, `provider`, `id`, `usage` including cost — API reference |
| Compatibility path | `https://openrouter.ai/api/v1/systemone` with the same OpenRouter account/key — [TypeSafe SDK compatibility](https://openrouter.ai/docs/guides/community/typesafe-sdk) |
| Direct TypeSafe | Still documents `https://api.typesafe.ai/v1/systemone` and `jev-1.13.0`; this is the old script's route, not the selected pilot route — [TypeSafe API](https://docs.typesafe.ai/api) |

The dated resolved model ID is not identical to the requested ID. Record both and validate
against an explicitly reviewed provider/version policy, not equality with the old direct
TypeSafe constant and not an unrestricted string prefix. Metadata is not an authenticated
inference receipt. Key availability, funded balance and account-specific access remain unverified.
`JEV_ORAK_KEY` is the operator draft's intended local credential variable; no value was read.

OpenRouter publishes a 32k context limit. Direct TypeSafe distinguishes 64k total from 32k
state-plus-longest-question; do not assume the larger limit applies to this route.
[Direct TypeSafe model limits](https://docs.typesafe.ai/models).

Choice confidence is not the selected probability. Score is a probability-weighted position;
Noul is the probability of yes and has no separate confidence. Thresholds need task evidence.
[Confidence](https://docs.typesafe.ai/confidence), [API answer types](https://docs.typesafe.ai/api).
Independent questions can share state in one batch; dependent requests may legitimately need
another call. Avoid treating all single-question requests as inherently wrong.
[Official integration skill](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md).

State can contain adversarial instructions and irrelevant history reduces usefulness.
These are reasons to keep bounded input and advisory semantics, not to invent a safety score.
[Published limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

## Original-input fingerprints

Paths below are relative to this `raw/` directory; preserve their bytes:

```text
1ea42bd43de6b5dcff820b2c79d48f76d0c33bf480dc85b45067b76caa742120  JEV_RESEARCH_AND_CLI_HANDOFF.md
91fc968a593ec1568656d9d819eaa661c6278f22a6bebafe0684dd580eab4a3e  jev_smoke.py
9cb89e9e8ca294dfcfd90ee22017a50a364d63286d4e16fc6c35046f0a5cbf14  session-draft-memory.md
```

## Offline observations on office

Python observed: 3.14.7. No packages installed and no model request sent.

```sh
python3 -B /home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/jev_smoke.py --self-test
python3 -B /home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/jev_smoke.py --dry-run
```

Observed: self-test exited 0, `PASS: 1 valid and 12 invalid local fixtures; no network calls.`
Dry run exited 0 and emitted one synthetic direct-TypeSafe request containing Choice, Noul
and Score. This is not evidence that the selected provider, live approval gate or integration works.

An additional in-memory probe copied the self-test's valid fixture and changed one value per
case, then called its unmodified `validate()`:

| mutation | observed outcome |
|---|---|
| `model = typesafe/jev-1.13-20260917` | rejected: unexpected model version |
| `next_step.choice = repeat`, while probability 1 remains on inspect | accepted |
| `context_relevance.score = 0`, while probability 1 remains on level 2 | accepted |
| add an unrequested answer named unexpected | accepted |

The original script is a diagnostic starting point. Its retained checks include numeric types,
finite/range checks, probability keys/sums, Score legend, token counts, response byte bound,
TLS verification, redirect refusal and no automatic retries. Production validation must be
driven by the frozen request and verify relevant internal consistency with rounding tolerance.
No need to reconstruct the vendor's undocumented confidence formula.

## Unverified before implementation

- Exact concrete per-send approval behavior in the enabled Claude and Codex paths.
- Authenticated OpenRouter behavior, actual resolved model/cost and account errors.
- JSONL concurrency/recovery and stale-input handling; the example is schema material only.
- Existing neutral session-launcher integration syntax; use explicit adapter settings until
  a real external interface is inspected. Do not manufacture a registry or silently add a row.
- Shadow accuracy, calibration and workflow savings. None are established by schema tests.
