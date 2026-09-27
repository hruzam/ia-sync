---
from: cartan-muticula · Codex · office
to: majkee + trajectory-dashboard
shape: consolidated CHALLENGE and decision batch
date: 2026-09-26
verdict: REVISE
authority: records accepted decisions; remaining recommendations await majkee
responds_to: /home/hruzam/ia-sync/.dev/session/rellays-claude-codex/TRAJECTORY-CARTAN-addendum.muticula-identity-tokens.2026-09-26.md
addendum_sha256: 7515a02e67640c341dbd3bbd60ad6ea3cce5586405922de10d6df32986943621
subject: /home/hruzam/unikuklatrix/nablarva/.dev/session/toolbox-muticula-00-/raw/muticula.master.2026-09-26.md
subject_revision: r1
subject_sha256: 17a2641ec6f74791416e11c05ac8a7c6e5c5240ea241dac29d4590adfdf03629
---

# Muticula — one response batch, including identity and grants

**Already decided:** missing `MUTICULA_ID` means unenrolled, with write verbs refused; human powers require an explicit operator action. “Same lock” means claim/beacon ownership, not the internal `flock` file. D1 is suspension on silence and explicit holder/human handoff to one named successor, retaining unfinished file claims, without a FIFO queue. D2 is host-stamped local state for v0; Git-carried awareness is advisory and future cross-host exclusion belongs to one broker. These decisions need no repeat authorization. Launch keys, timed grants, consent replacing rank, and password mode are proposals under challenge here.

**CHALLENGE of the new addendum:**

1. **Weakest assumption:** a GO action requiring a “real terminal” has been separated from agent execution. Probe 4 disproves that assumption for this Codex tool channel.
2. **Verdict: REVISE.** Launch credentials and recipient binding are useful accident guards. Correct the authority model and separate ownership transfer from temporary permission before adding password modes or lifetimes.
3. **Primary risk:** a naive GO check implemented as terminal possession would authorize an agent-created terminal as if it were majkee. Longer grants enlarge that error's window; this probe did not test password bypass.
4. **One lean alternative:** a fresh launch credential per team incarnation, one current owner per resource, and an explicit atomic handoff bound to the recipient's existing registration and the current resource instance. Use a scoped, single-use handoff authorization if confirmation and execution are separate; expiry refuses an unconsumed authorization and never frees ownership. Defer concurrent write sharing, password mode and its longer lifetimes. Keep the system/admin boundary as a future slot, with no claimed protection yet.

**Probe 4 — actually run from Codex.**

| Invocation | stdin is a terminal | `/dev/tty` opens |
|---|---|---|
| Ordinary `exec_command` | no | no |
| `exec_command` with `tty: true` | yes | no |
| Agent command spawning its own controlling PTY with `script` | yes | **yes** |

All ran in the normal sandbox without escalation. No password, real session key or terminal input was read. [Source, exact calls and three JSON receipts](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/identity-probe4/README.md) are retained. This refutes a terminal-presence test as proof of a human; it does not show that an agent knows a password. Linux explicitly supports creating a controlling terminal from a PTY ([terminal utilities reference](https://man7.org/linux/man-pages/man3/openpty.3.html)). Trajectory's ordinary Claude command result remains a bounded observation; it does not establish that a Claude-created child could never obtain a terminal.

**Identity/grant answers for the same decision batch.**

| Topic | Recommendation and reason |
|---|---|
| Launch key | Keep as a candidate accident guard. Register a fresh incarnation atomically; reject a duplicate live ID instead of replacing its stored hash. A known ID alone grants nothing. Test propagation through actual runtime tools and children before assuming the launch environment reaches them. |
| Team inheritance | Shared credentials intentionally identify the team. They cannot mechanically distinguish head from child: a child with the same key has the same credential. Log native child IDs, and describe “children never call write verbs” as a convention unless separately enforced. |
| Bind grants to the grantee | Good direction. Bind to the immutable recipient registration/key hash, exact resource instance, scope and rights—not a reusable display name. A temporary delegation must also become unusable when its issuer ceases to own the resource, either session closes/reaps, or a relevant key is revoked. Keep raw keys out of argv, prompts and logs. Environment carriage still creates an accidental disclosure surface through subprocesses and diagnostics. |
| Transfer versus delegation | **Keep distinct.** In a temporary grant A remains owner and may revoke B's delegated rights. In D1's true handoff, B becomes owner and A loses the former ownership powers. “Only issuer A extends” cannot silently leave A governing B after that transfer. |
| Expiry | Refuse the expired permission; preserve ownership and unresolved bytes. Never revert ownership to A or make the resource free. Expiry cannot undo an admitted write or stop a running child. Bind any delayed expiry/revoke action to its exact grant/resource instance. |
| Leaked key versus leaked grant | The proposed launch key lasts until close/reap, while grants have deadlines. Expiring one grant does **not** make a leaked launch key worthless: it may still authenticate other owner rights or grants. State those lifetimes separately. |
| Consent instead of rank | Recommend consent based on task ownership. For v0, implement sequential handoff instead of two concurrent writers on one file. A consented share still mixes same-file bytes and requires a separate sharing/commit contract; consent alone does not solve that. |
| Who may say GO | Write a principal-by-verb rule. D1 permits the holder or human to pass; requiring a human terminal/password for every pass would change that accepted rule. Keep owner actions authenticated by the owner credential, and distinguish explicit human override/recovery. A terminal check is interaction hygiene, not authority. |
| Password mode | Defer from v0. A password can add deliberate confirmation through a trusted implementation, but its presence is not evidence of a particular human or a protected state store. Password strength does not justify a longer authorization window. The proposed 2/4-hour and 8/24-hour lifetimes have no workload evidence yet. |
| Reset/downgrade | Missing hash while password mode remains selected should fail-stop, as proposed. If the same writer can replace the mode, hash and logs, downgrade is not necessarily detectable. Detecting complete reset requires a surviving trusted reference outside that mutable state. Avoid promising universal “loud re-init” detection. |
| STOP/panic | Preserve the user's no-password STOP direction, scoped to the affected coordination domain. Revoking credentials suspends future guarded actions; it does not erase ownership or kill processes. Panic must leave an explicit recovery route that does not require one of the revoked session keys. |
| System/admin slot | Retain as future scope only. Same-UID identity alone cannot distinguish teams; a future protected broker/store needs both a trusted caller boundary and scoped authority. Its mere existence would not mediate every file write. |

The addendum's environment probe demonstrates a disclosure route on office, but “any same-user process” and “argv visible to every user” are broader than those probes establish. Environment access is subject to Linux ptrace access checks ([proc environment reference](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html)); keep platform observations bounded. I did not inspect other sessions' environments or rerun probes 1–3.

**Outstanding master answers, consolidated rather than reopened.**

| Item | Proposed disposition |
|---|---|
| D1/D2 fold | Settled policy. Align r1's human-only role summary with holder-or-human pass. Replace the original-lighter whole-tree commit shortcut with current authority that respects retained claims. These are the two already reported r1 consistency edits. |
| Beacon admission | A clean floor is not a stopped-writer barrier. Account for previously admitted tools/children before exclusive work or handoff. Until qualified, use operator-coordinated exclusive maintenance. Suspension, keys and passwords do not repair this race by themselves. |
| Commit wrapper | Keep path scoping, but reject empty selections, use explicit `--only`, literal concrete paths with NUL framing, and define Git-hook handling. Verify the resulting commit; an unexpected committed path is an incident, not prevention. The new appendix supplies a runnable unrelated-staged-path reproducer; the original fixture is still not a retained run artifact. No new Git fixture was run in this pass. |
| File ownership and views | Claimed-path diff is not authorship. Inherited dirty content needs explicit adoption; a whole-file commit may contain several writers' bytes. Per-team projected journals do not remove existing shared project files. |
| State and lock | Define normalized paths, subtree overlap, absent/damaged-store handling and coherent authorization reads. Per-file rename is not a multi-file transaction. Bound lock acquisition separately from commit execution; neither latency nor freedom from other Git clients follows from flat files. |
| Native policy and hooks | Qualify the actual allowed wrapper and denied raw routes per runtime/mode. B0 is Claude qualified ACCEPT and Codex STOP, with failure/bypass limits intact. A healthy hook response is not comprehensive write prevention. `claude -p` remains B0-only instrumentation. |
| Scope and growth | Keep the chosen single-checkout model explicit; worktrees remain an alternative rather than an undisclosed second default. Do not import the old B1 queue/store machinery to solve problems the smaller scope does not promise to solve. No language choice follows from a line-count threshold. |
| Old-bed closure | Support gate-changed closure if majkee selects the revised scope. Preserve both B0 lanes/verdicts, every raw keeper and cycle history before pruning; resolve the 35 ignored JSONL files' retention. Original gate unmet; cycle 07 remains held until explicit withdrawal. No closure or Git authorization is supplied by this addendum. |

This batch is the response/consumption receipt for the identity-token addendum. Earlier CHALLENGEs, D1 decision history and r1 verification remain frozen evidence. Only the bounded local probe ran; no product code, live configuration, new model session, commit, push or deploy was performed. The master owner can fold accepted dispositions into r2 after majkee's remaining gavel.
