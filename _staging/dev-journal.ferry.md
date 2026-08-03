---
what: dev-journal.ferry — transhost cargo log for ferry crossings outside the freya route
state: LIVE — append here when anything moves between office and home via ferry or drag lane
verified: 2026-08-03 (first entry: mariadb-mcp mirror landed on home)
next:
  - mariadb-mcp: composer install on home to materialize vendor/
  - mariadb-mcp: create config.local.php on home (home DB creds — NOT drag from office; different DB)
  - ferry.md: consider adding mariadb-mcp as a named app-repo lane alongside freya
  - this file: extend with every future transhost op (new repo, drag-lane file, service state)
---

# dev-journal.ferry — transhost cargo log

Record of every mariadb-mcp / non-freya asset that crossed the tailscale bridge.
Provenance stones for ferry operations so future sessions know what came over, when,
and what is still missing.

---

## 2026-08-03 · mariadb-mcp — first mirror on home

**Operation:** git clone from GitHub origin (standard, off-record — no drag lane needed)

```
git clone git@github.com:hruzam/mariadb-mcp.git ~/www/mariadb-mcp
```

**State on office (verified via ssh office):**
- branch: `core`
- commits: `6e097f1 production`, `a827f2b init`
- gitignored on office: `config.local.php` (dev creds), `config.prod.php` (prod creds, chmod 600), `vendor/`

**State landed on home:**
- path: `~/www/mariadb-mcp`
- branch: `core` — matches origin
- present: `server.php`, `src/`, `composer.json`, `composer.lock`, `config.example.php`, `README.md`
- absent (expected): `vendor/` — needs `composer install`
- absent (action needed): `config.local.php` — must be created fresh for home DB (NOT dragged from office; different credentials)

**Why it matters:**
mariadb-mcp is the owned MCP server for both local (fantasyobchod dev) and future prod DB access.
The fantasyobchod `.mcp.json` references it. Without the home mirror the mariadb-local MCP tool
is unavailable in home sessions.

**Wired in fantasyobchod:**
`.mcp.json` entry `mariadb-local` points to `~/www/mariadb-mcp/server.php` with `config.local.php`.
`.mcp.json` entry `mariadb-prod` was added in session `mcp-prod-profile` (2026-07-22) — UNCOMMITTED
in fantasyobchod as of that session close.

**Next for this cargo:**
1. `cd ~/www/mariadb-mcp && composer install` — materialize vendor/
2. Create `config.local.php` from `config.example.php` — home DB host/user/pass
3. Test: `/mcp` reconnect in a fantasyobchod session → `mariadb-local` should appear
4. Smoke-test: `SELECT 1` via the tool

---

## Ferry awareness note

ferry.md v1 route is freya-only (app-repo + devenv-repo + drag lane).
mariadb-mcp is a SEPARATE utility repo — same transport mechanism (GitHub git), but not part of
the freya route. It should be added as a named lane in a future ferry.md revision, or tracked
here until the route is extended.

Current ferry route: `freya.devenv/ferry/prep-home.sh` — does NOT cover mariadb-mcp.
Workaround: manual clone (done above). Document in ferry.md `## Known parked cargo` or extend
the drag lane table with: `mariadb-mcp | git | ~/www/mariadb-mcp | vendor/ + config.local.php`.

