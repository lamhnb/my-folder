"""Inspect known/discovered repository identities; expand only same-repo checkouts."""
import json,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]
scan=json.loads((OUT/'extracted/local_scan_scope.json').read_text())
candidates=set(scan['discovered_repos'])
for p in Path('D:/').iterdir():
 if p.is_dir() and (p/'.git').exists():candidates.add(str(p))
checked=[];matches=[]
for p in sorted(candidates):
 try:
  r=subprocess.run(['git','-C',p,'remote','-v'],capture_output=True,timeout=12)
  same='github.com/lamhnb/my-folder' in r.stdout.decode('utf-8','replace').lower()
  checked.append(dict(path=p,same_requested_repository=same,returncode=r.returncode))
  if same:
   data=dict(path=p)
   for key,args in [('refs',['for-each-ref','--format=%(refname)|%(objectname)']),('worktrees',['worktree','list','--porcelain']),('status',['status','--short'])]:
    q=subprocess.run(['git','-C',p,*args],capture_output=True,timeout=20);data[key]=q.stdout.decode('utf-8','replace')
   matches.append(data)
 except Exception as e:checked.append(dict(path=p,error=type(e).__name__))
(OUT/'extracted/other_checkout_scan.json').write_text(json.dumps(dict(checked=checked,same_repo_checkouts=matches,scope='Discovered selected local roots plus immediate D drive child Git repositories; no other hosts or undisclosed locations'),indent=2),encoding='utf-8')
print('Checked',len(checked),'repositories; same-repo checkouts:',[r['path'] for r in matches])
