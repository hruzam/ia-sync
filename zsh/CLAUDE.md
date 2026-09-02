# ~/.config/zsh — machine-layer hive (office)

@AGENTS.md

## What this place is
Operator's personal zsh config on host `office` (`$MACHINE_NAME`). NOT a temple project — no
project-flow, no phases; quick surgical sessions. NOT a git repo on office: every edit is live
at the next shell, and nothing travels by itself (cross-machine = ia-sync deploy; the home seat holds
the home side, the office seat holds the office side).

## Direct-work rules (this folder)
1. The imported AGENTS.md above is the live map — trust disk + map over memory; if you move or
   add files, update the map in the same session.
2. **Temple family is GATED:** `ai/temple-*.zsh`, `ai/temple-*.hook`, `ai/base.zsh` (signpost),
   `ai/adr-guard.*` — no edits without a temple gate (decision 0009; `ai/README.md` dev rule 1).
   Draft + mail the temple instead.
3. **Control-panel convention** (section above): keyboard = the one interactive surface —
   aliases only, bodies in scope engines behind it (LAW: `guides/guide-for-builder.md`
   §Architecture rules). No aliases inside engines.
4. **Verify-real-trigger (0009 L5):** anything with a systemd/hook/cron trigger counts as done
   only when the trigger fires and produces output — never by hand-run alone
   (`ai/doorbell-smoke.zsh` is the standing instrument).
5. `.env/` = secrets. Never read, print, or copy contents.
6. **Guides are the operator's memory:** any user-facing change lands or extends a guide in
   `guides/`. Machine surface keeps factory-standard naming; metaphor stays in the culture layer.
   Index + writer convention: guides/index.md.

## Where things are decided
- Canon, decisions, mail, seats: the temple → `/home/hruzam/reposoma` (route by seat via its
  AGENTS.md). Send mail from here with `temple-mail <origin>:<agent> <scope> …`
  (guide: `guides/guide-temple-mail.md`; picker: `temple-mail-switch`).
- A change here that needs a decision: draft it, mail `reposoma:houston` — do NOT lock from
  this seat.
