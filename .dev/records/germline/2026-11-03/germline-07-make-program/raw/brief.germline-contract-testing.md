# Contract testing — reusable method candidate

2026-10-21 · requested by Majkee · documentation only, uninstalled.

General techniques here reflect learned engineering practice. No specific training
document or external research was retrieved as their origin. In the worked case,
expected results came from the approved v4 contract, 19 pinned references/four exact
corpus slices, review requirements and observed failures. Generated cases are
authored examples; generating them does not make them independent verification.

## Procedure

1. **Fix the task inputs.** Record contract/version/hash, owned files and allowed
   side effects, callable API and real entrypoints, reference identities/slices,
   accepted limitations and acceptance criteria. Set performance budgets, host,
   timing boundary, sample count and statistic before measurement. Surface contract
   ambiguity before inventing a default.
2. **Derive witnesses from rules.** For each material rule, choose a valid example,
   a violating example and relevant boundary combinations. Include precedence when
   two rules fail together. Write expected values, bytes, coordinates, ordering and
   exit status from the contract or frozen source facts, independently of the code
   under test. Do not obtain a golden by asking that same implementation what is
   correct. Generated combinations extend coverage; they still need reviewed oracles.
3. **Check the logical contract.** Exercise the API directly. Where preservation
   matters, compare exact bytes and original spans, including encoding, line endings,
   empty data and boundary positions. A round trip alone can miss a wrong shared
   boundary: also compare the extracted piece to the independently pinned source.
   For an all-or-nothing result, corrupt a later part after a valid prefix and prove
   that no usable partial result survives. Repeat diagnostics to check determinism.
4. **Exercise actual boundaries.** Run the installed/source entry actually being
   claimed, with explicit input, an unrelated cwd and relevant environment variants.
   Assert stdout, stderr, status, input preservation and observable side effects.
   Check operational failures such as missing input and a failing output sink,
   including buffered flush/shutdown. Logical checks or mocked wiring alone do not
   establish functional behavior. For inert input, combine literal command-looking
   text, absent sentinels, unchanged-file checks and call-path inspection; mocks
   supplement these observations rather than proving an OS sandbox. Give hostile
   environment/sentinel probes a positive control so a broken probe cannot pass.
5. **Measure the promised path.** Generate fixtures before timing; then include the
   complete required startup/I/O/work/output boundary. Save every sample, input size
   and hash, runtime/host, command, environment and criteria identity. Recompute the
   declared statistic. Fail against the original budget; preserve that run and
   authorize a bounded correction before rechecking. Do not rerun until green,
   subtract startup or qualify an unmeasured host by analogy.
6. **Separate the judgments.** The author supplies implementation and evidence. A
   fresh verifier reads the contract, reproduces declared checks against identified
   bytes and adds independently derived probes. Reusing an author's suite is
   reproduction; it does not turn its cases into independent designs. The
   integrating head checks returned artifacts, scope, claims and remaining gates.
   A report without executed evidence is not a functional acceptance finding.

Scale checks to material risk. A documentation-only edit may need just a diff,
pointer and provenance check; this method does not require a large suite for it.

## Invocation and return contract

An existing verifier/program can receive this brief-shaped task; no implicit
loader, new persona, controller or universal framework is required:

```yaml
objective: <observable transition and acceptance decision>
contract: <version/hash; rules and accepted limitations>
ownership: <read/write scope; side effects allowed and prohibited>
interfaces: <API plus actual command/wiring to exercise>
references: <immutable identities, exact slices and expected-outcome derivation>
cases: <positive, negative, boundaries, precedence, operational failures>
measurement: <host, full timing boundary, samples/statistic, fixed budgets or none>
evidence: <new empty destination per authorized run; temporary-write scope>
return: <PASS/FAIL/unverified; commands, observed vs expected, artifact hashes,
         preserved failure/correction links, limitations and remaining gate>
roles: <author; fresh verifier; integrating head>
```

Before handing back, link the contract-to-case reasoning, exact commands/exits and
output comparisons, input/source identities, side-effect observations, all timing
samples and a finding bounded by what ran. Preserve failed runs and link each fix
to its recheck. **Future retests require fresh evidence destinations:** recorded
old commands document past runs and do not authorize overwriting their files.

For later reviewed promotion, the general procedure could become a method of an
existing verifier/program or a shared vendor-neutral skill. Reusable executable
tooling can be parameterized when repeated needs justify it; concrete grammar
fixtures and expected diagnostics stay with their parser. This candidate creates
no germline primitive and installs nothing.

## Worked example and evidence — Termbrana Phase 0

Source/tests: [/home/hruzam/ia-sync/zsh/termbrana/](/home/hruzam/ia-sync/zsh/termbrana/).
Evidence links below are historical records; no tests were rerun to write this brief.

- [Approved v4](grammar.builder.v4.md), SHA256
  `a977682c65bcd6b3c66cc67cb7c2b40a926cf4d96a7f58eb50f1a1fb0839b2ec`,
  plus [corpus inventory](corpus-inventory.cartan.json): four bodies total 38,799
  bytes; journal extent [2061,16595). Contract cases include LF-only physical lines,
  BOM byte positions, first-closer precedence, five required fields, removed-key
  rejection and invalid-document packet suppression. Reference corpus bytes are
  fixed evidence; generated wrappers/negative variations are authored cases.
- [Head draft observation](head.pre-return-checks.phase0.md): valid parse output
  redirected to `/dev/full` exited 120 with Python shutdown-flush prose, violating
  operational exit 74. Flushing inside the error boundary and handling the failed
  sink corrected it. The [actual-source head recheck](head.output-failure.source-check.json)
  records both valid parse and invalid check output failures returning 74 with fixed
  safe stderr; the unit suite retains this regression. A happy parse had not tested
  the real CLI's output-failure contract.
- Builder performance history remains [first failure](implementation.phase0/benchmark.first.json)
  (corpus p95 151.972688 ms), [import correction failure](correction.phase0/benchmark.json)
  (101.100023 ms), then [isolated-entry pass](startup.phase0/benchmark.json)
  (90.669896 ms), all against 100 ms. No failed result was replaced or budget relaxed.
  Final builder [summary](startup.phase0/summary.json): 27 unit methods, 62 byte
  comparisons and 38 CLI cases twice. Entry tests also compare clean/isolated output
  parity; that equivalence check alone is not an independent validity oracle.
- Fresh verifier [finding](verification.phase0/verifier.finding.md) and
  [additional probe report](verification.phase0/edge-report.json): independently
  reproduced 27/62/38-twice and added 33 derived probes. Its
  [benchmark](verification.phase0/declared/benchmark.json) passed corpus/1 MiB/4 MiB
  p95 92.968602/89.864265/106.243155 ms against 100/500/2000 ms, median ratio
  1.839460 against <=5; 30 fresh full zsh/Python invocations per input, p95 sorted
  index 28. Office host hruzam-120922, Python 3.14.7 only; home and larger resource
  exhaustion remain unverified.
- [Head acceptance](../_bus/26.cartan.verdict.md) checked the fresh finding, source
  hashes, all 62 output pairs and statistics from 90 samples, without another
  benchmark. It accepted Phase 0; deployment and later phases stayed outside scope.
  [Germline placement context](/home/hruzam/ia-sync/germline/README.md) describes the
  reviewed shared source; this brief remains a candidate in evidence.
