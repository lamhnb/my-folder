"""Close-up 3D cutaway of actual saved collector states, no invented trajectories."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from scripts.render import cuboid
ROOT=Path(__file__).resolve().parents[1]


def main():
    r=json.loads((ROOT/'results/seed0.json').read_text());c=r['config']
    d=np.load(ROOT/'results/seed0.npz');ts=d['time'];positions=d['position'];mechanism=d['mechanism'];radii=d['radii']
    z=-np.sqrt(c['radius']**2-c['mouth_radius']**2);floor=z-c['pocket_height'];a=c['mouth_radius'];w=a+.008;hh=c['gate_thickness']/2
    vv=np.array([[x,y,zz] for x,zz in [(-w,-hh),(-w,0),(w,.012),(w,-hh)] for y in [-w,w]])
    hull=ConvexHull(vv)
    fig=plt.figure(figsize=(13,5),dpi=140)
    phi=np.linspace(0,2*np.pi,16);theta=np.linspace(0,np.pi,10)
    for j,phase in enumerate(['ADMIT','HOLD','RELEASE']):
        state=next(q for q in r['states'] if q['phase']==phase)
        offset_time=.35 if phase=='RELEASE' else .2
        k=min(len(ts)-1,np.searchsorted(ts,state['time']+offset_time));ax=fig.add_subplot(1,3,j+1,projection='3d')
        pts=positions[k]
        for i,q in enumerate(pts):
            if q[2]>z+.1 or q[2]<floor-.09 or np.linalg.norm(q[:2])>.11:continue
            rr=radii[i]
            xx=q[0]+rr*np.outer(np.cos(phi),np.sin(theta));yy=q[1]+rr*np.outer(np.sin(phi),np.sin(theta));zz=q[2]+rr*np.outer(np.ones_like(phi),np.cos(theta))
            ax.plot_surface(xx,yy,zz,color='#dfa833',linewidth=0,alpha=.9)
        offset=np.array([mechanism[k,1],0,z])
        ax.add_collection3d(Poly3DCollection([vv[face]+offset for face in hull.simplices],facecolors='#34556c',alpha=.65,edgecolors='#233f4f',linewidths=.3))
        ax.add_collection3d(Poly3DCollection(cuboid([w,w,hh],[mechanism[k,2],0,floor]),facecolors='#577d8c',alpha=.65))
        for ph in np.linspace(0,2*np.pi,12,endpoint=False):
            ax.plot([a*np.cos(ph)]*2,[a*np.sin(ph)]*2,[z-.12,z+.002],color='#8b9298',alpha=.4,lw=.6)
        for zz in [z,floor]:ax.plot(a*np.cos(phi),a*np.sin(phi),np.full_like(phi,zz),color='#7b888f',alpha=.6)
        ax.set(xlim=(-.065,.15),ylim=(-.065,.065),zlim=(floor-.13,z+.10),xlabel='x / m',ylabel='y / m',zlabel='z / m',title=f'{phase} | actual saved t={ts[k]:.2f}s')
        ax.set_xticks([-.05,.05,.15]);ax.set_yticks([-.05,0,.05]);ax.set_zticks([-.5,-.4,-.3])
        ax.view_init(elev=18,azim=-62);ax.set_box_aspect((.215,.13,.29))
    fig.suptitle('Hypothetical two-gate escapement: contact support, isolation, release\nCutaway view; ball surfaces use stored radii and centers, not a recovered hardware model',fontsize=11)
    fig.tight_layout();fig.savefig(ROOT/'renders/collector_states.png');plt.close(fig)

if __name__=='__main__':main()
