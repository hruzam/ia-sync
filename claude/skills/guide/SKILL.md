---
name: guide
description: Invoke as /guide. Temple guide reader over ~/reposoma/raw.guides/ — the single guide surface (B′, 2026-08-20). Folder-per-guide skill model — /guide = list slugs · /guide <slug> = read <slug>/GUIDE.md · /guide <slug> <chapter> = read one chapter file. Legacy loose files and published project mirrors resolved by fallback. Staleness + mirror warnings. Carries the 3-line writer law.
---

I serve the temple's guides from their single home: `~/reposoma/raw.guides/`.

The law behind me (gaveled 2026-08-20, B′ + skill-model taxonomy): **executable/deployed
lives on the surgical table (`~/ia-sync`); knowledge/readable lives in the temple.** The
canonical shape mirrors skills 1:1 — **one topic = one slug folder = one `GUIDE.md`**,
optional chapter files beside it. The old `~/.config/zsh/guides/` is a pointer stub; I
never read it as a source.

## Resolution (hardcoded on purpose — fixed filename is the contract)

**`/guide <slug>`** →
1. `~/reposoma/raw.guides/<slug>/GUIDE.md` exists → Read it, present **verbatim** (the
   operator wanted the guide, not my digest).
2. No such slug → legacy fallback: case-insensitive substring match on basenames across
   `raw.guides/**/*.md`. One hit → read it. Many → list candidates, ask. None → show the
   slug listing.

**`/guide <slug> <chapter>`** → `raw.guides/<slug>/<chapter>*.md` (substring on chapter
filename). This is the fine-slice read: one chapter, not the whole guide.

**Bare `/guide`** → derived overview, no hand-index (derived-index principle):
1. `Glob ~/reposoma/raw.guides/*/GUIDE.md` → the slug list.
2. One Grep pass for the signal line: pattern `^(title|machine|verified):` with
   `output_mode: content` over that glob — never read whole files for a listing.
3. Render: `slug · title · machine · verified`, plus chapter files per slug (basenames
   only), then two marked zones below: **legacy loose files** (top-level `*.md`, not yet
   migrated) and **published mirrors** (project folders, banner-marked, read-only).

## Staleness organ (run on every read, cheap)

- Frontmatter has `verified:` + `half_life_days:` → compare against today. Expired →
  prepend: `⚠ stale knowledge-card — verified <date>, half-life exceeded; refresh-cycle
  territory (re-synthesize, never hand-patch).`
- File carries a `PUBLISHED MIRROR · do not edit here` banner → prepend: `◈ read-only
  mirror — source of truth is the owning project (see guide-publishing).`
- Neither → serve silently.

## Sibling classes + orphan flag (the manifest law)

A slug folder holds four classes: `GUIDE.md` (canonical entry + manifest) · chapters
(`chapter-of:` frontmatter) · attachments (non-md; registered ONLY via GUIDE.md's
`## Manifest`) · legacy (manifest-marked "superseded, do not follow"). When I read a
slug and see a sibling file NOT named in its manifest, I append one line:
`⚠ orphan sibling: <name> — not in manifest (drift; register or remove).` I never read
attachments or legacy files unless explicitly asked.

## Naming guard (the anti-hell rule)

Slugs are **topic-specific** (`remote-control`, `machine-home`, `temple-mail`) — never
generic buckets (`machine`, `tooling`, `misc`). If a slug's chapters stop belonging to
ONE topic, that is two guides — say so when I see it.

## Writer law (the 3 lines — full manual: `/guide guide-writing`)

1. New guide → new slug folder `~/reposoma/raw.guides/<slug>/GUIDE.md`; chapters as
   sibling files. NEVER into `~/.config/zsh/guides/` — that tree is a stub.
2. YAML frontmatter required: `title:` · `scope:` (= slug) · `audience:` · `machine:` ·
   `verified:` (volatile → knowledge-card extras: `half_life_days`, `recheck`,
   `verify_cmd`).
3. Commit reposoma the same session — under B′ there is no deploy.sh safety net; an
   uncommitted guide does not exist on the other machine or in the RAG.
