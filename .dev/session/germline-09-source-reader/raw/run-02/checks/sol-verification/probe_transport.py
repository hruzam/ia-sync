"""Independent fake-clock, fake-transport checkpoints; no external process permitted."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
from pathlib import Path
from types import SimpleNamespace

SOURCE=Path('/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py')
os.environ['TUNNEL_CODEX_TIMEOUT']='1800'
spec=importlib.util.spec_from_file_location('sol_transport',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def blocked(*args,**kwargs): raise AssertionError('REAL SUBPROCESS FORBIDDEN')
subprocess.run=blocked;subprocess.Popen=blocked
rows=[]
class Clock:
    value=0.0
    def monotonic(self): return self.value
clock=Clock();m.time.monotonic=clock.monotonic
class Fake:
    def __init__(self,path,stage): self.path,self.stage,self.events,self.counter,self.closed=path,stage,[],0,False
    def start(self): pass
    def close(self):self.closed=True
    def notify(self,*args):pass
    def respond_error(self,*args):pass
    def request(self,method,params):
        self.counter+=1
        if method=='turn/start':
            saved=json.loads(self.path.read_text())
            assert saved['threadId']=='T-sol','birth/resume was not durable before dispatch'
            if self.stage=='before-ack':return self.counter
            value={'turn':{'id':'U-sol'}}
        elif method=='initialize':value={}
        elif method in ('thread/start','thread/resume'):value={'thread':{'id':'T-sol'},'model':'gpt-6.1-sol','sandbox':{'type':'readOnly','networkAccess':False}}
        elif method=='thread/read':
            value={'thread':{'turns':[{'id':'U-sol','status':'completed','items':[{'type':'agentMessage','text':'answer'}]}]}}
            if self.stage=='reconcile-failure':value={'thread':{'turns':[]}}
        else:raise AssertionError(method)
        self.events.append((5,{'id':self.counter,'result':value}))
        if method=='turn/start' and self.stage in ('success','reconcile-failure'):
            self.events.extend([(2,{'method':'item/completed','params':{'item':{'type':'agentMessage','text':'answer'}}}),(3,{'method':'turn/completed','params':{'threadId':'T-sol','turn':{'id':'U-sol','status':'completed'}}})])
        if method=='turn/start' and self.stage=='after-ack':
            self.events.append((2,{'method':'item/started','params':{}}))
        return self.counter
    def next_message(self,timeout):
        if self.events:
            delay,value=self.events.pop(0);clock.value+=delay;return value
        clock.value+=timeout
        raise m.TransportTimeout('fake queue exhausted')

for verb in ('send','ask'):
 for born in (False,True):
  for stage in ('before-ack','after-ack','reconcile-failure','success'):
   with tempfile.TemporaryDirectory(prefix='g09-sol-transport-') as directory:
    clock.value=0
    path=Path(directory)/'state.json'
    path.write_text(json.dumps({'enabled':True,'threadId':'T-sol' if born else None,'lastTurnId':None,'model':'gpt-6.1-sol','sandbox':'read-only'}))
    fake=Fake(path,stage);m.AppServerTransport=lambda **kwargs:fake
    out,err=io.StringIO(),io.StringIO();failure=None
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
     try:getattr(m,'cmd_'+verb)(SimpleNamespace(state=str(path),text='fake only'))
     except m.TunnelError as exc:failure=str(exc)
    saved=json.loads(path.read_text());assert fake.closed
    assert not Path(str(path)+'.turn.lock').exists()
    assert saved['threadId']=='T-sol'
    if stage=='success':assert saved['lastTurnId']=='U-sol' and 'inFlightTurnId' not in saved and failure is None and 'answer' in out.getvalue()
    else:
     assert saved['lastTurnId'] is None and failure and not out.getvalue()
     if stage=='before-ack':assert not saved.get('inFlightTurnId') and 'phase=turn/start response' in failure and 'threadId=T-sol' in failure
     else:assert saved['inFlightTurnId']=='U-sol'
     if stage=='after-ack':
      assert 'phase=turn/completed' in failure and 'elapsed=1800.000s' in failure and 'configured_budget=1800.000s' in failure and 'last_event_age=1798.000s' in failure and 'turnId=U-sol' in failure
    rows.append({'verb':verb,'resumed':born,'stage':stage,'state':saved,'failure':failure,'closed':fake.closed,'clock':clock.value})
print(json.dumps({'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'target_model_turns':0,'checks':len(rows),'rows':rows},indent=2))
