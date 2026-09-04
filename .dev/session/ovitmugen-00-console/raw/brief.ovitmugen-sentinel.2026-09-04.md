---
type: brief
name: kukla-sentinel
date: 2026-09-04
thread: agentive-collaboration (conceptual) → park into practical project
status: DRAFT · agreed in principle (Symmetry + Asymmetry triangulated) · not yet implemented
sovereignty: HIGH — key lives in the definition file, protected by YAML/TOML comment spec, zero vendor-loader dependency
lineage: agent-file-custom-metadata thread 2026-09-04; rejected: xattr, JSON sidecar roster, database, developer_instructions embedding
tags: [#kukla-sentinel, #one-parser, #roster-is-a-view, #comments-are-the-seam, #group-is-a-list]
---

# Brief — `@kukla` sentinel: private sorting key in agent definition files

## Axioms (strike any that misread)
1. The key must live **inside** the definition file. A second file drifts.
2. The key must be **inert to every vendor loader** now and after updates — protection by spec, not by tolerance.
3. **One shape, one parser** across all three file types. No per-vendor branch.
4. `group` is a **list** from day one.
5. The roster is a **derived view**; any materialized roster is generated and gitignored.
6. No build beyond the parser until scanning is measurably slow.

## The seam  (#comments-are-the-seam)
YAML and TOML are parsed from byte one — there is no "before the engine" zone as in PHP. A comment is the construct the parser is *required* to tokenize and discard. That is the only channel guaranteed by specification rather than by a vendor's current leniency.

## Sentinel grammar  (#kukla-sentinel)
```
<comment-char> @kukla <one-line JSON object>
```
- Exactly one sentinel per file. Second occurrence → validation error, not merge.
- Must be a **single line**; multi-line JSON is not permitted (keeps the regex trivial).
- Comment char: `#` for both YAML frontmatter and TOML. `<!-- @kukla {...} -->` is reserved as the never-used fallback if a host ever loses comment support.
- Placement: inside the frontmatter block for `.md`; top of file for `.toml`.

### Schema (v1)
| key   | type          | required | notes |
|-------|---------------|----------|-------|
| group | string[]      | yes      | non-empty; lowercase slugs |
| tier  | integer       | no       | 1..3 |
| tags  | string[]      | no       | free |
| v     | integer       | no       | schema version, default 1 |

Unknown keys → warning, not error (forward compatibility for your own future).

## Examples — three file types, one shape

**Claude Code skill — `SKILL.md`**
```yaml
---
name: opencart-b2b-review
description: Reviews OpenCart B2B pricing code
# @kukla {"group":["review","opencart"],"tier":2}
---
```
Optional mirror if Anthropic tooling ever reads it (keep sentinel authoritative):
```yaml
metadata:
  kukla: {group: [review, opencart], tier: 2}
```

**Claude Code subagent — `.claude/agents/reviewer.md`**
```yaml
---
name: reviewer
description: Security-minded code review
model: opus
# @kukla {"group":["review","security"],"tier":2}
---
```

**Codex agent — `.codex/agents/reviewer.toml`**
```toml
# @kukla {"group":["review","security"],"tier":2}
name = "reviewer"
description = "Security-minded code review"
```

## Reader — Python  (#one-parser)
```python
#!/usr/bin/env python3
"""kukla.py — derive the agent roster from @kukla sentinels."""
import json, re, sys
from pathlib import Path

SENTINEL = re.compile(r'^\s*#\s*@kukla\s+(\{.*\})\s*$', re.M)
GLOBS = ['.claude/agents/*.md', '.codex/agents/*.toml', '**/SKILL.md']
SCHEMA = {'group': list, 'tier': int, 'tags': list, 'v': int}

def read(path: Path) -> dict | None:
    hits = SENTINEL.findall(path.read_text(encoding='utf-8'))
    if not hits:
        return None
    if len(hits) > 1:
        raise ValueError(f'{path}: multiple @kukla sentinels')
    meta = json.loads(hits[0])
    if not isinstance(meta.get('group'), list) or not meta['group']:
        raise ValueError(f'{path}: group must be a non-empty list')
    for k, v in meta.items():
        if k in SCHEMA and not isinstance(v, SCHEMA[k]):
            raise ValueError(f'{path}: {k} must be {SCHEMA[k].__name__}')
        if k not in SCHEMA:
            print(f'warn: {path}: unknown key {k}', file=sys.stderr)
    return meta

def roster(root: Path = Path('.')) -> list[dict]:
    out = []
    for g in GLOBS:
        for p in sorted(root.glob(g)):
            m = read(p)
            if m:
                out.append({'file': str(p), 'vendor': p.suffix.lstrip('.'), **m})
    return out

def by_group(name: str, root: Path = Path('.')) -> list[dict]:
    return [r for r in roster(root) if name in r['group']]

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(by_group(arg) if arg else roster(), indent=2))
```
Usage:
```
python3 kukla.py              # full roster
python3 kukla.py review       # agents in group "review"
```

## Reader — shell fallback (no validation, quick look)
```sh
grep -rHn '^#\s*@kukla' .claude/agents .codex/agents --include='*.md' --include='*.toml'
```

## Roster as view  (#roster-is-a-view)
Nothing is maintained. If a materialized roster is wanted later:
```
agentctl roster > .kukla/roster.json    # gitignored, generated-and-gitignored tier
```
Regenerate on demand; nobody edits it, so it cannot drift.

## Brakes
- Do **not** build the cache until a scan over both machines is measurably slow.
- Do **not** reach for a database until a query turns relational (joins across time/model/group).
- Do **not** add a second channel (`metadata.kukla`) as authoritative; mirror only.

## Rejected (with reason, append-only)
- filesystem xattr — git/cp/rsync/tar drop them; fatal for two-machine Tailscale + git-as-bus.
- JSON sidecar roster — second file, drifts on first forgotten update.
- database — second source of truth, not greppable/diffable, no relational query exists yet.
- `developer_instructions` embedding — visible to model, consumes work space; kept only as theoretical fallback.
- `x-` prefixed top-level keys — no host spec grants them; skill packager hard-rejects.

## Open (underlined items)
- `tier` semantics (1..3) not yet defined — define when the first dispatcher consumes it.
- Whether `**/SKILL.md` glob is too wide on the office machine (vendor skill mirrors).
- Empirical check: does `.codex/agents/*.toml` reject unknown keys? (optional; sentinel makes it moot.)

## Mosaic
gate: sentinel grammar → reader: one regex + validation → view: roster on demand → telemetry: validation errors map malformed agent files. Closed as a loop; graduates to mechanism only when a dispatcher consumes `group`.
