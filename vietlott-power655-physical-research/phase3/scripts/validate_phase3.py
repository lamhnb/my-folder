"""Validate actual artifacts/source binding and run software tests; keep science gates separate."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path

import cv2
import numpy as np
import scipy

from extract_pilot import read_csv,sha
from order_tests import eligible_draws,validate_draw

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE='e55fd8dba5bac41c7c157a5a3bc0d7ff2718de7a'

def validate(redecode=False):
    rows=read_csv(ROOT/'draw_order_verified.csv');quality={r['draw_id']:r for r in read_csv(ROOT/'quality_audit.csv')}
    sources=read_csv(ROOT/'source_registry.csv');groups=defaultdict(list);checks=[]
    def check(name,condition,detail=''):
        checks.append(dict(name=name,passed=bool(condition),detail=detail))
    for r in rows:groups[r['draw_id']].append(r)
    check('35_rows_five_unique_draws',len(rows)==35 and len(groups)==5)
    for draw,group in groups.items():
        ordered,nums=validate_draw(group)
        check(f'{draw}_seven_distinct_valid_roles',True)
        s=next(s for s in sources if s['draw_id']==draw)
        check(f'{draw}_source_sha256',sha(s['local_input_path'])==s['source_sha256'])
        pub=json.loads((ROOT/'evidence'/'result_sources'/f'draw{draw}.json').read_text(encoding='utf-8'))['secondary']
        check(f'{draw}_secondary_set_reconciliation',pub['parser_status']=='parsed_seven' and set(nums[:6])==set(pub['published_numbers'][:6]) and nums[6]==pub['published_numbers'][6])
        for r in ordered:
            folder=(ROOT/r['evidence_image_path']).parent;frames=read_csv(folder/'frames.csv')
            check(f'{draw}_{r["capture_index"]}_bounds_bind_samples',r['readable_pts_start']==frames[0]['source_pts_seconds'] and r['readable_pts_end']==frames[1]['source_pts_seconds'])
            check(f'{draw}_{r["capture_index"]}_row_hash_binding',r['evidence_sha256']==frames[0]['evidence_sha256'] and r['source_sha256']==s['source_sha256'])
            for f in frames[:2]:
                path=ROOT/f['evidence_image_path'];im=cv2.imread(str(path))
                check(f'{draw}_{r["capture_index"]}_{f["sample_index"]}_native_image_and_hash',im is not None and im.shape==(1080,1920,3) and sha(path)==f['evidence_sha256'] and hashlib.sha256(im.tobytes()).hexdigest()==f['bgr_sha256'])
                check(f'{draw}_{r["capture_index"]}_{f["sample_index"]}_PTS_ticks',abs(int(f['pts_ticks'])/30000-float(f['source_pts_seconds']))<1e-6)
            log=json.loads((folder/'extraction.json').read_text())
            check(f'{draw}_{r["capture_index"]}_frozen_analysis',log['analysis_plan_sha256']==sha(ROOT/'analysis_plan.md'))
            if redecode:
                # Replay recorded command with 2 samples; compare native pixels, not PNG encoder output.
                cmd=log['command'].copy();cmd[cmd.index('-frames:v')+1]='2'
                replay=subprocess.run(cmd,capture_output=True,timeout=90)
                block=1920*1080*3
                check(f'{draw}_{r["capture_index"]}_source_redecode',replay.returncode==0 and len(replay.stdout)==2*block and all(hashlib.sha256(replay.stdout[i*block:(i+1)*block]).hexdigest()==frames[i]['bgr_sha256'] for i in range(2)))
    accepted,reasons=eligible_draws(rows,quality)
    check('all_current_rows_remain_provisional',len(accepted)==0 and all(r['verification_status']=='provisional_one_review' for r in rows))
    tests=read_csv(ROOT/'order_bias_tests.csv')
    check('primary_results_not_fabricated',len(tests)==5 and all(r['p_value']=='NA' and r['status']=='not_testable' and r['n_analyzed_draws']=='0' for r in tests))
    branch=subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],cwd=REPO,text=True).strip()
    check('correct_branch',branch=='research/power655-draw-order-phase3')
    changed=subprocess.check_output(['git','diff',BASE,'--name-only'],cwd=REPO,text=True).splitlines()
    check('protected_tracked_files_unchanged',all(p.startswith('vietlott-power655-physical-research/phase3/') for p in changed),str(changed))
    unit=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'scripts'),'-p','test_phase3.py','-v'],capture_output=True,text=True)
    (ROOT/'evidence'/'unit_test_output.txt').write_text(unit.stdout+unit.stderr,encoding='utf-8')
    check('unit_tests',unit.returncode==0)
    return dict(generated_utc=datetime.now(timezone.utc).isoformat(),base_commit=BASE,branch=branch,
        software_and_integrity_passed=all(c['passed'] for c in checks),checks=checks,
        sample_counts=dict(collected_distinct_draws=5,capture_rows=35,readable_primary_labels=35,
            native_frames_extracted=210,native_frames_published=70,fully_readable_single_reviewer_draws=5,
            fully_verified_two_review_official_draws=0,recognition_completion_fraction=1.,recognition_accuracy=None,
            independent_secondary_reviews=0,cross_review_agreement=None),
        scientific_gates=dict(A='physical_reading_complete_official_reconciliation_incomplete',
            B='independent_second_review_missing',C='historical_expansion_and_holdout_not_complete',
            primary_analysis_executed=False,predictive_evaluation_executed=False,target_100_draws_met=False),
        limitations=list(set(reasons.values()))+['official_numeric_result_HTTP_403','five_nonrandom_draws_only','no_equipment_ids','no_future_holdout'],
        source_redecode_verified=redecode,runtime=dict(python=platform.python_version(),numpy=np.__version__,opencv=cv2.__version__,scipy=scipy.__version__))

def main():
    p=argparse.ArgumentParser();p.add_argument('--redecode-evidence',action='store_true');a=p.parse_args()
    report=validate(a.redecode_evidence)
    (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
    if not report['software_and_integrity_passed']:raise SystemExit(1)
if __name__=='__main__':main()
