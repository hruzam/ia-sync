---
name: session-resume
description: Invoke when flow wire is lost and you need to recover last session context. Derives project from CWD, finds most recent .jsonl, reads handoff.json if present. Always asks before reading — never auto-reads.
---

I recover session context for the current project. I do not auto-read anything — I ask first.

## Steps

1. **Derive project slug from CWD** (via @Delta):
   ```bash
   pwd
   ```
   Convert the absolute path: replace each `/` with `-`, strip the leading `-`.
   Example: `/home/hruzam/www/imago_cz/fantasyobchod` → `-home-hruzam-www-imago-cz-fantasyobchod`

2. **List recent sessions** (via @Delta):
   ```bash
   ls -lt ~/.claude/projects/<derived-slug>/*.jsonl 2>/dev/null | head -5
   ```

3. **Surface and ask** — show UUID, date, file size. Ask:
   > "Found session `<UUID>` from `<date>` (`<size>`). Read it? (yes / no / different project)"

4. **If yes** — check for a handoff file first (lighter than the full jsonl):
   ```bash
   find . -name "handoff.json" -path "*/.dev/session/*" 2>/dev/null | sort -r | head -3
   ```
   If a handoff exists, read it. If not, offer to grep the jsonl for keywords.

5. **If wrong project** — ask which project path to use instead. Never assume.

## Rules

- Never hardcode `~/.claude` — always derive slug from CWD at invocation time
- Always ask before reading any session file (single token-economy ask covers all)
- If the derived slug returns no sessions, ask the user which project scope to search
- Do not crawl upward looking for the nearest journal — that risks the wrong project
- Spawn @Delta for any bash operations (this skill has no Bash access)
