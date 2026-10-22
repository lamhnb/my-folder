"""Extract existing pinned local footage for ID inspection; pixels stay outside Git.
Uses native PTS, no AI enhancement, no OCR guesses or interpolated frames.
"""
import csv, hashlib, json, math, re, subprocess
from pathlib import Path
import cv2, numpy as np
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parents[1]
MEDIA=Path('C:/vietlott-research-output/physical-audit-20261022')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def main():
    if MEDIA.exists():raise SystemExit('Refuse overwrite: '+str(MEDIA))
    MEDIA.mkdir()
    sources=list(csv.DictReader((ROOT/'vietlott-power655-physical-research/phase2/phase2_sources.csv').open(encoding='utf-8')))
    rows=[];logs=[]
    for src in sources:
        file=Path(src['input_file_local_only'])
        digest=sha(file)
        if digest!=src['video_sha256']:raise ValueError('source mismatch')
        folder=MEDIA/src['draw_id'];folder.mkdir()
        count=51;every=300;start=600
        vf=f'select=not(mod(n\\,{every})),showinfo,format=bgr24'
        cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','info','-seek_timestamp','1','-ss',str(start),'-copyts','-i',str(file),'-an','-vf',vf,'-frames:v',str(count),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','pipe:1']
        r=subprocess.run(cmd,capture_output=True,timeout=180)
        pts=[float(v) for v in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)',r.stderr.decode(errors='replace'))]
        n=len(r.stdout)//(1920*1080*3);pts=pts[:n]
        if r.returncode or n!=count or len(pts)!=n:raise RuntimeError(f'incomplete {n}')
        ims=np.frombuffer(r.stdout,np.uint8).reshape(n,1080,1920,3)
        cells=[]
        for i,(t,im) in enumerate(zip(pts,ims)):
            p=folder/f'pts_{t:.6f}.png';cv2.imwrite(str(p),im)
            rows.append(dict(draw_id=src['draw_id'],source_url=src['source_url'],source_sha256=digest,source_pts_seconds=t,local_frame_path=str(p),frame_sha256=sha(p),bgr_sha256=hashlib.sha256(im.tobytes()).hexdigest(),width=1920,height=1080,method='ffmpeg native select every 300 frames from seek 600; contact sheet resized only'))
            cell=cv2.resize(im,(384,216),interpolation=cv2.INTER_AREA)
            cv2.putText(cell,f"{src['draw_id']} PTS {t:.6f}",(5,16),cv2.FONT_HERSHEY_SIMPLEX,.42,(0,255,255),1)
            cells.append(cell)
            if len(cells)==24 or i==n-1:
                while len(cells)%3:cells.append(np.zeros_like(cell))
                sheet=np.vstack([np.hstack(cells[j:j+3]) for j in range(0,len(cells),3)])
                cv2.imwrite(str(folder/f'sheet_{i//24:02d}.jpg'),sheet);cells=[]
        logs.append(dict(draw_id=src['draw_id'],command=cmd[:-1]+['<rawvideo pipe>'],source_sha256=digest,count=n,first_pts=pts[0],last_pts=pts[-1]))
        print(json.dumps({k:logs[-1][k] for k in ['draw_id','count','first_pts','last_pts']}),flush=True)
    with (OUT/'extracted/identity_frame_manifest.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'extracted/identity_extraction.json').write_text(json.dumps(dict(script_sha256=sha(Path(__file__)),ffmpeg_version=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],logs=logs,rights='Local inspection only; no new footage pixels committed'),indent=2),encoding='utf-8')
if __name__=='__main__':main()
