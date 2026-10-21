"""Recover the old gate-controller source and require its recorded byte hash.

This is an inverse-patch recovery after the failure, not a claim that the old
source had already been committed. No archive is accepted without the exact
SHA recorded by the eight original engine runs.
"""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    source=(ROOT/'simulator/core.py').read_bytes().decode('utf-8')
    source=source.replace('        old_gate=self.gate_open;old_floor=self.floor_open\n','')
    start=source.index('            # A contact-limited actuator pauses')
    end=source.index('            if self.gate_open==0:',start)
    source=source[:start]+"            self.gate_open=max(0,self.gate_open-c['gate_speed']*dt)\n"+source[end:]
    source=source.replace('        p.resetBaseVelocity(self.upper,[(self.gate_open-old_gate)/dt,0,0])',
       "        p.resetBaseVelocity(self.upper,[c['gate_speed'] if self.phase=='ADMIT' and self.gate_open<.11 else\n                                       -c['gate_speed'] if self.phase=='ISOLATE' and self.gate_open>0 else 0,0,0])")
    source=source.replace('        p.resetBaseVelocity(self.lower,[(self.floor_open-old_floor)/dt,0,0])',
       "        p.resetBaseVelocity(self.lower,[c['gate_speed'] if self.phase=='RELEASE' and self.floor_open<.11 else\n                                       -c['gate_speed'] if self.phase=='RESET' and self.floor_open>0 else 0,0,0])")
    old=json.loads((ROOT/'results/development_gate_v1/baseline_seed1004.json').read_text())
    expected=old['implementation_sha256']['core.py'];actual=hashlib.sha256(source.encode()).hexdigest()
    if actual!=expected:raise RuntimeError(f'Old source not recovered exactly: {actual} != {expected}')
    package=ROOT/'results/development_gate_v1/replay';(package/'simulator').mkdir(exist_ok=True,parents=True);(package/'configs').mkdir(exist_ok=True)
    (package/'simulator/core.py').write_bytes(source.encode())
    for name in ['geometry.py','__init__.py']:(package/'simulator'/name).write_bytes((ROOT/'simulator'/name).read_bytes())
    (package/'configs/baseline.json').write_text(json.dumps(old['config'],indent=2))
    (package/'replay.py').write_text('''import argparse,json
from pathlib import Path
from simulator.core import load_config,simulate
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=1004);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
if a.out.exists():raise SystemExit('Refuse overwrite; choose a new output file')
r=simulate(load_config(),a.seed);a.out.write_text(json.dumps(r,indent=2));print(r['failures'],r['max_penetration_m'])
''')
    (package/'source_recovery.json').write_text(json.dumps({'method':'inverse patch after failure; exact SHA matched recorded original run',
         'expected_core_sha256':expected,'recovered_core_sha256':actual,
         'geometry_sha256':hashlib.sha256((package/'simulator/geometry.py').read_bytes()).hexdigest(),
         'not_preexisting_github_prototype':True},indent=2))
    print('Recovered old source byte-exact:',actual)

if __name__=='__main__':main()
