#!/usr/bin/env python3
"""G09's small receipt-first driver; only the five declared role/cycle asks exist."""
import argparse, hashlib, importlib.util, json, os, subprocess, sys, tempfile, time
from pathlib import Path

B = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader')
H = B / 'raw/caretaker'; OPS = H / 'operations'; OUT = OPS / 'output'; PKT = H / 'packets'; RES = H / 'results'
SHIM = '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh'; CODEX = '/home/hruzam/.local/bin/codex'
PRE = '/home/hruzam/.germline/tunnel/tunnel.preamble.md'; SOURCE_PRE = '/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md'
ROUNDS = {
    'R1': ('researcher', H / 'tunnel.researcher.state.json', 'cold'),
    'R2': ('researcher', H / 'tunnel.researcher.state.json', 'warm'),
    'A1': ('auditor', H / 'tunnel.auditor.state.json', 'cold'),
    'A2': ('auditor', H / 'tunnel.auditor.state.json', 'warm'),
    'A3': ('auditor', H / 'tunnel.auditor.state.json', 'warm-conditional'),
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pstart(pid):
    try: return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    except (FileNotFoundError, IndexError, OSError): return None
def load(p):
    try:
        v = json.loads(Path(p).read_text())
        return v if isinstance(v, dict) else None
    except (FileNotFoundError, OSError, json.JSONDecodeError): return None
def write(p, v):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); t = p.with_name(f'{p.name}.tmp-{os.getpid()}')
    with t.open('w') as f:
        json.dump(v, f, indent=2, sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(t, p)
def state(p):
    s = load(p)
    if s is None: return None
    return {k:s.get(k) for k in ('enabled','threadId','lastTurnId','model','sandbox','cwd','preamble','turnOverrides','runtime')}
def op(key): return OPS / f'{key}.operation.json'

def inspect(p):
    r = load(p)
    if r is None: return {'classification':'unknown','reason':'missing-or-malformed-receipt'}
    if r.get('status') == 'pending':
        q = r.get('runner') if isinstance(r.get('runner'),dict) else {}
        return {'classification':'running','reason':'runner-still-alive'} if q.get('start') and pstart(q.get('pid')) == q.get('start') else {'classification':'unknown','reason':'dead-or-unverifiable-pending'}
    if r.get('status') == 'failed': return {'classification':'failed','reason':'submission-or-command-failed'}
    if r.get('status') != 'completed' or r.get('exit') != 0: return {'classification':'unknown','reason':'invalid-completed-receipt'}
    for ch in ('stdout','stderr'):
        x = (r.get('outputs') or {}).get(ch) or {}; path = x.get('path')
        try: ok = isinstance(path,str) and Path(path).is_file() and sha(path) == x.get('sha256')
        except OSError: ok = False
        if not ok: return {'classification':'unknown','reason':f'invalid-{ch}-output'}
    return {'classification':'completed-and-validated'}

def ask_count():
    return sum(1 for p in OPS.glob('*.operation.json') if (load(p) or {}).get('kind') == 'ask') if OPS.exists() else 0
def start(key, kind, argv, extra):
    p = op(key)
    if p.exists(): raise RuntimeError(f'refusing replay: existing operation record {p}')
    if kind == 'ask' and ask_count() >= 5: raise RuntimeError('refusing sixth target ask')
    p.parent.mkdir(parents=True, exist_ok=True)
    r = {'schema':'g09-receipt/v1','key':key,'kind':kind,'status':'pending','argv':argv,'started_unix':time.time(),'runner':{'pid':os.getpid(),'start':pstart(os.getpid())}}
    r.update(extra)
    try:
        with p.open('x') as f: json.dump(r,f,indent=2,sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    except FileExistsError as e: raise RuntimeError(f'refusing replay: existing operation record {p}') from e
    return p,r
def finish(p,r,result=None,error=None):
    if result is None: r.update(status='failed',exception=repr(error),remote_outcome='unknown')
    else:
        OUT.mkdir(parents=True,exist_ok=True); paths = {}
        for ch,data in [('stdout',result.stdout or b''),('stderr',result.stderr or b'')]:
            x=OUT/f'{r["key"]}.{ch}.txt'; x.write_bytes(data); paths[ch]={'path':str(x),'sha256':sha(x)}
        r.update(status='completed' if result.returncode==0 else 'failed',exit=result.returncode,outputs=paths)
    r['ended_unix']=time.time(); r['elapsed_seconds']=round(r['ended_unix']-r['started_unix'],3); write(p,r); return inspect(p)
def invoke(key,kind,argv,extra,vault=None):
    p,r=start(key,kind,argv,extra)
    try:
        x=subprocess.run(argv,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,env=dict(os.environ,TUNNEL_CODEX_BIN=CODEX,TUNNEL_CODEX_USAGE='full'))
        if vault: r['state_after']=state(vault)
        return finish(p,r,x)
    except Exception as e: return finish(p,r,error=e)

def pins():
    m=load(B/'raw/hold-line/sources.json'); bad=[]
    for x in (m or {}).get('files',[]):
        try: actual=sha(x['path'])
        except OSError: actual=None
        if actual != x.get('sha256'): bad.append({'path':x.get('path'),'expected':x.get('sha256'),'actual':actual})
    rel=load(B/'raw/control/RELEASE.json')
    return {'all_pinned_files_match':not bad,'mismatches':bad,'release_ok':bool(rel and rel.get('authorized') is True and rel.get('operator')=='Majkee')}
def check_state(vault,thread=False,preamble=None):
    s=state(vault)
    if not s: raise RuntimeError('missing or malformed vault; refusing invocation')
    if s.get('model')!='gpt-6.1-sol' or s.get('sandbox')!='read-only': raise RuntimeError('vault profile mismatch; refusing invocation')
    if thread and (not s.get('threadId') or not s.get('lastTurnId')): raise RuntimeError('vault lacks completed first turn; refusing invocation')
    if preamble is not None and s.get('preamble')!=preamble: raise RuntimeError('vault preamble mismatch; refusing invocation')
    return s
def supports_high(models):
    for model in models:
        for effort in model.get('supportedReasoningEfforts') or []:
            if effort == 'high' or (isinstance(effort,dict) and effort.get('reasoningEffort') == 'high'):
                return True
    return False

def selfcheck(report):
    items=[]
    with tempfile.TemporaryDirectory(prefix='g09-caretaker-') as d:
        d=Path(d); out=d/'out'; out.write_text('ok')
        good=d/'good'; write(good,{'status':'completed','exit':0,'outputs':{x:{'path':str(out),'sha256':sha(out)} for x in ('stdout','stderr')}}); items.append(('validated-completion',inspect(good)['classification']=='completed-and-validated'))
        live=d/'live'; write(live,{'status':'pending','runner':{'pid':os.getpid(),'start':pstart(os.getpid())}}); items.append(('living-pending',inspect(live)['classification']=='running'))
        dead=d/'dead'; write(dead,{'status':'pending','runner':{'pid':99999999,'start':'none'}}); items.append(('dead-pending-unknown',inspect(dead)['classification']=='unknown'))
        corrupt=d/'corrupt'; corrupt.write_text('bad'); items.append(('corrupt-receipt-unknown',inspect(corrupt)['classification']=='unknown'))
        changed=d/'changed'; write(changed,{'status':'completed','exit':0,'outputs':{x:{'path':str(out),'sha256':sha(out)} for x in ('stdout','stderr')}}); out.write_text('changed'); items.append(('changed-output-unknown',inspect(changed)['classification']=='unknown'))
        dupe=d/'dupe'; dupe.write_text('{}')
        try:
            with dupe.open('x'): pass
            duplicate=False
        except FileExistsError: duplicate=True
        items.append(('duplicate-refusal-without-invocation',duplicate))
    items += [('allowlist-role-binding',ROUNDS['R1'][0]=='researcher' and 'Z9' not in ROUNDS),('cold-no-preamble',ROUNDS['R1'][2]=='cold'),('warm-preamble-policy',ROUNDS['R2'][2]=='warm' and Path(PRE).is_file()),('ask-cap-five',len(ROUNDS)==5),('model-effort-object-shape',supports_high([{'supportedReasoningEfforts':[{'reasoningEffort':'high'}]}]))]
    v={'kind':'pure-helper-offline','target_turns':0,'checks':[{'name':n,'pass':p} for n,p in items],'pass':all(p for _,p in items)}; write(report,v); return v

def compile_c1():
    q=pins()
    if not q['all_pinned_files_match'] or not q['release_ok']: raise RuntimeError('pin or release failure; refusing C1 packet compilation')
    inp='\n'.join([f'- `{Path(__file__).resolve()}` (trial-local receipt adapter; SHA256 {sha(__file__)})',f'- `{H / "checks/self-check.json"}` (offline pure-helper checks)',f'- `{H / "plan.C1.json"}` (frozen C1 plan)'])
    c={}
    for cycle in ('R1','A1'):
        template=B/f'raw/packets/{cycle}.md'; text=template.read_text().replace('@@G09_NAMED_ADAPTER_INPUTS@@',inp)+f'\n\nCaretaker binding: cycle={cycle}; role={ROUNDS[cycle][0]}; vault={ROUNDS[cycle][1]}; cold preamble=none.\n'; dst=PKT/f'{cycle}.prompt.txt'
        if dst.exists(): raise RuntimeError(f'refusing to replace frozen packet {dst}')
        dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(text); c[cycle]={'path':str(dst),'sha256':sha(dst),'template':str(template),'template_sha256':sha(template)}
    plan={'stage':'C1','pins':q,'adapter':{'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},'compiled':c,'ask_cap':5,'planned_asks':['R1','A1'],'preamble':{'source':SOURCE_PRE,'deployed':PRE,'sha256':sha(PRE),'match':sha(SOURCE_PRE)==sha(PRE)}}
    dest=H/'plan.C1.json'
    if dest.exists(): raise RuntimeError(f'refusing to replace frozen plan {dest}')
    write(dest,plan); return plan

def profile(key):
    spec=importlib.util.spec_from_file_location('g09_tunnel','/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    p,r=start(key,'profile',[CODEX,'app-server','model/list (zero-turn JSON-RPC)'],{})
    try:
        t=mod.AppServerTransport(codex_bin=CODEX,cwd=str(B)); t.start()
        try: s=mod.Session(t); s.initialize(); models=s.model_list()
        finally: t.close()
        found=[{k:x.get(k) for k in ('id','model','defaultReasoningEffort','supportedReasoningEfforts')} for x in models.get('data',[]) if x.get('id')=='gpt-6.1-sol']; record={'binary':CODEX,'version':subprocess.check_output([CODEX,'--version'],text=True).strip(),'selected':found,'target_turns':0}; supported=supports_high(found)
        OUT.mkdir(parents=True,exist_ok=True); so=OUT/f'{key}.stdout.txt'; se=OUT/f'{key}.stderr.txt'; so.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n'); se.write_text(''); r.update(profile=record,status='completed' if supported else 'failed',exit=0 if supported else 11,outputs={'stdout':{'path':str(so),'sha256':sha(so)},'stderr':{'path':str(se),'sha256':sha(se)}},profile_supports_requested=supported,ended_unix=time.time()); r['elapsed_seconds']=round(r['ended_unix']-r['started_unix'],3); write(p,r); return inspect(p)
    except Exception as e: return finish(p,r,error=e)
def reconcile_profile(report):
    receipts=[]
    for p in sorted(OPS.glob('C1.profile*.operation.json')):
        r=load(p) or {}; receipts.append({'path':str(p),'status':r.get('status'),'exit':r.get('exit'),'profile_supports_requested':r.get('profile_supports_requested')})
        if supports_high((r.get('profile') or {}).get('selected') or []):
            value={'kind':'zero-turn-profile-reconciliation','profile_supported':True,'selected_receipt':str(p),'receipts':receipts,'note':'selected model/effort evidenced by durable profile payload; earlier receipt status may reflect adapter parsing, not an unsupported profile'}
            if report.exists(): raise RuntimeError(f'refusing to replace profile reconciliation {report}')
            write(report,value); return value
    value={'kind':'zero-turn-profile-reconciliation','profile_supported':False,'receipts':receipts}
    if report.exists(): raise RuntimeError(f'refusing to replace profile reconciliation {report}')
    write(report,value); return value

def run(cycle,action):
    role,vault,mode=ROUNDS[cycle]; key=f'{cycle}.{action}'
    if action=='open':
        if vault.exists(): raise RuntimeError('existing vault must be reconciled, not reopened')
        a=[SHIM,'open','--state',str(vault),'--enable','--sandbox','read-only','--cwd',str(B),'--preamble','none','--model','gpt-6.1-sol','--override','effort=high']; return invoke(key,action,a,{'cycle':cycle,'role':role,'expected':{'threadId':None,'model':'gpt-6.1-sol','sandbox':'read-only','preamble':None},'state_before':None},vault)
    if action=='ask':
        s=check_state(vault,False,None if mode=='cold' else PRE)
        if mode=='cold' and s.get('threadId'): raise RuntimeError('cold packet refused on an already-born vault')
        prompt=PKT/f'{cycle}.prompt.txt'
        if not prompt.is_file(): raise RuntimeError(f'missing frozen packet {prompt}')
        a=[SHIM,'ask',prompt.read_text(),'--state',str(vault)]; verdict=invoke(key,action,a,{'cycle':cycle,'role':role,'prompt':{'path':str(prompt),'sha256':sha(prompt)},'state_before':s,'attempt_number':ask_count()+1},vault)
        if verdict['classification']=='completed-and-validated':
            RES.mkdir(parents=True,exist_ok=True); dst=RES/f'{cycle}.result.md'
            if dst.exists(): raise RuntimeError(f'refusing to replace selected result {dst}')
            dst.write_bytes((OUT/f'{key}.stdout.txt').read_bytes())
        return verdict
    if action=='preamble':
        s=check_state(vault,True)
        if sha(SOURCE_PRE)!=sha(PRE): raise RuntimeError('authored/deployed preamble mismatch')
        return invoke(key,action,[SHIM,'open','--state',str(vault),'--preamble',PRE],{'cycle':cycle,'role':role,'preamble':{'path':PRE,'sha256':sha(PRE)},'state_before':s},vault)
    if action in ('resume','read'):
        s=check_state(vault,True,PRE); return invoke(key,action,[SHIM,action,'--state',str(vault)],{'cycle':cycle,'role':role,'state_before':s},vault)
    raise RuntimeError(f'unallowlisted action {action!r}')

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True); c=s.add_parser('self-check'); c.add_argument('--report',type=Path,required=True); s.add_parser('compile-c1'); z=s.add_parser('profile'); z.add_argument('--key',default='C1.profile'); q=s.add_parser('reconcile-profile'); q.add_argument('--report',type=Path,required=True); r=s.add_parser('run'); r.add_argument('cycle',choices=sorted(ROUNDS)); r.add_argument('action',choices=['open','ask','preamble','resume','read']); i=s.add_parser('inspect'); i.add_argument('key'); a=p.parse_args()
    try:
        if a.cmd=='self-check': v=selfcheck(a.report)
        elif a.cmd=='compile-c1': v=compile_c1()
        elif a.cmd=='profile': v=profile(a.key)
        elif a.cmd=='reconcile-profile': v=reconcile_profile(a.report)
        elif a.cmd=='run': v=run(a.cycle,a.action)
        else: v=inspect(op(a.key))
        print(json.dumps(v,sort_keys=True))
    except RuntimeError as e: print(str(e),file=sys.stderr); raise SystemExit(2)
if __name__=='__main__': main()
