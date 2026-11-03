---
binding: oraculum
vendor: codex
scope: native entry, loading, permissions and proof only; authority remains in identity.md
updated: 2026-10-27
stamp: f1bab274
verified: A2 source revision; A1 office witnesses cover prior bytes; revised lab entry pending
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

Native read/search tools serve both routes. Native edit tools are used only by an
operator-assigned main planning, research or synthesis scope. A child returns to its caller; a main returns
to the operator and the explicitly assigned document destination. No project copy
of the global agent/profile is installed; projects specialise through the addendum.

Syntax and copied bytes do not prove runtime loading. Fresh route checks must inspect
the injected developer body, ordered tool reads before the first answer, current
stamps, actual model/effort, main/child authority and return. Probe a child's refused
write/delegation and a main's scoped document grant separately. Record the exact
route/host and limits; neither proves the other, another host or compaction.

Official sources (checked 2026-10-26):
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/config-file/config-advanced#profiles
- https://learn.chatgpt.com/docs/config-file/config-reference
