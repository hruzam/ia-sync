# experimental/ — experimental brick scope (machine surface)

A top-level zsh scope (sibling of `ai/`), promoted out of `ai/experimental/` on
2026-09-22: bricks named "experimental" but hidden inside `ai/` became orphans.
Holds opt-in, portable experiments that earn a run but are not stable enough to
become a first-class Claude, Codex, or Gemini surface.

Two brick kinds, distinguished by entrypoint filename — **this is LAW, not
convention** (`base.zsh` PARTITION 3 header repeats it):

- `experimental/<id>/runner.zsh` — **lazy runner.** Nothing loads at shell startup;
  the dispatcher only ever executes it on demand via `exp-run <id>`. Mechanical
  safety: a broken runner cannot break the shell, only its own invocation.
- `experimental/<id>/<id>.zsh` — **sourced brick.** Loads at shell startup, wired
  by explicit name in `base.zsh` PARTITION 3 (never globbed), `zsh -n`-gated (a
  syntax error skips the source — command absent, never shell dead). Must be
  define-only: no work, no prints on source.

## Layout

```text
experimental/
  base.zsh          signpost — sourced by config.<machine>.zsh; wires the scope
                    + carries the MAINTAINER LOG (per-brick provenance/status)
  keyboard.zsh      control panel — aliases only (exp-list, exp-run, per-brick shims)
  dispatcher.zsh    engine — _exp_list / _exp_run bodies; resolves runners lazily
  README.md
  <id>/
    runner.zsh      lazy runner brick (see Contract) — OR —
    <id>.zsh        sourced brick (see Contract) — a brick is one or the other,
                    never both
    registry.json   optional, brick-local convenience data (either kind)
```

`<id>` is lowercase letters, digits, and hyphens. The dispatcher resolves exactly
`experimental/<id>/runner.zsh` for lazy runners; no registry or `deploy.sh` change
is needed. A sourced brick instead needs one explicit `base.zsh` PARTITION 3 line
(see "Add a sourced brick" below) — `deploy.sh` carries the folder in either way,
but never wires the source line for you.

## Contract

Lazy runners (`<id>/runner.zsh`):
- Executable zsh program, not a file sourced at shell startup.
- Invoke it with `exp-run <id> [arguments]`; `exp-list` discovers installed runners.
- Every runner must support `--help` without making a network request.
- A friendly alias may be added to `keyboard.zsh`, but it must delegate to `_exp_run <id>`.

Sourced bricks (`<id>/<id>.zsh`):
- **Define-only.** No work, no prints on source — functions / `typeset -g` only
  (decision 0009 L2 discipline). The command itself does whatever it needs when
  the operator invokes it by hand; it must not run itself at source time.
- Wired by one **explicit-name** line in `base.zsh` PARTITION 3 — never a glob.
  Add the line in the same edit as the brick's maintainer-log row.
- The wiring line is `zsh -n`-gated: a syntax error skips the source instead of
  breaking shell startup. This is a mechanical backstop, not a substitute for
  testing — verify with a fresh shell before calling it done (see below).

Both kinds:
- Keep API keys, chat transcripts, caches, and provider login state outside this portable
  tree. Use the existing machine-local secret surface only at runtime.
- Do not give a brick filesystem writes, tool execution, or persistent memory by default.
  Add those capabilities only with an explicit task and verification gate.

## Maintainer log & approval

Every brick is **EXPERIMENTAL ONLY until @majkee approves** graduation to a first-class
surface. The maintainer log in `base.zsh`'s head records each brick's plug date, origin,
and approval status. When you plug a new brick, add its row there; when a brick graduates,
remove its row and move it out of this scope.

## Add a runner

1. Create `experimental/<id>/runner.zsh` in `~/ia-sync/zsh/`.
2. Run `zsh -n` on it and `exp-run <id> --help` after deployment.
3. Add a row to the maintainer log in `base.zsh` (plug date · origin · status).
4. Add the runner's own README when it has setup, limits, or security notes beyond this
   contract.
5. Run `bash ~/ia-sync/deploy.sh --dry-run`; recursive zsh deployment carries the folder.

The first runner, `ox-alpha`, is the reference implementation.

## Add a sourced brick

1. Create `experimental/<id>/<id>.zsh` in `~/ia-sync/zsh/` — define-only (functions /
   `typeset -g`; no work, no prints on source).
2. In the SAME edit: add the `base.zsh` PARTITION 3 wiring line (explicit name,
   `zsh -n`-gated — copy the existing pattern) AND the maintainer-log row.
3. Run `zsh -n` on the brick, then `bash ~/ia-sync/deploy.sh --dry-run` / `deploy.sh`.
4. Verify in a **fresh shell**: the command exists and behaves; then a deliberate-red —
   temporarily break the brick's syntax, open a fresh shell, confirm it still boots
   clean and the command is simply absent, then restore.

The first sourced brick, `4x1`, is the reference implementation.
