# markdown-preview-settings — install task

```
version:     1.0
hosts:       home office
automation:  auto
src-root:    ~/www/elements-factory/applications-in-common
```

---

## What this installs

`MarkdownPreview.sublime-settings` in Sublime Text's `Packages/User/`.

MarkdownPreview's default extension list includes several `pymdownx.*` extensions
(`pymdownx.superfences`, `pymdownx.betterem`, `pymdownx.magiclink`, etc.). These
extensions import `markdown.extensions.attr_list` at module load time, which does
not exist in Sublime Text's bundled Python 3.3 environment. The result is a hard
crash (`ImportError`) whenever MarkdownPreview tries to render a file.

This settings file overrides `markdown_extensions` to use only stdlib-safe extensions,
removing all `pymdownx.*` entries.

---

## Source

```
experiments/editor-pin-sublime/MarkdownPreview.sublime-settings
```

---

## Smoke test (after install)

Open any `.md` file in Sublime, press `alt+m`. Expect: browser opens rendered HTML,
no error in Sublime console (`Ctrl+\``). If console still shows `ImportError: No module
named 'markdown.extensions.attr_list'` — Sublime needs a restart (not just reload).

---

<!-- install:check -->
```bash
[ -d "$HOME/.config/sublime-text/Packages/User" ] || { echo "Sublime Text not installed or never launched"; exit 1; }
[ -f "$SRC/experiments/editor-pin-sublime/MarkdownPreview.sublime-settings" ] || { echo "source file not found at $SRC/experiments/editor-pin-sublime/MarkdownPreview.sublime-settings"; exit 1; }
```
<!-- /install:check -->

<!-- install:run -->
```bash
DEST="$HOME/.config/sublime-text/Packages/User/MarkdownPreview.sublime-settings"
if [ -e "$DEST" ]; then
    echo "exists — backing up to $DEST.bak before overwrite"
    cp "$DEST" "$DEST.bak"
fi
cp "$SRC/experiments/editor-pin-sublime/MarkdownPreview.sublime-settings" "$DEST"
echo "installed MarkdownPreview.sublime-settings"
```
<!-- /install:run -->
