#!/usr/bin/env python3
"""Cartan-owned offline pin generation; never authorizes release."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[3]
R=B/'raw/run-02'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
fixed=[B/'RUNBOOK.md',B/'ACCEPTANCE.md',B/'raw/input/SOURCE-MAP.md',R/'CONTRACT.json',R/'SCHEDULE.md',R/'RECONCILIATION.md',R/'control/ROUND-MAP.json',R/'control/CONTRACT.template.json',Path(__file__).resolve(),B.parents[2]/'zsh/ai/tunnel-codex.py',B.parents[2]/'zsh/ai/tunnel-codex.zsh',B.parents[2]/'codex/agents/implementer.toml',B.parents[2]/'codex/agents/astrobley.toml',B.parents[2]/'codex/agents/verifier.toml',Path('/home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md'),Path('/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md'),Path('/home/hruzam/.germline/tunnel/tunnel.preamble.md')]
for name in ['hold-line','briefs','packets']:
 fixed.extend(sorted((R/name).rglob('*.md')))
for name in ['caretaker','repair']:
 fixed.extend(sorted((R/name).rglob('*.py')))
if (R/'TUNNEL.md').exists(): fixed.append(R/'TUNNEL.md')
missing=[str(p) for p in fixed if not p.is_file()]
if missing: raise SystemExit('missing pin input: '+repr(missing))
manifest={'schema':'g09-run02-pins/v1','run_id':'run-02','files':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(set(fixed))],'preamble':{'source':'/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md','deployed':'/home/hruzam/.germline/tunnel/tunnel.preamble.md'},'mutable_authority_checked_each_effect':['STATUS.md','control/RELEASE.json','control/HOLD.json','caretaker/plan.*.json','control/A3.GRANT.json'],'authority':'Hashes identify exact inputs. Actual fresh GO and release checks alone authorize dispatch. No retention/correctness claim.'}
p=R/'hold-line/sources.json'; p.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'pins':len(manifest['files']),'manifest_sha256':sha(p),'contract_sha256':sha(R/'CONTRACT.json')}))
