import json
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.core import simulate,load_config
from simulator.geometry import initial_positions


def test_run_report_serializes_all_values():
    r=simulate(load_config(max_seconds=.01),109)
    j=json.loads(json.dumps(r,allow_nan=False))
    assert j['remaining_in_chamber']==55
    assert j['body_count']==89


def test_y_reflection_preserves_initial_pair_distances():
    a=initial_positions(load_config(),71);b=initial_positions(load_config(mirror_y=True),71)
    assert np.allclose(a*np.array([1,-1,1]),b,rtol=0,atol=0)
    assert np.allclose(np.linalg.norm(a[:,None]-a[None,:],axis=2),np.linalg.norm(b[:,None]-b[None,:],axis=2))
