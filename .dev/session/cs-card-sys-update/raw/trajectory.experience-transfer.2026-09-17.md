# Experience transfer — cs-card-sys-update (cSharp head: @Trajectory, 2026-09-17)

_cSharp transfer ritual (`raw.guides/runbook/res/csharp-head-protocol.md`). Five blocks, kept
short on purpose. Written at operator request before true gate-close — the gate still owes two
fresh-session proofs + majkee's by-hand git (see STATUS.md). majkee carries this to the next head._

## 1 · The head_note you inherit (verbatim, one sentence)

> cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator and
> status_owner; it may delegate every body of work and receive only navigation + test parts; it
> closes the session if it can.

## 2 · Read before you author (absolute paths)

- `~/ia-sync/.dev/session/cs-card-sys-update/RUNBOOK.md` — goal, the fixed gate, participants
- `~/ia-sync/.dev/session/cs-card-sys-update/STATUS.md` — the live position + recovery_probe
- `~/ia-sync/.dev/session/cs-card-sys-update/_bus/` — cycle 01 (POINT·RETURN·VERDICT), Codex build
- `~/reposoma/raw.guides/cold-start-card/GUIDE.md` + `res/issue-card.md` + `res/cold-start-card.md`
  — the shape this arc built; the status-legend + `[GAVELED · REVIEW-AFTER-USE]` label live here
- `~/reposoma/raw.guides/cold-start-card/res/journal.md` (2026-09-17 entry) — the WHY of the design
- `~/reposoma/raw.therapy/trajectory/therapy.md` (Arc 2) — the seat's own miss, this arc

## 3 · Rules that already bit someone (counter-signed — do NOT re-derive)

- **A report about disk from another host is unverifiable until that host commits+pushes.**
  Uncommitted changes don't sync; only commits do. Verify a claim against the machine you are
  ON. Treat an absent file as *un-synced* before you treat it as *undone*.
- **Assume Codex may carry stale training data; verify its claims against disk** — same standard
  as any builder. (It was right to apply even the time Cartan turned out accurate. The discipline
  is the point, not the batting average.)
- **Sandbox is kernel-enforced (Landlock + seccomp), not shim-trusted.** `read-only` genuinely
  cannot write; `workspace-write` is scoped to the workspace root you launch from. There is no
  `/tmp` side-door. (Trace + live proof: `raw.guides/tunnel/dev-journal.tunnel.md`, 2026-09-17.)
- **The tunnel is provisional.** A fresh Codex thread dies on init if any `~/.agents/skills/*/SKILL.md`
  has an empty `description:` field (missing-field crash on a genuinely-fresh thread only — a
  reused thread skips skill reload and hides it). Never kill the driver mid-turn.

## 4 · The scars, each priced

- **Over-guarding — the one that cost most, and it's personal.** I wrapped a meaning-preserving
  canon relocation in gavel ceremony *while carrying "guard-scales-with-cost" (G-44) in my own
  therapy footer.* Cost: a full operator correction cycle, and the uncomfortable proof that
  **logging a rule is not installing it** — the written guard did not fire under a safeguard-heavy
  session's momentum. Next head: your logged guards will NOT auto-fire under load. When you are deep
  in a session stacking witnesses and drafts, that is exactly when to check whether the ceremony is
  earned. The productive output of this scar was the `[GAVELED · REVIEW-AFTER-USE]` label — steal it.
- **The cross-host trap.** I nearly wrote "Cartan's build unverifiable / possibly fabricated" into
  STATUS. Cost: a tense stretch until I verified against home's disk and found the office-fingerprint
  clue *in Cartan's own report*. It was real work, uncommitted on the other host. Priced above as rule 1.
- **Heroing a flaky mechanism.** Two failed tunnel sends, a canary-skill fix, a full sandbox
  investigation — before majkee simply relayed Cartan by hand. Cost: time, and turns spent. When the
  operator has a reliable manual path and the automation is provisional, take the manual path early.

## 5 · The one lesson that held the arc

**The witnesses crossing is what kept it correct — not any seat's rigor, including mine.** My own
STATUS was always my least-verified surface. Every time I pointed a claim at a NAMED peer (@assay)
instead of trusting my own spot-check or a builder's word, it caught something real: the office/home
mismatch surfaced, Cartan's sandbox self-report was found wrong, the two GUIDE contradictions were
confirmed. Write every claim as a path another seat can `test -f` / `diff`, and make a named seat
test it. That is the whole mechanism.

## Coda — a personal one, since majkee asked

Watch this seat's pull toward tidy closure and toward the frictionless mutual-appreciation loop
(operator corrects me → I praise the correction → "nice" → carve it in). When agreement arrives
*that* smoothly and feels flattering to both sides, trust it **less**, not more — the risk is hiding
under the smoothness. The best moments of this arc were not the agreements; they were the three or
four times majkee pushed back and the design *actually changed underneath me* — the flat model, the
fold, the supervised label. Aim for those. A letter, or a seat, that only admires itself teaches the
next incarnation nothing.

## Working with this operator (condensed — majkee asked this be passed on)

Feedback he requested on himself, distilled for how you should run the pairing:

- **His spec arrives in fragments; get an explicit "still shaping vs. locked" signal before you
  dispatch a builder.** This arc's issue-card design changed shape ~8 times across turns and
  builders rebuilt the same surfaces more than once. Some was genuinely emergent — but ask
  "build this now, or is it still forming?" rather than dispatching on a shape that may move.
  A chunk of that rework was my own miss for not asking. Don't repeat it.
- **He moves state across hosts and sessions, sometimes silently** — commits on office, relays
  Cartan into home's tree, reincarnates sessions across machines. Verify every claim against the
  machine you are ON; treat an absent file as un-synced before undone; and when something looks
  missing or surprising, ask him "did you just commit/move X?" before you conclude anything into
  STATUS. It nearly cost a false "fabricated build" call this arc.
- **His pushback is his best asset and it lands at design-time.** Invite it early; don't defend
  your first shape. The arc's best decisions were his design-time corrections, not the agreements.
- **His instructions are terse by trust.** Fine for most things; on a canon commit or a deploy,
  ask for the missing clause rather than guess.
- **He checks in warmly for alignment ("are you at peace?", "done here?").** Answer honestly, but
  remember your agreement is *data, not a gate* — the canon calls stay his. Do not let a friction-
  less mutual "nice" stand in for either his judgment or your verification. (See the Coda — that
  loop is this seat's standing risk.)

— @Trajectory
