# Tools — JSONL reader

Shell layout follows `zsh/AGENTS.md`'s control-panel convention: `base.zsh` loads
the engine and the aliases-only `keyboard.zsh`. Python uses only the standard library.

## A small reading session

After the tools scope is installed and loaded:

```zsh
tools-help                               # compact navigation panel
tools-browse ~/projects/my-project       # interactive file and record browser
tools-jsonl load /path/to/records.jsonl   # first 12 numbered previews
tools-jsonl list --start 13 --limit 12   # another sip
tools-jsonl pick 2,5-7                   # mark these physical lines; create Markdown
tools-jsonl list                        # [x] marks the selection
tools-jsonl open                        # open Markdown with subl, or print its path
tools-jsonl path                        # print the temporary Markdown path
tools-jsonl save ~/chosen-excerpts.md   # explicitly retain; refuses an existing path
tools-jsonl refresh                     # reread source, discard selection and old Markdown
tools-jsonl clear                       # delete cached snapshot and Markdown
```

In `tools-browse`, use arrows and Enter to navigate folders and open a JSONL file,
Space to mark records, and `p` to create the Markdown view. `b` returns to files,
Backspace goes to the parent folder, and `q` quits. The generated view starts with a
record index, explanation of physical lines and JSON Pointers, and `grep`/`cat`
examples for the source. Only explicitly selected records are included.

For Jev records, run `jev-browse` instead. Choose a session with arrows and Enter;
press `m` to toggle authored memory notes versus all events, Space to mark events,
`a` to mark all visible events, and `p` to compose a private Markdown view. The
printed path can be opened with `subl`. Marked events stay selected when the filter
changes. The view is generated through Jev's native locked replay; model replies,
explicit memory notes and dispositions remain distinct events. If no memory notes
exist, toggle back to all events to browse requests and replies. `b` returns to
sessions and `q` quits. `--root /path/to/vault` selects another existing Jev vault.

`pick` replaces the previous selection and view. Arrays and objects are expanded into
fields with JSON Pointer paths (`/questions/0/text`, `/a~1b` for key `a/b`), original
types and literal text blocks. UTF-8 prose and line breaks remain readable. Control and
bidirectional formatting characters become visible escapes. Source markup and commands
stay in literal blocks. The reader does not summarize or execute record content.

Line numbers mean physical JSONL lines, including blank or malformed lines. Invalid lines
are reported in the preview and Markdown with diagnostics; they are never repaired.
The generic reader does not validate a domain ledger or establish causal order.

## Temporary means disposable

The tool keeps one loaded snapshot at a time. It lives in a private `tools-jsonl/`
directory under the user's runtime directory (`$XDG_RUNTIME_DIR` or `/run/user/$UID`).
Linux `/dev/shm/tools-jsonl-$UID/` is the volatile fallback. These locations are cleared
on reboot; the runtime directory may also disappear on logout. Files have mode 0600,
directories 0700. `clear` removes this reader's two files immediately; saved exports remain.

Reading uses the frozen snapshot until `refresh` or another `load`. Markdown identifies
the source path, byte hash, renderer version, load/generation times and selected lines.
Changing the source does not silently alter the selected snapshot. Temporary output is a
derived reading view, never a fresh model reply or an automatic memory injection.

`--cache-dir /private/temp/path` is available for isolated tests or an explicitly chosen
temporary location. Its lifetime follows that location, so arbitrary overrides are not
guaranteed to disappear on reboot. The source cannot live inside the disposable cache.

## Jev records

Direct Jev event JSONL is refused: native replay must validate its history, locking,
incomplete tails and recovery state before rendering. Use the separate validated Jev
reader provided by the integration, or Jev's native `show` command. Do not convert a
ledger to generic JSONL to bypass validation. Ordinary JSONL is supported here; this
module alone does not claim the Jev handoff's full native audit acceptance.
An existing `audit.md` is already Markdown: open it directly, rather than loading it
into `tools-jsonl`. A view made with `--request` covers that request's events; omit
the option when you want all events in the selected Jev session.

For a Jev session, create a private disposable directory first, then use the native
reader (replace the session and optional request IDs):

```zsh
jev_view_dir=$(mktemp -d "${XDG_RUNTIME_DIR:-/run/user/$UID}/jev-view.XXXXXXXX")
python3 -B ~/.config/zsh/jev/reader.py --session SESSION_ID --request REQUEST_ID \
  --output "$jev_view_dir/view.md"
subl "$jev_view_dir/view.md"            # or open the printed path yourself
```

The directory is private and disappears with the runtime directory. To clear it sooner,
delete `view.md` and the now-empty directory. Each output must be a new file in an
owned 0700 directory. The reader replays and validates Jev's ledger; it does not send
requests or change the saved events. Its Markdown is a derived view, not a fresh reply.

## From the surgical table

```zsh
source /home/hruzam/ia-sync/zsh/tools/base.zsh
tools-jsonl --help
```

Equivalent non-shell invocation: `python3 -B zsh/tools/jsonl_reader.py --help`.
Shell startup only defines commands; it reads no data and creates no cache.
Sublime is optional and opens only upon `open`. `save` never overwrites existing files.

Verification: `python3 -B -m unittest discover -s zsh/tools -p 'test_jsonl_reader.py'`.
