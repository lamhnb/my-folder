"""Read public video into volatile memory, decode with ffmpeg stdin, no media files.

Reduced preview images are inspection only; never accepted by measurement tools.
"""
import argparse,base64,json,subprocess,urllib.request,datetime,hashlib,time
from pathlib import Path
import numpy as np, cv2
from inspect_stream import metadata,stream_url
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--limit-mb',type=int,default=16);ap.add_argument('--frames',type=int,nargs='+',default=[0,300,600]);args=ap.parse_args()
    info,clean=metadata(args.video_id);fmt=stream_url(info)
    log={'video_id':args.video_id,'format_id':fmt['format_id'],'width':fmt.get('width'),'height':fmt.get('height'),'fps_reported':fmt.get('fps'),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'media_saved':False}
    start=time.monotonic()
    try:
        req=urllib.request.Request(fmt['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=25) as r: raw=r.read(args.limit_mb*1024*1024)
        log['bytes_in_memory']=len(raw);log['sha256_memory_buffer']=hashlib.sha256(raw).hexdigest()
        expr='+'.join('eq(n\\,'+str(n)+')' for n in args.frames)
        p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i','pipe:0','-vf',f'select={expr},scale=640:360','-fps_mode','passthrough','-frames:v',str(len(args.frames)),'-f','rawvideo','-pix_fmt','bgr24','pipe:1'],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=55)
        log['ffmpeg_exit_code']=p.returncode;log['decoder_stderr']=p.stderr.decode(errors='replace')[-1000:]
        count=len(p.stdout)//(640*360*3);log['preview_frames_decoded']=count
        if count:
            ims=np.frombuffer(p.stdout[:count*640*360*3],np.uint8).reshape(count,360,640,3).copy()
            for i,im in enumerate(ims):cv2.putText(im,f'{args.video_id} decoded n={args.frames[i]}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,255,255),1)
            rows=[]
            for i in range(0,count,2):rows.append(np.hstack([ims[i],ims[i+1] if i+1<count else np.zeros_like(ims[i])]))
            encoded=base64.b64encode(cv2.imencode('.jpg',np.vstack(rows))[1]).decode()
        else:encoded=None
    except subprocess.TimeoutExpired:log.update(error='ffmpeg pipe decoding timeout',preview_frames_decoded=0);encoded=None
    except Exception as e:log.update(error_type=type(e).__name__,preview_frames_decoded=0);encoded=None
    log['elapsed_seconds']=time.monotonic()-start
    (ROOT/'evidence'/f'{args.video_id}_memory_decode.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    if encoded:log['image_base64']=encoded
    print(json.dumps(log))
if __name__=='__main__':main()
