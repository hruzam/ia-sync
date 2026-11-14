# Cycle 02 — pre-registered real TUI receiver contract

2026-11-12 · author: home:cartan · baseline `df9339f` · input: VERDICT 01 / POINT 02.
Commit this document BEFORE changing the adapter. This registers a conservative screen-inferred contract, not an authenticated or atomic input API. Implementation/test results and new observations belong in a later report; do not rewrite this registration to match them.

## Live endpoint allowlist

| Server | Exact pane | Session | Expected foreground and top-level argv0 | Width/height observed |
|---|---|---|---|---|
| default | `%0` | traj-home | claude | 116×59 |
| default | `%1` | cartan-home | codex | 116×59 |

These two bindings alone are added. Explicit server and pane ID remain mandatory. Every other default pane, server and command combination refuses before input; unknown endpoints should refuse before any tmux connection. Do not support a caller override that turns another live endpoint into a trusted one. Isolated `vist-test` legacy fixtures remain available; mirrored runtime renderers may be selected there only, never as a bypass for a live endpoint's fixed runtime classifier. Keep PID/start-time and top-level lifetime checks from cycle 01.

## Read-only source observations

All live actions so far in this cycle are plain/ANSI `capture-pane` or `display-message`; no keys have been sent. Observations were obtained on 2026-11-12 around 08:42–08:46 UTC.

| Runtime/state | Observation | Status |
|---|---|---|
| Claude typed draft | `❯` plus NBSP, non-dim multiline text (body redacted); cursor `(50,55)` below first composer row | directly observed 08:42; reject occupied |
| Claude idle dim suggestion | raw `ESC[39m❯ NBSP ESC[2m<suggestion>ESC[0m`; cursor `(2,46)` at composer row46; separator and auto-mode footer below, no active busy marker | directly observed after the draft changed; eligible only under checks below |
| Claude footer | horizontal separator; `⏵⏵ auto mode on (shift+tab to cycle)` optionally with agent-count text | directly observed; footer is not composer |
| Claude empty idle | plain empty composer with ready footer | not observed in this cycle; predicted equivalent empty state, fixture only until actual observation |
| Claude busy | current footer containing `esc to interrupt` | observed in earlier manual handoff; not controlled or newly reproduced here; fixture hypothesis |
| Codex busy with placeholder | `• Working (... • esc to interrupt)` at row51; composer at row55 is still `› Ask Codex to do anything`; cursor `(2,55)` | directly observed 08:42 and 08:45; placeholder is NOT idle |
| Codex ANSI placeholder | `ESC[1m› ESC[0m ESC[48;2;57;60;66m <space> ESC[2mAsk Codex to do anything ESC[0m...` | directly observed; RGB color parameter `2` is not itself dim |
| Codex footers | model/effort/seat/context line, then `← for agents · ? for shortcuts`, below composer | directly observed; host-local thread handle and unrelated content excluded from report |
| Codex idle-empty/placeholder | same composer/footers, no current busy status, cursor at input start | UNVERIFIED hypothesis: this running main cannot observe itself idle; Trajectory's reverse send is the planned live validation after this turn |
| Codex typed draft / alternative suggestion | typed draft unobserved; arbitrary dim suggestion other than the exact known placeholder unobserved | conservative refusal; stand-in coverage only |

The typed Claude body and continuation text remain only in host-local scratch; no private operator input is copied to Git. The direct evidence retained here is the renderer's style/row/cursor relationship. Source snapshot process IDs were 1815650 (Claude), 1821701 (Codex); those are observations, not lifetime guarantees or portable handles.

## Registered decision rules

1. Locate the bottommost anchored composer glyph for the endpoint runtime (`❯` for Claude, `›` for Codex), rather than taking the screen's last non-empty line. Earlier prompt-looking transcript lines must not win. Normalize the observed prompt NBSP separator, not arbitrary user content.
2. Establish a coherent snapshot: expected exact endpoint/command/top-level process, live PID/start time, composer row, cursor, ANSI cells and observed footer shape below the composer. Cursor must be at x2 on that composer row for a ready input. Missing/unknown layout, footer, unsupported wrap or inconsistent snapshot refuses.
3. Empty suffix may be eligible. A Claude suggestion is eligible only when the entire visible suffix is dim and cursor is at input start. Codex accepts only the exact dim known placeholder (or empty suffix under the registered predicted idle rule); other suffixes refuse. Any visible non-dim text, whitespace draft or multiline continuation refuses. Parse SGR dim/reset state: do not confuse RGB/indexed color payload values with SGR2. Mixed dim/non-dim text is a draft/unknown state, not a suggestion.
4. Busy takes precedence over placeholder/suggestion. Claude checks the current footer region after the selected composer for `esc to interrupt`. Codex checks the eight physical rows immediately above the selected composer for an anchored current `• ...esc to interrupt` status, plus the current footer region. Earlier transcript matches are not current status. This is a version/frame-specific rule: unseen progress placements are a limitation, not evidence of readiness.
5. Keep bounded literal pointer validation and atomic attempt reservation. Reject a pointer too wide for the current pane's single input row (`pointer bytes + 2 < pane width`), before injection. Do not build wrapped-input editing support in this cycle. Re-read/recheck the endpoint and exact injected non-dim pointer/cursor before sending Enter separately; retain an uncertain reservation on change or interruption. No clearing, hidden retry or operator-draft submission.
6. `--check` remains read-only, injects nothing and creates no attempt state. A passing snapshot is not a receipt, a writability guarantee or a proof that the state cannot change before send. `--send` success remains labelled `receipt=unproven`.

Known information limit: capture plus cursor cannot prove there are no invisible/trimmed spaces when an operator moves the cursor back to the start. Likewise, concurrent editing, malicious renderer behavior, external respawn, unrecognized progress indicators and the final observation-to-Enter race remain outside the guarantee. The trial assumes a stable, trusted, uncontested receiver UI during its one scheduled send. If the evidence is ambiguous, refuse and report it; never count an unsafe guess as a successful case.

## Fixture registration and amendment

Retain C01–C18 under their original semantics and legacy stand-in layout. C17's old example `default:%0` becomes an explicitly registered endpoint in this cycle; amend its examples to an unregistered server and an unregistered default pane. Both still must refuse locally with zero tmux calls. This amendment is registered before implementation; it does not relax the forbidden-endpoint expectation.

Add mirrored fixture cases below. All execute only on `vist-test`, using redacted synthetic text. Predicted/unobserved live states are fixtures, never relabelled as observed live behavior.

| ID | Mirrored condition | Expected |
|---|---|---|
| T01 | Claude empty prompt with separator/footer at a nonzero row | ready check0; literal ordinary send may submit on fixture |
| T02 | Claude wholly dim suggestion, cursor at x2 | eligible; typing replaces the suggestion; exact pointer and separate Enter verified |
| T03 | Claude non-dim typed draft, including cursor at start | occupied refusal23; bytes/cursor unchanged |
| T04 | Claude whitespace-only draft with non-start cursor | occupied refusal23; text/cursor unchanged |
| T05 | Claude multiline draft / cursor below first composer row | occupied/unknown refusal; no input |
| T06 | Claude active busy footer with an otherwise empty/suggested prompt | busy refusal24 |
| T07 | Codex observed busy indicator plus dim known placeholder and footers | busy refusal24; placeholder never overrides busy |
| T08 | predicted Codex idle known placeholder plus footers, x2 on composer | fixture eligible; live status remains unverified until reverse send |
| T09 | Codex typed draft (non-dim), including x2 at its start | occupied refusal23, unchanged |
| T10 | color SGR38/48 payload contains2 but text is not dim; mixed styled suffix | refuse draft/unknown; no false dim classification |
| T11 | missing or unrecognized footer / alternate unknown suggestion | refuse unknown state29, no input |
| T12 | historical prompt and busy-looking lines above the current region; footer below actual composer | select actual bottom composer, classify current state only |
| T13 | pointer would wrap at current pane width | validation refusal before reservation/input |
| T14 | unregistered server/default pane | local refusal with zero tmux calls |
| T15 | state changes after text before Enter in mirrored layout | refusal27/uncertain reservation; no blind resend |
| T16 | read-only check on both mirrored layouts | state and composer unchanged; no attempt created |

Numeric fallback occupied/unknown outcomes in ambiguous cases must be reported as observed, not forced by weaker checks. New cases discovered later are exploratory unless an amendment is committed before their first run.

## Live experiment schedule (one send per direction)

1. Cartan finishes adapter, fixtures, report and `02.cartan.return.md`, commits/pushes all owned work while the Git window is open, and performs as many read-only checks as needed.
2. Only when Claude is eligible by this contract, Cartan calls the adapter ONCE in send mode with a short real pointer to this cycle's RETURN, using explicit local attempt state. That one send is also the ready poke closing the Git window. No additional manual poke or retry consumes a second send. If send fails/uncertain, report the result and preserve its reservation; do not bypass it.
3. Trajectory verifies and commits VERDICT02, then runs the exact reverse adapter command supplied in the RETURN when Codex is idle. It points at that VERDICT and uses a distinct message key. Cartan does not send to its own active pane. Trajectory records the reverse outcome in its state/next cycle.

The reverse direction is pending by design at Cartan's RETURN. At most one actual send in each direction belongs to this cycle. Notification attempt, turn submission, consumption and independent verification remain separate evidence. This does not yet close the 3+3 ordinary-message gate or establish VIST relevance.
