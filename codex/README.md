# Codex portable surface

This directory is the compose-first authoring surface for portable Codex behavior on
majkee's office and home hosts. Edit here, review, and deploy outward with `deploy.sh`.
Never harvest live `~/.codex` state back into this repository.

## Deployment map

| Repository source | Live target | Semantics |
|---|---|---|
| `codex/AGENTS.md` | `~/.codex/AGENTS.md` | Global Cartan identity and working contract |
| `codex/agents/` | `~/.codex/agents/` | Personal Codex custom agents, additive when present |
| `codex/skills/` | `~/.agents/skills/` | Personal Codex skills, additive when present |

`deploy.sh` copies only these reviewed keep-set paths. It does not copy `config.toml`,
`hooks.json`, rules, credentials, memories, histories, sessions, databases, caches, logs,
installation identity, or trust hashes. Those surfaces are host-local until each earns an
explicit portable design and merge rule.

Candidate observations and experiments belong in `_staging/codex/`, not here. Promotion
into this directory requires evidence, review, and a clear live deployment target.
