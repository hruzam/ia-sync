#!/usr/bin/env zsh
_tools_jsonl() {
  command python3 -B "${_TOOLS_SOURCE_DIR}/jsonl_reader.py" "$@"
}

_tools_browse() {
  command python3 -B "${_TOOLS_SOURCE_DIR}/jsonl_browser.py" "$@"
}

_tools_jev_browse() {
  command python3 -B "${_TOOLS_SOURCE_DIR:h}/jev/browser.py" "$@"
}

_tools_help() {
  cat <<'EOF'
TOOLS — JSONL reader and Jev views

  tools-help                         this navigation panel
  tool-help                          same panel
  tools-browse [PROJECT-DIRECTORY]   browse folders and select JSONL records
  jev-browse                         browse Jev sessions, select events and compose

  Ordinary JSONL: one JSON value per line
  tools-jsonl load FILE               load a private snapshot and preview
  tools-jsonl list --start 13        browse the next records
  tools-jsonl pick 2,5-7             select lines and make a Markdown view
  tools-jsonl open                    open that view in Sublime or show its path
  tools-jsonl path                    show the current view's path
  tools-jsonl save ~/chosen.md        keep a copy; never overwrite
  tools-jsonl refresh                 reread the source and clear the selection
  tools-jsonl clear                   discard this reader's temporary files

  Jev browser: Enter opens a session; m filters memory notes; Space marks events;
  a marks visible events; p composes Markdown; b goes back; q quits.
  Jev: open an existing audit.md directly in Sublime; it is already Markdown.
  Jev ledgers require their validated reader, not tools-jsonl. For a new view:
  jev_view_dir=$(mktemp -d "${XDG_RUNTIME_DIR:-/run/user/$UID}/jev-view.XXXXXXXX")
  python3 -B ~/.config/zsh/jev/reader.py --session SESSION_ID --request REQUEST_ID \
    --output "$jev_view_dir/view.md"
  subl "$jev_view_dir/view.md"

  A view is disposable and local; omit --request to include all session events.
  Detailed guide: ~/.config/zsh/tools/README.md
EOF
}
