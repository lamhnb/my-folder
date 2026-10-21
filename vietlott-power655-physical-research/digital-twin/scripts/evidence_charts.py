"""Original schematics and timing charts; no third-party video pixels."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    rows=list(csv.DictReader((ROOT/'geometry/landmarks.csv').open()))
    fig,axs=plt.subplots(1,2,figsize=(11,5))
    for ax,sid in zip(axs,['IUU05082QtE','is8GgE2gQu8']):
        rr=[r for r in rows if r['source_id']==sid]
        for r in rr:
            x,y,u=map(float,[r['x_px'],r['y_px'],r['uncertainty_px']])
            ax.errorbar(x,y,xerr=u,yerr=u,fmt='o',ms=4)
            offsets={'hub_left':(-28,18),'hub_center':(-15,-20),'hub_right':(0,18)}
            ax.annotate(r['landmark'].replace('housing_front_','').replace('inner_rim_',''),(x,y),xytext=offsets.get(r['landmark'],(5,5)),textcoords='offset points',fontsize=7)
        if sid=='IUU05082QtE':
            ph=np.linspace(0,2*np.pi,100);ax.plot(859.5+420.5*np.cos(ph),549.5+437.5*np.sin(ph),ls='--',alpha=.5)
        ax.set(xlabel='native x / px',ylabel='native y / px',title=sid+' | approximate image landmarks')
        ax.invert_yaxis();ax.set_aspect('equal')
    fig.suptitle('Image geometry only: click ranges are not calibration accuracy');fig.tight_layout();fig.savefig(ROOT/'charts/image_landmarks.png',dpi=150);plt.close(fig)
    intervals=list(csv.DictReader((ROOT/'calibration/intervals.csv').open()))
    fig,ax=plt.subplots(figsize=(9,4))
    for j,draw in enumerate(['01372','01373','01374','01375','01376']):
        rr=[r for r in intervals if r['draw_id']==draw and r['role']=='main_interval']
        mid=np.array([float(r['midpoint_s']) for r in rr]);lo=np.array([float(r['lower_s']) for r in rr]);hi=np.array([float(r['upper_s']) for r in rr])
        xx=np.arange(1,6)+j*.045
        ax.errorbar(xx,mid,yerr=[mid-lo,hi-mid],fmt='o-',label=f'{draw} {rr[0]["partition"]}',alpha=.75,capsize=2)
    ax.axhline(13.1247783,ls='--',color='black',label='two-draw training mean')
    ax.set(xlabel='main-to-main interval index',ylabel='downstream appearance interval / s',title='Real Phase 2 proxies: neither isolation time nor RPM')
    ax.legend(fontsize=7,ncol=2);fig.tight_layout();fig.savefig(ROOT/'charts/video_cadence.png',dpi=150);plt.close(fig)
    # Bind manual coordinates to previously pinned source frame file hashes.
    provenance=[]
    for name in sorted(set(r['frame_relative_path'] for r in rows)):
        path=ROOT.parent/name
        ledger=path.parent/'frames.csv';expected=None
        if ledger.exists():
            matches=[r for r in csv.DictReader(ledger.open(encoding='utf-8-sig')) if Path(r['file']).name==path.name]
            if len(matches)==1:expected=matches[0]['sha256']
        actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        provenance.append({'path':name,'exists_locally':path.exists(),'sha256':actual,
                           'expected_prior_frame_ledger_sha256':expected,'matches_prior_frame_ledger':actual is not None and actual==expected,
                           'new_pixels_redistributed':False})
    (ROOT/'geometry/landmark_provenance.json').write_text(json.dumps(provenance,indent=2))
    if not all(r['matches_prior_frame_ledger'] for r in provenance):raise RuntimeError('Geometry source frame hash mismatch; do not use landmarks as verified pixel provenance')

if __name__=='__main__':main()
