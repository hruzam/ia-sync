"""Check the exact-thread bootstrap contract with a malformed identity-free readback."""
import contextlib,io,json,os,runpy,tempfile
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):helpers=runpy.run_path(str(Path(__file__).with_name('probe_bootstrap_profile.py')))
a,setup,receipt,dump,sha=(helpers[k] for k in ('a','setup','receipt','dump','sha'))
with tempfile.TemporaryDirectory(prefix='g09-sol-missing-thread-') as directory:
 run,files,vault,c=setup(Path(directory))
 state={'threadId':'T-ack','lastTurnId':'U-ack'}
 ack=dict(c['bootstrap_ack']['required'],role='researcher',sources=c['bootstrap_ack']['sources']['researcher'])
 text='G09.run-02.R1\nBOOTSTRAP '+json.dumps(ack)+'\nSubstantive answer'
 receipt(c,'run02.R1.ask',text,state)
 receipt(c,'run02.R1.read',json.dumps({'thread':{'turns':[{'id':'U-ack','status':'completed','items':[{'type':'agentMessage','text':text}]}]}}),state)
 source=Path(os.environ.get('SOL_ADAPTER_PATH',str(helpers['R']/'caretaker/run_operations.py')))
 if os.environ.get('SOL_ADAPTER_PATH'):
  a=helpers['imp']('sol_frozen_missing_thread',source);a.B=Path(directory);a.R=run
 try:result=a.verify_bootstrap('R1');rejected=False
 except RuntimeError as exc:result=str(exc);rejected=True
 print(json.dumps({'source_sha256':sha(source),'criterion':'CONTRACT.bootstrap_ack.verification exact role/thread/turn','missing_thread_identity_rejected':rejected,'result':result,'target_model_turns':0},indent=2))
