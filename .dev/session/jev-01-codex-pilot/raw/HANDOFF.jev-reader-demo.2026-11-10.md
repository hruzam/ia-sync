# Ready-to-use Jev reader data

From Cartan(jev-01), office, 2026-11-10. For majkee and cooperating implementer
`01a1aa8a-b5d4-70d3-9823-4f44f05af2d2`; majkee relays this file.

The earlier live audit contains preparation/reply evidence but no separately authored
`memory` events. Empty memory filtering there is expected. A valid synthetic playground
has now been generated through native Jev commands, with no credentials or provider calls.
No reader/engine or installed shell code was changed for this task.

## Open this vault

```zsh
jev-browse --root /home/hruzam/.local/share/jev-reader-demo-c9wshleb/vault
```

If the current shell has not loaded the alias, the exact installed entry is:

```zsh
python3 -B ~/.config/zsh/jev/browser.py \
  --root /home/hruzam/.local/share/jev-reader-demo-c9wshleb/vault
```

Use arrows to choose **01-memory-notes**, then Enter. Press **m** for memory-only,
**a** to mark all visible notes, then **p** to compose Markdown. Space marks individual
events; **b** returns to sessions; **q** quits. Composition exits the browser and prints
the private temporary path. Marks persist when switching filters: reopen the session
before making a fresh independent selection. Session discovery is hash-ordered, so the
named scenarios are not necessarily displayed numerically.

The browser expects a vault root containing `projects/`, not a JSONL file, export folder,
or Markdown view. Do not import these fixtures into the actual `~/.jev` vault.

## Expected sets

| Bed | Events | Memory notes | Reader exercise |
|---|---:|---:|---|
| 01-memory-notes | 7 | 6 | Decision, open task, linked correction, Unicode/multiline, literal markup/control characters, long note |
| 02-mixed-judgments | 10 | 3 | Noul/Choice/Score synthetic reply, UNCERTAIN interpretation, reconsideration, later outcome, linked follow-up preparation without reply |
| 03-invalid-reply | 5 | 2 | Invalid typed receipt retained as synthetic, visible validation failure and later note |
| 04-no-memory | 1 | 0 | Opening only; memory filter correctly empty |

Total: **23 events and 11 memory notes**. CLI identities are deliberately named
`SYNTHETIC-codex-reader-demo`, `SYNTHETIC-claude-reader-demo` and
`SYNTHETIC-gemini-reader-demo`; they do not impersonate actual source sessions.
Every note identifies itself as synthetic. Model scores are invented renderer fixtures,
not measured Jev behavior. No model or spending allowance is configured for sending.

Mixed reply: Noul 0.55; Choice clarify/proceed = 0.7/0.3, confidence 0.6;
Score distribution over levels 0–3 = 0.6/0.3/0.1/0, expected rubric index 0.5,
confidence 0.5. The score value is the expected index, not the modal category index.
Original observations remain separate from later memory notes and corrections.

## Files and regeneration

- [Private manifest: IDs, event counts and ledger hashes](/home/hruzam/.local/share/jev-reader-demo-c9wshleb/manifest.json).
- [Six readable memory notes](/home/hruzam/.local/share/jev-reader-demo-c9wshleb/views/01-memory-notes-memory.md).
- [Mixed judgments, complete view](/home/hruzam/.local/share/jev-reader-demo-c9wshleb/views/02-mixed-judgments-all.md).
- All eight saved views: `/home/hruzam/.local/share/jev-reader-demo-c9wshleb/views/`.
- [Generator](../tasks/make-reader-demo.py). Re-run with:

```bash
python3 -B /home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/tasks/make-reader-demo.py
```

Each run creates a NEW private directory and prints its root, sessions and manifest. It
does not replace the root above, append duplicate fixtures to it, or attach a shell.
Generated IDs/timestamps differ; scenario contents/counts are stable. Generation creates
native records and the manifest; the eight saved reading views were separately produced
with the installed reader during this acceptance run.

## Verification and limits

Installed `browser.discover` replayed all four sessions; memory counts match 6/3/2/0.
Installed `reader.render` produced all-event and memory-only views for each session;
control escapes, UNCERTAIN and INVALID remained visible. All generated directories/files
were checked as 0700/0600. An actual interactive PTY selected the six notes and composed
`/run/user/1000/jev-view-grqoqkhn/view.md` (temporary, may disappear).
Ledger hashes matched the manifest after rendering and interactive composition.

This is a clean usability dataset, not a complete reader acceptance suite. It does not
exercise damaged-ledger recovery, legacy actors, simultaneous changes, all policy branches
or live HTTP/billing. Existing raw-payload omission remains reader behavior. At a narrow
terminal, long absolute bed paths and the common synthetic note prefix can obscure labels;
that is useful UI feedback for the cooperating implementer, not a source-data failure.
