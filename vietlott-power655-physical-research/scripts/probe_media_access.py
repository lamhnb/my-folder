"""Bounded public resource diagnostics, no media persistence or authentication."""
import argparse, base64, json, urllib.request, urllib.error, datetime
from pathlib import Path
import cv2, numpy as np
from inspect_stream import metadata, stream_url
ROOT=Path(__file__).resolve().parents[1]

def fetch(url,limit):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=12) as r:
            b=r.read(limit)
            return {'status':r.status,'content_type':r.headers.get('Content-Type'),'bytes_read':len(b)},b
    except urllib.error.HTTPError as e:return {'status':e.code,'error':'HTTPError'},None
    except Exception as e:return {'status':None,'error_type':type(e).__name__},None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    info,_=metadata(args.video_id);formats=info['formats'];results=[];preview=None
    f=stream_url(info);r,_=fetch(f['url'],1024);r.update(kind='video_https',format_id=f['format_id']);results.append(r)
    hls=[f for f in formats if f.get('protocol')=='m3u8_native' and f.get('height')==1080]
    if hls:
        r,_=fetch(hls[-1]['url'],2048);r.update(kind='hls_manifest',format_id=hls[-1]['format_id']);results.append(r)
    sb=[f for f in formats if f.get('format_note')=='storyboard']
    if sb:
        f=sb[-1];frag=f.get('fragments',[{}])[0];url=frag.get('url',f['url'])
        r,b=fetch(url,8_000_000);r.update(kind='storyboard',format_id=f['format_id'],thumbnail_width=f.get('width'),thumbnail_height=f.get('height'),fps=f.get('fps'))
        results.append(r)
        if b and args.preview:
            im=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_COLOR)
            if im is not None:preview=base64.b64encode(cv2.imencode('.jpg',im)[1]).decode()
    log={'video_id':args.video_id,'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resources':results}
    (ROOT/'evidence'/f'{args.video_id}_access.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    if preview:log['image_base64']=preview
    print(json.dumps(log))
if __name__=='__main__':main()
