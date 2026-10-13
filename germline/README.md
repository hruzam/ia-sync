# germline — the canonical, vendor-blind global source

**Rule (gaveled 2026-09-25, majkee):** what lives here is the *source* (ia-sync `germline/`; deployed copy: `~/.germline/`); every vendor file derived
from it is a one-way, stamped rendering (`derived from <path> @ <revision> — do not edit here`).
Edit the source, re-render; never edit a rendering. Precedent: `raw.vendor-neutral-agents/ptyra/README.md`.

- `agents/<slug>/identity.md` — an agent's identity, rendered into Claude `.md` / Codex `.toml` wrappers (ia-sync table → deploy).
  **Runtime-load variant (Houston, final fold 2026-10-10):** the wrappers carry only a loader; at entry the agent
  reads `identity.md` → `binding.<vendor>.md` → the nearest project addendum → `cards/<card>.md` and quotes each
  file's `stamp:`. **Stamp rule:** every loaded germline file carries `stamp: <8-hex random token>`, unique per
  file, **regenerated on every edit** (`openssl rand -hex 4`) — a matching token proves the current file was read.
- `skills/skill.<slug>.md` — vendor-neutral methods; the chatbot skills (ChatGPT · Claude.ai) read these files as-is.

Scope: ~/ia-sync/germline/ is the reviewed global source; deploy.sh copies it to a real host-local ~/.germline/ (never a symlink), while <project>/.germline/ remains that project's separate scoped layer.
Author here in ia-sync, commit, then deploy; live `~/.germline/` is a deploy target, not a source. Deploy is additive:
a file removed at source lingers live until retired by hand (`deploy.sh` lists such ghosts).

No index here by design (discovery bus = parked, own session). Design + open decisions:
`~/ia-sync/.dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md`.
