"""Extract native-PTS samples and review sheets from a pinned local video clip.

PNG evidence contains unmodified full native frames or the explicitly logged crop.
Contact sheets are reduced inspection aids; they are never angle inputs.
"""
import argparse, csv, hashlib, json, math, re, subprocess
from pathlib import Path
from fractions import Fraction
import cv2, numpy as np
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--tag',required=True)
    p.add_argument('--start',type=float,required=True);p.add_argument('--duration',type=float,required=True)
    p.add_argument('--every',type=int,default=30);p.add_argument('--crop',type=int,nargs=4)
    p.add_argument('--width',type=int,default=480);p.add_argument('--cols',type=int,default=3)
    p.add_argument('--rows',type=int,default=8)
    p.add_argument('--native',action='store_true');a=p.parse_args()
    folder=ROOT/'evidence'/a.tag
    if folder.exists():raise SystemExit('Refuse overwrite')
    folder.mkdir(parents=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(a.input)]))['streams'][0]
    w,h=probe['width'],probe['height']
    if a.crop:x,y,w,h=a.crop
    sw=a.width;sh=round(sw*h/w)
    if a.native:ow,oh=w,h
    else:ow,oh=sw,sh
    crop=f'crop={w}:{h}:{a.crop[0]}:{a.crop[1]},' if a.crop else ''
    scale='' if a.native else f'scale={ow}:{oh},'
    count=math.ceil(a.duration*float(Fraction(probe['avg_frame_rate']))/a.every)
    vf=f'select=not(mod(n\\,{a.every})),showinfo,{crop}{scale}format=bgr24'
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','info','-seek_timestamp','1','-ss',str(a.start),'-copyts','-i',str(a.input),'-an','-vf',vf,'-frames:v',str(count),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','pipe:1']
    r=subprocess.run(cmd,capture_output=True,timeout=180)
    pts=[float(v) for v in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)',r.stderr.decode(errors='replace'))]
    n=len(r.stdout)//(ow*oh*3);pts=pts[:n]
    if r.returncode or n!=count or len(pts)!=n:raise RuntimeError(f'incomplete extraction {n}/{count}')
    ims=np.frombuffer(r.stdout,np.uint8).reshape(n,oh,ow,3)
    rows=[];cells=[];sheets=[]
    for i,(t,im) in enumerate(zip(pts,ims)):
        name=f'pts_{t:.6f}.png';file=folder/name
        # Native crops used for dense reviews can be very large; save explicitly.
        cv2.imwrite(str(file),im)
        rows.append({'sample_index':i,'source_pts_seconds':t,'relative_native_index':i*a.every,'file':str(file.relative_to(ROOT)).replace('\\','/'),
                     'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'bgr_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':ow,'height':oh})
        cell=cv2.resize(im,(sw,sh),interpolation=cv2.INTER_AREA)
        cv2.putText(cell,f'{a.tag} PTS {t:.6f}',(5,18),cv2.FONT_HERSHEY_SIMPLEX,.43,(0,255,255),1)
        cells.append(cell)
        if len(cells)==a.cols*a.rows or i==n-1:
            while len(cells)%a.cols:cells.append(np.zeros_like(cell))
            sheet=np.vstack([np.hstack(cells[j:j+a.cols]) for j in range(0,len(cells),a.cols)])
            sn=folder/f'sheet_{len(sheets):03d}.jpg';cv2.imwrite(str(sn),sheet,[cv2.IMWRITE_JPEG_QUALITY,82]);sheets.append(str(sn));cells=[]
    with (folder/'frames.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    log={'input_file':str(a.input),'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'arguments':vars(a)|{'input':str(a.input)},
         'count':n,'first_pts':pts[0],'last_pts':pts[-1],'native_pixels':a.native,'source_dimensions':[probe['width'],probe['height']],
         'output_dimensions':[ow,oh],'source_avg_frame_rate':probe['avg_frame_rate'],'pts_origin':'source rendition; packet-copy clip; seek_timestamp=1',
         'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sheets':sheets}
    (folder/'extraction.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    print(json.dumps({k:log[k] for k in ['count','first_pts','last_pts','sheets']}))
if __name__=='__main__':main()
