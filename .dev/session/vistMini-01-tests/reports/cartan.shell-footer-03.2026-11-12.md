# Cycle03 exact shell-task footer registration

2026-11-12 · home:cartan · baseline e6ecc03 · register before code.

The reverse02 clean29 diagnostic at09:51:40Z now supplies the missing frame. Composer is empty `❯ NBSP`, cursor at its start; after the separator, the stripped footer is exactly:

```text
  ⏵⏵ auto mode on · 1 shell · ← 1 agent · ↓ to manage
```

The current classifier recognizes only the footer containing `(shift+tab to cycle)`, so this actual background-shell-task variant is coherently unknown and refuses29. The one shell is the caller's ongoing handoff. This confirms the cause for reverse02; it does not retroactively prove the cause of reverse01's uncaptured frame.

Register this **exact** one-shell/one-agent footer in addition to the existing footer. Keep both endpoint checks in the one-shot. Do not skip the sender's check, broaden unknown footers, change lifetime checks or treat busy/draft as ready. A background shell-task indicator is different from a surviving root shell: root must still be the agent. A busy marker takes precedence over either footer.

Registered isolated cases before execution:

- F01: exact observed footer + empty Claude composer → check0 and one fixture submission, no real peer.
- F02: exact observed footer + dim suggestion → check0 and exact pointer submission.
- F03: same footer + typed draft →23 unchanged; same footer + busy marker →24 unchanged.
- F04: unobserved two-shell footer →29 unchanged. Do not generalize count/layout without evidence.

Run all C/T/R cases and these F variants on `vist-test`. Then commit, open thread03 through the adapter and wait for its reply. Reverse01 and reverse02 both remain failed/manual, so four pairs alone cannot now yield three successful reverse sends; ask the head to authorize a fifth bounded pair to replace reverse02. No manual notice is counted and no push by Cartan.
