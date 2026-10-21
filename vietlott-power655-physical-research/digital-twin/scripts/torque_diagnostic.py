"""Post-hoc actuator stress diagnostic, separate from the frozen 78-run study."""
import concurrent.futures
import json
import math
from pathlib import Path
from simulator.core import load_config,simulate
ROOT=Path(__file__).resolve().parents[1]


def worker(seed):
    r=simulate(load_config(ROOT/'configs/torque_diagnostic.json'),seed)
    path=ROOT/f'results/torque_diagnostic/seed{seed}.json'
    path.write_text(json.dumps(r,indent=2,allow_nan=False));return seed,r['failures']


def main():
    folder=ROOT/'results/torque_diagnostic';folder.mkdir(exist_ok=True)
    protocol={'status':'post_hoc_engineering_diagnostic','reason':'The completed78-run study showed positive-direction motor speed far below its request under load.',
       'seeds':[1000,1001,1002],'changed_parameter':{'motor_torque_N_m':30.},'baseline_motor_torque_N_m':3.,
       'scope':'Tenfold assumed actuator stress; not measured hardware torque or an independent confirmation. Baseline config is not changed.',
       'written_before_these_runs':True}
    (folder/'protocol.json').write_text(json.dumps(protocol,indent=2))
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for result in pool.map(worker,protocol['seeds']):print(result,flush=True)
    summarize()


def summarize():
    rows=[]
    for seed in [1000,1001,1002]:
        for scenario,path in [('baseline',ROOT/f'results/runs/baseline_seed{seed}.json'),
                              ('torque30',ROOT/f'results/torque_diagnostic/seed{seed}.json')]:
            r=json.loads(path.read_text());samples=[q[1] for q in r['rotor_samples_time_omega_torque_SI'] if q[0]>=r['config']['ramp_seconds']]
            rows.append({'scenario':scenario,'seed':seed,'requested_RPM':r['config']['rpm'],
                 'achieved_mean_RPM_post_ramp':sum(samples)/len(samples)*60/(2*math.pi),
                 'captures':len(r['captures']),'failures':r['failures'],'max_penetration_m':r['max_penetration_m']})
    result={'status':'post_hoc_diagnostic_not_primary_MC','runs':rows,
       'scope':'Paired motor-torque stress under assumed geometry; commands and achieved speed differ. No actual Vietlott torque/RPM inferred.'}
    (ROOT/'results/torque_diagnostic/summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
