# pad.4-env-vault — seal `zsh/.env/` into a travelling ciphertext blob, on the surgical table

> mode: MANNED (majkee driving, Flight seat) · date: 2026-07-30 · authored from: office
> **Purpose:** encrypt the one folder that actually leaked into git (`zsh/.env/`) so the
> *git copy* is ciphertext, without changing how you reach the plaintext day to day.
> Sequential operator test surface — run one STEP, paste the result in its `>MAJKEE report`
> slot, then the next. Nothing here deploys; the whole pad runs on the surgical table.
> **charter note:** like pad.2, this is ia-sync/repo content, not OS/desktop state — it
> stretches this folder's scope, kept here for pad continuity.

Tool: `~/ia-sync/env-vault` (already round-trip tested on dummy data, 2026-07-30).
Design in one line: **the seal is additive** — plaintext `zsh/.env/` is never moved or
deleted, the blob is an *extra* encrypted copy. You cannot be locked out on a working
machine; the one thing to not-lose is the key file.

Scope locked with operator: **`zsh/.env` only** this session. `.majkee/` and other projects
adopt the same two verbs later — do NOT widen scope inside this pad.

---

### STEP 0 — state + office↔home conflict audit (run first, report back)

The last two days had messy overwrite ordering; confirm office is on a clean, non-divergent
base before sealing anything onto it.

```bash
cd ~/ia-sync
git status --short
git log --oneline -3
git fetch origin 2>&1 | tail -2 && git log --oneline --left-right --count HEAD...origin/main 2>/dev/null || echo "(no upstream/main to compare — note it)"
echo "--- live seal target ---"
ls -la ~/.config/zsh/.env/
echo "--- age present on office? ---"; age --version
```

Expected: working tree clean (or only this pad/env-vault untracked); no unexplained
divergence from origin; `~/.config/zsh/.env/` holds the 5 known files; age ≥ 1.3.

- clean + no conflict → STEP 1
- **any divergence or uncommitted mess you did not expect → STOP, resolve the audit first.**
  That is the "audit here" gate — do not seal onto a contested tree.

>MAJKEE report 0
```zsh

```

---

### STEP 1 — free hygiene stone (optional, independent of the vault)

`secrets.zsh`/`secrets.json`/`.htaccess`/`office.gemini.curl.md` are `644` (world-readable);
only `fo-db.cnf` is `600`. This is the live-FS boundary we are *not* defending, so it is
optional — but it is free and closes a real local hole.

```bash
chmod 700 ~/.config/zsh/.env
chmod 600 ~/.config/zsh/.env/*
ls -la ~/.config/zsh/.env/
```

>MAJKEE report 1
```zsh

```

---

### STEP 2 — generate the shared key, and BACK IT UP (the one anti-trap step)

```bash
cd ~/ia-sync
./env-vault init
# verify it is readable and note the public recipient line:
./env-vault status
```

Then, **before going further**, back the key up off this repo and off git, and copy it to
home over tailscale (home needs the same key to open the blob):

```bash
cp ~/.secrets/zsh/id.age ~/  # or a USB / password-manager attachment — your durable spot
# copy to home (adjust user/host):
scp ~/.secrets/zsh/id.age hruzam@100.110.27.60:~/.secrets/zsh/id.age  # mkdir -p there first if needed
```

Expected: key at `~/.secrets/zsh/id.age` mode 600; a backup you have *verified you can read*;
home has the same file. **This is the only "don't forget" in the whole system.**

>MAJKEE report 2
```zsh

```

---

### STEP 3 — pre-seal plaintext backup (reposoma Phase-3 non-negotiable)

The additive design means the plaintext persists anyway — but a verified backup *before the
first real seal* is cheap insurance against a fat-fingered `--force` later.

```bash
tar -C ~/.config/zsh -czf ~/zsh-env.plaintext-backup.$(date +%F).tgz .env
tar -tzf ~/zsh-env.plaintext-backup.*.tgz | head   # verify it is readable
```

>MAJKEE report 3
```zsh

```

---

### STEP 4 — seal for real (round-trip auto-verified)

```bash
cd ~/ia-sync
./env-vault seal ~/.config/zsh/.env zsh/env.vault.age
./env-vault status zsh/env.vault.age ~/.config/zsh/.env
# prove no plaintext leaked into the blob (must print OK):
grep -aqf <(grep -rhoE '[A-Za-z0-9_-]{12,}' ~/.config/zsh/.env/secrets.zsh) zsh/env.vault.age && echo "LEAK!" || echo "OK: no plaintext token in blob"
```

Expected: `sealed + round-trip verified`; status shows blob present (ciphertext) AND plaintext
present ("safe from lockout here"); grep prints `OK`. The `seal` command already decrypted the
candidate and compared it to source before writing — if it printed success, it opens.

>MAJKEE report 4
```zsh

```

---

### STEP 5 — wire the guards (one decision to gavel)

The blob must **commit** (so it travels) while the plaintext stays **excluded**.

```bash
cd ~/ia-sync
git check-ignore zsh/env.vault.age && echo "BAD: blob is gitignored — fix" || echo "OK: blob is committable"
git check-ignore zsh/.env/ && echo "OK: plaintext folder still excluded" || echo "CHECK: plaintext not ignored"
grep -q '^\.env$' sync.deny && echo "OK: sync.deny still excludes .env plaintext" || echo "CHECK sync.deny"
```

**Decision to gavel (my lean in brackets):** should a deployed copy of the blob round-trip
back through `sync.sh` and cause re-seal churn? age re-encrypts differently every time, so a
blob that travels live→repo would show as "changed" on every sync. **[My lean: add
`env.vault.age` to `sync.deny`** so the repo blob is authoritative and never overwritten by a
synced-back copy; the blob is produced by `env-vault seal` into the repo directly, not via the
live folder.] Confirm and I add the one line.

>MAJKEE report 5
```zsh

```

---

### STEP 6 — commit only the blob (pad.3 STEP 8 lesson: verify staged == intended)

```bash
cd ~/ia-sync
git add zsh/env.vault.age env-vault install-pkgs/maintenance/pad.4-env-vault.md
git add install-pkgs/maintenance/README.md   # index row for pad.4
git diff --cached --name-only    # <-- MUST be exactly these; NO zsh/.env/* plaintext
```

Expected: staged list contains the blob, the tool, this pad, the README — and **nothing from
`zsh/.env/`**. If any plaintext appears, STOP and unstage.

>MAJKEE report 6
```zsh

```

---

### STEP 7 — cross-machine deploy test (the real "test against pad 4")

On **home**, after it pulls, prove the shared key opens the blob *without touching home's live
plaintext*:

```bash
# on home:
cd ~/ia-sync && git pull --rebase
./env-vault open zsh/env.vault.age /tmp/env-verify
diff -r /tmp/env-verify ~/.config/zsh/.env && echo "OK: blob opens to home's live secrets" || echo "DIFF — investigate"
rm -rf /tmp/env-verify
```

Expected: the blob office sealed opens cleanly on home with the shared key and matches home's
own `.env/`. That closes the loop: one folder, sealed on office, openable on home, ciphertext
in git.

>MAJKEE report 7
```zsh

```

---

## Companion hygiene (parked, not part of this seal)

- **`~/.majkee/cooking-recipies/`** — delicate small notes in the SHM harness. **Must be
  deploy-excluded** (deny-list entry) when `.majkee/` lands. Capture now so it is not
  forgotten; wire it with the `.majkee/` sync leg, not here.
- **Relay to home** — home installs `age` (`pacman -S age`) and receives the shared key
  (STEP 2). Without both, STEP 7 cannot run on home.

## Execution record (2026-07-31, office, majkee in the seat)

Walked compressed in-session rather than step-by-step — operator present throughout:
STEP 0 ✅ (audit ran across the day: 0/0 both repos, deploy clean) · STEP 2 ✅ key created
`~/.secrets/zsh/id.age`, recipient `age19faqvmfsv3uv6my3sccg7d8pde7cl7lxelqtlj8a5dsjud3jzdtquj8r0p`
· STEP 3 ✅ plaintext backup `~/zsh-env.plaintext-backup.2026-07-31.tgz` verified readable ·
STEP 4 ✅ sealed `zsh/env.vault.age` (10440 b), round-trip verified, blob leak-check opaque ·
STEP 5 ✅ gavel resolved per lean: `env.vault.age` added to `sync.deny` · STEP 6 ✅ this commit.
STEP 1 (chmod) not run — folder perms deferred, operator's call. STEP 7 pending on home
(needs key: home pulls `scp office:~/.secrets/zsh/id.age` — office→home ssh has no pubkey
trust, home→office does). Key durable backup = operator's item, OPEN.

## Still open

- **Operator: durable key backup** (USB / password manager) — the one don't-forget.
- STEP 1 chmod 700/600 on live `.env/` — optional hygiene, not run.
- STEP 7 — home-side open test, after home pulls the key.
- Whether `deploy.sh` should push the blob to the live tree at all (my lean: no — the blob is
  a repo/travel artifact; the live machine already has the plaintext). Decide when wiring deploy.
- `.majkee/` adoption of the same two verbs — next session, its own pad.
