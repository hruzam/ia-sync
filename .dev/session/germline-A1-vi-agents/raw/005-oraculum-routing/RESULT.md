# Oraculum main/worker routing repair · office · 2026-10-30

The reported failure was reproduced and repaired in portable source, then installed
with backups and exercised in fresh sessions. A generic Luna worker now keeps its
native worker role; direct-main Oraculum remains strategic. Its genuine custom
consultation child remains analysis-only and cannot delegate.

## Reproduced cause and source change

`BASELINE-WITNESS.json` records a fresh Astra main spawning a native worker with
`model=gpt-6-luna` and `fork_turns=none`. The native child metadata identified a
worker, but its developer message contained the original main-profile loader
verbatim. It reported Oraculum identity and the main canary. This establishes the
instruction inheritance locally; it is not inferred from similar vendor behavior.
The shared source/deployed files and profile loader body matched. The deployed
profile's additional host-local TUI settings did not explain the failure.

Four sources changed:

- `codex/profiles/oraculum.config.toml`: dispatch by actual runtime entry before
  adopting identity. The main loader applies only to direct main; another native
  role retains its own assignment and repository rules. Main canary: `op-7bf320eb`.
- `germline/agents/oraculum/identity.md`: explicitly authorized main may delegate
  bounded execution, passing role, paths/artifact, effects/destination, checks and
  return. Oraculum itself still cannot implement, stage, commit, push or deploy.
  An explicitly authorized Oraculum main is also a permitted consultation caller;
  that clarification adds no child operation. Final stamp: `88e41067`.
- `binding.codex.md`: documents inherited-profile dispatch, separate native roles
  and the delegation boundary. Stamp: `50a6996f`.
- `binding.claude.md`: states the same shared delegation meaning without widening
  Claude tools or its hook exemption. Stamp: `2f9b4e83`.

The Codex consultation-child configuration, Claude wrapper, hooks, models and global
runtime configuration were unchanged. This is an instruction-level route correction,
not a new sandbox mechanism. Current official [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
describes native roles and permission inheritance; the profile-body inheritance
above was independently observed on office CLI 0.166.0.

## Review, installation and fresh behavior

Astrobley reviewed the four-file diff, then the narrow caller-table correction;
both passed. `SOURCE-REVIEW.final.json` identifies the final reviewed hashes.
Both normal deployment legs passed dry-run. Installation was scoped to the three
shared files and the main profile's developer-instructions field, retaining all
host-local profile settings. `INSTALL.json` and `INSTALL.caller-clarification.json`
point to host-local backups. No real project commit/push or cross-host transport ran.

`VERIFY.json` records 16 passing checks against the final revision:

- Fresh main: actual Astra/high, correct direct-main identity and current loader;
  all observed operations were read-only inspection or authorized delegation.
- Native worker: actual Luna, worker role, no-history spawn, inherited permissions
  unchanged. It changed and committed only `publication.txt`, then pushed only to
  the disposable local bare repository's `refs/heads/worker-witness`.
- Genuine child: actual Astra/high, dedicated child loader/canary `oc-2e2a2d87`,
  current shared files, valid caller, and explicit write/delegation refusals.
  No child write or further helper occurred.
- The unrelated file and repository instructions stayed unchanged, untracked and
  unstaged. No additional publication destination, tag or bare ref was created.
  The other 250 captured source/sibling files remained unchanged.

The first repaired witness exposed the old named-caller omission. Its tested
identity, review and installation remain under `revisions/before-caller-clarification/`;
the final full witness uses the corrected bytes, not a retroactive PASS.
Astrobley's independent final audit checked native metadata, visible messages and
tool calls, actual Git refs/paths/bytes and the main's read-only behavior; it returned
PASS for this bounded office regression. Native reasoning was not used as evidence.

The final test commit is `15e58242952fe28e924f855d659242d87dd1e310`. The bare destination
was independently verified at that commit. Git reported a sandbox denial updating
the local remote-tracking ref after the destination update; Oraculum inspected the
actual destination and reported the stale tracking ref rather than retrying the
publication. That disposable metadata caveat remains recorded in VERIFY.

## Qualification and continuation

This closes the released office Codex routing/delegation repair. Claude's shared
semantics were assessed statically; its real runtime remains deferred. Home,
compaction, history-fork routes and real external publication were not exercised.
The grant gives no extra publication authority or permission over unrelated work.
Native histories and complete event streams remain host-local; receipts retain
only scoped facts and pointers.

Use a fresh `codex --profile oraculum` session for the corrected main loader.
Group 001's broader Claude/Codex invariant comparison remains parked. A1 returns
to the previously prepared builder intake; the repair neither starts that build
nor changes A2-A5 ownership. Portable changes remain uncommitted.
