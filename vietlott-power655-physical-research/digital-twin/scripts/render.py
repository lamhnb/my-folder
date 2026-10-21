"""Matplotlib 3D replay of stored states; no generated or interpolated ball tracks."""
import io
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import imageio.v2 as imageio
from simulator.geometry import arm_parts


def cuboid(half,pos,rotation=None):
    h=np.asarray(half);v=np.array([[x,y,z] for x in [-h[0],h[0]] for y in [-h[1],h[1]] for z in [-h[2],h[2]]])
    if rotation is not None:v=v@rotation.T
    v+=pos
    return [[v[i] for i in f] for f in [[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]]]


def rot(a):return np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])


def render(trajectory,out,c):
    data=np.load(trajectory);xyz=data['position'];times=data['time']
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    frames=[]
    # Store max 160 actual samples, shown at 12 fps (time compression labelled).
    indices=np.unique(np.linspace(0,len(times)-1,min(160,len(times))).astype(int))
    fig=plt.figure(figsize=(9,6),dpi=90);ax=fig.add_subplot(111,projection='3d')
    a=c['mouth_radius'];z=-np.sqrt(c['radius']**2-a*a);floor=z-c['pocket_height'];top=floor-.13
    phi=np.linspace(0,2*np.pi,48);theta=np.linspace(0,np.pi-np.arcsin(a/c['radius']),28)
    xx=c['radius']*np.outer(np.cos(phi),np.sin(theta));yy=c['radius']*np.outer(np.sin(phi),np.sin(theta))*c['depth_scale'];zz=c['radius']*np.outer(np.ones_like(phi),np.cos(theta))
    for count,k in enumerate(indices):
        ax.clear();ax.plot_wireframe(xx,yy,zz,rstride=5,cstride=5,color='#7b93a4',alpha=.25,linewidth=.5)
        balls=xyz[k];ax.scatter(balls[:,0],balls[:,1],balls[:,2],s=55,c=data['labels'],cmap='turbo',edgecolors='#333333',linewidths=.25,depthshade=True)
        angle=data['mechanism'][k,0] if 'mechanism' in data else c['rpm']*2*np.pi/60*times[k]
        for half,pos,local in arm_parts(c):
            vertices=cuboid(half,rot(angle)@np.array(pos),rot(angle+local))
            ax.add_collection3d(Poly3DCollection(vertices,facecolors='#df6b32',alpha=.7,linewidths=.1))
        gate=data['mechanism'][k,1:] if 'mechanism' in data else [0,0]
        for gz,gx in zip([z,floor],gate):
            ax.add_collection3d(Poly3DCollection(cuboid([a+.008,a+.008,.003],[gx,0,gz]),facecolors='#577d8c',alpha=.8))
        tubez=np.linspace(z-.13,z,2)
        for ph in np.linspace(0,2*np.pi,10):ax.plot([a*np.cos(ph)]*2,[a*np.sin(ph)]*2,tubez,color='gray',alpha=.5,linewidth=.7)
        for y in [-.05,.05]:ax.plot([-.08,.8],[y,y],[top+.08*.16,top-.8*.16],color='black',linewidth=2)
        ax.plot([-.08,.8],[0,0],[top+.08*.16,top-.8*.16],color='#4f7e66',linewidth=6,alpha=.4)
        ax.set(xlim=(-.36,.84),ylim=(-.36,.36),zlim=(-.72,.36),xlabel='x / m',ylabel='y / m',zlabel='z / m')
        ax.set_box_aspect((1.2,.72,1.08));ax.view_init(elev=17,azim=-68)
        ax.set_title(f'HYPOTHETICAL mechanism | t={times[k]:.2f} s\n55 rigid spheres, stored physics samples; compressed time',fontsize=10)
        fig.tight_layout()
        buf=io.BytesIO();fig.savefig(buf,format='png');buf.seek(0);frames.append(imageio.imread(buf))
        if count in [0,len(indices)//2,len(indices)-1]:
            fig.savefig(out.parent/f'{out.stem}_{count:03}.png',dpi=130)
    imageio.mimsave(out,frames,duration=1/12,loop=0);plt.close(fig)
    print(f'Rendered {len(frames)} actual states to {out}')
