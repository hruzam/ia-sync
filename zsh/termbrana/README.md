# Termbrana composition — Phase 0

Independent bytes-in validation of the approved [request/0.1 contract](GRAMMAR.md).
This family follows the parent [control-panel convention](../AGENTS.md#control-panel-convention-canonical--operator-gaveled-2026-07-07--tightened-2026-07-11)
and [builder architecture rules](../guides/guide-for-builder.md#architecture-rules-gaveled-2026-07-11).
Central governance is [Nablarva flag L17](../../../unikuklatrix/nablarva/.dev/session/flag.md);
the [product direction](../../../unikuklatrix/nablarva/toolbox/termbrana/README.md#composition-and-explicit-input-direction)
separates the composition family from the existing Rust/WASM Zellij observer.

## Source-only use

Nothing is wired into host config or deployed. From this family directory:

```sh
python3 -I -S -B composer.py check /path/to/saved-document.md
python3 -I -S -B composer.py parse /path/to/saved-document.md
```

Standalone commands use isolated, no-site, no-bytecode startup (`-I -S -B`),
including through the zsh engine. They ignore inherited Python environment paths
and skip automatic site initialization; all dependencies are Python stdlib.
Ordinary API imports continue to use the caller's Python environment.

Either subcommand accepts `-` or no file operand to read stdin. Only that explicit
input file is opened; paths mentioned in headers/body are never loaded. Input is
read-only. There are no state/cache/output files, network calls or child processes.

The optional zsh surface defines `tbc-check`/`tbc-parse` aliases after explicitly
sourcing `base.zsh`. It is quiet and idempotent, resolves the helper beside its own
source, and needs neither deployed copies nor a particular working directory:

```zsh
source /path/to/termbrana/base.zsh
tbc-check /path/to/saved-document.md
tbc-parse /path/to/saved-document.md
```

For a single noninteractive command (including benchmarking), call its engine
function after source; this avoids same-line alias-expansion timing:

```sh
zsh -f -c 'source "$1/base.zsh"; _tbc_check "$2"' tbc /path/to/termbrana /path/to/input.md
```

Aliases live only in keyboard.zsh; functions only in composer.zsh. Names use `tbc-`
(Termbrana composition), avoiding PHP Composer. The core needs no zsh, tmux, editor,
ovitmugen, RUNBOOK bed or interactive shell.

## Python API and safe output

Import `composer` from the family using Python `-B` or
`PYTHONDONTWRITEBYTECODE=1` to suppress interpreter import caches:

```python
result = composer.parse(saved_bytes)
if result.document is not None:
    packet = result.packets[0]
    body = saved_bytes[slice(*packet.body_span)]
    assert result.document.to_bytes() == saved_bytes
```

`parse(bytes)` returns `ParseResult(document, diagnostics)`. Valid documents retain
source bytes and ordered packets with nonce, decoded fields, packet/header/body
and three frame spans. Spans are absolute, half-open byte offsets. Both absent
list fields (`consult` and `context`) default to `[]` under contract §5; all other
absent optional fields stay absent. `to_bytes()` copies source spans without
reserializing edited decoded fields. Invalid input always has document `None` and
packets `()`, including after a sound prefix. Pure API misuse raises TypeError;
operational resource errors are not successful parses.

`check`: valid input emits no bytes. `parse`: valid input emits one ASCII JSON line
with packet fields and spans, never raw bodies. Both emit only fixed-order,
ASCII-escaped diagnostic JSONL on invalid input, exactly as GRAMMAR.md §8, with
no paths/raw body text interleaved. Diagnostics go to stdout; operational errors
use fixed `{"error":"io_or_resource_failure"}` JSON on stderr. Exits: 0 valid,
65 input invalid, 74 I/O/resource/output failure, 64 usage. Both kinds of buffered
stdout failure are handled inside the operational boundary. No raw controls go
to the terminal, and parse success grants no authority.

## Operator limits

The first exact column-1 same-nonce end line closes the body, even inside a fence.
A retained later end invalidates the entire document as nonce reuse; absent
structural evidence of intent cannot be detected. Nonempty body without final LF
is unrepresentable. Mixed body EOLs, initial BOM and outside bytes are retained.
No cap is selected; available resources bound operations, not grammar validity.
There is no writer, renderer, body-export command, source loader, picker, identity
resolver, target binding, activation or delivery. Future adjustable-source and
integration requirements remain in the product direction, not runtime code.

## Checks and evidence tooling

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/acceptance.py --bed /path/to/reference-bed --out /path/to/authorized-evidence
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/benchmark.py --family "$PWD" --evidence /path/to/authorized-evidence --fixed /path/to/acceptance.fixed.json
zsh -n base.zsh && zsh -n keyboard.zsh && zsh -n composer.zsh
```

Unit tests are standalone; `acceptance.py` is explicit test tooling requiring
the caller's frozen reference bed and authorized evidence directory. It checks
independent frozen source hashes, all four exact corpus slices and saved v4
handwritten fixture, records actual `cmp`/CLI commands, exact golden negatives,
sentinel absence and unchanged references. Only this test tooling writes fixtures
and evidence. The runtime never reads the reference bed or inventory.

The benchmark generates fixtures before timing, then measures 30 fresh actual zsh
check invocations per input, including shell/Python startup, I/O and output capture.
p95 is the 29th sorted sample. Office budgets fixed before measurement: four
corpus bodies (38,799 body bytes) <=100 ms; 1 MiB <=500 ms; 4 MiB <=2 s and median
<=5 times 1 MiB median. Serialized sizes and all samples are reported separately.
These are implementation acceptance budgets, never body-size limits. Results do
not qualify another host or authorize deployment; independent verification follows.
