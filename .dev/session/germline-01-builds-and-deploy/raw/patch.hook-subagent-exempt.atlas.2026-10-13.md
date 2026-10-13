---
type: patch-proposal
status: APPROVED majkee 2026-10-13 — source edited by delta; deploy + S1–S5 + live check by majkee
author: atlas(harness) · spawned inside oraculum row
date: 2026-10-13
target: ~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh  (SOURCE; live ~/.claude/hooks/… is a byte-identical deploy copy)
stacks_on: patch.hook-tunnel-whitelist.atlas.2026-10-13.md (option-A, already applied + deployed today)
reason: the PreToolUse[Bash] whitelist is inherited by every subagent oraculum spawns and denies their Bash; majkee wants the fence to judge ONLY the main-session carrier
---

# Patch proposal — exempt subagents from the carrier's bash-whitelist

## 1. The problem (confirmed live this session)

The hook is wired only in `oraculum.md` frontmatter (`PreToolUse` matcher `Bash`), yet it fires on
the Bash calls of **every subagent oraculum spawns** — undocumented inheritance down the spawn tree.
Observed today: @delta / @trajectory Bash denied. Confirmed again while drafting this patch: my own
(atlas, a subagent) `set` / `awk` / `bash` calls were denied by this very hook, which is why the
test harness below must be run by majkee, not by an agent.

Majkee's intent: the whitelist judges **only the main-session carrier** (oraculum, started
`claude --agent oraculum`); subagents it spawns are unrestricted by this hook — their own `tools:`
lists bound them.

No matcher/scope option restricts a frontmatter hook to the main agent (docs
https://code.claude.com/docs/en/hooks.md + sub-agents.md, 2026-10-13), so the gate must be a
**script-level early exit**.

## 2. The discriminator — `agent_id`

Per "Common input fields" (hooks.md, 2026-10-13), stdin JSON carries `agent_id` = "Unique identifier
for the subagent or in-process teammate the hook fires in". It is **present in a subagent's** hook
input and **absent on the main carrier thread** (inferred; point 5 verifies empirically).

- Do **not** key on `agent_type` — it is `"oraculum"` on the main thread too, so it cannot tell
  carrier from spawn.
- Do **not** key on `transcript_path`.
- `agent_id` is the only field that separates the two, so: **non-empty `agent_id` → spawn → allow.**

## 3. stdin-once discipline (the load-bearing constraint)

The current hook reads the command with `jq -r '.tool_input.command // empty'` **from stdin** (line
22). stdin is a one-shot stream: a second `jq` reading `.agent_id` from stdin would get nothing. The
early exit must therefore **capture stdin once** into a variable and feed BOTH the `agent_id` test
and the existing `.tool_input.command` extraction from that variable. This is the smallest correct
diff. (heredoc / `<<<` / `$( )` inside the hook SCRIPT are fine — the script is the vetter, not a
vetted command.)

Fail-closed is preserved: if `jq` errors on the `agent_id` line (malformed JSON), the substitution
yields empty → test false → control falls through to the `CMD=…|| deny` line, which still fails
closed. The exemption cannot weaken the fence; it can only lift it for a confirmed spawn.

## 4. Unified diff (against the SOURCE, which already carries the option-A tunnel patch)

```diff
--- a/claude/hooks/oraculum-bash-whitelist.sh
+++ b/claude/hooks/oraculum-bash-whitelist.sh
@@ -19,8 +19,17 @@ deny() { echo "bash-whitelist: $1 — $ROUTE" >&2; exit 2; }
 
 command -v jq >/dev/null 2>&1 || deny "jq missing, cannot read the command (fail closed)"
-CMD=$(jq -r '.tool_input.command // empty' 2>/dev/null) || deny "unreadable hook input (fail closed)"
+INPUT=$(cat)                                   # capture stdin ONCE — jq must not consume it twice
+
+# ── subagent exemption ──────────────────────────────────────────────────────
+# This frontmatter hook (wired only on oraculum) fires on the carrier AND on every subagent oraculum
+# spawns — undocumented inheritance, observed 2026-10-13 (delta/trajectory Bash denied). Judge the
+# carrier ONLY: subagents are bound by their own tools: lists, not this economy fence. agent_id is
+# present in a subagent's hook input, absent on the main carrier thread → non-empty agent_id = spawn.
+# See patch.hook-subagent-exempt.atlas.2026-10-13.md (risk §6: spawns gain fully unrestricted Bash).
+[ -n "$(jq -r '.agent_id // empty' 2>/dev/null <<< "$INPUT")" ] && exit 0
+
+CMD=$(jq -r '.tool_input.command // empty' 2>/dev/null <<< "$INPUT") || deny "unreadable hook input (fail closed)"
 [ -z "$CMD" ] && exit 0
```

Only the stdin-read region changes (old line 22 → eight lines). Everything downstream — the two
masking passes, the per-segment whitelist, the tunnel verb gate from the option-A patch — is
untouched and still runs for the carrier.

## 5. Tests (majkee runs these against the LIVE hook path — agents cannot run Bash under it)

exit 0 = ALLOW, exit 2 = DENY. Build JSON with `jq -n` so inner quotes are safe. `t` = no agent_id
(carrier); `ta` = agent_id present (spawn).

```zsh
H=~/.claude/hooks/oraculum-bash-whitelist.sh
t(){  jq -n --arg c "$1"            '{tool_input:{command:$c}}'          | bash "$H"; echo "exit=$?"; }
ta(){ jq -n --arg c "$1" --arg a "$2" '{agent_id:$a,tool_input:{command:$c}}' | bash "$H"; echo "exit=$?"; }

# S1 DENY  — carrier, non-whitelisted command, no agent_id
t  'python3 -c 1'                                              # expect exit=2, "out of whitelist (python3)"

# S2 ALLOW — same command, but agent_id present → subagent exempt
ta 'python3 -c 1' 'a123'                                       # expect exit=0

# S3 ALLOW — carrier regression: T1-style tunnel ask still passes the full whitelist
t  'TUNNEL_CODEX_TIMEOUT=1800 zsh ~/.config/zsh/ai/tunnel-codex.zsh ask "hi"'   # expect exit=0

# S4 DENY  — carrier regression: carrier/majkee-only verb still blocked (option-A verb gate)
t  'zsh ~/.config/zsh/ai/tunnel-codex.zsh close'              # expect exit=2, "tunnel verb 'close' …"

# S5 ALLOW — agent_id present + close → exempt (DOCUMENTED CONSEQUENCE, see §6)
ta 'zsh ~/.config/zsh/ai/tunnel-codex.zsh close' 'a123'       # expect exit=0
```

S5 is intended behavior under majkee's rule, not a leak: once a subagent is exempt, the hook stops
vetting it entirely, so it can issue any tunnel verb. Carrier-only verbs (`resume` / `close` /
`open` / `steer`) are kept carrier-only by the **tunnel protocol**, not by this hook — the hook no
longer polices spawns at all.

## 6. Risk note — what subagents gain

- **Full, unrestricted Bash for every oraculum-spawned subagent.** The economy fence (and the
  tunnel verb gate) now protects the carrier ONLY. A spawn can run any command, write anywhere, and
  issue any tunnel verb. This is the explicit goal (spawns are bound by their `tools:` lists, not by
  this hook), but it is a real widening — state it at handoff.
- **Dependence on an inferred field.** The patch assumes `agent_id` is absent on the carrier and
  present on spawns. The failure directions are asymmetric:
  - If a spawn ever *lacks* `agent_id`, it gets re-restricted by the fence — annoying, fail-safe.
  - If the carrier ever *has* `agent_id`, the carrier fence silently disappears — the dangerous
    direction. **This is why the live check (step 5 of §7) is mandatory, not optional.**
- Interaction with option-A: unchanged. The tunnel verb gate still governs the carrier; it is simply
  never reached for a spawn.

## 7. Apply steps (operator / majkee — I hold read-only Bash, no deploy rights)

1. Edit the SOURCE only: `~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh` (apply §4). Never edit
   the live `~/.claude/hooks/…` copy; do NOT run `sync.sh` against the freshly edited source before
   deploy (it would overwrite it with the stale live copy).
2. Syntax: `bash -n ~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh` → no output.
3. Dry run: `bash ~/ia-sync/deploy.sh --dry-run` — confirm only this hook reports UPDATE.
4. Deploy: `bash ~/ia-sync/deploy.sh`, then
   `cmp ~/ia-sync/claude/hooks/oraculum-bash-whitelist.sh ~/.claude/hooks/oraculum-bash-whitelist.sh`
   → identical. Commit + push in `~/ia-sync`; other machine `git pull` + `deploy.sh`.
5. Run S1–S5 (§5) against the live path — all must match expected.
6. **One empirical live check** (reload uncertainty: script edits likely apply on the next call; if
   not, restart the session). As oraculum: spawn @delta to run `python3 -c 'print(1)'` → must
   **succeed**; then the carrier runs the same `python3 -c 'print(1)'` → must be **denied**. This is
   the test that proves `agent_id` actually discriminates carrier from spawn in the field.
