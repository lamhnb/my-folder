"""Authorized local source -> lossless selected PNGs and complete original PTS map.

No FPS conversion, interpolation, enhancement or audio modification.
Frame 0 is the first decoded display frame in this file, not a broadcaster frame.
"""
import argparse,json
from pathlib import Path
import cv2,numpy as np
from common import digest,probe,frame_pts,write_csv
def main():
    ap=argparse.ArgumentParser();ap.add_argument('video',type=Path);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--indices',type=int,nargs='+',required=True);ap.add_argument('--rights-confirmed',action='store_true',required=True)
    args=ap.parse_args()
    if args.out.exists():raise SystemExit('Output must be new: refusing to overwrite prior evidence')
    if min(args.indices)<0:raise SystemExit('Negative index')
    meta=probe(args.video);pts=frame_pts(args.video)
    if not pts or np.any(np.diff(pts)<=0):raise SystemExit('Missing/nonmonotonic PTS; audit source before continuing')
    if max(args.indices)>=len(pts):raise SystemExit('Frame index outside PTS map')
    args.out.mkdir(parents=True);wanted=set(args.indices);cap=cv2.VideoCapture(str(args.video));n=0;records=[]
    try:
        while True:
            ok,im=cap.read()
            if not ok:break
            if n>=len(pts):raise RuntimeError('Decoder/ffprobe frame count mismatch')
            file=None;sha=None
            if n in wanted:
                file=f'frame_{n:08d}.png'
                if not cv2.imwrite(str(args.out/file),im):raise RuntimeError('Image write failed')
                sha=digest(args.out/file)
            records.append({'frame_index':n,'timestamp_seconds':pts[n]-pts[0],'absolute_pts_seconds':pts[n],
                            'evidence_frame':file,'sha256':sha,'width':im.shape[1],'height':im.shape[0]});n+=1
    finally:cap.release()
    if n!=len(pts):raise RuntimeError('Incomplete decode: output cannot be treated as complete evidence')
    write_csv(args.out/'frame_manifest.csv',list(records[0]),records)
    meta['input_basename']=args.video.name;meta['sha256']=digest(args.video)
    meta['frame_count_verified']=n;meta['fps_changed']=False;meta['relative_time_origin_pts']=pts[0]
    (args.out/'video_probe.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps({'status':'extracted','verified_frames':n,'saved_frames':len(wanted),'sha256':meta['sha256']}))
if __name__=='__main__':main()
