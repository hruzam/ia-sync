# Guide: Harness Check — AI settings-card freshness

`~/.config/zsh/guides/guide-harness-check.md · audience: operator · machine: office · verified: 2026-07-11`
`replaces guides/ai.md (retired 2026-07-11): §1 kept here · token-hygiene → guide-for-user.md §Hygiene · ai/ layout → AGENTS.md + ai/README.md (point, never copy)`

---

## What it is

`ai/harness-check.zsh` keeps machine-level knowledge cards fresh. It parses the YAML
frontmatter of settings cards (`raw.card.*.md`), computes time elapsed since `verified:`,
and flags any card past its `half_life_days:`. Stale cards produce a mail file in the
temple's `toAll` inbox — volatile AI facts never rot silently.

---

## Registry config

**Path:** `~/.config/zsh/registries/ai.json`

```json
{
  "native-primitives-update-pattern": "~/reposoma/raw.settings/raw.card.*.md",
  "mail-inbox-dir": "~/reposoma/_mail/toAll/inbox/"
}
```

- `native-primitives-update-pattern` — glob of cards to check (`~/` keeps it per-machine portable).
- `mail-inbox-dir` — where background stale alerts land.

---

## Interactive check: `harness-stale`

Wired by `ai/base.zsh` (no `.zshrc` edit needed — the signpost carries the alias):

```bash
harness-stale        # = harness-check.zsh --debug
```

Output: one line per card — `FRESH` / `STALE`, verified date, elapsed vs. limit, and the
would-be mail path if anything is stale.

---

## Scheduled run (systemd, weekly)

| Unit | Path | Schedule | Role |
|---|---|---|---|
| `harness.timer` | `~/.config/systemd/user/harness.timer` | Mon 09:00, `Persistent=true` | fires weekly; catches up after downtime |
| `harness.service` | `~/.config/systemd/user/harness.service` | oneshot | runs `ai/harness-check.zsh`; writes toAll mail if stale |

Management:

```bash
systemctl --user list-timers --all          # status + next run
systemctl --user start harness.service     # trigger now (this IS the L5-valid test)
journalctl --user -u harness.service       # execution history
```

---

## When a card goes stale — the action loop

1. Open the alert: `~/reposoma/_mail/toAll/inbox/zsh.stale-settings-cards-<date>.md`.
2. Run the card's **verification command** (e.g. `gemini --version`) and/or visit its recheck links.
3. Confirm whether anything actually changed (versions, flags, breaking changes).
4. Edit the card's frontmatter: set `verified:` to today.
5. `harness-stale` → confirm `FRESH`.

---

## Cautionary tale — the dead-path bug (why rule 0009 L5 exists)

`harness-check.zsh` was once moved from `fresh/` to `ai/` but `harness.service` kept pointing
at the old path. The timer fired, the service failed silently, the checker never ran — found
only by inspecting the unit. The move had been "verified" by a hand-run of the script; the
trigger was never exercised.

**Standing rule (0009 L5):** for any script with a trigger (systemd / git hook / cron), done =
**the trigger fires and produces its artifact**. A hand-run is not verification. Close the loop
with `systemctl --user start` + `journalctl`, or a test commit on the watched path.

---

## Pointers

- Live file map + temple-family rules: `~/.config/zsh/AGENTS.md` · `~/.config/zsh/ai/README.md`
- Mail/doorbell probes (`doorbell-smoke`, `transport-selftest`, dry-fire): panel `temple-help` ·
  `guide-temple-mail.md`
- Token hygiene for Gemini sessions: `guide-for-user.md` §Hygiene
