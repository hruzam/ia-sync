---
kind: documentary-fixture-inventory
date: 2026-11-13
author: cartan
controller_thread: 01a1d58a-3b43-7221-bf9b-fa98b219df6b
source_revision: 511b7a2af7776102f66834b74636c3abba757647
accepted_report_revision: 3584a02d5be8dd2f0a1168e9e2b39621a747b9d8
accepted_report_sha256: dc219b62e304b48f02c98117f258b25be0a86061520ed289892f17a337e72d39
availability_observed_utc: 2026-11-13T17:44:04.105203+00:00
status: documentary inventory; independent review recorded separately in _bus/
---

# VIST offline fixture inventory — six documentary rows

This inventories existing evidence for the six rows of P13. It performs no replay, classifier invocation, carrier attempt or new native experiment. Observation, controller interpretation/decision, actuator attempt and receiver receipt are analytical columns here, not an adopted event envelope or a grant of delivery authority.

The accepted report is P0, independently checked by P11 and accepted as reporting evidence by P12. The report frontmatter and P13's “review16 pending” wording predate that acceptance; they do not reopen it. The original all-cases requirement remains **PARTIAL/OPEN**, and **Majkee GO/STOP remains OPEN**. Prototype release, X0, room protocol adoption and shared-layer implementation/activation are outside this unit.

## Corpus and custody

All P references resolve under `/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/` at the explicit Git revision below. SHA256 hashes are over exact Git blob bytes, not the current working file. P0's live bytes were also checked against its accepted hash. P1 carries preregistrations and observed r1/r2/r3 tables; row references below name those sections rather than treating every historic statement as current.

R1, R2 and R3 are **private local evidence roots**, respectively:

- R1 = `/tmp/vc08r1.tkz50zbf/`
- R2 = `/tmp/vc08r2.kk50sqqh/`
- R3 = `/tmp/vc08r3.j6lgeedf/`

All 37 selected files in the local pin table were readable at the observation UTC above. That is a point-in-time home-host availability observation, not cross-host custody, redaction approval or a claim that these files are durable fixtures. The inventory publishes metadata and hashes only. It does not copy private frames, tool transcripts, native histories, settings backups or credential material.

A portable prose extract can support documentary interpretation without constituting an independently annotated native replay fixture. Every row below therefore distinguishes its available sources from the fixture still missing. None of the inventory rows receives a new experimental PASS.

## Runtime and build pins

- r1 helper = P6 (`06cc9b4`), signatures P9. r2 = P7 (`22d5008`), signatures P10. r3 = P8 (`37887e7`), unchanged r2 signatures P10, as frozen in P1's r3 preregistration. Use commit and content hash: the source header still says “v2”, while the r3 build card `_bus/08.trajectory.build-r3.md@511b7a2` calls P8 “v3.1”.
- P1 “Observed source identity” records **installed probes** Codex0.169.0 and Claude2.1.323 on Nov13. Those probes do not prove the executable version of every already-running process. The selected frame metadata has no executable-version field.
- r1 Claude identity in selected metadata: PID183856, session `f98f955d-f706-4bdc-b993-08c8f21187b7`. The r2 default-mode relaunch is PID385465, session `81e509d3-0774-4fae-a0ae-61ea1e76bdcf`; C05/C13 predate that relaunch. P1 records actual permission-tool models Haiku5.5 for pwd and Opus4.8 after fallback for the approval-producing call; it is not a same-model pair.
- r1 Codex PID189655/thread `01a1d496-8940-7941-9d4b-97564cb5fd22` is retired in C02. Rebound r2/r3 sample PID356560/thread `01a1d4de-ecc1-75d1-ab32-03caf35f72a7`, GPT-6-Luna, is a distinct lifetime. R3/baseline.json includes a sample process-start-tick field; earlier selected .meta files do not.
- q01 occurred Nov12: P2 gives the receiving-turn start at12:57:33Z. Its sender verdict `_bus/05.trajectory.verdict.md@511b7a2` is dated Nov13, which is not a new delivery date. A research note `reports/cartan.codex-channels.2026-11-12.md@511b7a2` probes CLI0.167.2; event-time executable-version proof is not present in P2. q02/q03 occur Nov13 at11:05:00.951Z/11:13:14.453Z; `_bus/06.trajectory.verdict.md@511b7a2` records CLI drift to0.169.0. Do not assign one executable version to all three receiving events.

All event times below are UTC; Nov13 means2026-11-13 unless Nov12 is explicit. File mtime is not used as an event timestamp.

## Row 1 — Observation versus decision/action

**Available evidence:** P1 r1 C04 `c08r1-04-90c4f4e6` and r2 C04 `c08r2-04-19820a5b`; R1/R2 results and Codex receipt extracts, busy frame/meta pairs, and R2/04-after.meta.

**Observation:** r1 queued at12:08:11Z while the first native setup task remained active until12:08:16.549Z. The helper recorded ready during active work. r2 accepted at12:31:23.777Z, with its setup turn completing12:31:28.041Z and the receiving user event at12:31:28.102Z. The corrected attempt observation recorded busy.

**Interpretation/decision:** the r1 ready classification failed its observation expectation; queue capability did not establish native idle. In particular R2/04-busy-before.meta still contains the prior attempt's ready value at12:31:23.431Z, before the corrected acceptance observation. A window option is a last observation, not a continuously sampled native truth.

**Actuator and receipt:** each test's queue acceptance is separate from the later native receiving turn/final. r1 final12:08:22.194Z and r2 final12:31:32.930Z do not retroactively make the earlier classifier correct.

**Independent oracle and missing fixture:** P1's correlation can be checked against the result/receipt extracts and timestamped private frames. Still missing: a portable redacted/annotated timeline with the native active interval, helper observation, decision and carrier event independently aligned. Hashing raw frames does not supply that annotation or qualify the heuristic universally.

## Row 2 — Busy versus queueable

**Available evidence:** the r2 C04 sources above plus P2/P3/P4 ordinary receiver receipts and sender verdicts05/06/07 at511b7a2.

**Observation:** an active Codex sample accepted queued work, then consumed it after the first task completed. q01/q02/q03 document three separately correlated ordinary receiving turns; those receipts describe the controller as idle before their arrival. They are not three additional busy tests.

**Interpretation/decision and actuator:** “queue accepted” permits a carrier-result statement only. Sender invocation and receiver turn are separate sources. No forced resume, second live writer or cross-host behavior is established by this inventory.

**Receipt/oracle:** match each sender queue event and exact receiver turn/nonce rather than inferring consumption from exit0. q01's native date is Nov12 despite the later verdict date. Accepted ordinary counts remain inherited from the reviewed report; this unit does not redo the complete native-history count audit.

**Missing fixture:** a single redacted, event-aligned busy/acceptance/consumption packet with event-time executable identity and independent annotations. The q receipts are portable extracts; their referenced complete native rollout was not selected, copied or newly hashed here. No universal queue or latency/reliability guarantee.

## Row 3 — Draft, approval and disclosed intervention

**Available evidence:** P1 r1 C08/r2 C05/C06/C07/C09; R1 draft-before/preserved pairs, R2 C05 draft/after metadata and receipt, R2 Bash approval-before/after pairs, permission-tool extract, Read grant, C07 receipt and post-return Bash approval record.

**Observation:** r1 C08 remained occupied for the bounded wait and refused31 at12:09:27Z; draft preservation is recorded. r2 C05's draft was deliberately removed only after preservation was witnessed; submission12:34:03Z and final12:34:05.839Z followed. Its fresh success does not retire r1 C05's uncertain27 at12:11:00Z or authorise retrying that ID.

**Decision/actuator:** the approval delivery C06 refused31 without input, marker absent, at12:55:30Z; the native Bash tool had been requested at12:52:47.103Z. Timeout was not approval or execution. C09's actual pwd call/result at12:47:25.416Z/12:47:25.849Z does not identify which rule permitted it.

**Receipt/intervention:** C07's pointer was submitted12:40:50Z; its nonce answer12:46:33.557Z followed the persistent local Read grant at12:46:27.847Z (native option2). The later one-time Bash option1 at13:10:46.716Z and tool success13:10:46.927Z are separate operator acts. Neither is unattended success, and sample results add nothing to senior ordinary counts.

**Oracle and missing fixture:** independently compare exact draft bytes/cursor before and after, observed native prompts, tool outcome, matching receipt and the two distinct grants. The selected raw pairs and JSON extracts exist locally; portable redacted comparison/annotation fixtures remain missing. Actual-model fallback and dated mode/grant scope must survive any extraction. Nov13 senior-seat permissions remain explicitly unverified operator/author accounts in P0; these sample fixtures cannot establish parity.

## Row 4 — Unknown versus registered dialog

**Available evidence:** P1 r1 C10 `c08r1-10-0c0e00f2`, r2 C13 `c08r2-13-42cd0f20`, P9/P10 signature inventories, R1/10-help-view and R2/13-help frame/meta pairs plus results.

**Observation:** real /help was read as needs_approval in r1; it returned31 instead of the expected unknown29, without carrier input. Its metadata capture is12:05:19.485Z. In r2 /help is a registered dialog: dry/hop1 classification waited five times and returned31 after5.458s (12:32:34.022Z–12:32:39.480Z). Frame metadata is12:32:34.017Z.

**Interpretation/decision and receipt:** the registered help regression is evidence about dialog discrimination, not a passed unknown-surface test. No receiver consumption is expected for either refusal; “no carrier input” is the relevant source predicate.

**Oracle and missing fixture:** compare annotated actual frame with its frozen signature set, then result/no-input evidence. **Genuine unregistered native-view fixture remains MISSING/UNQUALIFIED:** version and lifetime binding, before/after frame metadata, redacted unsupported view, signature hash, refusal29 and no-carrier proof are absent as a correlated packet. C13 cannot substitute; no synthetic screen is introduced.

## Row 5 — Rebuilt pane and native session identity

**Available evidence:** P1 C02 and r2 rebind preregistration/results; R1/02-alive-before.meta, 02-dead-before-deliver.meta, 02-after.meta; R2/new-codex-bound.meta; P5 turn10 identity snapshot; P0 cycle09 callback22 table. r1 dead-before-delivery capture12:10:17.814Z and post-delivery12:10:17.922Z are both already dead, not an alive/dead pair by themselves. The earlier alive metadata is a separate selected file.

**Observation:** C02 retains the dead sample pane and refuses21, without resume/carrier. r2 rebind records a new PID/native thread; cycle09 callbacks later refuse22 on shell-rooted Codex panes%23/%47. P5 is a later timestamped inventory, not a lifetime bridge back to C02.

**Interpretation/decision and actuator:** pane numbers and labels are insufficient lifetime authority; dead/non-agent refusals are not delivery failures to repair by guessing or relaunching. Existing dead/rebound observations establish only their stated instants.

**Oracle and missing fixture:** **complete rebuilt-pane replay remains MISSING/UNQUALIFIED**: one correlated chain old native identity → retirement → relaunch → new PID/start identity/session → routing result, with same-instant inventory evidence at each transition. Earlier selected .meta files lack start ticks/executable versions; R3's later start-tick field does not fill the earlier chain. No rebuild or target input was performed for this inventory.

## Row 6 — Failure notice, carrier result and consumption

**Available evidence:** P0 cycle09, P1 r2 C12/C12b and r3 C12, R2 results/receipt extracts, R3 receipt/baseline/parent/observation records; selected existing cycle09 delivery-log terminals below.

**Observation/decision:** cycle09 parent messages `20261113T-a09nablarva-cartan` and `20261113T-a09cartan` refused29 at15:49:07Z/15:50:07Z on recipient Trajectory; their .n callbacks refused22 at15:49:08Z/15:50:07Z. Ack files record29, not22. No such refused callback establishes consumption.

**Actuator versus receipt:** r2 C12 logs spawn but no child attempt/receiving turn within budget. C12b conditionally queues with caller held10s; final about41s is late. Fresh r3 parent20 returns immediately at13:14:06.492236Z; child acceptance is separate from native turn start+0.325s, notice read+3.916s, final+7.852s. The sender role in that sample test was verifier-orchestrated, not a spontaneous senior's failure/recovery loop. No second-hop notice was observed within the recorded bounded check; this does not prove arbitrary semantic/hop enforcement.

**Oracle and missing fixture:** compare parent/child selected events with native notice-read and matching final, not spawn or queue exit alone. R3's selected receipt permits documentary correlation; a portable redacted multi-event replay packet with independently annotated sources is not yet assembled. Specific process-group/client-selection causes remain hypotheses. Expiry, misaddress, real receiver semantic/hop limits, and real post-text exit/crash coverage remain unqualified despite this inventory.

The local mutable log is `~/.local/state/vist/deliver.log`. Selection predicate: event=refused and msg exactly one of the two a09 IDs above or their .n IDs; preserve original file order and each line's trailing newline. At inventory time the selection had **4 lines, 587 bytes**, SHA256 `2e21099d632fc59810b8ed56db0bee1ae126fdb261fdf1584b8e774a96928c71`. This pins the selected terminal slice, not the entire appendable log. Log payloads remain local.

## Redaction and missingness record

| Source class | Current inventory treatment | Before portable replay use |
|---|---|---|
| P Git sources | Existing published prose/metadata; exact commit and hash retained | Cite the selected scope; do not treat historical PASS as a new replay |
| Local .meta | Names, file hashes and relevant UTC/lifetime fields only | Annotate field grammar and stale-option semantics; disclose absent executable/start-tick fields |
| Local .ansi | Hash/availability only; private full screens remain local | Produce and inspect minimal redacted frames preserving relevant styling/cursor/geometry; record transformation and output hash |
| Local result/receipt/tool JSON | Whole-file hashes; only scoped event interpretation reported | Select correlated events and remove unrelated context/tool output; record source offsets/selection and output hash |
| Local grants | Read/Bash interventions described separately; settings backup excluded | Retain exact grant scope/mode/model/time necessary to interpret the case; exclude unrelated settings/secrets |
| Complete histories, credentials, tokens, settings backups | Not selected, copied, published or assigned fixture status | No requirement to publish them; extract only the minimum authorised evidence locally |

Missing redacted/annotated fixture packets are explicit gaps, not a new operator-approval gate for this already-authorised documentary unit. This artifact inventories what can be interpreted now and what must still be qualified before replay claims. Durable preservation of /tmp originals outside this inventory is **not established**. No selected private fixture is silently promoted into a shared repository.

## Portable source hashes

| ID | Revision and bed-relative path | Bytes | SHA256 |
|---|---|---:|---|
| P0 | `3584a02:reports/trial-report.vistmini-01.md` | 11963 | `dc219b62e304b48f02c98117f258b25be0a86061520ed289892f17a337e72d39` |
| P1 | `511b7a2:reports/cartan.cases-08.2026-11-13.md` | 56851 | `363850b7da8cb2e2347ac9395c72de9837248a3aecdabbb1b2655601ad6b79cf` |
| P2 | `511b7a2:reports/trial-msgs/q01.cartan.receipt.md` | 2678 | `7aae0b99f9216ad453b5b48ed77cf36ad9452ae100dcdec4237dc879f200be93` |
| P3 | `511b7a2:reports/trial-msgs/q02.cartan.receipt.md` | 1796 | `b0369e4e08e9e3f62db26a088acfc9d1684fb4f8a7d464e6a8f4448161a8192c` |
| P4 | `511b7a2:reports/trial-msgs/q03.cartan.receipt.md` | 1542 | `88a90eec2fd5f91fb9eadbaf3126c078bc5a263a6f7ebd1c9111fae77617351f` |
| P5 | `511b7a2:reports/10.context-observation.json` | 1786 | `4efc61ec64995576b15156e63d9bb5f1d050e8ef3eb31970964fae1f1901d12e` |
| P6 | `06cc9b4:scripts/vist-deliver.sh` | 9291 | `f6eb1c2848883e2760fad23ac41704acd5cf437f23715915ccc6593bd1322894` |
| P7 | `22d5008:scripts/vist-deliver.sh` | 10740 | `c8935790c6d6c3d05e2eaade44e7a66b44e0588dbc511d0118260a427fb6b13f` |
| P8 | `37887e7:scripts/vist-deliver.sh` | 10875 | `5516d92f6a65d8a464ec266b80e483b6c923873e8634167085408fef7175b6b7` |
| P9 | `06cc9b4:scripts/vist-signatures.conf` | 695 | `39040d20dd83675636f021e314a9df240c482646fcda716c1f37c17a50fecda6` |
| P10 | `22d5008:scripts/vist-signatures.conf` | 789 | `235fc96c7df0abb568e4550394cf6d2ee51198c4357b6b8a166c33464f7491f8` |
| P11 | `511b7a2:_bus/16.next-cartan.return.md` | 3227 | `050a5dafe33cdce693f990ec9a7fea123d4c352cec3c9152df0985e71faee066` |
| P12 | `511b7a2:_bus/16.cartan.verdict.md` | 457 | `a14ec4890c82f053bc0b6888eec59f978668bf8d9ca2fd0a34b0bc8d08b9dc67` |
| P13 | `511b7a2:reports/vist.offline-qualification-proposal.2026-11-13.md` | 3723 | `71634d527a9e9c6faa57d3a9ca7c6bcc2142e355b3b4722fe3aacd3eb08ec059` |

## Local availability and content pins

All selected files below were available/readable at the observation UTC. Root prefixes are defined above; hashes name private input bytes, not redacted output artifacts. Full screens and raw JSON contents are not included here.

| Root/file | Bytes | SHA256 |
|---|---:|---|
| `R1/results.jsonl` | 15255 | `e2778f5aeb1cd837e7485573940fcfe2c33b940583e9988ccee41a00406c05cf` |
| `R1/codex-receipts.json` | 1382 | `43b6971dac2547c2bf91d97782ad7595b8f889270d3825fd5b644bee5baef799` |
| `R1/04-busy-before-queued.meta` | 162 | `57c466f793c75774369f4ac2aeb6625043eee4f411e40d94f2e2e77faeb890d8` |
| `R1/04-busy-before-queued.ansi` | 1539 | `87fc92e291980013c4ae9a5d08b3fe809a52a6aec43f7ccf70dbad65815ec044` |
| `R1/08-draft-before.meta` | 168 | `9f3ad3f8ae5aa29f0353e6ec83afc7e54f3fb91e23acc5fd430dde7737f6719a` |
| `R1/08-draft-before.ansi` | 3192 | `b1d14e0785e5a9dad5607cca5b529f560b4054f80cf111b9c4e45c331a1570bd` |
| `R1/08-draft-preserved.meta` | 162 | `1b4bfcf5ea3703fbc52026786b65633a9ae78a50582f847e597ec416b9df12f1` |
| `R1/08-draft-preserved.ansi` | 3192 | `b1d14e0785e5a9dad5607cca5b529f560b4054f80cf111b9c4e45c331a1570bd` |
| `R1/10-help-view.meta` | 112 | `8dcfb247c75ff6fdf1061eb7bd30f61ba33b663bc2078e9ff1d8697ee497c61d` |
| `R1/10-help-view.ansi` | 4010 | `b59d850bbb9e89990e2170f63ce79767410d01362b6ce9901d06b10a8f62474a` |
| `R1/02-alive-before.meta` | 156 | `f4ee88672cf001d76c181a12e387a458de0f3dfdacf01de3180d5d7346639276` |
| `R1/02-dead-before-deliver.meta` | 156 | `94a15e1a787406aff6bb1fa24bc8587fa13c98da6a39a1b80e4f847649c99d52` |
| `R1/02-after.meta` | 156 | `41f1bef2e7a8fac94f69edf122768386f4a9d3f8b8647a92433d1cc69d1ee61c` |
| `R2/results.jsonl` | 16603 | `3dbbb0d66b1c51b58806de9314796227171ba06a48ebc977bd3959374224fccc` |
| `R2/codex-receipts.json` | 1215 | `de083ee61e4244863d32f034f9fdca4aa90f8156a5a912c6a6b3a6840c909587` |
| `R2/04-busy-before.meta` | 162 | `019a3fb5ebaf35ae6e05b4ec0a37def4d0ce8a047c764b91299cd395eada2845` |
| `R2/04-busy-before.ansi` | 2171 | `be49045bf85b04d6aeb6356527a9cf794c8760f79cebfdd4b5c0d8302fb67c94` |
| `R2/04-after.meta` | 155 | `5f5ffdd8dc2898988b011f5cb63a7d99920fe2c3faf22ef17d1a61336d5cddb2` |
| `R2/05-draft-before.meta` | 160 | `b98839ef7c40a6e8332e6376dcba46ca0c8e1b2b0079590cad4d53b31114402b` |
| `R2/05-draft-before.ansi` | 2481 | `8ebbfb8c5f7325bc5efc64ce4df3222176809c5b996894094965009ca929608f` |
| `R2/05-after.meta` | 160 | `288045be0728295ab4823b66141dc7e98df1d11ca2a628ae3fc7669e0a3ca054` |
| `R2/05-claude-receipt.json` | 403 | `3785b1236cbe9256a3c4f90d5cffc78210ac23a1d8b9b026575f1af458493808` |
| `R2/06-bash-approval-before.meta` | 166 | `2e5cf587713cfe88ec4be177b476727a0e8088377aacc7b465b11491ffbe4abf` |
| `R2/06-bash-approval-before.ansi` | 4077 | `6921537d9230e9199f42a8a30c43cfd3bc350ce7bace4a0ae0a0bde74e500ed7` |
| `R2/06-bash-approval-after.meta` | 167 | `8a2fa8dc7875b9c57051becc15751d3db586490c9105c1546f1229dbf3b3b94b` |
| `R2/06-bash-approval-after.ansi` | 4077 | `6921537d9230e9199f42a8a30c43cfd3bc350ce7bace4a0ae0a0bde74e500ed7` |
| `R2/permission-tool-evidence.json` | 725 | `450c12be0321c94420263fb020232d951525b33101f805a78f7a2d5e5529448f` |
| `R2/operator-read-grant.json` | 286 | `2bec6b8af41a705e9b1b731e12e48006109cb4fd6dbf807562b124932c150c24` |
| `R2/07-default-receipt.json` | 346 | `b566e005ae31f72ae5ecd625d0966931c602d34dd943c1d62a682209da4d3af6` |
| `R2/post-return-bash-approval.json` | 4374 | `31359a12ef6dcd0bd454d9bcb5400abacc3ef581036b0f20c7cdfbbf0070ca70` |
| `R2/13-help.meta` | 163 | `c3f17caa56eee2ff12a3b728bb99912466a50baa1e74750c5edaf9703eb461ae` |
| `R2/13-help.ansi` | 2985 | `7b27268aca7df10ef10a3ca6d097f67091c6c66637d5155eb010b97e854a683c` |
| `R2/new-codex-bound.meta` | 113 | `77028960fd216cb12d0e15fdcfc35f8a89cf506cdb5863ed02d46a082e38e210` |
| `R3/receipt.json` | 2011 | `6566baec7354e7e44adbd9bc39b8c5ead0d905184d8b8013a1fb69f753f5e2ce` |
| `R3/baseline.json` | 275 | `0b3d499289c63bca15f811a99e0f40945ecfa29ad7f7fd2faf42e5b996fee2ed` |
| `R3/parent-result.json` | 263 | `6c37e0c71aafe459e9b52f38758dc36bbc8eca3538dabb1be50445367e7f56a9` |
| `R3/observation.json` | 189 | `911b97989fa60b4d3475f0fe75907150170b30c01ee74634a49b8ce9a60365e7` |

## Review and gate boundary

An independent reviewer must verify this exact artifact hash, recheck the P pins and selected local pins, inspect the six interpretations against their cited sources, and ensure missing evidence never becomes PASS. Its POINT/RETURN/VERDICT in _bus/ are the acceptance record; this inventory does not self-certify review completion.

Packet completeness, runtime qualification, original trial acceptance and actuator release are separate conclusions. At this documentary edge the all-cases requirement and Majkee GO/STOP remain OPEN; no X0 or new shared-layer authority is inferred.
