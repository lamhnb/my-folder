"""Inspect publicly served media in memory. Never writes video or frame copies.

Only sanitized metadata is persisted; signed media URLs are never logged.
This is visual reconnaissance, not a frame-accurate measurement source.
"""
import argparse, base64, io, json, subprocess, sys, re
from pathlib import Path
import cv2
import numpy as np
import yt_dlp

ROOT = Path(__file__).resolve().parents[1]

class Quiet:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def metadata(video_id):
    with yt_dlp.YoutubeDL({'quiet': True, 'logger': Quiet(), 'skip_download': True,
                         'socket_timeout': 20, 'retries': 1, 'noplaylist': True}) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=' + video_id, download=False)
    keys = ['id','title','channel','channel_id','channel_url','uploader','uploader_id',
            'upload_date','release_date','release_timestamp','timestamp','duration',
            'license','availability','live_status','fps','width','height','webpage_url']
    clean = {k: info.get(k) for k in keys}
    clean['formats'] = [{k:f.get(k) for k in ['format_id','width','height','fps','vcodec','acodec','has_drm','protocol']}
                        for f in info.get('formats', []) if f.get('vcodec') != 'none']
    return info, clean

def stream_url(info, max_height=1080):
    choices = [f for f in info['formats'] if f.get('vcodec') not in ('none',None)
               and f.get('protocol') == 'https' and not f.get('has_drm')
               and (f.get('height') or 0) <= max_height]
    if not choices: raise RuntimeError('No public non-DRM HTTPS video format')
    # Prefer native H.264 for decoder compatibility, then highest size/rate.
    choices.sort(key=lambda f:(f.get('height') or 0, (f.get('vcodec') or '').startswith('avc'),f.get('tbr') or 0))
    return choices[-1]

def frame_at(url, seconds):
    try:
        p = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-rw_timeout','12000000','-ss',str(seconds),
            '-i',url,'-frames:v','1','-f','image2pipe','-c:v','png','pipe:1'],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25)
    except subprocess.TimeoutExpired:
        raise RuntimeError('Public stream decoding timed out (25s); no image decoded') from None
    if p.returncode or not p.stdout:
        # Do not include ffmpeg stderr: it can contain signed URLs and IP addresses.
        safe=re.sub(r'https?://\S+','[REDACTED_URL]',p.stderr.decode(errors='replace'))
        raise RuntimeError('Public stream decode failed, ffmpeg exit='+str(p.returncode)+' '+safe[-600:])
    im = cv2.imdecode(np.frombuffer(p.stdout,np.uint8),cv2.IMREAD_COLOR)
    if im is None: raise RuntimeError('PNG decode failed')
    return im

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('video_id'); ap.add_argument('--times', nargs='*',type=float,default=[])
    ap.add_argument('--metadata-only',action='store_true')
    args=ap.parse_args()
    info, clean=metadata(args.video_id)
    (ROOT/'evidence'/'metadata').mkdir(parents=True,exist_ok=True)
    (ROOT/'evidence'/'metadata'/f'{args.video_id}.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.metadata_only:
        print(json.dumps(clean,ensure_ascii=True)); return
    fmt=stream_url(info)
    ims=[]; errors=[]
    for t in args.times:
        try:
            im=frame_at(fmt['url'],t)
            im=cv2.resize(im,(640,360),interpolation=cv2.INTER_AREA)
            cv2.putText(im,f'{args.video_id} seek={t:.3f}s (approx)',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,255,255),1)
            ims.append(im)
        except Exception as e: errors.append({'seek_seconds':t,'error':str(e)})
    out={'video_id':args.video_id,'format_id':fmt['format_id'],'errors':errors,'frames_decoded':len(ims)}
    if ims:
        if len(ims)%2: ims.append(np.zeros_like(ims[0]))
        contact=np.vstack([np.hstack(ims[i:i+2]) for i in range(0,len(ims),2)])
        out['image_base64']=base64.b64encode(cv2.imencode('.jpg',contact)[1]).decode()
    print(json.dumps(out))

if __name__=='__main__': main()
