# board

Presence board — advisory only. A record informs other sessions that a
bed is attached somewhere; it never authorizes or blocks anything.

## Shell

```
rb-mark [bed] [note...]   attach this session to a bed (exclusive-create)
rb-unmark [bed|id]        detach own record(s) — no arg = all own
rb-board                  render all records; * marks your own
```

## In the TUI

```
m   attach the selected bed (writes one presence record, owned by you)
u   detach your own record(s) for the selected bed
B   open the board modal — Enter lands on a local-host record's bed
```

`●` before a bed's name in the tree = attached on the board right now
(any seat, any host). Board state is recomputed live on the 1s tick.

Full contract (record grammar, ownership rules, staleness policy):
`~/reposoma/raw.guides/runbook/res/presence-board.md`
