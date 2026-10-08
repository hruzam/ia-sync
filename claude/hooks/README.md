# claude/hooks/ — agent-scoped hook scripts

Deployed by `deploy.sh` (hooks leg, 2026-10-08) → `~/.claude/hooks/` on both hosts. No `--delete`:
a live-only script survives until folded here. Author here, never in the live tree.

## Pattern — per-seat Bash whitelist (token economy by mechanism)

A head/carrier seat keeps Bash for bookkeeping; anything else is denied with a reason the seat sees,
so it routes the work to a spawn. Prose rules cannot stop the hand (G-27); this does.

**Adopt for a seat `<seat>`:**
1. Copy `oraculum-bash-whitelist.sh` → `<seat>-bash-whitelist.sh`; edit only its `case` list. One
   script per seat — do not widen one list to serve two seats.
2. Add to the seat's frontmatter (shape = houston.md's, the in-house precedent):
   ```yaml
   hooks:
     PreToolUse:
       - matcher: "Bash"
         hooks:
           - type: command
             command: "bash ~/.claude/hooks/<seat>-bash-whitelist.sh"
   ```
   `bash <path>` on purpose — no exec bit needed.
3. Unit-probe offline: `jq -nc --arg c "<cmd>" '{tool_input:{command:$c}}' | bash <script>; echo $?`.
4. Deploy (operator): `deploy.sh --dry-run` → `deploy.sh` → commit + push → other host pulls + deploys.

**Contract the script must honour:** input = JSON on **stdin** (`.tool_input.command`), never an env
var · deny = exit 2 + stderr · fail closed when input is unreadable. Every segment of a compound
command (`&& || ; | &` newline, quote-aware) must pass; `$( )` / backticks / `<( )` are denied outright.
It is an economy fence, not a security boundary.

## Verified behaviour (claude 2.1.293, 2026-10-08 — re-probe on client bumps)

| Mode | Hook fires? |
|---|---|
| seat as main thread (`claude --agent <seat>`), trusted source | yes |
| seat spawned as subagent | yes |
| agent def from an **untrusted project folder** (`.claude/agents/` there) | **NO — silently skipped**; only the debug log says so (`Skipping frontmatter hooks … not trusted`) |

The third row is the trap: a project-level copy of a seat drops its hook with no visible warning.
User-level seats (`~/.claude/agents/`) are unaffected. Probe evidence: CS card
`~/reposoma/_cold-start/card/CS.oraculum-bash-whitelist-hook.2026-10-07.md` + pulse.atlas 2026-10-08.

## Scripts here

| script | seat | purpose |
|---|---|---|
| `oraculum-bash-whitelist.sh` | oraculum | bookkeeping-only Bash (git · inspect · hashes · tunnel helper) |
| `guard-destructive.sh` | houston (moot — no Bash tool) | deny-list: `rm -rf /…` (any absolute path) · `DROP TABLE` · `mkfs` · `dd of=/dev` · forced artisan migrations |

`guard-destructive.sh` folded from live 2026-10-08 with its input read fixed (it read a never-set env
var and passed everything) — `~/reposoma/_cold-start/issues/ISS.guard-destructive-reads-dead-env-var.2026-10-08.md`.
