"""Recheck support for audit statements without executing physical simulation."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,subprocess,collections,math
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1];EX=OUT/'extracted';DT=ROOT/'vietlott-power655-physical-research/digital-twin'
def dump(name,rows,fields=None):
 with (EX/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 # Selected executed query strings, not a claim of a complete provider response archive.
 queries=[
 'site:vietlott.vn Power 6/55 "bộ bóng" "máy"',
 'site:smartplay.com Vietlott Power 655 machine',
 'site:vietlott.vn "12,34" "50,5"',
 'Vietlott Power 6/55 mua sắm bóng kiểm định máy quay Smartplay',
 'site:vietlott.vn "bộ bóng" "Power"',
 'site:vietlott.vn "máy quay" "Smartplay"',
 'site:smartplay.com Vietlott',
 'site:vietlott.vn "bảo dưỡng" "quay"',
 'site:vietlott.vn "bóng" "kiểm định"',
 'site:vietlott.vn "Smartplay"',
 'site:vietlott.vn "bóng" "thay thế" "Power"',
 'site:smartplay.com "balls" "tolerance"',
 'site:vietlott.vn "Power 6/55" "thiết bị"',
 'site:vietlott.vn "lồng cầu" "Mỹ"',
 'site:muasamcong.mpi.gov.vn "Vietlott" "bóng"',
 'site:vietlott.vn "bộ bóng" "mã"',
 '"Power 6/55" "Smartplay" "máy" -site:reddit.com',
 '"Vietlott" "Magnum"',
 '"Vietlott" "mua sắm" "lồng cầu"',
 '"Vietlott" "bộ bóng" "kiểm tra"',
 'site:vietlott.vn "lựa chọn" "vali"',
 'site:vietlott.vn "lồng cầu" "xuất xứ"',
 'site:vietlott.vn "bộ bóng" "kiểm định" "Power 6/55"',
 'site:smartplay.com "Vietlott" "Power"',
 'site:vietlott.vn "thiết bị quay số" "hãng"',
 'site:vietlott.vn "quy trình" "bóng" "Power"',
 '"Vietlott" "thay" "bóng" "Smartplay"',
 '"Power 6/55" "serial"',
 '"site:vietlott.vn" "UCVMkZX9ciaYRghvpNlSQVnQ"',
 '"Vietlott" "bảo dưỡng lồng cầu"',
 '"Vietlott" "biên bản" "bóng" "kiểm tra"',
 '"Vietlott" "mua sắm" "quay số"',
 '"Vietlott" "mua sắm bóng"',
 '"Vietlott" "cung cấp bóng"',
 '"Vietlott" "kiểm định" "lồng cầu" "bóng"',
 'site:vietlott.vn "bảo trì" "lồng cầu"',
 'site:vietlott.vn "Power" "kiểm định" "2017"',
 'site:smartplay.com "Vietlott" "2017"',
 'site:muasamcong.mpi.gov.vn Vietlott Smartplay',
 'site:muasamcong.mof.gov.vn "Vietlott" "bóng"',
 'site:vietlott.vn "cung cấp" "bóng"',
 'site:vietlott.vn "POWER 6/55" "VC2"',
 'site:smartplay.com "Vietlott" "serial"',
 '"UCucGZm2OZJxf3LpIpKGAQhA" "Power"',
 'site:vietlott.vn "quy trình quay"',
 'site:youtube.com/watch "Vietlott" "kiểm tra" "bóng"',
 'site:vietlott.vn "Smartplay International"',
 'site:smartplay.com "Magnum II" manual',
 'site:smartplay.com "Magnum II" dimensions',
 '"Vietlott" "VC2" "bóng"',
 '"Vietlott" "Magnum II" "bảo dưỡng"',
 ]
 dump('search_log.csv',[dict(query_id=f'Q{i+1:02d}',run_date_utc='2026-10-22',method='web search; selected executed query ledger',query=q,outcome='Vendor/product or rule context located; no independently verified per-draw serial/set register or actual metrology in reviewed results',recovered_evidence='R01-R12; source HTTP ledger; current-rule visual facts',limitation='Bounded selected results; no exhaustive or authenticated tender-attachment history; raw provider result archive not exported') for i,q in enumerate(queries)])
 rows=[]
 for id,p in [('T2',Path('C:/Users/Ho Lam/.codex/attachments/d5cb5d81-200e-454a-883c-3febb0395915/Văn bản đã dán.txt')),('T3',Path('C:/Users/Ho Lam/.codex/attachments/3c06cafe-d9a3-409d-8c8d-0211ff09f966/Văn bản đã dán.txt'))]:
  rows.append(dict(evidence_id=id,local_user_attachment=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,redistributed=False))
 dump('task_attachment_hashes.csv',rows)
 absence=[]
 with (EX/'refs.csv').open(encoding='utf-8') as f:
  frozen_commits=sorted({r['commit_sha'] for r in csv.DictReader(f)})
 for s in ['main.vi/08.2022/cms/power655.pdf','MAGNUM II']:
  cmd=['git','log',*frozen_commits,'--oneline','-S',s,'--','vietlott-power655-physical-research','vietlott-power655-research']
  r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
  absence.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,meaning='Query frozen pre-audit ref commits; absence of recorded source, not proof no person ever saw it'))
 (EX/'prior_source_absence.json').write_text(json.dumps(dict(checked_utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),checks=absence),indent=2),encoding='utf-8')
 files=sorted((DT/'results/runs').glob('*.json'))
 runs=[json.loads(p.read_text()) for p in files]
 baseline=[r for p,r in zip(files,runs) if p.name.startswith('baseline_seed')]
 counts=collections.Counter()
 mismatches=[]
 hashes={n:hashlib.sha256((DT/'simulator'/n).read_bytes()).hexdigest() for n in ['core.py','geometry.py']}
 for r in runs:
  if r['implementation_sha256']!=hashes:mismatches.append(r['seed'])
  for f in r['failures']:counts[f]+=1
 summary=json.loads((DT/'results/summary.json').read_text())
 num=json.loads((DT/'validation/numerical.json').read_text());system=json.loads((DT/'validation/system.json').read_text())
 audit=dict(scope='Recomputed saved-result integrity/counts only; no new simulator or Monte Carlo execution',runs=len(runs),valid_runs=sum(not r['failures'] for r in runs),incomplete_runs=sum(len(r['captures'])<7 for r in runs),complete_with_failures=sum(len(r['captures'])==7 and bool(r['failures']) for r in runs),failure_counts=dict(counts),baseline_runs=len(baseline),baseline_valid=sum(not r['failures'] for r in baseline),baseline_max_penetration_m=max(r['max_penetration_m'] for r in baseline),all_implementation_hashes_match=not mismatches,implementation_hashes=hashes,stored_summary_total_runs=sum(x['runs'] for x in summary),stored_summary_valid_runs=sum(x['valid_runs'] for x in summary),stored_numerical_checks=len(num['checks']),stored_numerical_all_pass=all(num['checks'].values()),stored_system_checks=len(system['checks']),stored_system_all_pass=all(system['checks'].values()),independent_physical_validation=False)
 (EX/'saved_simulation_review.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 dump('operator_history_events.csv',[dict(event_date='2025-01-22',event_type='venue_amendment_effective',machine_id='UNKNOWN',ball_set_id='UNKNOWN',evidence_ids='R10',status='VERIFIED',notes='PDF page 15 amendment effect; source changes venue to floor 21 VTC Online, 18 Tam Trinh Hanoi. No asset replacement inferred.')])
 # Remove invisible word separators introduced by report composition.
 for p in OUT.glob('*.md'):
  text=p.read_text(encoding='utf-8');clean=text.replace('\u200b','').replace('\ufeff','')
  if text!=clean:p.write_text(clean,encoding='utf-8')
 for p in EX.glob('thread_*.json'):
  d=json.loads(p.read_text(encoding='utf-8'))
  if 'visible_item_type_counts' in d:d['visible_item_type_counts'].pop('reasoning',None)
  p.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
