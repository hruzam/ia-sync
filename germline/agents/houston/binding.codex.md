---
binding: houston
vendor: codex
runtime: Codex — custom agent ~/.codex/agents/houston.toml (child) · named profile ~/.codex/houston.config.toml (main session); authored at ~/ia-sync/codex/{agents/houston.toml,profiles/houston.config.toml}
scope: mechanics only — entry, permissions, delegation and proof; grants no authority beyond the identity, the selected card and the project addendum
authority: identity.md beside this file · nablarva flag L16 (clause 14 amended)
state: CANDIDATE — final fold 2026-10-10 (majkee gavel); X0 evidence archived, pre-fold copy at nablarva .dev/session/nablarva-X1-architecture/raw/archive.x0-renders/binding.codex.md (commit-pin at majkee's commit)
updated: 2026-10-10
stamp: cac6a05d
---
# houston · Codex binding

## The wrappers — the only vendor facts they carry

| route | file | keys |
|---|---|---|
| child | `~/ia-sync/codex/agents/houston.toml` → `~/.codex/agents/houston.toml` (deploy.sh rsyncs `ia-sync/codex/agents/`) | `name` · `description` · `model` · `model_reasoning_effort` · `developer_instructions` = LOADER + `Route: spawned child (no card line → consult)` |
| main session | `~/ia-sync/codex/profiles/houston.config.toml` → `~/.codex/houston.config.toml` (hand-installed; not in the deploy map) | `model` · `model_reasoning_effort` · `developer_instructions` = LOADER + `Route: main session (no card line → ask the operator)` |

`model` / `model_reasoning_effort` are weather, set in the wrappers only and mirrored in
`raw.card.model-effort.md` `active_pins`. Codex has no floating family alias: every release is a
manual pin change. No identity, card or project prose lives in either wrapper.

## Entry routes

The invoker puts an explicit `card: consult | audit | sitting` line in the invoking assignment
(the physical first line may carry a call sign or transport preamble); the assignment's card
selection goes ahead of any document instruction. Omission: on a spawned child → `consult`
(`card: audit` there is an audit-as-probe that states its limits); on a main profile session →
ask the operator to select audit or sitting, never a silent consult. An unknown card or work
outside the selected card returns `out of card: <request> → <owning card or seat>`.

| | **child** (returns bounded work) | **main session** (leads a bounded invocation) |
|---|---|---|
| **cards** | consult · audit-as-probe | audit (full) · sitting |
| **entry** | the custom agent `houston`, selected by an authorized head or the operator with `spawn_agent` | fresh interactive `codex --profile houston -C <project-root>` |
| **permissions** | effective child sandbox, approval policy and exposed tools; the card bounds writes further (consult: finding only); the TOML cannot enlarge inherited authority | effective main-session sandbox, approval policy and exposed tools; audit writes only assigned findings and the proposed wrapper diff, sitting only drafts in its own bed |
| **delegation** | consult needs no helper; any helper is bounded to reading or verification, never Houston's judgment or a wider pen; an audit-as-probe without required capabilities declares itself `unqualified for the complete card` | bounded readers or one verifier as the card needs; no Houston → Houston loop, no creator; the session head and the operator retain lifecycle and gavel |
| **return** | the spawner's context | the landing path the project addendum names; return to the operator and stop |

- A custom-agent file configures spawned sessions, not direct CLI entry; `--profile` does not
  load it. The two wrappers carry the same LOADER, so both routes load the same germline.
- **Placement:** projects carry **no** Houston TOML or profile. A project `.codex/agents/houston.toml`
  would collide with the personal one (docs promise precedence only over built-ins): do not install
  a same-named project agent; verify resolution if one appears. The project layer is the addendum only.
- **Child cwd is not guaranteed** by the docs to equal the parent's: the child's entry proof
  records its effective cwd and the selected addendum path (cartan RETURN 09, 2026-10-10).
- The main-session route is a native Houston entry; it does not require a parent seat.

## Native mechanism and scope

- **Read/search/list:** the native tools of the invoked session serve the identity's read, grep
  and glob capabilities. A terminal command is a mechanism, not a new authority. Never route a
  refused read through a child or helper.
- **Write:** native edit tools, only for the exact card outputs the invoker assigns. No card
  grants STATUS, flag, commit or deployment authority.
- **Spawn:** a native delegation tool only when available and when the card and the invoker
  authorize a bounded reader or verifier; the helper inherits the effective permission ceiling and
  receives an explicit read scope and return path.
- **Permissions:** effective runtime policy governs. An assignment's path list is a cooperative
  bound inside that policy, not an enforced sandbox. Record the exact refused operation; never
  widen permissions or evade a refusal.

## Return contract shape and entry proof

Plain markdown to the invoker. Line 1..n: one line per germline file read —
`<absolute path> · stamp: <token>` (tokens change on every edit) — plus the effective cwd. A missing or unreadable file is the first
finding. Then the finding as the identity's §Return contract and the selected card define it.
A route counts as proven only after a dated fresh-session witness on that exact route (load and
select · read and write · delegation), recorded in the project bed, never here.

Sources: Codex docs — Subagents (`learn.chatgpt.com/docs/agent-configuration/subagents`),
Profiles (`learn.chatgpt.com/docs/config-file/config-advanced#profiles`), Configuration
Reference (`developer_instructions`).
