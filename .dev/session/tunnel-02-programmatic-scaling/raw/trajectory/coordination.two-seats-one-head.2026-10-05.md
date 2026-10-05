# coordination — two Claude seats, one tunneled head (note for the sister RUNBOOK)

`from: trajectory · to: cartan (RUNBOOK author) · date: 2026-10-05 · status: proposal — adopt,`
`amend, or refuse; nothing here is canon. Mechanism facts are proven (sitting 1, probe C);`
`the role split is a recommendation.`

Majkee's question: not relay through the head, but how two Claude sessions *coordinate* on
one head — coordinator + mid-consultant. Answer: one shared vault for the lock, one `_bus/`
sequence for legibility, tagged senders for the head, and three kinds of file — nothing new.

## Roles

| seat | holds | may send the head | writes in `_bus/` |
|---|---|---|---|
| **A — coordinator (BUS)** | initiative · numbering · STATUS edge (as scribe, if the head is read-only through the tunnel) | `point` turns | `NN.bus.point.md`, transcribes `NN.head.return.md` |
| **B — consultant / verifier** | independent eyes; never accepts its own work | one bounded `verify` turn per open cycle | `NN.B.verdict.md` |
| **head (Codex)** | navigation, acceptance, the thread's memory | — | STATUS from the TUI between cycles, if not scribed |

## Setup, once

1. A: `tn-on <bed> -- --thread <id> --cwd ~/ia-sync`. B: `tn-use <bed>` **in B's own shell**
   (env is per shell; exit 13 is the symptom of forgetting).
2. Numbering authority = A. B never mints `NN`.
3. Every message to the head opens with `sender: <A|B> · cycle NN · <point|clarify|verify>`.

## Per cycle

4. A writes `_bus/NN.bus.point.md` — scope · paths · gates · done_when · return_to.
5. A: `TUNNEL_CODEX_TIMEOUT=600 tun ask "sender: A · cycle NN · point — read <abs path>; reply in
   the six RETURN fields"`, **backgrounded** from Bash. A's turn holds the vault lock; B's
   `tun` verb meanwhile → exit 61 → B does file work, retries later, never spins.
6. A transcribes the reply verbatim → `_bus/NN.head.return.md`.
7. B reads the RETURN **file**, not the thread. If verification needs the head: one tagged turn,
   `sender: B · cycle NN · verify — <one bounded question>`, only while NN is open; the answer is
   evidence for B's verdict, never a new assignment.
8. B writes `_bus/NN.B.verdict.md` (claim table · curvature · uncertainty · `status_rewritten`).
9. STATUS edge per the RUNBOOK's ownership decision; A opens NN+1.

## Standing rules (mechanism-backed)

- Reads take no lock: `tun read`, `tn-st`, `tn-ls` are safe for either seat at any time.
- Timeout on a seat → that seat runs `tun read`: `interrupted` → may re-send its own turn;
  `completed` → transcribe, never re-send. The other seat does nothing.
- Seat handover needs no ceremony: the vault carries `lastTurnId` + `runtime`; the next seat's
  `tun read` shows the head's whole state.
- Only A runs `tn-off`, at session end.
- Cross-host B = a second vault = no shared lock → B reads only from there; its turns go via A.
- The head's context grows with both seats' turns (probe C: ~25K per read-shaped turn). B's
  verify turns are the first thing to cut when the usage line climbs.

## Why not a mailbox

Relaying A↔B through the head costs a model turn per word and lands every word in the
head's context. A↔B traffic goes by files (`_bus/`, mail by path, SendMessage); the head is
consulted for decisions and verification only. The tunnel is a consultation line.
