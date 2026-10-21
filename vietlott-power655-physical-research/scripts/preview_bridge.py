import argparse,base64,json,subprocess,datetime,re
from pathlib import Path
import numpy as np,cv2
from inspect_stream import metadata,stream_url
from media_bridge import Bridge
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--times',type=float,nargs='+',required=True);args=ap.parse_args()
    info,_=metadata(args.video_id);f=stream_url(info);ims=[];logs=[]
    with Bridge(f['url']) as bridge:
        for t in args.times:
            try:
                p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-rw_timeout','20000000','-ss',str(t),'-i',bridge.url,'-frames:v','1','-vf','scale=640:360','-f','image2pipe','-c:v','png','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
                im=cv2.imdecode(np.frombuffer(p.stdout,np.uint8),cv2.IMREAD_COLOR) if p.stdout else None
                log={'seek_seconds':t,'ffmpeg_exit_code':p.returncode,'decoded':im is not None,'stderr':p.stderr.decode(errors='replace')[-500:]}
                if im is not None:
                    cv2.putText(im,f'{args.video_id} seek={t:.3f}s approx',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,255,255),1);ims.append(im)
            except subprocess.TimeoutExpired:log={'seek_seconds':t,'decoded':False,'error':'timeout45s'}
            logs.append(log)
        result={'video_id':args.video_id,'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'media_saved':False,'frames':logs,'bytes_sent':bridge.bytes_sent,'transport_errors':bridge.errors}
    folder=ROOT/'evidence'/'access';folder.mkdir(parents=True,exist_ok=True)
    tag=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    (folder/f'{args.video_id}_{tag}_bridge_preview.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    if ims:
        if len(ims)%2:ims.append(np.zeros_like(ims[0]))
        contact=np.vstack([np.hstack(ims[i:i+2]) for i in range(0,len(ims),2)])
        # Compact inspection rendering; never used as a measurement input.
        contact=cv2.resize(contact,(768,int(contact.shape[0]*768/contact.shape[1])),interpolation=cv2.INTER_AREA)
        result['image_base64']=base64.b64encode(cv2.imencode('.jpg',contact,[cv2.IMWRITE_JPEG_QUALITY,45])[1]).decode()
    print(json.dumps(result))
if __name__=='__main__':main()
