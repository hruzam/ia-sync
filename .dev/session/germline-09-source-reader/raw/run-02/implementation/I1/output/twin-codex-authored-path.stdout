---
name: guide
description: Temple guide access over ~/reposoma/raw.guides/ in two modes — consult shared law silently while doing another task, or serve one GUIDE.md or res/ chapter verbatim on an explicit list/read/show request ($guide, "read the runbook guide", "show the fanout chapter"). Not for OpenAI product documentation (openai-docs) and not for writing guides.
---

# Guide — temple guide reader

The guides' single home is `~/reposoma/raw.guides/`: one topic = one slug folder = one
`GUIDE.md`, subchapters beside it in `res/`. Read-only: never edit, create, or reorganize a
guide. Writer law: `~/reposoma/raw.guides/guide-writing/GUIDE.md`.

## Two modes — consult is not display

- **Consult** — this skill was selected while another task depends on shared law: read the
  resolved file, apply it, and cite its path and the specific clause in the answer. Do not
  print guide text the caller never asked to see.
- **Display** — the caller explicitly asks to list, read, show, or print a guide or chapter:
  serve the resolved file verbatim and complete, frontmatter included. The caller wanted the
  law, not a digest.

## Resolution — one rule, only GUIDE.md and res/ resolve

- no argument → the catalog: for every `~/reposoma/raw.guides/*/GUIDE.md`, report the slug,
  its `title:` / `machine:` / `verified:` frontmatter values, and the `res/` chapter
  basenames. Build the catalog from those lines alone; do not read guide bodies.
- `<slug>` → `~/reposoma/raw.guides/<slug>/GUIDE.md`. No such folder → show the catalog;
  resolve nothing else.
- `<slug> <chapter>` → the `res/*.md` file whose **basename contains `<chapter>` as a
  case-insensitive substring** (the one matching rule: `turns` resolves `fanout-turns.md`).
  Exactly one match → resolve it. Several → report the matching basenames and ask; resolve
  nothing. None → show that GUIDE.md's `## Manifest`; resolve nothing.

## Contract (shared law: guide-writing res/slug-directories.md — point, never restate)

- Side-directories (`raw/`, `src/`, `ast/`, `cod/`, and any other) are never resolved here;
  they are reached only by explicit path from a manifest line.
- Manifest check at the gaveled granularity, one warning line per finding, never recursive:
  each `res/*.md` chapter appears per-file in the owning `## Manifest`; each side-directory
  appears as exactly one directory entry, its children never inspected; an undeclared sibling
  file or side-directory is drift.
- Staleness: `verified:` + `half_life_days:` past expiry → prefix one warning naming the
  verified date. A `PUBLISHED MIRROR` banner → state that the owning project is the truth.
