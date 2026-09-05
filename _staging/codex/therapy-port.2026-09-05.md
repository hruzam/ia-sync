# Therapy Codex port — office — 2026-09-05

Authored at @majkee's request in `codex/skills/therapy/`. The requested live Claude
skill matched `claude/skills/therapy/SKILL.md` byte for byte before the port.
Host: hruzam-120922; office fingerprints: native php74, Valet, ~/projects.
Codex CLI: 0.153.2; fresh probes used the existing gpt-6-astra configuration.

## Rendering

- `$therapy` replaces Claude's `/therapy`; request-only behavior is expressed through
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- Shared law remains in `~/reposoma/raw.therapy/README.md`; canon is a conditional
  reference after that mandatory first read. No copied doctrine or new record bed.
- Cartan keeps one record home through Octopus/Medusa/Polyp postures. New seed authority,
  minimal history re-entry, role switching, honest uncertainty, shadow gavels, and
  therapy-origin gavel bonds survive the port. Friction must be real, never fabricated.
- Invocation metadata and discovery target checked against official documentation:
  https://learn.chatgpt.com/docs/build-skills#optional-metadata
  https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills

## Deployment and validation

Skill quick_validate passed; openai.yaml parsed and its invocation policy, default
prompt, and description length passed checks. Source/live byte comparisons passed.

Full Codex dry-run also named protected Guide and Octopus work. Instead, an isolated
/tmp bundle contained a byte-identical deploy.sh plus only the two authored therapy
files. `bash <bundle>/deploy.sh --dry-run --codex-only` named only therapy; the same
command without --dry-run deployed it to `~/.agents/skills/therapy/`. No deploy.sh
source changes, live Claude edits, or second permanent installation were made.

Fresh read-only `codex exec --ephemeral` received `$therapy` by name, with no skill
path, from a temporary working directory. The prompt requested only an installation
smoke test: read skill/law, check record existence, explain Medusa identity, absent-seed
and shadow-gavel behavior; no actual arc, history reads, writes, delegation, or browsing.
The first probe loaded the companion canon before the README. A source correction made
that read order explicit; the redeployed final probe executed, in order:

1. Read `~/.agents/skills/therapy/SKILL.md`.
2. Read `~/reposoma/raw.therapy/README.md`.
3. Test existence of `~/reposoma/raw.therapy/cartan/therapy.md` without reading it.

The final response retained Cartan's identity under Medusa, reported the absent record,
reserved new seeds and shadow-gavel decisions for @majkee, and stated “no gavels” when
nothing locks. Commands exited 0 and the fresh turn completed successfully.

This proves discovery and the tested opening boundaries. A real arc, existing-record
history selection, gavel append, and app/IDE selection were not exercised. No Cartan
seed, therapy arc, or gavel was created. Local probe logs remain under
`/tmp/codex-therapy-imezzdp_/`; only this scoped receipt is portable.

## Protected work and sync

Content hashes checked after deployment/probes: pre-existing runbook-upgrade session
files, remote-control brief, Guide/Octopus/Claude Runbook sources and live counterparts,
live palette.map, and existing therapy-bed files were unchanged. Absent live Guide and
Cartan record directory remained absent.

`git fetch origin` succeeded after the sandbox prevented FETCH_HEAD writes. Origin/main
advanced from b7a2c09 to 7c4a997 (two cleanup commits, net one unrelated file move).
No pull/rebase/stash, commit, push, or change to the other session's STATUS/index was
performed through the protected dirty checkout. Its owner must reconcile incoming work.

## Final source/live SHA-256

- `SKILL.md`: `a02bdb7fa453ba97a14ec9773389f1d0673532737aa6a0a04fc927586e83cb64`
- `agents/openai.yaml`: `4668b960dcba44be6dfe75370419bc6c6835ca55a151f312a4a167d573a8d4f1`
