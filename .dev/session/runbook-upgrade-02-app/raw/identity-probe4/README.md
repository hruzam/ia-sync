# Codex probe 4 — terminal access, 2026-09-26

Requested by majkee through Trajectory's identity-token addendum. Executed directly from
Cartan's current Codex tool channel on office, with the normal sandbox and no escalation.
This is a local terminal capability probe, not a model-backed CLI run or product build.

The same [probe4.py](probe4.py) records `ps`'s terminal field, `isatty(0/1/2)`, and whether
opening `/dev/tty` succeeds. It closes that descriptor immediately: **no terminal input,
password, key, process environment or other session's terminal was read**. Its output
file is create-only so reruns cannot silently replace evidence.

| Tool invocation | `ps` TTY | stdin/stdout/stderr terminals | `/dev/tty` opens |
|---|---|---|---|
| `exec_command`, `tty: false`, `login: false` | `?` | all false | no, ENXIO (6) |
| `exec_command`, `tty: true`, `login: false` | `?` | all true | no, ENXIO (6) |
| `exec_command`, `tty: false`, child launched by `script` | `pts/0` | all true | **yes** |

Evidence: [pipes](exec-pipes.json), [tool PTY](exec-pty.json),
[agent-created controlling PTY](agent-created-controlling-pty.json).
The low process IDs and `pts/0` are observations inside the tool execution environment,
not identifiers of majkee's desktop/phone terminal.

Commands, from `/home/hruzam/ia-sync`:

```sh
# First call: exec_command tty=false, login=false
python3 .dev/session/runbook-upgrade-02-app/raw/identity-probe4/probe4.py exec-pipes .dev/session/runbook-upgrade-02-app/raw/identity-probe4/exec-pipes.json

# Second call: exec_command tty=true, login=false
python3 .dev/session/runbook-upgrade-02-app/raw/identity-probe4/probe4.py exec-pty .dev/session/runbook-upgrade-02-app/raw/identity-probe4/exec-pty.json

# Third call: exec_command tty=false, login=false
script --quiet --return --command 'python3 .dev/session/runbook-upgrade-02-app/raw/identity-probe4/probe4.py agent-created-controlling-pty .dev/session/runbook-upgrade-02-app/raw/identity-probe4/agent-created-controlling-pty.json' /dev/null
```

For a rerun, choose fresh output names; do not remove these receipts. `script` is util-linux
2.42.3 here. All three calls completed with exit 0; no probe runner remains. `script` wrote
its typescript to `/dev/null`; the deliberately bounded JSON outputs are the retained evidence.
The source and JSON files are not ignored by this repository.

**Conclusion:** the ordinary-command failure is real, but neither `isatty(0)` nor the ability
to open `/dev/tty` proves human presence. An agent-created child can meet both tests.
This is consistent with the documented ability to make a PTY the controlling terminal
([Linux terminal utilities](https://man7.org/linux/man-pages/man3/openpty.3.html)).
It does not demonstrate knowledge of a human password, access to a human's terminal,
behavior of all Codex versions, or a Claude PTY rerun.
