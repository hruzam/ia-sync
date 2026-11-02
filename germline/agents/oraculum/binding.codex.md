---
binding: oraculum
vendor: codex
scope: native entry, loading, permissions and proof only; authority remains in identity.md
updated: 2026-10-30
stamp: 50a6996f
verified: A1 routing repair; exact source and exercised-route qualification belong to its receipts
---
# oraculum · Codex binding

| Route | Source → deployed target | Shared entry scope |
|---|---|---|
| Native child | `~/ia-sync/codex/agents/oraculum.toml` → `~/.codex/agents/oraculum.toml` | Child consultation; named authorized caller and bounded return |
| Direct main | `~/ia-sync/codex/profiles/oraculum.config.toml` → `~/.codex/oraculum.config.toml` | Operator-assigned planning, research and synthesis, selected with `codex --profile oraculum -C <project-root>` |

These files hold only model/effort, native capability settings and a loader. Their
Route canaries identify the injected body and change whenever that body changes.
The model pin stays in the wrappers. A custom-agent TOML configures spawned agents;
selecting a profile loads the separate main file. No user config or trust registry
is edited by this fold. `deploy.sh` explicitly allowlists the main profile.

The main profile's developer instructions can be inherited by spawned agents,
including a worker created without conversation history. Its entry dispatch applies
the main identity/loader only to the actual direct main. A native worker or other
role keeps its own assignment and repository rules; the parent's profile is not
its identity or a source of strategic-seat restrictions. A selected oraculum custom
child uses the separate child loader and remains analysis-only/nondelegating.
Resolve entry from actual runtime metadata; ambiguous entry is a finding before
side effects. fork_turns controls history, not this identity distinction.

Load `~/.germline/agents/oraculum/identity.md`, then this binding, then the nearest
readable `.germline/agents/oraculum/<ancestor-basename>.md` found by walking upward
from effective cwd. Skip the global `~/.germline`. No addendum means neutral Oraculum;
ambiguous selection is a finding. The first reply records effective cwd, the actual
main/child scope, Route canary and all loaded absolute paths/stamps.

A child inherits the parent's effective permissions, provider and MCP servers;
its file cannot enlarge them. The preserved disabled feature settings are native
capability choices. Its analysis-only contract, including no writes or delegation,
is an instruction boundary inside that runtime, not a claimed read-only sandbox.
The main profile inherits effective main-session policy and tools; the shared
identity limits planning/research/synthesis writes and delegation further. Capabilities do not grant
a project pen. Neither route provides persistence or a resumable child by itself.

An explicitly authorized main may use a suitable native execution worker for the
bounded task specified in the shared identity. Pass exact allowed effects/paths,
Git or publication destination, required checks and return. This does not authorize
Oraculum to implement or publish directly, widen the genuine Oraculum child, or
give a worker additional access/authority. Inspect actual diffs and results before
accepting completion; no unrequested publication follows from tool availability.

Native read/search tools serve both routes. Native edit tools are used only by an
operator-assigned main planning, research or synthesis scope. A child returns to its caller; a main returns
to the operator and the explicitly assigned document destination. No project copy
of the global agent/profile is installed; projects specialise through the addendum.

Syntax and copied bytes do not prove runtime loading. Fresh route checks must inspect
the injected developer body, ordered tool reads before the first answer, current
stamps, actual model/effort, main/child authority and return. Probe a child's refused
write/delegation and a main's scoped document grant separately. Record the exact
route/host and limits; neither proves the other, another host or compaction.

Official sources (subagent mechanics rechecked 2026-10-30; inheritance also reproduced locally):
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/config-file/config-advanced#profiles
- https://learn.chatgpt.com/docs/config-file/config-reference
