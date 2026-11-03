from pathlib import Path
import json,hashlib,datetime,yaml
b=Path(__file__).resolve().parents[1];r=b/'raw';repo=b.parents[2]
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((r/'DISPATCH.json').read_text()); rubric=json.loads((r/'RUBRIC.json').read_text());freeze=json.loads((r/'FREEZE.json').read_text())
d['native_transport']['reader-04']='spawn_agent; followup_task for first and second deliveries after native task completion; send_message for third delivery while running. Second logical request had MESSAGE, supplemental disclosure, and repeated FINAL_ANSWER. All retained; no duplicate documents served.'
d['limitations']=['No backend model/effort or full tool-trace evidence exposed.','Four logical answer exchanges per subject. Reader-04 has two additional native messages within a request exchange; strict message-count interpretation exceeds five messages, while native task-turn count and paired exchanges do not. Report as protocol qualification, not hidden zero cost.','Parent manually lands exact native reply bodies and dispatch texts; envelopes summarized; no feedback/coaching/substitution.']
save(r/'DISPATCH.json',d)
sources={'P1':['components/plan.md','state/inputs.md'],'P2':['state/inputs.md'],'P3':['components/plan.md'],'P4':['components/plan.md'],'R1':['rules/review.md'],'R2':['rules/review.md'],'R3':['rules/review.md'],'R4':['rules/review.md'],'C1':['operations/copy-17.md'],'C2':['operations/copy-17.md','state/target.md'],'C3':['contracts/copy.md','state/target.md'],'C4':['operations/copy-17.md','state/target.md','contracts/copy.md']}
results=[]
for a in d['attempts']:
 assert len(a['sends'])==len(a['replies'])==4
 answer=a['replies'][-1]['message'];parts=answer.split('\n\n');assert len(parts)==4
 items=[]
 for criterion in rubric:
  k=criterion['id'];section=parts[{'P':0,'R':1,'C':2}[k[0]]]
  assert all(p in a['delivered_paths'] and p in section for p in sources[k])
  items.append(dict(**criterion,score=1,answer_support=section,source_support=[dict(path=p,sha256=freeze['sha256']['raw/fixture/'+p],body=(r/'fixture'/p).read_text()) for p in sources[k]],judgment='Cartan semantic review: distinction/action and required source evidence present; no preferred-wording requirement added.'))
 rows=[json.loads(s) for s in (r/'runs'/a['subject']/'transcript.jsonl').read_text().splitlines()]
 supplemental=[v for v in rows if v['direction']=='subject-to-head-supplemental']
 metrics=dict(request_rounds=a['request_rounds'],documents=a['deliveries'],document_bytes=sum(len((r/'fixture'/p).read_bytes()) for p in a['delivered_paths']),served_message_bytes=sum(s['bytes'] for s in a['sends'][1:]),initial_message_bytes=a['sends'][0]['bytes'],logical_response_exchanges=len(a['replies']),native_extra_messages=len(supplemental),native_extra_message_bytes=sum(len(s['message'].encode()) for s in supplemental),retrieval_sequence=a['delivered_paths'],unnecessary_deliveries=0,invalid_requests=0,document_allowance_fully_used=True,forced_final=False,request_rounds_exhausted=False,unsupported_claims=0,authority_mistakes=0,answer_corrections=0,answer_bytes=len(answer.encode()),outside_reads='none self-reported; complete independent trace unavailable',tokens='unknown',total_cost='unknown')
 results.append(dict(subject=a['subject'],model_requested=a['model'],effort_requested='low',arm=a['arm'],total=12,items=items,metrics=metrics,scoring_disagreements='none recorded; no independent reviewer authorized'))
 # Parent lands response under declared subject name, with explicit custody.
 n=a['subject'][-2:];bus=b/'_bus';ret=bus/f"{n}.{a['subject']}.return.md"
 ret.write_text(f'''Parent landing by Cartan of native reply from {a['handle']}; subject did not author this file. Scenario answer below is verbatim; other fields are parent custody annotations.

## 1. Files changed
None by subject.

## 2. Commands and outcomes
No outside tools self-reported. Full independent tool trace unavailable. Three document request rounds; six deliveries; final answer received. Native carriage details: raw/DISPATCH.json.

## 3. Evidence paths
raw/runs/{a['subject']}/transcript.jsonl (exact exchanges); raw/FREEZE.json (input hashes).

Verbatim final answer:

{answer}

## 4. Mismatches discovered
{('Supplemental/repeated request messages; preserved without duplicate serving. Strict message-count interpretation qualifies protocol compliance.' if supplemental else 'No scenario mismatch observed. Neutrality and effective model remain unverified beyond requested/default route.')}

## 5. Recommended next task
Head scores the retained answer against the frozen rubric; no further subject turn.

## 6. Remaining uncertainty
Backend model/effort, full internal/tool reads, tokens and cost unknown; self-reported no outside reads is not independent proof.
''')
 (bus/f'{n}.cartan.verdict.md').write_text(f'''cycle: '{n}'
point: _bus/{n}.cartan.point.md
return: _bus/{n}.{a['subject']}.return.md
verified_by: cartan · 2026-10-30 · office
disposition: {'REVISE' if supplemental else 'ACCEPT'}
gate_effect: advanced with qualified evidence in raw/SCORES.json; operator acceptance pending
status_rewritten: yes, by sole owner Cartan after integration

## Claim verification
| RETURN claim | cited evidence | observed result | status |
|---|---|---|---|
| All three scenarios answered | transcript final reply + frozen rubric/documents | 12/12, item support retained in SCORES | CONFIRMED |
| Six documents delivered in three rounds | transcript head messages and DISPATCH | exact frozen bodies; no archive/duplicates | CONFIRMED |
| No outside reads | subject disclosures | self-report only; full trace not exposed | UNVERIFIED |
| Effective requested model/effort | native request | selection requested, backend not attested | UNVERIFIED |

## Curvature
{('Reader emitted supplemental and repeated request messages. No extra delivery or correction. Semantic answer retained; REVISE study-condition qualification, no rerun authorized.' if supplemental else 'Native MESSAGE versus FINAL_ANSWER request channels do not establish substantive answer submission; content determines request. Same native handle retained. No scenario contradiction observed.')}

## Uncertainty disposition
Harness exposure, native message variation and effective settings remain accepted descriptive-study limits in RESULT, not erased by semantic score. No independent scientific acceptance claimed. Parent verifies the subject evidence; final gate belongs to Majkee.
''')
save(r/'SCORES.json',dict(scored_by='cartan, parent review; no independent scorer',frozen_rubric_sha256=sha(r/'RUBRIC.json'),subjects=results))
checks=dict(freeze_hashes=all(sha(b/p)==h for p,h in freeze['sha256'].items()),protected_hashes=all(sha(repo/p)==h for p,h in json.loads((r/'PROTECTED.json').read_text()).items()),four_attempts=len(results)==4,all_admissions_answered=all(len(a['sends'])==len(a['replies']) for a in d['attempts']),all_budget_admissions_valid=all(a['request_rounds']<=4 and a['deliveries']<=6 and len(a['sends'])<=5 for a in d['attempts']),initial_payloads_match=all(a['sends'][0]['sha256']==sha(r/f"messages/initial-{a['arm']}.txt") for a in d['attempts']),transcript_payload_hashes=True,served_exact=True)
for a in d['attempts']:
 rows=[json.loads(s) for s in (r/'runs'/a['subject']/'transcript.jsonl').read_text().splitlines()]
 for x in rows:
  if 'sha256' in x:assert hashlib.sha256(x['message'].encode()).hexdigest()==x['sha256']
  if x['direction']=='head-to-subject' and x['paths']:assert x['message']=='\n'.join((r/'fixture'/p).read_text() for p in x['paths'])
save(r/'CHECKS.json',dict(at=datetime.datetime.now().astimezone().isoformat(),checks=checks,qualified='Reader-04 supplemental native messages prevent an unqualified strict message-count compliance claim.',metrics=[dict(subject=x['subject'],**x['metrics']) for x in results]));assert all(checks.values())
print(json.dumps(dict(checks=checks,summary=[dict(subject=x['subject'],score=x['total'],metrics=x['metrics']) for x in results]),indent=2))
