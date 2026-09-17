# raw/date-name-frontmatter.md — sort-key evidence for the issue-card system

Made by: @Epoch (online research) + a ChatGPT cross-check ("wave"). Transcribed from the
operator's TURN 2 substrate 2026-09-17. Substrate — reached by explicit path, not served by
the resolver. The RUNBOOK's "one open question" (sort by name or frontmatter) rests on this.

Bottom line the RUNBOOK carries: **PATH/FILENAME = radar · FRONTMATTER = manifest · BODY =
payload.** Cheap deterministic routing key (a date + a couple associations in the name) →
cheap metadata inspection (frontmatter) → expensive body read. A date in the filename is
**repository data** and survives clone / checkout / host-move; filesystem **mtime is only the
observational state of one checkout** and resets on any git operation — different epistemic
classes. This cross-vendor invariant holds across Anthropic, OpenAI, Google, and Cursor
despite different harness designs; that invariance matters more than whether one vendor ships
a `Glob` this month. Semantic retrieval complements, does not replace, deterministic routing.

---

## @Epoch report (2026-09-16)

Trigger: do Codex/Claude Code/Cursor agents get cheap help from date-in-filename when
wandering non-vendor-primitive files, and do they surface frontmatter cheaply via
grep/glob/bash/py? Scope excludes vendor-native primitives (SKILL.md/.mdc) — those are
harness-auto-indexed; the interesting case is arbitrary files (CS.*.YYYY-MM-DD.md,
_mail/*/inbox/*.md) that nothing vendor-side indexes.

Findings:
- None of the three ship a "read frontmatter only" primitive for arbitrary files; all fall
  back to generic grep/glob/shell — assembly is the agent's. Frontmatter-cheap scanning is a
  CAPABILITY, not a behavior — it happens only if the harness (AGENTS.md/CLAUDE.md) tells the
  agent to filter by filename/frontmatter before reading bodies.
  Source: Claude Code tools reference; openai/codex #4443; Cursor search docs. Confidence H/M.
- Claude Code Glob sorts by mtime (cap 100, ignores .gitignore by default); Grep is
  ripgrep-based, supports head_limit/offset/output_mode:content — an agent can cheaply pull
  just frontmatter lines across a glob in one call; Read supports offset/limit. mtime is
  fragile as a recency signal — git checkout/clone/sync resets it; a filename date does not.
  The CS.*.YYYY-MM-DD.md convention is the correct hedge against exactly that failure mode.
  Source: code.claude.com/docs/en/tools-reference. Confidence H.
- Codex CLI exposes essentially one tool — shell (+ apply_patch through it); no dedicated
  Glob/Grep; its own prompt tells it to prefer rg / rg --files. So filename-date filtering and
  frontmatter peeks are 100% improvised shell one-liners — a strong, trivially-greppable
  filename convention matters MORE for Codex, not less. Source: openai/codex #4443 +
  prompt_with_apply_patch_instructions.md. Confidence M.
- Cursor: semantic Codebase Search + Instant Grep (custom regex engine); neither auto-surfaces
  frontmatter nor treats filename dates specially; exact-string tools, not embeddings, are the
  leverage point for date conventions. Source: Cursor blog + docs. Confidence H.
- Industry direction (third-party): Claude Code / Cursor / Devin lean on grep/find/direct
  reads over vector RAG for code-adjacent search — "fast, exact, deterministic." Confidence M.
- Practitioner note argues YYYY-MM-DD-slug.md is near-universal and frontmatter-first manifest
  scanning (~50-100 tok/doc vs 500-2000 for bodies) with a two-tier narrow-then-read pattern
  beats vector RAG below ~100-1000 docs. Numbers are DIRECTIONAL, not authoritative (small
  unattributed blog); treat as corroborating, candidate for a mirror/vega cross-check if it
  ever backs a canon decision. Confidence L-M.

Synthesis: date-in-filename helps concretely (cheapest signal = a filename match, zero reads;
strictly more durable than Glob's mtime-sort); tools show frontmatter cheaply only when the
agent chooses to assemble the peek; agents do it only when the harness biases them to;
Python frontmatter parsing appears only if an agent deliberately scripts it (heavier than
head/grep, for validation not filtering).

## ChatGPT cross-check ("wave")

Keeps the central idea, tightens claims:
- Real principle is not "dates are good filenames" but **low-entropy sortable metadata in the
  namespace**: `CS.reincarnation.cartan.2026-09-17.md` beats `2026-09-17.md` because an agent
  eliminates candidates by class + subject/seat + time without opening anything. Date is ONE
  dimension of the routing key. → directly supports TURN 2's ">=7 associations": put a couple
  discriminators in the name, the rest in frontmatter.
- Frontmatter carries what should not be forced into the filename: status, responds_to,
  supersedes, gate, participants, thread, valid_until.
- Vendor corrections: Claude Code on Linux may have Glob/Grep ABSENT from default toolset
  (searches via Bash bfs/ugrep), enable-able; Codex has apply_patch + others but discovery is
  still rg-based shell; Cursor DOES build a semantic index but does not index arbitrary YAML
  frontmatter as a manifest; **Gemini CLI** (missing from Epoch) has first-class glob /
  grep_search / read_file(limit) / read_many_files / shell — same filename→metadata→body
  pattern is cheap there too. Naming fix: Cursor is by Anysphere.
- "Only when prompted" is too binary — agents often spontaneously use cheap exact search
  because their system prompts bias them to; what is NOT guaranteed is the ORDERING
  (filename filter → metadata → body), which is exactly what repo discipline must supply.
- Would NOT canonize "vectors lose": semantic retrieval and deterministic routing solve
  different problems. Filename dates win "latest Cartan inbox item" (structure already in the
  query); semantic wins "which old discussion reasoned about transcript injection".

Canonizable bottom line (wave's wording): "For arbitrary repository artifacts, encode cheap,
durable, deterministic routing metadata in paths/filenames; put richer discriminators in small
frontmatter; instruct agents to narrow by namespace first, inspect metadata second, read full
bodies only after candidate reduction. Treat filesystem mtime as non-authoritative. Vendor
context/rule/skill mechanisms are a separate layer. Semantic retrieval complements this."
Resist canonizing the numeric claims (50-100 tok/doc, "vectors win above 1000 files") — weak
evidence.

Sources: code.claude.com/docs/en/tools-reference · github.com/openai/codex (prompt +
protocol base_instructions) · cursor.com/blog (fast-regex-search, secure-codebase-indexing) +
docs · github.com/google-gemini/gemini-cli (tools.md, gemini-md.md) · mindstudio.ai ·
zylos.ai/research 2026-06-14.
