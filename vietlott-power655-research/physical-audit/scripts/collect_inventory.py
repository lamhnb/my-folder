"""Read-only Git/local inventory. Never opens private conversation/session bodies."""
from pathlib import Path
import csv, hashlib, json, os, subprocess, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
EX = OUT / 'extracted'
EX.mkdir(exist_ok=True)
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8', 'replace').strip()
def write_csv(name, rows, fields):
    with (OUT/name).open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def relevant(p):
    s=p.lower()
    return 'vietlott' in s or 'power655' in s or 'power-655' in s or 'power_655' in s
def purpose(p):
    s=p.lower()
    for k,v in [('digital-twin','Digital Twin source/configuration/results'),('phase4','Phase 4 work order'),('phase3','Phase 3 order-label/bias research'),('phase2','Phase 2 observability/timing/video evidence'),('physical-research','Phase 1 reconnaissance/technical evidence'),('b1_adaptive','B1 Adaptive context; preserved'),('b1_physical','B1 physical challenger context; preserved')]:
        if k in s:return v
    return 'Lottery research context; preserved'

refs=git('for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/remotes').splitlines()
rows=[];refrows=[];unique_blobs=set()
for line in refs:
    ref,commit=line.split('|')
    if ref.endswith('/HEAD'):continue
    files=git('ls-tree','-r',commit).splitlines()
    n=0
    for item in files:
        meta,path=item.split('\t',1)
        if not relevant(path):continue
        # The new audit is not evidence of previous work.
        if path.startswith('vietlott-power655-research/physical-audit/'):continue
        mode,typ,blob=meta.split();n+=1;unique_blobs.add((path,blob))
        rows.append(dict(artifact=path,location=ref+':'+path,commit_sha=commit,purpose=purpose(path),status='COMMITTED_REF_SNAPSHOT',blob_sha=blob,sha256='',notes='Snapshot commit, not necessarily file introduction commit'))
    refrows.append(dict(ref=ref,commit_sha=commit,relevant_file_count=n))
write_csv('extracted/refs.csv',refrows,['ref','commit_sha','relevant_file_count'])
fsck=git('fsck','--full','--no-reflogs','--unreachable')
(EX/'git_fsck.txt').write_text(fsck,encoding='utf-8')
reachable=set(git('rev-list','--all').splitlines())
unreachable=[]
for line in fsck.splitlines():
    if not line.startswith('unreachable commit '):continue
    commit=line.split()[-1]
    desc=git('show','-s','--format=%aI|%s',commit)
    changed=git('diff-tree','--root','--no-commit-id','--name-only','-r',commit).splitlines()
    rel=[p for p in changed if relevant(p)]
    if rel:
        for p in rel:
            rows.append(dict(artifact=p,location='fsck-reported:'+commit+':'+p,commit_sha=commit,purpose=purpose(p),status='FSCK_REPORTED_ALREADY_REACHABLE' if commit in reachable else 'UNREACHABLE_OBJECT',blob_sha='',sha256='',notes=desc+'; reachability cross-checked with git rev-list --all'))
    unreachable.append(dict(commit_sha=commit,description=desc,relevant_changed_paths=rel,reachable_from_current_ref=commit in reachable))
(EX/'unreachable_commits.json').write_text(json.dumps(unreachable,indent=2),encoding='utf-8')
(EX/'git_log_all.txt').write_text(git('log','--all','--date=iso-strict','--format=%H|%aI|%d|%s'),encoding='utf-8')
(EX/'git_reflog.txt').write_text(git('reflog','--all','--date=iso-strict'),encoding='utf-8')
(EX/'git_worktrees.txt').write_text(git('worktree','list','--porcelain'),encoding='utf-8')
history=[]
for commit in git('rev-list','--all','--','vietlott-power655-physical-research','vietlott-power655-research').splitlines():
    for item in git('diff-tree','--root','--no-commit-id','--name-status','-r',commit).splitlines():
        parts=item.split('\t');p=parts[-1]
        if not relevant(p) or p.startswith('vietlott-power655-research/physical-audit/'):continue
        history.append(dict(commit_sha=commit,change=parts[0],path=p))
write_csv('extracted/commit_file_history.csv',history,['commit_sha','change','path'])

# Bounded discovery of likely output/worktree locations. No raw application logs read.
scan_roots=[Path('C:/vietlott-research-output'),ROOT,Path('C:/Users/Ho Lam/Desktop'),Path('C:/Users/Ho Lam/Documents'),Path('C:/Users/Ho Lam/Downloads'),Path('C:/Users/Ho Lam/Claude'),Path('C:/Users/Ho Lam/source'),Path('C:/Users/Ho Lam/.codex/worktrees'),Path('D:/workspace'),Path('D:/Tổng hợp')]
prune={'.git','node_modules','.venv','venv','site-packages','__pycache__','.next','target','dist','sessions','session','cache','.cache','logs','physical-audit-20261022'}
scan=[];repos=[]
for base in scan_roots:
    count=0;matches=0
    if not base.exists():
        scan.append(dict(root=str(base),status='ABSENT',files_seen=0,matches=0));continue
    for d,dirs,files in os.walk(base):
        if '.git' in dirs or '.git' in files:repos.append(str(Path(d)))
        dirs[:]=[s for s in dirs if s.lower() not in prune]
        for name in files:
            p=Path(d)/name;count+=1
            if count>250000:break
            if OUT in p.parents or name=='MEMORY_AGENT_STATE.md':continue
            if not relevant(str(p)):continue
            matches+=1
            rel=str(p.relative_to(ROOT)).replace('\\','/') if ROOT in p.parents else ''
            tracked=False
            if rel:
                tracked=subprocess.run(['git','ls-files','--error-unmatch','--',rel],cwd=ROOT,capture_output=True).returncode==0
            if tracked:continue
            size=p.stat().st_size
            digest=sha(p) if size<100*1024*1024 else ''
            rows.append(dict(artifact=name,location=str(p),commit_sha='',purpose=purpose(str(p)),status='LOCAL_ONLY_UNTRACKED_OR_IGNORED',blob_sha='',sha256=digest,notes=f'{size} bytes; large media hash recovered separately from frozen ledger' if not digest else f'{size} bytes'))
        if count>250000:break
    scan.append(dict(root=str(base),status='BOUNDED_250000_FILES' if count>250000 else 'SCANNED',files_seen=count,matches=matches))
(EX/'local_scan_scope.json').write_text(json.dumps(dict(scans=scan,discovered_repos=sorted(set(repos)),excluded=list(sorted(prune)),limitations='Only accessible selected local roots; no other hosts, deleted branches, external Cowork accounts or undisclosed repositories. Private session/log bodies excluded.'),indent=2),encoding='utf-8')

zip_rows=[]
for p in Path('C:/vietlott-research-output').glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        bad=z.testzip()
        for item in z.infolist():
            data=z.read(item)
            rel=item.filename
            candidates=[ROOT/rel, ROOT/'vietlott-power655-physical-research'/rel]
            local=next((q for q in candidates if q.is_file()),None)
            zip_rows.append(dict(zip_path=str(p),member=rel,sha256=hashlib.sha256(data).hexdigest(),same_as_current=str(local is not None and hashlib.sha256(data).hexdigest()==sha(local)),crc_status='PASS' if bad is None else bad))
write_csv('extracted/zip_members.csv',zip_rows,['zip_path','member','sha256','same_as_current','crc_status'])
write_csv('ARTIFACT_INVENTORY.csv',rows,['artifact','location','commit_sha','purpose','status','blob_sha','sha256','notes'])
summary=dict(generated_at_utc=datetime.now(timezone.utc).isoformat(),base_commit=git('rev-parse','HEAD'),ref_count=len(refrows),inventory_rows=len(rows),unique_committed_path_blobs=len(unique_blobs),fsck_reported_unreachable_commits=len(unreachable),reported_unreachable_also_reachable=sum(x['reachable_from_current_ref'] for x in unreachable),genuinely_unreachable_lottery_commits=sum(bool(x['relevant_changed_paths']) and not x['reachable_from_current_ref'] for x in unreachable),historical_file_change_rows=len(history),local_only_rows=sum(x['status']=='LOCAL_ONLY_UNTRACKED_OR_IGNORED' for x in rows),zip_members=len(zip_rows))
(EX/'inventory_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
