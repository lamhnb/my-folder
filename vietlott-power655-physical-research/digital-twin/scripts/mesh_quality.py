"""Audit the parameterized collision shell and export an equivalent welded mesh.

The clean OBJ is a CAD convenience artifact; the recorded experiments use the
original engine triangulation. Removing zero-area pole faces does not recover
unknown hardware geometry or certify the dynamics of a different mesh ordering.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
from simulator.geometry import shell
ROOT=Path(__file__).resolve().parents[1]


def main():
    c=json.loads((ROOT/'configs/baseline.json').read_text());v,f=shell(c);v=np.array(v)
    unique=[];lookup={};mapping=[]
    for q in v:
        key=tuple(np.round(q,12))
        if key not in lookup:lookup[key]=len(unique);unique.append(q)
        mapping.append(lookup[key])
    clean=[];degenerate=0
    for tri in f:
        q=v[tri];area2=np.linalg.norm(np.cross(q[1]-q[0],q[2]-q[0]))
        if area2<1e-14:degenerate+=1;continue
        clean.append([mapping[i] for i in tri])
    edges=Counter(tuple(sorted((tri[j],tri[(j+1)%3]))) for tri in clean for j in range(3))
    errors=[]
    # Inner surface is the first 2*nlat*nlon triangles. Its planes lie inside
    # the assumed ideal spherical surface; this is a geometric discretization bound.
    for tri in f[:2*c['mesh_lat']*c['mesh_lon']]:
        q=v[tri]/[1,c['depth_scale'],1];normal=np.cross(q[1]-q[0],q[2]-q[0]);nn=np.linalg.norm(normal)
        if nn<1e-14:continue
        distance=abs(np.dot(normal/nn,q[0]));errors.append(c['radius']-distance)
    lines=['# SI welded shell from baseline parameters, equivalent surface; not used for recorded engine runs']
    lines+=['v '+' '.join(f'{a:.12g}' for a in q) for q in unique]
    lines+=['f '+' '.join(str(a+1) for a in q) for q in clean]
    dest=ROOT/'geometry/chamber_clean.obj';dest.write_text('\n'.join(lines)+'\n')
    report={'raw_vertices':len(v),'raw_triangles':len(f),'zero_area_pole_triangles':degenerate,
      'welded_vertices':len(unique),'clean_triangles':len(clean),'all_clean_edges_have_two_incident_faces':all(n==2 for n in edges.values()),
      'clean_euler_characteristic':len(unique)-len(edges)+len(clean),
      'max_inner_facet_plane_sagitta_m':float(max(errors)),
      'clean_obj_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
      'scope':'discretization of assumed sphere only; no hardware dimension accuracy inferred',
      'limits':['Changing mouth radius also changes latitude tessellation; gate sensitivity is not isolated from mesh discretization.',
       'Clean export is not substituted into frozen engine runs; no claim of identical chaotic trajectories after mesh reordering.']}
    (ROOT/'geometry/mesh_quality.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if not report['all_clean_edges_have_two_incident_faces']:raise RuntimeError('Nonmanifold welded shell')

if __name__=='__main__':main()
