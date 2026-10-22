# Termbrana request/0.1 — wire contract

Approved by Majkee on 2026-10-20 under [central flag L17](../../../unikuklatrix/nablarva/.dev/session/flag.md).
This is the durable wire home promoted from the unchanged reviewed v4 proposal.
Section numbers retain its anchors. Only proposal/provenance wording and historical
fixture commentary were removed; the approved field, byte, marker, scalar/list,
error and whole-document rules and every complete example are unchanged.
Publication/activation and later preparation, loading or delivery are separate.

## 2. Document, Q3 and ownership

One human-owned Markdown exchange containing several packets in source
order. Outside text may precede, separate and follow packets and is preserved.
Read only saved bytes; never write the exchange or claim an unsaved editor buffer
was parsed. Informal `to-...`, `from-...`, `&&`, `---`, fences and headings open
no packets and confer no authority.

Q3 is composition in that exchange, without a second per-prompt drafts
tree. Later Phase 2 may freeze selected packets to `prompts/<id>/<rev>.md`; Phase 0
creates none. Frozen EXCHANGE files are unchanged test bodies, not files to migrate.
Q4 gives `&&` no Phase 0 action; Q1/Q2 render policy and Q5 rotation remain open.
Do not open references, resolve bindings or execute header, body or outside text.

Agent/program/controller/function selections belong in the composed prompt body;
their references and instructions are prepared before sending. Several selections
may coexist as ordinary body text. Phase 0 neither discovers nor loads instructions,
resolves selections, dispatches collaborators nor executes text. `from`, `to` and
`consult` are retained metadata, not a selection mechanism or dispatch authority.
Picker notation and later preparation/rendering design remain open; quoted `ctrl`,
`&&`, `program:` or `function:` body examples below adopt no picker syntax. The
existing exact active end line remains the body's only structural boundary.

Agent-made marker drafts and a future stdout-only skeleton brick are permitted
forms of preparation, never exchange-writing authority. This Phase 0 interface
includes neither a skeleton nor a writer. STATUS remains the head's sole position.

## 3. Frame and exact byte ownership

Markers have exactly these ASCII spellings at column 1, with the shown spaces:

```text
<!-- composer:packet N -->
<!-- composer:body N -->
<!-- composer:end N -->
```

N is 4–8 characters matching `[a-z0-9]{4,8}`. It correlates syntax, not identity or
content integrity. Each structural packet opening uses a nonce not previously used
by another structural packet in that whole document. Once opened, that nonce stays
used through EOF; do not reset it between packets, notes or Markdown sections.
Marker-looking data inside B does not register a structural nonce.

State sequence is outside → header(N) → body(N) → outside. Outside accepts packet
openings. An exact body/end marker outside is orphaned (`marker_order`), except
that any exact marker there with an already used nonce fails `nonce_reused` first.
In header(N), only the exact body marker with N advances state; other exact markers
are `marker_order`. No nested packet opens in a header.

Physical lines end at LF. Immediately preceding CR makes that EOL CRLF; bare CR
is not a line separator. Let E be the opening marker's LF or CRLF. Opening, header
and body-marker syntax lines must end with E. A recognized end line may terminate
at EOF without EOL; otherwise its EOL must equal E. Packets may choose different E.
Outside/body EOL bytes remain unchanged, including mixed LF/CRLF and bare CR data.

After the body-marker EOL, let s be the next byte offset. Inspect successive
physical lines solely to recognize the first column-1 line whose entire content
is exactly `<!-- composer:end N -->`. Here content excludes its LF or CRLF EOL;
an EOF-terminated line has no EOL to exclude. Let t be that line's start. B is
exactly [s,t). The recognized line ends B before its own EOL is validated. If that
EOL is the wrong kind for E, fail `frame_eol` there and stop; never choose a later
correctly terminated end line instead. At EOF, an exact complete end line is valid.

All other lines in body(N) are data: same-nonce packet/body markers, different-nonce
end markers, indented/inline/quoted ends, trailing spaces, bad nonce spellings,
partial end tokens, headers, commands and Markdown fences. Do not apply the
outside/header marker-syntax check inside B. In particular, a malformed end-like
line is not a structural closer or an immediate error; it remains B. If no exact
closer ever follows, fail `missing_end` at EOF. A token followed by bare CR at EOF
is not an exact line (the CR is content); it also remains data. These rules separate
recognition from EOL validation without guessing intended delimiters.

The opening/body-marker EOLs and all marker bytes are framing. The end marker's
own EOL, when present, is framing. B includes every byte before the end line,
including its own final LF or CRLF. There is no extra separator and no newline
stripping. Empty B means the end marker starts immediately after the body-marker
EOL. Nonempty B necessarily ends in LF; a nonempty intended body without final LF
cannot be represented. Do not add a newline and claim byte identity. A body ending
in bare CR alone is likewise unrepresentable; a bare CR elsewhere stays data.

| frame E | intended B in byte notation | bytes after body-marker EOL before end line | result |
|---|---|---|---|
| LF | empty | empty | valid empty B |
| LF | `x\n` | `x\n` | valid; final LF belongs to B |
| LF | `x\n\n` | `x\n\n` | valid; both final LFs belong to B |
| LF | `x\r\n` | `x\r\n` | valid; body CRLF is unchanged |
| LF | `x\r` or `x` | no representation | accepted limitation |
| CRLF | empty | empty | valid empty B |
| CRLF | `x\n` | `x\n` | valid; body need not use frame E |
| CRLF | `x\r\n` | `x\r\n` | valid; no extra CRLF |
| CRLF | `x\n\r\n` | `x\n\r\n` | valid; mixed body EOLs retained |
| either | `x\ry\n` | `x\ry\n` | valid; internal bare CR retained |

Whole-document validity requires at least one complete packet. Any later error
invalidates the entire document: no valid-prefix extraction or downstream packet
result. After a sound closer, resume outside at the following physical line.

Outside/header lines beginning `<!-- composer:` after removing leading ASCII
spaces/tabs, but failing the marker grammar, are `marker_syntax`. Indentation,
trailing spaces, capitalized verbs, invalid nonces or truncated tokens never form
delimiters. Uppercase `COMPOSER` and inline markers are ordinary outside prose.
Markdown fences shield nothing in outside/header states. An exact marker with an
LF/CRLF EOL is recognized before checking whether that EOL matches E.

## 4. Encoding and lossless representation

Validate the complete input as UTF-8 before structure; reject invalid sequences
without replacement decoding. Preserve an optional initial UTF-8 BOM at absolute
offset zero as outside bytes, ignoring it only for first-line recognition. U+FEFF
elsewhere is body/outside data; it is invalid in a header. An initial body BOM
is never stripped and does not exempt that line from exact column-1 matching.

No text-mode newline conversion, Unicode normalization or decode/re-encode round
trip may change source bytes. Delimiters lie on physical-line boundaries; B's
endpoints therefore cannot split a valid UTF-8 character. `é∇\n` is preserved as
its UTF-8 bytes, regardless of display width or character count.

Retain original document bytes, ordered packet/header/frame/body spans and decoded
header fields. All header values remain strings or flat string lists. Lossless
re-emission copies original spans rather than serializing decoded fields anew.
Packets and whole documents must round-trip byte-identically, including raw quotes,
spacing, field order, BOM, outside notes and framing EOLs. Editing decoded values
and generating new documents is outside this Phase 0 contract.

No fixed body-size cap is selected. If wanted, one fixed limit
and its diagnostic must be separately decided; never add a size header. No helper
or limit implementation follows. Memory/I/O exhaustion is operational failure,
never an empty valid document or a successful shortened body.

## 5. Flat header and string scalars

Header lines are column-1 `key: value`, key `[a-z][a-z0-9_]*`, colon and one required
ASCII space. Additional ASCII spaces around a value are trimmed only for decoding
and retained in raw bytes. No tabs, blank lines, comments, indentation, continuations,
nesting or multiline values. Order is free. Unknown keys and repeated known keys
are errors even if repeated values agree. Diagnostic tokenization also recognizes
uppercase ASCII key letters; uppercase keys are `unknown_key`, never corrected.

| key | required | decoded value |
|---|---|---|
| `format` | yes | scalar exactly `request/0.1` |
| `id` | yes | nonempty scalar, unique by exact decoded value across document |
| `from`, `to` | yes | nonempty scalar declarations; no authentication |
| `requested_scope` | yes | nonempty scalar; no enforcement claim |
| `consult` | no | flat string list; absent means empty list |
| `in_reply_to` | no | nonempty scalar; resolution deferred |
| `context` | no | flat string list; absent means empty list |
| `expected_return`, `stop` | no | nonempty scalar; no semantic evaluation |

Exactly five keys are required. Absent-required-field order expands combined rows
left to right: format, id, from, to, requested_scope. No other implicit defaults. No body-size,
bus/type/hold/created/thread/rev or extension keys. A legacy body_bytes line is an
unknown key; it never changes B. Names/references are opaque case-sensitive strings:
no path opening, registry query, reply-lineage resolution or permission evaluation.
Only decoded id uniqueness is structural.

`program` and `function` are not allowed keys, including optional or list-valued
aliases. A well-shaped header line with either key gives FIELD_INVALID/unknown_key
before inspecting its value: scalar, list, empty or malformed value is immaterial
once the key is unknown. Each repeated occurrence remains unknown_key, not
duplicate_key. Their absence produces no required_absent. Existing syntax-line
EOL and line-shape precedence still comes first (§8); no new diagnostic is added.

Scalar source is bare text or one complete JSON double-quoted string. Bare values
are nonempty and exclude C0/DEL controls, ASCII double/single quotes, square/curly
brackets and U+FEFF. U+2018/U+2019/U+201C/U+201D are prohibited only as the first/last
bare-value character to catch accidental smart quote delimiters; internally they
are data. Colons, hashes, backticks, `&&`, dates, digits and backslashes are literal;
no YAML comments, aliases or coercions. `no`, `2026-10-17`, `01234567` remain strings.

JSON-string form uses standard JSON escapes with no trailing nonspace text. Reject
empty decoded strings, C0/DEL, unpaired surrogate escapes and U+FEFF. Quoted strings
may contain apostrophes, brackets, commas and smart quotes. Escaped newline/tab is
invalid after decoding. Tabs in header source are always invalid, even in a quoted
string. Trailing ASCII spaces are accepted and preserved in the raw header.

## 6. Flat lists

Only consult/context use lists: `[` zero or more string items separated by commas
`]`, with ASCII spaces around tokens. `[]` is valid. No empty items, trailing comma,
nesting, maps, comments, tabs or multiline forms. A bare item follows scalar rules
but cannot contain a comma. JSON-quote items needing commas/brackets, e.g.
`context: ["a,b", "path with spaces"]`. Respect quotes and escapes during tokenization;
do not blindly split commas. Empty decoded items are invalid. `consult: [Astrobley]`
remains accepted. Preserve order and repeated elements; resolution/deduplication is
not parsing. Scalar in list field or list in scalar field is `wrong_shape`. Do not
convert list items into dates/numbers.

## 7. Complete examples and editing limits

Valid LF document; B is `alpha\nomega\n`, with no extra separator:

```text
<!-- composer:packet a7b2 -->
format: request/0.1
id: example
from: Majkee
to: myShell
requested_scope: read-only
<!-- composer:body a7b2 -->
alpha
omega
<!-- composer:end a7b2 -->
```

Valid empty body in a separate document:

```text
<!-- composer:packet empty8 -->
format: request/0.1
id: empty-example
from: Majkee
to: myShell
requested_scope: read-only
<!-- composer:body empty8 -->
<!-- composer:end empty8 -->
```

Required negative insertion witness: insert one same-nonce end line into the first
example's intended body while retaining the original end. This entire document is
invalid:

```text
<!-- composer:packet a7b2 -->
format: request/0.1
id: example
from: Majkee
to: myShell
requested_scope: read-only
<!-- composer:body a7b2 -->
alpha
<!-- composer:end a7b2 -->
omega
<!-- composer:end a7b2 -->
```

The first end closes B as `alpha\n`. `omega\n` is outside text. The retained true
end is then an exact outside marker with a used nonce: `BOUNDARY_INVALID/nonce_reused`
at that second end's line start, field null, nonce `a7b2`. Reject the whole document,
including that shorter packet; never scan past the first closer to repair B.

If that true end is absent, the syntax can instead be valid with a shorter B and
outside prose. Framing cannot discover the author's unrecorded intent. A random or
agent-suggested nonce is no proof against later collision, authenticity or mutation.
To include an exact end-looking line as body data, choose an active nonce different
from that line before use; no escaping or automatic nonce repair is defined. Bodies
with no final LF remain unrepresentable. Ordinary prose edits need no size metadata.

An additional valid document has several selections entirely in its body. These
literal strings witness opaque composition data, not adopted picker notation:

```text
<!-- composer:packet mix4z -->
format: request/0.1
id: composed-body-example
from: Majkee
to: myShell
requested_scope: read-only
consult: [Astrobley]
<!-- composer:body mix4z -->
For the eventual recipient: ask Astrobley to inspect and Oraculum to challenge.
Use the prepared references/instructions supplied with that later request.
program: journal-continuity
function: list-pending
program: project-saddle
function: saddle-project
Literal composition sample: ctrl journal-continuity&list-pending && ctrl project-saddle&saddle-project
These body strings trigger no Phase 0 lookup, loading or execution.
<!-- composer:end mix4z -->
```

## 8. Deterministic diagnostics and aggregation boundary

Check success exits 0; input data errors exit 65.
Operational file/I/O/resource failure exits 74 and is never success.
The CLI and Python API are described in README.md. Invalid input returns
diagnostics and no usable packet result, even after a sound prefix. Retaining raw
input for human diagnosis is permitted; acting on prefix packets is not.

Each diagnostic has exactly code, reason, byte_offset, line, byte_column,
packet_nonce (string or null), field (header key or null). Offsets are zero-based
absolute; line/byte_column one-based, with each LF starting a new line. BOM bytes
count toward offsets/columns. EOF is len(input), following final LF at next line
column 1. Never emit raw body text, time, randomness, paths or locale-dependent prose.

| code | reasons |
|---|---|
| ENCODING_INVALID | invalid_utf8 |
| BOUNDARY_INVALID | marker_syntax, marker_order, nonce_reused, missing_body, missing_end, frame_eol, no_packets |
| HEADER_INVALID | header_line, header_syntax, unsupported_format |
| FIELD_MISSING | required_absent, empty_value |
| FIELD_INVALID | unknown_key, duplicate_key, wrong_shape, invalid_string, invalid_list, duplicate_id |

This is the complete reason set. Count/byte-endpoint/separator errors are removed.
The former exact-position end_mismatch/end_truncated reasons also have no v4 role:
nonmatching/partial body lines are data, and exhaustion without a closer is
`missing_end`. A recognized closer with wrong LF/CRLF uses `frame_eol`. No size-limit
code is added without selection of a fixed limit.

Textual diagnostics are one JSON object per LF-terminated line, keys in the order
above, no spaces around separators, integer decimal offsets, literal JSON null,
no summary or interleaved output. Empty sequence emits no diagnostic bytes.

Deterministic processing and stopping rules:

1. Validate whole-input UTF-8 first. Failure yields only `invalid_utf8` at the first
   invalid-sequence start, null nonce/field; parse no structure.
2. Walk outside/header lines in source order. For marker-like lines there, precedence
   is malformed spelling, reused nonce (outside only), marker order, required EOL.
   Stop at the first such structural failure, retaining prior independent header
   findings. A wrong-nonce marker in a header is `marker_order`. Header EOF without
   its body marker yields `missing_body`; no search forward or resynchronization.
3. Header ordinary lines first require E (otherwise `frame_eol`, stop). Then check
   line shape, known/unique key, value shape, string/list decoding, supported format,
   and decoded id uniqueness. Emit only the first failure per line. A recognized key
   with invalid value still counts as seen; later occurrence is `duplicate_key`.
   Unknown-key repetitions stay `unknown_key`. A successfully decoded id registers
   for document uniqueness even if another field in its packet is invalid.
   In particular program/function header lines use `unknown_key` for every
   well-shaped occurrence, even empty/list/repeated values. Value decoding does
   not follow an unknown-key finding; neither `empty_value`, `wrong_shape`,
   `invalid_list` nor `duplicate_key` replaces it. Existing EOL/line-shape failures
   still precede key lookup. The field is the tokenized removed key, with active N,
   anchored at that line's start. A line without required colon-space instead uses
   `header_syntax`; a tab-containing line uses `header_line` (after EOL validation).
4. At a structurally sound matching body marker, emit `required_absent` for never-seen
   required keys in §5 order. Invalid/empty seen keys already have findings. Collect
   all independent header findings and continue delimiter recognition even when
   header values are invalid; these values cannot change the delimiter nonce.
   Only format/id/from/to/requested_scope are required. Omitted program/function
   adds no absent-field findings, regardless of body composition text.
5. In body(N), ignore every line except the first exact column-1 end line with N
   under §3. EOF without one yields `missing_end` at EOF, active N, null field;
   no guessed later packets/header findings. Once recognized, validate its EOL
   immediately. LF versus CRLF mismatch is `frame_eol` at the first differing EOL
   byte. EOF without any EOL is valid. Never skip a recognized wrong-EOL closer.
6. After a sound closer, resume outside, retaining all known ids/nonces. Thus the
   insertion witness's second end fails `nonce_reused`. At otherwise clean EOF with
   no opened packet, report `no_packets` at offset zero. Do not add it after a more
   specific opening/header/structural error. Any finding invalidates the document.

For outside/header syntax lines, an exact marker token at EOF is still recognized
for precedence. An opening or body marker there then lacks its required E and gives
`frame_eol` at EOF. A bare-CR suffix fails marker spelling there (`marker_syntax`);
in body it remains data as §3 specifies. For ordinary header lines, bare CR is an
invalid EOL: `frame_eol` at that CR. LF/CRLF mismatch anchors at its first differing
byte; missing required EOL anchors at EOF. These rules do not require uniform body EOL.

Blank/comment/indented/tab-containing ordinary header lines use `header_line`; other
key/colon-space violations use `header_syntax`. After a known unique key, scalar
value beginning `[`/`{`, or list value not beginning `[`, uses `wrong_shape`. Bad
scalar syntax uses `invalid_string`; bad list syntax/items uses `invalid_list`.
Empty bare/decoded scalar uses `empty_value`; empty list item uses `invalid_list`.
Unsupported decoded format uses `unsupported_format`. Duplicate id checks use exact
successfully decoded strings, without case folding/normalization.

Header findings anchor at line start, absent keys at body-marker start, malformed/
order/reused markers at their line start. `missing_body`/`missing_end` anchor at EOF.
Fields are populated only after key tokenization; structural/encoding errors use
null field. Marker errors in header/body use active N. Outside exact markers use
their parsed nonce; malformed outside markers use null. `no_packets` and initial
UTF-8 errors use null nonce; outside frame errors on openings use the opening N.

Sort final diagnostics by byte_offset ascending, then code ASCII, reason ASCII,
field ASCII with null first; exact ties retain encounter order, no deduplication.
Absent fields therefore encounter §5 order but final output follows this total
sort. Aggregate only independently knowable findings before the structural stop;
claim none for an unframed suffix. This is the explicit research A7 boundary.
