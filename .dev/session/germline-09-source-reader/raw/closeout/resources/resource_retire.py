#!/usr/bin/env python3
"""G09 run-01 resource retirement only: one known thread and one local vault."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

BED = Path('/home/hruzam/ia-sync/.dev/session/germline-09-source-reader')
HOME = BED / 'raw/closeout'
HERE = HOME / 'resources'
SNAPSHOTS = HOME / 'snapshots'
THREAD = '01a176f7-532b-7722-9324-0ecb92694073'
VAULT = BED / 'raw/caretaker/tunnel.researcher.state.json'
CODEX = '/home/hruzam/.local/bin/codex'
SHIM = '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f'{path.name}.tmp-{os.getpid()}')
    with tmp.open('w') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
def operation(name, argv):
    path = HERE / f'{name}.json'
    if path.exists(): raise RuntimeError(f'refusing existing cleanup receipt {path}')
    record = {'kind':'g09-run-01-resource-retirement','operation':name,'argv':argv,
              'started_unix':time.time(),'status':'pending','pid':os.getpid(),
              'pid_namespace':os.readlink('/proc/self/ns/pid')}
    write(path, record); return path, record
def finish(path, record, outcome=None, error=None):
    record.update(status='completed' if error is None else 'failed', ended_unix=time.time(),
                  elapsed_seconds=round(time.time()-record['started_unix'],3))
    if error is not None: record['error']=repr(error)
    if outcome is not None: record['outcome']=outcome
    write(path,record)
def transport():
    spec=importlib.util.spec_from_file_location('g09_tunnel', '/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module, module.AppServerTransport(codex_bin=CODEX,cwd=str(BED))
def selected_thread(raw):
    thread=raw.get('thread') or {}; turns=thread.get('turns') or []
    return {'id':thread.get('id'),'status':thread.get('status'),'cwd':thread.get('cwd'),
            'turns':[{'id':x.get('id'),'status':x.get('status')} for x in turns]}
def read_current(name):
    path,record=operation(name,['app-server','thread/read',THREAD,'includeTurns=true'])
    try:
        module,t=transport(); t.start()
        try:
            session=module.Session(t,timeout=30); session.initialize(); raw=session.thread_read(THREAD,include_turns=True)
        finally: t.close()
        payload=json.dumps(raw,sort_keys=True).encode()
        finish(path,record,{'thread':selected_thread(raw),'response_sha256':hashlib.sha256(payload).hexdigest(),
                            'target_model_turns':0})
    except Exception as e: finish(path,record,error=e)
def inventory():
    path,record=operation('01.inventory',['scoped-files-and-known-pid-observation'])
    try:
        vaults=sorted(str(x) for x in BED.rglob('tunnel*.state.json'))
        known_pid=1319728
        finish(path,record,{'known_thread':THREAD,'vaults':vaults,
                            'known_r1_runner':{'pid':known_pid,'present':Path(f'/proc/{known_pid}').exists(),
                                               'checker_pid_namespace':os.readlink('/proc/self/ns/pid')},
                            'native_worker':'same requested /root/caretaker; no separately discoverable OS PID asserted',
                            'owned_cleanup_processes_before':[os.getpid()]})
    except Exception as e: finish(path,record,error=e)
def archive():
    path,record=operation('03.archive-R1',[CODEX,'archive',THREAD])
    try:
        run=subprocess.run([CODEX,'archive',THREAD],cwd=BED,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        out=HERE/'03.archive-R1.stdout.txt'; err=HERE/'03.archive-R1.stderr.txt'; out.write_bytes(run.stdout); err.write_bytes(run.stderr)
        finish(path,record,{'exit':run.returncode,'stdout':{'path':str(out),'sha256':sha(out)},
                            'stderr':{'path':str(err),'sha256':sha(err)},'supported_operation':'codex archive'})
    except Exception as e: finish(path,record,error=e)
def snapshot():
    path,record=operation('05.snapshot-vault',[str(VAULT),str(SNAPSHOTS/'tunnel.researcher.state.json')])
    try:
        if not VAULT.is_file(): raise RuntimeError('expected G09 vault missing before snapshot')
        dest=SNAPSHOTS/'tunnel.researcher.state.json'
        if dest.exists(): raise RuntimeError('refusing to overwrite vault snapshot')
        shutil.copyfile(VAULT,dest)
        finish(path,record,{'source':str(VAULT),'source_sha256':sha(VAULT),'snapshot':str(dest),
                            'snapshot_sha256':sha(dest),'exact_bytes':VAULT.read_bytes()==dest.read_bytes(),
                            'state':json.loads(dest.read_text())})
    except Exception as e: finish(path,record,error=e)
def close():
    path,record=operation('06.close-vault',[SHIM,'close','--state',str(VAULT)])
    try:
        run=subprocess.run([SHIM,'close','--state',str(VAULT)],cwd=BED,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        out=HERE/'06.close-vault.stdout.txt'; err=HERE/'06.close-vault.stderr.txt'; out.write_bytes(run.stdout); err.write_bytes(run.stderr)
        finish(path,record,{'exit':run.returncode,'stdout':{'path':str(out),'sha256':sha(out)},
                            'stderr':{'path':str(err),'sha256':sha(err)},'vault_exists_after':VAULT.exists(),
                            'lock_exists_after':Path(str(VAULT)+'.lock').exists(),'supported_operation':'tunnel-codex close'})
    except Exception as e: finish(path,record,error=e)
def main():
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['inventory','read-before','archive','read-after','snapshot','close']); a=p.parse_args()
    {'inventory':inventory,'read-before':lambda:read_current('02.read-before-archive'),'archive':archive,
     'read-after':lambda:read_current('04.read-after-archive'),'snapshot':snapshot,'close':close}[a.action]()
if __name__ == '__main__': main()
