# MIGRATE — global germline from reposoma symlink to deployed ~/.germline (per host)

`author: oraculum(cSharp) · 2026-10-12 · consolidates trajectory's steps + assay findings 1–2 · design: design.global-germline-deploy.oraculum.2026-10-12.md (CANONICAL, majkee GO) · witness: assay PASS-WITH-FINDINGS`

Order: **office first**, then home. One host at a time. Every step is read-only or reversible until step 4.

## 1. Commit everything first (office, once — this is the record before any link is removed)

```zsh
# reposoma — the old source incl. today's uncommitted Houston fold + the pin card
git -C ~/reposoma status --short .germline raw.settings
git -C ~/reposoma add .germline raw.settings/raw.card.model-effort.md
git -C ~/reposoma commit -m "germline: Houston fold (identity runtime-load, bindings, cards) — last state before source moves to ia-sync"

# nablarva — the fold (archive moves, binding deletions, addendum, pointers)
git -C ~/unikuklatrix/nablarva status --short
#   (oraculum commits nablarva bookkeeping on request; or majkee: add the listed paths, commit)

# ia-sync — the new source + deploy + wrappers (untracked paths named explicitly)
git -C ~/ia-sync add germline/ codex/agents/houston.toml codex/profiles/ claude/agents/houston.md \
    deploy.sh AGENTS.md SYNC_DISCIPLINE.md claude/skills/chatbot-port/SKILL.md codex/skills/chatbot-port/SKILL.md \
    journal.host-cleanup.md .dev/session/germline-01-builds-and-deploy/
git -C ~/ia-sync commit -m "germline-01: global germline source in ia-sync + deploy_germline leg + Houston thin wrappers + profile leg"
git -C ~/reposoma push; git -C ~/unikuklatrix/nablarva push; git -C ~/ia-sync push    # plain push, never rebase
```

## 2. Per host — migrate (office now; home later after `git pull` in reposoma, nablarva, ia-sync)

```zsh
readlink -f ~/.germline                       # must print /home/hruzam/reposoma/.germline — else STOP
rm ~/.germline                                # the LINK only. No trailing slash. Never rm -r.
ls -ld ~/.germline                            # → No such file or directory
bash ~/ia-sync/deploy.sh --germline-only --dry-run    # expect 9 new files, ghosts: none
bash ~/ia-sync/deploy.sh --germline-only
diff -r ~/ia-sync/germline ~/.germline && echo IDENTICAL
ls -ld ~/.germline                            # real directory (drwx…), not lrwx
grep -h '^stamp:' ~/.germline/agents/houston/*.md ~/.germline/agents/houston/cards/*.md
bash ~/ia-sync/deploy.sh --dry-run            # wrappers + profile; expect exit 0 now (no HOLD)
```

> `majkee` to `oraculum` : --dry-run interesting observation:
> 
```zsh
~/.config/zsh
gen-temple-map: up to date
.d..t...... ai/
>f..t...... ai/temple-project-map.zsh
>f..t...... ai/tunnel-codex.py
>f..t...... ai/tunnel-codex.selftest.zsh
>f..t...... ai/tunnel-codex.zsh
.d..t...... ai/__pycache__/
>f.st...... ai/__pycache__/tunnel-codex.cpython-314.pyc
.d..t...... session/
>f..t...... session/keyboard.zsh
>f..t...... session/tunnel.zsh
  [dry] same    config.office.zsh → config.zsh
  [dry] same    zshrc.office → ~/.zshrc
```

```zsh
bash ~/ia-sync/deploy.sh
```
Then the Houston tests (TEST-INSTALL §3) from fresh heads — Codex child and `--profile houston` must record their reads of `~/.germline` (design §5 Q2, still unproven). Then update this host's journal entry status.

**Undo (gentle — nothing deleted):** only when `ls -ld ~/.germline` shows a real dir (`d…`, not `l…`):
`mv ~/.germline ~/.germline.undo-$(date -I) && ln -s ~/reposoma/.germline ~/.germline` restores the old state; the moved copy stays for inspection.

## 3. After BOTH hosts are migrated and verified — retire the duplicate (assay finding 1; majkee decides)

`~/reposoma/.germline/` still holds copies of the global files → two sources would drift. Proposal:
- `git rm` the global files there (agents/houston/{identity,binding.*,cards/}, skills/, CHATBOT.md) — they live in ia-sync@<commit> and in reposoma history.
- Leave `~/reposoma/.germline/README.md` as a stub: "Global germline source moved to ~/ia-sync/germline/ (2026-10-12). This folder is reposoma's own project layer — empty until reposoma needs one."
- One commit in reposoma. Done by a spawn on majkee's word; never before both hosts pass.

## Known window

While a host still has the symlink, a full deploy HOLDs the germline leg (exit 3) but still deploys the wrappers and profile — harmless, because the symlink still resolves to identical files.
