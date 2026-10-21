"""Anonymous circle detections and conservative short tracks in an authorized file.

Outputs candidate collector events only. No result number/OCR, no 3D inference.
Any ambiguity or missed detection ends a track; no interpolation of hidden balls.
"""
import argparse,json
from pathlib import Path
import cv2,numpy as np
from scipy.optimize import linear_sum_assignment
from common import read_csv,write_csv,BALLS

def associate(previous,current,max_displacement,ambiguity_margin):
    if not previous or not current:return {}
    a=np.asarray(previous);b=np.asarray(current)
    d=np.linalg.norm(a[:,None,:2]-b[None,:,:2],axis=2)
    r,c=linear_sum_assignment(d);pairs={}
    for i,j in zip(r,c):
        if d[i,j]>max_displacement:continue
        row=np.sort(d[i]);col=np.sort(d[:,j])
        if (len(row)>1 and row[1]-row[0]<ambiguity_margin) or (len(col)>1 and col[1]-col[0]<ambiguity_margin):continue
        pairs[int(j)]=int(i)
    return pairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('video',type=Path);ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--draw-id',required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--start-frame',type=int,required=True);ap.add_argument('--end-frame',type=int,required=True)
    ap.add_argument('--roi',type=int,nargs=4,required=True,metavar=('X','Y','W','H'))
    ap.add_argument('--radius',type=int,nargs=2,required=True);ap.add_argument('--gate-px',type=float,required=True)
    ap.add_argument('--ambiguity-px',type=float,default=3);ap.add_argument('--hough-threshold',type=float,default=25)
    args=ap.parse_args()
    if args.out.exists():raise SystemExit('Refusing overwrite')
    if args.start_frame<0 or args.end_frame<args.start_frame or min(args.radius)<=0 or args.radius[0]>args.radius[1]:raise SystemExit('Invalid range')
    times={int(r['frame_index']):float(r['timestamp_seconds']) for r in read_csv(args.manifest)}
    x,y,w,h=args.roi
    if x<0 or y<0 or w<=0 or h<=0:raise SystemExit('Invalid ROI')
    cap=cv2.VideoCapture(str(args.video));n=0;prev=[];ids=[];next_id=0;rows=[]
    try:
        while n<=args.end_frame:
            ok,im=cap.read()
            if not ok:raise RuntimeError('Incomplete native decode before requested end')
            if n>=args.start_frame:
                if n not in times:raise RuntimeError('PTS map missing frame')
                if x+w>im.shape[1] or y+h>im.shape[0]:raise RuntimeError('ROI outside image')
                gray=cv2.cvtColor(im[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY)
                circles=cv2.HoughCircles(cv2.GaussianBlur(gray,(5,5),1),cv2.HOUGH_GRADIENT,1,
                    minDist=max(2,2*args.radius[0]),param1=100,param2=args.hough_threshold,minRadius=args.radius[0],maxRadius=args.radius[1])
                cur=[] if circles is None else [[float(a+x),float(b+y),float(r)] for a,b,r in circles[0]]
                pairs=associate(prev,cur,args.gate_px,args.ambiguity_px);curids=[]
                for j,c in enumerate(cur):
                    if j in pairs:tid=ids[pairs[j]]
                    else:tid=f'anonymous_{next_id:06d}';next_id+=1
                    curids.append(tid)
                    rows.append(dict(zip(BALLS,[args.draw_id,times[n],n,tid,*c,None,False])))
                prev,ids=cur,curids
            n+=1
    finally:cap.release()
    write_csv(args.out,BALLS,rows)
    args.out.with_suffix('.method.json').write_text(json.dumps({'status':'unvalidated_candidates','physical_ball_identity':'unknown',
        'coordinate_space':'full_source_pixels','hidden_positions_imputed':False,'roi':args.roi,'radius_range_px':args.radius,
        'gate_px':args.gate_px,'ambiguity_px':args.ambiguity_px,'hough_threshold':args.hough_threshold,
        'warning':'Hough detections include reflections and partial circles; manual review required. No mechanical events asserted.'},indent=2),encoding='utf-8')
if __name__=='__main__':main()
