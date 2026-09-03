# RUNBOOK — roster-reform-01-triad

```yaml
goal:            The octopus triad (planning-head · working-head · PAD-driver) has exactly one home
                 on the Claude side, mirrored 1:1 in role to its Codex-native siblings, with no
                 duplicated seat left on the Claude table.
gate:            Three re-homings exist on the surgical table — medusa→@Flight, polyp→@Vara,
                 octopus→`/runbook` skill — each cross-checked against its Codex sibling for
                 role-parity-not-file-parity, @Cartan countersigned in `_bus/`, @majkee gaveled
                 in STATUS `checkpoint:`.
participant_0:   [@atlas-ui · head,  {claude, fable, high},  office]   # THIS RUNBOOK's author · status_owner
participant_1:   [@atlas-ui · fold,  {claude, opus,  high},  office]   # session fc.repos-atlas-opus.polyp-medusa
participant_2:   [@majkee, human, office + home]
participant_3:   [@Cartan, {codex, sol, -}, office]                    # countersign only — reads, never edits Claude files
status_owner:    @atlas-ui · head    # single writer of STATUS.md AND of ~/reposoma/pulse.atlas.md — see holds
schema_note:     conforms to ~/reposoma/raw.guides/runbook/GUIDE.md rev 2026-08-27
```

> **Read this once.** Nothing here changes during the session. Position lives in `STATUS.md`.
> Two Atlas incarnations share this gate. Neither started here; both attach here.

---

## Why this session exists

Commit `c0cd75c roster-reform` began trimming the Claude roster. The octopus family (medusa ·
polyp · octopus) crossed to the Codex line as **protocol skills** (`~/ia-sync/codex/skills/`,
Cartan accepted 2026-09-03, `108850d`). Their Claude-side jobs did not vanish — they need homes:

| triad seat | Codex home (done) | Claude home (this gate) | who |
|---|---|---|---|
| working-head (medusa) | `codex/skills/medusa` | folded into `@Flight` | fold |
| PAD-driver (polyp) | `codex/skills/polyp` | folded into `@Vara` | fold |
| planning-head (octopus) | `codex/skills/octopus` | **`/runbook` skill** — did not exist | head |

Two sessions were already running the two halves without a shared frame. This RUNBOOK is the
frame. The keystone (gaveled 2026-09-02): style lives ONCE in the vendor-neutral guides
(`raw.guides/{runbook,status,PAD,bus}`); a Codex polyp and a Claude vara consume the SAME law, so
they cannot drift. Every re-homing here points at those guides; none reproduces them.

---

## prompt-0 — @atlas-ui · head (master seat, this author)

You own `STATUS.md` and `~/reposoma/pulse.atlas.md` for the life of this gate.

**Read, in order:** this file · `STATUS.md` · `~/ia-sync/codex/skills/octopus/SKILL.md` (the
sibling rendering) · `~/ia-sync/codex/skills/codex-harness/references/cross-runtime-roles.md`
§Session operating protocols · the four guides.

**Your work, in order:**

**(a)** Author `~/reposoma/raw.guides/runbook/res/token-economy.md` — the extending chapter
(res/ shape per `~/reposoma/_runbook/README.md`), + ONE pointer line in
`~/reposoma/raw.guides/runbook/GUIDE.md` marked `DRAFT — awaiting majkee gavel`. Source of
truth = `raw.research/capabilities-economy-hygiene.claude.md` + the @field melt (this session).
Corrections already ruled: drop the image-cost claim · move "sequential PAD with remote
operator" to `PAD/raw/` as an observation · add S/E ratio + effort axis · spend record lives in
promoted evidence + one benchmark row, never in RUNBOOK or STATUS.

**(b)** Read the triangulation substrate — **already done by @majkee by hand** (Symmetry ⊥
Asymmetry, two blind rounds); do NOT run another round. Order fixed by @majkee:
1. `~/ia-sync/.dev/session/runbook-upgrade/raw/brief.agent-working-routines.2026-09-02.md`
2. `~/ia-sync/.dev/session/runbook-upgrade/raw/reply.agent-working-routines.field-research.2026-09-02.md`
3. `~/ia-sync/.dev/session/runbook-upgrade/raw/brief-r2.guides-audit.2026-09-03.md`
4. `~/ia-sync/.dev/session/runbook-upgrade/raw/reply-r2.guides-audit.2026-09-03.md`
5. `~/ia-sync/.dev/session/runbook-upgrade/raw/raw.session-routines-and-file-plane.2026-09-03.md`
`brief.*` = Symmetry's master prompts · `reply*` = Asymmetry's answers · `raw.*` = Symmetry's
synthesis. Substrate, not evidence: every claim taken into the skill is verified against the
guides or a dated vendor source.

**(c)** Author `~/ia-sync/claude/skills/runbook/SKILL.md`: the Claude rendering of the
planning-head protocol. Entry: `/buffering-cycle` → smoothed → `/runbook`. The C-shape
(#the-c-shape: intention → substrate/runbook → strong seat maintains → specialist only when
needed) is the process it drives. Same authority edge as Cartan's octopus (author RUNBOOK +
initial STATUS · recommend the seat · PARK · never implement, spawn, or deploy). Attaches to
Houston-family seats by pointer; at most one line in `houston.md`, gaveled.

**(d)** POINT `_bus/NN.head.point.md` to @Cartan for countersign of (c) — role parity vs
`codex/skills/octopus`, not file parity.

**(e)** Receive the fold seat's RETURN, verify on disk (`git diff` — read-only), write VERDICT,
fold its ledger text into `pulse.atlas.md`, rewrite STATUS.

**You may not:** edit `flight.md`, `vara.md`, or anything in the fold seat's scope · run
write-side git, `deploy.sh`, `rm`, `cp` · amend the body of any GUIDE (one pointer line only).

---

## prompt-1 — @atlas-ui · fold (session `fc.repos-atlas-opus.polyp-medusa`)

You were spawned from `~/reposoma/_cold-start/archive/CS.roster-trim-fold.2026-09-02.md` and
have just finished Batch B (operator-executed). **From here you work inside this gate.** Read
this file, then `STATUS.md`, then continue your card's Batch C.

**Your scope (exclusive):** `~/ia-sync/claude/agents/flight.md` · `~/ia-sync/claude/agents/vara.md`
· promotion of `/track-run` onto `~/ia-sync/claude/skills/track-run/` · the Batch B/C
deletions you hand to the operator. Fold WIDE, not temple-locked (card + 09-02 gavel).

**What changed for you:**
- **Do not write `~/reposoma/pulse.atlas.md` while this RUNBOOK is live.** Two live Atlases on a
  single-writer file is the exact collision the STATUS guide names. Put the ledger text you
  would have written into your RETURN (below); the head seat folds it in verbatim.
- **Point, don't build, the planning-head.** Where Flight (as working-head) needs to say "the
  RUNBOOK you work inside is authored by the planning head", the pointer is **`/runbook`** —
  the name is fixed here so your fold and the head's skill meet. Do not describe how RUNBOOKs
  are built inside `flight.md`; the guide and the skill own that.
- **Do not touch** `houston.md`, `oraculum.md`, `skills/runbook/`, `raw.guides/runbook/`.

**When your Batch C is authored on the table:** write `_bus/NN.fold.return.md` — six fields per
the BUS guide, plus a seventh block `## pulse-ledger text` = the OPEN LEDGER line + dated entry
you want in `pulse.atlas.md`, verbatim. Then stop; the head verifies and writes VERDICT. If you
discover a hold, mail it: `~/reposoma/_mail/atlas/inbox/atlas-fold.<topic>.<date>.md` — the
head reads its inbox at every saddle.

**If the head session dies first** (STATUS `updated:` older than your own last turn by a full
day and @majkee confirms): ownership transfers to you — rewrite STATUS as the new
`status_owner`, one verified transition, and you inherit the pulse pen. Never assume it.

---

## prompt-2 — @majkee (human seat — hands and gavel)

- **Hands:** execute Batch B/C deletions, `cp` deposits, commits, `deploy.sh` — no Atlas seat
  runs those. Release @Delta for the surgical cuts the head briefs (octopus-pilot orphan first).
- **Gavel:** the `/runbook` skill body before it lands on the table · the economy chapter
  pointer line (against the runbook-upgrade brake — see holds) · the fold shape of Flight/Vara
  · session close.
- **Transport:** `.dev/session/` travels with `~/ia-sync` git; home sees this RUNBOOK after
  `git pull`. No tailscale hand-carry.

---

## prompt-3 — @Cartan (countersign seat)

You read `_bus/NN.head.point.md` when it exists. Verify **role parity, not file parity**
(`codex-harness/references/cross-runtime-roles.md` §Shared invariants): does `/runbook` keep the
same purpose · trigger · authority boundary · output kind · park envelope as your `octopus`
skill, expressed Claude-natively? Return `_bus/NN.cartan.return.md`, six fields. You do not edit
any Claude file. If you find the economy chapter changes what `octopus` should bond to when it
authors a RUNBOOK, say so in field 4 (mismatches) — that is the head's mail to you, pre-empted.

---

## Known constraints and destructive holds

Fixed at authoring time. Discovered mid-session → `STATUS.md` `holds:`.

- **`status_owner` = head, and the same seat holds the pen on `~/reposoma/pulse.atlas.md`.**
  The fold seat delivers ledger text via RETURN. *Cause: two live incarnations of one seat on
  one single-writer file; no lock exists; the ledger is the temple's memory of this work.*
- **Disjoint file scopes** (above). A seat that must cross the line mails the head instead of
  editing. Neither Atlas edits `houston.md` beyond one gaveled pointer line.
- **No Atlas runs write-side git, `deploy.sh`, `rm`, `cp`, `push`, `ssh`.** Operator or an
  executor (@Delta) only. Everything authored here is STAGED until @majkee deploys.
- **Nothing duplicated against `~/ia-sync/codex/skills/{medusa,polyp,octopus}`.** A Claude
  seat re-homed here must not become a copy of the Codex rendering — role parity via the shared
  guides, native expression per runtime (Cartan's acceptance mail, 2026-09-03).
- **runbook-upgrade brake.** The sibling session `~/ia-sync/.dev/session/runbook-upgrade/`
  holds *no guide amended before the cold-resume probe is measured*. The economy chapter is a
  `res/` addition + one pointer line, orthogonal to what that probe measures. If @majkee rules
  the pointer line breaches the brake, the chapter waits unlinked in `res/` until the probe
  closes. The GUIDE body is not amended by anyone in this session.
- **1:1 folder mirroring** is assumed by every absolute path here (the unstated law named in
  `runbook-upgrade/raw/raw.session-routines-and-file-plane.2026-09-03.md` §#mirroring). A path
  that resolves on one host and not the other is a finding — record it, do not patch it.
- **Symmetry/Asymmetry are not seats.** They are @majkee's chatbots (claude.ai · chatgpt.com),
  reached by hand. Their two blind rounds are DONE and live in `runbook-upgrade/raw/` — raw
  substrate, never evidence. No seat opens a third round inside this gate.
- **Closing sweep is part of closure, not a new gate.** Every orphan or contradiction surfaced
  by this work — scripts AND artifacts — is adjudicated before prune: fixed by an executor
  (@Delta) under @majkee's release, or logged as a finding into `runbook-upgrade`'s evidence.
  Known at authoring: `raw.research/octopus-pilot/` (Claude-skill orphan; rows harvested first)
  · `/program-pulse` (probable lingerer post-crossing) · header≠folder naming
  (`<program>-<NN>-<phase>` law vs slug-named folders — a GUIDE finding, not a fix here) · the
  `_runbook/<project>/<slug>` zsh opener needing a `.dev/session/<slug>` shape (parked by
  @majkee; sweep if time).
- **No router file in `~/ia-sync`** (no `pulse.md`, no `flag.md` — verified 2026-09-03). This
  session is routed from `~/reposoma/pulse.atlas.md` OPEN LEDGER instead (temple exception);
  one line, slug + STATUS path. Not a second authority.

---

## references

Point, do not copy.

- `~/reposoma/raw.guides/{runbook,status,PAD,bus}/GUIDE.md` — the law both runtimes consume
- `~/reposoma/_runbook/README.md` — bench shape; `raw/` = substrate, `res/` = extending chapters
- `~/reposoma/_cold-start/archive/CS.roster-trim-fold.2026-09-02.md` — the fold seat's card
- `~/reposoma/_mail/atlas/inbox/cartan.medusa-polyp-seat-transfer-accepted.2026-09-03.md` — hold released
- `~/reposoma/_mail/oraculum/inbox/oraculum-termbrana.runbook-guide-economy-extension.2026-09-02.md` — economy proposal (re-routed to head)
- `~/reposoma/raw.research/capabilities-economy-hygiene.claude.md` — B+E+P+S, measured runs
- `~/ia-sync/codex/skills/{octopus,medusa,polyp}/SKILL.md` — the Codex renderings (what NOT to duplicate)
- `~/ia-sync/codex/skills/codex-harness/references/cross-runtime-roles.md` — parity contract
- `~/ia-sync/.dev/session/runbook-upgrade/` — the sibling program; its `raw/` holds the two blind rounds
- `~/reposoma/pulse.atlas.md` — OPEN LEDGER "Octopus family" line (Batch A–D history)

---

## What closes this gate

`STATUS.md checkpoint:` points at three things on disk: the folded `flight.md` + `vara.md`
(fold RETURN verified by VERDICT), `skills/runbook/SKILL.md` (Cartan RETURN in `_bus/`, majkee
gavel recorded), and `raw.guides/runbook/res/token-economy.md` (gavel recorded). Deploy is
**not** part of the gate — it is the operator's step after closure.

On closure: fold both seats' ledger text into `pulse.atlas.md` (tick the Octopus-family line's
Batch C item); promote the Cartan RETURN to `~/reposoma/_mail/cartan/archive/` (operator mv);
remove this session's line from the OPEN LEDGER; prune the directory. `raw/` (brief + two
replies) is promoted to `~/reposoma/raw.guides/runbook/raw/` only if the skill cites it —
otherwise it dies with the session.

---

## What this session deliberately does not do

- **No Batch D.** Advisor-ladder collapse, freya ledger Gen-1→Gen-2, taskexpert reader,
  normalization arc — separate gates, separate siblings (`roster-reform-02-…`) if ever.
- **No GUIDE body amendment.** The runbook-upgrade brake holds. Contradictions found (naming,
  `raw/`-vs-`res/` law) are logged for that program, not fixed here.
- **No program-level file** above the siblings (#open-program-level stays parked).
- **No cold-resume probe.** That is `runbook-upgrade`'s gate; this session must not pre-empt
  its measurement by "fixing" what it would measure.
