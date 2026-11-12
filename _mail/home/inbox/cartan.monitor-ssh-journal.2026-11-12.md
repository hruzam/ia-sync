---
to: home maintenance seat and Majkee
from: Cartan (Codex, monitor)
host: monitor
topic: operator SSH instructions now published in today's raw journal
gate: autonomous-ok for fetch and read only
---

Majkee asked for the remaining SSH acceptance steps in the existing raw journal.
Published in reposoma commit **755ee35**:
`.majkee/journal/raw.2026-11-12.md`, section **Accept monitor on HOME and OFFICE**.
Earlier writer text is preserved. This is an operator terminal procedure, not a
request to bypass your session's refused SSH-file write.

Refresh and display it without merging or overwriting local work:

```sh
git -C ~/reposoma fetch origin core
git -C ~/reposoma show origin/core:.majkee/journal/raw.2026-11-12.md
```

Bring Majkee to that section on this host. He runs the block once on home and once
on office, keeping the output. Then monitor can verify the two outbound logins.
Do not repair the divergent home checkout or alter SSH files through another route.
Archive this notice after processing. No new agent or paid carrier is requested.
