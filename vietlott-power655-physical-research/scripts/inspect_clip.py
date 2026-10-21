"""PTS-labelled in-memory contact sheet and hash ledger of real decoded frames.

Samples retain native PTS; preview downsizing is never a measurement input.
No video, audio or frame image is written to disk. Scalar hashes/PTS only.
"""
import argparse,base64,datetime,hashlib,json,re,subprocess
from pathlib import Path
import cv2,numpy as np
from inspect_stream import metadata,stream_url
from media_bridge import Bridge
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--start',type=float,required=True)
    ap.add_argument('--duration',type=float,required=True);ap.add_argument('--every',type=int,default=60)
    ap.add_argument('--cell-width',type=int,default=320);ap.add_argument('--cols',type=int,default=4)
    ap.add_argument('--crop',type=int,nargs=4)
    args=ap.parse_args();info,_=metadata(args.video_id);f=stream_url(info)
    width=args.cell_width;height=round(width*(args.crop[3]/args.crop[2] if args.crop else 9/16))
    if args.every<1 or args.duration<=0:raise SystemExit('Invalid sampling')
    with Bridge(f['url']) as b:
        # -copyts preserves source PTS; -frames bounds selected output instead of rebasing time.
        count=int(args.duration*float(f['fps'])/args.every)+1
        crop_filter=(f'crop={args.crop[2]}:{args.crop[3]}:{args.crop[0]}:{args.crop[1]},') if args.crop else ''
        p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-rw_timeout','20000000',
            '-ss',str(args.start),'-copyts','-i',b.url,'-an','-vf',f'select=not(mod(n\\,{args.every})),showinfo,{crop_filter}scale={width}:{height}',
            '-fps_mode','passthrough','-frames:v',str(count),'-f','rawvideo','-pix_fmt','bgr24','pipe:1'],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240)
        stderr=p.stderr.decode(errors='replace')
        pts=[float(x) for x in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)',stderr)]
        n=len(p.stdout)//(width*height*3);pts=pts[:n]
        if n!=len(pts):raise RuntimeError('Frame/PTS mismatch')
        ims=np.frombuffer(p.stdout,np.uint8).reshape(n,height,width,3).copy()
        log={'video_id':args.video_id,'requested_start':args.start,'duration_requested':args.duration,'source_format_id':f['format_id'],
            'source_width':f.get('width'),'source_height':f.get('height'),'fps_metadata':f.get('fps'),'frames_decoded':n,
            'frame_index_global':None,'frame_index_note':'Global native index not verified; PTS is the primary source locator.',
            'sampling_every_native_frames':args.every,'media_saved':False,'ffmpeg_exit_code':p.returncode,
            'preview_width':width,'preview_height':height,'crop_source_pixels':args.crop,
            'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'transport_errors':b.errors,'bytes_sent':b.bytes_sent,
            'samples':[{'source_pts_seconds':t,'preview_bgr_sha256':hashlib.sha256(im.tobytes()).hexdigest()} for t,im in zip(pts,ims)]}
        log['status']='decoded' if p.returncode==0 and n==count else 'decode_failed_or_incomplete'
        if p.returncode:log['decoder_error']=re.sub(r'https?://\S+','[URL]',stderr[-1500:])
    folder=ROOT/'evidence'/'clips';folder.mkdir(parents=True,exist_ok=True)
    tag=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    (folder/f'{args.video_id}_{args.start:g}_{tag}.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    # Independent sheets of 24 retain readable source PTS labels.
    for begin in range(0,n,24):
        cells=[]
        for i in range(begin,min(begin+24,n)):
            im=ims[i];cv2.putText(im,f'PTS {pts[i]:.6f}s',(5,18),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,255,255),1);cells.append(im)
        while len(cells)%args.cols:cells.append(np.zeros_like(cells[0]))
        sheet=np.vstack([np.hstack(cells[i:i+args.cols]) for i in range(0,len(cells),args.cols)])
        encoded=base64.b64encode(cv2.imencode('.jpg',sheet,[cv2.IMWRITE_JPEG_QUALITY,45])[1]).decode()
        print(json.dumps({'video_id':args.video_id,'sheet_first_sample':begin,'image_base64':encoded}),flush=True)
    print(json.dumps({'video_id':args.video_id,'status':log['status'],'sample_count':n,'first_pts':pts[0] if pts else None,'last_pts':pts[-1] if pts else None,'log':str(folder.name+'/'+args.video_id+'_'+str(args.start))}),flush=True)
if __name__=='__main__':main()
