"""Physical checks on the actual 55-body chamber; retain failed results."""
import json
from pathlib import Path
import numpy as np
import pybullet as p
from simulator.core import Twin,load_config,simulate
ROOT=Path(__file__).resolve().parents[1]


def jam_check(jam,c):
    return (len(jam['captures'])==0 and jam['remaining']==55 and jam['remaining_in_chamber']==55 and
            'incomplete_seven' in jam['failures'] and not jam['uncollected_exit_ids'] and
            'escaped_body' not in jam['failures'] and jam['max_penetration_m']<=c['penetration_limit'])


def run_system():
    c=load_config()
    r=simulate(c,0,ROOT/'results/seed0.npz')
    (ROOT/'results/seed0.json').write_text(json.dumps(r,indent=2))
    # Deliberate geometric jam: aperture smaller than the ball radius.
    jam=simulate(load_config(mouth_radius=.020,max_seconds=8,mix_seconds=1),901)
    (ROOT/'validation/jam.json').write_text(json.dumps(jam,indent=2))
    xyz=np.array(r['final_positions']);distance=np.linalg.norm(xyz[:,None]-xyz[None,:],axis=2);np.fill_diagonal(distance,np.inf)
    checks={'seven':len(r['captures'])==7,'no_duplicate':len(set(r['physical_ids']))==len(r['physical_ids']),
       'six_main_then_special':[x['role'] for x in r['captures']]==['main']*6+['special'],
       'special_from_remaining_49':len(r['pre_capture'])==7 and r['pre_capture'][6]['remaining_before']==49,
       '49_after_six':len(r['captures'])>=6 and r['captures'][5]['remaining']==49,
       '48_after_seven':r['remaining']==48,'48_physically_in_chamber':r['remaining_in_chamber']==48,
       'no_unauthorized_exit':not r['uncollected_exit_ids'],
       'body_conservation':r['body_count']==89,
       'penetration':r['max_penetration_m']<=c['penetration_limit'],
       'ball_overlap':r['max_ball_overlap_m']<=c['penetration_limit'],
       'no_coincident_centers':float(distance.min())>2*c['ball_radius']-c['penetration_limit'],
       'no_escape':not any(x in r['failures'] for x in ['escaped_body','unauthorized_exit']),
       'jam_fails_closed':jam_check(jam,c)}
    return {'passed':all(checks.values()),'checks':checks,'baseline_seed':0,'minimum_final_center_separation_m':float(distance.min()),
            'baseline_failures':r['failures'],'max_penetration_m':r['max_penetration_m'],
            'jam_failures':jam['failures'],'scope':'one_baseline_seed_plus_forced_geometric_jam; ensemble has its own quality gate'}
