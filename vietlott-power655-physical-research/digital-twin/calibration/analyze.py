"""Cadence description with interval arithmetic and explicit nonidentifiability."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT.parent/'phase2/capture_event_audit.csv'
    rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
    partition={'01372':'calibration','01373':'calibration','01374':'validation','01375':'validation','01376':'retrospective_reserved'}
    output=[];drawmeans={}
    for draw,part in partition.items():
        rr=sorted([r for r in rows if r['draw_id']==draw],key=lambda r:int(r['capture_index']))
        intervals=[]
        for before,after in zip(rr,rr[1:]):
            key='trough_entry_visible_proxy_'
            lo=float(after[key+'lower_pts'])-float(before[key+'upper_pts'])
            hi=float(after[key+'upper_pts'])-float(before[key+'lower_pts'])
            role='to_special' if after['capture_type']=='special' else 'main_interval'
            output.append(dict(draw_id=draw,partition=part,interval_index=int(after['capture_index'])-1,
                               role=role,lower_s=lo,upper_s=hi,midpoint_s=(lo+hi)/2))
            if role=='main_interval':intervals.append((lo+hi)/2)
        drawmeans[draw]=float(np.mean(intervals))
    train=[drawmeans[d] for d in partition if partition[d]=='calibration']
    cadence=float(np.mean(train))
    with (ROOT/'calibration/intervals.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    split={'partitions':partition,'locked_before_this_analysis':True,
           'unseen_future_holdout':False,'reason':'All five draws were explored in earlier phases; retrospective reservation cannot undo exposure.',
           'no_outcome_labels_loaded':True,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT/'calibration/split.json').write_text(json.dumps(split,indent=2))
    # Constant latency cancels from differences. Cadence alone cannot recover omega,
    # restitution, friction, depth, mass, geometry or actual control/isolation times.
    params=['command_period','constant_transport_delay','omega','friction','restitution','depth']
    jac=np.zeros((10,len(params)));jac[:,0]=1
    summary={'scope':'downstream_proxy_cadence_only','training_draws':2,'validation_draws':2,
       'retrospective_reserved_draws':1,'cadence_training_mean_s':cadence,
       'training_draw_means_s':train,'all_draw_means_s':drawmeans,
       'validation_absolute_errors_s':{d:abs(drawmeans[d]-cadence) for d in ['01374','01375']},
       'reserved_absolute_error_s':abs(drawmeans['01376']-cadence),
       'jacobian_parameters':params,'reduced_observation_jacobian_rank':int(np.linalg.matrix_rank(jac)),
       'singular_values':np.linalg.svd(jac,compute_uv=False).tolist(),
       'interpretation':'Rank 1 of 6 in the explicit constant-latency cadence observation model. This is a structural counterexample, not a computed Jacobian of the full Bullet simulator.',
       'physical_parameters_identified':[], 'RPM_verified':False,'physical_calibration_passed':False,
       'limits':['Command timing and transport delay are unobserved, so even cadence is not verified command period.',
                 'Different physical parameter sets can share cadence if actuated at a common period.',
                 'No 3D trajectories or independent mass/friction/geometry data exist.',
                 'The five broadcasts do not supply a previously unseen prediction holdout.']}
    (ROOT/'calibration/identifiability.json').write_text(json.dumps(summary,indent=2))
    (ROOT/'configs/video_cadence.json').write_text(json.dumps({'capture_period':cadence,'max_seconds':130},indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
