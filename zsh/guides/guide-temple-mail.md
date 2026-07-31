# Guide: Temple Mail (send · read · pick)

`~/.config/zsh/guides/guide-temple-mail.md`

---

## Quick reference

| Command | Role | Writes? |
|---|---|---|
| `temple-mail <origin>:<agent> <scope> [body\|-] [--from <o>:<a>]` | Send mail into a seat's inbox | yes |
| `temple-mail-inbox <origin>:<agent>` | List UNREAD inbox + toAll items (presence-only, never cats) | no |
| `temple-mail-switch [--project <origin>]` | Interactive destination picker (fzf + preview) | no |
| `temple-mail-manage [--list\|--archive r/f\|--restore r/f]` | manage read-state (inbox↔archive) | **yes (moves files)** |
| `temple-doorbell-run` | Ring stale projects via mail (canon doorbell) | yes |

All are functions wired by `~/.config/zsh/ai/base.zsh` (the signpost, 0009 L2) — available in
every shell. Source `base.zsh`, never the individual scripts.

---

## Addressing

`<origin>:<agent>` — origin = logical project name, agent = seat name.
The same seat name in two projects never collides: `reposoma:houston` ≠ `piql.dev:houston`.

Origins are defined **only** in the P0 map (`ai/temple-project-map.zsh` — the single home of
physical paths on this host). Current office origins:
`reposoma · subai.devenv · reposoma.devenv · freya.devstudio · piql.dev · vacuole`

Read-state convention: **presence in `inbox/` = unread; moving to `archive/` = read.**
No stamps, no database — the filesystem is the state machine.

---

## Send

```bash
# body from file:
temple-mail reposoma:houston my-scope body.md --from reposoma:oraculum

# body from stdin:
echo "quick note" | temple-mail piql.dev:houston doorbell-stale - --from temple:houston
```

Lands as `<receiver-repo>/_mail/<agent>/inbox/<sender>.<scope>.<YYYY-MM-DD>.md` with
frontmatter (`from/to/scope/date/host`). Receiver owns; no sent-copy; replies return to the
sender's own inbox.

---

## Pick a destination (when you don't remember the address)

```bash
temple-mail-switch                      # all projects on this host
temple-mail-switch --project reposoma   # one project's seats only
```

- Candidate lines are **derived live** from the P0 map + each repo's `_mail/*/` — nothing is
  registered, nothing can rot.
- Cursor on a line → preview pane shows the head of that seat's newest inbox item.
- Enter → prints exactly `origin:agent` to stdout. ESC → exit 1, empty output.
- No fzf on the host → numbered select menu, same output contract.

Compose with send — the intended idiom:

```bash
temple-mail $(temple-mail-switch) <scope> <body-file>
```

---

## Read

```bash
temple-mail-inbox reposoma:houston      # lists unread by presence; quiet when empty
```

Ask-first rule (token economy, `_mail/README.md`): agents list presence, then **ask the
operator before reading content**. This listing interface is what the cross-machine twins bind
to (0010 R-b) — never the file layout.

---

## Manage (mark read / archive)

```bash
temple-mail-manage          # TUI — interactive inbox/archive manager
temple-mail-manage --list   # non-interactive listing (agents)
temple-mail-manage --archive houston/reposoma.oraculum.engine-e-adoption.2026-07-11.md
temple-mail-manage --restore houston/reposoma.oraculum.engine-e-adoption.2026-07-11.md
```

TUI keys: Up/Down move cursor · SPACE mark/unmark · TAB toggle inbox/archive view ·
`a` archive-or-restore all marked · `q` quit.

CLI modes (`--list`, `--archive`, `--restore`) are designed for agent invocation — no
interactive state, exit 0 on success.

This is the decision 0010 read-state transition made executable: moving a file from
`inbox/` to `archive/` is the act of marking it read; the reverse restores it to unread.
No stamps, no database — the filesystem is the state machine.

---

## Deeper

- Live map + temple-family rules: `~/.config/zsh/AGENTS.md` (temple transport family block)
- File map + dev rules: `~/.config/zsh/ai/README.md`
- Canon: reposoma decisions **0008** (transport) · **0009** (ai/ namespace + signpost) ·
  **0010** (cross-machine mail)
- Gemini seats guide (separate surface): `~/.config/zsh/guides/guide-for-user.md`
