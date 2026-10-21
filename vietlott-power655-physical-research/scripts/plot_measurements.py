"""Own scientific plots; no source video pixels embedded."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import read_csv
ROOT=Path(__file__).resolve().parents[1]
def main():
    out=ROOT/'charts';out.mkdir(exist_ok=True)
    rows=read_csv(ROOT/'measurements'/'draw_01372_857_appearance.csv')
    t=np.array([float(x['timestamp_seconds']) for x in rows]);a=np.array([float(x['candidate_appearance_angle_deg']) for x in rows]);amp=np.array([float(x['amplitude']) for x in rows])
    fig,axes=plt.subplots(2,1,figsize=(11,6),sharex=True,layout='constrained')
    axes[0].plot(t,a,lw=1);axes[0].set(ylabel='Candidate appearance phase / 3 (deg)',title='01372: unvalidated image signal — physical paddle RPM remains NA')
    axes[1].plot(t,amp,lw=1);axes[1].set(xlabel='Source PTS (s)',ylabel='Harmonic-3 amplitude (gray units)')
    fig.savefig(out/'appearance_phase.png',dpi=150);plt.close(fig)
    sp=read_csv(ROOT/'measurements'/'draw_01372_857_appearance_spectrum.csv');f=np.array([float(x['frequency_hz']) for x in sp]);p=np.array([float(x['power']) for x in sp])
    fig,ax=plt.subplots(figsize=(10,4),layout='constrained');ax.plot(f,p);ax.set(xlabel='Pattern frequency (Hz)',ylabel='Periodogram power',title='Same clip, second calculation: spectrum — no independent mechanical validation')
    ax.text(.98,.93,'Phase candidate 63.8 vs spectrum candidate 94.9 RPM\nThreefold symmetry assumed; disagreement retained',transform=ax.transAxes,ha='right',va='top',fontsize=9)
    fig.savefig(out/'appearance_spectrum.png',dpi=150);plt.close(fig)
    balls=read_csv(ROOT/'measurements'/'draw_01372_ball_tracking.csv');bx=np.array([float(x['center_x_px']) for x in balls]);by=np.array([float(x['center_y_px']) for x in balls])
    fig,ax=plt.subplots(figsize=(7,6),layout='constrained');hist=ax.hist2d(bx,by,bins=20,range=[[510,1410],[60,960]],cmap='viridis');ax.invert_yaxis();ax.set_aspect('equal');fig.colorbar(hist[3],ax=ax,label='Unlinked color-component detections')
    ax.set(xlabel='Source x (px)',ylabel='Source y (px)',title='109 unvalidated detections / 120 frames\nVisibility-biased sample; not ball occupancy probability')
    fig.savefig(out/'candidate_detection_density.png',dpi=150);plt.close(fig)
    print(json.dumps({'charts':['appearance_phase.png','appearance_spectrum.png','candidate_detection_density.png']}))
if __name__=='__main__':main()
