"""Locked small research ensemble. Each Bullet process has a separate client.

This is an engineering sensitivity sweep, not a statistical power study or
model of actual pre-draw information. Failures remain in every denominator.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from simulator.core import load_config,simulate
ROOT=Path(__file__).resolve().parents[1]


def worker(job):
    name,seed,updates=job
    cfg=load_config(**updates)
    out=ROOT/'results/runs'/f'{name}_seed{seed}.json';out.parent.mkdir(exist_ok=True,parents=True)
    trace=ROOT/'results'/f'{name}_seed{seed}.npz' if name in ['baseline','jitter'] and seed==1000 else None
    report=simulate(cfg,seed,trace)
    out.write_text(json.dumps(report,indent=2,allow_nan=False))
    return name,seed,len(report['captures']),report['failures']


def jobs():
    configurations={
      'baseline':{},
      'rpm15':{'rpm':15.},'rpm45':{'rpm':45.},
      'friction_low':{'friction':.07,'rolling_friction':0.0002},
      'friction_high':{'friction':.45,'rolling_friction':.003},
      'elastic_low':{'restitution':.25},'elastic_high':{'restitution':.8},
      'mouth_narrow':{'mouth_radius':.029},'mouth_wide':{'mouth_radius':.037},
      'pocket_deep':{'pocket_height':.070},
      'loading_top':{'loading':'top_layer'},
      'ball_tolerances':{'diameter_tolerance':.001,'mass_tolerance':.000617},
      'depth_shallow':{'depth_scale':.8},
      'jitter':{'initial_jitter':1e-7},
      'label_shift':{'label_shift':17},
      'insertion_reverse':{'reverse_insertion':True},
      'dt_half':{'dt':.00025},'dt_double':{'dt':.001},
      'solver40':{'solver_iterations':40},'solver160':{'solver_iterations':160},
      'repeat':{},'reverse_rotation':{'rpm':-25.}
      ,'mirror_y':{'mirror_y':True}
    }
    result=[]
    for name,updates in configurations.items():
        count=20 if name=='baseline' else 3 if name not in ['jitter','label_shift','insertion_reverse','repeat'] else 1
        result.extend((name,1000+i,updates) for i in range(count))
    return configurations,result


def main(workers=8):
    numerical=json.loads((ROOT/'validation/numerical.json').read_text())
    system=json.loads((ROOT/'validation/system.json').read_text())
    if not numerical['passed'] or not system['passed']:raise RuntimeError('Numerical and baseline physical validation gates must pass before ensemble')
    conf,plan=jobs()
    protocol={'configurations':conf,'jobs':plan,'seed_rule':'1000 + replication index; paired across configurations',
       'baseline_count':20,'unpowered_per_number_bias':True,
       'development_exposed_baseline_seeds':list(range(1000,1008)),
       'new_baseline_seeds_after_controller_repair':list(range(1008,1020)),
       'blind_validation':False,
       'convergence_thresholds':{'paired_mean_main_interval_relative':.05,'paired_mean_rms_speed_relative':.15,
                                 'penetration_m':.002,'all_compared_runs_physical_valid':True},
       'analysis':'All jobs retained. Compare per-run completion, wait/entry times, rms speed, penetration; paired differences. Label shift must preserve physical trajectories exactly. Insertion reverse need not preserve chaotic trajectory; report as solver-order sensitivity.',
       'fixed_before_execution':True}
    (ROOT/'experiments/protocol.json').write_text(json.dumps(protocol,indent=2))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        fut={pool.submit(worker,job):job for job in plan}
        for f in concurrent.futures.as_completed(fut):
            print(f.result(),flush=True)

if __name__=='__main__':main()
