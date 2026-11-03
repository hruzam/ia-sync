"""Independent final-I2 P7 checks. Existing commands only; deployment preview only."""
import datetime,hashlib,json,os,stat,subprocess,time
from pathlib import Path
B=Path('/home/hruzam/ia-sync');R=B/'.dev/session/germline-09-source-reader/raw/run-02';E=Path(__file__).resolve().parent;P=B/'zsh/experimental/source-reader';X=B/'zsh/experimental'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
manifest=R/'implementation/I2/MANIFEST.json';alias=manifest.with_name('manifest.json');expected_manifest='b760f1a3d3cf5833adea9e696abadf0efa88e06698fb3d1e0bba43d011ff5ade'
assert sha(manifest)==sha(alias)==expected_manifest
m=json.loads(manifest.read_text());expected=m['audited_files'];assert len(expected)==24
before={p:sha(p) for p in expected};assert before==expected
symlinks={p:os.readlink(p) for p in m['audited_symlinks']};assert symlinks==m['audited_symlinks']
modes={p:oct(stat.S_IMODE(Path(p).stat().st_mode)) for p in expected};assert modes==m['product_modes']
base=X/'base.zsh';oldbase=Path(m['base_row']['before_snapshot']);row=b'#   source-reader \xe2\x80\x94 plugged 2026-10-29 \xe2\x80\x94 G09 D1 \xe2\x80\x94 lazy read-only source browser \xe2\x80\x94 EXPERIMENTAL ONLY (not approved)\n'
base_bytes=base.read_bytes();assert base_bytes.count(row)==1 and base_bytes.replace(row,b'',1)==oldbase.read_bytes()
assert sha(base)==m['i1_hashes'][str(base)]==m['base_row']['after_sha256']
contracts=[B/'deploy.sh',B/'machines.json',X/'dispatcher.zsh',X/'README.md',B/'zsh/registries/gen-temple-map.sh',B/'zsh/registries/projects.json',B/'zsh/ai/temple-project-map.zsh']
contract_before={str(p):sha(p) for p in contracts}
write(E/'before.json',{'manifest_sha256':expected_manifest,'audited_files':before,'symlinks':symlinks,'modes':modes,'contract_files':contract_before})
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');checks=[]
def run(name,argv,stdin=None):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
 completed=subprocess.run(argv,cwd=B,env=env,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=60)
 paths={}
 for channel,data in [('stdout',completed.stdout),('stderr',completed.stderr)]:
  path=E/(name+'.'+channel);path.write_bytes(data);paths[channel]={'path':str(path),'sha256':sha(path),'bytes':len(data)}
 item={'name':name,'argv':argv,'cwd':str(B),'started_at':started,'elapsed_seconds':round(time.monotonic()-tick,3),'exit':completed.returncode,'outputs':paths};checks.append(item)
 return completed
shell_prefix='typeset -g _EXPERIMENTAL_ROOT=/home/hruzam/ia-sync/zsh/experimental; source "$_EXPERIMENTAL_ROOT/dispatcher.zsh"; '
def dispatch(name,args):return run(name,['/usr/bin/zsh','-f','-c',shell_prefix+'_exp_run source-reader "$@"','g09-p7',*args])
for name,path in [('syntax-base',base),('syntax-dispatcher',X/'dispatcher.zsh'),('syntax-runner',P/'runner.zsh')]:assert run(name,['/usr/bin/zsh','-n',str(path)]).returncode==0
silent='typeset -g _EXPERIMENTAL_ROOT=/home/hruzam/ia-sync/zsh/experimental; function python3(){ print -u2 PYTHON_CALLED_DURING_SOURCE; return 77; }; function zsh(){ print -u2 ZSH_CALLED_DURING_SOURCE; return 77; }; source "$_EXPERIMENTAL_ROOT/dispatcher.zsh"; source "$_EXPERIMENTAL_ROOT/dispatcher.zsh"; (( $+functions[_exp_run] && $+functions[_exp_list] ))'
out=run('silent-source-lazy-twice',['/usr/bin/zsh','-f','-c',silent]);assert out.returncode==0 and out.stdout==out.stderr==b''
out=dispatch('dispatcher-help',['--help']);assert out.returncode==0 and b'catalog' in out.stdout and out.stderr==b''
roots=str(P/'fixtures/roots.json');out=dispatch('dispatcher-catalog-json',['--roots',roots,'catalog','--json']);assert out.returncode==0 and out.stderr==b'';catalog=json.loads(out.stdout);assert catalog['entries']
assert all(str(P/'fixtures') in e['absolute_path'] for e in catalog['entries'])
out=dispatch('dispatcher-catalog-plain',['--roots',roots,'catalog']);assert out.returncode==0 and b'runtime visibility/activation unknown' in out.stdout and out.stderr==b''
selected=[]
for label,relative in [('codex-guide','codex/guide/SKILL.md'),('linked','codex/linked/SKILL.md'),('canary','codex/canary/SKILL.md'),('guide-chapter','guides/topic/res/unique.md')]:
 path=P/'fixtures'/relative;entry=next(e for e in catalog['entries'] if e['absolute_path']==str(path))
 for kind,selection in [('path',str(path)),('id',entry['id'])]:
  out=dispatch('dispatcher-show-'+label+'-'+kind,['--roots',roots,'show',selection]);assert out.returncode==0 and out.stdout==path.read_bytes() and out.stderr==b''
 selected.append({'lexical_path':str(path),'resolved_path':str(path.resolve()),'id':entry['id'],'selected_bytes_sha256':sha(path)})
# Full existing deployment contract. Every copy/ensure leg is guarded; rsync gets -n;
# generated map uses --check and does not traverse project paths stored in its JSON.
dry_exit=None
blocked_argv=['/usr/bin/bash',str(B/'deploy.sh'),'--dry-run']
blocked_reason='Explicit no-Nablarva boundary: full preview necessarily rsync-scans entire zsh/ including protected mirror; no experimental-subtree option exists.'
(E/'deploy-dry-run.stdout').write_bytes(b'')
(E/'deploy-dry-run.stderr').write_text(blocked_reason+'\n')
checks.append({'name':'deploy-dry-run','argv':blocked_argv,'executed':False,'exit':None,'status':'BLOCKED_UNVERIFIED','reason':blocked_reason,'outputs':{channel:{'path':str(E/('deploy-dry-run.'+channel)),'sha256':sha(E/('deploy-dry-run.'+channel))} for channel in ('stdout','stderr')}})
preview=''
proposals=[];section=None
for line in preview.splitlines():
 if line.startswith('→ '):section=line[2:]
 stripped=line.strip()
 itemized=len(line)>10 and line[0] in '<>ch.*' and line[1:2] in 'fdLDS.'
 cpchange='[dry] CREATE' in line or '[dry] UPDATE' in line or '[dry] mkdir' in line
 if itemized or cpchange:
  owned=(section=='~/.config/zsh' and ('experimental/source-reader/' in line or stripped.endswith('experimental/base.zsh')))
  proposals.append({'section':section,'line':line,'scope':'P7-product' if owned else 'foreign-preview-only','applied':False})
write(E/'foreign-preview-proposals.json',{'applied':False,'foreign':[p for p in proposals if p['scope']=='foreign-preview-only'],'product':[p for p in proposals if p['scope']=='P7-product'],'raw_preview':str(E/'deploy-dry-run.stdout'),'raw_preview_sha256':sha(E/'deploy-dry-run.stdout')})
after={p:sha(p) for p in expected};assert after==before==expected
contract_after={str(p):sha(p) for p in contracts};assert contract_after==contract_before
assert {p:os.readlink(p) for p in m['audited_symlinks']}==symlinks
assert {p:oct(stat.S_IMODE(Path(p).stat().st_mode)) for p in expected}==modes
assert sha(manifest)==sha(alias)==expected_manifest
result={'schema':'g09-independent-p7/v1','verdict':'PASS' if dry_exit==0 else 'UNVERIFIED','manifest':str(manifest),'manifest_alias':str(alias),'manifest_sha256':expected_manifest,'manifest_aliases_equal':True,'complete_audited_map':expected,'before_product_map':before,'after_product_map':after,'product_preserved':True,'symlinks':symlinks,'modes':modes,'base_owned_row':row.decode().rstrip(),'base_only_one_row_added':True,'base_unchanged_from_I1':True,'contract_before':contract_before,'contract_after':contract_after,'checks':checks,'selected_byte_comparisons':selected,'dry_run_exit':dry_exit,'foreign_preview_proposals':str(E/'foreign-preview-proposals.json'),'foreign_preview_sha256':sha(E/'foreign-preview-proposals.json'),'gaps':[blocked_reason],'deploy_available_options':['--dry-run','-n','--codex-only','--germline-only','--adopt-germline'],'deploy_missing_option':'No zsh/experimental-only scope or user exclusion option; codex/germline-only omit the owned zsh product.','foreign_proposals_observed':False,'model_turns':0,'actual_deployments':0,'limits':['Source-tree dispatcher only: base is syntax/hash/owned-row checked; its live dependency sources were not loaded.','Optional interactive fzf not required or exercised.','Full preview not executed; no current foreign proposals observed or applied. Prior I1 builder preview remains historical only.']}
write(E/'results.json',result)
print(json.dumps({'verdict':result['verdict'],'checks':len(checks),'product_files':len(expected),'selected_files':len(selected),'dry_run_exit':dry_exit,'foreign_proposals':len([p for p in proposals if p['scope']=='foreign-preview-only']),'product_proposals':len([p for p in proposals if p['scope']=='P7-product']),'results':str(E/'results.json')},indent=2))
