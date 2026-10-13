# For chatbots — where your skills live

You are a chat assistant (ChatGPT, Claude.ai, or the next one) working with majkee. Your skills
and, when assigned, your identity come from **one place**, in one GitHub repository. Read this
card once; it tells you where to look and how to read what you find.

## The repository

- GitHub: `hruzam/reposoma` (private; majkee grants you access via the GitHub connector, or
  hand-drops the files into your project memory — both are valid).
- The shared home inside it: **`.germline/`** — a hidden folder at the repository root.

## Where to search

| you need | path in the repo | filename shape |
|---|---|---|
| a **skill** (a method: how to do one kind of task) | `.germline/skills/` | `skill.<slug>.md` — one file = one skill |
| an **identity** (who you are for a project or seat, only when majkee assigns it) | `.germline/agents/<slug>/` | `identity.md` |
| a project-scoped skill or identity | `<project-repo>/.germline/` | same shapes |

There is deliberately **no index** — search the folder by filename. `skill.<slug>.md` is the only
skill shape; anything else in the repository is not a skill for you.

## How to read a skill file

1. The YAML frontmatter is the contract: `name` (the slug majkee will say), `description` (when it
   applies), and provenance (`source`, `twin`, `orphan`, `near-miss`, `source-commit`, `ported`).
   Provenance is for maintenance — you do not act on it.
2. The line `_Ported from the CLI skill — do not edit here …_` is maintenance framing, not part of
   the method. Skip it.
3. The body is the method, written in first person. When majkee names the skill (or the situation
   in `description` occurs), behave as the body says. Do not merge two skills; do not add steps.
4. If a step asks for something a tool would have fetched, the body says *"ask majkee for …"* —
   do exactly that; do not guess.

## Rules

- Skill files are **read-only** for you. If one seems wrong or stale, say so to majkee; he re-runs
  the port on his side. Never rewrite one from memory.
- Prefer the repository copy over any version in your project memory when both exist and differ;
  tell majkee they differ.
- Skills and identities are vendor-neutral by design: the same file is meant for every chat
  assistant. If something in a file only makes sense on a command line, it is a porting defect —
  report it.

Maintainer note (not for the chatbot): rule and layout in `README.md` beside this file; the port
tool is the `chatbot-port` skill on both CLI lines.
