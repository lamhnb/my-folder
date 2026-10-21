"""SI geometry shared by collision engine, OBJ export, and rendering.

The aperture and two-gate escapement are hypotheses, not recovered hardware.
"""
import math
from pathlib import Path
import numpy as np


def shell(c):
    radius, a = c['radius'], c['mouth_radius']
    end = math.pi - math.asin(a / radius)
    vertices, faces = [], []
    # Inner and outer surfaces, both truncated at the same opening plane.
    for offset in [0, c['wall_thickness']]:
        for i in range(c['mesh_lat'] + 1):
            theta = end * i / c['mesh_lat']
            for j in range(c['mesh_lon']):
                phi = 2 * math.pi * j / c['mesh_lon']
                r = radius + offset
                vertices.append([r*math.sin(theta)*math.cos(phi),
                                 r*math.sin(theta)*math.sin(phi)*c['depth_scale'],
                                 r*math.cos(theta)])
    n = (c['mesh_lat'] + 1)*c['mesh_lon']
    for layer in [0, 1]:
        for i in range(c['mesh_lat']):
            for j in range(c['mesh_lon']):
                p=layer*n+i*c['mesh_lon']+j
                q=layer*n+i*c['mesh_lon']+(j+1)%c['mesh_lon']
                u=p+c['mesh_lon']; v=q+c['mesh_lon']
                faces.extend([[p,q,u],[q,v,u]] if layer else [[p,u,q],[q,u,v]])
    # Opening lip closes the shell thickness, never caps the outlet.
    for j in range(c['mesh_lon']):
        p=c['mesh_lat']*c['mesh_lon']+j
        q=c['mesh_lat']*c['mesh_lon']+(j+1)%c['mesh_lon']
        faces.extend([[p,q,p+n],[q,q+n,p+n]])
    return vertices, faces


def arm_parts(c):
    """Three curved box chains, spaced 120 degrees, one assumed horizontal axis."""
    parts=[]
    for k in range(3):
        angle=k*2*math.pi/3
        for j in range(5):
            r0=0.035+j*(c['arm_length']-0.035)/5
            r1=0.035+(j+1)*(c['arm_length']-0.035)/5
            x=(r0+r1)/2
            z=c['arm_curve']*(x/c['arm_length'])**2
            # rotate local x,z in physical x,z plane
            pos=[x*math.cos(angle)+z*math.sin(angle),0,
                 -x*math.sin(angle)+z*math.cos(angle)]
            parts.append(([.5*(r1-r0)+.001,c['arm_depth']/2,c['arm_width']/2],pos,angle))
    return parts


def initial_positions(c, seed):
    rng=np.random.default_rng(seed)
    positions=[]
    spacing=2*(c['ball_radius']+c['diameter_tolerance']/2)+.002
    for _ in range(200000):
        p=rng.uniform(-c['radius']*.78,c['radius']*.78,3)
        p[1]*=c['depth_scale']
        if c['loading']=='top_layer': p[2]=abs(p[2])*.5+.08
        if np.linalg.norm(p/[1,c['depth_scale'],1])>c['radius']-spacing: continue
        # Loading ensemble is above all arm volumes (in y), or clear of swept hub.
        if abs(p[1])<c['arm_depth']/2+c['ball_radius']+.012: continue
        if all(np.linalg.norm(p-q)>spacing for q in positions): positions.append(p)
        if len(positions)==55: break
    if len(positions)!=55: raise ValueError('Cannot pack 55 nonoverlapping spheres')
    positions=np.asarray(positions)
    positions[0,0]+=c['initial_jitter']
    if c.get('mirror_y',False): positions[:,1]*=-1
    return positions


def export_obj(c, path):
    v,f=shell(c)
    lines=['# Hypothetical SI collision chamber; not manufacturer CAD']
    lines += ['v '+' '.join(f'{x:.9f}' for x in p) for p in v]
    lines += ['f '+' '.join(str(x+1) for x in t) for t in f]
    Path(path).write_text('\n'.join(lines)+'\n',encoding='utf-8')
