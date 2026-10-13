#!/usr/bin/env python3
"""guide-census — read-only census of raw.guides/ for the guide-model audit.

Facts only, never verdicts. Writes nothing; prints markdown to stdout.
Usage:  python3 guide-census.py [RAW_GUIDES_DIR] [--today YYYY-MM-DD]
Default RAW_GUIDES_DIR: ~/reposoma/raw.guides
Law it reads against: raw.guides/guide-writing/GUIDE.md (+ res/slug-directories.md).
"""
import re, sys, datetime as dt
from pathlib import Path

REQ = ("title", "scope", "audience", "machine", "verified")
SLOTS = ("res", "raw", "src", "ast", "cod")
MIRROR = re.compile(r"^<!--\s*PUBLISHED MIRROR", re.M)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
RESREF = re.compile(r"(?<![\w/.-])res/([\w.@-]+\.md)")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

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
    if not fm or "verified" not in fm:
        return "—"
    d = DATE.search(fm["verified"])
    if not d:
        return "?date"
    if "half_life_days" not in fm:
        return f"{d.group()} no-clock"
    try:
        limit = int(re.match(r"\d+", fm["half_life_days"]).group())
    except (AttributeError, ValueError):
        return f"{d.group()} ?hl"
    age = (today - dt.date.fromisoformat(d.group())).days
    return f"{d.group()} {'STALE' if age > limit else 'fresh'} {age}/{limit}d"

def fm_cell(fm):
    if fm is None:
        return "no-yaml"
    miss = [k for k in REQ if k not in fm]
    return "ok" if not miss else "−" + ",".join(miss)

def audit_folder(d, today):
    g = d / "GUIDE.md"
    files = sorted(p for p in d.rglob("*.md"))
    mirror = sum(1 for p in files if MIRROR.search(p.read_text(errors="replace")))
    if not g.exists():
        return dict(slug=d.name, kind="mirror-dir" if mirror else "no-GUIDE",
                    note=f"{len(files)} md, {mirror} mirror-bannered")
    text = g.read_text(errors="replace")
    fm = frontmatter(text)
    res = sorted((d / "res").glob("*.md")) if (d / "res").is_dir() else []
    no_chof = [p.name for p in res
               if "chapter-of" not in (frontmatter(p.read_text(errors="replace")) or {})]
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
        for p in siblings:
            if p.is_dir() and p.name == "res":
                unreg += [f"res/{c.name}" for c in res if c.name not in man]
            elif p.is_dir():
                if f"{p.name}/" not in man:
                    unreg.append(p.name + "/")
            elif p.name not in man:
                unreg.append(p.name)
    dangling = sorted({r for r in RESREF.findall(text) if not (d / "res" / r).exists()})
    flags = []
    if mirror:
        flags.append(f"mirror×{mirror}")
    if not KEBAB.match(d.name):
        flags.append("non-kebab")
    if (fm or {}).get("shape") == "model":
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
        shape=(fm or {}).get("shape", "—"), clock=clock(fm, today),
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
        flags = (["mirror"] if MIRROR.search(t) else []) + \
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
