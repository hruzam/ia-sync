---
name: refresh
description: >
  Invoke as /refresh <scope>. Unified research fetch-and-synthesize runner.
  Reads scope config from raw.research/<scope>/draft/README.md, fetches sources,
  writes substrate to report/, updates card body with compressed synthesis.
  Scope is mandatory — if omitted, lists available scopes.
  Use for any periodic or on-demand knowledge refresh: news feeds, docs snapshots,
  model catalogs.
tools:
  - Read
  - WebFetch
  - Write
---

I am the `/refresh` skill — a single runner for all research fetch-and-synthesize cycles.
The variable part (what to fetch, how to output, whether to persist) lives in the scope's
`draft/README.md`. I read it, execute the cycle, and prompt once before writing anything.

## Persist discipline

Scope `persist:` field controls git tracking of `report/` output:

- `ephemeral` — report/ is gitignored by default. Old substrate files are cleaned up or
  archived. Use for periodic refreshes: news feeds, docs snapshots, model catalogs.
- `canonical` — report/ content is tracked. Use for wide-scope or cross-measured research
  worth carrying across machines and into future synthesis passes. Operator adds a
  `!raw.research/<scope>/report/` negation to .gitignore at scope creation time.
- `ask` — I prompt the operator before writing. Decide per-run.

When in doubt: if the output is a briefing you will read once and act on → `ephemeral`.
If it is a synthesis artifact that future sessions need to read → `canonical`.

## Steps

1. **Check scope argument.** If missing:
   - List `~/reposoma/raw.research/` subdirs
   - Ask which scope to run
   - Stop here

2. **Read scope config** from `~/reposoma/raw.research/<scope>/draft/README.md`.
   Extract: `sources_file`, `output_path`, `card`, `output_mode`, `window_days` (default 7),
   `persist`. If README is missing, report the error, list available scopes, stop.
   Note: if the README contains a `pull:` section, ignore it — that section is for `/pull`.

3. **Read sources** from `sources_file` (JSONL). Each record: `id`, `url`, `title`,
   `domain`, `tags`, and optionally `note`, `tier`, `x`.

4. **Fetch each source** via WebFetch.
   - `output_mode: briefing` — apply `window_days` recency filter; skip older items.
   - `output_mode: snapshot` — fetch full content, no date filter.
   - Sources where `url` contains `x.com` or `note` contains `manual-check`: cannot be
     auto-fetched — collect for the footer, do not attempt.
   - On fetch failure: note the source, continue — do not stop the run.

5. **Synthesize in-session** — grouped by `domain` field, emitted to chat.
   Domain order: `research-depth` → `tools-releases` → `policy-governance` → `czech-scene`
   → (any other domains, alphabetical).
   Sources with no items in window: note inline as "(no items this window)".

6. **Cross-reference look-back** (runs in memory — no writes yet):
   - Read the last 3 existing substrate files from `raw.research/<scope>/report/`
     (sorted by date descending, skip missing). Combined with this run's items in memory,
     the window covers N=4 runs total.
   - For each item across all runs, build an entity key:
     1. arXiv ID if present in URL (e.g. `arxiv.org/abs/2407.XXXXX`)
     2. Canonical URL (strip query params, trailing slash)
     3. Fallback: normalized title — lowercase, strip punctuation, collapse whitespace
   - Find any entity appearing in **2 or more independent source IDs** across the window.
   - **Independence caveat:** aggregators (e.g. `latent-space`, any source tagged
     `aggregator`) echo primary sources. A convergence that includes only aggregators, or
     mixes one primary + one aggregator, is marked `(weak — aggregator echo)`. Two or more
     primary sources = full convergence. Mark explicitly; do not suppress.
   - Produce a `Convergence:` line:
     - Hits found → one short phrase per converging entity, source IDs in parentheses,
       strength marker if weak. Example:
       `Grok 4.5 launch (import-ai, latent-space — weak: aggregator echo) · Fable GPU kernel (import-ai, deep-learning-focus)`
     - No hits → `none in window`
   - *Note: if title-dedup degrades noticeably at larger source counts, the next step is a
     JSONL sidecar index per scope. Not built yet — implement only when pain is demonstrated.*

7. **Prepare write artifacts** (written together on confirmation):

   **A — Substrate file** (`output_path` with `<YYYY-MM-DD>` substituted to today):
   ```
   # <scope> — substrate
   _Fetched: <date> | Window: <N> days | Sources: <fetched>/<total>_

   ## research-depth
   [raw item list — title, date, one-line summary per item]

   ## tools-releases / policy-governance / czech-scene / ...
   [same pattern per domain]

   ## Run metadata
   - No items in window: [ids]
   - Feed flags: [ids with notes — dead feeds, broken RSS, etc.]
   - Manual-check (not fetched): [ids]
   ```

   **B — Card body run block** *(only if `card:` is present in scope README)*
   Prepend above `<!-- older runs -->` comment in the card body:
   ```
   ## <YYYY-MM-DD>

   **Lead:** <2–4 sentence compressed synthesis of the most significant items>

   **Convergence:** <output from Step 6 — entity list with source IDs, or "none in window">

   **Quiet:** <comma-separated ids of sources with no items in window>

   **Feed flags:** <id (note) per flagged source>

   **Manual-check:** <id (note) per X-only or manual-check source>

   ---
   ```
   Keep the last 4 run blocks. Prune any blocks beyond that (oldest first).
   If `card:` absent from scope README → skip 7-B entirely; do not touch `raw.settings/`.

8. **Single confirm prompt** — emit footer first, then ask once:
   ```
   ## Run summary
   - Sources fetched: N / total
   - No items in window: [ids]
   - Feed flags: [ids with notes]
   - Manual-check (not fetched): [ids]
   - Convergence: <one-liner from Step 6>
   - Persist: <ephemeral|canonical|ask>
   - Card: <card path>  ← omit this line if no card: in scope README

   Write substrate to report/? (yes / no)                       ← no card defined
   Write substrate to report/ and update card? (yes / no)       ← card defined
   ```
   **On yes:** write all prepared artifacts (7-A always; 7-B + `verified:` update only if
   `card:` defined in scope README).
   **On no:** nothing written — in-session synthesis only.

## Output shape for briefing mode (Step 5)

```
## <domain label>

**<title>** (<author if present>) — <1–2 sentence synthesis of items in window>
[repeat per source with items]
```

Tight — briefing bullets, not summaries.
