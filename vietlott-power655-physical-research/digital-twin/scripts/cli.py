"""Command line entry point; paths are relative to digital-twin unless specified."""
import argparse
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.core import load_config,simulate


def write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(description='Assumption-explicit Power 6/55 rigid body research simulator')
    sub=ap.add_subparsers(dest='command',required=True)
    run=sub.add_parser('run');run.add_argument('--seed',type=int,default=0);run.add_argument('--config',type=Path)
    run.add_argument('--out',type=Path,default=ROOT/'results/seed0.json');run.add_argument('--trajectory',type=Path)
    sub.add_parser('validate');sub.add_parser('experiment');sub.add_parser('calibrate');sub.add_parser('report')
    mc=sub.add_parser('monte-carlo');mc.add_argument('--seeds',type=int,default=20);mc.add_argument('--config',type=Path)
    mc.add_argument('--out',type=Path,default=ROOT/'results/monte_carlo.json');mc.add_argument('--start',type=int,default=1000)
    render=sub.add_parser('render');render.add_argument('--trajectory',type=Path,default=ROOT/'results/seed0.npz')
    render.add_argument('--out',type=Path,default=ROOT/'renders/seed0.gif');render.add_argument('--config',type=Path)
    sub.add_parser('geometry')
    tracks=sub.add_parser('export-tracks');tracks.add_argument('--trajectory',type=Path,default=ROOT/'results/seed0.npz')
    tracks.add_argument('--out',type=Path,default=ROOT/'results/trajectory.csv')
    args=ap.parse_args()
    if args.command=='run':
        c=load_config(args.config);r=simulate(c,args.seed,args.trajectory);write(args.out,r)
        print(json.dumps({k:r[k] for k in ['seed','seconds','remaining','max_penetration_m','failures']}))
        return
    if args.command=='export-tracks':
        import csv
        import numpy as np
        d=np.load(args.trajectory)
        times,labels,positions,velocities=[d[k] for k in ['time','labels','position','velocity']]
        with args.out.open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['time_s','physical_id','label','x_m','y_m','z_m','vx_m_s','vy_m_s','vz_m_s'])
            for k,t in enumerate(times):
                for i in range(55):w.writerow([t,i,int(labels[i]),*positions[k,i],*velocities[k,i]])
        print(args.out)
        return
    if args.command=='monte-carlo':
        for name in ['numerical','system']:
            if not json.loads((ROOT/f'validation/{name}.json').read_text())['passed']:
                raise RuntimeError('Validation gate failed: '+name)
        c=load_config(args.config);rows=[]
        for seed in range(args.start,args.start+args.seeds):
            r=simulate(c,seed);rows.append(r);write(args.out,{'config':c,'runs':rows})
            print(seed,len(r['captures']),r['failures'],flush=True)
        return
    if args.command=='validate':
        from validation.numerical import run_numerical
        r=run_numerical();write(ROOT/'validation/numerical.json',r);print(json.dumps(r['checks']))
        # Failure blocks MC and experiments; full-system physical gate reported separately.
        if not r['passed']:raise SystemExit(2)
        from validation.system import run_system
        r=run_system();write(ROOT/'validation/system.json',r);print(json.dumps(r['checks']))
        if not r['passed']:raise SystemExit(3)
    elif args.command=='geometry':
        from simulator.geometry import export_obj
        export_obj(load_config(),ROOT/'geometry/chamber.obj')
    elif args.command=='render':
        from scripts.render import render
        render(args.trajectory,args.out,load_config(args.config))
    elif args.command=='calibrate':
        from calibration.analyze import main
        main()
    elif args.command=='experiment':
        from experiments.run import main
        main()
    elif args.command=='report':
        from scripts.report import main
        main()

if __name__=='__main__':main()
