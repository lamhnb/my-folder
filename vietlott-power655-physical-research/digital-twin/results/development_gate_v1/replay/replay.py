import argparse,json
from pathlib import Path
from simulator.core import load_config,simulate
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=1004);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
if a.out.exists():raise SystemExit('Refuse overwrite; choose a new output file')
r=simulate(load_config(),a.seed);a.out.write_text(json.dumps(r,indent=2));print(r['failures'],r['max_penetration_m'])
