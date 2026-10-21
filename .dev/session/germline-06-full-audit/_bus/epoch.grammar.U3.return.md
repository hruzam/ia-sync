---
from: epoch (subagent, Claude, spawned by Flight) · unit U3 addendum · date: 2026-10-21
status: native return preserved verbatim (inline hand-back copied by Flight; no edits)
---

# @Epoch report: CLI grammar for "program + function + free text"
Date: 2026-10-21. Scope: default radar plus the question. No file writes.

Live-verified this run (H): clig.dev, the MCP draft tools spec, and the Anthropic "Define tools" page. Everything else below is from training memory (M/L). These are stable conventions, but I did not re-fetch them. The per-tool rows (git, kubectl, npm, Rake, Nix, Cargo and so on) were not re-checked, so treat them as memory.

## (1) Conventions table
Parse-safety is about the raw line pasted into a shell, a URL, YAML or Markdown.

| Form | Example | Used by | Parse-safety | Readability |
|---|---|---|---|---|
| Space-separated noun-verb or verb-noun | `docker container create`, `gh pr list`, `kubectl get pods`, `git remote add` | git, gh, kubectl, docker, cargo, npm | High. Whitespace tokenizes. Shell-safe. | High |
| `ns:task` (colon) | `rake db:migrate`, `npm run build:prod`, `task web:build`, `yarn workspace:cmd` | Rake, Gulp, npm script names, go-task | High in shell. Collides with `scheme:` URLs, YAML `key: value` (a colon plus space ends a key), and Nix `path:`. A bare `a:b` is fine in YAML. | Good |
| `pkg@ver` | `npm i react@18`, `pnpm add pkg@latest` | npm, yarn, pnpm | Fine. Clashes with scoped `@org/pkg`, emails and mentions. | Good for a version, poor for a function |
| `target#attr` | `nix build .#pkg`, `flake#attr` | Nix | Unsafe. `#` starts a shell comment after whitespace, and it is the URL fragment marker. | Medium |
| Dotted address | `module.name.attr` (Terraform), `pkg.Func` (Go), `admin.tools.list` (MCP) | Terraform, Go, MCP | High. Collides only with filenames and domains. | Good for addressing a sub-item |
| `::` path | `crate::mod::item` | Rust and C++ | Fine in shell (`::` is inert). Reads as a Rust path. | Good only to Rust readers |
| Underscore or hyphen prefix | `github_list_prs`, `server__tool` | Anthropic API, MCP clients, OpenAI | Highest. It is a single token. | Medium. It is an identifier, not a phrase. |
| Slash path | `docs/guide/intro`, `owner/repo` | gh (`owner/repo`), URLs, paths | Ambiguous with filesystem paths and URLs. | Good |
| Target plus flags | `make test`, `just --list`, `--flag value` | Make, just, task | High. `just` takes `recipe arg…`, with space-separated recipes. | High |
| `&`, `&&`, `;`, `|`, `>` | `a && b` | Shell only | Unsafe. These are shell operators. | Reads like prose ("and") |

## Standards verified live
- clig.dev (accessed 2026-10-21; H). It says "Either `noun verb` or `verb noun` ordering works, but `noun verb` seems to be more common", and cites `docker container create`. It also says "Prefer flags to args", and that two or more positional args for different things is a smell. It advises lowercase names with dashes only, and warns against ambiguous subcommands and against arbitrary abbreviations, since a later addition can break scripts that relied on a prefix.
- MCP draft spec, Tools (accessed 2026-10-21; H). Tool names SHOULD be 1 to 128 characters, case-sensitive, and use only A-Z, a-z, 0-9, `_`, `-` and `.`. Spaces, commas and other special characters SHOULD NOT appear. `admin.tools.list` is given as a valid example. Clients that aggregate servers should disambiguate by prefixing a server identifier. The spec does not fix `server__tool`; that double underscore is a client convention (M, from memory).
- Anthropic "Define tools" (accessed 2026-10-21; H). The name regex is `^[a-zA-Z0-9_-]{1,128}$`, so dots are not allowed on the Claude API even though the MCP spec allows them. It advises "meaningful namespacing" by service prefix (`github_list_prs`, `slack_send_message`). It also advises consolidating related operations into fewer tools with an `action` parameter rather than one tool per verb.

## (2) Forms most commonly favoured for program + function + free text
1. **Space-separated: `program function: free text`, or `program function -- free text`.** This is the dominant CLI idiom (clig.dev, git, gh, kubectl, docker). It is trivially tokenizable: split on whitespace, take the first two tokens, and treat the rest as the payload. It has no operator collisions. The weakness is that the free text is ambiguous unless it is quoted or delimited. The `--` end-of-options marker is the POSIX convention for "everything after this is literal."
2. **Colon namespace: `program:function`, with free text after a space.** This is the Rake, go-task and npm-script idiom. It reads as a single address and splits on the first `:`. Residual risk: a YAML key (`a:b` is fine, `a: b` is not), URL schemes, and Nix `path:`. The usual mitigation is to keep the address to `[a-z-]+:[a-z-]+` and put the free text after a space or `--`.
3. **Dotted or underscore identifier: `program.function` or `program_function`.** This is the agent-tool naming idiom. Dots suit MCP; underscores are the only option on the Claude API regex. It is the safest to parse but reads as an identifier, not a sentence. For addressing a sub-item inside a named thing, dotted paths (Terraform, Go) are the most widely used. `#` (Nix) is the least safe.

## (3) `&` and `&&` risks
- In a POSIX shell, `&` backgrounds the preceding command and `&&` chains on success. In zsh, `ctrl journal-continuity&audit-beds` pasted raw would background `ctrl journal-continuity` and then run `audit-beds` as a separate command. This is a real hazard if the line is ever pasted into a terminal or passed through `sh -c`, instead of being treated only as text or quoted.
- The same applies to `|`, `;`, `>` and `<`. A grammar that uses any of these as a delimiter is unsafe without quoting.
- Outside the shell, `&` is also the URL query separator and an HTML entity prefix, so it appears in many other contexts. Prose also reads `&` as "and", so `journal-continuity&audit-beds` can look like two separate functions when one name is intended.
- I found no CLI convention that uses `&` as a namespace or subcommand separator (M; absence from memory, not from an exhaustive search). Mainstream tools reserve it for the shell.
- Not found: any 2025-2026 guidance from Google, Microsoft or the 12-factor CLI that prescribes a separator (L; I did not search these). Only clig.dev and the two vendor docs above were verified.

## (4) Sources
- https://clig.dev/ (accessed 2026-10-21; H)
- https://modelcontextprotocol.io/specification/draft/server/tools (accessed 2026-10-21; H)
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools (accessed 2026-10-21; H)
- Everything else (git, kubectl, docker, npm, Rake, just, Nix, Terraform, Cargo, Go; POSIX shell operators; `--` convention): training memory, not re-fetched this run (M).

Sections to refresh: [per-tool rows (git, kubectl, npm, Rake, just, Nix, Terraform, Cargo, Go); Google and Microsoft CLI style guides; 12-factor CLI; OpenAI tool naming]
