# commands

RB ENGINE — runbook session browser (shell layer)

```
rb-open [-R] [root]   Launch TUI (-R: tree column on the right)
rb-pick [root]        fzf picker — prints selected bed path
rb-board               Render presence board (* = own attachments)
rb-mark [bed] [note...]   Attach this session to the board
rb-unmark [bed|id]        Detach own record(s) (no arg = all own)
rb-help                This CLI help panel
rb-selftest             Sandboxed selftest, zero side effects
```

## Root resolution (in order)

1. explicit argument (any `.dev/session/` tree)
2. `$RB_ROOT` — default bench, set in `config.<machine>.zsh`
3. walk-up from `$PWD` (stops at a `session/` dir whose parent is `.dev`)

## Inside the TUI

Press `?` for the named-scope help navigator. Its scope list is discovered from
`session/help/*/HELP.md`, so new help folders appear automatically. `Ctrl+F`
searches the open scope; uppercase `F` searches every scope.
`rb-help` (this panel) still covers the CLI surface for anyone who runs it
before ever opening the TUI.
