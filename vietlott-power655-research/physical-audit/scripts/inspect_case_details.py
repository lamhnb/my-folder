"""Follow up visible POWER case labels; retain native frames locally only."""
import csv, hashlib, json, re, subprocess
from pathlib import Path
import cv2, numpy as np
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parents[1]
MEDIA=Path('C:/vietlott-research-output/physical-audit-20261022')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=list(csv.DictReader((ROOT/'vietlott-power655-physical-research/phase2/phase2_sources.csv').open(encoding='utf-8')))
    starts=[686,686,686,676,636];rows=[];logs=[]
    for src,start in zip(sources,starts):
        folder=MEDIA/src['draw_id']/'case_details'
        if folder.exists():raise ValueError('Refuse overwrite')
        folder.mkdir()
        cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','info','-seek_timestamp','1','-ss',str(start),'-copyts','-i',src['input_file_local_only'],'-an','-vf','select=not(mod(n\\,30)),showinfo,format=bgr24','-frames:v','12','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','pipe:1']
        r=subprocess.run(cmd,capture_output=True,timeout=90)
        pts=[float(v) for v in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)',r.stderr.decode(errors='replace'))][:12]
        if r.returncode or len(r.stdout)!=12*1920*1080*3 or len(pts)!=12:raise ValueError('Incomplete')
        ims=np.frombuffer(r.stdout,np.uint8).reshape(12,1080,1920,3);cells=[]
        for t,im in zip(pts,ims):
            p=folder/f'pts_{t:.6f}.png';cv2.imwrite(str(p),im)
            rows.append(dict(draw_id=src['draw_id'],source_url=src['source_url'],source_sha256=src['video_sha256'],source_pts_seconds=t,local_frame_path=str(p),frame_sha256=sha(p),bgr_sha256=hashlib.sha256(im.tobytes()).hexdigest(),width=1920,height=1080,method='ffmpeg select every 30 native frames; adaptive detail follow-up'))
            cell=cv2.resize(im,(640,360),interpolation=cv2.INTER_AREA);cv2.putText(cell,f"{src['draw_id']} {t:.6f}",(4,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),1);cells.append(cell)
        cv2.imwrite(str(folder/'sheet.jpg'),np.vstack([np.hstack(cells[i:i+3]) for i in range(0,12,3)]))
        logs.append(dict(draw_id=src['draw_id'],command=cmd,first_pts=pts[0],last_pts=pts[-1]))
    with (OUT/'extracted/case_frame_manifest.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'extracted/case_extraction.json').write_text(json.dumps(dict(logs=logs,script_sha256=sha(Path(__file__)),transforms='Contact sheets resized only; native full frames unmodified; optional crop+180 degree display is documented in visual_review.csv'),indent=2),encoding='utf-8')
    print('60 native detail frames extracted; no IDs inferred automatically')
if __name__=='__main__':main()
