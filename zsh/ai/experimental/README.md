# Experimental runners

This folder holds opt-in, portable experiments that are useful enough to run but not
stable enough to become a first-class Claude, Codex, or Gemini surface.

## Layout

```text
experimental/
  README.md
  <id>/
    runner.zsh
```

`<id>` is lowercase letters, digits, and hyphens. The dispatcher resolves exactly
`experimental/<id>/runner.zsh`; no registry or `deploy.sh` change is needed.

## Contract

- `runner.zsh` is an executable zsh program, not a file sourced at shell startup.
- Invoke it with `exp-run <id> [arguments]`; `exp-list` discovers installed runners.
- Every runner must support `--help` without making a network request.
- Keep API keys, chat transcripts, caches, and provider login state outside this portable
  tree. Use the existing machine-local secret surface only at runtime.
- Do not give a runner filesystem writes, tool execution, or persistent memory by default.
  Add those capabilities only with an explicit task and verification gate.
- A friendly alias may be added to `keyboard.zsh`, but it must delegate to `_exp_run <id>`.

## Add a runner

1. Create `experimental/<id>/runner.zsh` in `~/ia-sync/zsh/ai/`.
2. Run `zsh -n` on it and `exp-run <id> --help` after deployment.
3. Add the runner's own README when it has setup, limits, or security notes beyond this
   contract.
4. Run `bash ~/ia-sync/deploy.sh --dry-run`; recursive zsh deployment carries the folder.

The first runner, `ox-alpha`, is the reference implementation.
