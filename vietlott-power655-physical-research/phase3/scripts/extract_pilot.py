"""Extract real native samples from SHA-pinned Phase 2 video; never label numbers."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT.parent / 'phase2'

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def extract(source, start, count, every, target):
    target.mkdir(parents=True, exist_ok=False)
    vf = f'select=not(mod(n\\,{every})),showinfo,format=bgr24'
    cmd = ['ffmpeg','-nostdin','-hide_banner','-loglevel','info','-seek_timestamp','1',
           '-ss',str(start),'-copyts','-i',source['input_file_local_only'],'-an','-vf',vf,
           '-frames:v',str(count),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','pipe:1']
    r = subprocess.run(cmd, capture_output=True, timeout=90)
    (target/'ffmpeg.log').write_bytes(r.stderr)
    pts = re.findall(rb'\bn:\s*\d+\s+pts:\s*(-?\d+)\s+pts_time:([0-9.e+\-]+)',r.stderr)
    size = 1920*1080*3
    if r.returncode or len(r.stdout) != count*size or len(pts)<count:
        raise RuntimeError(f'incomplete decode: {target}')
    frames = np.frombuffer(r.stdout,np.uint8).reshape(count,1080,1920,3)
    rows=[]
    for i, (frame,(ticks,seconds)) in enumerate(zip(frames,pts)):
        path=target/f'frame_{i:02d}.png'
        if not cv2.imwrite(str(path),frame): raise RuntimeError('PNG write failed')
        rows.append(dict(sample_index=i,source_id=source['source_id'],source_sha256=source['video_sha256'],
                         pts_ticks=int(ticks),pts_time_base='1/30000',source_pts_seconds=seconds.decode(),
                         evidence_image_path=path.relative_to(ROOT).as_posix(),evidence_sha256=sha(path),
                         bgr_sha256=hashlib.sha256(frame.tobytes()).hexdigest(),width=1920,height=1080))
    write_csv(target/'frames.csv',rows)
    (target/'extraction.json').write_text(json.dumps(dict(command=cmd,source_sha256=source['video_sha256'],
        created_utc=datetime.now(timezone.utc).isoformat(),native_pixels=True,script_sha256=sha(__file__),
        analysis_plan_sha256=sha(ROOT/'analysis_plan.md'),ffmpeg_version=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]),indent=2))
    # A native full frame remains the evidence; below is only an annotated crop viewing aid.
    cells=[]
    for row,frame in zip(rows,frames):
        cell=cv2.resize(frame[500:980,180:1880],(850,240),interpolation=cv2.INTER_AREA)
        cv2.putText(cell,f"{target.name} PTS {row['source_pts_seconds']}",(8,22),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,255,255),1)
        cells.append(cell)
    sheet=np.vstack([np.hstack(cells[i:i+2]) for i in range(0,len(cells),2)]) if count%2==0 else np.vstack(cells)
    cv2.imwrite(str(target/'sheet.jpg'),sheet,[cv2.IMWRITE_JPEG_QUALITY,94])
    return rows

def main():
    p=argparse.ArgumentParser(); p.add_argument('--draw-id'); p.add_argument('--capture',type=int)
    p.add_argument('--offset',type=float,default=2.0); p.add_argument('--count',type=int,default=6)
    p.add_argument('--every',type=int,default=15); p.add_argument('--tag',default='pilot_v1'); a=p.parse_args()
    sources={s['draw_id']:s for s in read_csv(P2/'phase2_sources.csv')}
    captures=read_csv(P2/'capture_event_audit.csv')
    checked={}; all_rows=[]
    for c in captures:
        if a.draw_id and c['draw_id'] != a.draw_id: continue
        if a.capture and int(c['capture_index']) != a.capture: continue
        s=sources[c['draw_id']]
        if s['source_id'] not in checked:
            actual=sha(s['input_file_local_only'])
            if actual != s['video_sha256']: raise RuntimeError('Source SHA256 mismatch; stop')
            checked[s['source_id']]=actual
        target=ROOT/'evidence'/a.tag/f"draw{c['draw_id']}_capture{int(c['capture_index']):02d}"
        start=float(c['trough_entry_visible_proxy_upper_pts'])+a.offset
        rows=extract(s,start,a.count,a.every,target)
        all_rows.extend(rows)
        print(f"{target.name}: {len(rows)} real frames",flush=True)
    (ROOT/'evidence'/f'{a.tag}_source_check.json').write_text(json.dumps(checked,indent=2))

if __name__=='__main__': main()
