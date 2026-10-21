import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.core import Twin,load_config
from simulator.geometry import initial_positions,shell


def test_nonoverlapping_load_and_repeatability():
    c=load_config();a=initial_positions(c,77);b=initial_positions(c,77)
    assert np.array_equal(a,b)
    d=np.linalg.norm(a[:,None]-a[None,:],axis=2);np.fill_diagonal(d,np.inf)
    assert d.min()>2*c['ball_radius']
    assert np.max(np.linalg.norm(a,axis=1))<c['radius']-c['ball_radius']


def test_invalid_time_rejected():
    with pytest.raises(ValueError):load_config(dt=0)


def test_shell_has_open_aperture():
    c=load_config();v,f=shell(c);v=np.array(v)
    # A cap would include a vertex on the axis near the lower pole.
    assert not np.any((np.linalg.norm(v[:,:2],axis=1)<.001)&(v[:,2]<0))
    assert len(f)>1000


def test_admission_never_selects_nearest_sphere_without_contact():
    twin=Twin(load_config(),1)
    try:
        twin.t=8;twin.set_phase('ADMIT')
        # Controller sees synthetic coordinates at the pocket, but engine has no
        # supporting contact there. Coordinate proximity alone cannot latch a ball.
        fake=twin.positions();fake[0]=[0,0,twin.floor_z+.025]
        twin.controller(fake)
        assert twin.held is None and not twin.captured and twin.phase=='ADMIT'
    finally:twin.close()


def test_label_permutation_does_not_change_initial_geometry():
    a=Twin(load_config(),2)
    try:pa=a.positions();labels=a.labels
    finally:a.close()
    b=Twin(load_config(label_shift=17),2)
    try:
        assert np.array_equal(pa,b.positions())
        assert b.labels==[1+(x-1+17)%55 for x in labels]
    finally:b.close()


def test_all_55_rigid_bodies_exist_during_motor_steps():
    twin=Twin(load_config(),7)
    try:
        for _ in range(50):twin.step()
        assert len(twin.balls)==len(set(twin.balls))==55
        assert not twin.captured
        assert twin.max_ball_overlap<.002
    finally:twin.close()


def test_actuator_pauses_at_measured_contact_penetration():
    import pybullet as p
    twin=Twin(load_config(),4)
    try:
        twin.gate_open=.02;twin.set_phase('ISOLATE')
        p.resetBasePositionAndOrientation(twin.upper,[.02,0,twin.z],[0,0,0,1])
        p.resetBasePositionAndOrientation(twin.balls[0],[0,0,twin.z+.01],[0,0,0,1])
        p.performCollisionDetection()
        depth=max(max(0,-cp[8]) for cp in p.getContactPoints(twin.upper))
        assert depth>twin.c['gate_pause_depth']
        twin.controller(twin.positions())
        assert twin.gate_open==.02
        assert p.getBaseVelocity(twin.upper)[0]==(0,0,0)
    finally:twin.close()
