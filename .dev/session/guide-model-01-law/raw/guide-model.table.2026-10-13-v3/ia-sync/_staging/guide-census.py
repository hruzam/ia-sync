#!/usr/bin/env python3
"""guide-census — read-only census of raw.guides/ for the guide-model audit.

Facts only, never verdicts. Writes nothing; prints markdown to stdout.
Usage:  python3 guide-census.py [RAW_GUIDES_DIR] [--today YYYY-MM-DD]
Default RAW_GUIDES_DIR: ~/reposoma/raw.guides
Law it reads against: raw.guides/guide-writing/GUIDE.md (+ res/slug-directories.md).

Checks — all mechanical:
  frontmatter   YAML block present; required keys present and non-empty (C4)
  clock         verified + half_life_days → fresh / STALE (L3)
  registration  every sibling named by an exact token in ## Manifest or ## Functions (C1)
  dangling      res/ pointers in GUIDE.md that resolve to no file (C2)
  chapters      chapter-of: present, and equal to the slug
  table drift   shape: model guides — Functions rows against occasion: fields (C3)
  flags         mirror banner (first non-empty line) · non-kebab slug · undeclared dirs · manifest heading
Assumptions and limits — verify by reading when they matter:
  frontmatter is line-based `key: value` (no nested YAML); dates are ISO
  a name mentioned anywhere in the Manifest or Functions section counts as registered, prose included
  a function listed in both Functions and Manifest is not flagged
v2 2026-10-13 exact-token registration (Wave R4) · v3 2026-10-13 boundary fixes (Wave F4)
"""
import re, sys, datetime as dt
from pathlib import Path

REQ = ("title", "scope", "audience", "machine", "verified")
SLOTS = ("res", "raw", "src", "ast", "cod")
MIRROR = re.compile(r"^<!--\s*PUBLISHED MIRROR")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
RESREF = re.compile(r"(?<![\w/.-])res/([\w.@-]+\.md)")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOKEN = re.compile(r"[\w.@/~-]+")

def named(toks, slug, rel, bare):
    """exact registration: 'res/x.md' · 'x.md' · 'raw/' (or 'raw/<file>') · '…/<slug>/<rel>'."""
    for t in toks:
        if t == rel or (bare and t == bare) or t.endswith(f"/{slug}/{rel}"):
            return True
        if rel.endswith("/") and (t.startswith(rel) or f"/{slug}/{rel}" in t):
            return True
    return False

def mirrored(text):
    """a mirror carries the banner as its first non-empty line (guide-publishing); quotes elsewhere don't count."""
    for ln in text.splitlines():
        if ln.strip():
            return bool(MIRROR.match(ln.strip()))
    return False

def val(fm, key):
    """a frontmatter value, trimmed and unquoted; '' when absent or empty."""
    v = (fm or {}).get(key)
    return v.strip().strip("\"'").strip() if v else ""

def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None                              # no YAML block at all
    keys = {}
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", ln)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return keys

def manifest(text):
    """(heading, body, lawful) — prefer the law's '## Manifest…'; else any '## …manifest…'."""
    for pat, lawful in ((r"^##\s+(Manifest\b[^\n]*)$", True),
                        (r"^##\s+([^\n]*manifest[^\n]*)$", False)):
        flags = re.M | re.S | (0 if lawful else re.I)
        m = re.search(pat + r"(.*?)(?=^##\s|\Z)", text, flags)
        if m:
            return m.group(1).strip(), m.group(2), lawful
    return None, None, True

def functions(text):
    m = re.search(r"^##\s+Functions\b[^\n]*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None

def table_drift(fbody, res):
    """model guides: every function's occasion: equals its Functions row; every row's file has one."""
    if fbody is None:
        return ["no-Functions-table"]
    rows = {}
    for ln in fbody.splitlines():
        m = RESREF.search(ln)
        if ln.lstrip().startswith("|") and m:
            rows[m.group(1)] = ln.strip().strip("|").split("|")[0].strip()
    out = []
    for p in res:
        occ = (frontmatter(p.read_text(errors="replace")) or {}).get("occasion")
        if occ is None:
            if p.name in rows:
                out.append(f"{p.name}:no-occasion")
            continue
        occ = occ.strip().strip('"\'')
        if p.name not in rows:
            out.append(f"{p.name}:no-row")
        elif rows[p.name] != occ:
            out.append(f"{p.name}:occasion≠row")
    return out

def clock(fm, today):
    v = val(fm, "verified")
    if not v:
        return "—"
    d = DATE.search(v)
    if not d:
        return "?date"
    try:
        when = dt.date.fromisoformat(d.group())
    except ValueError:
        return f"{d.group()} ?date"
    hl = val(fm, "half_life_days")
    if not hl:
        return f"{d.group()} no-clock"
    m = re.match(r"\d+", hl)
    if not m:
        return f"{d.group()} ?hl"
    limit, age = int(m.group()), (today - when).days
    return f"{d.group()} {'STALE' if age > limit else 'fresh'} {age}/{limit}d"

def fm_cell(fm):
    if fm is None:
        return "no-yaml"
    miss = [k for k in REQ if not val(fm, k)]
    return "ok" if not miss else "−" + ",".join(miss)

def audit_folder(d, today):
    g = d / "GUIDE.md"
    files = sorted(p for p in d.rglob("*.md"))
    mirror = sum(1 for p in files if mirrored(p.read_text(errors="replace")))
    if not g.exists():
        return dict(slug=d.name, kind="mirror-dir" if mirror else "no-GUIDE",
                    note=f"{len(files)} md, {mirror} mirror-bannered")
    text = g.read_text(errors="replace")
    fm = frontmatter(text)
    res = sorted((d / "res").glob("*.md")) if (d / "res").is_dir() else []
    chof = {p.name: val(frontmatter(p.read_text(errors="replace")), "chapter-of") for p in res}
    no_chof = [n for n, c in chof.items() if not c]
    bad_chof = [n for n, c in chof.items() if c and c != d.name]
    siblings = [p for p in d.iterdir() if p.name != "GUIDE.md"]
    dirs = [p.name for p in siblings if p.is_dir()]
    head, man, lawful = manifest(text)
    fbody = functions(text)
    if man is not None or fbody is not None:
        man = (man or "") + (fbody or "")
    unreg = []
    if siblings and man is None:
        unreg = [f"(no manifest section: {len(siblings)} siblings)"]
    elif man is not None:
        toks = {t.rstrip(".,;:") for t in TOKEN.findall(man)}
        for p in siblings:
            if p.is_dir() and p.name == "res":
                unreg += [f"res/{c.name}" for c in res if not named(toks, d.name, f"res/{c.name}", c.name)]
            elif p.is_dir():
                if not named(toks, d.name, f"{p.name}/", None):
                    unreg.append(p.name + "/")
            elif not named(toks, d.name, p.name, p.name):
                unreg.append(p.name)
    dangling = sorted({r for r in RESREF.findall(text) if not (d / "res" / r).exists()})
    flags = []
    if mirror:
        flags.append(f"mirror×{mirror}")
    if not KEBAB.match(d.name):
        flags.append("non-kebab")
    if bad_chof:
        flags.append("chapter-of≠slug:" + ",".join(bad_chof))
    if val(fm, "shape") == "model":
        drift = table_drift(fbody, res)
        if drift:
            flags.append("table-drift:" + ",".join(drift))
    if head and not lawful:
        flags.append("manifest-heading≠law")
    other = [x for x in dirs if x not in SLOTS]
    if other:
        flags.append("dirs:" + ",".join(other))
    return dict(
        slug=d.name, kind="folder", lines=len(text.splitlines()), fm=fm_cell(fm),
        shape=val(fm, "shape") or "—", clock=clock(fm, today),
        res=f"{len(res)}" + (f" (✗chapter-of {len(no_chof)})" if no_chof else ""),
        side=" ".join(s for s in SLOTS[1:] if s in dirs) or "—",
        jnl="y" if any(p.name.startswith("dev-journal") for p in siblings) else "—",
        bg="y" if (d / "BACKGROUND.md").exists() else "—",
        unreg=", ".join(unreg) or "—", dangling=", ".join(dangling) or "—",
        flags=" ".join(flags) or "—")

def main(argv):
    today = dt.date.today()
    if "--today" in argv:
        i = argv.index("--today")
        today = dt.date.fromisoformat(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    root = Path(argv[1] if len(argv) > 1 else "~/reposoma/raw.guides").expanduser()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    folders = [audit_folder(d, today) for d in sorted(root.iterdir()) if d.is_dir()]
    loose = sorted(p for p in root.glob("*.md"))
    names = {d["slug"] for d in folders}

    print(f"# guide-census · {root} · {today}\n")
    print("Facts only — verdicts belong to the auditor.\n")
    print("## Folders\n")
    print("| slug | lines | fm | shape | clock | res | side | jnl | bg | unregistered | dangling | flags |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in folders:
        if r["kind"] != "folder":
            print(f"| {r['slug']} | — | {r['kind']} | | | | | | | | | {r['note']} |")
            continue
        print("| {slug} | {lines} | {fm} | {shape} | {clock} | {res} | {side} | {jnl} | {bg} "
              "| {unreg} | {dangling} | {flags} |".format(**r))
    print("\n## Loose top-level files (legacy zone)\n")
    print("| file | lines | fm | clock | flags |")
    print("|---|---|---|---|---|")
    for p in loose:
        t = p.read_text(errors="replace")
        fm = frontmatter(t)
        toks = set(re.split(r"[-.]", p.stem))
        overlap = sorted(n for n in names if n in toks or n == p.stem)
        flags = (["mirror"] if mirrored(t) else []) + \
                ([f"name-overlap:{','.join(overlap)}/"] if overlap else [])
        print(f"| {p.name} | {len(t.splitlines())} | {fm_cell(fm)} | {clock(fm, today)} "
              f"| {' '.join(flags) or '—'} |")

    f = [r for r in folders if r["kind"] == "folder"]
    print("\n## Counts\n")
    print(f"- entries {len(folders) + len(loose)} · slug folders {len(f)} · "
          f"other folders {len(folders) - len(f)} · loose files {len(loose)}")
    print(f"- frontmatter: no-yaml {sum(r['fm'] == 'no-yaml' for r in f)} · "
          f"missing keys {sum(r['fm'].startswith('−') for r in f)}")
    print(f"- STALE {sum('STALE' in r['clock'] for r in f)} · "
          f"no half-life clock {sum('no-clock' in r['clock'] for r in f)}")
    print(f"- unregistered siblings in {sum(r['unreg'] != '—' for r in f)} slugs · "
          f"dangling res/ refs in {sum(r['dangling'] != '—' for r in f)} slugs")
    print(f"- shape declared {sum(r['shape'] != '—' for r in f)} · "
          f"BACKGROUND.md {sum(r['bg'] == 'y' for r in f)} · "
          f"journals {sum(r['jnl'] == 'y' for r in f)}")

if __name__ == "__main__":
    main(sys.argv)
