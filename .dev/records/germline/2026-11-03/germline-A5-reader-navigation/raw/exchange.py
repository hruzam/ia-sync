from pathlib import Path
import json,sys,datetime,hashlib,yaml
b=Path(__file__).resolve().parents[1]; r=b/'raw'
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def now(): return datetime.datetime.now().astimezone().isoformat()
def log(s,x):
 p=r/'runs'/s/'transcript.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('a') as f:f.write(json.dumps(dict({"at":now()},**x),ensure_ascii=False)+'\n')
def status(cp,flight,nxt,exp):
 p=b/'STATUS.md';x=yaml.safe_load(p.read_text().split('```yaml\n')[1].split('```')[0]);x.update(updated=now(),checkpoint=cp,in_flight=flight,next=nxt,expected=exp);p.write_text('```yaml\n'+yaml.safe_dump(x,sort_keys=False,allow_unicode=True)+'```\n')
x=json.loads(sys.argv[2]);s=x['subject'];d=json.loads((r/'DISPATCH.json').read_text());rows=d['attempts']; row=next((a for a in rows if a['subject']==s),None)
if sys.argv[1]=='admit':
 for path,h in json.loads((r/'FREEZE.json').read_text())['sha256'].items():assert hashlib.sha256((b/path).read_bytes()).hexdigest()==h,path
 if row is None:
  a=next(a for a in json.loads((r/'ASSIGNMENT.json').read_text()) if a['subject']==s);row=dict(**a,handle=None,request_rounds=0,deliveries=0,sends=[],replies=[],delivered_paths=[]);rows.append(row)
 assert len(row['sends'])==len(row['replies']),'uncertain prior send'
 paths=x.get('paths',[])
 if not row['sends']:msg=(r/f"messages/initial-{row['arm']}.txt").read_text()
 elif paths:
  assert len(paths)<=2 and row['request_rounds']<4 and row['deliveries']+len(paths)<=6
  assert all(p in [a['path'] for a in json.loads((r/'FACTS.json').read_text())['documents']] for p in paths)
  msg='\n'.join((r/'fixture'/p).read_text() for p in paths);row['request_rounds']+=1;row['deliveries']+=len(paths);row['delivered_paths']+=paths
 else:msg=(r/'messages/final.txt').read_text()
 assert len(row['sends'])<5
 send=dict(turn=len(row['sends'])+1,at=now(),handle=row['handle'],sha256=hashlib.sha256(msg.encode()).hexdigest(),paths=paths,bytes=len(msg.encode()),budget=dict(rounds_left=4-row['request_rounds'],deliveries_left=6-row['deliveries']))
 row['sends'].append(send);save(r/'DISPATCH.json',d);log(s,dict(direction='head-to-subject',**send,message=msg));status('Freeze verified; admission persisted in raw/DISPATCH.json.',f"{s} turn {send['turn']} admitted; native send may have occurred; no duplicate without reconciliation.",f"Reconcile native response for {s} admitted turn {send['turn']} and preserve it.",'Exact reply and handle retained; budget reconciled before any next send.')
 if len(row['sends'])==1:
  bus=b/'_bus';bus.mkdir(exist_ok=True);n=s[-2:];(bus/f'{n}.cartan.point.md').write_text(f'''cycle: '{n}'
from: cartan
to: {s}
scope: Frozen synthetic navigation task via message-mediated retrieval
paths: No file writes; receive only assigned entrance and requested shared bodies
gates: Four rounds, six deliveries, one final answer; no peers/keys/fixture reads
done_when: Final answer or exhausted/failed native attempt retained
return_to: {bus}/{n}.{s}.return.md

Exact messages: raw/runs/{s}/transcript.jsonl. Requested route: {row['model']} / low, default, fork_turns none. Parent lands native replies; subject writes no bus file.
''')
 print(msg)
elif sys.argv[1]=='receive':
 assert len(row['sends'])==len(row['replies'])+1
 if 'handle' in x:row['handle']=x['handle']
 reply=dict(turn=len(row['replies'])+1,at=now(),message=x['message'],bytes=len(x['message'].encode()),sha256=hashlib.sha256(x['message'].encode()).hexdigest());row['replies'].append(reply);save(r/'DISPATCH.json',d);log(s,dict(direction='subject-to-head',handle=row['handle'],**reply));status(f"{s} turn {reply['turn']} reply retained; {row['request_rounds']}/4 retrieval rounds and {row['deliveries']}/6 deliveries used.",'none',f"Cartan inspects {s} response and admits only its valid frozen continuation or records final scoring.",'No unanswered admission; one safe continuation or final answer recorded.');print('preserved')
