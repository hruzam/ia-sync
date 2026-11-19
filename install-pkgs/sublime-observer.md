# sublime-observer — install task

```
developed-on: home (hruzam)
source:       ~/unikuklatrix/nablarva/toolbox/sublime-observer/ (payload: SublimeObserver/, five files)
status:       not qualified; the first install is the normal-profile witness of nablarva session sublime-observer-X1-file-publish
version:      1.1
hosts:        home
automation:   manual
src-root:     ~/unikuklatrix/nablarva/toolbox/sublime-observer
```

> **manual** until majkee's GO on that session's gate. The runner only gates on `check`
> below, then points here. Do the steps by hand, then record it:
> `bash ~/ia-sync/install-pkgs/run.sh mark sublime-observer`.
 

---

## What this installs

The Sublime Text package `SublimeObserver`. When the operator shares a view (command palette,
one toggle), the editor keeps a file copy of that view's text and state under
`/run/user/<uid>/sublime-observer/` for CLI agents to read with ordinary file tools. Views
that are not shared are never published. No socket, no notification, no control function.

The package is a copy of exactly five files into `~/.config/sublime-text/Packages/SublimeObserver/`
(never a symlink): `.python-version`, `SublimeObserver.sublime-commands`,
`SublimeObserver.sublime-settings`, `contract.py`, `publisher.py`. The source folder's
`README.md` and `tests/` are never installed.

Reader contract, limits and tests: `~/unikuklatrix/nablarva/toolbox/sublime-observer/README.md`.

**Trust note.** Published files are readable by every process running as the same user;
sharing is not per-agent isolation. Only views the operator shares are published. While
Sublime runs, `publisher.json` and `index.json` exist even with nothing shared, so a
same-user process can see that the editor is running (no content).

**Runtime path.** The settings default (`"root": null`) resolves to
`$XDG_RUNTIME_DIR/sublime-observer` when that variable names a private 0700 directory, else
`/run/user/<uid>/sublime-observer`. On home both are `/run/user/1000/sublime-observer`.
Directory mode 0700, files 0600. Heartbeat 1 s; a reader treats a heartbeat older than 3 s
as "publisher not live".

**Plugin host.** The check accepts only `plugin_host-3.14`, the only host this package has been verified on.

---

## Check alone (no other task touched)

`bash run.sh update` runs this check, but it also installs every other new or stale **auto**
task on this host. To run only this task's check:


>from `majkee`
```bash
bash install-pkgs/run.sh update
host: hruzam (home) · state: /home/hruzam/.local/state/ia-sync/installed.json
  chatgpt-desktop        1.0       already current, skip
  claude-desktop         1.0       already current, skip
  codex-cli              1.0       already current, skip
  harden-host            1.0       already current, skip
  markdown-core-patch    2.1       already current, skip
  markdown-preview-settings 1.0       already current, skip
  netOrchestrating       1.0       manual — run steps in netOrchestrating.md, then: run.sh mark netOrchestrating
  sublime-keymap         1.2→1.3 manual — run steps in sublime-keymap.md, then: run.sh mark sublime-keymap
  sublime-observer       1.0       already current, skip
  tmux                   1.0       already current, skip
  tmux-pin-bus           1.0       already current, skip
  zellij                 1.0       already current, skip
```



```bash
cd ~/ia-sync/install-pkgs && SRC="$HOME/unikuklatrix/nablarva/toolbox/sublime-observer" \
  bash -c "$(awk '$0=="<!-- install:check -->"{i=1;next} $0=="<!-- /install:check -->"{i=0} i && substr($0,1,3)!="\140\140\140"' sublime-observer.md)"
```
>from `majkee`

```bash
cd ~/ia-sync/install-pkgs && SRC="$HOME/unikuklatrix/nablarva/toolbox/sublime-observer" \
  bash -c "$(awk '$0=="<!-- install:check -->"{i=1;next} $0=="<!-- /install:check -->"{i=0} i && substr($0,1,3)!="\140\140\140"' sublime-observer.md)"

prereqs ok (Sublime build 4215) — do the install steps by hand

```



`[X]` Expected last line: `prereqs ok (Sublime build NNNN) — do the install steps by hand`.

---

## Install (by hand)

Run the check first. Then paste this block as a whole (it runs in its own `bash`, so a
`STOP` never closes your shell). It has two paths:

- **First install** (no `Packages/SublimeObserver` yet): the five files are staged in
  `~/.config/sublime-text/.SublimeObserver-install-staging` (same filesystem, outside
  `Packages/`), compared with the source, then moved into `Packages/SublimeObserver` with one
  `mv`, so Sublime never sees a partial package. The block refuses if the staging name already
  exists (a leftover: inspect and remove it by hand). When a step of the block fails, the block
  removes the staging directory and leaves nothing in the profile. A run that is interrupted
  (killed, power loss, terminal closed) can leave the staging directory behind; the next run
  then stops and names it. Sublime may stay open.
- **Update** (the folder exists and holds only the five names): each of the five files is
  replaced by a fresh copy (`cp --remove-destination`: the old name is unlinked first, so a
  destination that is a hard link to some other file never writes into that file). Best done
  with Sublime closed, or followed by a restart: while it runs, Sublime may reload the plugin
  mid-copy (**inferred**). A mismatch after a copy leaves the folder partly replaced; rerun the
  block or use Removal.

Ownership is judged by the five file names only: any `Packages/SublimeObserver` folder that
holds nothing but those names is treated as this task's copy and is overwritten (or, by
Removal, deleted), whatever its content. The guards look at `Packages/SublimeObserver` and its
five files only; if `~/.config/sublime-text` or `Packages/` is itself a symlink, the copy goes
wherever it points, unchecked.

```bash
bash <<'EOF'
set -u
S="$HOME/unikuklatrix/nablarva/toolbox/sublime-observer/SublimeObserver"
P="$HOME/.config/sublime-text/Packages"
T="$P/SublimeObserver"
STG="$HOME/.config/sublime-text/.SublimeObserver-install-staging"
# order matters: the Python pin first, contract.py before publisher.py (publisher imports it)
FILES=".python-version SublimeObserver.sublime-settings SublimeObserver.sublime-commands contract.py publisher.py"
made=0
trap '[ "$made" = 1 ] && [ -d "$STG" ] && [ ! -L "$STG" ] && command rm -r -- "$STG"' EXIT
[ -d "$P" ] || { echo "STOP: $P does not exist"; exit 1; }
[ ! -L "$T" ] || { echo "STOP: $T is a symlink; this task installs by copy only — inspect it by hand"; exit 1; }
for f in $FILES; do
  if [ ! -f "$S/$f" ] || [ -L "$S/$f" ]; then echo "STOP: source file missing or not regular: $S/$f"; exit 1; fi
done
if [ -e "$T" ]; then
  # update: guarded in-place replacement of the five files
  [ -d "$T" ] || { echo "STOP: $T exists and is not a directory"; exit 1; }
  other="$(cd "$T" && find . -mindepth 1 -printf '%P\n' | grep -vxF -e .python-version \
    -e SublimeObserver.sublime-settings -e SublimeObserver.sublime-commands -e contract.py -e publisher.py)"
  if [ -n "$other" ]; then
    echo "STOP: $T holds entries this task does not own:"; printf '%s\n' "$other" | sed 's/^/  /'; exit 1
  fi
  for f in $FILES; do
    if [ -L "$T/$f" ] || { [ -e "$T/$f" ] && [ ! -f "$T/$f" ]; }; then echo "STOP: $T/$f is not a regular file"; exit 1; fi
  done
  # fresh inodes: unlink each destination name first, never write through a hard link
  for f in $FILES; do command cp --remove-destination -- "$S/$f" "$T/$f" || { echo "FAILED copying $f"; exit 1; }; done
  for f in $FILES; do cmp -s -- "$S/$f" "$T/$f" || { echo "MISMATCH after copy: $f"; exit 1; }; done
  echo "ok: five files replaced in $T (restart Sublime if it was open)"
else
  # first install: stage, verify, one mv
  if [ -e "$STG" ] || [ -L "$STG" ]; then echo "STOP: staging $STG already exists — inspect and remove it by hand"; exit 1; fi
  mkdir -- "$STG" || { echo "STOP: cannot create $STG"; exit 1; }
  made=1
  for f in $FILES; do command cp -- "$S/$f" "$STG/$f" || { echo "FAILED staging $f"; exit 1; }; done
  # verify staged files against the source
  for f in $FILES; do cmp -s -- "$S/$f" "$STG/$f" || { echo "MISMATCH in staging: $f"; exit 1; }; done
  [ "$(stat -c %d -- "$STG")" = "$(stat -c %d -- "$P")" ] || { echo "STOP: staging and Packages/ are on different filesystems"; exit 1; }
  if [ -e "$T" ] || [ -L "$T" ]; then echo "STOP: $T appeared during staging"; exit 1; fi
  command mv -T -- "$STG" "$T" || { echo "FAILED moving staging into $T"; exit 1; }
  made=0
  echo "ok: five files installed into $T"
fi
ls -la "$T"
EOF
```
>to oraculum
```
ok: five files installed into /home/hruzam/.config/sublime-text/Packages/SublimeObserver
total 56
drwxr-xr-x 2 hruzam hruzam  4096 16. lis 00.44 .
drwx------ 6 hruzam hruzam  4096 16. lis 00.44 ..
-rw-r--r-- 1 hruzam hruzam 19765 16. lis 00.44 contract.py
-rw-r--r-- 1 hruzam hruzam 13904 16. lis 00.44 publisher.py
-rw-r--r-- 1 hruzam hruzam     4 16. lis 00.44 .python-version
```


It writes only `Packages/SublimeObserver/` and, during a first install, the staging directory.
It never touches `Packages/User/`, `SFTP`, `Terminal` or any other package.

**Restart after a first install?** Not expected. Sublime watches `Packages/` and loads a new
package folder while it runs; that is Sublime's general behavior, **inferred** — the disposable
trials copied the package in before launch, so a live load of this package was never observed.
That Sublime ignores the dot-named staging directory beside `Packages/` is also inferred. If the
checks below fail, quit Sublime normally (not a kill), start it again and recheck.

### Verify by eye

1. Console (`` ctrl+` ``): no traceback naming `SublimeObserver`, and no line starting
   `sublime-observer: not publishing`.
2. Command palette (`ctrl+shift+p`): **Sublime Observer: Share This View (toggle)** is listed.
> to oraculum -  sublime ribbon  message: `refuse to share .... operator vault (.majkee)`  


3. The publisher file appears (nothing needs to be shared yet):

   ```bash
   ls -la "/run/user/$(id -u)/sublime-observer/"
   jq '{sublime_build, plugin_python, heartbeat_interval_s, heartbeat_at}' "/run/user/$(id -u)/sublime-observer/publisher.json"
   ```

   Expect a `drwx------` directory with `publisher.json`, `publisher.lock`, `index.json`, `views/`;
   `plugin_python` 3.14.x (a 3.3.x value means the wrong plugin host — restart Sublime);
   `heartbeat_at` grows when you run the `jq` line again a few seconds later.

>to oraculum:
```bash
total 8
drwx------  3 hruzam hruzam 100 16. lis 01.10 .
drwx------ 15 hruzam hruzam 560 16. lis 01.07 ..
-rw-------  1 hruzam hruzam 123 16. lis 01.04 index.json
-rw-------  1 hruzam hruzam 268 16. lis 01.10 publisher.json
drwx------  2 hruzam hruzam  40 16. lis 01.04 views
{
  "sublime_build": "4215",
  "plugin_python": "3.14.6",
  "heartbeat_interval_s": 1.0,
  "heartbeat_at": 1794787821.470717
}

```

Then record it:

```bash
bash ~/ia-sync/install-pkgs/run.sh mark sublime-observer
```

> to oraculum:

```bash
bash ~/ia-sync/install-pkgs/run.sh mark sublime-observer
host: hruzam (home) · state: /home/hruzam/.local/state/ia-sync/installed.json

```


---

## Removal

Deletes `Packages/SublimeObserver/` and nothing else. Stops if that folder holds anything
other than the five file names, or is a symlink. Ownership is by those five names only (see
Install): a folder of that name holding only those names is deleted whatever its content.

```bash
bash <<'EOF'
set -u
T="$HOME/.config/sublime-text/Packages/SublimeObserver"
[ ! -L "$T" ] || { echo "STOP: $T is a symlink, not this task's copy — inspect it by hand"; exit 1; }
[ -e "$T" ] || { echo "nothing at $T"; exit 0; }
[ -d "$T" ] || { echo "STOP: $T is not a directory"; exit 1; }
other="$(cd "$T" && find . -mindepth 1 -printf '%P\n' | grep -vxF -e .python-version \
  -e SublimeObserver.sublime-settings -e SublimeObserver.sublime-commands -e contract.py -e publisher.py)"
if [ -n "$other" ]; then
  echo "STOP: $T holds entries this task does not own:"; printf '%s\n' "$other" | sed 's/^/  /'; exit 1
fi
command rm -r -- "$T" && echo "removed $T"
EOF
```

Then check the runtime directory (give Sublime a few seconds):

```bash
ls -la "/run/user/$(id -u)/sublime-observer" 2>&1
```

>to oraculum response:

```bash
bash <<'EOF'
set -u
T="$HOME/.config/sublime-text/Packages/SublimeObserver"
[ ! -L "$T" ] || { echo "STOP: $T is a symlink, not this task's copy — inspect it by hand"; exit 1; }
[ -e "$T" ] || { echo "nothing at $T"; exit 0; }
[ -d "$T" ] || { echo "STOP: $T is not a directory"; exit 1; }
other="$(cd "$T" && find . -mindepth 1 -printf '%P\n' | grep -vxF -e .python-version \
  -e SublimeObserver.sublime-settings -e SublimeObserver.sublime-commands -e contract.py -e publisher.py)"
if [ -n "$other" ]; then
  echo "STOP: $T holds entries this task does not own:"; printf '%s\n' "$other" | sed 's/^/  /'; exit 1
fi
command rm -r -- "$T" && echo "removed $T"
EOF

removed /home/hruzam/.config/sublime-text/Packages/SublimeObserver


```
>check

```bash
ls: cannot access '/run/user/1000/sublime-observer': No such file or directory
```

Expected: `No such file or directory`. On unload the package removes its own files and the
directory (code: `Store.shutdown`). That Sublime unloads a package whose folder is deleted
while it runs is **inferred**, not observed. If the directory is still there: quit Sublime
normally (a graceful exit runs the same cleanup — observed in the disposable trial) and check
again. If it is still there with no Sublime running, removing it is your judgment: the
command below does not check that no publisher is running or that the directory holds only
this package's files.

```bash
command rm -r -- "/run/user/$(id -u)/sublime-observer"
```

Then:

```bash
bash ~/ia-sync/install-pkgs/run.sh unmark sublime-observer
```

**What removal does not undo.** The package itself writes only inside its runtime directory
(code: every write in `contract.py` is under that root; `publisher.py` writes no file and
never saves settings). Outside the package's own effects:

- Sublime's bytecode cache for the package, expected at
  `~/.cache/sublime-text/Cache/__pycache__/data/Packages/SublimeObserver/` (**inferred** from
  the layout seen for `SFTP` and `Terminal`; written by Sublime, harmless). Optional:
  `command rm -r -- "$HOME/.cache/sublime-text/Cache/__pycache__/data/Packages/SublimeObserver"`
- A `Packages/User/SublimeObserver.sublime-settings`, only if the operator made one by hand.
  The package creates none; this task never touches `User/`.
- Anything a reader already copied out of the runtime directory.

---

## Update rule

When the payload changes, bump the `version:` line above. `run.sh list` then shows
`STALE (have <old>)`; run the install block again (it replaces the five files with fresh
copies and refuses anything foreign), verify, then `run.sh mark sublime-observer`. If the
payload's file set changes, the five names in the check, install and removal blocks change
in the same edit.

`automation` stays `manual` until majkee's GO on the session gate; switching to `auto` then
means an `install:run` block and a version bump.

---

<!-- install:check -->
```bash
# read-only: never starts, queries or signals Sublime
[ -n "${SRC:-}" ] || { echo "src-root not set"; exit 1; }
P="$SRC/SublimeObserver"
if [ ! -d "$P" ] || [ -L "$P" ]; then echo "payload missing: $P"; exit 1; fi
want="$(printf '%s\n' .python-version SublimeObserver.sublime-commands SublimeObserver.sublime-settings contract.py publisher.py)"
have="$(cd "$P" && find . -mindepth 1 -printf '%P\n' | LC_ALL=C sort)"
[ "$have" = "$want" ] || { echo "payload $P must hold exactly the five payload files; found: $(printf '%s' "$have" | tr '\n' ' ')"; exit 1; }
for f in $want; do
  if [ ! -f "$P/$f" ] || [ -L "$P/$f" ]; then echo "payload entry is not a regular file: $P/$f"; exit 1; fi
done
ST=/opt/sublime_text
[ -x "$ST/sublime_text" ] || { echo "Sublime Text not installed at $ST"; exit 1; }
build="$(grep -o -m1 -E 'Build [0-9]+' "$ST/changelog.txt" 2>/dev/null | head -n1 | tr -dc '0-9')"
[ -n "$build" ] || { echo "cannot read the Sublime build from $ST/changelog.txt"; exit 1; }
[ "$build" -ge 4205 ] || { echo "Sublime build $build is below 4205"; exit 1; }
[ -x "$ST/plugin_host-3.14" ] || { echo "no $ST/plugin_host-3.14 (the only plugin host this package is verified on)"; exit 1; }
PK="$HOME/.config/sublime-text/Packages"
[ -d "$PK" ] || { echo "$PK does not exist"; exit 1; }
[ ! -L "$PK/SublimeObserver" ] || { echo "$PK/SublimeObserver is a symlink; this task installs by copy only"; exit 1; }
if [ -e "$PK/SublimeObserver" ]; then
  [ -d "$PK/SublimeObserver" ] || { echo "$PK/SublimeObserver exists and is not a directory"; exit 1; }
  other="$(cd "$PK/SublimeObserver" && find . -mindepth 1 -printf '%P\n' | grep -vxF -f <(printf '%s\n' $want))"
  [ -z "$other" ] || { echo "$PK/SublimeObserver holds entries other than the five payload names: $(printf '%s' "$other" | tr '\n' ' ')"; exit 1; }
fi
echo "prereqs ok (Sublime build $build) — do the install steps by hand"
```
<!-- /install:check -->
