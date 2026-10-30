# source-reader — lazy, read-only terminal source browser

Run through the existing experimental dispatcher. No shell-startup body or new alias:

```zsh
exp-run source-reader --help
exp-run source-reader catalog --json
exp-run source-reader show /exact/lexical/path/from/catalog/SKILL.md
exp-run source-reader show <catalog-id>
exp-run source-reader guide
exp-run source-reader guide runbook
exp-run source-reader guide runbook fanout
exp-run source-reader browse --plain
```

Requires existing zsh and Python 3 stdlib. Optional `fzf` provides interactive selection;
without it, or with `--plain`, select a numbered row. UI and diagnostics use stderr;
selected file bytes alone use stdout. NonTTY `browse` prints metadata and never prompts.
Cancellation returns 1; invalid selection, ambiguous/absent chapter, unknown slug or read
failure returns 2. Catalog and successful reads return 0. Output is raw bytes without
Markdown rendering, a pager or interpretation of instructions. Reading a source never
loads it into a model or changes runtime activation.

The default map uses the current user's ia-sync authored germline, deployed `.germline`,
temple `reposoma/raw.guides`, authored Codex/Claude skills, personal `.agents/skills` and
`.claude/skills`, ia-sync project skill roots, the observed Codex `.codex/skills/.system`,
the declared Claude account-sync root and two admin candidates. Source checkout location
is derived when run from ia-sync; deployed copies use `~/ia-sync`. These are discovery
boundaries, not universal runtime discovery rules. Missing/empty/unreadable roots are
visible gaps; undeclared plugin/bundled roots and publisher identity remain unknown.

Each invocation builds an ephemeral metadata catalog: stable ID, lexical absolute path,
resolved symlink target, family, source-file kind, root ID, vendor, origin, name and
available leading frontmatter. IDs incorporate root ID, origin and lexical path. Same
names have no precedence or merging; `show` accepts only an exact ID or catalog path.
Frontmatter is a bounded flat metadata projection (128 lines / 32 KiB); YAML structures
and multiline scalar bodies are not evaluated. Catalog never reads document bodies or
hashes their contents. All catalog/browse output says: **found on disk; runtime
visibility/activation unknown**.

Discovery is shallow: root child `SKILL.md`; guide `*/GUIDE.md` and immediate `res/*.md`;
germline `agents/*/{identity.md,binding.*.md,method.*.md,cards/*.md,methods/*.md}` and
`skills/skill.*.md`. Account-sync scans one observed account bucket's child skills; zero
or multiple buckets are disclosed instead of broadening the crawl. Symlinked declared
sources remain selectable with their lexical and resolved paths. No home/cache crawl,
durable index, network, model, install or source execution is involved.

Guide resolution follows `codex/skills/guide/SKILL.md`: no/unknown slug lists guide
metadata and chapter basenames; known slug reads its complete GUIDE. A chapter query
matches case-insensitive basename substrings within immediate `res/` only. Ambiguity
lists every match without a body; zero match emits only the owning `## Manifest`
section. Duplicate slugs across roots are ambiguous; use exact `show` selection.
Stale metadata, published-mirror and shallow manifest warnings use stderr. Legacy
Claude recursive fallback is deliberately not adopted; side directories never resolve.

For a bounded fixture/source map, pass `--roots /absolute/roots.json` before or after
the command. The JSON object contains `roots`, an array of objects with `id`, `kind`,
`vendor_if_any` (string or null), `origin`, `absolute_path` and `layout` (one of
`skills`, `synced-skills`, `guides`, `germline`). Root IDs must be distinct. An empty
array is allowed. The checked-in immutable fixture map names this ia-sync source-tree
location; audit commands and CLI fixture tests use those exact paths:

```zsh
python3 -B ~/ia-sync/zsh/experimental/source-reader/test_source_reader.py
```

Control-panel law: `zsh/guides/guide-for-builder.md` §Architecture rules and parent
`experimental/README.md`. This is a lazy experimental runner; no activation/install
or graduation claim follows from source tests.
