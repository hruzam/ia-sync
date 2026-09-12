---
title: Stage A decision brief — Codex identity resolution
scope: codex-identity-resolution
status: PROPOSAL · awaiting majkee gavel · no implementation authority
authored: 2026-09-09
host: office · hruzam-120922
author: Cartan · resident owner
---

# Stage A decision brief — open decisions 1–5

## Recommendation at a glance

Gavel the smallest sufficient implementation: one Astrobley posture at
`codex/postures/astrobley.md`, deployed to `~/.codex/postures/astrobley.md`; keep the existing
spawned-agent adapter; add one Astrobley-only top-level profile source at
`codex/profiles/astrobley.config.toml`, deployed flat to `~/.codex/astrobley.config.toml`; make an
explicit `--profile astrobley` mandatory on launch and resume; and record RETURN topology inside
canonical BUS field 2 rather than adding schema.

No item below is implemented or behaviorally proved by this brief. Decisions 1–5 and the proposed
`codex/AGENTS.md` wording all require @majkee's gavel before Stage B.

## Resolved frame and evidence boundary

- Repository: `/home/hruzam/ia-sync`, branch `main`, HEAD `0f52f56`.
- Actual host: `office` / `hruzam-120922`. `MACHINE_NAME=office`; `/usr/bin/php74`, Valet, and
  `/home/hruzam/projects` are present; `machines.json` maps this hostname to `office` and Tailscale
  node `n5f4JzTU5Z11CNTRL`. The live Tailscale query returned no usable node ID, so the node-ID
  anti-spoof factor was not independently observed in this pass.
- Index: empty. Worktree: dirty with protected concurrent `runbook-upgrade`, journal, pulse, zsh,
  session-rescope, and remote-control session work. The identity-resolution directory was wholly
  untracked at inspection. No protected path was edited.
- Existing identity-resolution artifacts inspected before this write: `RUNBOOK.md`, `STATUS.md`,
  and `raw/draft.codex-session-identity-resolution.2026-09-06.md`. `codex/postures/` and
  `codex/profiles/` are absent, confirming Stage B has not begun.
- Installed CLI evidence: `codex-cli 0.153.4`. `codex --help` and `codex resume --help` both expose
  `-p, --profile` as a layer at `$CODEX_HOME/<name>.config.toml`; neither exposes a top-level
  `--agent-type`. `codex agents --help` exists and describes browsing sessions. Help inspection is
  syntax/discovery evidence only; no profiled launch, resume, session listing, or spawn was run.
- Current official OpenAI documentation says `--profile profile-name` overlays
  `~/.codex/profile-name.config.toml` on the base user config, with top-level keys in each profile:
  [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced). It lists
  `developer_instructions` as additional session instructions, while `model_instructions_file`
  replaces built-in instructions instead of `AGENTS.md`:
  [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).
- Official documentation also says standalone files in `~/.codex/agents/` define custom agents,
  are loaded as configuration layers for spawned sessions, and are identified by their `name`
  field: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Decision 1 — posture paths

**Recommend:**

| Coordinate | Exact path |
|---|---|
| Portable source | `/home/hruzam/ia-sync/codex/postures/astrobley.md` |
| Deployed target | `/home/hruzam/.codex/postures/astrobley.md` (`$HOME/.codex/postures/astrobley.md`) |
| Adapter pointer | `/home/hruzam/.codex/postures/astrobley.md` |

`postures/` is the narrow machine-facing noun already proposed by the draft. It keeps the stable
behavior contract separate from the two runtime adapters without creating a role registry or RPG
framework. Both known hosts use the `hruzam` home path, so an absolute deployed pointer is currently
both-host-valid and unambiguous to the model.

Use `developer_instructions` in both adapters to require reading this exact file before acting. Do
not use `model_instructions_file`: current official documentation describes that key as replacing
built-in instructions instead of `AGENTS.md`, which would undermine the intended default/override
resolution rather than compose with it.

**Uncertainty:** documentation establishes the config key and path layers, not that a model will
actually read and obey an instruction-pointed Markdown file. P2 and P6 must prove that behavior.
This mapping also assumes the repository's existing `$HOME/.codex` deployment convention; a custom
`CODEX_HOME` is not covered by the current deploy script and is out of this cut.

## Decision 2 — profile deployment mechanism

**Recommend:** extend the existing `deploy_codex()` leg in `deploy.sh`; do not use `install-pkgs`.

The exact Stage B mapping should be:

- additive directory deployment:
  `codex/postures/` -> `$HOME/.codex/postures/`;
- one explicit single-file deployment through existing `copy_file()`:
  `codex/profiles/astrobley.config.toml` -> `$HOME/.codex/astrobley.config.toml`.

This is a plain portable-file copy, which is exactly the responsibility already held by
`deploy_codex()`. That leg already supports `--codex-only`, itemized dry-run behavior, directory
creation, additive semantics, and backup-before-overwrite for single files. `install-pkgs` is
documented for out-of-repo installation work that rsync/copy cannot perform; it would add state and
indirection without need.

Use an explicit Astrobley profile copy in this first cut rather than a generic flat-directory loop.
That makes the deployment boundary match decision 3 and prevents unrelated files under
`codex/profiles/` from silently landing at the root of `~/.codex`.

**Proposed future commands, not run:**

```bash
bash deploy.sh --dry-run --codex-only
bash deploy.sh --codex-only               # only after majkee confirms the dry-run
cmp codex/postures/astrobley.md "$HOME/.codex/postures/astrobley.md"
cmp codex/profiles/astrobley.config.toml "$HOME/.codex/astrobley.config.toml"
cmp codex/agents/astrobley.toml "$HOME/.codex/agents/astrobley.toml"
cmp codex/AGENTS.md "$HOME/.codex/AGENTS.md"
```

These are Stage C candidates. Their behavior has not been tested against the not-yet-authored
sources, and this brief grants no deploy authority.

## Decision 3 — profile scope

**Recommend:** Astrobley alone earns a top-level profile in this implementation.

The repeated task class is specific: Astrobley has already been appointed to independent,
full-session work, and the 2026-09-06 attempt demonstrated that a custom-agent name pasted into a
root window does not produce the required sovereign topology. The portable `codex/AGENTS.md` also
requires a distinct repeated task class before adding another global role. No equivalent evidence
was presented here for architect, challenger, researcher, implementer, verifier, or
`harness_builder`.

Adding profiles for the full roster would enlarge deployment and behavioral proof sevenfold while
answering no current acceptance condition. A later repeated sovereign-session need can reuse the
same posture/profile pattern only after separate evidence and gavel.

## Decision 4 — resume law

**Recommend:** always repeat the profile explicitly:

```bash
codex resume --profile astrobley <SESSION_ID>
```

The installed 0.153.4 help accepts this option and identifies `<SESSION_ID>` as a UUID or session
name. Official documentation establishes profile selection through `--profile`; neither source
inspected here guarantees that a stored session retains or re-applies its original profile when the
operator omits the option. Repetition is therefore an inspectable authority declaration at the
resume boundary, not a claim about undocumented retention.

**Tested:** help/argument discovery only. **Untested:** an actual profiled launch, session discovery,
resume, retained thread context, reasserted Astrobley behavior, and the effect of omitting the
profile. P4 remains the behavioral proof and must record the operator's observed command. If the
installed CLI rejects or reorders the candidate spelling during P4, the observed working spelling
wins in the closing VERDICT without weakening the explicit-profile law.

## Decision 5 — RETURN topology without a schema fork

**Recommend:** record topology as the first provenance item inside canonical BUS field
`## 2. Commands and outcomes`.

Use this shape:

```markdown
## 2. Commands and outcomes

- Execution topology: `top-level profile` | `spawned subagent`.
- Basis: <exact launch/spawn command and observable result, or explicitly attributed operator
  attestation when process relation is not independently inspectable>.
```

If expected and observed topology disagree, repeat the disagreement and its evidence in
`## 4. Mismatches discovered`. Do not add a seventh heading, a new required frontmatter key, or a
new BUS kind.

The gaveled BUS guide fixes exactly six RETURN headings and defines field 2 as the home for exact
commands and outcomes. Execution topology is command/process provenance, so field 2 is the narrowest
semantic fit. Current `runbook-upgrade` RETURNs 24, 26, and 28 use an extra
`execution_topology` frontmatter key, but their own text limits it to operator testimony and the
canonical guide does not define that extra key. Preserve those historical artifacts; do not copy
their local extension into this session's schema.

**Uncertainty:** a model's self-report does not prove process ancestry or sovereign-window identity.
P2–P6 must distinguish model report, operator-observed launch command, client session listing, and
actual parent/child relation rather than upgrading any one source by repetition.

## Proposed `codex/AGENTS.md` override wording

Place this narrow paragraph after the resident introduction, subject to the same gavel:

> Cartan is the default top-level resident and integration owner when no operator-selected seat
> profile is active. A Codex session launched or explicitly resumed with `--profile <named-seat>`
> occupies that named top-level seat for the session. It must read the deployed named posture,
> accept project authority only from its assigned RUNBOOK or POINT, must not identify as Cartan or
> inherit Cartan's controller, STATUS, or integration ownership, and must not spawn a same-seat
> substitute. A seat name or `agent_type` pasted into an existing chat does not change that
> session's identity.

This keeps the unprofiled default deterministic while making the exception explicit, launch-time or
resume-time, named, and operator-controlled. The profile supplies posture; the RUNBOOK/POINT supplies
project scope.

## Gavel requested

@majkee: ACCEPT or amend decisions 1–5 and the exact `codex/AGENTS.md` paragraph above. Until that
single gavel arrives, Stage B is closed: no `codex/` authoring, deploy mapping, dry-run, runtime
mutation, or P0–P6 proof may begin.
