# markdown-core-patch — install task

```
version:     2.0
hosts:       home office
automation:  auto
src-root:    ~/www/elements-factory/applications-in-common
```

---

## What this installs

A targeted patch to `~/.config/sublime-text/Lib/python33/markdown/core.py`
that works around a Python 3.3 + Pep562 interaction in Sublime Text 4.

## Root cause

Python-Markdown 3.2.2 includes a PEP 562 compatibility shim (`pep562.py`).
In Python < 3.7 (`PY37 = False`), both `markdown/__init__.py` and
`markdown/util.py` call `Pep562(__name__)`, which replaces those entries in
`sys.modules` with proxy wrapper objects. In ST's actual Python 3.3.6
environment, this proxy replacement causes ALL module-level relative imports
in `core.py` to silently bind `None` in `core.py`'s globals — both on fresh
load and on plugin reload (where the Pep562 proxy is already active).

The fix: change the three methods that use those names (`build_parser`,
`__init__`, `registerExtensions`) to fetch the needed objects directly from
`sys.modules` at call time. By the time `Markdown()` is instantiated, all
submodules are correctly registered in `sys.modules` regardless of the Pep562
proxy state.

## Patch summary (v2.0)

- `build_parser()` — fetches all five `build_*` functions via `sys.modules`
- `__init__()` — initialises `output_formats` from `sys.modules['markdown.serializers']`
  and uses `sys.modules['markdown.util'].HtmlStash()`
- `registerExtensions()` — fetches `Extension` from `sys.modules['markdown.extensions']`

## Symptoms without patch

```
File "markdown/core.py", line 103, in build_parser
    self.preprocessors = build_preprocessors(self)
TypeError: 'NoneType' object is not callable
```

## History

- v1.0 (2026-08-07): module-level rebinding block — worked on first load,
  failed on plugin reload (sys.modules state unpredictable at import time)
- v1.1 (2026-08-07): fixed NameError in v1.0 del cleanup — still same root issue
- v2.0 (2026-08-07): replaced with method-level sys.modules lookups at call time

---

<!-- install:check -->
```bash
CORE="$HOME/.config/sublime-text/Lib/python33/markdown/core.py"
[ -f "$CORE" ] || { echo "markdown core.py not found — Package Control not run yet?"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
CORE="$HOME/.config/sublime-text/Lib/python33/markdown/core.py"

python3 << 'PATCHEOF'
import sys, os

core_path = os.path.expanduser(
    "$HOME/.config/sublime-text/Lib/python33/markdown/core.py"
)

with open(core_path, 'r') as f:
    content = f.read()

V2_MARKER = "sys.modules['markdown.preprocessors']"

# v2.0 already applied — nothing to do
if V2_MARKER in content:
    print("patch v2.0 already applied, nothing to do")
    sys.exit(0)

changed = False

# ─── Patch 1: build_parser — use sys.modules at call time ────────────────────
BP_OLD = '''    def build_parser(self):
        """ Build the parser from the various parts. """
        self.preprocessors = build_preprocessors(self)
        self.parser = build_block_parser(self)
        self.inlinePatterns = build_inlinepatterns(self)
        self.treeprocessors = build_treeprocessors(self)
        self.postprocessors = build_postprocessors(self)
        return self'''

BP_NEW = '''    def build_parser(self):
        """ Build the parser from the various parts. """
        # ST Python 3.3 + Pep562 workaround: module-level relative imports may bind
        # None; fetch submodules from sys.modules at call time to bypass that.
        _prep  = sys.modules['markdown.preprocessors']
        _blkp  = sys.modules['markdown.blockprocessors']
        _inlp  = sys.modules['markdown.inlinepatterns']
        _treep = sys.modules['markdown.treeprocessors']
        _postp = sys.modules['markdown.postprocessors']
        self.preprocessors  = _prep.build_preprocessors(self)
        self.parser         = _blkp.build_block_parser(self)
        self.inlinePatterns = _inlp.build_inlinepatterns(self)
        self.treeprocessors = _treep.build_treeprocessors(self)
        self.postprocessors = _postp.build_postprocessors(self)
        return self'''

if BP_OLD in content:
    content = content.replace(BP_OLD, BP_NEW, 1)
    changed = True
    print("patched: build_parser")
else:
    print("ERROR: build_parser anchor not found — markdown version may differ")
    sys.exit(1)

# ─── Patch 2: __init__ — fix util.HtmlStash() + re-init output_formats ───────
INIT_OLD = '''        self.build_parser()

        self.references = {}
        self.htmlStash = util.HtmlStash()'''

INIT_NEW = '''        self.build_parser()

        # ST Python 3.3 + Pep562 workaround: output_formats is a class-level dict
        # evaluated at import time (to_html_string/to_xhtml_string may be None then);
        # replace it as an instance attribute with values fetched from sys.modules now.
        _ser = sys.modules['markdown.serializers']
        self.output_formats = {
            'html':  _ser.to_html_string,
            'xhtml': _ser.to_xhtml_string,
        }

        self.references = {}
        self.htmlStash = sys.modules['markdown.util'].HtmlStash()'''

if INIT_OLD in content:
    content = content.replace(INIT_OLD, INIT_NEW, 1)
    changed = True
    print("patched: __init__ (util.HtmlStash + output_formats)")
else:
    print("ERROR: __init__ anchor not found — markdown version may differ")
    sys.exit(1)

# ─── Patch 3: registerExtensions — use sys.modules for Extension ──────────────
REG_OLD = '''        for ext in extensions:
            if isinstance(ext, str):
                ext = self.build_extension(ext, configs.get(ext, {}))
            if isinstance(ext, Extension):
                ext._extendMarkdown(self)
                logger.debug(
                    'Successfully loaded extension "%s.%s".'
                    % (ext.__class__.__module__, ext.__class__.__name__)
                )
            elif ext is not None:
                raise TypeError(
                    'Extension "{}.{}" must be of type: "{}.{}"'.format(
                        ext.__class__.__module__, ext.__class__.__name__,
                        Extension.__module__, Extension.__name__
                    )
                )
        return self'''

REG_NEW = '''        # ST Python 3.3 + Pep562 workaround: Extension may be None from relative import.
        _Extension = sys.modules['markdown.extensions'].Extension
        for ext in extensions:
            if isinstance(ext, str):
                ext = self.build_extension(ext, configs.get(ext, {}))
            if isinstance(ext, _Extension):
                ext._extendMarkdown(self)
                logger.debug(
                    'Successfully loaded extension "%s.%s".'
                    % (ext.__class__.__module__, ext.__class__.__name__)
                )
            elif ext is not None:
                raise TypeError(
                    'Extension "{}.{}" must be of type: "{}.{}"'.format(
                        ext.__class__.__module__, ext.__class__.__name__,
                        _Extension.__module__, _Extension.__name__
                    )
                )
        return self'''

if REG_OLD in content:
    content = content.replace(REG_OLD, REG_NEW, 1)
    changed = True
    print("patched: registerExtensions (Extension)")
else:
    print("ERROR: registerExtensions anchor not found — markdown version may differ")
    sys.exit(1)

# ─── Cleanup: remove old v1.x module-level block if present ──────────────────
OLD_BLOCK_MARKER = '# ── ST Python 3.3 + Pep562 workaround'
if OLD_BLOCK_MARKER in content:
    # Find and replace the entire old block through the end comment
    import re
    old_block_pattern = r'# ── ST Python 3\.3 \+ Pep562 workaround ─+.*?# ── end workaround ─+\n?'
    replacement_comment = (
        '# NOTE: module-level relative imports (from . import util, from .preprocessors import ...)\n'
        '# may bind None in ST\'s embedded Python 3.3 when the Pep562 proxy is active in sys.modules.\n'
        '# All affected names (util, build_*, Extension, to_*_string) are now resolved at call time\n'
        '# via sys.modules inside the methods that use them — see build_parser(), __init__(),\n'
        '# registerExtensions(). No module-level fix is needed or possible here.\n'
    )
    content_new = re.sub(old_block_pattern, replacement_comment, content, flags=re.DOTALL)
    if content_new != content:
        content = content_new
        changed = True
        print("cleaned up: old v1.x module-level block replaced with comment")

if changed:
    with open(core_path, 'w') as f:
        f.write(content)
    print("patch v2.0 written to", core_path)
else:
    print("nothing changed (unexpected — check manually)")
PATCHEOF
```
<!-- /install:run -->

---

## After install

Restart Sublime Text for the patched `core.py` to take effect. The in-memory
`sys.modules` cache survives package reloads but not full process restarts.

## Fragility note

Package Control may overwrite `core.py` when upgrading the Markdown library.
If `alt+m` crashes again after a Package Control upgrade, re-run:
```bash
bash ~/ia-sync/install-pkgs/run.sh unmark markdown-core-patch
bash ~/ia-sync/install-pkgs/run.sh update
```
Then restart Sublime Text.
