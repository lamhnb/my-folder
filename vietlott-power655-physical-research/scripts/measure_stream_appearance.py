"""Exploratory appearance signals, not certified paddle RPM or physical ball IDs.

Read non-DRM public native frames into RAM, crop WITHOUT resizing, retain source
PTS and scalar measurements, discard pixels. CLI parameters are part of provenance.
The harmonic symmetry is a hypothesis, not a recovered machine parameter.
"""
import argparse,datetime,hashlib,json,re,subprocess
from pathlib import Path
import cv2,numpy as np
from scipy.signal import periodogram
from inspect_stream import metadata,stream_url
from media_bridge import Bridge
from common import write_csv,BALLS
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--draw-id',required=True)
    ap.add_argument('--start',type=float,required=True);ap.add_argument('--count',type=int,default=120)
    ap.add_argument('--roi',type=int,nargs=4,required=True);ap.add_argument('--center',type=float,nargs=2,required=True)
    ap.add_argument('--annulus',type=float,nargs=2,required=True);ap.add_argument('--harmonic',type=int,default=3)
    args=ap.parse_args();info,_=metadata(args.video_id);f=stream_url(info);x,y,w,h=args.roi
    if args.count<3 or args.count>300 or w*h>1_000_000:raise SystemExit('Bounded clip only')
    prefix=f'draw_{args.draw_id}_{args.start:g}_appearance'
    out=ROOT/'measurements';out.mkdir(parents=True,exist_ok=True)
    if (out/(prefix+'.json')).exists():raise SystemExit('Refusing overwrite of prior run')
    with Bridge(f['url']) as b:
        p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-ss',str(args.start),'-copyts','-i',b.url,'-an',
            '-vf',f'showinfo,crop={w}:{h}:{x}:{y}','-frames:v',str(args.count),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        pts=[float(v) for v in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)',p.stderr.decode(errors='replace'))]
        n=len(p.stdout)//(w*h*3);pts=np.array(pts[:n]);ims=np.frombuffer(p.stdout,np.uint8).reshape(n,h,w,3)
        if n!=args.count or len(pts)!=n or np.any(np.diff(pts)<=0):raise RuntimeError('Incomplete decode or invalid PTS; no valid measurement run')
        transport={'bytes_sent':b.bytes_sent,'errors':b.errors}
    cx,cy=args.center;radii=np.linspace(*args.annulus,120);phi=np.linspace(0,2*np.pi,360,endpoint=False)
    mx=(cx+radii[:,None]*np.cos(phi)[None,:]).astype(np.float32);my=(cy-radii[:,None]*np.sin(phi)[None,:]).astype(np.float32)
    profiles=[];balls=[];hashes=[];yellow_areas=[]
    for i,im in enumerate(ims):
        hashes.append(hashlib.sha256(im.tobytes()).hexdigest())
        hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV);mask=cv2.inRange(hsv,np.array([18,75,65]),np.array([42,255,255]))
        yellow_areas.append(int(np.count_nonzero(mask)))
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
        polar=cv2.remap(gray,mx,my,cv2.INTER_LINEAR);valid=cv2.remap((mask==0).astype(np.float32),mx,my,cv2.INTER_NEAREST)
        profiles.append(np.sum(polar*valid,axis=0)/np.maximum(valid.sum(axis=0),1))
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area=cv2.contourArea(c);per=cv2.arcLength(c,True)
            if area<350 or area>7000 or per==0 or 4*np.pi*area/per**2<.45:continue
            (a,d),r=cv2.minEnclosingCircle(c)
            if not 12<=r<=55:continue
            balls.append(dict(zip(BALLS,[args.draw_id,float(pts[i]),None,f'unlinked_frame{i:04d}_detection{len(balls):06d}',float(a+x),float(d+y),float(r),None,None])))
    profiles=np.asarray(profiles);moving=profiles-np.median(profiles,axis=0)
    coeff=moving@np.exp(1j*args.harmonic*phi)/len(phi)
    phase=np.unwrap(np.angle(coeff))/args.harmonic;candidate=np.rad2deg(phase)
    slope=np.polyfit(pts-pts[0],candidate,1)[0]/6
    fs=1/np.median(np.diff(pts));freq,power=periodogram(coeff.real,fs=fs,window='hann',detrend='linear')
    valid=(freq>.5)&(freq<fs/2);peak=float(freq[valid][np.argmax(power[valid])]);spectral_rpm=peak*60/args.harmonic
    rows=[]
    for i,t in enumerate(pts):rows.append({'draw_id':args.draw_id,'source_id':args.video_id,'timestamp_seconds':float(t),'clip_frame_index':i,
        'source_frame_index':None,'harmonic':args.harmonic,'coefficient_real':float(coeff[i].real),'coefficient_imag':float(coeff[i].imag),
        'amplitude':float(abs(coeff[i])),'candidate_appearance_angle_deg':float(candidate[i]),'yellow_mask_area_px':yellow_areas[i],
        'native_crop_bgr_sha256':hashes[i]})
    write_csv(out/(prefix+'.csv'),list(rows[0]),rows)
    write_csv(out/(f'draw_{args.draw_id}_ball_tracking.csv'),BALLS,balls)
    write_csv(out/(prefix+'_spectrum.csv'),['frequency_hz','power'],[{'frequency_hz':float(a),'power':float(v)} for a,v in zip(freq,power)])
    result={'status':'exploratory_unvalidated_appearance_only','arguments':vars(args),'source_format_id':f['format_id'],
        'source_width':f.get('width'),'source_height':f.get('height'),'fps_metadata':f.get('fps'),'sample_count':n,
        'source_pts_first':float(pts[0]),'source_pts_last':float(pts[-1]),'observed_sample_rate_hz':float(fs),
        'method1_candidate_signed_rpm':float(slope),'method2_pattern_spectrum_candidate_abs_rpm':float(spectral_rpm),
        'spectrum_bin_width_hz':float(fs/n),'spectral_rpm_bin_width':float(fs/n*60/args.harmonic),
        'alias_rpm_spacing':float(fs/args.harmonic*60),'principal_alias_rpm_limit':float(fs/args.harmonic*30),
        'physical_rpm':None,'physical_direction':None,'physical_paddle_ids':None,
        'signal_note':'Threefold white/gray appearance amid moving balls. Symmetry, camera stability, feature identity, and alias branch are not independently verified. Values cannot be reported as machine RPM.',
        'ball_detections':len(balls),'ball_identity':'unknown; rows are unlinked color-component candidates, not tracked balls',
        'occlusion':'unknown; no hidden center or trajectory imputed','frames_saved':False,'source_video_sha256':None,
        'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'transport':transport}
    (out/(prefix+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
