---
type: patch-proposal
status: APPLIED — option A chosen by majkee 2026-10-13; source edited by delta, deployed + T1–T7 run by majkee by hand; superseded-in-part by patch.hook-subagent-exempt (subagents exempt)
author: atlas(harness) · spawned inside oraculum(cSharp) row
date: 2026-10-13
target: ~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh  (SOURCE; live is a deploy copy)
reason: the PreToolUse[Bash] whitelist blocks oraculum's carrier Bash from driving the Codex tunnel
---

# Patch proposal — tunnel turn shape through the bash-whitelist hook

## 1. Wiring + scope found (file:line)

- **Hook script (SOURCE of truth):** `~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh`.
  Live copy `~/.claude/hooks/oraculum-bash-whitelist.sh` is byte-identical — it is a
  `deploy.sh` rsync target, NOT an independent file. Edit the source, never the live copy.
- **Deploy leg:** `~/ia-sync/deploy.sh:311-315` rsyncs `$REPO/claude/hooks/` →
  `~/.claude/hooks/` (additive, no `--delete`).
- **Only wiring point:** `~/ia-sync/claude/agents/oraculum.md:24-29` — frontmatter
  `hooks: PreToolUse: matcher "Bash" → bash ~/.claude/hooks/oraculum-bash-whitelist.sh`.
  `grep` across `~/ia-sync/claude/agents/` and `~/.claude/agents/` returns ONLY oraculum.md.
  `~/.claude/settings.json` has **no** `hooks` key (grep count 0). The project
  `~/unikuklatrix/nablarva/.claude/` wires nothing. So the hook has exactly one declared owner.
- **Effective scope (the finding that matters):** although declared only on oraculum, the hook
  **blocked @delta and @trajectory subagents today**. Those seats carry no `bash-whitelist`
  wiring of their own. The only consistent explanation is that Claude Code applies a parent
  agent's `PreToolUse[Bash]` frontmatter hook to the subagents spawned *during that agent's run*
  — the hook inherits down the spawn tree. So the real blast radius is **oraculum + everything
  oraculum spawns** (delta, trajectory, atlas(harness), etc.), not oraculum alone. This patch
  does not change that inheritance; it only changes what the hook allows. Confirm the inheritance
  empirically if it matters (it governs whether delta/trajectory can ever run code-side Bash while
  under oraculum).

## 2. What the patch allows / still blocks

**Allows** (new):
- An optional leading tunnel env prefix in the same segment as the helper call:
  `TUNNEL_CODEX_TIMEOUT=<digits>` and/or `TUNNEL_CODEX_STATE=/…tunnel.state.json` — shape-checked,
  then peeled so the real command word resolves to `zsh`, not to the assignment.
- The tunnel helper with a verb in **{ask, send, read, status}** and exactly one quoted argument
  for ask/send (none for read/status). Both the tilde/`$HOME`/`$home_tunnel` forms and the literal
  `/home/hruzam/.config/zsh/ai/tunnel-codex.zsh` absolute form are accepted.

**Still blocks** (unchanged or newly tightened):
- `open`, `close`, `resume`, `steer` on the tunnel — **newly denied** by the verb gate (see the
  RISK below; today the hook checks no verb at all, so these pass).
- Any chaining after the tunnel call (`;`, `&&`, `|`) whose next segment is not itself whitelisted
  — handled by the pre-existing per-segment model, not by new code. The only "chains" that survive
  are `export …; zsh …tunnel…` (both segments pass) and the sanctioned recovery
  `zsh …tunnel… read | jq '…'` (both pass).
- Env-prefix abuse: `TUNNEL_CODEX_TIMEOUT=1 curl …` still denies (peel only strips the two tunnel
  vars; the trailing command word is vetted normally).
- Heredocs (`<<`), `sed -i`, write redirects to non-`.md`, substitution `$( )` / backticks / `<( )`
  — all unchanged.

### RISK — flag for majkee's decision before applying
The verb gate **tightens** the hook: it currently allows every tunnel verb. Restricting to
{ask, send, read, status} means the **carrier (oraculum) can no longer `resume`/`close`/`open`
through its own Bash** — only majkee's terminal (no hook fires there) could. Tunnel protocol
Rule 2 grants `resume`/`close` to the carrier between settled turns. The hook cannot tell
carrier-oraculum from an atlas/delta subagent — it is one process tree — so a 4-verb allowlist
hits the carrier too. Three options:
- **(A)** Apply as written (4 verbs). Carrier does `resume`/`close` via majkee or an explicit
  non-hooked shell. Matches the task's literal instruction; costs the carrier its Rule-2 verbs.
- **(B)** Allow {ask, send, read, status, resume, close} (carrier keeps Rule 2), still block
  `open`/`steer` (`open --enable` is majkee's hand; steer is nobody's in this trial). Smaller
  behavior change; keeps carrier autonomy.
- **(C)** Drop the verb gate entirely; fix only the env-prefix (hunk 1). Minimal; leaves
  open/close/resume/steer as open as they are today.
The diff below implements **(A)** as requested. Switching to (B) = add `resume|close` to the
`read|status` arm. I lean (B) on the merits, but defer to majkee.

## 3. Unified diff (against the SOURCE)

```diff
--- a/claude/hooks/oraculum-bash-whitelist.sh
+++ b/claude/hooks/oraculum-bash-whitelist.sh
@@ -85,6 +85,20 @@ for seg in "${SEGS[@]}"; do
     ((k++))
   done
   [ ${#argv[@]} -eq 0 ] && continue
+
+  # Peel a leading tunnel env prefix so `TUNNEL_CODEX_TIMEOUT=1800 zsh …tunnel… ask "…"`
+  # resolves to the helper, not to the assignment word (tunnel protocol Rule 4). Only the
+  # two tunnel vars, each shape-checked; any other prefix is left in place → vetted/denied
+  # normally below, so this cannot widen the whitelist.
+  e=0
+  while [ $e -lt ${#argv[@]} ]; do
+    case "${argv[e]}" in
+      TUNNEL_CODEX_TIMEOUT=*) [[ ${argv[e]} =~ ^TUNNEL_CODEX_TIMEOUT=[0-9]+$ ]] || break; ((e++)) ;;
+      TUNNEL_CODEX_STATE=*)   [[ ${argv[e]} == TUNNEL_CODEX_STATE=/*tunnel.state.json ]] || break; ((e++)) ;;
+      *) break ;;
+    esac
+  done
+  [ $e -gt 0 ] && argv=("${argv[@]:e}")
+  [ ${#argv[@]} -eq 0 ] && continue
   cmd=${argv[0]}
 
   if [ ${#redir_md[@]} -gt 0 ] && [[ $cmd != echo && $cmd != printf ]]; then
@@ -111,9 +125,14 @@ for seg in "${SEGS[@]}"; do
       for x in "${argv[@]:1}"; do [[ $x == -i* || $x == --in-place* ]] && deny "sed -i"; done ;;
     ls|cat|head|tail|wc|grep|cmp|diff|sha256sum|cd|pwd|date|hostname|jq|echo|printf) ;;
     zsh)
       case "${argv[1]}" in
-        '~/.config/zsh/ai/tunnel-codex.zsh'|'$HOME/.config/zsh/ai/tunnel-codex.zsh'|"$home_tunnel") ;;
+        '~/.config/zsh/ai/tunnel-codex.zsh'|'$HOME/.config/zsh/ai/tunnel-codex.zsh'|'/home/hruzam/.config/zsh/ai/tunnel-codex.zsh'|"$home_tunnel") ;;
         *) deny "zsh ${argv[1]:-<none>} (only the tunnel helper)" ;;
       esac
+      case "${argv[2]}" in
+        ask|send)    [ ${#argv[@]} -eq 4 ] || deny "tunnel ${argv[2]} takes exactly one quoted argument" ;;
+        read|status) [ ${#argv[@]} -eq 3 ] || deny "tunnel ${argv[2]} takes no argument" ;;
+        *) deny "tunnel verb '${argv[2]:-<none>}' — only ask/send/read/status (open/close/resume/steer stay carrier/majkee)" ;;
+      esac ;;
     export)
       [ ${#argv[@]} -eq 2 ] && [[ ${argv[1]} == TUNNEL_CODEX_STATE=* ]] || deny "export (only TUNNEL_CODEX_STATE=…)" ;;
```

Note: the `zsh)` arm ends with `esac ;;` in the new version — the first `esac` closes the path
check, the second closes the new verb check, and `;;` closes the `zsh)` case branch. (The old
version had a single `esac ;;`.)

Index math for the verb check (after the peel, argv[0]=zsh): argv[1]=helper path, argv[2]=verb,
argv[3]=the quoted message (collapsed to one word by pass-1 masking). ask/send → 4 tokens;
read/status → 3 tokens.

## 4. Point 3 (heredoc with backticks) — CONSIDERED, RECOMMEND DEFER

The reported `command substitution … cannot be vetted` on a `cat > f <<'EOF' … backticks … EOF`
is a **red herring for a safe small fix**: even with a quoted delimiter and zero substitution, the
hook denies the heredoc anyway at the `<<` gate, and `cat > f` is not an append-to-`.md` write, so
it is denied twice over. Allowing that case is not a one-line relaxation — it requires teaching
pass 1 to track heredoc-delimiter state (to suppress the backtick/`$(`-flag inside the body) AND
rewriting pass 2 so the multi-line body is not split into bogus command segments AND permitting
`cat >file`. That is a structural change to an economy-fence hook, not a small safe hunk.
**Recommendation:** do not touch heredocs here. The sanctioned path already exists — append with
`printf '…\n' >> file.md` (the hook's own deny message says so), or route a real file write to a
spawned @delta/@vector (the hook's whole ROUTE philosophy). If heredoc authoring from the carrier
becomes a recurring need, it earns its own reviewed design pass, not a rider on this patch.

## 5. Test commands (majkee runs these against the SOURCE after editing it)

The hook reads JSON on stdin and takes the command from `.tool_input.command` (line 22). Build the
JSON with `jq -n` so inner quotes are safe. exit 0 = ALLOW, exit 2 = DENY (reason on stderr).

```zsh
H=~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh
t(){ jq -n --arg c "$1" '{tool_input:{command:$c}}' | bash "$H"; echo "exit=$?"; }

# T1 ALLOW — the exact command that failed today (export state ; TIMEOUT prefix ; ask + quoted msg)
t 'export TUNNEL_CODEX_STATE=/home/hruzam/unikuklatrix/nablarva/.dev/session/nablarva-X1-architecture/tunnel.state.json; TUNNEL_CODEX_TIMEOUT=1800 zsh ~/.config/zsh/ai/tunnel-codex.zsh ask "atlas · cycle 11 · read /abs/_bus/11.point.md"'   # expect exit=0

# T2 ALLOW — sanctioned recovery read piped to jq
t 'export TUNNEL_CODEX_STATE=/home/hruzam/unikuklatrix/nablarva/.dev/session/nablarva-X1-architecture/tunnel.state.json; zsh ~/.config/zsh/ai/tunnel-codex.zsh read | jq ".thread.turns[-1]"'   # expect exit=0

# T3 ALLOW — bare status, no env prefix
t 'zsh ~/.config/zsh/ai/tunnel-codex.zsh status'   # expect exit=0

# T4 DENY — carrier/majkee-only verb (proves the verb gate; this is option A's behavior)
t 'zsh ~/.config/zsh/ai/tunnel-codex.zsh close'   # expect exit=2, "tunnel verb 'close' …"

# T5 DENY — chaining after the tunnel call
t 'TUNNEL_CODEX_TIMEOUT=1800 zsh ~/.config/zsh/ai/tunnel-codex.zsh ask "hi"; rm -rf /tmp/x'   # expect exit=2, "out of whitelist (rm)"

# T6 DENY — env prefix cannot smuggle a non-whitelisted command
t 'TUNNEL_CODEX_TIMEOUT=1800 curl http://evil'   # expect exit=2, "out of whitelist (curl)"

# T7 ALLOW — regression: bare exported state still fine
t 'export TUNNEL_CODEX_STATE=/home/hruzam/unikuklatrix/nablarva/.dev/session/nablarva-X1-architecture/tunnel.state.json'   # expect exit=0

# T8 DENY — regression: heredoc still blocked (point 3 untouched)
t "cat > f.md <<'EOF'
\`x\`
EOF"   # expect exit=2, "heredoc (<<) …"
```

## 6. Apply steps (operator / majkee — I hold read-only Bash, no deploy rights)

1. Edit the SOURCE only: `~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh` (apply the hunks
   above; choose option A/B/C on the verb gate first).
2. Run the T1–T8 tests above against the source file. All must match expected allow/deny.
3. Dry run the deploy: `bash ~/ia-sync/deploy.sh --dry-run` — confirm the hooks/ leg reports the
   single file as UPDATE and nothing else unexpected.
4. Deploy: `bash ~/ia-sync/deploy.sh` (repo → live on this box). Then commit + push in `~/ia-sync`;
   the other machine does `git pull` + `deploy.sh`.
5. Never edit `~/.claude/hooks/oraculum-bash-whitelist.sh` directly, and do NOT run `sync.sh`
   against this freshly authored file before deploy (it would overwrite the source with the stale
   live copy).
6. Live-verify once: as oraculum, run T1's command for real and confirm the tunnel turn proceeds.
</content>
</invoke>
