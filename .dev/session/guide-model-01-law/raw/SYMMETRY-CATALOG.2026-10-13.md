# Symmetry drop — catalog · 2026-10-13

`what: an extraction receipt and bounded index for the Claude.ai Symmetry package; it does not gavel or promote anything.`

## Receipt

- Source archive: `../../guide-model.zip` (relative to this `raw/` directory).
- SHA-256: `b0a0fae9d036bfd758b3c4c9aaa33b90414bb61b8ec14b4d11155a7d586fc3aa`.
- Integrity: `unzip -t` reported every member `OK` and no compressed-data errors.
- Extracted unchanged to `symmetry-drop-2026-10-13/guide-model/`; 12 files, all under the archive's single `guide-model/` root.

## Contents and directly observable status

| file | observed role | observable status |
|---|---|---|
| `PACKAGE.md` | placement map and package reading order | package/proposal; says nothing was written from its originating thread |
| `RUNBOOK.guide-model-01-law.md` | proposed 01 execution contract and writer/witness prompts | proposed session runbook; its goal requires majkee gavel and a fresh witness |
| `RUNBOOK.guide-model-02-audit.md` | proposed later audit contract | future-session proposal; explicitly makes 01's gaveled guide its yardstick |
| `model-shape.md` | proposed model-guide law and conversion method | frontmatter: `state: DRAFT — gavel text` |
| `write-background.md` | proposed `BACKGROUND.md` standard/function | frontmatter: `state: DRAFT` |
| `BACKGROUND.guide-writing.seed.md` | proposed first `guide-writing/BACKGROUND.md` | frontmatter: `seed: DRAFT`; says its decision rows require majkee confirmation |
| `GUIDE.template.txt` | controller template | template; no claim of canonical installation |
| `FUNCTION.template.txt` | function-chapter template | template; no claim of canonical installation |
| `BACKGROUND.template.txt` | background template | template; no claim of canonical installation |
| `guide-census.py` | read-only census implementation | executable source supplied as staging/probe material; not run by this extraction task |
| `census.2026-10-12.md` | dated census receipt/results | dated receipt, explicitly facts-only and already liable to staleness after repository change |
| `hypotheses.reconcile-only.md` | sealed audit hypotheses | explicitly non-evidence; read only after the future auditor freezes a worklist |

No extracted item establishes canonical law by itself: the three substantive documents label themselves draft/seed, and both RUNBOOKs name gavel, witness, or later-session gates.

## Minimal reading order for the future Astrobley head

1. Current bed `RUNBOOK.md`, `STATUS.md`, and `PROGRAM.md` — live local control surfaces, outside this drop.
2. This catalog, then `PACKAGE.md` — disposition and intended placement.
3. `RUNBOOK.guide-model-01-law.md` — proposed gate and the writer's exact bounded prompt.
4. The prompt-0 canonical inputs named there (live `guide-writing/GUIDE.md` + `res/slug-directories.md`, then the staged `model-shape.md` + `write-background.md`, then the live Claude `/guide` skill). Treat the drop copies as reference/receipt unless their placement is verified.
5. `BACKGROUND.guide-writing.seed.md`, followed by the three templates only when the conversion step needs them.

Defer `RUNBOOK.guide-model-02-audit.md`, `census.2026-10-12.md`, `guide-census.py`, and `hypotheses.reconcile-only.md`: they support the later audit or its tool/receipt, not 01's first gavel.
