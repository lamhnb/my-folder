"""Conservative measurement from audited marker annotations, no automatic ID claims.

Input points: frame_index,paddle_id,segment_id,center_x_px,center_y_px,
tip_x_px,tip_y_px,sigma_px,tracking_confidence. PTS from frame_manifest.csv.
Require a uniquely identifiable marker and a sampling bound justified externally.
Angles are projected screen angles unless --rectified-plane is asserted by calibration.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import numpy as np
from common import read_csv,write_csv,PADDLES

def estimate(t,wrapped,maximum_rpm,sigma_deg=None):
    t=np.asarray(t,float);wrapped=np.asarray(wrapped,float)
    if len(t)<3 or np.any(np.diff(t)<=0):raise ValueError('Need >=3 monotone PTS samples')
    if maximum_rpm<=0 or np.max(np.diff(t))*maximum_rpm*6>=180:
        raise ValueError('Sampling cannot exclude >180 degree alias under supplied RPM bound')
    angle=np.rad2deg(np.unwrap(np.deg2rad(wrapped)))
    if np.any(np.abs(np.diff(angle)/np.diff(t))>maximum_rpm*6+1e-8):raise ValueError('Observed motion exceeds declared bound; review IDs/alias')
    omega=np.gradient(angle,t);coef=np.polyfit(t-t[0],angle,1);rpm=coef[0]/6
    # Second method: same-marker full-turn crossings, not an independent sensor.
    direction=1 if coef[0]>=0 else -1;a=direction*angle
    crossings=[]
    if np.all(np.diff(a)>0):
        for level in np.arange(np.ceil(a[0]/360)*360,a[-1],360):
            crossings.append(float(np.interp(level,a,t)))
    cycle_rpm=float(direction*60/np.mean(np.diff(crossings))) if len(crossings)>=3 else None
    residual=angle-np.polyval(coef,t-t[0])
    return angle,omega,{'slope_rpm_signed':float(rpm),'cycle_rpm_signed':cycle_rpm,'cycle_count':max(0,len(crossings)-1),
        'apparent_rpm_cv':float(np.std(omega)/abs(np.mean(omega))) if np.mean(omega)!=0 else None,
        'fit_residual_deg_rms':float(np.sqrt(np.mean(residual**2))),
        'bound_rpm_external':maximum_rpm,'sigma_angle_deg_median':float(np.median(sigma_deg)) if sigma_deg is not None else None,
        'uncertainty_note':'Pixel uncertainty only; perspective, blur, calibration, PTS and alias systematics separate. No empirical CI inferred.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('points',type=Path);ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--draw-id',required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--maximum-rpm',type=float,required=True);ap.add_argument('--unique-marker-confirmed',action='store_true',required=True)
    ap.add_argument('--rectified-plane',action='store_true');args=ap.parse_args()
    if args.out.exists():raise SystemExit('Refusing overwrite')
    times={int(x['frame_index']):float(x['timestamp_seconds']) for x in read_csv(args.manifest)};groups=defaultdict(list)
    for r in read_csv(args.points):groups[(r['segment_id'],r['paddle_id'])].append(r)
    rows=[];summaries=[]
    for (seg,pad),g in groups.items():
        g.sort(key=lambda r:int(r['frame_index']));t=[times[int(r['frame_index'])] for r in g]
        dx=np.array([float(r['tip_x_px'])-float(r['center_x_px']) for r in g]);dy=np.array([float(r['center_y_px'])-float(r['tip_y_px']) for r in g])
        radii=np.hypot(dx,dy)
        if np.any(radii<=0):raise ValueError('Zero radius marker')
        wrapped=np.rad2deg(np.arctan2(dy,dx));sigma=np.rad2deg(np.sqrt(2)*np.array([float(r['sigma_px']) for r in g])/radii)
        angle,omega,summary=estimate(t,wrapped,args.maximum_rpm,sigma)
        summary.update(segment_id=seg,paddle_id=pad,angle_space='rectified_rotation_plane' if args.rectified_plane else 'projected_screen',direction_convention='positive counterclockwise in image')
        summaries.append(summary)
        for i,r in enumerate(g):rows.append(dict(zip(PADDLES,[args.draw_id,t[i],int(r['frame_index']),pad,float(angle[i]),float(omega[i]),float(omega[i]/6),float(r['tracking_confidence'])])))
    write_csv(args.out,PADDLES,rows)
    args.out.with_suffix('.summary.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
if __name__=='__main__':main()
